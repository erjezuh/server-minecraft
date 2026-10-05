#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

MC_VERSION="${MC_VERSION:-1.21.1}"
LOADER="${LOADER:-fabric}"
LOADER_VERSION="${LOADER_VERSION:-0.19.5}"
MODS_FILE="${MODS_FILE:-$ROOT_DIR/modpack/mods.txt}"
MODRINTH_API_BASE_URL="${MODRINTH_API_BASE_URL:-https://api.modrinth.com/v2}"
MODRINTH_CDN_BASE_URL="${MODRINTH_CDN_BASE_URL:-https://cdn.modrinth.com}"
API_USER_AGENT="server-minecraft-modpack-builder/1.0.0 (https://github.com/erjezuh/server-minecraft)"

CLIENT_DIR="$ROOT_DIR/build/client"
MODS_DIR="$CLIENT_DIR/mods"
API_CACHE_DIR="$ROOT_DIR/build/.modrinth-cache"
CLIENT_ZIP="$ROOT_DIR/build/minecraft-client-${MC_VERSION}-${LOADER}.zip"

for command_name in curl jq zip unzip sha256sum sha1sum sha512sum; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "::error::Required build command is missing: $command_name" >&2
    exit 1
  fi
done

if [[ ! -f "$MODS_FILE" ]]; then
  echo "::error::Mod manifest not found: $MODS_FILE" >&2
  exit 1
fi

rm -rf "$CLIENT_DIR" "$API_CACHE_DIR"
rm -f "$CLIENT_ZIP"
mkdir -p "$MODS_DIR" "$API_CACHE_DIR"

declare -A RESOLVED_PROJECTS=()
declare -A RESOLVED_VERSIONS=()

urlencode() {
  jq -nr --arg value "$1" '$value | @uri'
}

# Preserve the existing project-name aliases, but also try the manifest slug
# first and use Modrinth search as a fallback for newly renamed projects.
modrinth_slug() {
  case "$1" in
    worldweaver) echo "world-weaver" ;;
    common-storage-library) echo "common-storage-lib" ;;
    cristellib) echo "cristel-lib" ;;
    better-dungeons) echo "yungs-better-dungeons" ;;
    betterfortresses) echo "yungs-better-nether-fortresses" ;;
    bettermineshafts) echo "yungs-better-mineshafts" ;;
    betterstrongholds) echo "yungs-better-strongholds" ;;
    mcw-*) echo "macaws-${1#mcw-}" ;;
    *) echo "$1" ;;
  esac
}

# Returns JSON on stdout. A 404 is returned as status 4 so project lookup can
# try another known alias without treating it as a network/API outage.
api_get() {
  local url="$1"
  local cache_key cache_file response_file error_file http_status curl_status=0

  cache_key="$(printf '%s' "$url" | sha256sum | awk '{print $1}')"
  cache_file="$API_CACHE_DIR/$cache_key.json"
  if [[ -s "$cache_file" ]]; then
    cat "$cache_file"
    return 0
  fi

  response_file="$(mktemp "$API_CACHE_DIR/.response.XXXXXX")"
  error_file="${response_file}.stderr"
  http_status="$(curl \
    --fail --location --silent --show-error \
    --retry 4 --retry-delay 1 --retry-max-time 60 \
    --connect-timeout 20 --max-time 120 \
    --user-agent "$API_USER_AGENT" \
    --output "$response_file" --write-out '%{http_code}' \
    "$url" 2>"$error_file")" || curl_status=$?

  if [[ "$http_status" == "404" ]]; then
    rm -f "$response_file" "$error_file"
    return 4
  fi

  if [[ "$curl_status" -ne 0 || ! "$http_status" =~ ^2[0-9][0-9]$ ]]; then
    echo "::error::Modrinth API request failed (HTTP ${http_status:-unknown}, curl exit $curl_status): $url" >&2
    if [[ -s "$error_file" ]]; then
      sed 's/^/  /' "$error_file" >&2
    fi
    rm -f "$response_file" "$error_file"
    return 1
  fi

  if ! jq -e . "$response_file" >/dev/null 2>&1; then
    echo "::error::Modrinth returned invalid JSON for: $url" >&2
    rm -f "$response_file" "$error_file"
    return 1
  fi

  mv "$response_file" "$cache_file"
  rm -f "$error_file"
  cat "$cache_file"
}

