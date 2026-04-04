# Blockly Visual Scripter — Profesionalización

**Branch:** `feat/blockly-pro`
**Description:** Transformar el prototipo Blockly en un editor visual completo con bloques paramétricos, generación de código robusta, y UX profesional.

## Goal

El prototipo actual tiene ~106 bloques definidos pero **ninguno tiene campos editables** (`args0: []`), sólo 3 generadores de código implementados, y el toolbox está vacío. El objetivo es convertirlo en una herramienta funcional que cubra las 144 funciones verificadas del registry, con inputs paramétricos, generación de Python correcta, y una GUI pulida.

## Diagnóstico Actual

| Problema | Impacto |
|----------|---------|
| `args0: []` en todos los bloques | Usuarios no pueden ingresar coordenadas, nombres, valores |
| Solo 3 generadores en `generators.js` | 100+ bloques fallan al generar código |
| Toolbox XML vacío (sin `<block>`) | No aparecen bloques en el editor |
| UTF-8 corrupto ("Geometr╝a") | Caracteres rotos en categorías |
| `_on_open_project()` no recarga bloques visualmente | Abrir proyecto no restaura workspace |
| WebChannel muerto en `index.html` | Código muerto, confuso |
| Sin atajos de teclado | UX pobre |
| Transpiler hardcodeado (3 casos) | No escala a 144 funciones |
| Sin validación de inputs | Valores inválidos pasan silenciosamente |

## Implementation Steps

---

### Step 1: Reescribir `blockly_generator.py` — Motor de generación con parámetros
**Files:** `scripts/blockly_generator.py`, `scripts/registry.json`
**What:** Reescribir el generador para que extraiga parámetros reales de cada función del registry (`parameter_notes`, `signature`, `notes`) y produzca:
- **`block_definitions.js`** con `args0` poblados (fields de texto, dropdowns para enums, números).
- **`generators.js`** con generadores Python para CADA bloque, usando el patrón `raw = SapModel.X.Y(...); ret_code = raw[-1]`.
- **`toolbox_structure.xml`** con bloques listados dentro de cada categoría, encoding UTF-8 correcto.

Para cada función del registry:
1. Parsear `parameter_notes` / `signature` para extraer nombre y tipo de cada parámetro.
2. Mapear tipos a Blockly fields: `str` → `field_input`, `float/int` → `field_number`, enums (eMatType, eUnits) → `field_dropdown`.
3. Generar el generador Python que interpola los valores del bloque en la llamada API correcta.
4. Incluir handling de ByRef basado en `notes` del registry (ej: "Returns [Name, ret_code]").

**Testing:**
```bash
python scripts/blockly_generator.py scripts/registry.json scripts/blockly
```
- Verificar que `block_definitions.js` tiene `args0` con campos para al menos 140 bloques.
- Verificar que `generators.js` tiene un generador para cada bloque.
- Verificar que `toolbox_structure.xml` lista bloques dentro de categorías.
- Verificar encoding UTF-8 correcto (Geometría, Análisis, etc.).
- Abrir `index.html` en browser y confirmar que los bloques aparecen con campos editables.

---

### Step 2: Reescribir `blockly_transpiler.py` — Transpilación data-driven
**Files:** `scripts/blockly_transpiler.py`
**What:** Reemplazar los `if/elif` hardcodeados por un sistema data-driven que:
1. Lea el block type del XML.
2. Extraiga los valores de los fields.
3. Use un mapa `BLOCK_TYPE → template` (auto-generado o derivado del registry) para producir el código Python.
4. Mantenga la validación de fases pero como **warning** en vez de error (permitir orden flexible).
5. Soporte correctamente el patrón ByRef para cada función según metadata del registry.

El transpiler debe ser capaz de generar código correcto para CUALQUIER bloque del registry sin agregar código manual por cada función nueva.

**Testing:**
- Unit test: XML con 5+ bloques de diferentes fases → Python output correcto.
- Verificar que el código generado sigue el patrón: `raw = SapModel.X.Y(...); ret = raw[-1]; assert ret == 0`.
- Verificar manejo de ByRef (funciones que retornan Name, lists, etc.).
- Verificar que fases desordenadas generan warning pero no error.

---

### Step 3: Mejorar `index.html` — Editor Blockly profesional
**Files:** `scripts/blockly/index.html`
**What:**
1. **Limpiar WebChannel muerto** — eliminar código no usado.
2. **Implementar `pyQtLoadXml(xml)`** — función JS que restaura workspace desde XML (para Open Project).
3. **Mejorar UI del workspace:**
   - Zoom controls visibles.
   - Trash can habilitado.
   - Grid / snap configuración.
   - Theme profesional (dark mode opcional).
4. **Exponer API JS limpia:**
   - `window.getWorkspaceXml()` → retorna XML actual.
   - `window.loadWorkspaceXml(xml)` → carga XML en workspace.
   - `window.generatePython()` → retorna Python generado por Blockly.
   - `window.clearWorkspace()` → limpia workspace.
5. **Toolbox mejorado:**
   - Search box en toolbox (Blockly built-in o custom).
   - Colapsable categories con iconos.
