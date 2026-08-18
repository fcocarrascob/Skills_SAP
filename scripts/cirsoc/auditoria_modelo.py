"""
auditoria_modelo — radiografía de un modelo de SAP2000 antes de confiar en él.

Recoge los chequeos que en la práctica encuentran errores reales, ordenados
por lo que cuesta descubrirlos a ojo. Todo es de **lectura**: no modifica nada.

Uso:
    from auditoria_modelo import auditar, imprimir
    imprimir(auditar(SapModel))

Cada hallazgo trae severidad y el número por el que se detecta, para poder
pegarlo en un informe sin volver a mirar el modelo:

    {"sev": bloqueante|mayor|menor|info,
     "cat": M|S|C|T,          # ver revision.reporte.CATEGORIAS
     "titulo", "detalle", "ubicacion", "fix"}

`auditar()` devuelve además un bloque `meta` que hace el snapshot
autodescriptivo. Eso importa porque el snapshot se guarda en disco y se lee
después: un resultado de modelo sin su archivo y su fecha al lado es
exactamente el error que costó una conclusión de fundaciones invertida
(bitácora B-45).

Este módulo **no importa `revision`**: el sandbox del MCP bloquea `os` y `sys`,
y el contacto con el disco está aislado en `guardar()`, que sólo se llama desde
fuera. El formato markdown del reporte vive en `revision.reporte`.
"""

from __future__ import annotations

import datetime as _dt

import sap_utils as su

#: Versión del esquema del snapshot. Sube cuando cambie la forma de `auditar()`,
#: para que un snapshot viejo no se lea como si fuera del formato actual.
#:
#: 3 — agrega `geometria`, `pmm`, `holgura`, `diseno.combos_seleccionados` y las
#:     dimensiones/propiedades de `secciones`. Es lo que el optimizador necesita
#:     para justificar qué propiedad hay que comprar en vez de suponerla.
ESQUEMA = 3


# --------------------------------------------------------------------------
# Bloques de la auditoría
# --------------------------------------------------------------------------

def _definiciones(SapModel) -> dict:
    g = lambda fn: list(fn(0, [])[1])
    d = {
        "materiales": g(SapModel.PropMaterial.GetNameList),
        "secciones": g(SapModel.PropFrame.GetNameList),
        "patrones": g(SapModel.LoadPatterns.GetNameList),
        "casos": g(SapModel.LoadCases.GetNameList),
        "funciones": g(SapModel.Func.GetNameList),
        "grupos": g(SapModel.GroupDef.GetNameList),
        "n_combos": int(SapModel.RespCombo.GetNameList(0, [])[0]),
    }
    try:
        d["codigo_acero"] = SapModel.DesignSteel.GetCode("")[0]
    except Exception:
        d["codigo_acero"] = None
    return d


def _secciones(SapModel) -> dict:
    """Peso, dimensiones y propiedades resistentes de cada sección.

    `TotalWt = 0` delata una sección definida pero **no asignada** a ninguna
    barra — típico placeholder olvidado.

    Las dimensiones `d/bf/tf/tw` van acá porque son el único modo de cruzar una
    sección contra el catálogo **dimensión por dimensión**. Cruzar por
    designación no sirve: en la iteración 12 un `W16x77` resultó tener geometría
    de `W16x67` y pasaba todos los controles de nombre.

    `Z33`, `S33` y `A` van porque el D/C no dice qué comprar: si el que manda es
    el momento hace falta módulo plástico, si es la axial hace falta área, y si
    es el pandeo hace falta radio de giro. Sin las tres, cualquier propuesta de
    sección alternativa es una corazonada.
    """
    out = {}
    for f in su.tabla(SapModel, "Frame Section Properties 01 - General"):
        out[f.get("SectionName")] = {
            "material": f.get("Material"),
            "forma": f.get("Shape"),
            "peso_total": su.num(f.get("TotalWt")),
            # dimensiones — para el cruce contra catálogo
            "d": su.num(f.get("t3")),
            "bf": su.num(f.get("t2")),
            "tf": su.num(f.get("tf")),
            "tw": su.num(f.get("tw")),
            # propiedades — para saber qué propiedad hay que comprar
            "A": su.num(f.get("Area")),
            "I33": su.num(f.get("I33")),
            "I22": su.num(f.get("I22")),
            "S33": su.num(f.get("S33")),
            "Z33": su.num(f.get("Z33")),
            "Z22": su.num(f.get("Z22")),
            "J": su.num(f.get("TorsConst")),
            "r33": su.num(f.get("R33")),
            "r22": su.num(f.get("R22")),
        }
    return out


