#!/usr/bin/env bash
set -euo pipefail

MC_VERSION="1.21.1"
LOADER="fabric"
LOADER_VERSION="0.19.5"

command -v jq >/dev/null
command -v curl >/dev/null
command -v zip >/dev/null

rm -rf build/client
mkdir -p build/client/mods
declare -A SEEN_VERSIONS=()

modrinth_slug() {
  case "$1" in
    worldweaver) echo "world-weaver" ;;
    common-storage-library) echo "common-storage-lib" ;;
    cristellib) echo "cristel-lib" ;;
    better-dungeons) echo "yungs-better-dungeons" ;;
    betterfortresses) echo "yungs-better-nether-fortresses" ;;
    bettermineshafts) echo "yungs-better-mineshafts" ;;
    betterstrongholds) echo "yungs-better-strongholds" ;;
    *) echo "$1" ;;
  esac
}

resolve_mod() {
  local slug="$(modrinth_slug "$1")"
  local wanted_version="${2:-}"
  local versions_json
  versions_json="$(curl -fsSL --retry 3 --retry-all-errors "https://api.modrinth.com/v2/project/$slug/version?game_versions=%5B%22$MC_VERSION%22%5D&loaders=%5B%22$LOADER%22%5D&include_changelog=false")"

  local version_id version_number
  if [[ -n "$wanted_version" ]]; then
    version_id="$(jq -r --arg v "$wanted_version" '
      [.[] | select(.version_number == $v or (.version_number | ltrimstr("v")) == $v)]
      | if length == 1 then .[0].id else empty end
    ' <<<"$versions_json")"

    if [[ -z "$version_id" ]]; then
      # Treat the pinned value as the base semantic version. Modrinth often
      # decorates it with loader/MC suffixes, e.g. 1.8.0-fabric-21.1.
      # Select the unique release whose version begins with that base and is
      # followed by a separator, preferring the first listed release if
      # multiple release builds share the same base.
      version_id="$(jq -r --arg v "$wanted_version" '
        ($v | split("+")[0]) as $base
        | [
            .[]
            | select(
                (.version_number | ltrimstr("v")) as $n
                | ($n == $base or ($n | startswith($base + "-")) or ($n | startswith($base + "+")) or ($n | endswith("-" + $base)) or ($n | endswith("+" + $base)))
              )
          ]
        | (map(select(.version_type == "release")) | if length > 0 then . else [] end)
        | .[0].id // empty
      ' <<<"$versions_json")"
    fi

    if [[ -z "$version_id" ]]; then
      echo "::error::Could not resolve compatible Modrinth version: $slug @ $wanted_version"
      jq -r '.[0:12][] | "  " + .version_number + " [" + .version_type + "] (" + .id + ")"' <<<"$versions_json" || true
      return 1
    fi
  else
    version_id="$(jq -r '
      [.[] | select(.status == "listed" and .version_type == "release")]
      | .[0].id // empty
    ' <<<"$versions_json")"
  fi

  if [[ -n "${SEEN_VERSIONS[$version_id]:-}" ]]; then
    return 0
  fi
  SEEN_VERSIONS[$version_id]=1

  local version_json
  version_json="$(curl -fsSL --retry 3 --retry-all-errors "https://api.modrinth.com/v2/version/$version_id")"
  version_number="$(jq -r '.version_number' <<<"$version_json")"
  echo "Resolving $slug @ ${wanted_version:-latest} -> $version_number"

  local primary filename
  primary="$(jq -r '[.files[] | select(.primary == true)][0].url // .files[0].url // empty' <<<"$version_json")"
  filename="$(jq -r '[.files[] | select(.primary == true)][0].filename // .files[0].filename // empty' <<<"$version_json")"
  [[ -n "$primary" && -n "$filename" ]] || {
    echo "::error::No downloadable file for $slug @ $version_number"
    return 1
  }

  echo "  -> $filename"
  curl -fL --retry 3 --retry-all-errors "$primary" -o "build/client/mods/$filename"

  while IFS=$'\t' read -r dep_project dep_version dep_type; do
    [[ -z "$dep_project" || "$dep_type" != "required" ]] && continue
    [[ -z "$dep_version" || "$dep_version" == "null" ]] && continue
    local dep_slug dep_ver
    dep_slug="$(curl -fsSL --retry 3 --retry-all-errors "https://api.modrinth.com/v2/project/$dep_project" | jq -r '.slug')"
    dep_ver="$(curl -fsSL --retry 3 --retry-all-errors "https://api.modrinth.com/v2/version/$dep_version" | jq -r '.version_number')"
    resolve_mod "$dep_slug" "$dep_ver"
  done < <(jq -r '.dependencies[]? | [.project_id // "", .version_id // "", .dependency_type // ""] | @tsv' <<<"$version_json")
}

while IFS='|' read -r slug version; do
  [[ -z "$slug" ]] && continue
  case "$slug" in
    #*) continue ;;
  esac
  resolve_mod "$slug" "$version"
done < modpack/mods.txt

find build/client/mods -type f -iname 'voicechat-*.jar' -delete

count="$(find build/client/mods -maxdepth 1 -type f -name '*.jar' | wc -l)"
echo "Client JAR count: $count"
test "$count" -gt 0

cat > build/client/README.txt <<EOF
Minecraft 1.21.1 Fabric $LOADER_VERSION
Generated automatically by GitHub Actions.
Mod versions are resolved through the Modrinth API.
Pinned versions use exact matches when available, otherwise compatible release metadata.
Required dependencies use their exact Modrinth version IDs.
Voice Chat is intentionally excluded.
EOF

cp modpack/modpack.yml build/client/modpack.yml

(
  cd build/client
  zip -qr ../minecraft-client-1.21.1-fabric.zip .
)

ls -lh build/minecraft-client-1.21.1-fabric.zip
