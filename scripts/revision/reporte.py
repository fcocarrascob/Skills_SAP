"""
reporte — severidades, formato del bloque de revisión y persistencia de snapshots.

Sin norma y sin SAP: transforma listas de hallazgos en el markdown que los
agentes devuelven y que la skill `revisar` archiva sin reescribir.

Dos decisiones que conviene no deshacer:

1. **Las severidades en Python no llevan emoji.** El código emite
   `bloqueante | mayor | menor | info` —lo que `auditoria_modelo` ya usaba— y
   el emoji se agrega sólo al dar formato. Así un hallazgo determinista viaja
   con su severidad intacta y ningún agente puede reclasificarlo por el camino.
2. **`bloque_reporte` obliga a declarar lo verificado y lo no cubierto.** Un
   reporte que sólo lista errores no distingue *revisado y correcto* de *no
   mirado*, y ese es justamente el dato que hace utilizable una revisión.
"""

from __future__ import annotations

import json

# --------------------------------------------------------------------------
# Escalas
# --------------------------------------------------------------------------

#: Severidades válidas, de mayor a menor. Mapa 1:1 con `auditoria_modelo`.
SEVERIDADES = ("bloqueante", "mayor", "menor", "info")

EMOJI = {"bloqueante": "🔴", "mayor": "🟠", "menor": "🟡", "info": "🔵"}
ORDEN = {s: i for i, s in enumerate(SEVERIDADES)}

#: Criterio de cada severidad, en términos de ingeniería. Se repite en los
#: prompts de los agentes; acá vive la versión canónica.
CRITERIO = {
    "bloqueante": "Invalida un resultado ya emitido, o un número usado para "
                  "defender una decisión. No se entrega ni se cita así.",
    "mayor": "Inconsistencia real que un revisor externo puede refutar, pero "
             "que no invalida el diseño por sí sola.",
    "menor": "Redondeo, nomenclatura, formato, precisión declarada de más.",
    "info": "Nota, o no verificable con lo disponible. Nunca se marca como "
            "error lo que no se pudo comprobar.",
}

#: Categorías de hallazgo. Cada letra responde una pregunta distinta sobre el
#: mismo número, por eso no se solapan.
CATEGORIAS = {
    "N": "Número — ¿la aritmética cierra y el valor es el mismo en todas sus apariciones?",
    "D": "Dato de origen — ¿de dónde salió, y la fuente dice eso?",
    "M": "Modelo — ¿el modelo que produjo el número es sano?",
    "S": "Sismo — ¿la demanda sísmica es la correcta?",
    "C": "Capacidad — ¿la capacidad alcanza y es real?",
    "T": "Trazabilidad — ¿es reproducible y vigente?",
}

ESTADO_ABIERTO = "⬜"


def sev_emoji(sev: str) -> str:
    """Emoji de una severidad. Una severidad desconocida no se silencia."""
    if sev not in EMOJI:
        raise ValueError(f"severidad desconocida: {sev!r}; válidas: {SEVERIDADES}")
    return EMOJI[sev]


def normalizar(h: dict) -> dict:
    """Completa los campos opcionales de un hallazgo.

    `auditoria_modelo` emitía `{sev, titulo, detalle}`; el contrato completo
    agrega `cat`, `ubicacion` y `fix`. Los que falten quedan vacíos en vez de
    romper el formato.
    """
    sev = h.get("sev", "info")
    if sev not in EMOJI:
        raise ValueError(f"severidad desconocida: {sev!r} en {h.get('titulo')!r}")
    cat = (h.get("cat") or "").upper()
    if cat and cat not in CATEGORIAS:
        raise ValueError(f"categoría desconocida: {cat!r} en {h.get('titulo')!r}")
    return {
        "sev": sev,
        "cat": cat,
        "titulo": h.get("titulo", ""),
        "detalle": h.get("detalle", ""),
        "ubicacion": h.get("ubicacion", ""),
        "fix": h.get("fix", ""),
    }


def clave(h: dict) -> tuple:
    """Identidad de un hallazgo para comparar dos snapshots.

    Deliberadamente **no** incluye la severidad: si un mismo defecto cambia de
    severidad entre corridas, queremos verlo como el mismo hallazgo modificado,
    no como uno resuelto más uno nuevo.
    """
    return ((h.get("cat") or "").upper(), h.get("titulo", ""))


def ordenar(hallazgos) -> list[dict]:
    """Por severidad, no por orden de aparición."""
    return sorted((normalizar(h) for h in hallazgos),
                  key=lambda h: (ORDEN[h["sev"]], h["cat"], h["titulo"]))


