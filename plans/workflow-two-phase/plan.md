# Workflow de Dos Fases: Script Interactivo → GUI Standalone

**Branch:** `workflow-two-phase-gui`
**Description:** Reestructurar los documentos de workflow para definir un flujo de 2 fases: (1) creación interactiva de scripts con el agente y (2) generación opcional de una GUI PySide6 standalone con conexión COM directa.

## Goal

Actualmente los workflows (`quick-reference-workflow.md` y `workflow-script-creation.md`) cubren solo la creación de scripts via MCP. El usuario necesita un flujo claro de **dos fases**:

1. **Fase Script**: El usuario y el agente construyen el script interactivamente (esto ya existe, pero se debe formalizar mejor).
2. **Fase GUI**: Opcionalmente, convertir el script verificado en un mini-software standalone (`gui_*.py` + `backend_*.py`) que NO dependa del MCP — comunicación directa vía COM con `comtypes`.

El resultado final es que el usuario obtiene un software integrable en sus propias herramientas, independiente del framework de IA.

## Resumen de Implementación

| Step | Componente | Archivos Afectados | Tipo |
|------|------------|-------------------|------|
| **1** | Backend Template | `scripts/templates/backend_template.py` | NUEVO |
| **2** | GUI Template | `scripts/templates/gui_template.py` | NUEVO |
| **3** | Workflow Principal | `plans/workflow-script-creation.md` | MODIFICAR (+Fase 6) |
| **4** | Quick Reference | `plans/quick-reference-workflow.md` | MODIFICAR (+GUI section) |
| **5a** | Ring Areas GUI | `scripts/ring_areas/` (backend + gui) | NUEVO + MOVER |
| **5b** | Placabase GUI | `scripts/placabase/` (backend + gui) | NUEVO + ELIMINAR viejo |
| **6** | Skill Docs | `.github/skills/sap2000-api/SKILL.md`, `.github/copilot-instructions.md` | MODIFICAR |

**Archivos totales**: 2 templates + 2 workflows + 4 archivos GUI (2×2) + 2 skill docs + limpieza = ~10 archivos

## Contexto Actual

### Qué existe hoy
- `plans/workflow-script-creation.md` — Guía exhaustiva de 5 fases para scripts complejos
- `plans/quick-reference-workflow.md` — Referencia rápida / checklist
- `scripts/ring_areas_parametric/gui_ring_areas.py` — GUI PySide6 que **usa MCP** (importa `sap_bridge` y `sap_executor`)
- `scripts/placabase_backend.py` — Backend que recibe `sap_model` por inyección (patrón correcto, pero importa de `app_logger` y `sap_utils_common` externos)
- `scripts/example_1001_simple_beam.py` — Ejemplo limpio y legible de script (referencia de estilo)

### Qué necesita cambiar
| Aspecto | Actual | Nuevo |
|---------|--------|-------|
| Workflow docs | Solo cubren fase script | 2 fases: Script → GUI |
| GUI pattern | Depende de MCP (`sap_bridge`, `sap_executor`) | COM directo con `comtypes` — 0 dependencias de MCP |
| Estructura carpeta GUI | `ring_areas_parametric/` tiene GUI + script mezclados | `{nombre}/gui_{nombre}.py` + `backend_{nombre}.py` — separación clara |
| Backend pattern | `placabase_backend.py` importa módulos externos (`app_logger`, `sap_utils_common`) | Self-contained: solo `comtypes`, `math`, `dataclasses`, PySide6 |
| Legibilidad script | Ya existe buen patrón en `example_1001_simple_beam.py` | Formalizar como plantilla obligatoria |

## Implementation Steps