#: Ry y Rt de AISC 341-22 **Tabla A3.2** — "Ry and Rt Values for Steel and Steel
#: Reinforcement Materials", pág. 9.1-6 (pdf 60), leída rasterizada el 2026-08-14.
#:
#: Dos cosas que la edición 2016 no obligaba a distinguir y la 2022 sí:
#:
#: 1. La tabla de Ry/Rt es la **A3.2**. En 341-16 era la A3.1, que en 341-22 pasó
#:    a ser el listado de materiales admitidos. Citar A3.1 hoy apunta a otra tabla.
#: 2. Los valores dependen de la **forma del producto**: un A36 laminado tiene
#:    Ry = 1,5 y el mismo A36 en chapa tiene 1,3. Importa cada vez que hay perfil
#:    armado soldado, que es chapa aunque SAP lo modele como "I/Wide Flange".
#:
#: Clave: (familia, forma) -> (Ry, Rt). Formas: laminado | hss | chapa.
TABLA_A3_2 = {
    ("A36", "laminado"): (1.5, 1.2),   ("A36", "chapa"): (1.3, 1.2),
    ("A529-50", "laminado"): (1.2, 1.2), ("A529-55", "laminado"): (1.1, 1.2),
    ("A572-42", "chapa"): (1.3, 1.0),
    ("A572", "laminado"): (1.1, 1.1),  ("A572", "chapa"): (1.1, 1.2),
    ("A588", "laminado"): (1.1, 1.1),  ("A588", "chapa"): (1.1, 1.2),
    ("A709-36", "laminado"): (1.5, 1.2), ("A709-36", "chapa"): (1.3, 1.2),
    ("A709", "laminado"): (1.1, 1.1),  ("A709", "chapa"): (1.1, 1.2),
    ("A913", "laminado"): (1.1, 1.1),
    ("A992", "laminado"): (1.1, 1.1),
    ("A1043-36", "laminado"): (1.3, 1.1), ("A1043-50", "laminado"): (1.2, 1.1),
    ("A1043-36", "chapa"): (1.3, 1.1),   ("A1043-50", "chapa"): (1.2, 1.1),
    ("A1011", "chapa"): (1.1, 1.1),
    ("A53", "hss"): (1.6, 1.2),
    ("A500-B", "hss"): (1.4, 1.3),     ("A500-C", "hss"): (1.3, 1.2),
    ("A500", "hss"): (1.4, 1.3),       # sin grado declarado: se asume Gr. B
    ("A501", "hss"): (1.4, 1.3),
    ("A1085", "hss"): (1.25, 1.15),
    ("A615-60", "armadura"): (1.2, 1.2), ("A615-80", "armadura"): (1.1, 1.2),
    ("A706", "armadura"): (1.2, 1.2),
}

#: Formas de SAP2000 que sí identifican el producto sin ambigüedad. Una "I/Wide
#: Flange" no sirve: puede ser un laminado de catálogo o un PRS soldado, y el
#: Ry difiere. Cuando no se puede decidir, el chequeo lo dice en vez de elegir.
_FORMA_SAP = {
    "box/tube": "hss", "pipe": "hss", "tube": "hss",
    "angle": "laminado", "channel": "laminado", "double angle": "laminado",
    "double channel": "laminado", "tee": "laminado",
}


def _familias(nombre: str) -> list[str]:
    """Claves de TABLA_A3_2 compatibles con la designación del material.

    Prioriza la más específica: 'A500 Gr.C' antes que 'A500'.
    """
    n = (nombre or "").upper().replace(" ", "")
    cands = {f for (f, _) in TABLA_A3_2 if f.replace("-", "") in n or f in n}
    if not cands:
        cands = {f for (f, _) in TABLA_A3_2 if f.split("-")[0] in n}
    return sorted(cands, key=lambda f: -len(f))


