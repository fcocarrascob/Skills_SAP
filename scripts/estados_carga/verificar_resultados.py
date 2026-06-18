"""
Set de prueba — verificación de resultados
============================================
Construye un caso con NÚMEROS REDONDOS (verificable a mano), lo guarda como
`ejemplo_verificacion.json` (cargable desde la GUI con «Cargar») y comprueba que
las resultantes por estado y por combinación coinciden con los valores
calculados manualmente.

Ejecutar:
    python verificar_resultados.py
"""

import os
import sys

# Consola Windows (cp1252) → forzar UTF-8 para los caracteres de caja/acentos.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from backend_estados import (
    EstadosCargaModel, LoadsModel, FORCE_KEYS,
    loads_by_name, state_resultants, combo_resultant, save_project,
)
from combos_norma import COMBOS_BY_METHOD


HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_PATH = os.path.join(HERE, "ejemplo_verificacion.json")


# ══════════════════════════════════════════════════════════════════════════════
# Datos del set de prueba
# ══════════════════════════════════════════════════════════════════════════════

# Mapeo estado normativo -> nombres de casos de carga.
ESTADOS = {
    "D":  ["PP", "Equipos"],
    "L":  ["SCU"],
    "Lr": ["Techo"],
    "Wx": ["Wx1"],
    "Ex": ["SismoX"],
}

# Cargas en el nodo (componentes no indicadas = 0).
CARGAS = [
    {"load_pat": "PP",     "fz": -10.0},
    {"load_pat": "Equipos","fz": -5.0, "mz": 1.0},
    {"load_pat": "SCU",    "fz": -8.0, "my": 2.0},
    {"load_pat": "Techo",  "fz": -3.0},
    {"load_pat": "Wx1",    "fx": 4.0, "fy": 1.0},
    {"load_pat": "SismoX", "fx": 6.0, "fz": -2.0, "mx": 3.0},
]

# ── Resultantes por estado esperadas (suma de las cargas de sus nombres) ──────
#   D  = PP + Equipos     -> Fz=-15, Mz=1
#   L  = SCU              -> Fz=-8,  My=2
#   Lr = Techo            -> Fz=-3
#   Wx = Wx1              -> Fx=4,   Fy=1
#   Ex = SismoX           -> Fx=6,   Fz=-2, Mx=3
EXPECTED_STATES = {
    "D":  {"fx": 0,  "fy": 0, "fz": -15, "mx": 0, "my": 0, "mz": 1},
    "L":  {"fx": 0,  "fy": 0, "fz": -8,  "mx": 0, "my": 2, "mz": 0},
    "Lr": {"fx": 0,  "fy": 0, "fz": -3,  "mx": 0, "my": 0, "mz": 0},
    "Wx": {"fx": 4,  "fy": 1, "fz": 0,   "mx": 0, "my": 0, "mz": 0},
    "Ex": {"fx": 6,  "fy": 0, "fz": -2,  "mx": 3, "my": 0, "mz": 0},
}

# ── Combinaciones esperadas (cálculo a mano) ─────────────────────────────────
#   LRFD_1 = 1.4D (+1.4T, T=0)
#       Fz = 1.4·(-15) = -21      Mz = 1.4·1 = 1.4
#   LRFD_2.R = 1.2D + 1.6L + 0.5Lr (+1.2T)
#       Fz = 1.2·(-15) + 1.6·(-8) + 0.5·(-3) = -18 -12.8 -1.5 = -32.3
#       My = 1.6·2 = 3.2          Mz = 1.2·1 = 1.2
#   ASD_5a.1 = 1.0D + 1.0Wx (+1.0T)
#       Fx = 4   Fy = 1   Fz = -15   Mz = 1
#   ASD_NCh.9x = 1.0D + 0.75SA + 0.7Ex + 0.21Ey + 0.21Ez (+1.0T)   (SA,Ey,Ez,T = 0)
#       Fx = 0.7·6 = 4.2   Fz = -15 + 0.7·(-2) = -16.4   Mx = 0.7·3 = 2.1   Mz = 1
EXPECTED_COMBOS = {
    "LRFD_1_+1.4D_+1.4T":
        {"fx": 0, "fy": 0, "fz": -21.0, "mx": 0, "my": 0, "mz": 1.4},
    "LRFD_2.R_+1.2D_+1.6L_+0.5R_+1.2T":
        {"fx": 0, "fy": 0, "fz": -32.3, "mx": 0, "my": 3.2, "mz": 1.2},
    "ASD_5a.1_+1.0D_+1.0WX_+1.0T":
        {"fx": 4, "fy": 1, "fz": -15, "mx": 0, "my": 0, "mz": 1},
    "ASD_NCh.9x_+1.0D_+0.75SA_+0.7EQX_+0.21EQY_+0.21EQZ_+1.0T":
        {"fx": 4.2, "fy": 0, "fz": -16.4, "mx": 2.1, "my": 0, "mz": 1},
}

TOL = 1e-9


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _vec_str(v: dict) -> str:
    return "  ".join(f"{k}={v[k]:+.3g}" for k in FORCE_KEYS)


def _assert_vec(label: str, got: dict, exp: dict) -> None:
    for k in FORCE_KEYS:
        if abs(got[k] - exp[k]) > TOL:
            raise AssertionError(
                f"{label}: componente {k} = {got[k]} (esperado {exp[k]})")


# ══════════════════════════════════════════════════════════════════════════════
# Programa
# ══════════════════════════════════════════════════════════════════════════════

def build_models():
    estados = EstadosCargaModel()
    for key, names in ESTADOS.items():
        for n in names:
            estados.add_name(key, n)
    loads = LoadsModel()
    loads.set_rows(CARGAS)
    return estados, loads


def main():
    estados, loads = build_models()

    # 1) Guardar el fixture para poder cargarlo en la GUI.
    save_project(FIXTURE_PATH, estados, loads)
    print(f"Fixture guardado en: {FIXTURE_PATH}\n")

    # 2) Calcular resultantes.
    by_name = loads_by_name(loads.to_list())
    sr = state_resultants(estados, by_name)

    # 3) Verificar resumen por estado.
    print("── Resumen por estado ────────────────────────────────────────")
    for key, exp in EXPECTED_STATES.items():
        got = sr[key]["vector"]
        _assert_vec(f"Estado {key}", got, exp)
        print(f"  {key:>2} ({sr[key]['n_names']} nombre/s):  {_vec_str(got)}   OK")

    # 4) Verificar combinaciones seleccionadas.
    combo_items = {name: items for _, name, items in COMBOS_BY_METHOD}
    print("\n── Combinaciones verificadas ─────────────────────────────────")
    for name, exp in EXPECTED_COMBOS.items():
        if name not in combo_items:
            raise AssertionError(f"Combinación no encontrada: {name}")
        got = combo_resultant(combo_items[name], sr)
        _assert_vec(name, got, exp)
        print(f"  {name}")
        print(f"      {_vec_str(got)}   OK")

    print(f"\nTotal de combinaciones en el set: {len(COMBOS_BY_METHOD)}")
    print("\n✔ Todas las resultantes coinciden con el cálculo manual.")


if __name__ == "__main__":
    main()