def conteo(hallazgos) -> dict:
    """{severidad: n} con todas las claves presentes, incluso en cero."""
    c = {s: 0 for s in SEVERIDADES}
    for h in hallazgos:
        c[normalizar(h)["sev"]] += 1
    return c


def veredicto(hallazgos) -> str:
    """`❌ bloqueado` con un solo 🔴; `✅ verificado` sin 🔴 ni 🟠."""
    c = conteo(hallazgos)
    n = sum(c.values())
    if n == 0:
        return "✅ verificado"
    desglose = " · ".join(
        f"{c[s]}{EMOJI[s]}" for s in SEVERIDADES if c[s]
    )
    if c["bloqueante"]:
        return f"❌ bloqueado — {n} hallazgos ({desglose})"
    if c["mayor"]:
        return f"⚠️ {n} hallazgos ({desglose})"
    return f"✅ verificado — {n} sin severidad ({desglose})"


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

def _celda(texto) -> str:
    """Deja un texto apto para una celda de tabla markdown.

    Las barras verticales de un mensaje de SAP (`kl/r > 4.0*Sqr(E/fy)`) y los
    saltos de línea de un detalle largo rompen la tabla sin ningún aviso.
    """
    s = "" if texto is None else str(texto)
    return s.replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def _fila(celdas) -> str:
    return "| " + " | ".join(_celda(c) for c in celdas) + " |"


def hallazgos_a_markdown(hallazgos, desde: int = 1) -> str:
    """Tabla de hallazgos del contrato, ordenada por severidad.

    `desde` permite numerar de corrido cuando un agente concatena bloques.
    """
    hs = ordenar(hallazgos)
    lineas = [
        "| # | Sev | Cat | Ubicación | Hallazgo | Fix propuesto | Estado |",
        "|---|-----|-----|-----------|----------|---------------|--------|",
    ]
    for i, h in enumerate(hs, start=desde):
        texto = h["titulo"]
        if h["detalle"]:
            texto = f"{texto} — {h['detalle']}"
        lineas.append(_fila([i, sev_emoji(h["sev"]), h["cat"] or "—",
                             h["ubicacion"] or "—", texto,
                             h["fix"] or "—", ESTADO_ABIERTO]))
    if not hs:
        lineas.append("| — | | | | _sin hallazgos_ | | |")
    return "\n".join(lineas)


def validos_a_markdown(validos) -> str:
    """Tabla de valores dados por válidos.

    Es obligatoria en el contrato: delimita el alcance del ✅ y es lo que
    convierte la revisión en un dictamen sobre cada valor, no en una lista de
    quejas. Cada entrada: `{valor, donde, como, veredicto}`.
    """
    lineas = [
        "| Valor | Dónde aparece | Cómo se verificó | Veredicto |",
        "|---|---|---|---|",
    ]
    for v in validos:
        lineas.append(_fila([v.get("valor", ""), v.get("donde", ""),
                             v.get("como", ""), v.get("veredicto", "✅")]))
    if not validos:
        lineas.append("| — | | _ningún valor recalculado en esta pasada_ | |")
    return "\n".join(lineas)


def _lista(items, vacio: str) -> str:
    items = [str(x) for x in (items or []) if str(x).strip()]
    return "; ".join(items) if items else vacio


#: Reglas de redacción del bloque. Se repiten en el prompt de cada revisor;
#: acá vive la versión canónica para que no se separen.
#:
#: El reporte se lee entre dos reuniones: lo que no cabe en una línea no se
#: lee. Un hallazgo largo no es más riguroso, es más fácil de ignorar.
ESTILO = """\
- Una fila por hallazgo y una línea por fila. Sin preámbulo ni cierre.
- Si asumes algo para poder juzgar, la fila empieza con `Supuesto: …`.
- Toda afirmación normativa lleva su cita entre paréntesis, con la página y si
  se leyó rasterizada: `(CIRSOC 301 §B.2.2, pág. 41 rast.)`. Sin cita, el
  veredicto es 🔵, no ✅.
- Si te falta un dato para cerrar un juicio, no lo estimes: va a `Necesito para
  cerrar` como una pregunta concreta y contestable.
"""