def _Ry(SapModel, secciones: dict) -> dict:
    """Ry = EffFy/Fy y Rt = EffFu/Fu de cada acero, contra AISC 341-22 Tabla A3.2.

    Cruza cada material con las formas de las secciones que lo usan, porque la
    tabla da valores distintos según el producto. Si el material sólo aparece en
    formas ambiguas (una "I/Wide Flange" puede ser laminado o armado soldado),
    se aceptan todos los valores aplicables y se declara el supuesto: es
    preferible a elegir uno y dar por bueno lo que no se verificó.
    """
    formas_por_material: dict[str, set] = {}
    for d in secciones.values():
        mat = (d.get("material") or "").strip()
        forma = _FORMA_SAP.get(str(d.get("forma", "")).strip().lower())
        formas_por_material.setdefault(mat, set()).add(forma)

    out = {}
    for f in su.tabla(SapModel, "Material Properties 03a - Steel Data"):
        nombre = f.get("Material") or ""
        Fy, Fu = su.num(f.get("Fy")), su.num(f.get("Fu"))
        eFy, eFu = su.num(f.get("EffFy")), su.num(f.get("EffFu"))
        if Fy <= 0:
            continue
        ry, rt = eFy / Fy, (eFu / Fu if Fu else 0.0)

        fams = _familias(nombre)
        vistas = formas_por_material.get(nombre.strip(), set())
        concretas = {x for x in vistas if x}
        ambiguo = (None in vistas) or not vistas
        formas = concretas | ({"laminado", "chapa"} if ambiguo else set())

        aplicables = {fo: TABLA_A3_2[(fa, fo)]
                      for fa in fams for fo in formas
                      if (fa, fo) in TABLA_A3_2}
        # Si la designación no dice el grado, la familia genérica ya cubre el caso.
        esp_ry = sorted({v[0] for v in aplicables.values()})
        esp_rt = sorted({v[1] for v in aplicables.values()})

        ok_ry = (not esp_ry) or any(abs(ry - e) < 0.03 for e in esp_ry)
        # Rt sólo se juzga si el material declara Fu; con Fu = 0 no hay razón.
        ok_rt = (not esp_rt) or rt == 0.0 or any(abs(rt - e) < 0.03 for e in esp_rt)

        out[nombre] = {
            "Fy_MPa": round(Fy / 1000, 1),
            "Ry": round(ry, 3), "Rt": round(rt, 3),
            "familias": fams,
            "formas_en_uso": sorted(concretas) or None,
            "forma_ambigua": ambiguo,
            "Ry_aplicables": {k: v[0] for k, v in aplicables.items()},
            "Rt_aplicables": {k: v[1] for k, v in aplicables.items()},
            "Ry_esperado": esp_ry[0] if len(esp_ry) == 1 else None,
            "Rt_esperado": esp_rt[0] if len(esp_rt) == 1 else None,
            "referencia": "AISC 341-22 Tabla A3.2 (pág. 9.1-6)",
            "ok_ry": ok_ry,
            "ok_rt": ok_rt,
            "ok": ok_ry and ok_rt,
        }
    return out


def _mass_source(SapModel) -> dict:
    filas = su.tabla(SapModel, "Mass Source")
    if not filas:
        return {}
    cab = filas[0]
    return {
        "desde_elementos": cab.get("Elements"),
        "desde_masas": cab.get("Masses"),
        "desde_cargas": cab.get("Loads"),
        "patrones": {f.get("LoadPat"): su.num(f.get("Multiplier"))
                     for f in filas if f.get("LoadPat")},
        "masa_total": su.masa_total(SapModel),
    }