### Step 1: Crear template de backend standalone (`backend_template.py`)
**Files:** `scripts/templates/backend_template.py` (NUEVO)
**What:** Crear una plantilla base para backends standalone que:
- Conecte a SAP2000 directamente via `comtypes.client` (NO MCP)
- Tenga clase `SapConnection` con `connect()`, `disconnect()`, `is_connected`
- Tenga clase `Backend` con método `run(params) -> dict` que ejecuta la lógica del script
- Sea self-contained (sin imports de `mcp_server/`, `app_logger`, etc.)
- El método `run()` internamente replique la estructura limpia de `example_1001_simple_beam.py` (tareas numeradas, asserts, result dict)
**Testing:** Verificar que el template es sintácticamente válido (`ast.parse`). Revisar que NO importa nada de `mcp_server/`.

### Step 2: Crear template de GUI standalone (`gui_template.py`)
**Files:** `scripts/templates/gui_template.py` (NUEVO)
**What:** Crear una plantilla base para GUIs PySide6 que:
- Importe solo `PySide6`, `backend_{nombre}` (relativo), y stdlib
- Tenga 3 botones core: Conectar, Ejecutar, Desconectar
- Inputs organizados en `QGroupBox` con `QGridLayout`
- Output log (`QTextEdit` read-only, font monospace)
- Status indicator (color rojo/verde)
- Workers (`QThread` + `Signal`) para operaciones SAP2000 async
- Pattern de `_busy(True/False)` para deshabilitar botones durante ejecución
- NO importe nada de `mcp_server/`
**Testing:** Verificar sintaxis (`ast.parse`). Lanzar con `python gui_template.py` (debe abrir ventana aunque no haya SAP2000).

### Step 3: Reescribir `workflow-script-creation.md` — Fase 1 (Script Interactivo)
**Files:** `plans/workflow-script-creation.md` (MODIFICAR)
**What:** Reestructurar el documento para que la Fase 1 sea explícitamente un flujo **interactivo usuario ↔ agente**:
- **Fase 1: Planificación** → El usuario describe qué quiere lograr. El agente hace preguntas clarificadoras.
- **Fase 2: Investigación API** → El agente busca wrappers/docs (sin cambios, esto ya funciona bien).
- **Fase 3: Desarrollo Iterativo** → El agente propone código tarea por tarea. El usuario valida en SAP2000. Se itera hasta que funcione.
- **Fase 4: Integración** → Script completo, ejecutado end-to-end (sin cambios).
- **Fase 5: Entrega** → NUEVO: Script guardado. Preguntar: *"¿Quieres generar una GUI standalone para este script?"*
  - Si → Ir a **Fase 6: Generación GUI**
  - No → Fin

Agregar **Fase 6: Generación GUI Standalone**:
- 6.1: Identificar inputs del script (variables configurables al inicio)
- 6.2: Generar `backend_{nombre}.py` a partir del script:
  - Extraer lógica en método `run(params)`
  - Reemplazar `SapModel` global por `self.sap_model` inyectado
  - Reemplazar `result[]` por return dict
  - Agregar `SapConnection` class con connect/disconnect COM directo
- 6.3: Generar `gui_{nombre}.py`:
  - Un `QLineEdit` por cada input identificado en 6.1
  - Botones: Conectar / Ejecutar / Desconectar
  - Log de salida
  - Workers async
- 6.4: Crear carpeta `scripts/{nombre}/` con ambos archivos
- 6.5: Testear que la GUI abre y que el flujo completo funciona

Enfatizar regla de legibilidad: referencia = `example_1001_simple_beam.py` (task headers con `# ──`, asserts, result dict).

**Testing:** Revisar que el documento es coherente, sin secciones duplicadas, y que la transición Fase 5 → Fase 6 es clara.

### Step 4: Reescribir `quick-reference-workflow.md` — Agregar sección GUI
**Files:** `plans/quick-reference-workflow.md` (MODIFICAR)
**What:** Agregar al final una sección `## 🖥️ GUI Standalone — Quick Reference` con:
- Checklist de la Fase 6
- Estructura de carpeta esperada
- Template de `SapConnection` (connect/disconnect COM directo, snippet de 20 líneas)
- Template de `Backend.run()` (snippet de 15 líneas)
- Template de `QThread` worker (snippet de 10 líneas)
- Reglas: NO MCP, NO `sap_bridge`, NO `sap_executor`
- Naming convention: `scripts/{nombre}/gui_{nombre}.py` + `backend_{nombre}.py`
**Testing:** Verificar que los snippets son sintácticamente válidos.

