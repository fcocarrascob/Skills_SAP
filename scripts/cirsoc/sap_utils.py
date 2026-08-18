"""
sap_utils — conocimiento de la API COM de SAP2000 encapsulado.

Recoge las trampas que cuesta descubrir trabajando contra `SapModel`:
firmas raras, enums, falsos negativos y el formato de las tablas.

No importa `comtypes` ni abre SAP: recibe siempre un `SapModel` ya conectado.
Así se puede usar tanto desde el MCP (que lo inyecta) como desde un script
propio con `comtypes.client`.

Referencia viva de los hallazgos: `Pachon/Estructurando/03_BITACORA_API_NORMATIVA.md`
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# Enums que la API usa como enteros pelados
# --------------------------------------------------------------------------

class Units:
    """eUnits. `SapModel.SetPresentUnits(Units.kN_m_C)`"""
    lb_in_F, lb_ft_F, kip_in_F, kip_ft_F = 1, 2, 3, 4
    kN_mm_C, kN_m_C, kgf_mm_C, kgf_m_C = 5, 6, 7, 8
    N_mm_C, N_m_C, Ton_mm_C, Ton_m_C = 9, 10, 11, 12
    kN_cm_C, kgf_cm_C, N_cm_C, Ton_cm_C = 13, 14, 15, 16


class ItemType:
    """eItemType — el argumento final de casi todos los Get/Set de asignaciones.

    TRAMPA: usar SELECTED desde un script devuelve 0 resultados **sin error**
    si no hay nada seleccionado en la GUI. Para barrer todo el modelo va
    GROUP con el nombre 'All', que siempre existe.
    """
    OBJECT = 0
    GROUP = 1
    SELECTED = 2


class LoadPatternType:
    """eLoadPatternType para `LoadPatterns.Add`."""
    DEAD = 1
    SUPER_DEAD = 2
    LIVE = 3
    REDUCE_LIVE = 4
    QUAKE = 5
    WIND = 6
    SNOW = 7
    OTHER = 8
    TEMPERATURE = 11
    ROOF_LIVE = 12


class Dir:
    """Dirección de las cargas distribuidas / puntuales sobre frames y áreas.

    TRAMPA GRANDE: con GRAVITY (10) el valor **positivo es hacia abajo**.
    Con GLOBAL_Z (6) el valor positivo es hacia arriba. Mezclarlas hace que
    las cargas se cancelen sin ningún aviso.
    """
    LOCAL_1, LOCAL_2, LOCAL_3 = 1, 2, 3
    GLOBAL_X, GLOBAL_Y, GLOBAL_Z = 4, 5, 6
    PROJ_X, PROJ_Y, PROJ_Z = 7, 8, 9
    GRAVITY = 10
    PROJ_GRAVITY = 11


class DistType:
    ONE_WAY = 1
    TWO_WAY = 2


class ComboType:
    LINEAR_ADD = 0
    ENVELOPE = 1
    ABSOLUTE_ADD = 2
    SRSS = 3
    RANGE_ADD = 4


class CNameType:
    """Segundo argumento de `RespCombo.SetCaseList`."""
    LOAD_CASE = 0
    LOAD_COMBO = 1


# Índices de liberación de extremo en `FrameObj.SetReleases`
REL_P, REL_V2, REL_V3, REL_T, REL_M2, REL_M3 = range(6)

#: Rótula de flexión en ambos ejes — lo que corresponde a una diagonal
#: de arriostramiento concéntrico o a una barra de celosía.
PIN = [False, False, False, False, True, True]

#: Rótula + axial libre. Para el extremo J de vigas en serie que **no** deben
#: formar un cordón continuo (p. ej. una vía de puente grúa sobre ménsulas).
PIN_SLIDE = [True, False, False, False, True, True]

FIXED = [False] * 6


# --------------------------------------------------------------------------
# Códigos de retorno
# --------------------------------------------------------------------------

def ret_code(result) -> int:
    """Devuelve el código de retorno de una llamada a la API.

    TRAMPA: una función con parámetros ByRef **no** devuelve el entero pelado
    sino una tupla `(*salidas, ret)`. Comparar el resultado contra 0 da False
    aunque la llamada haya funcionado.

        >>> ret_code(SapModel.FrameObj.SetReleases(...)) == 0   # correcto
        >>> SapModel.FrameObj.SetReleases(...) == 0             # SIEMPRE False
    """
    if isinstance(result, (int, float)):
        return int(result)
    try:
        return int(result[-1])
    except (TypeError, IndexError, ValueError):
        return -1


def ok(result) -> bool:
    """True si la llamada devolvió 0 (éxito, convención de SAP2000)."""
    return ret_code(result) == 0


def check(result, que: str = "") -> None:
    """Levanta RuntimeError si la llamada falló."""
    c = ret_code(result)
    if c != 0:
        raise RuntimeError(f"SAP2000 devolvió {c}" + (f" en {que}" if que else ""))


# --------------------------------------------------------------------------
# Tablas de base de datos — la vía confiable para leer el modelo
# --------------------------------------------------------------------------

def num(s, default: float = 0.0) -> float:
    """float() tolerante al separador decimal coma de los locales es-*.

    Los getters de la API devuelven floats nativos, pero **las tablas
    devuelven strings** con el separador del sistema.
    """
    if isinstance(s, (int, float)):
        return float(s)
    if s is None:
        return default
    try:
        return float(str(s).replace(",", "."))
    except ValueError:
        return default


def tabla(SapModel, key: str, grupo: str = "", limite: int | None = None) -> list[dict]:
    """Lee una tabla de base de datos y la devuelve como lista de dicts.

    La firma correcta es la de abajo. Pasar `[]` en vez de `['']` en el
    FieldKeyList produce `'int' object is not iterable`.

    El retorno es `(FieldKeyList, TableVersion, FieldKeysIncluded,
    NumberRecords, TableData, ret)` — los campos están en el índice **2**,
    no en el 1.
    """
    res = SapModel.DatabaseTables.GetTableForDisplayArray(
        key, [""], grupo, 0, [""], 0, [""]
    )
    campos = list(res[2])
    n = int(res[3])
    data = list(res[4])
    nf = len(campos)
    if nf == 0 or n == 0:
        return []
    tope = n if limite is None else min(n, limite)
    filas = [dict(zip(campos, data[i * nf:(i + 1) * nf])) for i in range(tope)]
    # SAP devuelve una sola fila {'None': 'Yes'} cuando la tabla está vacía
    if len(filas) == 1 and set(filas[0]) == {"None"}:
        return []
    return filas


def tablas_disponibles(SapModel, filtro: str = "") -> list[str]:
    res = SapModel.DatabaseTables.GetAvailableTables(0, [], [], [])
    claves = list(res[1])
    if not filtro:
        return claves
    f = filtro.upper()
    return [k for k in claves if f in k.upper()]


def masa_total(SapModel) -> float:
    """Masa sísmica ensamblada del modelo, en las unidades activas.

    TRAMPA: la tabla `Assembled Joint Masses` incluye una fila de resumen
    llamada **SumAccelUZ** que contiene la suma de todas las demás. Sumar la
    columna a ciegas da exactamente el doble.
    """
    filas = tabla(SapModel, "Assembled Joint Masses")
    for f in filas:
        if f.get("Joint") == "SumAccelUZ":
            return num(f.get("U3"))
    return sum(num(f.get("U3")) for f in filas if str(f.get("Joint", "")).isdigit())


def seleccionar_salida(SapModel, casos=(), combos=()) -> None:
    """Filtra qué casos/combos aparecen en las tablas de resultados.

    Sin esto, `Base Reactions` devuelve una fila por modo del caso modal.
    """
    S = SapModel.Results.Setup
    S.DeselectAllCasesAndCombosForOutput()
    for c in casos:
        S.SetCaseSelectedForOutput(c)
    for c in combos:
        S.SetComboSelectedForOutput(c)


def reacciones_base(SapModel, casos=(), combos=()) -> dict:
    """{nombre: {'FX':..,'FY':..,'FZ':..}} para los casos/combos pedidos."""
    seleccionar_salida(SapModel, casos, combos)
    out = {}
    for f in tabla(SapModel, "Base Reactions"):
        clave = f.get("OutputCase")
        paso = f.get("StepType")
        if paso:
            clave = f"{clave}::{paso}"
        out[clave] = {
            "FX": num(f.get("GlobalFX")),
            "FY": num(f.get("GlobalFY")),
            "FZ": num(f.get("GlobalFZ")),
            "MX": num(f.get("GlobalMX")),
            "MY": num(f.get("GlobalMY")),
        }
    return out


def modos(SapModel, caso: str = "MODAL") -> list[dict]:
    """Períodos y participación modal, ya convertidos a float."""
    seleccionar_salida(SapModel, casos=[caso])
    return [
        {
            "modo": int(num(x.get("StepNum"))),
            "T": num(x.get("Period")),
            "UX": num(x.get("UX")), "UY": num(x.get("UY")), "UZ": num(x.get("UZ")),
            "RZ": num(x.get("RZ")),
            "SumUX": num(x.get("SumUX")), "SumUY": num(x.get("SumUY")),
            "SumUZ": num(x.get("SumUZ")),
        }
        for x in tabla(SapModel, "Modal Participating Mass Ratios")
    ]


def periodo_traslacional(SapModel, direccion: str = "UX", caso: str = "MODAL") -> float:
    """Período del modo con mayor participación en la dirección pedida.

    Es el T que pide CIRSOC 103 §6.2.3 para el coeficiente sísmico.
    """
    ms = modos(SapModel, caso)
    if not ms:
        return 0.0
    return max(ms, key=lambda m: m[direccion])["T"]


# --------------------------------------------------------------------------
# Inventario y conectividad
# --------------------------------------------------------------------------

def inventario(SapModel) -> dict:
    """Conteo de objetos por tipo.

    TRAMPA: `FrameObj.GetNameList` no ve los **links**. En un modelo con
    ménsulas o aisladores, la diferencia contra el grupo 'All' son ellos.
    """
    def n(fn):
        try:
            return int(fn(0, [])[0])
        except Exception:
            return 0
    inv = {
        "frames": n(SapModel.FrameObj.GetNameList),
        "points": n(SapModel.PointObj.GetNameList),
        "areas": n(SapModel.AreaObj.GetNameList),
        "links": n(SapModel.LinkObj.GetNameList),
    }
    try:
        inv["grupo_All"] = int(SapModel.GroupDef.GetAssignments("All", 0, [], [])[0])
    except Exception:
        inv["grupo_All"] = None
    inv["suma_tipos"] = sum(v for k, v in inv.items() if k != "grupo_All")
    return inv


def conectividad(SapModel) -> dict[str, list[str]]:
    """{nodo: [barras que llegan]}. No existe un getter directo en la API.

    Sirve para detectar nodos huérfanos: puntas de ménsula sin nada montado,
    barras sueltas, etc.
    """
    conn: dict[str, list[str]] = {}
    for f in SapModel.FrameObj.GetNameList(0, [])[1]:
        p1, p2, _ = SapModel.FrameObj.GetPoints(f, "", "")[:3]
        conn.setdefault(p1, []).append(f)
        conn.setdefault(p2, []).append(f)
    return conn


def nodos_huerfanos(SapModel) -> list[tuple[str, tuple]]:
    """Nodos que no pertenecen a ninguna barra (pueden tener links o nada)."""
    conn = conectividad(SapModel)
    fuera = []
    for p in SapModel.PointObj.GetNameList(0, [])[1]:
        if p not in conn:
            c = SapModel.PointObj.GetCoordCartesian(p, 0, 0, 0)[:3]
            fuera.append((p, tuple(round(v, 3) for v in c)))
    return fuera


def liberaciones_por_seccion(SapModel) -> dict:
    """Cuántas barras de cada sección están rotuladas en **ambos** extremos.

    Un arriostramiento concéntrico modelado con un solo extremo liberado
    trabaja a flexión y arruina el chequeo PMM sin que se note: el ratio sube
    por momento, no por axial.
    """
    FO = SapModel.FrameObj
    out: dict[str, dict] = {}
    for f in FO.GetNameList(0, [])[1]:
        s = FO.GetSection(f, "", "")[0]
        g = FO.GetReleases(f, [False] * 6, [False] * 6, [0.0] * 6, [0.0] * 6)
        ii, jj = list(g[0]), list(g[1])
        d = out.setdefault(s, {"total": 0, "rotuladas": 0, "rigidas": []})
        d["total"] += 1
        if ii[REL_M2] and ii[REL_M3] and jj[REL_M2] and jj[REL_M3]:
            d["rotuladas"] += 1
        elif len(d["rigidas"]) < 8:
            d["rigidas"].append(f)
    return out


def liberaciones_arriostramiento(SapModel, claves=("DIAG", "BRACE", "ARRIOSTR")) -> dict:
    """Liberaciones de las diagonales, distinguiendo el tipo de extremo.

    `liberaciones_por_seccion` cuenta una barra como correcta sólo si está
    rotulada en **ambos** extremos, y eso da un falso positivo en cuanto la
    diagonal se dividió en el punto de cruce de una X: ahí cada mitad tiene un
    extremo interno que **debe quedar rígido**, porque liberarlo convierte el
    cruce en una rótula y arma un mecanismo.

    Los dos errores son reales y opuestos, así que se cuentan por separado:

    - un extremo de **conexión** (llega a columna, viga u otra sección) sin
      rótula hace que la diagonal tome flexión del drift y el chequeo PMM se
      dispare por momento en vez de por axial;
    - un nudo **interno** rotulado invalida el modal — fue lo que costó una
      iteración entera en El Pachón.

    El criterio es **geométrico, no de vecindad**: un extremo es un punto de
    división cuando en ese nudo continúa otra barra de la misma sección **en la
    misma recta**. Mirar sólo qué secciones concurren no alcanza — en un nudo de
    celosía llegan varias diagonales que no continúan ninguna, y contarlo como
    división produce un bloqueante falso.
    """
    import math

    FO = SapModel.FrameObj
    PO = SapModel.PointObj
    nombres = list(FO.GetNameList(0, [])[1])
    secc = {f: FO.GetSection(f, "", "")[0] for f in nombres}

    ext, conn = {}, {}
    for f in nombres:
        p1, p2 = FO.GetPoints(f, "", "")[:2]
        ext[f] = (p1, p2)
        conn.setdefault(p1, []).append(f)
        conn.setdefault(p2, []).append(f)

    coord: dict[str, tuple] = {}

    def xyz(p):
        if p not in coord:
            coord[p] = tuple(PO.GetCoordCartesian(p, 0.0, 0.0, 0.0)[:3])
        return coord[p]

    def direccion(f, desde):
        """Vector unitario de la barra saliendo del nudo `desde`."""
        p1, p2 = ext[f]
        otro = p2 if p1 == desde else p1
        a, b = xyz(desde), xyz(otro)
        v = [b[i] - a[i] for i in range(3)]
        L = math.sqrt(sum(c * c for c in v))
        return [c / L for c in v] if L else [0.0, 0.0, 0.0]

    def continua(f, g, nudo, tol=1e-3):
        """True si `g` prolonga a `f` en la misma recta a través de `nudo`."""
        u, w = direccion(f, nudo), direccion(g, nudo)
        return sum(u[i] * w[i] for i in range(3)) < -1.0 + tol

    out: dict[str, dict] = {}
    for f, s in secc.items():
        S = (s or "").upper()
        if not any(k in S for k in claves):
            continue
        d = out.setdefault(s, {
            "barras": 0,
            "conexion": 0, "conexion_rotulados": 0, "conexion_rigidos": [],
            "internos": 0, "internos_rotulados": 0, "internos_rotulados_ej": [],
        })
        g = FO.GetReleases(f, [False] * 6, [False] * 6, [0.0] * 6, [0.0] * 6)
        ii, jj = list(g[0]), list(g[1])
        d["barras"] += 1
        for rel, p in ((ii, ext[f][0]), (jj, ext[f][1])):
            vecinos = [x for x in conn.get(p, []) if x != f and secc[x] == s]
            interno = any(continua(f, x, p) for x in vecinos)
            rotulado = rel[REL_M2] and rel[REL_M3]
            if interno:
                d["internos"] += 1
                if rotulado:
                    d["internos_rotulados"] += 1
                    if len(d["internos_rotulados_ej"]) < 6:
                        d["internos_rotulados_ej"].append(f)
            else:
                d["conexion"] += 1
                if rotulado:
                    d["conexion_rotulados"] += 1
                elif len(d["conexion_rigidos"]) < 6:
                    d["conexion_rigidos"].append(f)
    return out


def normal_area(SapModel, nombre: str, punto_interior=(0.0, 0.0, 0.0)):
    """(normal_unitaria, signo) del eje local 3 de un área.

    El eje local 3 sale del producto vectorial de los tres primeros nodos.
    `signo` vale +1 si apunta hacia afuera respecto de `punto_interior`.

    Sirve para cargar una presión normal a superficies con orientaciones
    distintas (presión interna de viento) usando `Dir.LOCAL_3`.
    """
    import math
    _, pl, _ = SapModel.AreaObj.GetPoints(nombre, 0, [])[:3]
    P = [SapModel.PointObj.GetCoordCartesian(p, 0, 0, 0)[:3] for p in pl]
    c = [sum(q[i] for q in P) / len(P) for i in range(3)]
    u = [P[1][i] - P[0][i] for i in range(3)]
    v = [P[2][i] - P[0][i] for i in range(3)]
    nr = [u[1] * v[2] - u[2] * v[1],
          u[2] * v[0] - u[0] * v[2],
          u[0] * v[1] - u[1] * v[0]]
    L = math.sqrt(sum(q * q for q in nr)) or 1.0
    nr = [q / L for q in nr]
    fuera = [c[i] - punto_interior[i] for i in range(3)]
    signo = 1 if sum(nr[i] * fuera[i] for i in range(3)) > 0 else -1
    return nr, signo


# --------------------------------------------------------------------------
# Ciclo de trabajo
# --------------------------------------------------------------------------

def copia_de_trabajo(SapModel, ruta: str) -> str:
    """`File.Save(ruta)` es un *Save As*: el original queda intacto en disco
    y el modelo activo pasa a ser el nuevo. Devuelve la ruta activa."""
    check(SapModel.File.Save(ruta), "File.Save")
    return SapModel.GetModelFilename(True)


def desbloquear(SapModel) -> None:
    """Tras un análisis el modelo queda bloqueado y los Set de definición
    fallan. Desbloquear **borra los resultados**: conviene agrupar todas las
    modificaciones antes de volver a analizar."""
    SapModel.SetModelIsLocked(False)


def analizar(SapModel, casos=None) -> int:
    """Marca los casos para correr (todos si `casos` es None) y analiza."""
    if casos is None:
        casos = list(SapModel.LoadCases.GetNameList(0, [])[1])
    for c in casos:
        SapModel.Analyze.SetRunCaseFlag(c, True)
    return ret_code(SapModel.Analyze.RunAnalysis())


def diseno_acero(SapModel, tabla_codigo: str, combos_si=None, combos_no=()) -> list[dict]:
    """Corre el diseño de acero y devuelve las filas del resumen.

    `combos_si`  — lista blanca (None = todas menos las de `combos_no`)
    `combos_no`  — prefijos a excluir, p. ej. ('ENV', 'S3', 'S4')

    TRAMPA: dos `StartDesign()` seguidos dejan resultados mezclados de las dos
    corridas. Se manifiesta como un máximo con **todas** las combinaciones
    menor que el máximo con un subconjunto — matemáticamente imposible.
    Por eso va `DeleteResults()` primero, siempre.
    """
    DS = SapModel.DesignSteel
    try:
        DS.DeleteResults()
    except Exception:
        pass
    todas = list(SapModel.RespCombo.GetNameList(0, [])[1])
    for c in todas:
        if combos_si is not None:
            sel = c in combos_si
        else:
            sel = not any(c.startswith(p) for p in combos_no)
        DS.SetComboStrength(c, sel)
    DS.StartDesign()
    return tabla(SapModel, tabla_codigo)


def resumen_diseno(SapModel, filas: list[dict]) -> dict:
    """Agrupa las filas del diseño por sección real de la barra.

    La tabla trae `DesignSect`, que puede diferir de la sección asignada
    cuando hay auto-select; para agrupar por perfil real hay que cruzar con
    `FrameObj.GetSection`.

    TRAMPA CRÍTICA: `Ratio = None` significa que SAP **no diseñó** la barra
    (esbeltez fuera de límite, Pu > Pe, sección no verificable…). Convertirlo
    a 0.0 la disfraza de barra holgada y la saca del recuento. Se cuentan
    aparte en `sin_disenar`, que es un dato **más** grave que un ratio > 1.
    """
    FO = SapModel.FrameObj
    sec = {f: FO.GetSection(f, "", "")[0] for f in FO.GetNameList(0, [])[1]}
    agg: dict[str, dict] = {}
    for x in filas:
        s = sec.get(x.get("Frame"), "?")
        a = agg.setdefault(s, {"n": 0, "max": 0.0, "excedidas": 0,
                               "sin_disenar": [], "peor": None, "combo": None})
        a["n"] += 1
        if x.get("Ratio") in (None, ""):
            a["sin_disenar"].append(x.get("Frame"))
            continue
        ra = num(x.get("Ratio"))
        if ra > a["max"]:
            a["max"] = round(ra, 3)
            a["peor"] = x.get("Frame")
            a["combo"] = x.get("Combo")
        if ra > 1.0:
            a["excedidas"] += 1
    return dict(sorted(agg.items(), key=lambda kv: -kv[1]["max"]))


#: Ítem de overwrite de AISC 360-16 que guarda el Fy del elemento.
#: `GetOverwrite` devuelve `(Value, ProgDet, ret)`: **`ProgDet=True` significa que
#: el valor lo puso el programa** y `False`, que alguien lo escribió a mano.
OW_FY_AISC360_16 = 35


def overwrites_acero(SapModel, item: int = OW_FY_AISC360_16,
                     objetos=None) -> list[dict]:
    """Barre un overwrite de diseño en todas las barras.

    TRAMPA QUE ESTO TAPA: un override manual de Fy no aparece en ningún lado.
    El diseño se corre con él, el D/C sale holgado y la tabla no dice nada. En
    El Pachón, 5 barras con `ProgDet=False` y Fy ≈ 784 MPa (contra 248-317
    reales) ocultaban dos elementos con D/C real 1,25 y 1,28.

    Devuelve [{'barra', 'valor', 'prog_det'}] con el valor en las unidades
    activas.
    """
    D = SapModel.DesignSteel.AISC360_16
    nombres = list(objetos or SapModel.FrameObj.GetNameList(0, [])[1])
    out = []
    for f in nombres:
        try:
            r = D.GetOverwrite(f, item, 0.0, True)
        except Exception:  # noqa: BLE001
            continue
        if ret_code(r) != 0:
            continue
        out.append({"barra": f, "valor": num(r[0]), "prog_det": bool(r[1])})
    return out


def overwrites_fy_sospechosos(SapModel, tol: float = 0.10,
                              item: int = OW_FY_AISC360_16) -> list[dict]:
    """Overwrites de Fy escritos a mano que no coinciden con su material.

    Compara cada override contra el Fy del material de la sección asignada a esa
    barra. Un valor puesto a mano que coincide con el material es inofensivo
    (alguien reescribió lo mismo); el que se aparta es el que oculta demanda.
    """
    FO = SapModel.FrameObj
    fy_mat = {}
    for x in tabla(SapModel, "Material Properties 03a - Steel Data"):
        fy_mat[x.get("Material")] = num(x.get("Fy"))
    mat_sec = {}
    for x in tabla(SapModel, "Frame Section Properties 01 - General"):
        mat_sec[x.get("SectionName")] = x.get("Material")

    out = []
    for o in overwrites_acero(SapModel, item):
        if o["prog_det"] or o["valor"] <= 0:
            continue                      # lo puso el programa: no es override
        sec = FO.GetSection(o["barra"], "", "")[0]
        fy = fy_mat.get(mat_sec.get(sec))
        if not fy:
            continue
        if abs(o["valor"] - fy) > tol * fy:
            out.append({**o, "seccion": sec, "material": mat_sec.get(sec),
                        "fy_material": fy,
                        "razon": round(o["valor"] / fy, 3)})
    return out


def mensajes_diseno(SapModel, filas: list[dict]) -> dict:
    """Agrupa los `ErrMsg`/`WarnMsg` de **todas** las barras, tengan o no ratio.

    TRAMPA QUE ESTO TAPA: `barras_sin_disenar` sólo mira `Ratio = None`, y hay
    errores que conviven con un D/C perfectamente calculado. El caso real: una
    riostra HSS con D/C 0,011 y al lado

        Error: Section is not seismically compact for moderately ductile
        members (AISC 341-16 Table D1.1)

    Leyendo sólo el ratio, el modelo parece limpio. El mensaje es el hallazgo.

    Devuelve {(tipo, mensaje): {n, secciones, ejemplos}} con tipo ERROR|AVISO.
    """
    FO = SapModel.FrameObj
    sec = {f: FO.GetSection(f, "", "")[0] for f in FO.GetNameList(0, [])[1]}
    out: dict = {}
    for x in filas:
        for tipo, msg in (("ERROR", x.get("ErrMsg")), ("AVISO", x.get("WarnMsg"))):
            msg = (msg or "").strip()
            if not msg or msg.lower() in ("no messages", "none"):
                continue
            d = out.setdefault((tipo, msg),
                               {"n": 0, "secciones": {}, "ejemplos": []})
            d["n"] += 1
            s = sec.get(x.get("Frame"), "?")
            d["secciones"][s] = d["secciones"].get(s, 0) + 1
            if len(d["ejemplos"]) < 6:
                d["ejemplos"].append(f"{x.get('Frame')} ({x.get('Combo')})")
    return out


def barras_sin_disenar(SapModel, filas: list[dict]) -> list[dict]:
    """Barras que SAP no pudo diseñar, con el motivo.

    Los mensajes que aparecen en la práctica:

    | Mensaje | Qué significa |
    |---|---|
    | `kl/r > 200 (AISC E2)` | esbeltez fuera del límite recomendado |
    | `Pu > Pe -- B1 is undefined` | la axial supera la carga de Euler: **la barra está pandeada** |
    | `kl/r > 4.0*Sqr(E/fy) (AISC 341 F1.5b)` | límite de esbeltez de riostras; salta si el `FrameType` global es OCBF/SCBF y la barra no es una riostra |
    """
    FO = SapModel.FrameObj
    out = []
    for x in filas:
        if x.get("Ratio") in (None, ""):
            fr = x.get("Frame")
            out.append({
                "frame": fr,
                "seccion": FO.GetSection(fr, "", "")[0],
                "status": x.get("Status"),
                "error": x.get("ErrMsg"),
                "aviso": x.get("WarnMsg"),
            })
    return out


# --------------------------------------------------------------------------
# Lo que hace falta para decidir un cambio de sección
# --------------------------------------------------------------------------
#
# Un D/C no dice qué comprar. Una columna a 0,95 por flexión necesita módulo
# plástico; la misma columna a 0,95 por axial necesita área; y si el que manda
# es el pandeo, necesita radio de giro o menos longitud no arriostrada. Las tres
# soluciones cuestan pesos distintos y sólo una sirve.
#
# Estas funciones existen para que el desglose se **lea**, no se suponga.

#: Nombres con los que las tablas de diseño de acero llaman a lo mismo según el
#: código y la versión de SAP. Se prueban en orden y se registra cuál se
#: encontró: un campo ausente vale `None`, nunca 0,0.
#:
#: Los de la izquierda son los de AISC 360-16 en SAP2000 v27, leídos de la tabla
#: real (`Steel Design 2 - PMM Details`) el 2026-08-15. Los alias que siguen son
#: los de otras versiones y códigos, y por eso el mapeo se resuelve en tiempo de
#: lectura y se reporta en `campos_hallados`: un nombre supuesto que no existe
#: produce un `None` visible, no un cero silencioso.
_ALIAS_PMM = {
    # demanda / capacidad
    "pr":          ("Pr", "PrDsgn", "Pu"),
    "pc_comp":     ("PcComp", "PhiPnc"),
    "pc_traccion": ("PcTension", "PhiPnt"),
    "mr_33":       ("MrMajorDsgn", "MrMajor", "MuMajor"),
    "mc_33":       ("McMajor", "PhiMnMajor"),
    "mr_22":       ("MrMinorDsgn", "MrMinor", "MuMinor"),
    "mc_22":       ("McMinor", "PhiMnMinor"),
    # ratios — lo que decide qué comprar
    "ratio_total": ("TotalRatio",),
    "p_ratio":     ("PRatio",),
    "m3_ratio":    ("MMajRatio", "MajRatio"),
    "m2_ratio":    ("MMinRatio", "MinRatio"),
    "dc_limite":   ("DCLimit",),
    "ecuacion":    ("Equation",),
    # estabilidad — de qué depende φPn
    "longitud":    ("Length",),
    "k1_33":       ("K1Major",),
    "k2_33":       ("K2Major",),
    "k1_22":       ("K1Minor",),
    "k2_22":       ("K2Minor",),
    "xl_33":       ("XLMajor",),
    "xl_22":       ("XLMinor",),
    "xl_ltb":      ("XLLTB",),
    "cb":          ("Cb",),
    # clasificación — para saber qué chequeo se aplicó y cuál no
    "clase":       ("SectClass",),
    "tipo_portico": ("FramingType",),
    "omega_0":     ("Omega0",),
    "fy":          ("Fy",),
}

#: Campos que no son números y no deben pasar por `num()`.
_PMM_TEXTO = {"ecuacion", "clase", "tipo_portico"}


def gobernante(p_ratio, m3_ratio, m2_ratio) -> tuple[str | None, float | None]:
    """Qué término del PMM manda, y qué fracción del total se lleva.

    Devuelve `(None, None)` si falta cualquiera de los tres: un término ausente
    no vale 0,0. Una columna con `PRatio` no leído y `MMajRatio = 0,9` diría
    "gobierna la flexión" con la misma cara con que lo diría una real.

    La fracción es lo que decide si el cambio de sección tiene sentido: con
    0,95 repartido 0,50/0,45 entre axial y flexión, comprar sólo módulo no
    baja el ratio a la mitad — baja lo que pesa el término de flexión.
    """
    if None in (p_ratio, m3_ratio, m2_ratio):
        return None, None
    pares = (("axial", float(p_ratio)),
             ("flexion_33", float(m3_ratio)),
             ("flexion_22", float(m2_ratio)))
    total = sum(v for _, v in pares)
    nombre, mayor = max(pares, key=lambda kv: kv[1])
    return nombre, (round(mayor / total, 3) if total > 0 else None)


def tabla_detalle_pmm(SapModel, codigo: str) -> str | None:
    """Localiza la tabla de detalle PMM del código activo, sin cablear el nombre.

    En AISC 360-16 es `Steel Design 2 - PMM Details - AISC 360-16`, pero el
    sufijo y el número cambian entre códigos y versiones. Se busca por patrón
    entre las tablas que el modelo declara disponibles.
    """
    for k in tablas_disponibles(SapModel, "PMM"):
        if "STEEL DESIGN" in k.upper():
            return k
    for k in tablas_disponibles(SapModel, "STEEL DESIGN"):
        if "DETAIL" in k.upper() and codigo.upper() in k.upper():
            return k
    return None


def detalle_pmm(SapModel, codigo: str) -> dict:
    """Desglose PMM por barra: qué término del ratio manda y por cuánto.

    Devuelve `{"tabla", "campos_hallados", "campos_ausentes", "barras": [...]}`.

    `campos_ausentes` no es decorativo: si la tabla de este código no trae
    `PRatio`, el criterio de "qué gobierna" no se puede sostener y quien lea el
    snapshot tiene que saberlo en vez de creerle a un cero.

    En AISC 360-16 / SAP v27 la tabla trae **una sola fila por barra: la
    gobernante** (799 filas para 799 barras, comprobado el 2026-08-15). Eso
    tiene una consecuencia que hay que decir en voz alta: **de acá no se puede
    sacar el D/C de una barra bajo otra combinación**. Para saber cuánto daría
    sin las combinaciones de sobrerresistencia hay que **volver a correr el
    diseño** con otra selección de combos, no filtrar esta tabla.

    Se conserva igual el `TotalRatio` máximo por barra, por si alguna versión o
    código emite una fila por combinación y estación.

    TRAMPA 2: el ratio gobernante **no** es la suma de `PRatio + MMajRatio +
    MMinRatio`. Las ecuaciones H1-1a y H1-1b de AISC 360 pesan el término axial
    de forma distinta (8/9 sobre el de flexión en H1-1a), así que sumar da un
    número que no coincide con `TotalRatio`. Se lee `TotalRatio`; los tres
    términos sirven para saber **qué** manda, no cuánto.
    """
    clave = tabla_detalle_pmm(SapModel, codigo)
    if not clave:
        return {"tabla": None, "campos_hallados": [], "campos_ausentes": list(_ALIAS_PMM),
                "barras": [], "nota": "El modelo no expone tabla de detalle PMM."}
    filas = tabla(SapModel, clave)
    if not filas:
        return {"tabla": clave, "campos_hallados": [], "campos_ausentes": list(_ALIAS_PMM),
                "barras": [], "nota": "Tabla presente pero vacía: el diseño no se corrió."}

    presentes = set(filas[0])
    mapa = {}
    for destino, alias in _ALIAS_PMM.items():
        for a in alias:
            if a in presentes:
                mapa[destino] = a
                break

    if "ratio_total" not in mapa:
        return {"tabla": clave, "campos_hallados": sorted(mapa),
                "campos_ausentes": sorted(set(_ALIAS_PMM) - set(mapa)),
                "barras": [],
                "nota": "Sin TotalRatio no se puede elegir la fila gobernante "
                        "sin sumar términos, y sumarlos es incorrecto en H1-1a."}

    FO = SapModel.FrameObj
    sec = {f: FO.GetSection(f, "", "")[0] for f in FO.GetNameList(0, [])[1]}
    col_total = mapa["ratio_total"]
    mejor: dict[str, dict] = {}
    for x in filas:
        fr = x.get("Frame")
        if not fr or x.get(col_total) in (None, ""):
            continue
        total = num(x[col_total])
        prev = mejor.get(fr)
        if prev is not None and total <= prev["ratio_total"]:
            continue
        v = {}
        for d, o in mapa.items():
            bruto = x.get(o)
            if bruto in (None, ""):
                v[d] = None
            elif d in _PMM_TEXTO:
                v[d] = str(bruto)
            else:
                v[d] = num(bruto)
        v.update({"frame": fr, "seccion": sec.get(fr, "?"), "combo": x.get("Combo")})
        mejor[fr] = v

    barras = []
    for v in mejor.values():
        gob, frac = gobernante(v.get("p_ratio"), v.get("m3_ratio"), v.get("m2_ratio"))
        v["gobierna"] = gob
        v["fraccion_del_termino"] = frac
        # Signo de Pr: negativo es compresión en SAP. Decide si hace falta radio
        # de giro (compresión) o basta área neta (tracción).
        pr = v.get("pr")
        v["esfuerzo_axial"] = None if pr is None else ("compresion" if pr < 0 else "traccion")
        barras.append(v)

    barras.sort(key=lambda b: -(b.get("ratio_total") or 0.0))
    return {"tabla": clave,
            "campos_hallados": sorted(mapa),
            "campos_ausentes": sorted(set(_ALIAS_PMM) - set(mapa)),
            "barras": barras}


def geometria_barras(SapModel) -> dict:
    """Longitud, sección y grupos de cada barra.

    La longitud real es lo que separa una esbeltez calculada de una supuesta, y
    permite convertir un ahorro de kg/m en toneladas sin volver a abrir SAP.
    """
    FO = SapModel.FrameObj
    nombres = list(FO.GetNameList(0, [])[1])
    Pt = SapModel.PointObj
    out = {}
    for f in nombres:
        try:
            i, j = FO.GetPoints(f, "", "")[:2]
            xi = Pt.GetCoordCartesian(i, 0.0, 0.0, 0.0)[:3]
            xj = Pt.GetCoordCartesian(j, 0.0, 0.0, 0.0)[:3]
            L = sum((a - b) ** 2 for a, b in zip(xi, xj)) ** 0.5
        except Exception:
            L = None
        out[f] = {"seccion": FO.GetSection(f, "", "")[0],
                  "longitud": round(L, 4) if L is not None else None}
    return out


#: Aceleración de la gravedad, para pasar de peso a masa. Existe porque
#: `TotalWt` de la tabla de secciones viene en la unidad de **fuerza** activa
#: (kN con `Units.kN_m_C`), no en toneladas. Leerlo como masa da un peso de
#: acero 9,8 veces mayor y, peor, *creíble*: 1.326,7 se lee como toneladas sin
#: chirriar, cuando son kN y equivalen a 135,2 t.
G = 9.80665


def holgura_por_seccion(resumen: dict, secciones: dict,
                        geometria: dict | None = None,
                        limite: float = 1.0) -> list[dict]:
    """Cuánto peso hay detrás de cada margen sin usar.

    NO propone secciones. Ordena las familias por *oportunidad* — peso instalado
    multiplicado por el margen disponible— para que el esfuerzo de rediseño vaya
    donde puede rendir. Una familia de 0,4 t con D/C 0,3 no vale una iteración
    de SAP; una de 100 t con D/C 0,5, sí.

    El margen se mide contra el D/C **máximo** de la familia, no el promedio:
    la sección la fija la barra peor, no la media.

    `limite` es el techo real del diseño (`SRatioLimit` de las preferencias), que
    no tiene por qué ser 1,0. Con el límite en 0,95, una familia a 0,949 tiene
    margen **0,001**, no 0,051. Medir contra 1,0 inventa un 5 % que no existe.
    """
    out = []
    for s, r in resumen.items():
        peso = (secciones.get(s) or {}).get("peso_total")
        dc = r.get("max") or 0.0
        if not peso or dc <= 0:
            continue
        margen = max(0.0, limite - dc)
        n_barras = r.get("n") or 0
        L = None
        if geometria:
            Ls = [g["longitud"] for g in geometria.values()
                  if g.get("seccion") == s and g.get("longitud")]
            L = round(sum(Ls), 2) if Ls else None
        masa_t = peso / G
        out.append({
            "seccion": s,
            "n": n_barras,
            #: tal como sale de la tabla: unidad de FUERZA activa (kN)
            "peso_kN": round(peso, 2),
            "masa_t": round(masa_t, 2),
            "longitud_total": L,
            "dc_max": dc,
            "dc_limite": limite,
            "barra_peor": r.get("peor"),
            "combo_gobernante": r.get("combo"),
            "margen": round(margen, 3),
            #: cota SUPERIOR del ahorro, no una predicción: supone que la masa
            #: escala con el ratio, y eso es falso siempre que el que manda es
            #: el pandeo o la rigidez. Sirve para priorizar, no para prometer.
            "oportunidad_t_cota": round(masa_t * margen, 2),
            "sin_disenar": len(r.get("sin_disenar") or []),
        })
    out.sort(key=lambda d: -d["oportunidad_t_cota"])
    return out


__all__ = [
    "Units", "ItemType", "LoadPatternType", "Dir", "DistType",
    "ComboType", "CNameType",
    "PIN", "PIN_SLIDE", "FIXED",
    "REL_P", "REL_V2", "REL_V3", "REL_T", "REL_M2", "REL_M3",
    "ret_code", "ok", "check", "num",
    "tabla", "tablas_disponibles", "masa_total", "seleccionar_salida",
    "reacciones_base", "modos", "periodo_traslacional",
    "inventario", "conectividad", "nodos_huerfanos",
    "liberaciones_por_seccion", "liberaciones_arriostramiento", "normal_area",
    "copia_de_trabajo", "desbloquear", "analizar",
    "diseno_acero", "resumen_diseno", "barras_sin_disenar", "mensajes_diseno",
    "overwrites_acero", "overwrites_fy_sospechosos", "OW_FY_AISC360_16",
    "gobernante", "tabla_detalle_pmm", "detalle_pmm",
    "geometria_barras", "holgura_por_seccion",
]