def _cargas(SapModel) -> dict:
    """Reacción vertical de cada caso — la forma robusta de saber qué está
    realmente cargado.

    Las tablas `Frame Loads - *` y `Area Loads - Uniform` aparecen vacías
    cuando las cargas se aplicaron como **Uniform to Frame** sobre las áreas,
    que viven en otro canal. Un patrón con reacción 0 está vacío de verdad.
    """
    casos = [c for c in SapModel.LoadCases.GetNameList(0, [])[1]]
    br = su.reacciones_base(SapModel, casos=casos)
    vacios = [k for k, v in br.items()
              if abs(v["FX"]) < 1e-6 and abs(v["FY"]) < 1e-6 and abs(v["FZ"]) < 1e-6]
    try:
        utf = SapModel.AreaObj.GetLoadUniformToFrame(
            "All", 0, [], [], [], [], [], [], su.ItemType.GROUP)
        n_utf = int(utf[0])
    except Exception:
        n_utf = None
    return {"reacciones": {k: {kk: round(vv, 1) for kk, vv in v.items()
                               if kk in ("FX", "FY", "FZ")}
                           for k, v in br.items()},
            "casos_vacios": vacios,
            "asignaciones_area_a_marco": n_utf}


def _sismo(SapModel) -> dict:
    rs = su.tabla(SapModel, "Case - Response Spectrum 1 - General")
    ld = su.tabla(SapModel, "Case - Response Spectrum 2 - Load Assignments")
    out = {
        "casos_espectrales": [
            {"caso": x.get("Case"), "combo_modal": x.get("ModalCombo"),
             "amortiguamiento": su.num(x.get("ConstDamp")),
             "excentricidad": su.num(x.get("EccenRatio"))} for x in rs],
        "asignaciones": [
            {"caso": x.get("Case"), "dir": x.get("LoadName"),
             "funcion": x.get("Function"), "SF": su.num(x.get("TransAccSF"))}
            for x in ld],
    }
    ms = su.modos(SapModel)
    if ms:
        out["n_modos"] = len(ms)
        out["sumas"] = {k: round(ms[-1][k], 4) for k in ("SumUX", "SumUY", "SumUZ")}
        out["dominantes"] = [
            {"modo": m["modo"], "T": round(m["T"], 3),
             "UX": round(m["UX"], 3), "UY": round(m["UY"], 3), "RZ": round(m["RZ"], 3)}
            for m in ms if max(m["UX"], m["UY"], m["RZ"]) > 0.15]
    return out


def _preferencias(SapModel, codigo: str | None) -> dict:
    if not codigo:
        return {}
    filas = su.tabla(SapModel, f"Preferences - Steel Design - {codigo}")
    return filas[0] if filas else {}


def _diseno(SapModel, codigo: str | None) -> dict:
    if not codigo:
        return {"ejecutado": False}
    filas = su.tabla(SapModel, f"Steel Design 1 - Summary Data - {codigo}")
    if not filas:
        return {"ejecutado": False}
    msgs = su.mensajes_diseno(SapModel, filas)
    return {"ejecutado": True, "n_barras": len(filas),
            "por_seccion": su.resumen_diseno(SapModel, filas),
            "sin_disenar": su.barras_sin_disenar(SapModel, filas),
            "combos_seleccionados": _combos_de_diseno(SapModel),
            "mensajes": [{"tipo": t, "mensaje": m, **d}
                         for (t, m), d in sorted(msgs.items(),
                                                 key=lambda kv: -kv[1]["n"])]}


def _combos_de_diseno(SapModel) -> dict:
    """Qué combinaciones entraron efectivamente en el diseño de resistencia.

    Un D/C sin la lista de combos que lo produjo no es reproducible. En este
    proyecto la diferencia es material: las combinaciones de sobrerresistencia
    `S3`/`S4` estaban **generadas pero deseleccionadas**, y con ellas dos
    riostras pasan de 0,678 a 1,148. El snapshot tiene que dejar ver cuál de
    las dos corridas está mirando.

    TRAMPA DE FIRMA: `GetComboStrength` **no** consulta un combo por nombre.
    Devuelve la lista completa de los seleccionados: la firma es
    `(NumberItems, MyName)` y se llama con `(0, [])`. Pasarle un nombre falla
    con `'str' object cannot be interpreted as an integer`, que no se parece en
    nada al error real.
    """
    try:
        todos = set(SapModel.RespCombo.GetNameList(0, [])[1])
        r = SapModel.DesignSteel.GetComboStrength(0, [])
        dentro = set(r[1])
    except Exception as e:
        return {"legible": False, "nota": f"{type(e).__name__}: {e}"}
    fuera = todos - dentro
    return {"legible": True, "n_dentro": len(dentro), "n_fuera": len(fuera),
            "dentro": sorted(dentro), "fuera": sorted(fuera)}


