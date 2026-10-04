#!/usr/bin/env python3
"""Prueba de arranque del servidor en entorno limpio (CI).

Arranca fabric-server-launch.jar con heap limitado, espera al estado listo
("Done ("), deja asentar, detiene con "stop" y analiza el log: errores,
crash-reports, mods cargados (lista de Fabric Loader), spotlight de mods
clave y, críticamente, que ningún mod de cliente se cargue en servidor.

Nunca modifica mods ni versiones: si algo falla, informa y sale 1.
Solo usa la stdlib.
"""

import argparse
import json
import re
import subprocess
import sys
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

LISTO = "Done ("
SPOTLIGHT = {
    "betterend": ["betterend"],
    "betternether": ["betternether"],
    "terralith": ["terralith"],
    "wizards": ["wizards"],
    "techreborn": ["techreborn"],
    "universal-graves": ["universalgrav", "graves"],
    "polymer": ["polymer"],
    "simple-voice-chat": ["voicechat"],
    "yungs-better-dungeons": ["yungs"],
    "yungs-better-mineshafts": ["yungs"],
    "yungs-better-strongholds": ["yungs"],
    "yungs-better-nether-fortresses": ["yungs"],
    "structory": ["structory"],
    "towns-and-towers": ["townsandtowers", "towns and towers"],
    "lithostitched": ["lithostitched"],
    "cristel-lib": ["cristel"],
    "noisium": ["noisium"],
    "bclib": ["bclib"],
    "worldweaver": ["worldweaver", "wover"],
}
PATRONES_ERROR = [re.compile(p, re.IGNORECASE) for p in
                  (r"\berror\b", r"\bfatal\b", r"exception", r"caused by",
                   r"\bfailed\b", r"unable to", r"\bmissing\b", r"incompatible",
                   r"\bcrash\b", r"conflict")]


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def rss_mb(pid: int):
    try:
        for ln in Path(f"/proc/{pid}/status").read_text().splitlines():
            if ln.startswith("VmRSS:"):
                return int(ln.split()[1]) // 1024
    except OSError:
        return None
    return None


def java_version(java: str) -> str:
    try:
        r = subprocess.run([java, "-version"], capture_output=True, text=True, timeout=30)
        return ((r.stderr or r.stdout).strip().splitlines() or ["?"])[0]
    except Exception as e:  # pragma: no cover
        return f"desconocida ({e})"


