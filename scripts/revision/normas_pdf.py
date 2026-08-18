"""
normas_pdf — leer un reglamento en PDF sin creerle a la capa de texto.

La regla que justifica este módulo entero: **la capa de texto de un PDF de
norma sirve para encontrar, no para leer.** Al extraer texto, las fracciones se
aplanan, los subíndices se pegan al símbolo y φ suele salir como `f`. Un
coeficiente transcrito así puede convivir años con una aritmética que cierra
consigo misma, y ninguna revisión de resultados lo encuentra: el error típico
no es aritmético, es de transcripción.

De ahí el reparto de trabajo:

- `buscar` / `buscar_articulo` — **localizan** el artículo en el PDF.
- `rasterizar` — renderiza la página a PNG para que el agente **la mire**.
  Es la única vía válida para dar por buena una ecuación, un coeficiente o una
  celda de tabla.
- `verificar_cita` — devuelve **evidencia** (dónde está, y el PNG), nunca un
  veredicto. Si esta función juzgara, volveríamos a confiar en la capa de texto.

Trabaja siempre contra un `Perfil`, así que sirve igual para CIRSOC, NCh, ACI o
AISC: lo único que cambia es la clave.

    from revision import perfil, normas_pdf
    p = perfil.cargar(r"...\\Pachon\\PERFIL.json")
    hits = normas_pdf.buscar_articulo("C103-P1", "Tabla 5.1", p)
    png = normas_pdf.rasterizar_hit(hits[0], p)   # y ahora se mira el PNG
"""

from __future__ import annotations

import os
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, asdict

_DOCS: dict = {}


def _pymupdf():
    """Import diferido y con mensaje accionable.

    `fitz` quedó deprecado en pymupdf 1.28 (y el venv corre Python 3.14), por
    eso se importa `pymupdf` y no el alias viejo.
    """
    try:
        import pymupdf
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "pymupdf no está instalado en este intérprete. El lector de normas "
            "necesita el venv de Skills_SAP: "
            r"C:\Proyectos_Python\Skills_SAP\.venv\Scripts\python.exe") from e
    return pymupdf


def _abrir(clave: str, perfil):
    n = perfil.norma(clave)
    if not n.existe:
        raise FileNotFoundError(
            f"El PDF de '{clave}' ({n.titulo}) no está en {n.ruta or '(sin ruta)'}. "
            "Sin el PDF no se puede verificar la cita: el veredicto es 🔵 no "
            "verificable, nunca ✅.")
    st = os.stat(n.ruta)
    ficha = (n.ruta, st.st_mtime, st.st_size)
    if ficha not in _DOCS:
        _DOCS.clear()
        _DOCS[ficha] = _pymupdf().open(n.ruta)
    return _DOCS[ficha]


def cerrar_todo() -> None:
    for d in _DOCS.values():
        try:
            d.close()
        except Exception:  # noqa: BLE001
            pass
    _DOCS.clear()


# --------------------------------------------------------------------------
# Normalización
# --------------------------------------------------------------------------

def _normalizar(t: str) -> str:
    """Deja el texto comparable sin alterar los caracteres que importan.

    NFKC junta los ligados que los PDF usan para 'fi'/'fl'; el colapso de
    espacios evita que un salto de línea a mitad de 'Tabla 5.1' impida
    encontrarla.
    """
    t = unicodedata.normalize("NFKC", t or "")
    return re.sub(r"[ \t\u00a0]+", " ", t)


def _rx_numero(core: str) -> str:
    """Regex de un identificador tipo `7.2.5`, `B.2.2` o `A3.1`.

    Tolera espacios alrededor de los puntos, que aparecen cuando el PDF corta
    el número entre dos cajas de texto.
    """
    return r"\s*\.\s*".join(re.escape(p) for p in core.split("."))


_TIPOS = ("tabla", "figura", "fig", "ecuación", "ecuacion", "expresión",
          "expresion", "artículo", "articulo", "capítulo", "capitulo", "anexo",
          "apéndice", "apendice", "sección", "seccion")


