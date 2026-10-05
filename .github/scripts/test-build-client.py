#!/usr/bin/env python3
"""Offline integration test for the Modrinth client-pack resolver."""

from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse
import zipfile


ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = ROOT / ".github/scripts/build-client.sh"


def make_jar(project: str) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("fabric.mod.json", json.dumps({"id": project, "version": "test"}))
    return output.getvalue()


class FixtureServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self) -> None:
        self.jars = {
            name: make_jar(name.removesuffix(".jar"))
            for name in (
                "root.jar",
                "fallback.jar",
                "alias.jar",
                "dependency.jar",
                "transitive.jar",
                "voicechat.jar",
                "macaws.jar",
            )
        }
        self.requests: list[str] = []
        super().__init__(("127.0.0.1", 0), FixtureHandler)

    @property
    def origin(self) -> str:
        host, port = self.server_address
        return f"http://{host}:{port}"

    def version(
        self,
        *,
        version_id: str,
        project_id: str,
        version_number: str,
        filename: str,
        dependencies: list[dict[str, str | None]] | None = None,
        direct_file: str | None = None,
        project_slug: str | None = None,
        date: str = "2026-01-01T00:00:00Z",
    ) -> dict:
        file_bytes = self.jars[filename]
        return {
            "id": version_id,
            "project_id": project_id,
            "version_number": version_number,
            "version_type": "release",
            "status": "listed",
            "date_published": date,
            "game_versions": ["1.21.1"],
            "loaders": ["fabric"],
            "files": [
                {
                    "url": direct_file or f"{self.origin}/files/{filename}",
                    "filename": filename,
                    "primary": True,
                    "size": len(file_bytes),
                    "hashes": {
                        "sha512": hashlib.sha512(file_bytes).hexdigest(),
                        "sha1": hashlib.sha1(file_bytes).hexdigest(),
                    },
                }
            ],
            "dependencies": dependencies or [],
            **({"slug": project_slug} if project_slug else {}),
        }


