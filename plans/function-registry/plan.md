# Function Registry — Registro de Funciones Verificadas de la API SAP2000

**Branch:** `feature/function-registry`
**Description:** Sistema de registro que cataloga funciones de la API SAP2000 verificadas, envueltas en scripts documentados, para facilitar su reutilización por el agente.

## Goal

Crear un sistema de registro (registry) que permita al agente saber qué funciones de la API de SAP2000 han sido verificadas exitosamente, en qué scripts se usan, y con qué parámetros han sido probadas. Cada función verificada se envuelve en un script-plantilla documentado que sirve como referencia y punto de partida para el agente.

## Contexto Actual

- Los scripts se guardan en `scripts/` con metadatos básicos (nombre, descripción, fecha, estado, tags)
- No existe un catálogo de funciones individuales de la API verificadas
- No hay trazabilidad de qué funciones se usan en cada script
- El agente debe buscar en la documentación y generated scripts desde cero cada vez
- Existen ~23 categorías de API documentadas en `API/*.md` con cientos de funciones

## Implementation Steps

### Step 1: Modelo de datos y módulo del registro (`function_registry.py`)

**Files:**
- `mcp_server/function_registry.py` (nuevo)
- `scripts/registry.json` (nuevo — archivo de datos)

**What:**
Crear el módulo `function_registry.py` con la clase `FunctionRegistry` que gestione un archivo JSON (`scripts/registry.json`) con la siguiente estructura:

```json
{
  "version": "1.0",
  "functions": {
    "SapModel.FrameObj.AddByCoord": {
      "category": "Object_Model",
      "description": "Agrega un frame por coordenadas",
      "signature": "Function AddByCoord(ByVal x1 As Double, ...)",
      "verified": true,
      "first_verified": "2026-03-20T00:00:00Z",
      "last_verified": "2026-03-20T00:00:00Z",
      "verification_count": 3,
      "wrapper_script": "func_FrameObj_AddByCoord",
      "used_in_scripts": ["simple_beam", "example_1001"],
      "parameter_notes": "x1,y1,z1,x2,y2,z2=coords; Name=optional; PropName=section; UserName=optional",
      "known_errors": [],
      "notes": "ByRef: raw[0]=Name asignado, raw[-1]=ret_code"
    }
  },
  "summary": {
    "total_registered": 1,
    "total_verified": 1,
    "last_updated": "2026-03-20T00:00:00Z"
  }
}
```

Operaciones del módulo:
- `register_function(function_path, category, description, ...)` — registrar una función nueva o actualizar existente
- `mark_verified(function_path, script_name)` — marcar como verificada, vincular a script
- `get_function(function_path)` — obtener detalle de una función
- `list_functions(category, verified_only, query)` — listar/buscar funciones con filtros
- `get_summary()` — resumen de cobertura (total, verificadas, porcentaje)
- `_save() / _load()` — persistencia atómica del JSON

**Testing:** Crear `mcp_server/tests/test_function_registry.py` con tests unitarios para cada operación CRUD. Ejecutar con `pytest`.

---

### Step 2: Template de wrapper-scripts para funciones individuales

**Files:**
- `scripts/wrappers/` (nuevo directorio)
- `scripts/wrappers/README.md` (nuevo)
- 2-3 wrapper-scripts de ejemplo (nuevos)

**What:**
Definir un formato estándar de "wrapper script" — un script minimalista que demuestra el uso correcto de una función individual de la API. Convención:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.AddByCoord
# Category: Object_Model
# Description: Agrega un elemento frame definido por coordenadas
# Verified: 2026-03-20
# Prerequisites: Modelo abierto, material y sección definidos
# ============================================================
"""
Uso: Crea un frame (viga/columna) entre dos puntos dados por coordenadas.
     Retorna el nombre asignado al frame.

API Signature:
  SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName, UserName, CSys)

ByRef Output:
  raw[0] = Name (nombre asignado por SAP2000)
  raw[-1] = ret_code (0=éxito)

Parámetros:
  x1,y1,z1 : float — Coordenadas del punto i [L]
  x2,y2,z2 : float — Coordenadas del punto j [L]
  Name     : str   — Nombre (vacío="auto")
  PropName : str   — Nombre de la sección de frame
  UserName : str   — Nombre de usuario (vacío=usa Name)
  CSys     : str   — Sistema de coordenadas (default="Global")
"""

# --- Setup mínimo requerido (modelo nuevo) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisitos: material y sección ---
MATERIAL_NAME = "MAT_TEST"
ret = SapModel.PropMaterial.SetMaterial(MATERIAL_NAME, 2)  # 2=Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

