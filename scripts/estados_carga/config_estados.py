"""
Config — Estados de Carga (Standalone)
=======================================
Definición fija de los estados de carga normativos (NCh3171 / NCh2369).

Cada entrada describe un símbolo normativo genérico al que, en la GUI, el usuario
asocia uno o más nombres de casos de carga reales de su modelo.

Campos:
    key         Símbolo normativo (clave interna y de serialización).
    label       Texto mostrado en la fila de la GUI.
    description Descripción larga (tooltip).
    role        Rol normativo — base para la futura generación de combinaciones.
    sap_type    ELoadPatternType de SAP2000 — uso futuro al crear patrones en SAP.
                (DEAD=1, LIVE=3, QUAKE=5, WIND=6, SNOW=7, OTHER=8, TEMP=10, ROOF=11)
                Ver ELOADTYPE en scripts/modelo_base/patterns_comb_lineal.py
"""

STATE_DEFINITIONS = [
    {"key": "D",  "label": "D: Dead",  "description": "Carga muerta",                    "role": "D",  "sap_type": 1},
    {"key": "L",  "label": "L: Live",  "description": "Carga viva",                      "role": "L",  "sap_type": 3},
    {"key": "Lr", "label": "Lr: Roof", "description": "Carga viva de techo",             "role": "Lr", "sap_type": 11},
    {"key": "S",  "label": "S: Snow",  "description": "Carga de nieve",                  "role": "S",  "sap_type": 7},
    {"key": "R",  "label": "R: Rain",  "description": "Carga de lluvia",                 "role": "R",  "sap_type": 8},
    {"key": "Wx", "label": "Wx",       "description": "Viento dirección X",              "role": "W",  "sap_type": 6},
    {"key": "Wy", "label": "Wy",       "description": "Viento dirección Y",              "role": "W",  "sap_type": 6},
    {"key": "Ex", "label": "Ex",       "description": "Sismo dirección X",               "role": "E",  "sap_type": 5},
    {"key": "Ey", "label": "Ey",       "description": "Sismo dirección Y",               "role": "E",  "sap_type": 5},
    {"key": "Ez", "label": "Ez",       "description": "Sismo vertical",                  "role": "E",  "sap_type": 5},
    {"key": "SO", "label": "SO",       "description": "Carga de operación (NCh2369)",    "role": "SO", "sap_type": 8},
    {"key": "SA", "label": "SA",       "description": "Sismo accidental (NCh2369)",      "role": "SA", "sap_type": 5},
    {"key": "aL", "label": "aL",       "description": "Fracción carga viva (NCh2369)",   "role": "aL", "sap_type": 3},
    {"key": "T",  "label": "T: Temp",  "description": "Temperatura",                     "role": "T",  "sap_type": 10},
]

# Orden y catálogo de claves válidas (deriva siempre de STATE_DEFINITIONS).
STATE_KEYS = [s["key"] for s in STATE_DEFINITIONS]

DEFAULT_SAVE_FILE = "estados_carga.json"