### Step 5a: Migrar `ring_areas_parametric/` al nuevo patrón
**Files:** 
- `scripts/ring_areas/gui_ring_areas.py` (NUEVO) 
- `scripts/ring_areas/backend_ring_areas.py` (NUEVO)
- `scripts/example_ring_areas_parametric.py` (MOVER desde `ring_areas_parametric/` a `scripts/`)

**What:** Refactorizar al patrón standalone:
1. **Mover script MCP**: Mover `scripts/ring_areas_parametric/example_ring_areas_parametric.py` → `scripts/example_ring_areas_parametric.py` (root de scripts, fuera de carpeta GUI)
2. **Crear nueva estructura**: Carpeta `scripts/ring_areas/` (sin `_parametric` - nombre limpio)
3. **Backend standalone** `backend_ring_areas.py`:
   - `SapConnection` class con `comtypes.client` directo (no MCP)
   - `RingAreasBackend` class con `run(params) -> dict`
   - Lógica de generación de áreas anulares (copiar del script MCP, adaptar)
   - Sin imports de `sap_bridge`, `sap_executor`, `mcp_server`
4. **GUI standalone** `gui_ring_areas.py`:
   - Importar de `backend_ring_areas` (relativo `. `)
   - Workers llaman a `backend.connect()`, `backend.run()`, `backend.disconnect()`
   - Mantener UI actual (inputs r_inner/r_outer, log, botones)
5. **Eliminar carpeta vieja**: `scripts/ring_areas_parametric/` queda vacía → borrar

**Testing:** `ast.parse` ambos. Ejecutar GUI (debe abrir). Si SAP2000 disponible, flujo completo.

### Step 5b: Migrar `placabase` al nuevo patrón
**Files:**
- `scripts/placabase/gui_placabase.py` (NUEVO)
- `scripts/placabase/backend_placabase.py` (NUEVO, basado en `placabase_backend.py` actual)
- `scripts/placabase_backend.py` (ELIMINAR - obsoleto después de migración)

**What:** Convertir el backend existente en GUI standalone:
1. **Analizar `placabase_backend.py`**: Identificar todas las dependencias externas (`app_logger`, `sap_utils_common`). Ver qué funciones usa y copiarlas inline (no import externo).
2. **Backend standalone** `backend_placabase.py`:
   - `SapConnection` class (igual que ring_areas)
   - `PlateConfig` dataclass (copiar del original)
   - `PlacaBaseBackend` class (renombrar de `BasePlateBackend`)
   - Método `run(config: PlateConfig) -> dict` que ejecuta toda la lógica
   - Reemplazar `self.logger` por `print()` o logging interno
   - Eliminar `app_logger`, `sap_utils_common` imports (copiar `check_ret_code` inline si necesario)
3. **GUI nueva** `gui_placabase.py`:
   - Inputs para `PlateConfig`: bolt_dia, H_col, B_col, n_pernos, plate_thickness, etc.
   - Sección "Centros de Pernos" (tabla o lista editable, opcional — sino auto-generar)
   - Checkbox "Include Anchor Chair"
   - Input ks_balasto (spring constant)
   - Workers + status + log (patrón estándar)
4. **Limpiar**: Eliminar `scripts/placabase_backend.py` obsoleto

**Testing:** `ast.parse` ambos. GUI abre. Si inputs complejos (bolt_centers), comenzar con auto-generación (usuario puede dejar vacío).

