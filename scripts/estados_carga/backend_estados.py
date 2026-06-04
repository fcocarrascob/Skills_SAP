"""
Backend — Estados de Carga (Standalone)
========================================
Modelo de datos puro (sin dependencia de SAP2000) que mantiene el mapeo

    símbolo normativo  ->  lista de nombres de casos de carga reales

Ej.:  "D" -> ["PP", "SC_perm", "Equipos"]

Sirve como base para que una iteración futura genere/verifique las combinaciones
normativas (NCh3171 / NCh2369) por fuera de SAP2000.
"""

import json

from config_estados import STATE_DEFINITIONS, STATE_KEYS


class EstadosCargaModel:
    """Mapeo símbolo normativo → lista de nombres de casos de carga."""

    def __init__(self):
        # Inicializa todas las claves normativas con listas vacías, en orden.
        self._states = {key: [] for key in STATE_KEYS}

    # ── Consultas ────────────────────────────────────────────────────────

    def names(self, key: str) -> list:
        """Lista de nombres asociados a un estado (copia defensiva)."""
        return list(self._states.get(key, []))

    def keys(self) -> list:
        """Claves de estado en orden de definición."""
        return list(STATE_KEYS)

    # ── Mutaciones ───────────────────────────────────────────────────────

    def add_name(self, key: str, name: str) -> bool:
        """Agrega un nombre a un estado.

        Normaliza (strip). Rechaza clave desconocida, nombre vacío o duplicado
        dentro del mismo estado. Retorna True si se agregó.
        """
        if key not in self._states:
            return False
        name = (name or "").strip()
        if not name:
            return False
        if name in self._states[key]:
            return False
        self._states[key].append(name)
        return True

    def remove_name(self, key: str, name: str) -> bool:
        """Elimina un nombre de un estado. Retorna True si existía."""
        if key in self._states and name in self._states[key]:
            self._states[key].remove(name)
            return True
        return False

    def clear(self) -> None:
        """Vacía todos los estados (conserva las claves)."""
        for key in self._states:
            self._states[key] = []

    # ── Serialización ────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Exporta el mapeo en orden de definición."""
        return {key: list(self._states[key]) for key in STATE_KEYS}

    def load_dict(self, data: dict) -> None:
        """Carga desde un dict tolerante: ignora claves desconocidas y
        valores no-lista; conserva el orden y las claves de STATE_DEFINITIONS."""
        self.clear()
        if not isinstance(data, dict):
            return
        for key in STATE_KEYS:
            value = data.get(key)
            if isinstance(value, list):
                for name in value:
                    self.add_name(key, str(name))

    def save(self, path: str) -> None:
        """Guarda el mapeo a un archivo JSON."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        """Carga el mapeo desde un archivo JSON."""
        with open(path, "r", encoding="utf-8") as fh:
            self.load_dict(json.load(fh))


# ══════════════════════════════════════════════════════════════════════════════
# Cargas en el nodo — modelo tabular (tipo "Joint Loads - Force")
# ══════════════════════════════════════════════════════════════════════════════

# Componentes de fuerza/momento (sin Joint ni CoordSys: nodo único asumido).
FORCE_KEYS = ["fx", "fy", "fz", "mx", "my", "mz"]


def parse_force(text) -> float:
    """Convierte un valor de celda a float.

    Tolera separador decimal coma (Excel es-CL), espacios y celdas vacías.
    Valores no numéricos se interpretan como 0.0.
    """
    if text is None:
        return 0.0
    s = str(text).strip().replace(",", ".")
    if s == "":
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


def make_load_row(load_pat: str = "", **forces) -> dict:
    """Construye una fila de carga normalizada."""
    row = {"load_pat": str(load_pat).strip()}
    for k in FORCE_KEYS:
        row[k] = parse_force(forces.get(k, 0.0))
    return row


class LoadsModel:
    """Tabla de cargas de un nodo: filas con load_pat + 6 componentes."""

    def __init__(self):
        self._rows = []  # list[dict]

    def rows(self) -> list:
        """Copia de las filas."""
        return [dict(r) for r in self._rows]

    def set_rows(self, rows) -> None:
        """Reemplaza las filas (normalizando cada una)."""
        self._rows = [make_load_row(**r) for r in rows]

    def to_list(self) -> list:
        return self.rows()

    def load_list(self, data) -> None:
        """Carga tolerante desde una lista de dicts."""
        self._rows = []
        if not isinstance(data, list):
            return
        for r in data:
            if isinstance(r, dict):
                self._rows.append(make_load_row(**r))


# ══════════════════════════════════════════════════════════════════════════════
# Cálculo de resultantes (resumen por estado y por combinación)
# ══════════════════════════════════════════════════════════════════════════════

def _empty_vector() -> dict:
    return {k: 0.0 for k in FORCE_KEYS}


def loads_by_name(rows) -> dict:
    """Agrupa filas de carga por load_pat, sumando componentes.

    Args:
        rows: lista de dicts (p. ej. salida de LoadsModel.to_list() o de la grilla).

    Returns:
        dict nombre -> {fx..mz} (sumado si un nombre aparece varias veces).
    """
    out = {}
    for r in rows:
        name = str(r.get("load_pat", "")).strip()
        if not name:
            continue
        v = out.setdefault(name, _empty_vector())
        for k in FORCE_KEYS:
            v[k] += parse_force(r.get(k, 0.0))
    return out


def state_resultants(estados: "EstadosCargaModel", by_name: dict) -> dict:
    """Resultante (suma) de cada estado normativo.

    Por estado, suma las cargas de todos sus nombres asignados.

    Returns:
        dict símbolo -> {"vector": {fx..mz}, "n_names": int, "missing": [nombres
        sin carga]}.
    """
    res = {}
    for key in estados.keys():
        v = _empty_vector()
        names = estados.names(key)
        missing = []
        for name in names:
            nv = by_name.get(name)
            if nv is None:
                missing.append(name)
                continue
            for k in FORCE_KEYS:
                v[k] += nv[k]
        res[key] = {"vector": v, "n_names": len(names), "missing": missing}
    return res


def combo_resultant(items, state_res: dict) -> dict:
    """Resultante de una combinación: suma de factor × resultante-de-cada-estado."""
    v = _empty_vector()
    for sym, factor in items:
        entry = state_res.get(sym)
        if entry is None:
            continue
        sv = entry["vector"]
        for k in FORCE_KEYS:
            v[k] += factor * sv[k]
    return v


def combo_resultants(combos, state_res: dict) -> list:
    """Aplica combo_resultant a una lista de combinaciones.

    Args:
        combos: lista de (nombre, items) o (método, nombre, items).
        state_res: salida de state_resultants.

    Returns:
        lista de dicts {method?, name, vector}.
    """
    out = []
    for combo in combos:
        if len(combo) == 3:
            method, name, items = combo
            out.append({"method": method, "name": name,
                        "vector": combo_resultant(items, state_res)})
        else:
            name, items = combo
            out.append({"name": name, "vector": combo_resultant(items, state_res)})
    return out


# ══════════════════════════════════════════════════════════════════════════════
# Proyecto combinado (estados + cargas) — persistencia única
# ══════════════════════════════════════════════════════════════════════════════

def save_project(path: str, estados: "EstadosCargaModel", loads: "LoadsModel") -> None:
    """Guarda estados de carga + cargas en un único JSON."""
    data = {"estados": estados.to_dict(), "cargas": loads.to_list()}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def load_project(path: str, estados: "EstadosCargaModel", loads: "LoadsModel") -> None:
    """Carga un JSON de proyecto en los modelos dados.

    Compatible con el formato heredado (dict plano = solo estados).
    """
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if isinstance(data, dict) and ("estados" in data or "cargas" in data):
        estados.load_dict(data.get("estados", {}))
        loads.load_list(data.get("cargas", []))
    else:
        # Formato heredado: el dict completo era el mapeo de estados.
        estados.load_dict(data)
        loads.load_list([])


# ══════════════════════════════════════════════════════════════════════════════
# Mini-test standalone (sin GUI)
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    m = EstadosCargaModel()

    # Agregar nombres válidos
    assert m.add_name("D", "PP") is True
    assert m.add_name("D", "SC_perm") is True
    assert m.add_name("Ex", "SX") is True
    assert m.names("D") == ["PP", "SC_perm"]

    # Rechazos: duplicado, vacío, clave desconocida
    assert m.add_name("D", "PP") is False, "duplicado debe rechazarse"
    assert m.add_name("D", "   ") is False, "vacío debe rechazarse"
    assert m.add_name("XX", "algo") is False, "clave desconocida debe rechazarse"

    # Normalización (strip)
    assert m.add_name("L", "  SCU  ") is True
    assert m.names("L") == ["SCU"]

    # Eliminar
    assert m.remove_name("D", "PP") is True
    assert m.remove_name("D", "noexiste") is False
    assert m.names("D") == ["SC_perm"]

    # Round-trip serialización
    data = m.to_dict()
    m2 = EstadosCargaModel()
    m2.load_dict(data)
    assert m2.to_dict() == data, "round-trip debe preservar el mapeo"

    # Tolerancia: claves desconocidas y tipos inválidos se ignoran
    m3 = EstadosCargaModel()
    m3.load_dict({"D": ["A", "B"], "ZZ": ["x"], "L": "no-es-lista"})
    assert m3.names("D") == ["A", "B"]
    assert m3.names("L") == []

    # ── Cargas: parseo tolerante (coma decimal, vacío, basura) ──────────
    assert parse_force("-0,02") == -0.02
    assert parse_force("  5,21 ") == 5.21
    assert parse_force("") == 0.0
    assert parse_force("xx") == 0.0
    assert parse_force(3) == 3.0

    loads = LoadsModel()
    loads.set_rows([
        {"load_pat": "DEAD", "fx": "-0,02", "fy": "-0,09", "fz": "-1,06"},
        {"load_pat": "Ex", "fx": "0,14", "mz": "0"},
    ])
    assert loads.rows()[0]["fz"] == -1.06
    assert loads.rows()[1]["load_pat"] == "Ex"
    assert loads.rows()[0]["mx"] == 0.0  # default

    # ── Proyecto combinado: round-trip por archivo ──────────────────────
    import tempfile, os
    tmp = os.path.join(tempfile.gettempdir(), "_estados_carga_test.json")
    save_project(tmp, m, loads)

    m_load, l_load = EstadosCargaModel(), LoadsModel()
    load_project(tmp, m_load, l_load)
    assert m_load.to_dict() == m.to_dict()
    assert l_load.to_list() == loads.to_list()

    # ── Compatibilidad con formato heredado (dict plano = estados) ──────
    legacy = os.path.join(tempfile.gettempdir(), "_estados_carga_legacy.json")
    with open(legacy, "w", encoding="utf-8") as fh:
        json.dump({"D": ["PP"], "L": ["SCU"]}, fh)
    m_leg, l_leg = EstadosCargaModel(), LoadsModel()
    load_project(legacy, m_leg, l_leg)
    assert m_leg.names("D") == ["PP"]
    assert l_leg.to_list() == []

    os.remove(tmp)
    os.remove(legacy)

    # ── Resultantes: resumen por estado y por combinación ────────────────
    est = EstadosCargaModel()
    est.add_name("D", "DEAD")
    est.add_name("D", "EquipD")   # dos nombres en D
    est.add_name("L", "SCU")
    by_name = loads_by_name([
        {"load_pat": "DEAD",   "fz": -10.0},
        {"load_pat": "EquipD", "fz": -4.0},
        {"load_pat": "SCU",    "fz": -6.0},
        {"load_pat": "HUERFANO", "fz": -99.0},  # no asignado a ningún estado
    ])
    sr = state_resultants(est, by_name)
    assert sr["D"]["vector"]["fz"] == -14.0   # -10 + -4
    assert sr["D"]["n_names"] == 2
    assert sr["L"]["vector"]["fz"] == -6.0
    assert sr["S"]["vector"]["fz"] == 0.0     # sin nombres

    # nombre asignado pero sin carga aparece en missing
    est.add_name("R", "LluviaSinCarga")
    sr2 = state_resultants(est, by_name)
    assert sr2["R"]["missing"] == ["LluviaSinCarga"]

    # Combo 1.2D + 1.6L: 1.2*(-14) + 1.6*(-6) = -16.8 - 9.6 = -26.4
    cr = combo_resultant([("D", 1.2), ("L", 1.6)], sr)
    assert abs(cr["fz"] - (-26.4)) < 1e-9, cr["fz"]

    crs = combo_resultants([("LRFD", "C1", [("D", 1.4)])], sr)
    assert crs[0]["method"] == "LRFD"
    assert abs(crs[0]["vector"]["fz"] - (-19.6)) < 1e-9

    print("OK — backend_estados: todas las aserciones pasaron.")
    print(json.dumps(m.to_dict(), ensure_ascii=False, indent=2))