def variantes(articulo: str) -> list[str]:
    """Las formas tipográficas en que un mismo artículo aparece en un PDF.

    `§7.2.5` puede estar escrito `7.2.5`, `7. 2. 5` o dentro de un título sin
    el símbolo; `[3.14]` a veces es `(3.14)`. Buscar una sola forma da un falso
    'no existe', que es peor que no buscar.
    """
    a = _normalizar(articulo).strip()
    tipo = ""
    m = re.match(r"^([A-Za-zÁÉÍÓÚáéíóú]+)\s+(.+)$", a)
    if m and m.group(1).lower() in _TIPOS:
        tipo, a = m.group(1), m.group(2)
    core = a.strip("§[]() \t").strip()
    if not core:
        return [re.escape(a)]
    rx = _rx_numero(core)

    vs: list[str] = []
    if tipo:
        vs.append(rf"{re.escape(tipo[:4])}\w*\.?\s*{rx}")
    vs += [
        rf"§\s*{rx}",
        rf"\[\s*{rx}\s*\]",
        rf"\(\s*{rx}\s*\)",
        rf"(?<![\w.]){rx}(?![\w.])",
    ]
    # sin duplicados, conservando la prioridad
    return list(dict.fromkeys(vs))


# --------------------------------------------------------------------------
# Búsqueda
# --------------------------------------------------------------------------

@dataclass
class Hit:
    clave: str
    pagina_pdf: int          #: 1-based, la que muestra el visor
    pagina_impresa: int      #: la impresa en el pie, según el offset del perfil
    contexto: str
    ocurrencias: int

    def dict(self) -> dict:
        return asdict(self)