### Step 6: Actualizar SKILL.md y copilot-instructions.md
**Files:** `.github/skills/sap2000-api/SKILL.md` (MODIFICAR), `.github/copilot-instructions.md` (MODIFICAR)
**What:**
- En `SKILL.md`: Agregar paso 10 al workflow: *"Ofrecer generar GUI standalone"*. Documentar la estructura `scripts/{nombre}/gui_*.py + backend_*.py`. Referenciar templates.
- En `copilot-instructions.md`: Mencionar que el agente puede generar GUIs standalone y apuntar al workflow actualizado.
**Testing:** Leer ambos archivos y verificar coherencia con los workflows actualizados.

## Estructura Final Esperada

```
scripts/
  templates/                          # NUEVO
    backend_template.py               # Plantilla backend COM directo
    gui_template.py                   # Plantilla GUI PySide6
  
  ring_areas/                         # NUEVO (renombrado, carpeta limpia)
    gui_ring_areas.py                 # MODIFICADO - sin MCP
    backend_ring_areas.py             # NUEVO - COM directo
  
  placabase/                          # NUEVO
    gui_placabase.py                  # NUEVO
    backend_placabase.py              # NUEVO - sin app_logger externo
  
  example_ring_areas_parametric.py    # MOVIDO (estaba en ring_areas_parametric/)
  example_1001_simple_beam.py         # Sin cambios (referencia de estilo)
  example_placabase_parametric.py     # Sin cambios (si existe)
  
  # ELIMINADOS:
  # ring_areas_parametric/ (carpeta vieja)
  # placabase_backend.py (archivo suelto reemplazado por placabase/)

plans/
  workflow-script-creation.md         # MODIFICADO - 6 fases
  quick-reference-workflow.md         # MODIFICADO - sección GUI
  workflow-two-phase/
    plan.md                           # Este plan
```

**Convención de naming final**:
- Scripts MCP verificados: `scripts/example_*.py` (root)
- GUIs standalone: `scripts/{nombre}/gui_{nombre}.py + backend_{nombre}.py`
- Templates: `scripts/templates/*.py`
- Wrappers: `scripts/wrappers/func_*.py` (sin cambios)

## Decisiones de Diseño

### ¿Por qué COM directo y no MCP?
El MCP bridge es excelente para desarrollo interactivo con IA (sandbox, seguridad, auto-registro). Pero el producto final que el usuario entrega a terceros no necesita IA — necesita ser simple, autónomo y sin dependencias extra. `comtypes` es la librería estándar para COM en Python.

### ¿Por qué 2 archivos (gui + backend) y no uno solo?
- **Separación de concerns**: La GUI no necesita saber de SAP2000 API. El backend no necesita saber de PySide6.
- **Testabilidad**: El backend se puede probar sin GUI (`python -c "from backend_x import ..."`).
- **Reusabilidad**: El backend se puede integrar en otro software sin la GUI.

### ¿Por qué no un tercer archivo `connection.py`?
Para mantener las cosas simples. La clase `SapConnection` vive dentro de `backend_*.py`. Si el proyecto crece, el usuario puede extraerla. No sobrediseñar.

### Estilo de script: ¿por qué `example_1001_simple_beam.py` como referencia?
- Headers claros con `# ── Task N: Nombre ──`
- Cada llamada API tiene `assert ret == 0`
- Variables configurables al inicio, separadas visualmente
- Resultado en dict (`result[]`)
- Fórmulas de referencia en comentarios
- Sin funciones auxiliares innecesarias para scripts simples

## Decisiones Finales (Usuario Confirmó)

1. ✅ **Migrar `placabase_backend.py` también** — Crear `scripts/placabase/backend_placabase.py` + `gui_placabase.py`. Cada GUI en su propia carpeta para mantener orden.

2. ✅ **Mover `example_ring_areas_parametric.py` fuera** — Carpetas GUI deben ser limpias: solo `gui_*.py` + `backend_*.py`. Scripts MCP van en `scripts/` root.

3. ✅ **Templates como archivos reales** — `scripts/templates/backend_template.py` y `gui_template.py` como archivos ejecutables. Beneficios: el agente puede `read_file`, validar con `ast.parse`, y copiar directamente. Más fácil de mantener que bloques de código en .md.
