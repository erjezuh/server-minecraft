#!/usr/bin/env python3
"""Construye los packs de cliente y servidor a partir de una resolución fijada.

Flujo:
  1. resolver.py --guardar build/resolucion.json   (requiere estado aprobado)
  2. construir.py --resolucion build/resolucion.json --salida build/

Genera:
  - build/<nombre>-<version>.mrpack  (importable en Modrinth App / Prism / MultiMC)
  - build/servidor/                   (mods de servidor+ambos, listo para comprimir/subir)
  - build/servidor.zip

No hace NADA si el manifiesto sigue en estado 'propuesto'.
"""

import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API = "https://api.modrinth.com/v2"
UA = {"User-Agent": "server-minecraft-construir/1.0 (+https://modrinth.com)"}

ENV_MRPACK = {
    "ambos": {"client": "required", "server": "required"},
    "cliente": {"client": "required", "server": "unsupported"},
    "servidor": {"client": "unsupported", "server": "required"},
}


def api_get(path: str):
    req = urllib.request.Request(API + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def sha512_de(path: Path) -> str:
    h = hashlib.sha512()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1024 * 256), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar(url: str, destino: Path, tamano: int | None = None, sha512: str | None = None):
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        ok = (not tamano or destino.stat().st_size == tamano)
        ok = ok and (not sha512 or sha512_de(destino) == sha512)
        if ok:
            return False  # ya estaba y cuadra
        destino.unlink()  # corrupto o distinto: re-descargar
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(destino, "wb") as f:
        while True:
            bloque = r.read(1024 * 256)
            if not bloque:
                break
            f.write(bloque)
    if tamano and destino.stat().st_size != tamano:
        destino.unlink()
        sys.exit(f"ERROR: {destino.name} descargado con tamaño incorrecto.")
    if sha512 and sha512_de(destino) != sha512:
        destino.unlink()
        sys.exit(f"ERROR: {destino.name} no cuadra su sha512 (descarga corrupta).")
    return True


def loader_fabric(mc: str, fijo: str | None) -> str:
    if fijo:
        return fijo
    req = urllib.request.Request(f"https://meta.fabricmc.net/v2/versions/loader/{mc}", headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.load(r)
    if not datos:
        sys.exit("ERROR: no se pudo averiguar la versión de Fabric Loader (pasa --fabric-loader).")
    return datos[0]["loader"]["version"]


def main():
    ap = argparse.ArgumentParser(description="Construye .mrpack + pack de servidor.")
    ap.add_argument("--manifiesto", default=str(RAIZ / "modpack" / "modpack.yml"))
    ap.add_argument("--resolucion", required=True)
    ap.add_argument("--salida", default=str(RAIZ / "build"))
    ap.add_argument("--fabric-loader", default=None, help="Fija versión (si no, usa la última estable).")
    args = ap.parse_args()

    try:
        import yaml
    except ImportError:
        sys.exit("ERROR: falta pyyaml. Instala con: pip install -r scripts/requirements.txt")
    m = yaml.safe_load(open(args.manifiesto, encoding="utf-8"))
    if m.get("estado_global") != "aprobado":
        sys.exit("⛔ El manifiesto sigue en estado 'propuesto'. Apruébalo antes de construir.")

    res = json.loads(open(args.resolucion, encoding="utf-8").read())
    assert res["minecraft"] == m["minecraft"] and res["loader"] == m["loader"], \
        "La resolución no cuadra con el manifiesto (¿cambió la versión?)."

    salida = Path(args.salida)
    mods_dir = salida / "descargas"
    ficheros_mrpack = []
    lado_por_fichero = {}

    print(f"Descargando {len(res['mods'])} mods de Modrinth...")
    for slug, pin in res["mods"].items():
        version = api_get(f"/version/{pin['version_id']}")
        candidatos = [f for f in version.get("files", []) if f.get("filename", "").endswith(".jar")]
        if not candidatos:
            sys.exit(f"ERROR: {slug} no tiene .jar en la versión fijada.")
        prim = next((f for f in candidatos if f.get("primary")), candidatos[0])
        destino = mods_dir / prim["filename"]
        nuevo = descargar(prim["url"], destino, prim.get("size"), prim.get("hashes", {}).get("sha512"))
        lado_por_fichero[prim["filename"]] = pin["lado"]
        print(f"  {'↓' if nuevo else '='} {prim['filename']} ({prim.get('size', 0) // 1024} KiB)")
        ficheros_mrpack.append({
            "path": f"mods/{prim['filename']}",
            "hashes": prim["hashes"],
            "env": ENV_MRPACK[pin["lado"]],
            "downloads": [prim["url"]],
            "fileSize": prim["size"],
        })

    # --- .mrpack para clientes (Modrinth App / Prism / MultiMC) ---
    nombre = f"{m.get('modpack_nombre', 'modpack')}-{m.get('modpack_version', '1.0.0')}"
    fijado = args.fabric_loader or res.get("fabric_loader")
    loader_v = fijado or loader_fabric(m["minecraft"], None)
    print(f"fabric-loader: {loader_v}" + (" (fijado)" if fijado else " (último estable; se registrará en el lockfile)"))
    indice = {"formatVersion": 1, "game": "minecraft", "versionId": m.get("modpack_version", "1.0.0"),
              "name": m.get("modpack_nombre", "modpack"),
              "dependencies": {"minecraft": m["minecraft"], "fabric-loader": loader_v},
              "files": sorted(ficheros_mrpack, key=lambda f: f["path"])}
    mrpack = salida / f"{nombre}.mrpack"
    with zipfile.ZipFile(mrpack, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("modrinth.index.json", json.dumps(indice, indent=2))
        z.writestr("overrides/LEEME.txt",
                   f"{nombre} — pack generado automáticamente. Asigna 3 GB de RAM (-Xmx3G).\n")
        n_cli = 0
        for f in sorted(mods_dir.glob("*.jar")):
            if lado_por_fichero.get(f.name, "ambos") == "servidor":
                continue  # el cliente no lleva mods exclusivos de servidor
            z.write(f, f"overrides/mods/{f.name}")
            n_cli += 1
    print(f"✔ Cliente: {mrpack} (fabric-loader {loader_v}, índice {len(ficheros_mrpack)} mods, {n_cli} .jar de cliente/ambos)")

    # --- Pack de servidor (sin mods exclusivos de cliente) ---
    srv = salida / "servidor"
    (srv / "mods").mkdir(parents=True, exist_ok=True)
    for f in mods_dir.glob("*.jar"):
        lado = lado_por_fichero.get(f.name, "ambos")
        if lado in ("servidor", "ambos"):
            (srv / "mods" / f.name).write_bytes(f.read_bytes())
    (srv / "LEEME.txt").write_text(
        f"{nombre} — pack de SERVIDOR.\n"
        f"Contiene solo mods de servidor+ambos ({len(list((srv/'mods').glob('*.jar')))} .jar).\n"
        "Requiere: Java 21, 4 GB de RAM, aceptar EULA de Mojang (eula.txt).\n"
        "Simple Voice Chat necesita el puerto UDP abierto (por defecto 24454).\n",
        encoding="utf-8")
    zsrv = salida / "servidor.zip"
    with zipfile.ZipFile(zsrv, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(srv.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(srv))
    print(f"✔ Servidor: {zsrv}")
    print("Hecho. Revisa el contenido antes de desplegar nada.")


if __name__ == "__main__":
    sys.exit(main())