def buscar(clave: str, patron: str, perfil, *, regex: bool = False,
           max_hits: int = 20, contexto: int = 160,
           desde: int = 1, hasta: int | None = None) -> list[Hit]:
    """Busca un patrón en el PDF y devuelve las páginas donde aparece.

    Ordena por número de ocurrencias: la página donde el artículo **se define**
    lo repite más que aquella donde sólo se lo cita de paso.
    """
    doc = _abrir(clave, perfil)
    rx = re.compile(patron if regex else re.escape(patron), re.IGNORECASE)
    hits: list[Hit] = []
    fin = len(doc) if hasta is None else min(hasta, len(doc))
    for i in range(max(0, desde - 1), fin):
        t = _normalizar(doc[i].get_text())
        ms = list(rx.finditer(t))
        if not ms:
            continue
        a = max(0, ms[0].start() - contexto // 2)
        hits.append(Hit(
            clave=clave, pagina_pdf=i + 1,
            pagina_impresa=perfil.pagina_impresa(clave, i + 1),
            contexto=" ".join(t[a:ms[0].end() + contexto // 2].split()),
            ocurrencias=len(ms)))
    hits.sort(key=lambda h: (-h.ocurrencias, h.pagina_pdf))
    return hits[:max_hits]


def buscar_articulo(clave: str, articulo: str, perfil, *, max_hits: int = 20,
                    contexto: int = 200) -> list[Hit]:
    """Localiza un artículo, tabla o expresión probando sus variantes."""
    for v in variantes(articulo):
        hits = buscar(clave, v, perfil, regex=True, max_hits=max_hits,
                      contexto=contexto)
        if hits:
            return hits
    return []


def texto_pagina(clave: str, pagina: int, perfil, *, impresa: bool = True) -> str:
    """Texto crudo de una página. Sirve para ubicarse, **no** para citar."""
    doc = _abrir(clave, perfil)
    p = perfil.pagina_pdf(clave, pagina) if impresa else int(pagina)
    if not 1 <= p <= len(doc):
        raise IndexError(
            f"'{clave}' tiene {len(doc)} páginas; se pidió la {p} "
            f"({'impresa ' + str(pagina) if impresa else 'del visor'}).")
    return _normalizar(doc[p - 1].get_text())


# --------------------------------------------------------------------------
# Rasterizado — la única vía válida para leer una ecuación
# --------------------------------------------------------------------------

def rasterizar(clave: str, pagina: int, perfil, *, dpi: int = 200,
               recorte: tuple[float, float, float, float] | None = None,
               destino: str | None = None, impresa: bool = True) -> str:
    """Renderiza una página a PNG y devuelve la ruta.

    `recorte` va en fracciones de la página `(x0, y0, x1, y1)`, para ampliar
    una tabla sin generar una imagen enorme. Subir el `dpi` es lo que hace
    legibles los subíndices.
    """
    pymupdf = _pymupdf()
    doc = _abrir(clave, perfil)
    p = perfil.pagina_pdf(clave, pagina) if impresa else int(pagina)
    if not 1 <= p <= len(doc):
        raise IndexError(f"'{clave}' tiene {len(doc)} páginas; se pidió la {p}.")
    page = doc[p - 1]

    clip = None
    if recorte:
        r = page.rect
        x0, y0, x1, y1 = recorte
        clip = pymupdf.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height,
                            r.x0 + x1 * r.width, r.y0 + y1 * r.height)

    if destino is None:
        sufijo = "_rec" if recorte else ""
        destino = os.path.join(perfil.dir_png, f"{clave}_p{p}_{dpi}{sufijo}.png")
    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)

    escala = dpi / 72.0
    pix = page.get_pixmap(matrix=pymupdf.Matrix(escala, escala), clip=clip)
    pix.save(destino)
    return os.path.abspath(destino)


def rasterizar_hit(h: Hit, perfil, *, dpi: int = 220) -> str:
    return rasterizar(h.clave, h.pagina_pdf, perfil, dpi=dpi, impresa=False)


# --------------------------------------------------------------------------
# Diagnóstico del PDF
# --------------------------------------------------------------------------

def info(clave: str, perfil) -> dict:
    """Radiografía del PDF: cuántas páginas tiene y si se puede buscar en él.

    `fraccion_con_texto` es el dato decisivo. Cerca de 0 significa que el PDF
    está escaneado: la búsqueda no va a encontrar nada y **el único camino es
    rasterizar y mirar**. Reportarlo como 'el artículo no existe' sería un
    falso negativo grave.
    """
    n = perfil.norma(clave)
    doc = _abrir(clave, perfil)
    total = len(doc)
    muestra = range(0, total, max(1, total // 40)) if total else []
    con_texto = sum(1 for i in muestra if len(doc[i].get_text().strip()) > 40)
    vistas = len(list(muestra)) or 1
    return {
        "clave": clave,
        "titulo": n.titulo,
        "edicion": n.edicion,
        "ruta": n.ruta,
        "paginas": total,
        "fraccion_con_texto": round(con_texto / vistas, 2),
        "escaneado": (con_texto / vistas) < 0.30,
        "cifrado": bool(doc.is_encrypted),
        "offset_declarado": n.offset_pagina,
        "rol": n.rol,
    }


def detectar_offset(clave: str, perfil, *, muestras: int = 24) -> dict:
    """Estima el desfase entre la página del visor y la impresa en el pie.

    Mira el encabezado y el pie de páginas repartidas por todo el documento
    buscando un número suelto. Es una **sugerencia**: hay que confirmarla
    mirando una página rasterizada antes de escribirla en el perfil, porque un
    offset mal puesto valida citas falsas sin que nada chille.
    """
    doc = _abrir(clave, perfil)
    total = len(doc)
    if not total:
        return {"clave": clave, "offset_sugerido": None, "confianza": 0.0}

    pymupdf = _pymupdf()
    paso = max(1, total // muestras)
    # Un offset se vota una sola vez por página: lo que distingue al bueno del
    # espurio no es aparecer muchas veces en una página, sino repetirse en
    # páginas distintas. El pie de un reglamento trae fechas, números de
    # capítulo y códigos de artículo que también parecen números de página;
    # sólo el verdadero mantiene la diferencia constante a lo largo del
    # documento.
    paginas_por_offset: dict[int, set[int]] = {}
    vistas = 0
    for i in range(0, total, paso):
        page = doc[i]
        r = page.rect
        bandas = [
            (r.x0, r.y1 - 0.10 * r.height, r.x1, r.y1),   # pie
            (r.x0, r.y0, r.x1, r.y0 + 0.09 * r.height),   # encabezado
        ]
        candidatos = set()
        for b in bandas:
            t = _normalizar(page.get_text(clip=pymupdf.Rect(*b)))
            # Entero suelto (la mayoría de los reglamentos) y numeración por
            # sección tipo `16.1-45` de AISC, donde la página impresa es el
            # número que va después del guion.
            for rx in (r"(?<!\S)(\d{1,4})(?!\S)",
                       r"(?<!\S)\d+\.\d+\s*-\s*(\d{1,4})(?!\S)"):
                for m in re.finditer(rx, t):
                    p = int(m.group(1))
                    if 1 <= p <= total + 60:
                        candidatos.add((i + 1) - p)
        for off in candidatos:
            paginas_por_offset.setdefault(off, set()).add(i + 1)
        vistas += 1

    if not paginas_por_offset:
        return {"clave": clave, "offset_sugerido": None, "confianza": 0.0,
                "declarado": perfil.norma(clave).offset_pagina, "coincide": False,
                "nota": "No se encontró numeración impresa. Si el PDF está "
                        "escaneado, el offset se calibra rasterizando una página."}

    votos = Counter({off: len(ps) for off, ps in paginas_por_offset.items()})
    off, n = votos.most_common(1)[0]
    declarado = perfil.norma(clave).offset_pagina
    return {
        "clave": clave,
        "offset_sugerido": off,
        "confianza": round(n / max(1, vistas), 2),
        "paginas_muestreadas": vistas,
        "declarado": declarado,
        "coincide": off == declarado,
        "candidatos": dict(votos.most_common(4)),
    }


# --------------------------------------------------------------------------
# Evidencia para el revisor normativo
# --------------------------------------------------------------------------

def verificar_cita(clave: str, articulo: str, perfil, *, dpi: int = 220,
                   afirmacion: str = "") -> dict:
    """Reúne la evidencia para juzgar una cita. **No la juzga.**

    Devuelve dónde está el artículo, el texto crudo de esa página y el PNG
    rasterizado. Quien decide si la norma *dice lo que el documento afirma* es
    el agente, mirando la imagen — porque eso es justo lo que la capa de texto
    no permite hacer con confianza.
    """
    n = perfil.norma(clave)
    if not n.existe:
        return {"clave": clave, "articulo": articulo, "afirmacion": afirmacion,
                "existe": False, "png": None, "hits": [],
                "motivo": f"PDF ausente en {n.ruta}",
                "veredicto_sugerido": "🔵 no verificable"}

    hits = buscar_articulo(clave, articulo, perfil)
    if not hits:
        d = info(clave, perfil)
        return {
            "clave": clave, "articulo": articulo, "afirmacion": afirmacion,
            "existe": False, "png": None, "hits": [],
            "motivo": ("El PDF está escaneado: la búsqueda de texto no aplica, "
                       "hay que rasterizar y mirar."
                       if d["escaneado"] else
                       "No se encontró el artículo con ninguna de sus variantes."),
            "escaneado": d["escaneado"],
            "veredicto_sugerido": "🔵 no verificable",
        }

    h = hits[0]
    return {
        "clave": clave,
        "articulo": articulo,
        "afirmacion": afirmacion,
        "existe": True,
        "pagina_pdf": h.pagina_pdf,
        "pagina_impresa": h.pagina_impresa,
        "png": rasterizar_hit(h, perfil, dpi=dpi),
        "texto_crudo": texto_pagina(clave, h.pagina_pdf, perfil, impresa=False),
        "cita": n.cita(articulo, h.pagina_pdf, rasterizada=True),
        "hits": [x.dict() for x in hits[:6]],
        "siguiente_paso": "Mirar el PNG y decidir si el artículo dice lo que se "
                          "afirma. Que exista no basta.",
    }


__all__ = [
    "Hit", "buscar", "buscar_articulo", "texto_pagina", "rasterizar",
    "rasterizar_hit", "info", "detectar_offset", "verificar_cita",
    "variantes", "cerrar_todo",
]