def _limite_dc(prefs: dict) -> float | None:
    """El techo real del diseño, que no tiene por qué ser 1,0.

    `SRatioLimit` es el valor contra el que SAP declara que una barra falla. Si
    está en 0,95, un D/C de 0,949 **no tiene 5 % de margen**: está al borde. Y
    la holgura del optimizador tiene que medirse contra ese número, no contra 1.
    """
    v = prefs.get("SRatioLimit")
    return su.num(v) if v not in (None, "") else None


# --------------------------------------------------------------------------

def auditar(SapModel) -> dict:
    SapModel.SetPresentUnits(su.Units.kN_m_C)
    defs = _definiciones(SapModel)
    cod = defs.get("codigo_acero")
    archivo = SapModel.GetModelFilename(True)
    secs = _secciones(SapModel)   # el chequeo de Ry necesita la forma del producto
    a = {
        "meta": {
            "esquema": ESQUEMA,
            "archivo": archivo,
            "fecha": _dt.datetime.now().isoformat(timespec="seconds"),
            "unidades": "kN, m, C",
        },
        "archivo": archivo,
        "bloqueado": SapModel.GetModelIsLocked(),
        "inventario": su.inventario(SapModel),
        "definiciones": defs,
        "secciones": secs,
        "aceros": _Ry(SapModel, secs),
        "mass_source": _mass_source(SapModel),
        "cargas": _cargas(SapModel),
        "sismo": _sismo(SapModel),
        "preferencias": _preferencias(SapModel, cod),
        "liberaciones": su.liberaciones_por_seccion(SapModel),
        "arriostramiento": su.liberaciones_arriostramiento(SapModel),
        "overwrites_fy": su.overwrites_fy_sospechosos(SapModel),
        "nodos_huerfanos": su.nodos_huerfanos(SapModel),
        "diseno": _diseno(SapModel, cod),
    }
    a["geometria"] = su.geometria_barras(SapModel)
    a["pmm"] = su.detalle_pmm(SapModel, cod) if cod else {"tabla": None, "barras": []}
    lim = _limite_dc(a["preferencias"])
    a["holgura"] = su.holgura_por_seccion(
        a["diseno"].get("por_seccion") or {}, secs, a["geometria"],
        limite=lim if lim else 1.0)
    a["hallazgos"] = _hallazgos(a)
    return a