class FixtureHandler(BaseHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        return

    @property
    def fixture(self) -> FixtureServer:
        return self.server  # type: ignore[return-value]

    def send_json(self, value: object, status: int = 200) -> None:
        payload = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_bytes(self, payload: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/java-archive")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        self.fixture.requests.append(self.path)

        if path.startswith("/files/"):
            filename = path.rsplit("/", 1)[-1]
            if filename in self.fixture.jars:
                self.send_bytes(self.fixture.jars[filename])
            else:
                self.send_json({"error": "not_found"}, 404)
            return

        if path.startswith("/cdn/data/"):
            filename = path.rsplit("/", 1)[-1]
            if filename in self.fixture.jars:
                self.send_bytes(self.fixture.jars[filename])
            else:
                self.send_json({"error": "not_found"}, 404)
            return

        if path.startswith("/v2/project/"):
            rest = path.removeprefix("/v2/project/")
            parts = rest.split("/")
            identifier = parts[0]
            if len(parts) == 3 and parts[1:] == ["version", ""]:
                # Defensive; normal paths have exactly two suffix components.
                pass
            if len(parts) == 2 and parts[1] == "version":
                query = parse_qs(parsed.query)
                game_versions = json.loads(query.get("game_versions", ["[]"])[0])
                loaders = json.loads(query.get("loaders", ["[]"])[0])
                if game_versions != ["1.21.1"] or loaders != ["fabric"]:
                    self.send_json({"error": "incorrect compatibility filter"}, 400)
                    return
                versions = self.versions_for(identifier)
                if versions is None:
                    self.send_json({"error": "not_found"}, 404)
                else:
                    self.send_json(versions)
                return

            project = {
                "root-mod": {"id": "rootProject", "slug": "root-mod"},
                "fallback-mod": {"id": "fallbackProject", "slug": "fallback-mod"},
                "common-storage-lib": {"id": "aliasProject", "slug": "common-storage-lib"},
                "rootProject": {"id": "rootProject", "slug": "root-mod"},
                "fallbackProject": {"id": "fallbackProject", "slug": "fallback-mod"},
                "aliasProject": {"id": "aliasProject", "slug": "common-storage-lib"},
            }.get(identifier)
            if project:
                self.send_json(project)
            else:
                self.send_json({"error": "not_found"}, 404)
            return

        if path.startswith("/v2/version/"):
            version_id = path.rsplit("/", 1)[-1]
            dependency = self.fixture.version(
                version_id="dep-v1",
                project_id="depProject",
                version_number="1.0.0",
                filename="dependency.jar",
                dependencies=[
                    {
                        "project_id": "nestedProject",
                        "version_id": None,
                        "dependency_type": "required",
                    }
                ],
            )
            voicechat = self.fixture.version(
                version_id="voice-v1",
                project_id="voicechatProject",
                version_number="2.5.0",
                filename="voicechat.jar",
            )
            if version_id == "dep-v1":
                self.send_json(dependency)
            elif version_id == "voice-v1":
                self.send_json(voicechat)
            else:
                self.send_json({"error": "not_found"}, 404)
            return

        self.send_json({"error": "not_found"}, 404)

    def versions_for(self, project_id: str) -> list[dict] | None:
        common_dependencies = [
            {
                "project_id": "depProject",
                "version_id": "dep-v1",
                "dependency_type": "required",
            },
            {
                "project_id": "voicechatProject",
                "version_id": "voice-v1",
                "dependency_type": "required",
            },
            {
                "project_id": "optionalProject",
                "version_id": None,
                "dependency_type": "optional",
            },
        ]
        if project_id == "rootProject":
            root = self.fixture.version(
                version_id="root-v1",
                project_id=project_id,
                version_number="3.4.0+fabric",
                filename="root.jar",
                dependencies=common_dependencies,
                direct_file=f"{self.fixture.origin}/files/missing-root.jar",
            )
            return [root]
        if project_id == "fallbackProject":
            return [
                self.fixture.version(
                    version_id="fallback-new",
                    project_id=project_id,
                    version_number="2.1.0",
                    filename="fallback.jar",
                    date="2026-05-01T00:00:00Z",
                ),
                self.fixture.version(
                    version_id="fallback-old",
                    project_id=project_id,
                    version_number="2.0.0",
                    filename="fallback.jar",
                    date="2025-01-01T00:00:00Z",
                ),
            ]
        if project_id == "aliasProject":
            return [
                self.fixture.version(
                    version_id="alias-v1",
                    project_id=project_id,
                    version_number="0.0.10",
                    filename="alias.jar",
                )
            ]
        if project_id == "nestedProject":
            return [
                self.fixture.version(
                    version_id="nested-v1",
                    project_id=project_id,
                    version_number="1.2.0",
                    filename="transitive.jar",
                )
            ]
        return None



def main() -> None:
    with tempfile.TemporaryDirectory(prefix="server-minecraft-test-") as temp_dir:
        manifest = Path(temp_dir) / "mods.txt"
        manifest.write_text(
            "root-mod|1.21.1-Fabric-3.4.0\n"
            "fallback-mod|99.99.99\n"
            "common-storage-library|0.0.10\n",
            encoding="utf-8",
        )

        server = FixtureServer()
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            env = os.environ.copy()
            env.update(
                {
                    "MODS_FILE": str(manifest),
                    "MODRINTH_API_BASE_URL": f"{server.origin}/v2",
                    "MODRINTH_CDN_BASE_URL": f"{server.origin}/cdn",
                }
            )
            result = subprocess.run(
                ["bash", str(BUILD_SCRIPT)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            if result.returncode != 0:
                raise SystemExit(
                    "Offline Modrinth integration test failed.\n"
                    f"--- stdout ---\n{result.stdout}\n"
                    f"--- stderr ---\n{result.stderr}"
                )

            archive_path = ROOT / "build/minecraft-client-1.21.1-fabric.zip"
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
            expected = {
                "mods/root.jar",
                "mods/fallback.jar",
                "mods/alias.jar",
                "mods/dependency.jar",
                "mods/transitive.jar",
                "mods/voicechat.jar",
                "README.txt",
                "modpack.yml",
            }
            missing = expected - names
            if missing:
                raise SystemExit(f"Client ZIP is missing expected entries: {sorted(missing)}")
            if "mods/optional.jar" in names:
                raise SystemExit("Optional dependencies must not be added as required mods")
            if "2.1.0" not in result.stderr:
                raise SystemExit("Unavailable pinned version did not fall back to a compatible release")
            if not any("/cdn/data/rootProject/versions/root-v1/root.jar" in req for req in server.requests):
                raise SystemExit("Canonical CDN fallback was not attempted after the file URL failed")

            print("Offline Modrinth integration test passed: version matching, compatible fallback,")
            print("slug aliases, transitive required dependencies, file verification, and ZIP creation.")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    main()
