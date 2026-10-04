#!/usr/bin/env python3
"""Verifica el manifiesto del modpack contra la API de Modrinth.

- Valida el esquema de modpack/modpack.yml (siempre, sin red).
- Comprueba que cada mod tiene build para Minecraft 1.21.1 + Fabric (requiere red).
- Comprueba que el entorno declarado (cliente/servidor/ambos) cuadra con Modrinth.
- Descubre dependencias 'required' no declaradas en el manifiesto.
- NUNCA descarga .jar (eso es trabajo de construir.py, solo si estado=aprobado).

Códigos de salida: 0 OK (avisos permitidos salvo --estricto), 1 fallos de
verificación, 2 errores de esquema/manifiesto.
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API = "https://api.modrinth.com/v2"
UA = {"User-Agent": "server-minecraft-resolver/1.0 (+https://modrinth.com)"}

LADOS = {"cliente", "servidor", "ambos"}
IMPACTOS = {"despreciable", "bajo", "moderado", "alto", "mejora"}
VERIFICACIONES = {"confirmada", "estandar", "pendiente"}
CAMPOS_MOD = {"slug", "nombre", "lado", "categoria", "impacto", "verificacion", "estado"}

_cache_proyectos = {}


def cargar_manifiesto(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("ERROR: falta pyyaml. Instala con: pip install -r scripts/requirements.txt")
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        sys.exit(f"ERROR: no existe el manifiesto: {path}")
    if not isinstance(data, dict):
        sys.exit("ERROR: el manifiesto no es un objeto YAML válido.")
    return data


def validar_esquema(m: dict) -> list:
    errores = []
    for campo in ("minecraft", "loader", "estado_global", "mods"):
        if campo not in m:
            errores.append(f"Falta el campo raíz '{campo}'.")
    if m.get("estado_global") not in ("propuesto", "aprobado"):
        errores.append("estado_global debe ser 'propuesto' o 'aprobado'.")
    vistos = set()
    for seccion in ("mods", "opcionales"):
        for i, mod in enumerate(m.get(seccion, []) or []):
            ctx = f"{seccion}[{i}]"
            if not isinstance(mod, dict):
                errores.append(f"{ctx}: debe ser un objeto.")
                continue
            faltan = {"slug", "nombre", "lado"} - set(mod)
            if faltan:
                errores.append(f"{ctx}: faltan campos {sorted(faltan)}.")
                continue
            slug = mod["slug"]
            if slug in vistos:
                errores.append(f"{ctx}: slug duplicado '{slug}'.")
            vistos.add(slug)
            if mod["lado"] not in LADOS:
                errores.append(f"{ctx} ({slug}): lado '{mod['lado']}' inválido.")
            if mod.get("impacto", "bajo") not in IMPACTOS:
                errores.append(f"{ctx} ({slug}): impacto inválido.")
            if mod.get("verificacion", "pendiente") not in VERIFICACIONES:
                errores.append(f"{ctx} ({slug}): verificacion inválida.")
    return errores


def api_get(path: str, params: dict | None = None):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def slug_desde_id(project_id: str) -> str:
    if project_id not in _cache_proyectos:
        proj = api_get(f"/project/{project_id}")
        _cache_proyectos[project_id] = (proj or {}).get("slug", project_id)
    return _cache_proyectos[project_id]


def mejor_version(slug: str, mc: str, loader: str):
    """Devuelve (proyecto, version) o (None, None) si no existe build compatible."""
    proyecto = api_get(f"/project/{slug}")
    if proyecto is None:
        return None, None
    versiones = api_get(
        f"/project/{slug}/version",
        {"loaders": json.dumps([loader]), "game_versions": json.dumps([mc]), "limit": 10},
    ) or []
    if not versiones:
        return proyecto, None
    orden = {"release": 0, "beta": 1, "alpha": 2}
    # Estable: primero lo más nuevo, luego por canal -> gana la release más reciente
    # (solo se usa beta/alpha si no existe release para 1.21.1/Fabric).
    versiones.sort(key=lambda v: v.get("date_published", ""), reverse=True)
    versiones.sort(key=lambda v: orden.get(v.get("version_type", "release"), 3))
    return proyecto, versiones[0]


def comprobar_lado(lado: str, entorno: dict) -> str | None:
    """Devuelve un aviso si el lado declarado no cuadra con Modrinth, o None."""
    cli, srv = entorno.get("client", "unknown"), entorno.get("server", "unknown")
    ok = {"required", "optional"}
    if lado == "ambos":
        if cli not in ok or srv not in ok:
            if cli == "unsupported" and srv in ok:
                return f"Modrinth dice SOLO SERVIDOR (client={cli}, server={srv}); sobra en clientes."
            if srv == "unsupported" and cli in ok:
                return f"Modrinth dice SOLO CLIENTE (client={cli}, server={srv}); sobra en servidor."
            return f"Entorno Modrinth inesperado (client={cli}, server={srv})."
    elif lado == "cliente":
        if cli not in ok:
            return f"Modrinth dice que NO es de cliente (client={cli}, server={srv})."
        if srv not in ("unsupported", "optional"):
            return f"Modrinth dice que también va en servidor (server={srv}); revisar lado."
    elif lado == "servidor":
        if srv not in ok:
            return f"Modrinth dice que NO es de servidor (client={cli}, server={srv})."
        if cli not in ("unsupported", "optional"):
            return f"Modrinth dice que también va en cliente (client={cli}); revisar lado."
    return None


def verificar(mods: list, mc: str, loader: str, declarados: set, nucleo: bool):
    resultados = []
    for mod in mods:
        slug = mod["slug"]
        fila = {"slug": slug, "nombre": mod.get("nombre", slug), "lado": mod["lado"],
                "nucleo": nucleo, "ok": True, "avisos": [], "error": None,
                "version": None, "dependencias": [], "lado_manual": False}
        try:
            proyecto, version = mejor_version(slug, mc, loader)
        except Exception as e:  # red caída, etc.
            fila["ok"] = False
            fila["error"] = f"Error consultando Modrinth: {e}"
            resultados.append(fila)
            continue
        if proyecto is None:
            fila["ok"] = False
            fila["error"] = "El slug NO EXISTE en Modrinth (¿nombre mal escrito?)."
            resultados.append(fila)
            continue
        if version is None:
            fila["ok"] = False
            fila["error"] = f"Sin build para {mc} + {loader}."
            resultados.append(fila)
            continue
        fila["version"] = {
            "id": version["id"],
            "numero": version.get("version_number", "?"),
            "tipo": version.get("version_type", "?"),
            # El lado "oficial" vive en el proyecto, no en la version.
            "entorno": {"client": (proyecto or {}).get("client_side", "unknown"),
                        "server": (proyecto or {}).get("server_side", "unknown"),
                        "detalle": version.get("environment", "?")},
        }
        if mod.get("lado_verificado_manual"):
            fila["lado_manual"] = True
        else:
            aviso = comprobar_lado(mod["lado"], fila["version"]["entorno"])
            if aviso:
                fila["avisos"].append(aviso)
        for dep in version.get("dependencies", []) or []:
            tipo = dep.get("dependency_type", "unknown")
            dep_slug = slug_desde_id(dep["project_id"]) if dep.get("project_id") else "?"
            fila["dependencias"].append({"slug": dep_slug, "tipo": tipo})
            if tipo == "required" and dep_slug not in declarados:
                fila["avisos"].append(
                    f"Requiere '{dep_slug}', NO declarado en el manifiesto (añadirlo o descartar)."
                )
        resultados.append(fila)
    return resultados


def escribir_informe(path: Path, m: dict, resultados: list):
    nucleo = [r for r in resultados if r["nucleo"]]
    opc = [r for r in resultados if not r["nucleo"]]
    ok = sum(1 for r in nucleo if r["ok"] and not r["error"])
    lineas = [
        f"# Informe de verificación — {m.get('modpack_nombre', '?')} {m.get('modpack_version', '?')}",
        "",
        f"Minecraft {m['minecraft']} + {m['loader']}. Estado: **{m['estado_global']}**.",
        f"Core: {ok}/{len(nucleo)} verificados. Opcionales: {len(opc)} (informativos).",
        "",
        "## Core",
        "",
        "| Mod | Lado | Versión | Entorno | Estado |",
        "| --- | ---- | ------- | ------- | ------ |",
    ]
    for r in nucleo + opc:
        if r["error"]:
            estado = f"❌ {r['error']}"
            ver, env = "-", "-"
        else:
            ver = f"{r['version']['numero']} ({r['version']['tipo']})"
            env = f"{r['version']['entorno']['client']}/{r['version']['entorno']['server']}"
            if r["avisos"]:
                estado = "⚠️ " + "; ".join(r["avisos"])
            elif r.get("lado_manual"):
                estado = "✅ OK (lado verificado manual)"
            else:
                estado = "✅ OK"
        lineas.append(f"| {r['nombre']} `{r['slug']}` | {r['lado']} | {ver} | {env} | {estado} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Verifica el manifiesto contra Modrinth (no descarga).")
    ap.add_argument("--manifiesto", default=str(RAIZ / "modpack" / "modpack.yml"))
    ap.add_argument("--solo-esquema", action="store_true", help="Solo valida el YAML, sin red.")
    ap.add_argument("--informe", default=None, help="Escribe informe markdown en esta ruta.")
    ap.add_argument("--guardar", default=None, help="Fija versiones en JSON (requiere estado aprobado).")
    ap.add_argument("--estricto", action="store_true", help="Los avisos también fallan.")
    args = ap.parse_args()

    m = cargar_manifiesto(Path(args.manifiesto))
    errores = validar_esquema(m)
    if errores:
        print("ERRORES DE ESQUEMA:")
        for e in errores:
            print(f"  - {e}")
        return 2

    n_core, n_opc = len(m.get("mods", [])), len(m.get("opcionales", []) or [])
    print(f"Esquema OK: {n_core} mods core + {n_opc} opcionales. Estado: {m['estado_global']}.")
    if args.solo_esquema:
        return 0

    mc, loader = m["minecraft"], m["loader"]
    declarados = {x["slug"] for x in (m.get("mods", []) + (m.get("opcionales", []) or []))}
    print(f"Verificando contra Modrinth ({mc} + {loader})... [NUCLEO=core, OPC=opcional]")
    resultados = verificar(m.get("mods", []), mc, loader, declarados, True)
    resultados += verificar(m.get("opcionales", []) or [], mc, loader, declarados, False)

    fallos = [r for r in resultados if r["nucleo"] and r["error"]]
    avisos_core = [r for r in resultados if r["nucleo"] and not r["error"] and r["avisos"]]
    for r in fallos:
        print(f"::error file=modpack/modpack.yml::[{r['slug']}] {r['error']}")
    for r in avisos_core:
        for a in r["avisos"]:
            print(f"::error file=modpack/modpack.yml::[{r['slug']}] {a}")
    for r in resultados:
        tag = "NUCLEO" if r["nucleo"] else "OPC   "
        if r["error"]:
            print(f"  [{tag}] ❌ {r['slug']}: {r['error']}")
        elif r["avisos"]:
            print(f"  [{tag}] ⚠️  {r['slug']}: " + " | ".join(r["avisos"]))
        else:
            extra = " (lado verificado manual)" if r.get("lado_manual") else ""
            print(f"  [{tag}] ✅ {r['slug']} {r['version']['numero']}{extra}")

    if args.informe:
        escribir_informe(Path(args.informe), m, resultados)
        print(f"Informe escrito en {args.informe}")

    if args.guardar:
        if m["estado_global"] != "aprobado":
            print("⛔ --guardar requiere estado_global: aprobado (estamos en propuesta).")
            return 2
        if fallos:
            print("⛔ Hay mods core sin build compatible; no se fija la resolución.")
            return 1
        resolucion = {"minecraft": mc, "loader": loader,
                      "mods": {r["slug"]: {"lado": r["lado"], "version_id": r["version"]["id"],
                                            "numero": r["version"]["numero"]}
                               for r in resultados if r["nucleo"]}}
        Path(args.guardar).parent.mkdir(parents=True, exist_ok=True)
        Path(args.guardar).write_text(json.dumps(resolucion, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Resolución fijada en {args.guardar}")

    if fallos:
        return 1
    if args.estricto and avisos_core:
        print("⛔ Hay avisos en el core (--estricto).")
        return 1
    print("Verificación superada. (No se ha descargado ningún .jar.)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        import traceback
        tb = traceback.format_exc().replace("\n", " | ")
        print(f"::error file=scripts/resolver.py::CRASH {tb[:1500]}")
        sys.exit(2)