def _hallazgos(a: dict) -> list[dict]:
    """Traduce la radiografía a una lista de hallazgos accionables.

    La categoría (`M` modelo, `S` sismo, `C` capacidad, `T` trazabilidad) dice
    qué revisor es dueño del hallazgo. La severidad la fija este código y
    ningún agente puede bajarla después: es lo que impide que un D/C de 1,25
    con una explicación plausible termine reclasificado como observación menor.
    """
    H: list[dict] = []

    def add(sev, cat, tit, det="", ubicacion="", fix=""):
        H.append({"sev": sev, "cat": cat, "titulo": tit, "detalle": det,
                  "ubicacion": ubicacion, "fix": fix})

    ow = a.get("overwrites_fy") or []
    if ow:
        det = " · ".join(f"{x['barra']} ({x['seccion']}: {x['valor']:.0f} vs "
                         f"{x['fy_material']:.0f}, ×{x['razon']})" for x in ow[:4])
        add("bloqueante", "M",
            f"{len(ow)} barras con override manual de Fy fuera de su material",
            f"`ProgDet=False` y valor que no coincide con el acero de la sección. "
            f"El diseño se corre con ese Fy y el D/C sale holgado sin que nada "
            f"avise. {det}", "overwrites de diseño",
            "Borrar el override y rediseñar; comprobar el D/C real después.")

    inv = a["inventario"]
    if inv.get("links"):
        add("info", "M", f"{inv['links']} links en el modelo",
            "No los ve FrameObj.GetNameList. Verificar su propiedad y su masa.",
            "inventario")

    for s, d in a["secciones"].items():
        if d["peso_total"] == 0:
            add("mayor", "M", f"Sección '{s}' definida pero sin asignar",
                "TotalWt = 0. Placeholder olvidado o sección pendiente de usar.",
                f"sección {s}", "Borrarla, o asignarla si estaba pendiente.")

    for m, d in a["aceros"].items():
        if not d.get("ok_ry", True):
            aplic = d.get("Ry_aplicables") or {}
            add("mayor", "M", f"Ry fuera de tabla en '{m}': {d['Ry']}",
                f"{d['referencia']} da " +
                " · ".join(f"{v} ({k})" for k, v in sorted(aplic.items())) +
                ". Afecta todo diseño por capacidad.",
                f"material {m}",
                "Fijar EffFy = Ry·Fy con el Ry de la forma que corresponde.")
        if not d.get("ok_rt", True):
            aplic = d.get("Rt_aplicables") or {}
            add("mayor", "M", f"Rt fuera de tabla en '{m}': {d['Rt']}",
                f"{d['referencia']} da " +
                " · ".join(f"{v} ({k})" for k, v in sorted(aplic.items())) +
                ". Rt gobierna los estados límite de rotura (bloque de corte, "
                "rotura de sección neta), no la fluencia: pasa inadvertido si "
                "sólo se mira Ry.",
                f"material {m}", "Fijar EffFu = Rt·Fu.")
        if d["ok"] and d.get("forma_ambigua") and len(set(
                (d.get("Ry_aplicables") or {}).values())) > 1:
            add("info", "M", f"Ry de '{m}' aceptado con supuesto de forma",
                f"Supuesto: no se pudo determinar si es laminado o chapa desde el "
                f"modelo (SAP declara ambos como I/Wide Flange). Aplicables: " +
                " · ".join(f"{v} ({k})" for k, v in
                           sorted((d.get('Ry_aplicables') or {}).items())) +
                f". El modelo usa {d['Ry']}. Confirmar si hay perfil armado soldado.",
                f"material {m}")

    ms = a["mass_source"]
    if ms and ms.get("desde_elementos") == "No" and not ms.get("patrones"):
        add("bloqueante", "S", "El mass source no tiene fuente de masa", "",
            "Mass Source", "Definir masa desde elementos o desde patrones.")
    for p, sf in (ms.get("patrones") or {}).items():
        if p.upper().startswith(("PP", "DEAD")) and sf < 1.0:
            add("mayor", "S", f"Peso propio '{p}' entra a la masa con factor {sf}",
                "Un peso propio debería entrar con 1,0.",
                "Mass Source", f"Subir el multiplicador de '{p}' a 1,0.")

    vac = [c for c in a["cargas"]["casos_vacios"] if c.upper() not in ("MODAL", "TEMP")]
    if vac:
        add("mayor", "M", f"{len(vac)} casos sin carga: {', '.join(vac[:8])}",
            "Reacción nula en las tres direcciones.", "casos de carga",
            "Cargarlos, o borrarlos si quedaron de una iteración anterior.")

    for c in a["sismo"].get("casos_espectrales", []):
        if c["excentricidad"] == 0:
            add("menor", "S", f"Excentricidad accidental = 0 en '{c['caso']}'",
                "CIRSOC 103 Tabla 6.3 lo admite sólo si se verifica la "
                "regularidad torsional de la Tabla 2.3.",
                f"caso {c['caso']}",
                "Cargar 5 % de excentricidad, o dejar constancia de la "
                "verificación de regularidad.")
    sm = a["sismo"].get("sumas") or {}
    for k, lbl in (("SumUX", "X"), ("SumUY", "Y")):
        if sm.get(k) is not None and sm[k] < 0.90:
            add("bloqueante", "S", f"Masa participante en {lbl} = {sm[k]:.1%}",
                "CIRSOC 103 §7.2.3 exige >= 90 %.", "análisis modal",
                "Subir el número de modos y volver a correr.")

    pref = a["preferencias"]
    if pref:
        if pref.get("Provision") == "ASD":
            add("bloqueante", "C", "Preferencias de diseño en ASD",
                "CIRSOC 103 §3.7.1 sólo formula combinaciones últimas: la base es LRFD.",
                "preferencias de diseño", "Cambiar Provision a LRFD y rediseñar.")
        if pref.get("CheckDefl") == "No":
            add("mayor", "C", "Verificación de flechas desactivada", "",
                "preferencias de diseño", "Activar CheckDefl y fijar los límites.")
        if su.num(pref.get("SystemR")) not in (0, 3.0, 4.0, 4.5, 5.0, 6.0, 7.0, 1.5, 2.5, 3.5):
            add("mayor", "S", f"R = {pref.get('SystemR')} en las preferencias",
                "No coincide con ningún valor de la Tabla 5.1 de CIRSOC 103.",
                "preferencias de diseño",
                "Fijar el R de la fila de Tabla 5.1 que corresponde al sistema.")
        if pref.get("SOMethod") == "General 2nd Order":
            add("menor", "M", "Second Order = General 2nd Order",
                "Requiere un caso no lineal P-Δ. Con casos lineales usar "
                "Amplified 1st Order.", "preferencias de diseño")

    for s, d in a.get("arriostramiento", {}).items():
        rigidos = d["conexion"] - d["conexion_rotulados"]
        if rigidos:
            add("bloqueante", "M",
                f"'{s}': {rigidos} de {d['conexion']} extremos de conexión sin rótula",
                "Una diagonal con el extremo de conexión rígido toma flexión del "
                "drift y el chequeo PMM se dispara por momento, no por axial. "
                f"P. ej. {', '.join(d['conexion_rigidos'][:4])}",
                f"sección {s}", "Liberar M2 y M3 en el extremo que llega a la "
                                "columna o a la viga.")
        # En los nudos internos —donde la diagonal se partió para armar la X— la
        # señal NO es el valor absoluto. Que estén todos rotulados es una
        # decisión de modelado coherente (un tirante de solo axial admite la
        # rótula intermedia); que estén todos rígidos también lo es. Lo que
        # delata que alguien tocó algo es la **minoría que difiere del resto de
        # su propia familia**: fue así como aparecieron los 12 nudos sin rigidez
        # fuera de plano que invalidaron el modal en la iteración 6.
        nr, ni = d["internos_rotulados"], d["internos"]
        if ni and 0 < nr < ni:
            minoria, criterio = ((nr, "rotulados") if nr * 2 <= ni
                                 else (ni - nr, "rígidos"))
            add("mayor", "M",
                f"'{s}': {minoria} de {ni} nudos internos difieren del resto",
                f"En esta sección {nr} nudos de división están rotulados y "
                f"{ni - nr} rígidos. La mezcla dentro de una misma familia suele "
                f"ser una liberación copiada de más o de menos, no una decisión. "
                f"Los {criterio} son la minoría. "
                f"P. ej. {', '.join(d['internos_rotulados_ej'][:4])}",
                f"sección {s}",
                "Unificar el criterio en toda la familia, o justificar la excepción.")
        elif ni and nr == ni:
            add("info", "M",
                f"'{s}': los {ni} nudos internos de cruce están rotulados",
                "Supuesto: se modela como tirante de solo axial, donde la rótula "
                "intermedia es admisible. Si la diagonal debe tomar compresión, el "
                "cruce necesita rigidez fuera de plano.",
                f"sección {s}")

    huer = a["nodos_huerfanos"]
    if huer:
        add("mayor", "M", f"{len(huer)} nodos sin ninguna barra",
            f"P. ej. {huer[0][0]} en {huer[0][1]}. Pueden tener links o estar sueltos.",
            "geometría", "Borrarlos, o confirmar que sostienen un link.")

    if not a["diseno"]["ejecutado"]:
        add("bloqueante", "C", "El diseño de acero nunca se ejecutó", "",
            "diseño de acero", "Correr StartDesign() tras DeleteResults().")
    else:
        sd = a["diseno"].get("sin_disenar") or []
        if sd:
            motivos = sorted({str(x["error"]) for x in sd})
            add("bloqueante", "C",
                f"{len(sd)} barras que SAP NO pudo diseñar",
                "No tienen ratio: pasan inadvertidas si se lee sólo el D/C máximo. "
                + " · ".join(motivos[:2]),
                f"p. ej. {', '.join(str(x['frame']) for x in sd[:4])}",
                "Resolver el motivo (esbeltez, Pu > Pe) antes de dar el diseño "
                "por cerrado.")
        # Los mensajes del diseño se leen aparte del ratio: un Error de
        # compacidad sísmica convive con un D/C perfectamente calculado, así que
        # mirar sólo el ratio lo deja pasar.
        for m in a["diseno"].get("mensajes", []):
            secs = ", ".join(f"{s} ({n})" for s, n in
                             sorted(m["secciones"].items(), key=lambda kv: -kv[1]))
            add("bloqueante" if m["tipo"] == "ERROR" else "menor", "C",
                f"{m['n']} barras con {m['tipo'].lower()} de diseño: {m['mensaje'][:90]}",
                f"Secciones: {secs}. P. ej. {', '.join(m['ejemplos'][:3])}. "
                "Convive con un D/C calculado: no aparece mirando el ratio.",
                "diseño de acero")

        exc = sum(d["excedidas"] for d in a["diseno"]["por_seccion"].values())
        if exc:
            peores = [f"{s} (D/C {d['max']}, {d['peor']}, {d['combo']})"
                      for s, d in a["diseno"]["por_seccion"].items()
                      if d["excedidas"]][:3]
            add("mayor", "C", f"{exc} barras con D/C > 1,0",
                " · ".join(peores), "diseño de acero")
    return H