6. **Validación visual:**
   - Bloques desconectados → borde rojo.
   - Bloques con campos vacíos → highlight amarillo.

**Testing:**
- Abrir en browser standalone, verificar que todos los bloques aparecen.
- Drag & drop bloques, verificar campos editables.
- Usar `generatePython()` desde consola JS y verificar output.
- Probar `loadWorkspaceXml()` con XML guardado.

---

### Step 4: Mejorar `blockly_gui.py` — GUI PySide6 profesional
**Files:** `scripts/blockly_gui.py`
**What:**
1. **Arreglar Open Project** — llamar `window.loadWorkspaceXml(xml)` vía `page().runJavaScript()`.
2. **Keyboard shortcuts:** Ctrl+S (save), Ctrl+E (export), Ctrl+R (run), Ctrl+N (new).
3. **Recent projects** — lista de últimos 5 `.blockly` files en menú.
4. **Mejorar layout:**
   - Toolbar superior con iconos (Run ▶, Save 💾, Export 📄, Open 📂).
   - Panel derecho colapsable con tabs: "Python Preview" | "Console".
   - Statusbar con: conexión SAP2000 (🟢/🔴), último guardado, conteo de bloques.
5. **Preview mejorado:**
   - Syntax highlighting en Python preview (QSyntaxHighlighter básico).
   - Usar JS `generatePython()` además del transpiler Python (comparar outputs).
6. **Comunicación mejorada:**
   - Reemplazar polling de 300ms por `QWebChannel` funcional, o al menos optimizar polling.
   - Callback desde JS cuando workspace cambia (`workspace.addChangeListener`).
7. **Export mejorado:**
   - Exportar con header que incluye metadata (fecha, versión, descripción).
   - Opción de exportar como script standalone (con `SapConnection` incluido).

**Testing:**
- Open project → bloques se restauran visualmente.
- Ctrl+S guarda, Ctrl+R ejecuta.
- Panel colapsable funciona.
- Python preview se actualiza en tiempo real.

---

### Step 5: Bloques compuestos y workflows
**Files:** `scripts/blockly_generator.py`, `scripts/blockly/block_definitions.js`
**What:** Agregar bloques de alto nivel que encapsulan patrones comunes:
1. **"Crear Viga Simple"** — Combo: material + sección + frame + apoyos + carga.
2. **"Crear Pórtico NxM"** — Grid de columnas y vigas con parámetros.
3. **"Loop/Repetir"** — Bloque for-loop para crear geometría paramétrica.
4. **"Variable"** — Definir y usar variables (coordenadas, dimensiones).
5. **"Ejecutar Análisis Completo"** — DOF + run + setup resultados.
6. **"Extraer Resultados"** — Template para joint/frame/area results.

Estos bloques se agregan como categoría "Workflows" adicional en el toolbox y generan secuencias de llamadas API correctas.

**Testing:**
- Bloque "Crear Viga Simple" → genera script funcional idéntico a `example_1001_simple_beam.py`.
- Bloque "Loop" con `FrameObj.AddByCoord` → genera N frames correctamente.
- Ejecutar script generado contra SAP2000 exitosamente.

---

### Step 6: Testing, documentación y polish
**Files:** `scripts/blockly/README.md`, `scripts/blockly_gui.py`, `scripts/blockly_transpiler.py`
**What:**
1. **Tests unitarios:**
   - `test_transpiler.py`: XML → Python para cada categoría de bloque.
   - `test_generator.py`: Registry → JS/XML generation correcta.
2. **README actualizado:**
   - Screenshots del editor.
   - Quick start guide.
   - Lista de bloques disponibles por categoría.
   - Guía para agregar bloques nuevos.
3. **Error handling robusto:**
   - Timeout real en executor (threading).
   - Mensajes de error claros en consola GUI.
   - Validación de conexión SAP2000 antes de ejecutar.
4. **Polish UI:**
   - Splash/loading screen mientras carga Blockly.
   - Confirmación antes de cerrar con cambios sin guardar.
   - Iconos SVG en toolbar.

**Testing:**
- Correr test suite completa.
- Workflow end-to-end: abrir GUI → armar modelo → ejecutar → ver resultados.
- Abrir/guardar proyectos correctamente.

---

## Prioridad y Dependencias

```
Step 1 (Generator) ──→ Step 2 (Transpiler) ──→ Step 5 (Workflows)
       │                      │
       └──→ Step 3 (HTML) ────┤
                              └──→ Step 4 (GUI) ──→ Step 6 (Tests/Docs)
```

**Steps 1-2** son blockers — sin bloques con parámetros y generación correcta, el resto no tiene sentido.
**Step 3** puede avanzar en paralelo parcialmente (cleanup HTML).
**Steps 4-6** dependen de que los bloques funcionen.

## Notas Técnicas

- **Fuente de verdad para firmas:** `scripts/wrappers/` + `scripts/registry.json`
- **Patrón ByRef universal:** `raw = SapModel.X.Y(...); ret = raw[-1]`
- **Enums clave:** `eMatType` (1=Steel,2=Concrete,3=NoDesign...), `eUnits` (6=kN_m_C), `eLoadPatternType`
- **Banderas de riesgo:** Nunca generar `exec()` desde input del usuario sin sanitizar
