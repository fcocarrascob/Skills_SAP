# Estados de Carga

Mini app **independiente de SAP2000** con tres pestañas:

1. **Estados de Carga** — asocia, a cada estado normativo (NCh3171 / NCh2369),
   uno o más nombres de casos de carga reales del modelo.
2. **Cargas** — grilla tipo Excel con las cargas de **un nodo** (Load Pat +
   Fx Fy Fz Mx My Mz).
3. **Resultados** — resumen de la resultante sumada por estado y la resultante
   de cada combinación normativa fija aplicada al nodo.

El proyecto (estados + cargas) se persiste en un único JSON.

## Concepto

Las normas usan símbolos genéricos (`D`, `L`, `Lr`, `S`, `R`, `W`, `E`, `SO`,
`SA`, `aL`). En un modelo real, cada símbolo puede mapear a **varios** casos con
nombres arbitrarios:

```
D  -> ["PP", "SC_perm", "Equipos"]
Ex -> ["SX"]
```

Esta app define ese mapeo símbolo → lista de nombres.

## Uso

```bash
# Activar el venv del proyecto, luego:
python scripts/estados_carga/gui_estados.py
```

### Pestaña «Estados de Carga»

- Cada fila es un estado normativo fijo. Escribe un nombre en **Nombre** y pulsa
  **Agregar** (o Enter) para añadirlo a ese estado; aparece como un *chip*.
- Click en el `✕` de un chip para quitar ese nombre.

### Pestaña «Cargas»

Grilla tipo Excel con las cargas de un nodo (se asume nodo único; sin columnas
Joint ni CoordSys). Columnas: `Load Pat`, `Fx`, `Fy`, `Fz` (tonf), `Mx`, `My`,
`Mz` (tonf·m).

- **Copiar/pegar** como en Excel: `Ctrl+C` / `Ctrl+V`. El pegado acepta bloques
  separados por TAB y reconoce el separador decimal **coma** (Excel es-CL);
  agrega filas automáticamente si hace falta. `Supr` limpia las celdas
  seleccionadas.
- **Load Pat** se valida contra los nombres de la pestaña 1: si no coincide, la
  celda se resalta en **rojo**.
- **Agregar fila** / **Eliminar fila(s)** y **Cargar desde Estados** (genera una
  fila por cada nombre definido en la pestaña 1, con fuerzas en 0).

**Guardar** / **Cargar** (barra inferior) persisten ambas pestañas en un único
archivo JSON.

### Pestaña «Resultados»

Se recalcula automáticamente al entrar (o con **Recalcular**):

- **Resumen por Estado** — para cada estado con nombres asignados, la resultante
  **sumada** (Fx Fy Fz Mx My Mz) de todas sus cargas, más la cantidad de nombres.
- **Combinaciones** — las ~190 combinaciones fijas (LRFD + ASD, NCh3171 +
  NCh2369 industrial) con la resultante en el nodo:
  `Σ factor × resultante-de-cada-estado`.
- Avisos: cargas con un `Load Pat` que no pertenece a ningún estado (huérfanas) y
  nombres asignados sin carga.

Las combinaciones están **hardcodeadas** en `combos_norma.py`, generadas a partir
del set canónico del proyecto (`modelo_base/patterns_comb_lineal.py`) remapeando
los nombres de caso SAP a los símbolos de la app (`DEAD→D`, `WINDX→Wx`,
`EQX→Ex`, ...).

## Formato del JSON

```json
{
  "estados": {
    "D": ["PP", "SC_perm"],
    "L": ["SCU"],
    "Ex": ["SX"],
    "...": []
  },
  "cargas": [
    {"load_pat": "DEAD", "fx": -0.02, "fy": -0.09, "fz": -1.06,
     "mx": 0.0, "my": 0.0, "mz": 0.0}
  ]
}
```

> Compatibilidad: un JSON heredado con solo el mapeo de estados (dict plano, sin
> las claves `estados`/`cargas`) sigue cargando correctamente.

## Archivos

- `config_estados.py` — lista fija `STATE_DEFINITIONS` (símbolo, label,
  descripción, rol normativo y `sap_type` para uso futuro).
- `combos_norma.py` — combinaciones LRFD/ASD hardcodeadas (símbolos de la app).
- `backend_estados.py` — modelos puros + JSON + cálculo de resultantes
  (`EstadosCargaModel`, `LoadsModel`, `state_resultants`, `combo_resultants`).
  Ejecutable directo para correr su mini-test: `python backend_estados.py`.
- `gui_estados.py` — interfaz PySide6 de 3 pestañas (estilo Fusion).
- `verificar_resultados.py` — set de prueba con números redondos: arma un caso,
  lo guarda como `ejemplo_verificacion.json` y comprueba las resultantes por
  estado y por combinación contra el cálculo manual. `python verificar_resultados.py`.
- `ejemplo_verificacion.json` — proyecto de ejemplo cargable desde la GUI
  («Cargar»), generado por el script anterior.

## Set de prueba / verificación

```bash
python scripts/estados_carga/verificar_resultados.py
```

Caso con números redondos verificable a mano:

| Estado | Nombres        | Resultante (Fz / otros) |
|--------|----------------|-------------------------|
| D      | PP, Equipos    | Fz = −15, Mz = 1        |
| L      | SCU            | Fz = −8,  My = 2        |
| Lr     | Techo          | Fz = −3                 |
| Wx     | Wx1            | Fx = 4, Fy = 1          |
| Ex     | SismoX         | Fx = 6, Fz = −2, Mx = 3 |

Comprobaciones (ejemplos): `1.4D` → Fz = −21, Mz = 1.4; `1.2D+1.6L+0.5Lr` →
Fz = −32.3, My = 3.2, Mz = 1.2. El script imprime cada resultante con `OK` y
falla con detalle si alguna no coincide. Cargá `ejemplo_verificacion.json` en la
GUI para ver el mismo caso en pantalla.

## Próxima iteración

Generación/verificación de las combinaciones normativas reusando:

- Simbología y combinaciones de `../../Docs/comb_cargas_norma.md`.
- Pesos `LRFD_COMBOS` / `ASD_COMBOS` de
  `../modelo_base/patterns_comb_lineal.py`.
- `sap_type` (`ELoadPatternType`) para, opcionalmente, crear los patrones en
  SAP2000 vía COM (`comtypes`).
