#!/usr/bin/env python3
"""Verifica un build del modpack y genera docs/INFORME_BUILD.md.

Comprueba (solo lectura sobre build/, salvo el informe):
  1. El lockfile (resolucion.json) está bien formado y cubre EXACTO el core.
  2. Ningún opcional está fijado ni descargado.
  3. Nº de .jar descargados == nº de mods fijados.
  4. El .mrpack indexa todos los mods; sus overrides/mods NO traen solo-servidor.
  5. servidor/mods trae EXACTO los jars de servidor+ambos (0 de cliente).
  6. servidor.zip existe y contiene lo mismo que servidor/.
  7. Totales y tamaños.

Uso en CI (tras construir.py):
  python3 scripts/verificar_build.py --resolucion modpack/resolucion.json \\
      --salida build/ --informe docs/INFORME_BUILD.md

En local sin build/ verifica al menos el lockfile contra el manifiesto.
Sale 0 si todo cuadra, 1 si hay algún error (los avisos no fallan).
"""

import argparse
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LADOS = ("cliente", "servidor", "ambos")


def mb(n: int) -> str:
    return f"{n / 1048576:.1f} MB"


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica el build y genera INFORME_BUILD.md.")
    ap.add_argument("--resolucion", required=True)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--manifiesto", default=str(RAIZ / "modpack" / "modpack.yml"))
    ap.add_argument("--informe", default=None)
    args = ap.parse_args()

    errores, avisos, oks = [], [], []
    res = json.loads(Path(args.resolucion).read_text(encoding="utf-8"))
    salida = Path(args.salida)
    mods = res.get("mods", {})

    # 1. Estructura del lockfile.
    if not mods:
        errores.append("lockfile sin mods.")
    for slug, pin in sorted(mods.items()):
        for campo in ("lado", "version_id", "numero"):
            if campo not in pin:
                errores.append(f"[{slug}] falta '{campo}' en el lockfile.")
        if pin.get("lado") not in LADOS:
            errores.append(f"[{slug}] lado inválido: {pin.get('lado')!r}.")
    if not errores:
        oks.append(f"lockfile válido: {len(mods)} mods fijados "
                   f"({res.get('minecraft')} + {res.get('loader')}).")

    # 2. Cruce con el manifiesto (requiere pyyaml; si no está, se omite).
    lados_manifiesto = {}
    try:
        import yaml
        m = yaml.safe_load(open(args.manifiesto, encoding="utf-8"))
        core = {x["slug"] for x in m.get("mods", [])}
        opc = {x["slug"] for x in (m.get("opcionales") or [])}
        lados_manifiesto = {x["slug"]: x["lado"] for x in m.get("mods", [])}
        if m.get("estado_global") != "aprobado":
            errores.append(f"manifiesto en estado {m.get('estado_global')!r}, no 'aprobado'.")
        if set(mods) != core:
            errores.append(f"lock({len(mods)}) != core manifiesto({len(core)}): "
                           f"+{sorted(set(mods) - core)} -{sorted(core - set(mods))}.")
        else:
            oks.append(f"el lock cubre EXACTO los {len(core)} mods core.")
        if set(mods) & opc:
            errores.append(f"opcionales dentro del lock: {sorted(set(mods) & opc)}.")
        else:
            oks.append(f"ningún opcional ({len(opc)}) dentro del lock.")
        for slug, lado in lados_manifiesto.items():
            if slug in mods and mods[slug]["lado"] != lado:
                errores.append(f"[{slug}] lado lock {mods[slug]['lado']!r} != manifiesto {lado!r}.")
    except ImportError:
        avisos.append("pyyaml no disponible: cruce lockfile↔manifiesto omitido.")
    n_cli = sum(1 for p in mods.values() if p.get("lado") == "cliente")
    n_srv = sum(1 for p in mods.values() if p.get("lado") == "servidor")
    n_amb = sum(1 for p in mods.values() if p.get("lado") == "ambos")

    # 3. Descargas.
    jars = sorted((salida / "descargas").glob("*.jar")) if (salida / "descargas").is_dir() else []
    tot_desc = sum(f.stat().st_size for f in jars)
    if not jars:
        avisos.append("build/descargas/ vacío o ausente: checks de .jar omitidos.")
    elif len(jars) != len(mods):
        errores.append(f"descargas({len(jars)}) != fijados({len(mods)}).")
    else:
        oks.append(f"{len(jars)} .jar descargados ({mb(tot_desc)}).")

    # 4. .mrpack (cliente).
    mrpacks = sorted(salida.glob("*.mrpack"))
    env_por_jar, index = {}, None
    mrpack_bytes, bundled = 0, []
    if len(mrpacks) != 1:
        (errores if jars else avisos).append(f".mrpack: hay {len(mrpacks)}, esperado 1.")
    else:
        mrpack_bytes = mrpacks[0].stat().st_size
        with zipfile.ZipFile(mrpacks[0]) as z:
            index = json.loads(z.read("modrinth.index.json"))
            names = z.namelist()
        files = index.get("files", [])
        env_por_jar = {f["path"].rsplit("/", 1)[-1]: f.get("env", {}) for f in files}
        if len(files) != len(mods):
            errores.append(f"índice mrpack({len(files)}) != fijados({len(mods)}).")
        bundled = [n for n in names if n.startswith("overrides/mods/") and n.endswith(".jar")]
        for b in bundled:
            fn = b.rsplit("/", 1)[-1]
            e = env_por_jar.get(fn)
            if e is None:
                errores.append(f"cliente/{fn} empaquetado sin entrada en el índice.")
            elif e.get("client") == "unsupported":
                errores.append(f"cliente/{fn} es SOLO-SERVIDOR y está en el cliente.")
        if len(bundled) != n_cli + n_amb:
            errores.append(f"cliente trae {len(bundled)} .jar, esperados {n_cli + n_amb}.")
        else:
            oks.append(f"cliente: {len(bundled)} .jar ({n_cli} cliente + {n_amb} ambos), "
                       f"0 solo-servidor.")
        loader = (index.get("dependencies") or {}).get("fabric-loader", "?")
        if res.get("fabric_loader") and res["fabric_loader"] != loader:
            errores.append(f"loader del lock ({res['fabric_loader']}) != mrpack ({loader}).")
        else:
            oks.append(f"fabric-loader {loader} consistente lock↔mrpack.")

    # 5. Servidor.
    srv_dir = salida / "servidor" / "mods"
    srv_mods = sorted(srv_dir.glob("*.jar")) if srv_dir.is_dir() else []
    if not srv_mods:
        (errores if jars else avisos).append("servidor/mods/ vacío o ausente.")
    else:
        for f in srv_mods:
            e = env_por_jar.get(f.name)
            if index is not None and e is None:
                errores.append(f"servidor/{f.name} sin entrada en el índice.")
            elif e is not None and e.get("server") != "required":
                errores.append(f"servidor/{f.name} NO es de servidor.")
        # Cruce por lado declarado en el lock (vía índice env).
        n_srv_idx = sum(1 for fn, e in env_por_jar.items()
                        if e.get("server") == "required" and e.get("client") == "unsupported")
        n_amb_idx = sum(1 for fn, e in env_por_jar.items()
                        if e.get("server") == "required" and e.get("client") == "required")
        if n_srv_idx or n_amb_idx:
            if len(srv_mods) != n_srv_idx + n_amb_idx:
                errores.append(f"servidor trae {len(srv_mods)} .jar, "
                               f"esperados {n_srv_idx + n_amb_idx}.")
            else:
                oks.append(f"servidor: {len(srv_mods)} .jar ({n_srv_idx} servidor + "
                           f"{n_amb_idx} ambos), 0 de cliente.")

    # 6. servidor.zip.
    zsrv = salida / "servidor.zip"
    if not zsrv.exists():
        (errores if jars else avisos).append("falta build/servidor.zip.")
    elif srv_mods:
        with zipfile.ZipFile(zsrv) as z:
            dentro = sorted(n for n in z.namelist() if n.startswith("mods/") and n.endswith(".jar"))
        fuera = sorted(f"mods/{f.name}" for f in srv_mods)
        if dentro != fuera:
            errores.append("servidor.zip no coincide con servidor/mods/.")
        else:
            oks.append(f"servidor.zip íntegro ({mb(zsrv.stat().st_size)}).")

    # 7. Informe markdown.
    if args.informe:
        ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        loader = (index.get("dependencies", {}).get("fabric-loader", "?") if index
                  else res.get("fabric_loader", "?"))
        lineas = [
            f"# Informe de construcción — {res.get('minecraft')} + {res.get('loader')}",
            "",
            f"- Fecha (UTC): {ahora}.",
            f"- Lockfile: `modpack/resolucion.json` ({len(mods)} mods, fabric-loader {loader}).",
            f"- Fijado en: {res.get('fijado_en', '?')}.",
            f"- Cliente: `{mrpacks[0].name if mrpacks else '?'}` "
            f"({mb(mrpack_bytes)}, {len(bundled)} .jar: {n_cli} cliente + {n_amb} ambos).",
            f"- Servidor: `servidor.zip` "
            f"({mb(zsrv.stat().st_size) if zsrv.exists() else '?'}"
            f", {len(srv_mods)} .jar: {n_srv} servidor + {n_amb} ambos).",
            f"- Descargas totales: {len(jars)} .jar ({mb(tot_desc)}).",
            "",
            "## Validaciones",
            "",
        ]
        for o in oks:
            lineas.append(f"- ✔ {o}")
        for a in avisos:
            lineas.append(f"- ⚠ {a}")
        for e in errores:
            lineas.append(f"- ❌ {e}")
        lineas += ["", "## Versiones fijadas", "",
                   "| Mod | Lado | Versión | Version ID |",
                   "| --- | --- | --- | --- |"]
        for slug in sorted(mods):
            p = mods[slug]
            lineas.append(f"| {slug} | {p.get('lado')} | {p.get('numero')} | `{p.get('version_id')}` |")
        lineas += ["",
                   "## Reproducir este build",
                   "",
                   "```bash",
                   "pip install -r scripts/requirements.txt",
                   "python3 scripts/resolver.py --estricto --informe build/informe-verificacion.md",
                   "python3 scripts/construir.py --resolucion modpack/resolucion.json --salida build/",
                   "python3 scripts/verificar_build.py --resolucion modpack/resolucion.json \\",
                   "    --salida build/ --informe docs/INFORME_BUILD.md",
                   "```",
                   "",
                   "No re-fijar versiones sin motivo (`--guardar` solo para actualizar",
                   "deliberadamente). Los opcionales quedan fuera del core.",
                   ""]
        Path(args.informe).parent.mkdir(parents=True, exist_ok=True)
        Path(args.informe).write_text("\n".join(lineas), encoding="utf-8")
        print(f"Informe escrito en {args.informe}")

    for o in oks:
        print(f"  ✔ {o}")
    for a in avisos:
        print(f"  ⚠ {a}")
    for e in errores:
        print(f"  ❌ {e}")
        print(f"::error::[build] {e}")
    print(f"::notice::BUILD mods={len(mods)} jars={len(jars)} "
          f"descargas={mb(tot_desc)} cliente={len(bundled)}x srv={len(srv_mods)}x "
          f"mrpack={mb(mrpack_bytes)}")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