SECTION_NAME = "SEC_TEST"
ret = SapModel.PropFrame.SetRectangle(SECTION_NAME, MATERIAL_NAME, 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# --- Función principal ---
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", SECTION_NAME, "")
frame_name = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"AddByCoord failed: {ret_code}"

# --- Verificación ---
count = SapModel.FrameObj.Count()
assert count >= 1, f"Expected at least 1 frame, got {count}"

# --- Resultado ---
result["function"] = "SapModel.FrameObj.AddByCoord"
result["frame_name"] = frame_name
result["frame_count"] = count
result["status"] = "verified"
```

Crear wrappers iniciales para funciones ya probadas en los ejemplos existentes:
1. `func_FrameObj_AddByCoord.py`
2. `func_PointObj_SetRestraint.py`
3. `func_LoadPatterns_Add.py`

**Testing:** Ejecutar cada wrapper en SAP2000 vía `run_sap_script` y verificar que `result["status"] == "verified"`.

---

### Step 3: Herramientas MCP para el registro

**Files:**
- `mcp_server/server.py` (modificar — agregar 3 tools)
- `mcp_server/function_registry.py` (importar en server)

**What:**
Agregar 3 herramientas MCP al servidor:

1. **`query_function_registry(function_path?, category?, verified_only?, query?)`**
   - Sin argumentos: retorna resumen de cobertura
   - Con `function_path`: retorna detalle de esa función
   - Con `category` / `query`: lista funciones filtradas
   - Con `verified_only=True`: solo funciones verificadas

2. **`register_verified_function(function_path, category, description, wrapper_script?, parameter_notes?, notes?)`**
   - Registra o actualiza una función en el registry
   - Si se proporciona `wrapper_script`, vincula al script wrapper

3. **`list_registry_categories()`**
   - Lista categorías con conteo de funciones registradas vs documentadas
   - Formato: `[{category, registered, verified, documented_estimate}]`

**Testing:** Llamar cada tool desde MCP y verificar respuestas.

---

### Step 4: Auto-registro al ejecutar scripts

**Files:**
- `mcp_server/sap_executor.py` (modificar — agregar extracción de funciones)
- `mcp_server/function_registry.py` (importar en executor)

**What:**
Modificar `run_script()` en `sap_executor.py` para que, al ejecutar un script exitosamente:

1. Extraer funciones API llamadas mediante análisis del código fuente (regex sobre `SapModel.X.Y(` y `SapObject.X.Y(`)
2. Registrar automáticamente cada función detectada como `verified` en el registry
3. Vincular el script que las usó (si se guardó con `save_as`)

Esto asegura que el registry crece automáticamente conforme se ejecutan scripts exitosos.

**Testing:**
- Ejecutar `simple_beam.py` vía `run_sap_script`
- Verificar que las funciones usadas aparecen en `registry.json` con `verified: true`
- Verificar que el script queda vinculado a cada función

---

### Step 5: Actualizar SKILL.md y documentación

**Files:**
- `.github/skills/sap2000-api/SKILL.md` (modificar)
- `scripts/wrappers/README.md` (ya creado en Step 2)
- `scripts/README.md` (modificar)

**What:**
Actualizar el SKILL.md para que el workflow del agente incluya:

1. **Nuevo paso en el workflow:** Antes de generar un script, consultar `query_function_registry` para ver si la función ya fue verificada y tiene un wrapper disponible
2. **Nuevo paso post-ejecución:** Después de verificar un script exitoso, usar `register_verified_function` para funciones nuevas que no estén en el registry
3. **Convención de wrappers:** Documentar el formato estándar de wrapper-scripts
4. Actualizar la tabla de herramientas MCP disponibles con las 3 nuevas

**Testing:** Verificar que el agente sigue el workflow actualizado al procesar una tarea de SAP2000.

---

## Diagrama de flujo actualizado

```
Copilot Agent
    ↓
SKILL.md (workflow actualizado)
    ↓
query_function_registry  ← registry.json
    ↓ (si la función ya está verificada)
load_script(wrapper)     ← scripts/wrappers/
    ↓ (adaptar wrapper al caso)
run_sap_script           → SAP2000 via COM
    ↓ (éxito)
auto-registro            → registry.json (actualizado)
    ↓
save_as                  → scripts/ (si aplica)
```

## Notas

- El registry es un JSON plano por simplicidad — no requiere base de datos
- Los wrappers viven en `scripts/wrappers/` separados de scripts de usuario
- El auto-registro en Step 4 es opt-in: solo funciones de scripts exitosos
- El formato de wrappers está diseñado para ser ejecutable directamente vía `run_sap_script`
