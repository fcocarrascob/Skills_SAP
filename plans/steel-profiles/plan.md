# Steel Profiles — Modelado de Perfiles como Placas Shell

**Branch:** `feat/steel-profiles-shell-plates`
**Description:** Nueva pestaña en el módulo steel_connections para modelar perfiles de acero (W, HSS, L, C) como elementos Shell (placas), con soporte para orientación en plano e inclinación arbitraria.

## Goal

Permitir al usuario modelar perfiles de acero estándar (W, HSS, L, C) en SAP2000 como conjuntos de placas (Area elements) que representan las alas, almas y paredes del perfil. El usuario define tipo de perfil, dimensiones, largo, plano de extensión e inclinación, y el backend genera los elementos Shell correspondientes. Se integra como segunda pestaña del módulo `steel_connections` junto al existente Bolt Plates.

## Definición de Perfiles

Cada perfil se descompone en placas rectangulares según su sección transversal:

| Perfil | Placas | Parámetros de sección |
|--------|--------|-----------------------|
| **W** (Wide Flange) | Ala superior + Alma + Ala inferior | d, bf, tf, tw |
| **HSS** (Rectangular) | 4 paredes (Top, Bot, Left, Right) | B, H, t |
| **L** (Ángulo) | Ala vertical + Ala horizontal | b1, b2, t |
| **C** (Canal) | Alma + Ala superior + Ala inferior | d, bf, tf, tw |

## Sistema de Coordenadas

- **Plano** (XZ, YZ, XY): define en qué plano global se extiende el largo del perfil.
- **Ángulo** (θ°): inclinación dentro de ese plano respecto al primer eje (e.g., en XZ: 0° = horizontal a lo largo de X, 90° = vertical a lo largo de Z).

Ejes locales derivados:

| Eje local | Definición | Ejemplo (plano XZ, θ) |
|-----------|------------|-----------------------|
| ê_L (largo) | Dirección longitudinal del perfil | (cos θ, 0, sin θ) |
| ê_d (peralte) | Perpendicular a ê_L, contenido en el plano | (−sin θ, 0, cos θ) |
| ê_w (ancho) | Fuera del plano (eje restante) | (0, 1, 0) |

Transformación: `P_global = origin + u·ê_L + v·ê_d + w·ê_w`

## Implementation Steps

### Step 1: Backend — Motor de Geometría de Perfiles
**Files:** `scripts/steel_connections/backend_steel_profiles.py` (NUEVO)

**What:** Crear el backend completo con:

1. **`SteelProfileConfig` dataclass:**
   - `profile_type: str` — "W" | "HSS" | "L" | "C"
   - Dimensiones de sección: `d, bf, tf, tw` (W/C), `B, H, t` (HSS), `b1, b2, t` (L)
   - `length: float` — largo del perfil
   - `origin_x/y/z: float` — punto base (inicio del perfil)
   - `plane: str` — "XZ" | "YZ" | "XY"
   - `angle: float` — inclinación en grados (0° = horizontal en el plano)
   - `n_length: int` — divisiones a lo largo del perfil
   - `n_width: int` — divisiones a lo ancho de cada placa
   - `area_prop: str` — nombre de propiedad Shell existente en el modelo

2. **Sistema de coordenadas** (`_build_axes`):
   - Calcula `(ê_L, ê_d, ê_w)` a partir de `plane` y `angle`
   - Función `_local_to_global(u, v, w)` → `(X, Y, Z)`

3. **Generadores de geometría** por tipo de perfil:
   - `_plates_W(config)` → lista de definiciones de placa `[(offset_d, offset_w, span_axis, plate_width), ...]`
   - `_plates_HSS(config)` → ídem
   - `_plates_L(config)` → ídem
   - `_plates_C(config)` → ídem
   - Cada placa definida por: offset en sección transversal + eje de extensión + ancho

