"""
revision.cli — la única superficie que los agentes revisores invocan por consola.

Todo subcomando acepta `--json` y escribe a stdout: los agentes **parsean**, no
interpretan texto libre. Un revisor que tiene que adivinar el formato de salida
inventa hallazgos.

    $env:PYTHONPATH = "C:\\Proyectos_Python\\Skills_SAP\\scripts"
    & "C:\\Proyectos_Python\\Skills_SAP\\.venv\\Scripts\\python.exe" -m revision.cli verificar

Códigos de salida: 0 todo bien · 1 el chequeo falló · 2 error de uso o de entorno.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

from . import SCRIPTS
from . import reporte

CIRSOC = os.path.join(SCRIPTS, "cirsoc")
VERIFICAR_CIRSOC = os.path.join(CIRSOC, "verificar_cirsoc.py")


def _utf8():
    """Windows abre la consola en cp1252 y los emoji de severidad la revientan
    con UnicodeEncodeError. Sin esto, `verificar` falla por imprimir un 🔴."""
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _salida(datos, como_json: bool, texto: str = "") -> None:
    if como_json:
        print(json.dumps(datos, ensure_ascii=False, indent=2, default=str))
    else:
        print(texto or datos)


# --------------------------------------------------------------------------
# verificar — smoke test del entorno y de la lógica normativa
# --------------------------------------------------------------------------

def cmd_verificar(args) -> int:
    """Se corre al inicio de cada pasada de revisión.

    Cubre las dos formas de romperse en silencio que tiene este montaje: que
    `Skills_SAP` se haya movido, y que el `__init__.py` del paquete haya roto
    el import plano del que depende el sandbox del MCP.
    """
    res: list[dict] = []

    def chk(etiqueta, ok, detalle=""):
        res.append({"chequeo": etiqueta, "ok": bool(ok), "detalle": str(detalle)})

    chk("scripts/ existe", os.path.isdir(SCRIPTS), SCRIPTS)
    chk("cirsoc/ existe", os.path.isdir(CIRSOC), CIRSOC)

    try:
        chk("reporte.sev_emoji('bloqueante') == 🔴",
            reporte.sev_emoji("bloqueante") == "🔴")
        vd = reporte.veredicto([{"sev": "bloqueante", "cat": "C", "titulo": "x"}])
        chk("un bloqueante deja el veredicto en ❌", vd.startswith("❌"), vd)
        vd0 = reporte.veredicto([])
        chk("sin hallazgos el veredicto es ✅", vd0.startswith("✅"), vd0)
    except Exception as e:  # noqa: BLE001
        chk("reporte importable", False, e)

    # El contrato con el sandbox del MCP: `import auditoria_modelo` PLANO.
    # Se prueba en un intérprete aparte para que el sys.path de este proceso
    # no lo haga pasar por casualidad.
    entorno = dict(os.environ, PYTHONPATH=CIRSOC)
    plano = subprocess.run(
        [sys.executable, "-c", "import auditoria_modelo, sap_utils; print('ok')"],
        capture_output=True, text=True, env=entorno, cwd=SCRIPTS)
    chk("import plano de auditoria_modelo (contrato del sandbox MCP)",
        plano.returncode == 0, (plano.stderr or plano.stdout).strip()[-300:])

    paquete = subprocess.run(
        [sys.executable, "-c",
         "import cirsoc; cirsoc.auditoria_modelo; print('ok')"],
        capture_output=True, text=True,
        env=dict(os.environ, PYTHONPATH=SCRIPTS), cwd=SCRIPTS)
    chk("import de cirsoc como paquete",
        paquete.returncode == 0, (paquete.stderr or paquete.stdout).strip()[-300:])

    try:
        import pymupdf  # noqa: F401
        chk("pymupdf disponible (lector de normas)", True)
    except ImportError as e:
        chk("pymupdf disponible (lector de normas)", False, e)

    if os.path.isfile(VERIFICAR_CIRSOC):
        vc = subprocess.run([sys.executable, VERIFICAR_CIRSOC],
                            capture_output=True, text=True,
                            env=entorno, cwd=CIRSOC)
        cola = (vc.stdout or "").strip().splitlines()[-1:] or [""]
        chk("aserciones de verificar_cirsoc.py", vc.returncode == 0, cola[0])
        if args.verbose and vc.stdout:
            print(vc.stdout)
    else:
        chk("verificar_cirsoc.py presente", False, VERIFICAR_CIRSOC)

    fallos = [r for r in res if not r["ok"]]
    if args.json:
        _salida({"ok": not fallos, "chequeos": res}, True)
    else:
        for r in res:
            print(f"  [{'OK  ' if r['ok'] else 'FALLA'}] {r['chequeo']}"
                  + (f"   {r['detalle']}" if r["detalle"] and not r["ok"] else ""))
        print(f"\n{len(res) - len(fallos)}/{len(res)} chequeos en verde.")
    return 1 if fallos else 0


# --------------------------------------------------------------------------
# auditar — snapshot del modelo abierto en SAP2000
# --------------------------------------------------------------------------

def cmd_auditar(args) -> int:
    """Produce el snapshot que después leen los revisores.

    Corre **fuera** del sandbox del MCP a propósito: necesita escribir un
    archivo, y el sandbox no permite E/S. Es también el motivo por el que un
    solo proceso habla con SAP2000: la conexión COM es de instancia única y
    varios revisores en paralelo se pisarían.
    """
    try:
        import comtypes.client
    except ImportError as e:
        print(f"comtypes no disponible: {e}", file=sys.stderr)
        return 2

    try:
        sap = comtypes.client.GetActiveObject("CSI.SAP2000.API.SapObject")
    except Exception as e:  # noqa: BLE001
        print("No se pudo conectar a SAP2000 (¿está abierto con el modelo "
              f"cargado?): {e}", file=sys.stderr)
        return 2

    sys.path.insert(0, CIRSOC)
    import auditoria_modelo as am

    a = am.auditar(sap.SapModel)
    if args.commit:
        a.setdefault("meta", {})["commit"] = args.commit

    destino = args.json_out
    if not destino:
        base = os.path.splitext(os.path.basename(a.get("archivo") or "modelo"))[0]
        fecha = a["meta"]["fecha"][:10]
        destino = f"snapshot_{base}_{fecha}.json"
    ruta = am.guardar(a, destino)

    c = reporte.conteo(a["hallazgos"])
    print(f"{ruta}")
    print(f"  {a['archivo']}")
    print(f"  {sum(c.values())} hallazgos · " +
          " · ".join(f"{c[s]} {s}" for s in reporte.SEVERIDADES if c[s]))
    if args.imprimir:
        am.imprimir(a)
    return 0


# --------------------------------------------------------------------------
# diff — qué cambió entre dos snapshots
# --------------------------------------------------------------------------

def cmd_diff(args) -> int:
    """Lo que el modelador devuelve al cerrar un cambio.

    Un cambio que agrega hallazgos se reporta como tal aunque el D/C haya
    bajado: bajar un ratio ensuciando el modelo no es una mejora.
    """
    d = reporte.diff_hallazgos(reporte.cargar_json(args.antes),
                               reporte.cargar_json(args.despues))
    if args.json:
        _salida(d, True)
    else:
        print(reporte.diff_a_markdown(d))
    return 1 if d["nuevos"] else 0


# --------------------------------------------------------------------------
# perfil / norma — lo que usa el revisor normativo
# --------------------------------------------------------------------------

def _perfil_de(args):
    from . import perfil as _p
    ruta = getattr(args, "perfil", None) or _p.buscar_perfil(os.getcwd())
    return _p.cargar(ruta)


def cmd_perfil(args) -> int:
    p = _perfil_de(args)
    r = p.resumen()
    if args.json:
        r["normas_detalle"] = {k: vars(n) for k, n in p.normas.items()}
        r["sistema"] = p.sistema
        _salida(r, True)
        return 0
    print(f"{p.proyecto}  ({p.pais}, base {p.base}, "
          f"módulo sísmico: {p.modulo_sismico or '— ninguno: el revisor sísmico degrada a 🔵'})")
    print(f"  perfil : {p.ruta_json}")
    print(f"  modelo : {p.modelo_vigente or '—'}")
    print(f"  {len(p.normas)} normas declaradas\n")
    for k in p.claves():
        n = p.norma(k)
        print(f"  {'✓' if n.existe else '✗'} {k:10s} {n.titulo[:58]:58s} "
              f"{n.edicion:24s} off {n.offset_pagina:+d}")
    falt = p.faltantes()
    if falt:
        print(f"\n  ⚠️ {len(falt)} sin PDF en disco: " +
              ", ".join(n.clave for n in falt))
        print("     Toda cita a estas normas es 🔵 no verificable hasta conseguirlas.")
    return 0


def cmd_norma(args) -> int:
    from . import normas_pdf as npdf
    p = _perfil_de(args)

    if args.accion == "info":
        claves = [args.clave] if args.clave else p.claves()
        datos = []
        for k in claves:
            try:
                datos.append(npdf.info(k, p))
            except FileNotFoundError as e:
                datos.append({"clave": k, "error": str(e)})
        if args.json:
            _salida(datos, True)
        else:
            for d in datos:
                if "error" in d:
                    print(f"  ✗ {d['clave']:10s} {d['error'][:110]}")
                    continue
                marca = "⚠️ ESCANEADO" if d["escaneado"] else "texto ok"
                print(f"  {d['clave']:10s} {d['paginas']:5d} pág · "
                      f"texto {d['fraccion_con_texto']:.0%} · {marca:12s} "
                      f"{d['titulo'][:52]}")
        return 0

    if args.accion == "offset":
        claves = [args.clave] if args.clave else p.claves()
        datos = []
        for k in claves:
            try:
                datos.append(npdf.detectar_offset(k, p))
            except FileNotFoundError as e:
                datos.append({"clave": k, "error": str(e)})
        if args.json:
            _salida(datos, True)
        else:
            for d in datos:
                if "error" in d:
                    print(f"  ✗ {d['clave']:10s} sin PDF")
                    continue
                print(f"  {d['clave']:10s} sugerido {str(d['offset_sugerido']):>5s} "
                      f"· confianza {d.get('confianza', 0):.0%} "
                      f"· declarado {d.get('declarado')} "
                      f"{'✓' if d.get('coincide') else '← revisar'}")
            print("\n  Confirmar mirando una página rasterizada antes de escribirlo "
                  "en el perfil.")
        return 0

    if args.accion == "buscar":
        hits = (npdf.buscar(args.clave, args.patron, p, regex=args.regex,
                            max_hits=args.max)
                if args.patron else
                npdf.buscar_articulo(args.clave, args.articulo, p,
                                     max_hits=args.max))
        if args.json:
            _salida([h.dict() for h in hits], True)
        else:
            if not hits:
                print("  sin resultados — si el PDF está escaneado, rasterizar y mirar")
            for h in hits:
                print(f"  pdf {h.pagina_pdf:4d} (impresa {h.pagina_impresa:4d}) "
                      f"×{h.ocurrencias}  {h.contexto[:150]}")
        return 0 if hits else 1

    if args.accion == "leer":
        png = npdf.rasterizar(args.clave, args.pagina, p, dpi=args.dpi,
                              impresa=not args.pdf_pagina,
                              recorte=tuple(args.recorte) if args.recorte else None)
        if args.json:
            _salida({"png": png, "clave": args.clave, "pagina": args.pagina,
                     "impresa": not args.pdf_pagina, "dpi": args.dpi}, True)
        else:
            print(png)
        return 0

    if args.accion == "verificar":
        ev = npdf.verificar_cita(args.clave, args.articulo, p, dpi=args.dpi,
                                 afirmacion=args.afirmacion or "")
        _salida(ev, True)
        return 0 if ev.get("existe") else 1

    print(f"acción desconocida: {args.accion}", file=sys.stderr)
    return 2


# --------------------------------------------------------------------------

def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m revision.cli",
        description="Herramientas deterministas del panel de revisión estructural.")
    sub = p.add_subparsers(dest="comando", required=True)

    v = sub.add_parser("verificar", help="smoke test del entorno; corre sin SAP")
    v.add_argument("--json", action="store_true")
    v.add_argument("-v", "--verbose", action="store_true",
                   help="vuelca la salida completa de verificar_cirsoc.py")
    v.set_defaults(func=cmd_verificar)

    a = sub.add_parser("auditar", help="snapshot del modelo abierto en SAP2000")
    a.add_argument("--json", dest="json_out", metavar="RUTA",
                   help="destino del snapshot (por defecto, junto al cwd con "
                        "nombre snapshot_<modelo>_<fecha>.json)")
    a.add_argument("--commit", help="sha corto del repo de proyectos, para sellar el snapshot")
    a.add_argument("--imprimir", action="store_true", help="además, radiografía por consola")
    a.set_defaults(func=cmd_auditar)

    d = sub.add_parser("diff", help="compara dos snapshots")
    d.add_argument("--antes", required=True)
    d.add_argument("--despues", required=True)
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_diff)

    # -- perfil normativo del proyecto --------------------------------
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument("--perfil", metavar="PERFIL.json",
                       help="por defecto, el PERFIL.json más cercano subiendo "
                            "desde el directorio actual")
    comun.add_argument("--json", action="store_true")

    pf = sub.add_parser("perfil", parents=[comun],
                        help="qué normas y qué sistema declara el proyecto")
    pf.set_defaults(func=cmd_perfil)

    nm = sub.add_parser("norma", parents=[comun], help="leer un reglamento en PDF")
    nsub = nm.add_subparsers(dest="accion", required=True)

    # `comun` va también en cada acción: argparse no pasa las opciones del
    # padre cuando aparecen después del subcomando, y escribir
    # `norma --perfil X info` en vez de `norma info --perfil X` es una trampa
    # que nadie recuerda.
    ni = nsub.add_parser("info", parents=[comun],
                         help="páginas y si tiene capa de texto buscable")
    ni.add_argument("--clave", help="una norma; sin esto, todas las del perfil")

    no = nsub.add_parser("offset", parents=[comun],
                         help="estimar el desfase página impresa ↔ visor")
    no.add_argument("--clave")

    nb = nsub.add_parser("buscar", parents=[comun],
                         help="localizar un artículo o un patrón")
    nb.add_argument("--clave", required=True)
    nb.add_argument("--articulo", help="'§7.2.5', 'Tabla 5.1', '[3.14]', 'A3.1'")
    nb.add_argument("--patron", help="texto o regex libre")
    nb.add_argument("--regex", action="store_true")
    nb.add_argument("--max", type=int, default=12)

    nl = nsub.add_parser(
        "leer", parents=[comun],
        help="rasterizar una página a PNG — la ÚNICA vía válida para "
             "leer una ecuación, un coeficiente o una celda de tabla")
    nl.add_argument("--clave", required=True)
    nl.add_argument("--pagina", type=int, required=True)
    nl.add_argument("--pdf-pagina", action="store_true",
                    help="la página es la del visor, no la impresa")
    nl.add_argument("--dpi", type=int, default=220)
    nl.add_argument("--recorte", type=float, nargs=4, metavar=("X0", "Y0", "X1", "Y1"),
                    help="fracciones de página, para ampliar una tabla")

    nv = nsub.add_parser("verificar", parents=[comun],
                         help="evidencia de una cita (dónde está + PNG)")
    nv.add_argument("--clave", required=True)
    nv.add_argument("--articulo", required=True)
    nv.add_argument("--afirmacion", help="lo que el documento sostiene, para el registro")
    nv.add_argument("--dpi", type=int, default=220)

    nm.set_defaults(func=cmd_norma)

    return p


def main(argv=None) -> int:
    _utf8()
    args = construir_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