def main() -> int:
    ap = argparse.ArgumentParser(description="Boot-test del servidor + informe.")
    ap.add_argument("--dir", required=True, help="Directorio del servidor instalado.")
    ap.add_argument("--resolucion", required=True, help="Lockfile con lados.")
    ap.add_argument("--informe", required=True, help="Markdown a generar.")
    ap.add_argument("--log", default=None, help="Fichero de log (def: <dir>/../arranque.log).")
    ap.add_argument("--java", default="java")
    ap.add_argument("--xms", default="1G")
    ap.add_argument("--xmx", default="4G")
    ap.add_argument("--installer", default="?")
    ap.add_argument("--timeout-arranque", type=int, default=600)
    ap.add_argument("--asentamiento", type=int, default=15)
    ap.add_argument("--timeout-parada", type=int, default=120)
    args = ap.parse_args()

    srv = Path(args.dir)
    log_path = Path(args.log) if args.log else srv.parent / "arranque.log"
    res = json.loads(Path(args.resolucion).read_text(encoding="utf-8"))
    mods_lock = res.get("mods", {})
    cli_lock = {s for s, p in mods_lock.items() if p.get("lado") == "cliente"}
    n_srv_esperados = sum(1 for p in mods_lock.values() if p.get("lado") in ("servidor", "ambos"))

    if not (srv / "fabric-server-launch.jar").exists():
        print("::error::[arranque] falta fabric-server-launch.jar en " + str(srv))
        return 2
    if not (srv / "eula.txt").exists():
        print("::error::[arranque] falta eula.txt (el workflow debe aceptarlo).")
        return 2

    ver_java = java_version(args.java)
    print(f"Java: {ver_java}")
    cmd = [args.java, f"-Xms{args.xms}", f"-Xmx{args.xmx}",
           "-jar", "fabric-server-launch.jar", "nogui"]
    print("Comando: " + " ".join(cmd))

    logf = open(log_path, "w", encoding="utf-8", errors="replace")
    cola = deque(maxlen=500)
    listo = threading.Event()
    proc = subprocess.Popen(cmd, cwd=srv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)

    def lector():
        try:
            for ln in proc.stdout:
                logf.write(ln)
                cola.append(ln.rstrip("\n"))
                if LISTO in ln:
                    listo.set()
        except Exception:
            pass
        finally:
            try:
                logf.flush()
            except Exception:
                pass

    t0 = time.time()
    threading.Thread(target=lector, daemon=True).start()
    pico, t_listo, causa_fallo = 0, None, None
    while time.time() - t0 < args.timeout_arranque:
        r = rss_mb(proc.pid)
        if r:
            pico = max(pico, r)
        if listo.is_set():
            t_listo = time.time()
            break
        if proc.poll() is not None:
            causa_fallo = f"el proceso terminó antes del listo (exit {proc.poll()})."
            break
        time.sleep(5)
    if t_listo is None and causa_fallo is None:
        causa_fallo = f"timeout ({args.timeout_arranque}s) sin llegar a listo."

    parada_limpia, exit_code = False, None
    if t_listo is not None:
        print(f"Listo en {t_listo - t0:.0f}s; asentando {args.asentamiento}s...")
        fin = time.time() + args.asentamiento
        while time.time() < fin and proc.poll() is None:
            r = rss_mb(proc.pid)
            if r:
                pico = max(pico, r)
            time.sleep(5)
        if proc.poll() is None:
            try:
                proc.stdin.write("stop\n")
                proc.stdin.flush()
            except BrokenPipeError:
                pass
            try:
                exit_code = proc.wait(timeout=args.timeout_parada)
                parada_limpia = (exit_code == 0)
            except subprocess.TimeoutExpired:
                causa_fallo = (causa_fallo or "") + " no se detuvo con 'stop' a tiempo."
                proc.terminate()
        else:
            exit_code = proc.poll()
            causa_fallo = (causa_fallo or "") + f" murió tras el listo (exit {exit_code})."
    else:
        try:
            if proc.poll() is None:
                proc.terminate()
                exit_code = proc.wait(timeout=60)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    time.sleep(2)
    try:
        logf.close()
    except Exception:
        pass

    # ---------- Análisis ----------
    texto = log_path.read_text(encoding="utf-8", errors="replace")
    lineas = texto.splitlines()
    bloques, actual = [], None
    for ln in lineas:
        if "Loading" in ln and "mods:" in ln:
            actual = []
            bloques.append(actual)
            continue
        if actual is not None:
            # El bloque solo termina con un evento nuevo ([HH:MM:SS] ...);
            # las líneas raras intermedias se saltan sin cortar la captura.
            if re.match(r"\[\d{2}:\d{2}:\d{2}\]", ln):
                actual = None
                continue
            # Entradas top-level ("- modid version") y anidadas ("|-- ...").
            m = re.match(r"\s*(?:\|--?|\\--?|-)\s*([A-Za-z0-9_.\-]+)(?:\s+(.+))?$", ln)
            if m:
                actual.append((m.group(1), (m.group(2) or "?").strip()[:64]))
    modids = dict(max(bloques, key=len)) if bloques else {}
    norm_ids = {norm(k): k for k in modids}

    en_srv = sorted(s for s in cli_lock if norm(s) in norm_ids)
    crash_dir = srv / "crash-reports"
    crashes = sorted(p.name for p in crash_dir.glob("*.txt")) if crash_dir.is_dir() else []

    bajo = texto.lower()
    spot = {}
    for slug, toks in SPOTLIGHT.items():
        if norm(slug) in norm_ids:
            spot[slug] = ("cargado", norm_ids[norm(slug)])
        elif any(t in bajo for t in toks):
            spot[slug] = ("mencionado", "en log")
        else:
            spot[slug] = ("SIN SEÑAL", "aviso")

    vistos, errores_log = set(), []
    for ln in lineas:
        if any(p.search(ln) for p in PATRONES_ERROR):
            clave = ln.strip()[:220]
            if clave not in vistos:
                vistos.add(clave)
                errores_log.append(clave)
    warns = [ln.strip()[:220] for ln in lineas if re.search(r"\bwarn(ing)?\b", ln, re.IGNORECASE)]
    top_warn, vw = [], set()
    for w in warns:
        if w not in vw:
            vw.add(w)
            top_warn.append(w)
        if len(top_warn) >= 15:
            break

    listo_ok = t_listo is not None and not en_srv and not crashes and parada_limpia
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    informe = [
        f"# Informe de arranque — servidor 1.0.0 ({res.get('minecraft')} + fabric)",
        "",
        f"- Fecha (UTC): {ahora}.",
        f"- Entorno limpio (CI): {ver_java}; installer {args.installer}; "
        f"loader {res.get('fabric_loader')}; JVM -Xms{args.xms} -Xmx{args.xmx}; nogui.",
        f"- Resultado: **{'LISTO ✔' if listo_ok else 'FALLO ❌'}**"
        + (f" ({causa_fallo.strip()})" if causa_fallo else ""),
        f"- Tiempo hasta listo: "
        f"{f'{t_listo - t0:.0f}s' if t_listo else '—'}; parada limpia: "
        f"{'sí' if parada_limpia else 'no'} (exit {exit_code}).",
        f"- Memoria: pico RSS ≈ {pico} MB con heap limitado a {args.xmx}.",
        f"- Mods detectados en Fabric Loader: {len(modids)} "
        f"(esperados en servidor: {n_srv_esperados}).",
        f"- Líneas de error únicas: {len(errores_log)}; WARN: {len(warns)}; "
        f"crash-reports: {len(crashes)}.",
        "",
        "## Checks",
        "",
        f"- {'✔' if t_listo else '❌'} Llegó a listo (`Done (`).",
        f"- {'✔' if parada_limpia else '❌'} Parada limpia con `stop` (exit 0).",
        f"- {'✔' if not crashes else '❌'} Sin crash-reports"
        + (f": {', '.join(crashes)}" if crashes else "."),
        f"- {'✔' if not en_srv else '❌'} Ningún mod de cliente cargado"
        + (f": {', '.join(en_srv)}" if en_srv else f" (0 de {len(cli_lock)})."),
        "",
        "## Spotlight",
        "",
        "| Mod | Estado | Detalle |",
        "| --- | --- | --- |",
    ]
    for slug, (est, det) in spot.items():
        informe.append(f"| {slug} | {est} | {det} |")
    informe += ["", "## Mods cargados (Fabric Loader)", ""]
    for mid in sorted(modids, key=str.lower):
        informe.append(f"- `{mid}` {modids[mid]}")
    informe += ["", f"## Líneas de error únicas ({len(errores_log)})", ""]
    informe += [f"- `{e}`" for e in errores_log[:40]] or ["- (ninguna)"]
    informe += ["", f"## Warnings ({len(warns)} total, top 15 únicos)", ""]
    informe += [f"- `{w}`" for w in top_warn] or ["- (ninguno)"]
    informe += ["", "## Cola del log (últimas 30 líneas)", "", "```"]
    informe += lineas[-30:] or ["(vacío)"]
    informe += ["```", "", "## Reproducir", "",
                "```bash",
                "pip install -r scripts/requirements.txt",
                "python3 scripts/construir.py --resolucion modpack/resolucion.json --salida build/",
                "mkdir -p prueba/servidor && cd prueba/servidor && \\",
                "  unzip -o ../../build/servidor.zip && \\",
                "  java -jar /tmp/fabric-installer.jar server "
                f"-mcversion {res.get('minecraft')} -loader {res.get('fabric_loader')} "
                "-downloadMinecraft && echo eula=true > eula.txt && cd ../..",
                "python3 scripts/probar_servidor.py --dir prueba/servidor \\",
                "    --resolucion modpack/resolucion.json --informe docs/INFORME_ARRANQUE.md",
                "```", ""]
    Path(args.informe).parent.mkdir(parents=True, exist_ok=True)
    Path(args.informe).write_text("\n".join(informe), encoding="utf-8")
    print(f"Informe escrito en {args.informe}")

    print(f"::notice::ARRANQUE listo={'si' if t_listo else 'no'} "
          f"t_listo={f'{t_listo - t0:.0f}s' if t_listo else '-'} "
          f"pico={pico}MB mods={len(modids)} errores={len(errores_log)} "
          f"warns={len(warns)} crash={len(crashes)} cliente_en_srv={len(en_srv)} "
          f"parada={'ok' if parada_limpia else 'no'}")
    if causa_fallo:
        print(f"::error::[arranque] {causa_fallo.strip()}")
    for s in en_srv:
        print(f"::error::[arranque] mod de CLIENTE cargado en servidor: {s}")
    for c in crashes:
        print(f"::error::[arranque] crash-report: {c}")
    if t_listo is None:
        for ln in [x for x in lineas if x.strip()][-40:]:
            print(f"::error::[log] {ln.strip()[:300]}")
    return 0 if listo_ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        import traceback
        print("::error::[arranque] CRASH " + traceback.format_exc().replace("\n", " | ")[:1500])
        sys.exit(2)
