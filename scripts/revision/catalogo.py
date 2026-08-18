"""
catalogo — qué perfiles existen de verdad, leídos del PDF del catálogo.

SAP2000 acepta cualquier dimensión que se le escriba: una sección inventada da
un D/C perfecto sobre un perfil imposible de comprar, y nada avisa. Este módulo
existe para cruzar toda designación contra el catálogo real antes de dar un
diseño por cerrado.

**No tiene datos cableados.** Extrae las tablas del PDF declarado en el perfil
del proyecto, así no hay una segunda copia que se desincronice. La contrapartida
es que la extracción tiene que ser robusta:

- Las páginas del catálogo CIRSOC están **rotadas 90°**, de modo que agrupar las
  palabras por coordenada Y devuelve columnas visuales, no filas. Hay que
  agrupar por X.
- Dentro de cada fila el orden sale **invertido** respecto de la lectura visual,
  por la misma rotación.

Ambas cosas se descubrieron mirando la salida contra una página rasterizada, y
por eso `verificar_cirsoc.py` incluye una aserción sobre un perfil conocido: si
el layout del PDF cambia, el módulo tiene que fallar ruidosamente y no devolver
números plausibles pero corridos de columna.

    from revision import perfil, catalogo
    p = perfil.cargar(r"...\\Pachon\\PERFIL.json")
    catalogo.buscar("W14x145", p)          # -> dict o None
    catalogo.validar_designaciones([...], p)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

#: Páginas del catálogo CIRSOC (Troglia) por serie, en número de página **del
#: visor**. Se toman del índice de la pág. impresa 1. Si se cambia de catálogo,
#: esto es lo único que hay que rehacer.
PAGINAS = {
    "IPN": (4, 4), "IPB": (5, 5), "IPBl": (6, 6), "IPBv": (7, 7), "IPE": (8, 8),
    "W": (9, 19), "HP": (20, 20), "M": (21, 21),
    "UPN": (22, 22), "C": (23, 23), "MC": (24, 25),
    "L": (26, 27), "T": (28, 29),
    "tubo_circular": (29, 35),
    "tubo_cuadrado": (36, 39),
    "tubo_rectangular": (40, 44),
}

#: Orden de columnas de las tablas de perfil doble T, tras invertir la fila.
#: Verificado contra W14x145 (d 375 · bf 394 · tf 27,7 · tw 17,3 · Ag 275,5 ·
#: peso 215,8), que reproduce exacto lo que SAP2000 tiene cargado.
#:
#: Las dos últimas parejas `Lp/Lr` son las de "Carga Alma" y "Carga Ala Sup." del
#: catálogo. `Lp` importa más de lo que parece: es la longitud no arriostrada
#: hasta la que el perfil desarrolla su momento plástico, y en vigas de gran luz
#: suele ser el dato que decide si un D/C en flexión pura sobrevive al pandeo
#: lateral-torsional.
COLS_DOBLE_T = [
    "d", "bf", "tf", "hw", "tw", "r", "bf_2tf", "hw_tw", "Ag", "peso",
    "Ix", "Sx", "rx", "Qx", "Zx", "Iy", "Sy", "ry", "Qy", "Sy_15", "Zy",
    "J", "Cw", "X1", "X2", "Lp", "Lr", "Lp_ala", "Lr_ala",
]

#: Ídem para tubo cuadrado. La primera columna (B) sólo aparece en la primera
#: fila de cada grupo de espesores, así que se arrastra.
COLS_TUBO_CUADRADO = ["t", "p", "Ag", "peso", "Ix", "Sx", "r", "Zx", "J", "C"]

RX_DESIGNACION = re.compile(r"^(?:W|M|HP|S|C|MC|L|T|IPN|IPB|IPBl|IPBv|IPE)"
                            r"\s?\d+[xX×]\d+$", re.IGNORECASE)

#: Fila de continuación dentro de un grupo de altura: "x211", "x145".
RX_CONTINUACION = re.compile(r"^[xX×]\d{1,4}$")

_CACHE: dict = {}


@dataclass
class Perfil:
    designacion: str
    serie: str
    dims: dict = field(default_factory=dict)

    def __repr__(self):
        d = " ".join(f"{k}={v}" for k, v in list(self.dims.items())[:5])
        return f"<{self.designacion} ({self.serie}) {d}>"


def _num(s: str):
    """Los números del catálogo usan coma decimal y a veces punto de miles."""
    s = s.strip()
    if s.count(",") == 1:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _filas(doc, pagina_pdf: int, tol: float = 2.5) -> list[list[str]]:
    """Filas visuales de una página rotada 90°, ya en orden de lectura."""
    page = doc[pagina_pdf - 1]
    ws = page.get_text("words")           # (x0, y0, x1, y1, palabra, ...)
    ws.sort(key=lambda w: (round(w[0] / tol), w[1]))
    grupos, actual, ref = [], [], None
    for w in ws:
        if ref is None or abs(w[0] - ref) <= tol:
            actual.append(w)
            ref = w[0] if ref is None else ref
        else:
            grupos.append(actual)
            actual, ref = [w], w[0]
    if actual:
        grupos.append(actual)
    # dentro del grupo, ordenar por Y e invertir: la rotación da el orden al revés
    return [[w[4] for w in sorted(g, key=lambda z: z[1])][::-1] for g in grupos]


def _doc(perfil, clave: str):
    from . import normas_pdf
    return normas_pdf._abrir(clave, perfil)


def serie_doble_t(perfil, serie: str = "W", clave: str = "PERF-AR") -> dict:
    """{designación: Perfil} de una serie de perfil doble T."""
    ficha = (clave, serie, perfil.norma(clave).ruta)
    if ficha in _CACHE:
        return _CACHE[ficha]

    doc = _doc(perfil, clave)
    desde, hasta = PAGINAS[serie]
    out: dict[str, Perfil] = {}
    for pag in range(desde, min(hasta, len(doc)) + 1):
        prefijo = None
        for fila in _filas(doc, pag):
            if not fila:
                continue
            # El catálogo escribe la designación completa sólo en el primer
            # perfil de cada grupo de altura ("W14x233") y los siguientes van
            # como continuación ("x211", "x145"). Descartarlas deja fuera el
            # 80 % de la serie — y hace que un perfil real parezca inexistente.
            if RX_DESIGNACION.match(fila[0]):
                desig = fila[0]
                m = re.match(r"^([A-Za-z]+\d+)", desig)
                prefijo = m.group(1) if m else None
            elif prefijo and RX_CONTINUACION.match(fila[0]):
                desig = f"{prefijo}{fila[0]}"
            else:
                continue

            desig = desig.replace("×", "x").replace("X", "x").replace(" ", "")
            vals = [_num(t) for t in fila[1:]]
            dims = {}
            for i, nombre in enumerate(COLS_DOBLE_T):
                if i < len(vals) and vals[i] is not None:
                    dims[nombre] = vals[i]
            if len(dims) >= 6:
                out[desig.upper()] = Perfil(desig, serie, dims)
    _CACHE[ficha] = out
    return out


#: Espesores de catálogo del tubo cuadrado IRAM-IAS U 500-218 / U 500-2592,
#: **transcritos de las páginas rasterizadas** impresas 34 a 37 (pdf 36 a 39) el
#: 2026-08-14.
#:
#: No se extraen del texto a propósito. La columna B es una celda combinada que
#: abarca todo su grupo de espesores, y reconstruirla por coordenadas asignaba
#: los lados corridos: daba por bueno un 200×200×12 con el área del 250×250×12.
#: Un número plausible pero de otra fila es peor que ningún número.
#:
#: {lado_mm: {espesor_mm: (Ag_cm2, r_cm, peso_kg_m)}}
TUBO_CUADRADO = {
    15:  {0.70: (0.388, 0.579, 0.304), 0.90: (0.487, 0.569, 0.382),
          1.25: (0.647, 0.552, 0.508)},
    20:  {0.90: (0.667, 0.773, 0.523), 1.25: (0.897, 0.756, 0.704),
          1.60: (1.112, 0.739, 0.873)},
    25:  {0.90: (0.847, 0.977, 0.665), 1.25: (1.147, 0.960, 0.901),
          1.60: (1.432, 0.943, 1.124), 2.00: (1.737, 0.924, 1.364)},
    30:  {0.90: (1.027, 1.181, 0.806), 1.25: (1.397, 1.165, 1.097),
          1.60: (1.752, 1.148, 1.375), 2.00: (2.137, 1.128, 1.678)},
    40:  {1.25: (1.897, 1.573, 1.489), 1.60: (2.392, 1.556, 1.877),
          2.00: (2.937, 1.537, 2.306), 2.50: (3.589, 1.512, 2.817)},
    50:  {1.60: (3.032, 1.964, 2.380), 2.00: (3.737, 1.945, 2.934),
          2.50: (4.589, 1.921, 3.602), 3.20: (5.727, 1.887, 4.495)},
    60:  {1.60: (3.67, 2.37, 2.88), 2.00: (4.54, 2.35, 3.56),
          2.50: (5.59, 2.33, 4.39), 3.20: (7.01, 2.30, 5.50),
          4.00: (8.55, 2.26, 6.71)},
    80:  {2.00: (6.14, 3.17, 4.82), 2.50: (7.59, 3.15, 5.96),
          3.20: (9.57, 3.11, 7.51), 4.00: (11.75, 3.07, 9.22),
          4.76: (13.74, 3.04, 10.79)},
    90:  {2.50: (8.59, 3.55, 6.74), 3.20: (10.85, 3.52, 8.51),
          4.00: (13.35, 3.48, 10.48), 4.76: (15.65, 3.44, 12.28),
          6.35: (20.21, 3.37, 15.86)},
    100: {3.20: (12.13, 3.93, 9.52), 4.00: (14.95, 3.89, 11.73),
          4.76: (17.55, 3.85, 13.78), 6.35: (22.75, 3.78, 17.86)},
    110: {3.20: (13.41, 4.34, 10.52), 4.00: (16.55, 4.30, 12.99),
          4.76: (19.45, 4.26, 15.27), 6.35: (25.29, 4.18, 19.85)},
    120: {4.00: (18.15, 4.71, 14.25), 5.00: (22.36, 4.66, 17.55),
          6.00: (26.43, 4.61, 20.75), 8.00: (34.19, 4.51, 26.84),
          10.00: (41.42, 4.42, 32.52), 12.00: (48.13, 4.32, 37.78)},
    140: {4.00: (21.35, 5.52, 16.76), 5.00: (26.36, 5.48, 20.69),
          6.00: (31.23, 5.43, 24.52), 8.00: (40.59, 5.33, 31.86),
          10.00: (49.42, 5.23, 38.80), 12.00: (57.73, 5.13, 45.32)},
    150: {4.00: (22.95, 5.93, 18.01), 5.00: (28.36, 5.88, 22.26),
          6.00: (33.63, 5.84, 26.40), 8.00: (43.79, 5.74, 34.38),
          10.00: (53.42, 5.64, 41.94), 12.00: (62.53, 5.54, 49.09)},
    180: {5.00: (34.36, 7.11, 26.97), 6.00: (40.83, 7.06, 32.05),
          8.00: (53.39, 6.96, 41.91), 10.00: (65.42, 6.87, 51.36),
          12.00: (76.93, 6.77, 60.39)},
    200: {5.00: (38.36, 7.92, 30.11), 6.00: (45.63, 7.88, 35.82),
          8.00: (59.79, 7.78, 46.94), 10.00: (73.42, 7.68, 57.64),
          12.00: (86.53, 7.59, 67.93)},
    250: {6.00: (57.63, 9.92, 45.24), 8.00: (75.79, 9.82, 59.50),
          10.00: (93.42, 9.73, 73.34), 12.00: (110.53, 9.63, 86.77)},
    300: {6.00: (69.63, 11.96, 54.66), 8.00: (91.79, 11.86, 72.06),
          10.00: (113.42, 11.77, 89.04), 12.00: (134.53, 11.67, 105.61)},
    350: {6.00: (81.63, 14.00, 64.08), 8.00: (107.79, 13.90, 84.62),
          10.00: (133.42, 13.81, 104.74), 12.00: (158.53, 13.71, 124.45)},
    400: {8.00: (123.79, 15.95, 97.18), 10.00: (153.42, 15.85, 120.44),
          12.00: (182.53, 15.75, 143.29), 14.00: (211.11, 15.66, 165.72)},
}

FUENTE_TUBO = ("PERF-AR", "págs. impresas 34-37 (pdf 36-39)", "2026-08-14",
               "rasterizada")


def tubo_cuadrado(perfil=None, clave: str = "PERF-AR") -> dict:
    """{(B, t): Perfil} del tubo cuadrado IRAM-IAS. No necesita el PDF."""
    return {
        (float(B), float(t)): Perfil(
            f"HSS{B}x{B}x{t:g}", "tubo_cuadrado",
            {"B": float(B), "t": float(t), "Ag": v[0], "r": v[1], "peso": v[2]})
        for B, esp in TUBO_CUADRADO.items() for t, v in esp.items()
    }


def espesores_disponibles(B: float, perfil=None, clave: str = "PERF-AR") -> list[float]:
    """Espesores de catálogo para un lado dado de tubo cuadrado."""
    return sorted(TUBO_CUADRADO.get(int(round(B)), {}))


def lados_disponibles(perfil=None, clave: str = "PERF-AR") -> list[int]:
    return sorted(TUBO_CUADRADO)


def mas_cercano(h: float, b: float, tf: float, tw: float, perfil,
                serie: str = "W", clave: str = "PERF-AR", n: int = 3) -> list:
    """Perfiles de catálogo más parecidos a unas dimensiones dadas.

    Es lo que convierte un "no está en catálogo" en algo accionable: dice cuál
    sería el equivalente comercial y cuánto habría que moverse para usarlo.
    La distancia pondera d y bf por encima de los espesores, porque cambiar el
    canto altera la geometría del conjunto y cambiar un espesor no.
    """
    tabla = serie_doble_t(perfil, serie, clave)
    ranking = []
    for p in tabla.values():
        q = p.dims
        if not all(k in q for k in ("d", "bf", "tf", "tw")):
            continue
        dist = (2.0 * abs(q["d"] - h) / max(h, 1) +
                2.0 * abs(q["bf"] - b) / max(b, 1) +
                abs(q["tf"] - tf) / max(tf, 1) +
                abs(q["tw"] - tw) / max(tw, 1))
        ranking.append((dist, p))
    ranking.sort(key=lambda x: x[0])
    return [p for _, p in ranking[:n]]


def buscar(designacion: str, perfil, clave: str = "PERF-AR") -> Perfil | None:
    """Busca una designación en las series de doble T del catálogo."""
    d = designacion.replace("×", "x").replace("X", "x").replace(" ", "").upper()
    for serie in ("W", "HP", "M", "IPN", "IPB", "IPBl", "IPBv", "IPE"):
        try:
            tabla = serie_doble_t(perfil, serie, clave)
        except (KeyError, IndexError):
            continue
        if d in tabla:
            return tabla[d]
    return None


def coincide_tubo(B: float, t: float, perfil=None, tol: float = 0.6,
                  clave: str = "PERF-AR") -> Perfil | None:
    for (b, tt), p in tubo_cuadrado().items():
        if abs(b - B) < tol and abs(tt - t) < tol:
            return p
    return None


def validar_designaciones(secciones: list[dict], perfil,
                          clave: str = "PERF-AR", tol_dim: float = 2.0) -> list[dict]:
    """Cruza las secciones de un modelo contra el catálogo.

    Cada entrada de `secciones`: {nombre, forma, h, b, tf, tw}. Devuelve un
    dictamen por sección con `veredicto`:

    - `catalogo`  — coincide con un perfil real, y las dimensiones cuadran.
    - `dimension` — el nombre existe en catálogo pero las dimensiones NO cuadran.
      Es el caso peligroso: parece de catálogo y no lo es.
    - `PRS`       — no está en catálogo. Hay que declararlo como perfil armado.
    """
    out = []
    for s in secciones:
        nombre = s.get("nombre", "")
        forma = (s.get("forma") or "").lower()
        h, b = s.get("h"), s.get("b")
        tf, tw = s.get("tf"), s.get("tw")

        if "tube" in forma or "box" in forma:
            p = coincide_tubo(h, tf, perfil, clave=clave)
            if p:
                v, det = "catalogo", p.designacion
            else:
                disp = espesores_disponibles(h, perfil, clave)
                det = (f"lado {h:.0f} mm admite t = "
                       + (", ".join(f"{x:.0f}" for x in disp) if disp
                          else "— ese lado no existe en la serie"))
                v = "PRS"
            out.append({"seccion": nombre, "forma": "tubo cuadrado",
                        "veredicto": v, "detalle": det,
                        "dims": f"{h:.0f}x{b:.0f}x{tf:.0f}"})
            continue

        p = buscar(nombre, perfil, clave)
        if p is None:
            # El nombre no dice nada, pero las dimensiones sí: puede ser un
            # perfil de catálogo con nombre propio. Se busca por geometría antes
            # de declararlo armado.
            cand = mas_cercano(h, b, tf, tw, perfil, clave=clave, n=3)
            exacto = next(
                (c for c in cand
                 if all(abs(c.dims.get(k, 1e9) - v) <= tol_dim
                        for k, v in (("d", h), ("bf", b), ("tf", tf), ("tw", tw)))),
                None)
            if exacto:
                out.append({
                    "seccion": nombre, "forma": "doble T", "veredicto": "catalogo",
                    "detalle": f"es {exacto.designacion} con otro nombre "
                               f"(d={exacto.dims['d']} bf={exacto.dims['bf']} "
                               f"tf={exacto.dims['tf']} tw={exacto.dims['tw']})",
                    "dims": f"{h:.0f}x{b:.0f}x{tf:.0f}/alma {tw:.0f}"})
            else:
                cerca = " · ".join(
                    f"{c.designacion} ({c.dims['d']:.0f}x{c.dims['bf']:.0f}x"
                    f"{c.dims['tf']:.1f}/{c.dims['tw']:.1f})" for c in cand)
                out.append({
                    "seccion": nombre, "forma": "doble T", "veredicto": "PRS",
                    "detalle": f"no está en catálogo. Más cercanos: {cerca}",
                    "dims": f"{h:.0f}x{b:.0f}x{tf:.0f}/alma {tw:.0f}"})
            continue

        difs = []
        for k, v in (("d", h), ("bf", b), ("tf", tf), ("tw", tw)):
            ref = p.dims.get(k)
            if ref is not None and v is not None and abs(ref - v) > tol_dim:
                difs.append(f"{k} modelo {v:.1f} vs catálogo {ref:.1f}")
        out.append({
            "seccion": nombre, "forma": "doble T",
            "veredicto": "catalogo" if not difs else "dimension",
            "detalle": "; ".join(difs) if difs else
                       f"{p.designacion}  d={p.dims.get('d')} bf={p.dims.get('bf')} "
                       f"tf={p.dims.get('tf')} tw={p.dims.get('tw')}",
            "dims": f"{h:.0f}x{b:.0f}x{tf:.0f}/alma {tw:.0f}",
        })
    return out


__all__ = [
    "PAGINAS", "Perfil", "serie_doble_t", "tubo_cuadrado", "buscar",
    "coincide_tubo", "espesores_disponibles", "lados_disponibles",
    "validar_designaciones",
]