# --------------------------------------------------------------------------

_SEV = {"bloqueante": "[!!]", "mayor": "[! ]", "menor": "[ ~]", "info": "[ i]"}


def imprimir(a: dict) -> None:
    print(f"\n{a['archivo']}")
    print(f"  bloqueado: {a['bloqueado']}   {a['inventario']}")
    d = a["definiciones"]
    print(f"  {len(d['secciones'])} secciones · {len(d['patrones'])} patrones · "
          f"{len(d['casos'])} casos · {d['n_combos']} combinaciones · {d['codigo_acero']}")
    if a["mass_source"]:
        print(f"  masa sísmica: {a['mass_source']['masa_total']:.1f}")
    sm = a["sismo"].get("sumas")
    if sm:
        print(f"  modos: {a['sismo'].get('n_modos')} · ΣUX {sm['SumUX']:.1%} "
              f"· ΣUY {sm['SumUY']:.1%} · ΣUZ {sm['SumUZ']:.1%}")
    print(f"\n  {len(a['hallazgos'])} hallazgos")
    orden = {"bloqueante": 0, "mayor": 1, "menor": 2, "info": 3}
    for h in sorted(a["hallazgos"], key=lambda x: orden[x["sev"]]):
        cat = h.get("cat") or "-"
        print(f"  {_SEV[h['sev']]} {cat}  {h['titulo']}")
        if h["detalle"]:
            print(f"           {h['detalle']}")