project_json_for_slug() {
  local requested_slug="$1"
  local alias_slug candidate candidate_url project_json search_json hit_json
  local project_id rc
  local -a candidates=()
  declare -A tried=()

  alias_slug="$(modrinth_slug "$requested_slug")"
  candidates+=("$requested_slug")
  if [[ "$alias_slug" != "$requested_slug" ]]; then
    candidates+=("$alias_slug")
  fi

  for candidate in "${candidates[@]}"; do
    [[ -n "${tried[$candidate]:-}" ]] && continue
    tried[$candidate]=1
    candidate_url="$(urlencode "$candidate")"
    if project_json="$(api_get "$MODRINTH_API_BASE_URL/project/$candidate_url")"; then
      if jq -e '(.id | type == "string") and (.slug | type == "string")' >/dev/null <<<"$project_json"; then
        printf '%s\n' "$project_json"
        return 0
      fi
      echo "::warning::Modrinth project lookup for '$candidate' did not return an id and slug; trying another identifier." >&2
    else
      rc=$?
      if [[ "$rc" -ne 4 ]]; then
        return "$rc"
      fi
    fi
  done

  # Exact-slug search catches renamed projects without accepting a similarly
  # named result. A project is only selected when its normalized slug matches.
  local facets
  facets="$(jq -nr '[["project_type:mod"]] | @json | @uri')"
  for candidate in "${candidates[@]}"; do
    candidate_url="$(urlencode "$candidate")"
    if search_json="$(api_get "$MODRINTH_API_BASE_URL/search?query=$candidate_url&facets=$facets&limit=100")"; then
      hit_json="$(jq -c --arg candidate "$candidate" '
        def normalize: ascii_downcase | gsub("[^a-z0-9]"; "");
        [
          .hits[]?
          | select(.project_type == "mod")
          | select(((.slug // "") | normalize) == ($candidate | normalize))
        ][0] // empty
      ' <<<"$search_json")"
      if [[ -n "$hit_json" ]]; then
        project_id="$(jq -r '.project_id // .id // empty' <<<"$hit_json")"
        if [[ -n "$project_id" ]]; then
          if project_json="$(api_get "$MODRINTH_API_BASE_URL/project/$(urlencode "$project_id")")"; then
            printf '%s\n' "$project_json"
            return 0
          else
            rc=$?
            if [[ "$rc" -ne 4 ]]; then
              return "$rc"
            fi
          fi
        fi
      fi
    else
      rc=$?
      if [[ "$rc" -ne 4 ]]; then
        return "$rc"
      fi
    fi
  done

  echo "::error::Could not resolve Modrinth project '$requested_slug' (tried: ${candidates[*]})." >&2
  return 1
}

compatible_versions_for_project() {
  local project_id="$1"
  local encoded_mc encoded_loader versions_json

  encoded_mc="$(jq -nr --arg mc "$MC_VERSION" '[$mc] | @json | @uri')"
  encoded_loader="$(jq -nr --arg loader "$LOADER" '[$loader] | @json | @uri')"
  versions_json="$(api_get "$MODRINTH_API_BASE_URL/project/$(urlencode "$project_id")/version?game_versions=$encoded_mc&loaders=$encoded_loader")" || return $?

  if ! jq -e 'type == "array"' >/dev/null <<<"$versions_json"; then
    echo "::error::Modrinth returned a non-array version response for project $project_id." >&2
    return 1
  fi
  printf '%s\n' "$versions_json"
}

# Prints a wrapper with the selected version JSON and how it was chosen. Pins
# are preferred (exact, normalized, then release core match); if a
# pin no longer exists, the latest listed release compatible with MC/loader is
# chosen rather than aborting the whole pack.
choose_compatible_version() {
  local versions_json="$1"
  local wanted_version="$2"
  local selection

  if [[ -n "$wanted_version" ]]; then
    selection="$(jq -c --arg mc "$MC_VERSION" --arg loader "$LOADER" --arg wanted "$wanted_version" '
      def compatible:
        (.status // "listed") == "listed"
        and (((.game_versions // []) | index($mc)) != null)
        and (((.loaders // []) | index($loader)) != null);
      [
        .[]
        | select(compatible)
        | select((.version_number | ascii_downcase | sub("^v"; "")) == ($wanted | ascii_downcase | sub("^v"; "")))
      ]
      | sort_by(.date_published // "")
      | reverse
      | .[0] // empty
    ' <<<"$versions_json")"
    if [[ -n "$selection" ]]; then
      jq -cn --argjson version "$selection" '{version: $version, resolution: "exact"}'
      return 0
    fi

    selection="$(jq -c --arg mc "$MC_VERSION" --arg loader "$LOADER" --arg wanted "$wanted_version" '
      def compatible:
        (.status // "listed") == "listed"
        and (((.game_versions // []) | index($mc)) != null)
        and (((.loaders // []) | index($loader)) != null);
      def normalize_version:
        ascii_downcase
        | sub("^v"; "")
        | gsub("[[:space:]_]"; "-")
        | gsub("\\+"; "-")
        | gsub("-+"; "-");
      [
        .[]
        | select(compatible)
        | select(.version_number | normalize_version == ($wanted | normalize_version))
      ]
      | sort_by(.date_published // "")
      | reverse
      | .[0] // empty
    ' <<<"$versions_json")"
    if [[ -n "$selection" ]]; then
      jq -cn --argjson version "$selection" '{version: $version, resolution: "normalized"}'
      return 0
    fi

    selection="$(jq -c --arg mc "$MC_VERSION" --arg loader "$LOADER" --arg wanted "$wanted_version" '
      def compatible:
        (.status // "listed") == "listed"
        and (((.game_versions // []) | index($mc)) != null)
        and (((.loaders // []) | index($loader)) != null);
      def primary_core($text):
        ($text | ascii_downcase | sub("^v"; "") | sub("^mc"; "")) as $lower
        | ($mc | ascii_downcase) as $game_version
        | (if ($lower | startswith($game_version)) then $lower[($game_version | length):] else $lower end)
        | sub("^[^0-9]*"; "")
        | (try match("^[0-9]+(\\.[0-9]+){1,3}").string catch "");
      (primary_core($wanted)) as $core
      | if $core == "" then empty else
          ($core | split(".") | join("[.]")) as $core_pattern
          | [
              .[]
              | select(compatible and .version_type == "release")
              | select((.version_number | ascii_downcase | test("(^|[^0-9])" + $core_pattern + "($|[^0-9])")))
            ]
          | sort_by(.date_published // "")
          | reverse
          | .[0] // empty
        end
    ' <<<"$versions_json")"
    if [[ -n "$selection" ]]; then
      jq -cn --argjson version "$selection" '{version: $version, resolution: "compatible-pin"}'
      return 0
    fi
  fi

  selection="$(jq -c --arg mc "$MC_VERSION" --arg loader "$LOADER" '
    def compatible:
      (.status // "listed") == "listed"
      and (((.game_versions // []) | index($mc)) != null)
      and (((.loaders // []) | index($loader)) != null);
    [ .[] | select(compatible and .version_type == "release") ]
    | sort_by(.date_published // "")
    | reverse
    | .[0] // empty
  ' <<<"$versions_json")"
  if [[ -n "$selection" ]]; then
    jq -cn --argjson version "$selection" '{version: $version, resolution: "latest-compatible"}'
    return 0
  fi

  # Some small projects publish only beta/alpha builds. Use one only when the
  # API confirms it supports the requested game version and loader.
  selection="$(jq -c --arg mc "$MC_VERSION" --arg loader "$LOADER" '
    def compatible:
      (.status // "listed") == "listed"
      and (((.game_versions // []) | index($mc)) != null)
      and (((.loaders // []) | index($loader)) != null);
    [ .[] | select(compatible) ]
    | sort_by(.date_published // "")
    | reverse
    | .[0] // empty
  ' <<<"$versions_json")"
  if [[ -n "$selection" ]]; then
    jq -cn --argjson version "$selection" '{version: $version, resolution: "latest-compatible-prerelease"}'
    return 0
  fi

  return 1
}

canonical_cdn_url() {
  local project_id="$1"
  local version_id="$2"
  local filename="$3"
  local encoded_filename

  encoded_filename="$(urlencode "$filename")"
  printf '%s/data/%s/versions/%s/%s\n' \
    "${MODRINTH_CDN_BASE_URL%/}" "$project_id" "$version_id" "$encoded_filename"
}

download_file() {
  local url="$1"
  local filename="$2"
  local expected_sha512="$3"
  local expected_sha1="$4"
  local expected_size="$5"
  local destination="$MODS_DIR/$filename"
  local part_file error_file curl_status=0 actual_hash actual_size

  if [[ "$filename" == */* || "$filename" == *\\* || "$filename" == "." || "$filename" == ".." ]]; then
    echo "  -> refusing unsafe Modrinth filename: $filename" >&2
    return 1
  fi

  if [[ -e "$destination" ]]; then
    if [[ -n "$expected_sha512" ]]; then
      actual_hash="$(sha512sum "$destination" | awk '{print $1}')"
      if [[ "$actual_hash" == "$expected_sha512" ]]; then
        return 0
      fi
    elif [[ -n "$expected_sha1" ]]; then
      actual_hash="$(sha1sum "$destination" | awk '{print $1}')"
      if [[ "$actual_hash" == "$expected_sha1" ]]; then
        return 0
      fi
    fi
    echo "::error::Two different Modrinth files have the same destination name: $filename" >&2
    return 1
  fi

  part_file="$(mktemp "$MODS_DIR/.download.XXXXXX")"
  error_file="${part_file}.stderr"
  if curl \
    --fail --location --silent --show-error \
    --retry 4 --retry-delay 1 --retry-max-time 60 \
    --connect-timeout 20 --max-time 300 \
    --user-agent "$API_USER_AGENT" \
    --output "$part_file" "$url" 2>"$error_file"; then
    :
  else
    curl_status=$?
    echo "  -> download failed (curl exit $curl_status): $url" >&2
    if [[ -s "$error_file" ]]; then
      sed 's/^/     /' "$error_file" >&2
    fi
    rm -f "$part_file" "$error_file"
    return 1
  fi
  rm -f "$error_file"

  if [[ ! -s "$part_file" ]]; then
    echo "  -> Modrinth returned an empty file for $filename" >&2
    rm -f "$part_file"
    return 1
  fi

  if [[ "$expected_size" =~ ^[0-9]+$ ]]; then
    actual_size="$(stat -c '%s' "$part_file")"
    if [[ "$actual_size" != "$expected_size" ]]; then
      echo "  -> size mismatch for $filename (expected $expected_size, got $actual_size)" >&2
      rm -f "$part_file"
      return 1
    fi
  fi

  if [[ -n "$expected_sha512" ]]; then
    actual_hash="$(sha512sum "$part_file" | awk '{print $1}')"
    if [[ "$actual_hash" != "$expected_sha512" ]]; then
      echo "  -> SHA-512 mismatch for $filename" >&2
      rm -f "$part_file"
      return 1
    fi
  elif [[ -n "$expected_sha1" ]]; then
    actual_hash="$(sha1sum "$part_file" | awk '{print $1}')"
    if [[ "$actual_hash" != "$expected_sha1" ]]; then
      echo "  -> SHA-1 mismatch for $filename" >&2
      rm -f "$part_file"
      return 1
    fi
  fi

  if ! unzip -tqq "$part_file" >/dev/null 2>&1; then
    echo "  -> downloaded file is not a valid JAR/ZIP: $filename" >&2
    rm -f "$part_file"
    return 1
  fi

  mv "$part_file" "$destination"
  return 0
}

download_version_file() {
  local version_json="$1"
  local project_slug="$2"
  local version_number="$3"
  local version_id="$4"
  local project_id="$5"
  local file_url filename sha512 sha1 size fallback_url
  local downloaded=0
  local jar_file_count=0

  while IFS=$'\x1f' read -r file_url filename sha512 sha1 size; do
    [[ -z "$file_url" || -z "$filename" ]] && continue
    jar_file_count=$((jar_file_count + 1))
    echo "  -> trying $filename" >&2

    if download_file "$file_url" "$filename" "$sha512" "$sha1" "$size"; then
      downloaded=1
      break
    fi

    # The version API's file URL is authoritative, but retry the canonical
    # Modrinth CDN path as a fallback (the old fallback only ran after a
    # successful download and therefore could never help).
    if [[ -n "$project_id" && -n "$version_id" ]]; then
      fallback_url="$(canonical_cdn_url "$project_id" "$version_id" "$filename")"
      if [[ "$fallback_url" != "$file_url" ]]; then
        echo "  -> trying canonical Modrinth CDN URL" >&2
        if download_file "$fallback_url" "$filename" "$sha512" "$sha1" "$size"; then
          downloaded=1
          break
        fi
      fi
    fi
  done < <(jq -r '
    (.files // [])
    | to_entries
    | sort_by(if .value.primary == true then 0 else 1 end)
    | .[]
    | select(((.value.filename // "") | ascii_downcase | endswith(".jar")))
    | [
        (.value.url // ""),
        (.value.filename // ""),
        (.value.hashes.sha512 // ""),
        (.value.hashes.sha1 // ""),
        (.value.size // "")
      ]
    | join("\u001f")
  ' <<<"$version_json")

  if [[ "$downloaded" -ne 1 ]]; then
    if [[ "$jar_file_count" -eq 0 ]]; then
      echo "::error::Modrinth version $project_slug @ $version_number has no JAR file." >&2
    else
      echo "::error::Could not download and verify any JAR for $project_slug @ $version_number." >&2
    fi
    return 1
  fi
}

process_version() {
  local version_json="$1"
  local display_name="$2"
  local resolution="${3:-dependency}"
  local version_id project_id version_number actual_slug
  local dep_project dep_version dep_type dep_json dep_versions selection
  local selected_resolution rc

  version_id="$(jq -r '.id // empty' <<<"$version_json")"
  project_id="$(jq -r '.project_id // empty' <<<"$version_json")"
  version_number="$(jq -r '.version_number // empty' <<<"$version_json")"
  actual_slug="$(jq -r '.slug // empty' <<<"$version_json")"
  [[ -n "$actual_slug" ]] || actual_slug="$display_name"

  if [[ -z "$version_id" || -z "$project_id" || -z "$version_number" ]]; then
    echo "::error::Modrinth returned incomplete version metadata while resolving '$display_name'." >&2
    return 1
  fi

  if [[ -n "${RESOLVED_PROJECTS[$project_id]:-}" ]]; then
    if [[ "${RESOLVED_PROJECTS[$project_id]}" == "$version_id" ]]; then
      return 0
    fi
    echo "::error::Conflicting required Modrinth versions for project '$actual_slug': ${RESOLVED_PROJECTS[$project_id]} and $version_id ($version_number)." >&2
    return 1
  fi
  if [[ -n "${RESOLVED_VERSIONS[$version_id]:-}" ]]; then
    return 0
  fi

  RESOLVED_PROJECTS[$project_id]="$version_id"
  RESOLVED_VERSIONS[$version_id]=1

  if [[ "$resolution" == "latest-compatible" || "$resolution" == "latest-compatible-prerelease" ]]; then
    echo "::warning::Pinned version for '$display_name' was unavailable for Minecraft $MC_VERSION/$LOADER; using compatible Modrinth version $version_number ($resolution)." >&2
  elif [[ "$resolution" == "compatible-pin" ]]; then
    echo "::notice::Matched '$display_name' pin to Modrinth version $version_number by its mod-version component." >&2
  elif [[ "$resolution" == "normalized" ]]; then
    echo "::notice::Matched '$display_name' pin to equivalent Modrinth version $version_number after normalizing version separators/case." >&2
  fi
  echo "Resolving $display_name -> $version_number [$version_id]" >&2

  download_version_file "$version_json" "$actual_slug" "$version_number" "$version_id" "$project_id"

  while IFS=$'\x1f' read -r dep_project dep_version dep_type; do
    [[ "$dep_type" == "required" ]] || continue
    if [[ -z "$dep_project" && -z "$dep_version" ]]; then
      continue
    fi

    if [[ -n "$dep_version" && "$dep_version" != "null" ]]; then
      if dep_json="$(api_get "$MODRINTH_API_BASE_URL/version/$(urlencode "$dep_version")")"; then
        local actual_dep_project
        actual_dep_project="$(jq -r '.project_id // empty' <<<"$dep_json")"
        if [[ -n "$dep_project" && -n "$actual_dep_project" && "$dep_project" != "$actual_dep_project" ]]; then
          echo "::error::Modrinth dependency version $dep_version belongs to project $actual_dep_project, not the declared project $dep_project." >&2
          return 1
        fi
        process_version "$dep_json" "required dependency $dep_project" "dependency"
      else
        rc=$?
        if [[ "$rc" -ne 4 || -z "$dep_project" ]]; then
          return "$rc"
        fi
        echo "::warning::Required dependency version $dep_version is unavailable; resolving a compatible version for project $dep_project instead." >&2
        dep_versions="$(compatible_versions_for_project "$dep_project")" || return $?
        selection="$(choose_compatible_version "$dep_versions" "")" || {
          echo "::error::No compatible Modrinth version found for required dependency project $dep_project." >&2
          return 1
        }
        dep_json="$(jq -c '.version' <<<"$selection")"
        selected_resolution="$(jq -r '.resolution' <<<"$selection")"
        process_version "$dep_json" "required dependency $dep_project" "$selected_resolution"
      fi
    elif [[ -n "$dep_project" ]]; then
      dep_versions="$(compatible_versions_for_project "$dep_project")" || return $?
      selection="$(choose_compatible_version "$dep_versions" "")" || {
        echo "::error::No compatible Modrinth version found for required dependency project $dep_project." >&2
        return 1
      }
      dep_json="$(jq -c '.version' <<<"$selection")"
      selected_resolution="$(jq -r '.resolution' <<<"$selection")"
      process_version "$dep_json" "required dependency $dep_project" "$selected_resolution"
    else
      echo "::error::A required Modrinth dependency of '$actual_slug' has no project or version id." >&2
      return 1
    fi
  done < <(jq -r '
    .dependencies[]?
    | [(.project_id // ""), (.version_id // ""), (.dependency_type // "")]
    | join("\u001f")
  ' <<<"$version_json")
}

resolve_root_mod() {
  local requested_slug="$1"
  local wanted_version="$2"
  local project_json project_id canonical_slug versions_json selection version_json resolution

  project_json="$(project_json_for_slug "$requested_slug")" || return $?
  project_id="$(jq -r '.id // empty' <<<"$project_json")"
  canonical_slug="$(jq -r '.slug // empty' <<<"$project_json")"
  if [[ -z "$project_id" || -z "$canonical_slug" ]]; then
    echo "::error::Modrinth project metadata is missing an id or slug for '$requested_slug'." >&2
    return 1
  fi

  versions_json="$(compatible_versions_for_project "$project_id")" || return $?
  if ! selection="$(choose_compatible_version "$versions_json" "$wanted_version")"; then
    echo "::error::No listed Modrinth version of '$canonical_slug' supports Minecraft $MC_VERSION with $LOADER." >&2
    return 1
  fi

  version_json="$(jq -c '.version' <<<"$selection")"
  resolution="$(jq -r '.resolution' <<<"$selection")"
  if [[ -n "$wanted_version" && "$resolution" == "latest-compatible" ]]; then
    echo "::warning::Pinned version '$wanted_version' for '$requested_slug' was not found; the latest compatible release will be used." >&2
  elif [[ -n "$wanted_version" && "$resolution" == "latest-compatible-prerelease" ]]; then
    echo "::warning::Pinned version '$wanted_version' for '$requested_slug' was not found; the latest compatible listed build will be used." >&2
  fi

  process_version "$version_json" "$requested_slug" "$resolution"
}

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

root_mod_count=0
while IFS='|' read -r slug wanted_version extra || [[ -n "${slug:-}${wanted_version:-}${extra:-}" ]]; do
  slug="$(trim "${slug:-}")"
  wanted_version="$(trim "${wanted_version:-}")"
  extra="$(trim "${extra:-}")"
  [[ -z "$slug" || "$slug" == \#* ]] && continue
  if [[ -n "$extra" ]]; then
    echo "::error::Invalid mod manifest row (expected slug|version): $slug|$wanted_version|$extra" >&2
    exit 1
  fi
  resolve_root_mod "$slug" "$wanted_version"
  root_mod_count=$((root_mod_count + 1))
done < "$MODS_FILE"

if [[ "$root_mod_count" -eq 0 ]]; then
  echo "::error::No top-level mods were found in $MODS_FILE." >&2
  exit 1
fi

jar_count="$(find "$MODS_DIR" -maxdepth 1 -type f -iname '*.jar' | wc -l | tr -d '[:space:]')"
if [[ "$jar_count" -eq 0 ]]; then
  echo "::error::The resolved client pack contains no JAR files." >&2
  exit 1
fi

cat > "$CLIENT_DIR/README.txt" <<EOF
Minecraft $MC_VERSION Fabric $LOADER_VERSION
Generated automatically by GitHub Actions.
Mod versions are resolved through the Modrinth API for $MC_VERSION and $LOADER.
Pinned versions are preferred; if a pin is no longer available, the latest compatible listed release is used.
Required Modrinth dependencies are resolved transitively by their exact version IDs where available.
EOF

cp "$ROOT_DIR/modpack/modpack.yml" "$CLIENT_DIR/modpack.yml"
(
  cd "$CLIENT_DIR"
  zip -qr "$CLIENT_ZIP" .
)
unzip -tqq "$CLIENT_ZIP"

printf 'Top-level manifest entries: %s\n' "$root_mod_count"
printf 'Resolved Modrinth projects (including required dependencies): %s\n' "${#RESOLVED_PROJECTS[@]}"
printf 'Client JAR count: %s\n' "$jar_count"
printf 'Client ZIP: '
ls -lh "$CLIENT_ZIP"
printf 'SHA-256: '
sha256sum "$CLIENT_ZIP"