4. **`run(config)` workflow:**
   - Task 1: Construir ejes locales
   - Task 2: Obtener lista de placas según `profile_type`
   - Task 3: Para cada placa, generar grilla de `n_length × n_width` celdas
   - Task 4: Crear área elements vía `AreaObj.AddByCoord(4, xs, ys, zs, "", prop, "", "Global")`
   - Task 5: Asignar grupo para identificación
   - Retorna: `{"success": bool, "num_areas": int, "num_plates": int, "profile_type": str, ...}`

5. **Reutilizar** `SapConnection` del módulo existente (importar desde `backend_bolt_plates`).

**Testing:**
- Ejecutar standalone (`if __name__ == "__main__"`) con SAP2000 abierto
- Verificar que un perfil W genera 3 placas × (n_length × n_width) = N áreas
- Verificar posicionamiento correcto con inclinación ≠ 0°

---

### Step 2: GUI — Widget de Perfiles de Acero con Preview
**Files:** `scripts/steel_connections/gui_steel_profiles.py` (NUEVO)

**What:** Crear el widget GUI completo (QWidget) con:

1. **Workers** (QThread): `ConnectWorker`, `DisconnectWorker`, `RunWorker` — mismo patrón que `gui_bolt_plates.py`, compartiendo `SapConnection`.

2. **`ProfilePreviewWidget(QWidget)`:**
   - Vista de sección transversal (2D): dibuja las placas del perfil seleccionado con cotas
   - Vista lateral (elevación): muestra el perfil en su largo con la inclinación
   - Se actualiza dinámicamente al cambiar tipo de perfil o dimensiones
   - Seguir patrón de `BoltPreviewWidget` (QPainter, `_draw_dimension()`)

3. **`SteelProfilesGUI(QWidget)`** — Panel de parámetros:
   - **Grupo "Tipo de Perfil"**: QComboBox con W, HSS, L, C
   - **Grupo "Dimensiones de Sección"**: Campos dinámicos según tipo seleccionado
     - W/C: d, bf, tf, tw
     - HSS: B, H, t
     - L: b1, b2, t
   - **Grupo "Longitud y Orientación"**: length, plane (QComboBox), angle
   - **Grupo "Discretización"**: n_length, n_width
   - **Grupo "Ubicación Punto Base"**: origin_x, origin_y, origin_z + botón "📍 Obtener Nodo"
   - **Grupo "Propiedad SAP2000"**: area_prop (QComboBox editable, poblada al conectar)
   - Layout: parámetros a la izquierda, preview a la derecha (QHBoxLayout)

4. **Lógica de campos dinámicos**:
   - Al cambiar tipo de perfil en el QComboBox, mostrar/ocultar campos relevantes
   - Actualizar preview automáticamente

**Testing:**
- `python gui_steel_profiles.py` abre correctamente sin SAP2000
- Cambiar tipo de perfil actualiza campos y preview
- Preview muestra sección transversal correcta para cada tipo

---

### Step 3: Integración — Ventana Principal con Tabs
**Files:** `scripts/steel_connections/gui_steel_connections.py` (NUEVO), `scripts/steel_connections/gui_bolt_plates.py` (modificación menor)

**What:**

1. **Crear `gui_steel_connections.py`:**
   - `SteelConnectionsWindow(QWidget)` con `QTabWidget`
   - Tab 1: "Placas Pernadas" → `BoltPlatesGUI` (importado)
   - Tab 2: "Perfiles de Acero" → `SteelProfilesGUI` (importado)
   - Barra de estado y título de ventana compartidos
   - Entry point standalone (`if __name__ == "__main__"`)

2. **Ajuste menor en `gui_bolt_plates.py`:**
   - Asegurar que `BoltPlatesGUI` funcione como widget embebido (ya es QWidget, compatible)
   - `SapConnection` se comparte entre tabs: exponer la conexión como parámetro opcional del constructor
   - La ventana principal gestiona la conexión y la inyecta a ambos tabs

**Testing:**
- `python gui_steel_connections.py` abre ventana con 2 tabs
- Ambos tabs funcionan independientemente
- Si se conecta en un tab, el otro puede reutilizar la conexión