def guardar(a: dict, ruta: str) -> str:
    """Persiste el snapshot como JSON y devuelve la ruta absoluta.

    El `mtime` del `.sdb` se sella acá porque es la única forma de detectar
    después que el snapshot quedó viejo: un resultado de modelo leído como
    vigente cuando ya no lo es fue exactamente lo que invirtió una conclusión
    de fundaciones (bitácora B-45).

    Importa `os`/`json` dentro de la función a propósito: el sandbox del MCP
    los bloquea, y así el módulo se sigue pudiendo importar allí aunque esta
    función no se pueda usar.
    """
    import json
    import os

    sdb = a.get("archivo") or ""
    meta = a.setdefault("meta", {})
    meta.setdefault("esquema", ESQUEMA)
    meta["archivo"] = sdb
    if sdb and os.path.exists(sdb):
        st = os.stat(sdb)
        meta["sdb_mtime"] = _dt.datetime.fromtimestamp(st.st_mtime).isoformat(
            timespec="seconds")
        meta["sdb_bytes"] = st.st_size
    else:
        meta["sdb_mtime"] = None
        meta["sdb_bytes"] = None

    carpeta = os.path.dirname(os.path.abspath(ruta))
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2, default=str)
    return os.path.abspath(ruta)


if __name__ == "__main__":
    try:
        import comtypes.client
        sap = comtypes.client.GetActiveObject("CSI.SAP2000.API.SapObject")
        imprimir(auditar(sap.SapModel))
    except Exception as e:
        print("No se pudo conectar a SAP2000:", e)
        print("Desde el MCP: from auditoria_modelo import auditar, imprimir; "
              "imprimir(auditar(SapModel))")