def bloque_reporte(meta: dict, hallazgos, validos=(), no_verificable=(),
                   no_cubierto=(), necesito=()) -> str:
    """El bloque markdown literal que un revisor devuelve como mensaje final.

    `meta` reconoce: fecha, proyecto, alcance, agente, commit, norma, modelo,
    snapshot, categorias, determinista.

    `necesito` son las preguntas que hay que contestarle al revisor para que
    pueda cerrar lo que dejó abierto. Van separadas de `no_verificable` porque
    son cosas distintas: una es el veredicto sobre un valor, la otra es un
    pedido accionable dirigido a una persona.

    La skill lo inserta **tal cual** en `REVISION.md`: no lleva preámbulo ni
    cierre conversacional a propósito.
    """
    cab = (f"### {meta.get('fecha', '')} · "
           f"`{meta.get('proyecto', '')}/{meta.get('alcance', '')}` · "
           f"{meta.get('agente', '')} · {veredicto(hallazgos)}")

    linea2 = " · ".join([
        f"**Commit:** `{meta.get('commit', '—')}`",
        f"**Norma:** `{meta.get('norma', '—')}`",
        f"**Modelo:** `{meta.get('modelo', '—')}`",
        f"**Snapshot:** `{meta.get('snapshot', '—')}`",
        f"**Cat.:** {meta.get('categorias', '—')}",
        f"**Determinista:** {meta.get('determinista', '—')}",
    ])

    return "\n".join([
        cab, "", linea2, "",
        hallazgos_a_markdown(hallazgos), "",
        "**Valores dados por válidos**", "",
        validos_a_markdown(validos), "",
        "**No verificable:** " + _lista(no_verificable, "—"), "",
        "**Necesito para cerrar:** " + _lista(necesito, "nada"), "",
        "**Alcance no cubierto:** " + _lista(
            no_cubierto, "_no declarado_ ⚠️ el contrato lo exige"),
    ])


# --------------------------------------------------------------------------
# Persistencia y comparación de snapshots
# --------------------------------------------------------------------------

def guardar_json(d: dict, ruta: str) -> str:
    """Escribe UTF-8 con `ensure_ascii=False`: los hallazgos llevan acentos y
    los queremos legibles al abrir el archivo, no como `\\u00f3`."""
    import os
    carpeta = os.path.dirname(os.path.abspath(ruta))
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2, default=str)
    return os.path.abspath(ruta)


def cargar_json(ruta: str) -> dict:
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def diff_hallazgos(antes: dict | list, despues: dict | list) -> dict:
    """Compara dos snapshots (o dos listas de hallazgos).

    Es lo que el modelador devuelve al cerrar un cambio: **un cambio que agrega
    hallazgos se reporta como tal aunque el D/C haya bajado.**

    Devuelve `{nuevos, resueltos, persisten, cambiaron_severidad}`.
    """
    def _hs(x):
        if isinstance(x, dict):
            x = x.get("hallazgos", [])
        return {clave(h): normalizar(h) for h in x}

    a, d = _hs(antes), _hs(despues)
    nuevos = [d[k] for k in d if k not in a]
    resueltos = [a[k] for k in a if k not in d]
    comunes = [k for k in d if k in a]
    cambio = [{"hallazgo": d[k], "sev_antes": a[k]["sev"], "sev_despues": d[k]["sev"]}
              for k in comunes if a[k]["sev"] != d[k]["sev"]]
    return {
        "nuevos": ordenar(nuevos),
        "resueltos": ordenar(resueltos),
        "persisten": ordenar([d[k] for k in comunes]),
        "cambiaron_severidad": cambio,
    }


def diff_a_markdown(d: dict) -> str:
    partes = []
    for k, titulo in (("nuevos", "Hallazgos nuevos"),
                      ("resueltos", "Hallazgos resueltos"),
                      ("persisten", "Hallazgos que persisten")):
        hs = d.get(k, [])
        partes.append(f"**{titulo}: {len(hs)}**")
        if hs:
            partes.append("")
            partes.append(hallazgos_a_markdown(hs))
        partes.append("")
    for c in d.get("cambiaron_severidad", []):
        partes.append(f"- Cambió de severidad: {c['hallazgo']['titulo']} "
                      f"({sev_emoji(c['sev_antes'])} → {sev_emoji(c['sev_despues'])})")
    return "\n".join(partes).strip()


__all__ = [
    "SEVERIDADES", "EMOJI", "ORDEN", "CRITERIO", "CATEGORIAS", "ESTADO_ABIERTO",
    "ESTILO",
    "sev_emoji", "normalizar", "clave", "ordenar", "conteo", "veredicto",
    "hallazgos_a_markdown", "validos_a_markdown", "bloque_reporte",
    "guardar_json", "cargar_json", "diff_hallazgos", "diff_a_markdown",
]
