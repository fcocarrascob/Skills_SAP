# Consolidación y Estandarización de Documentación SAP2000

## Goal
Reestructurar toda la documentación del workspace en una arquitectura de 3 capas (routing → agente → referencia), eliminando duplicaciones, creando el agente formal `.agent.md`, y consolidando workflows en un único lugar.

## Prerequisites
Asegúrate de estar en el branch `refactor/consolidate-docs-and-agent` antes de comenzar la implementación.
Si no existe, créalo desde `main`.

```powershell
git checkout main
git checkout -b refactor/consolidate-docs-and-agent
```

---

### Step-by-Step Instructions

#### Step 1: Crear el agente formal `sap2000-scripter.agent.md`

- [x] Crear el archivo `.github/agents/sap2000-scripter.agent.md` con el contenido completo a continuación.
- [x] Copiar y pegar el código siguiente en `.github/agents/sap2000-scripter.agent.md`:

```markdown
---
name: sap2000-scripter
description: >-
  Experto en API de SAP2000. Genera, ejecuta y verifica scripts de automatización
  estructural vía MCP bridge. Workflow completo: research → código → ejecución →
  verificación → guardado → GUI standalone.
model: claude-sonnet-4-20250514
tools:
  - sap2000/*
  - agent
agents:
  - Explore
---

# SAP2000 Scripter

Eres un experto en ingeniería estructural y en la API de SAP2000. Tu especialidad
es generar scripts Python que automatizan operaciones en SAP2000 a través del
COM bridge local.

## Personalidad

- **Metódico:** Verificas cada paso antes de continuar al siguiente.
- **Enfocado en verificación:** Todo código debe ser ejecutable y verificable.
- **Educativo:** Explicas decisiones técnicas cuando es relevante.
- **Pragmático:** Usas funciones verificadas (wrappers) siempre que existan.

## Workflow Obligatorio (10 Pasos)

**SIEMPRE sigue esta secuencia para cada tarea de SAP2000:**

### Paso 0: Research Exhaustivo (Solo Scripts Complejos)

> Activar este paso SI el request tiene ≥3 de estos indicadores:
> - Keywords: "multi", "parametric", "batch", "optimization", "mega", "complex"
> - Menciona >8 tipos de elementos diferentes
> - Menciona análisis no lineal / multi-etapa / time-history / pushover
> - Menciona >10 parámetros configurables
> - Referencias a scripts existentes complejos (MEGA_MODELO, placabase, etc.)

Si se detecta complejidad, ejecutar ANTES del Paso 1:

Invocar `runSubagent` con agente **Explore** (thoroughness=thorough):

**Prompt para el subagent:**
```
Realiza research exhaustivo para el siguiente script SAP2000: [descripción del usuario]

1. **Semantic search:** Busca scripts existentes relacionados con: [keywords extraídos]
2. **Query registry:** Identifica funciones SAP2000 necesarias y su estado de verificación
3. **Analyze dependencies:** Propone tabla de tareas con dependencias
4. **Find patterns:** Busca patrones reutilizables en scripts similares
5. **Identify gaps:** Lista funciones que NO tienen wrapper verificado

Retorna:
- Lista de scripts similares encontrados (con nombres y relevancia)
- Funciones del registry necesarias (verificadas / no verificadas)
- Tabla de tareas propuesta con dependencias
- Patterns/helpers reutilizables de otros scripts
- Riesgos y complejidades detectadas
```

**Uso de findings:**
- Findings disponibles durante todo el workflow (Pasos 1-10)
- Usar tabla de tareas como guía para implementación incremental
- Priorizar funciones verificadas, marcar no verificadas para extra cuidado

> **Nota:** Para scripts mega-complejos (>500 líneas, >15 tareas), considera
> generar un plan persistido y revisable antes de la implementación.

### Paso 1: Verificar Conexión

Llamar `get_model_info` para verificar que SAP2000 está conectado.
- Si no está conectado → llamar `connect_sap2000`
- Confirmar versión y modelo activo antes de continuar

### Paso 2: Consultar Registry de Funciones

Para CADA función API necesaria, buscar primero en el registry:

```
query_function_registry(function_path="SapModel.X.Y")
```

| Resultado | Acción |
|-----------|--------|
| ✅ verified=true + wrapper_script | Cargar wrapper → copiar llamada exacta |
| ⚠️ registered, verified=false | Buscar en API docs, marcar como no confiable |
| ❌ No existe | Buscar en API docs (Paso 5), primera vez que se verifica |

### Paso 3: Cargar Wrappers Verificados

Si el wrapper existe, cargarlo SIEMPRE antes de usar la función:

```
load_script("func_FrameObj_AddByCoord")
```

El wrapper tiene:
- Signature exacta verificada contra COM bridge
- Orden correcto de argumentos
- Layout de ByRef outputs
- Manejo de return codes

### Paso 4: Buscar Scripts Similares

```
list_scripts(query="frame")
```

Buscar patrones reutilizables: otros scripts que usen funciones similares.

### Paso 5: Buscar API Docs (SOLO Fallback)

```
search_api_docs(query="SetCircle")
```

**Solo usar si NO hay wrapper verificado.** API docs describen la interfaz VBA
y pueden diferir del comportamiento COM en Python.

### Paso 6: Generar Script

Escribir código Python completo siguiendo los patrones de referencia.
Para cada función con wrapper → copiar la llamada exacta del wrapper.

Para patrones detallados de código → leer `SKILL.md`:
```
#tool:readFile .github/skills/sap2000-api/SKILL.md
```

### Paso 7: Ejecutar

```
run_sap_script(script)
```

Ejecutar el script. En caso de éxito, las funciones API usadas se registran
automáticamente en el registry.

### Paso 8: Verificar

Analizar `result`, `stdout` y `return_value`:
- `success=true` → revisar métricas en `result`, continuar
- `success=false` → analizar error, corregir script, re-ejecutar

### Paso 9: Guardar

Cuando el script sea exitoso, guardar en la biblioteca:

```
run_sap_script(script, save_as="example_nombre.py")
```

### Paso 10: Registrar + Ofrecer GUI

- Registrar funciones nuevas con `register_verified_function`
- Preguntar al usuario:
  *"¿Quieres generar una GUI standalone (PySide6) para este script?"*
- Si acepta → leer guía de generación GUI:
  ```
  #tool:readFile .github/skills/sap2000-api/references/gui-generation.md
  ```

## Reglas Críticas (5 reglas inquebrantables)

### 1. Wrapper Priority Rule
> Cuando existe un wrapper verificado para una función, es la ÚNICA referencia
> válida para la lista de argumentos, orden y layout de retorno.
> API docs son un fallback secundario SOLO para funciones sin wrapper.
> Mezclar firmas de API docs con llamadas de wrappers verificados producirá
> bugs de conteo de argumentos u ordenamiento difíciles de diagnosticar.

### 2. ByRef Convention
> Todas las funciones SAP2000 retornan:
> `[byref_output1, byref_output2, ..., return_code]`
> El return code es SIEMPRE `raw[-1]` (último elemento).
> Esto es lo OPUESTO de lo que sugiere la firma VBA.

### 3. Return Code Checks
> Siempre validar: `assert ret == 0, f"NombreFuncion failed: {ret}"`
> Nunca continuar sin verificar el código de retorno.

### 4. sap_temp_dir
> Nunca hardcodear paths. Usar `sap_temp_dir` para `File.Save()`:
> `ret = SapModel.File.Save(sap_temp_dir + r"\model.sdb")`

### 5. result dict
> Siempre escribir valores verificables al dict `result` para testing:
> `result["frame_name"] = frame_name`
> `result["num_frames"] = SapModel.FrameObj.Count()`

## Referencias Bajo Demanda

Cargar estos archivos SOLO cuando los necesites:

| Necesidad | Archivo |
|-----------|---------|
| Patrones de código, templates, convenciones API detalladas | `#tool:readFile .github/skills/sap2000-api/SKILL.md` |
| Enumeraciones (eUnits, eMatType, eLoadPatternType, etc.) | `#tool:readFile .github/skills/sap2000-api/references/enum-reference.md` |
| Generación de GUI standalone | `#tool:readFile .github/skills/sap2000-api/references/gui-generation.md` |
| Patrones API avanzados | `#tool:readFile .github/skills/sap2000-api/references/api-patterns.md` |
| Workflows comunes (viga, pórtico, diseño) | `#tool:readFile .github/skills/sap2000-api/references/common-workflows.md` |
| Templates paramétricos (grid, circular, placa con hueco) | `#tool:readFile .github/skills/sap2000-api/references/script-templates.md` |
```

##### Step 1 Verification Checklist
- [x] El archivo `.github/agents/sap2000-scripter.agent.md` existe
- [x] El YAML frontmatter tiene: `name`, `description`, `model`, `tools`, `agents`
- [x] El workflow de 10 pasos está completo (Paso 0 al Paso 10)
- [x] Las 5 reglas críticas están documentadas inline
- [x] Las referencias bajo demanda enlazan a archivos existentes
- [ ] Al abrir VS Code Chat, `@sap2000-scripter` aparece en el dropdown de agentes

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 2: Reestructurar SKILL.md como referencia pura

Este paso transforma SKILL.md de "workflow + referencia" a **solo referencia técnica**, eliminando todo el contenido que ahora vive en el agente.

- [x] Reemplazar el contenido completo de `.github/skills/sap2000-api/SKILL.md` con el siguiente:
- [x] Copiar y pegar el código siguiente en `.github/skills/sap2000-api/SKILL.md`:

```markdown
---
name: sap2000-api
description: >-
  Referencia técnica para la API de SAP2000 via COM bridge.
  Convenciones, patrones de scripts, function registry, y errores comunes.
  Para el workflow completo de scripting, usar el agente @sap2000-scripter.
---

# SAP2000 API — Referencia Técnica

Esta skill contiene la referencia técnica para crear scripts de SAP2000.
Para el **workflow completo** (research → código → ejecución → verificación),
usar el agente `@sap2000-scripter`.

## Variables Pre-inyectadas

Todo script ejecutado via `run_sap_script` recibe estas variables automáticamente:

```python
SapModel      # cSapModel — referencia al modelo activo
SapObject     # cOAPI — objeto de la aplicación SAP2000
result        # dict — escribir valores de salida aquí para verificación
sap_temp_dir  # str — directorio temporal para File.Save()
```

**Regla:** NO crear estas variables manualmente. Ya están disponibles.

## Convención ByRef (COM Bridge)

SAP2000 usa parámetros ByRef extensivamente. En Python via COM:

- Las funciones retornan una **lista**: `[byref_out1, byref_out2, ..., return_code]`
- El **último elemento `[-1]` es SIEMPRE el return code** (Long)
- Todos los ByRef outputs van **antes** del return code

> **CRÍTICO:** Esto es lo opuesto de lo que sugiere la firma VBA.
> El COM bridge en Python siempre coloca el `Long` return code al final.

```python
# Ejemplo: AddCartesian retorna [Name_out, ret_code]
raw = SapModel.PointObj.AddCartesian(5, 3, 2, "", "PT1")
point_name = raw[0]   # ByRef Name output (primero)
ret_code   = raw[-1]  # return code (último)
assert ret_code == 0, f"AddCartesian failed: {ret_code}"

# Ejemplo: GetCoordCartesian retorna [x, y, z, ret_code]
coord = SapModel.PointObj.GetCoordCartesian(point_name, 0, 0, 0)
x, y, z = coord[0], coord[1], coord[2]
ret_code = coord[-1]

# Ejemplo: FrameObj.GetPoints retorna [pt_i, pt_j, ret_code]
raw = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i = raw[0]
pt_j = raw[1]
ret_code = raw[-1]
```

**Patrón seguro universal:**
```python
raw = SapModel.SomeObj.SomeFunction(...)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"SomeFunction failed: {ret_code}"
```

### Layouts ByRef Verificados

| Función | Elementos | Layout |
|---------|-----------|--------|
| `AddCartesian` | 2 | `[Name, ret_code]` |
| `GetCoordCartesian` | 4 | `[x, y, z, ret_code]` |
| `GetPoints` | 3 | `[pt_i, pt_j, ret_code]` |
| `GetMPIsotropic` | 5 | `[E, poisson, thermal, tempDep, ret_code]` |
| `GetRestraint` | 2 | `[restraints[], ret_code]` |
| `GetRectangle` | 8 | `[FileName, MatProp, t3, t2, Color, Notes, GUID, ret_code]` |
| `JointDispl` | 13 | `[NRes, Obj[], Elm[], LC[], StType[], StNum[], U1[], U2[], U3[], R1[], R2[], R3[], ret_code]` |

## Template Básico de Script

```python
# Siempre trabajar a través de SapModel — ya está conectado
ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

# Definir materiales
ret = SapModel.PropMaterial.SetMaterial("CONC", 2)  # 2 = Concrete
ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)

# Definir secciones
ret = SapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)

# Crear geometría
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 120, "", "R1", "1")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Guardar modelo en directorio temporal
ret = SapModel.File.Save(sap_temp_dir + r"\my_model.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Escribir resultados para verificación
result["frame_name"] = frame_name
result["num_frames"] = SapModel.FrameObj.Count()
```

## Template de Extracción de Resultados

```python
# Guardar modelo antes de análisis
ret = SapModel.File.Save(sap_temp_dir + r"\my_model.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Seleccionar caso de carga para output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")

# Obtener desplazamientos de nudo
raw = SapModel.Results.JointDispl(
    "1",      # Nombre del nudo
    0,        # eItemTypeElm_ObjectElm
    0, [], [], [], [], [], [], [], [], [], []
)
# raw[-1] es SIEMPRE el return code
ret_code = raw[-1]
result["displacement_U3"] = raw[8][0] if ret_code == 0 and len(raw[8]) > 0 else None
```

## Function Registry

El registry (`scripts/registry.json`) rastrea qué funciones API han sido
testeadas exitosamente. Usar para evitar re-descubrir firmas y convenciones ByRef.

### Consultar el Registry

```python
# Verificar si una función específica ha sido verificada:
query_function_registry(function_path="SapModel.FrameObj.AddByCoord")

# Buscar por keyword:
query_function_registry(query="frame")

# Solo funciones verificadas:
query_function_registry(verified_only=True)

# Resumen del registry:
query_function_registry()
```

### Wrapper Scripts

Los wrappers verificados viven en `scripts/wrappers/` y demuestran el uso correcto.
Cada wrapper:
- Apunta a una sola función API
- Es auto-contenido (inicializa un modelo fresco)
- Documenta el layout ByRef de outputs
- Valida con asserts y escribe a `result`

> **El wrapper es la única fuente de verdad para esa función.**
> El conteo de argumentos, orden, y layout de retorno mostrados en el wrapper
> han sido verificados contra el COM bridge live de SAP2000.

**Workflow para usar un wrapper:**
1. `query_function_registry(function_path="SapModel.X.Y")` → verificar `wrapper_script`
2. Si existe: `load_script("func_X_Y")` → copiar la llamada verbatim
3. Solo si no existe: consultar `search_api_docs` y marcar como no verificado

### Auto-Registro

Cuando un script se ejecuta exitosamente via `run_sap_script`, todas las
funciones API usadas se detectan y registran automáticamente como verificadas.
La respuesta incluye una lista `registered_functions` mostrando lo capturado.

## Unidades

Establecer unidades ANTES de crear geometría:
```python
ret = SapModel.SetPresentUnits(6)  # kN_m_C
```

Para la lista completa de enumeraciones (eUnits, eMatType, eLoadPatternType, etc.)
→ ver [enum-reference.md](references/enum-reference.md).

## Arrays

- **0-based** en todos los casos
- Al pasar arrays a COM, usar listas de Python
- Arrays dinámicos en output: COM los llena y retorna en la tupla

## Modificadores de Sección Frame

Array de 8 valores (índices 0–7):
```python
ModValue = [1000, 0, 0, 1, 1, 1, 1, 1]
# [0]=Area, [1]=AS2, [2]=AS3, [3]=Torsion, [4]=I22, [5]=I33, [6]=Mass, [7]=Weight
ret = SapModel.PropFrame.SetModifiers("R1", ModValue)
```

## Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `return_code != 0` | Parámetros inválidos o estado incorrecto | Verificar tipos y orden de params via wrapper o `search_api_docs` |
| `AttributeError: 'NoneType'` | SapModel es None | Conexión perdida — llamar `connect_sap2000` |
| `COMError` | Fallo de interfaz COM | SAP2000 pudo haber crasheado — reconectar |
| `Module blocked` | Importando os, subprocess, etc. | Usar solo módulos permitidos (math, json, datetime, etc.) |
| `Timeout after 120s` | Análisis tomando demasiado tiempo | Simplificar modelo o aumentar timeout |
| `IndexError` | Layout ByRef incorrecto | Verificar wrapper: `raw[0]` vs `raw[-1]` |
| `AssertionError` | Validación falló | Leer mensaje del assert, ajustar parámetros |

## Jerarquía de Objetos

```
SapObject (cOAPI)
├── ApplicationStart()
├── ApplicationExit(save)
├── GetOAPIVersionNumber()
└── SapModel (cSapModel)
    ├── InitializeNewModel()
    ├── SetPresentUnits(units)
    ├── GetPresentUnits()
    ├── File
    │   ├── NewBlank()
    │   ├── New2DFrame(type, stories, height, bays, width)
    │   ├── New3DFrame(type, stories, height, baysX, widthX, baysY, widthY)
    │   ├── Save(path)
    │   └── OpenFile(path)
    ├── PropMaterial
    │   ├── SetMaterial(name, type)
    │   └── SetMPIsotropic(name, E, poisson, thermal)
    ├── PropFrame
    │   ├── SetRectangle(name, material, depth, width)
    │   └── SetModifiers(name, value_array)
    ├── FrameObj
    │   ├── AddByCoord(x1,y1,z1, x2,y2,z2, name, section, group)
    │   ├── GetPoints(name) → [point1, point2, ret_code]
    │   ├── Count() → int
    │   ├── SetLoadDistributed(name, pattern, type, dir, dist1, dist2, val1, val2)
    │   └── SetLoadPoint(name, pattern, type, dir, dist, val)
    ├── AreaObj
    │   ├── AddByCoord(nPoints, x[], y[], z[], name, prop)
    │   ├── AddByPoint(nPoints, points[], name, prop)
    │   └── Count() → int
    ├── PointObj
    │   ├── SetRestraint(name, restraint_array)
    │   ├── SetLoadForce(name, pattern, value_array)
    │   └── Count() → int
    ├── LoadPatterns
    │   └── Add(name, type, selfMassMultiplier)
    ├── LoadCases
    │   └── ChangeName(old, new)
    ├── RespCombo
    │   └── Add(name, comboType)
    ├── Analyze
    │   ├── RunAnalysis()
    │   ├── CreateAnalysisModel()
    │   └── DeleteResults(name, all)
    ├── Results
    │   ├── Setup
    │   │   ├── DeselectAllCasesAndCombosForOutput()
    │   │   └── SetCaseSelectedForOutput(name)
    │   └── JointDispl(name, itemType, ...) → [NRes, Obj[], Elm[], LC[], StType[], StNum[], U1[], U2[], U3[], R1[], R2[], R3[], ret_code]
    ├── View
    │   └── RefreshView(window, zoom)
    └── SelectObj
        ├── All()
        └── ClearSelection()
```

## Archivos de Referencia

Para información detallada, cargar estos archivos bajo demanda:
- [Patrones API](references/api-patterns.md) — Patrones detallados para operaciones comunes
- [Workflows Comunes](references/common-workflows.md) — Pasos para tareas típicas
- [Referencia de Enumeraciones](references/enum-reference.md) — Valores completos de enums
- [Templates de Scripts](references/script-templates.md) — Templates paramétricos reutilizables
- [Generación de GUI](references/gui-generation.md) — Guía para generar GUI standalone
```

##### Step 2 Verification Checklist
- [x] SKILL.md ya NO contiene el workflow de 10 pasos (ahora vive en el agente)
- [x] SKILL.md ya NO contiene instrucciones de personalidad/comportamiento
- [x] SKILL.md MANTIENE: convenciones ByRef, templates de script, function registry, errores comunes, jerarquía de objetos
- [x] Los enums inline (eMatType, eLoadPatternType, e2DFrameType, e3DFrameType) han sido ELIMINADOS y reemplazados por enlace a `enum-reference.md`
- [x] El enlace a `gui-generation.md` está presente (se creará en Step 3)
- [x] Todo el texto está en español (excepto nombres de funciones/variables que son en inglés)
- [ ] Sin errores de Markdown

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 3: Crear `gui-generation.md` y consolidar enums

Este paso crea la guía dedicada de generación de GUI y verifica que los enums estén consolidados.

- [ ] Crear el archivo `.github/skills/sap2000-api/references/gui-generation.md` con el siguiente contenido:
- [ ] Copiar y pegar el código siguiente en `.github/skills/sap2000-api/references/gui-generation.md`:

```markdown
# Generación de GUI Standalone (PySide6 + COM Directo)

## Cuándo Ofrecer GUI

Ofrecer generación de GUI **después** de que un script ha sido:
- ✅ Ejecutado exitosamente via `run_sap_script`
- ✅ Guardado en la biblioteca de scripts
- ✅ Funciones registradas en el registry

**Pregunta de transición:**
> *"El script está verificado y guardado. ¿Quieres generar una GUI standalone
> (PySide6) para que puedas ejecutar este modelo sin necesidad del agente/MCP?"*

## Objetivo

Convertir un script MCP verificado en un mini-software standalone compuesto por:
- `backend_{nombre}.py` — Lógica SAP2000 con COM directo (`comtypes.client`)
- `gui_{nombre}.py` — Interfaz PySide6 con botones Conectar/Ejecutar/Desconectar

**Resultado:** Un software que el usuario puede distribuir e integrar en sus
herramientas, **independiente del framework de IA**.

## Estructura de Archivos

```
scripts/{nombre}/
    gui_{nombre}.py         # GUI PySide6
    backend_{nombre}.py     # Lógica SAP2000 COM directo
```

**Regla:** La carpeta GUI solo contiene `gui_*.py` + `backend_*.py`.
Los scripts MCP originales van en `scripts/` root (ej: `scripts/example_*.py`).

## Paso 1: Identificar Inputs del Script

Revisar las variables configurables al inicio del script verificado.
Cada variable configurable se convierte en un campo de la GUI.

**Ejemplo — ring_areas:**
```python
# Estas variables del script...
r_inner = 1.0
r_mid1  = 2.0
r_mid2  = 3.5
r_outer = 5.0
t1 = 0.30
t2 = 0.20
n_segs = 36

# ...se convierten en inputs de GUI:
#   QLineEdit("r_inner", default="1.0")
#   QLineEdit("r_mid1",  default="2.0")
#   ...etc.
```

## Paso 2: Generar Backend Standalone

Usar como base la plantilla `scripts/templates/backend_template.py`:

1. **Copiar** `backend_template.py` → `backend_{nombre}.py`
2. **Renombrar** `MyConfig` → `{Nombre}Config` con los parámetros del script
3. **Renombrar** `MyBackend` → `{Nombre}Backend`
4. **Copiar la lógica** del script verificado al método `run()`:
   - Variables globales → `config.param_x`
   - `SapModel` (pre-inyectado en sandbox) → `self.sap_model`
   - `result` global → `result` local (dict)
   - `sap_temp_dir` → Ruta configurable o `tempfile.gettempdir()`
   - Funciones auxiliares → métodos de la clase Backend
5. **Mantener asserts** y estructura de tareas numeradas

### Reglas Inquebrantables del Backend

- ❌ NO importar `sap_bridge`, `sap_executor`, ni nada de `mcp_server/`
- ❌ NO importar `app_logger`, `sap_utils_common`, ni módulos externos no estándar
- ✅ Solo `comtypes.client`, `math`, `dataclasses`, stdlib
- ✅ `SapConnection` con `connect()`, `disconnect()`, `is_connected`

### Patrón del Backend

```python
import comtypes.client
from dataclasses import dataclass

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""
    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing=True) -> dict:
        # ... ver backend_template.py para implementación completa
        pass

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}

@dataclass
class NombreConfig:
    param_1: float = 1.0
    param_2: str = "DEFAULT"

class NombreBackend:
    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    def run(self, config: NombreConfig) -> dict:
        SapModel = self.sap_model
        result = {}
        # ... lógica del script verificado ...
        result["success"] = True
        return result
```

## Paso 3: Generar GUI Standalone

Usar como base la plantilla `scripts/templates/gui_template.py`:

1. **Copiar** `gui_template.py` → `gui_{nombre}.py`
2. **Ajustar import:** `from backend_{nombre} import SapConnection, {Nombre}Backend, {Nombre}Config`
3. **Reemplazar inputs:** Un `QLineEdit` por cada variable configurable (de Paso 1)
4. **Ajustar `_build_config()`:** Leer los inputs y crear el Config
5. **Ajustar `_format_result()`:** Mostrar métricas relevantes del resultado
6. **Renombrar** `MainWindow` → `{Nombre}GUI`
7. **Ajustar título** del `setWindowTitle()`

### Patrón de la GUI

La GUI usa 3 Workers (QThread) para operaciones async:
- `ConnectWorker` — Conexión a SAP2000
- `RunWorker` — Ejecución del backend
- `DisconnectWorker` — Desconexión

Elementos de la interfaz:
- Status indicator (rojo/verde)
- Input section (QGroupBox + QLineEdit fields)
- Output log (QTextEdit, read-only, Consolas 9pt)
- 3 botones: Conectar / Ejecutar / Desconectar
- `_busy(True/False)` para deshabilitar botones durante ejecución

## Paso 4: Testing

1. **Sintaxis:** `python -c "import ast; ast.parse(open('backend_*.py').read())"`
2. **GUI abre:** `python gui_{nombre}.py` → debe abrir ventana (sin SAP2000)
3. **Flujo completo** (si SAP2000 disponible):
   - Conectar → status verde
   - Ingresar parámetros → Ejecutar → log muestra resultado
   - Desconectar → status rojo

## Templates de Referencia

- **Backend base:** `scripts/templates/backend_template.py`
- **GUI base:** `scripts/templates/gui_template.py`

## Ejemplos Existentes

- **Placa Base:** `scripts/placabase/backend_placabase.py` + `gui_placabase.py`
- **Ring Areas:** `scripts/ring_areas/backend_ring_areas.py` + `gui_ring_areas.py`

## Estilo de Código

Todo el código generado debe seguir el estilo de `scripts/example_1001_simple_beam.py`:
- Headers claros: `# ── Task N: Nombre ──────────────────────────────`
- Cada llamada API: `assert ret == 0, f"NombreFuncion failed: {ret}"`
- Variables configurables al inicio, separadas visualmente
- Resultado en dict (`result["key"] = value`)
- Fórmulas de referencia en comentarios (si aplica)
```

- [ ] Verificar que `.github/skills/sap2000-api/references/enum-reference.md` contiene TODOS estos enums:

| Enum | Verificar presente |
|------|--------------------|
| eUnits (12 valores) | ✅ Ya presente |
| eMatType (7 valores) | ✅ Ya presente |
| eLoadPatternType (13 valores) | ✅ Ya presente |
| e2DFrameType (3 valores) | ✅ Ya presente |
| e3DFrameType (4 valores) | ✅ Ya presente |
| eLoadCaseType (12 valores) | ✅ Ya presente |
| eItemTypeElm (4 valores) | ✅ Ya presente |
| eConstraintType (7+ valores) | ✅ Ya presente (incluye Local=7, Weld=13) |
| eCombType (5 valores) | ✅ Ya presente |

> **Nota:** El archivo `enum-reference.md` existente ya contiene todos los enums necesarios. No requiere modificación.

##### Step 3 Verification Checklist
- [ ] `gui-generation.md` existe en `.github/skills/sap2000-api/references/`
- [ ] Contiene workflow completo: identificar inputs → backend → GUI → testing
- [ ] Enlaza correctamente a templates (`scripts/templates/backend_template.py`, `gui_template.py`)
- [ ] Enlaza correctamente a ejemplos (`scripts/placabase/`, `scripts/ring_areas/`)
- [ ] Reglas de importación están claras (NO importar mcp_server, SOLO comtypes + stdlib)
- [ ] `enum-reference.md` tiene los 9 tipos de enum completos
- [ ] Ningún otro archivo duplica las tablas de enums (SKILL.md ya no las incluye tras Step 2)

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 4: Reescribir `copilot-instructions.md` como router ligero

- [ ] Reemplazar el contenido completo de `.github/copilot-instructions.md` con el siguiente:
- [ ] Copiar y pegar el código siguiente en `.github/copilot-instructions.md`:

```markdown
# SAP2000 API Skill — Instrucciones de Copilot

## ¿Qué es este workspace?

Framework para automatizar SAP2000 mediante scripts Python ejecutados a través
de un MCP bridge local (COM). Permite generar modelos estructurales, asignar
cargas, ejecutar análisis y extraer resultados de forma programática.

## Mapa de Documentación

| Documento | Para qué |
|-----------|----------|
| `.github/agents/sap2000-scripter.agent.md` | Agente con workflow completo (usa `@sap2000-scripter`) |
| `.github/skills/sap2000-api/SKILL.md` | Referencia técnica API (convenciones, templates, registry) |
| `.github/skills/sap2000-api/references/api-patterns.md` | Patrones detallados de operaciones comunes |
| `.github/skills/sap2000-api/references/enum-reference.md` | Enumeraciones completas (eUnits, eMatType, etc.) |
| `.github/skills/sap2000-api/references/common-workflows.md` | Workflows paso a paso para tareas típicas |
| `.github/skills/sap2000-api/references/script-templates.md` | Templates paramétricos (grid, circular, placa) |
| `.github/skills/sap2000-api/references/gui-generation.md` | Guía de generación de GUI standalone (PySide6) |
| `scripts/wrappers/` | Funciones verificadas (fuente de verdad para firmas) |
| `scripts/templates/` | Templates base para backend y GUI standalone |
| `scripts/registry.json` | Registry de funciones verificadas |

## Configuración MCP

El servidor MCP se autoconfigura via `.vscode/mcp.json`:
- **Python venv:** `.venv/Scripts/python.exe`
- **Script:** `mcp_server/server.py`
- **Protocolo:** stdio (auto-start al invocar herramientas)
- **Tools expuestos:** 12 (connect, disconnect, get_model_info, execute_sap_function,
  run_sap_script, list_scripts, load_script, search_api_docs, list_api_categories,
  query_function_registry, register_verified_function, list_registry_categories)

## Cuándo usar qué

### Agente SAP2000 Scripter (`@sap2000-scripter`)

**Usar para:**
- Generar scripts de SAP2000 (marcos, áreas, análisis)
- Automatización estructural completa
- Workflow: research → código → ejecución → verificación → guardado

**Capacidades:**
- Research automático para scripts complejos (via subagent Explore)
- Consulta inteligente al registry de funciones verificadas
- Generación iterativa con testing incremental
- Oferta de GUI standalone al finalizar

### Skill sap2000-api (attachment)

**Usar para:**
- Consultas rápidas sobre convenciones API (ByRef, return codes)
- Patrones de código específicos
- Referencia de enumeraciones y jerarquía de objetos

## Requisitos del Sistema

- Windows OS (SAP2000 solo corre en Windows)
- Python 3.10+
- SAP2000 instalado localmente
- Paquetes: `comtypes`, `mcp[cli]` (ver `mcp_server/requirements.txt`)

## Quick Start

1. Activar venv: `.venv/Scripts/Activate.ps1`
2. Invocar agente: `@sap2000-scripter genera una viga simple con carga muerta`
3. El agente maneja el resto (conexión, registry, generación, ejecución)
```

##### Step 4 Verification Checklist
- [ ] `copilot-instructions.md` es un router ligero (~70 líneas)
- [ ] Contiene mapa de documentación con todos los archivos relevantes
- [ ] Documenta la configuración MCP (`.vscode/mcp.json`)
- [ ] Explica cuándo usar el agente vs la skill
- [ ] Lista requisitos del sistema
- [ ] Todo en español
- [ ] Un nuevo usuario puede leer este archivo y entender qué es el workspace, dónde buscar info, y cómo empezar

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5: Archivar workflows redundantes

- [ ] Crear el directorio `plans/_archive/`
- [ ] Mover `plans/workflow-script-creation.md` a `plans/_archive/workflow-script-creation.md`
- [ ] Mover `plans/quick-reference-workflow.md` a `plans/_archive/quick-reference-workflow.md`
- [ ] Crear `plans/_archive/README.md` con el siguiente contenido:

```powershell
# Comandos para mover archivos (ejecutar en terminal):
New-Item -ItemType Directory -Force -Path "plans/_archive"
Move-Item -Path "plans/workflow-script-creation.md" -Destination "plans/_archive/workflow-script-creation.md"
Move-Item -Path "plans/quick-reference-workflow.md" -Destination "plans/_archive/quick-reference-workflow.md"
```

- [ ] Copiar y pegar el código siguiente en `plans/_archive/README.md`:

```markdown
# Archive — Workflows Originales

Estos workflows fueron consolidados en el agente `sap2000-scripter.agent.md`
(`.github/agents/sap2000-scripter.agent.md`).

Se mantienen aquí como referencia histórica.

**No usar estos archivos** — el workflow actual vive en el agente.

## Archivos archivados

| Archivo | Contenido original | Nuevo destino |
|---------|--------------------|---------------|
| `workflow-script-creation.md` | Workflow de 6 fases (500 líneas, español) | Pasos 0-10 del agente + `gui-generation.md` |
| `quick-reference-workflow.md` | Quick reference (80 líneas, mixto) | Reglas críticas del agente |

## Fecha de archivado

Consolidado como parte del refactor `refactor/consolidate-docs-and-agent`.
```

- [ ] Verificar que no hay enlaces rotos en la documentación activa:

| Archivo | Enlace a verificar | Estado esperado |
|---------|--------------------|-----------------| 
| `SKILL.md` | `references/api-patterns.md` | ✅ Existe |
| `SKILL.md` | `references/common-workflows.md` | ✅ Existe |
| `SKILL.md` | `references/enum-reference.md` | ✅ Existe |
| `SKILL.md` | `references/script-templates.md` | ✅ Existe |
| `SKILL.md` | `references/gui-generation.md` | ✅ Creado en Step 3 |
| `copilot-instructions.md` | Todas las rutas en mapa de docs | ✅ Verificar |

##### Step 5 Verification Checklist
- [ ] `plans/_archive/` existe y contiene los 3 archivos (2 workflows + README)
- [ ] `plans/workflow-script-creation.md` ya NO existe en su ubicación original
- [ ] `plans/quick-reference-workflow.md` ya NO existe en su ubicación original
- [ ] `plans/_archive/README.md` explica el archivado y el nuevo destino
- [ ] No hay enlaces rotos en `SKILL.md`, `copilot-instructions.md`, ni `sap2000-scripter.agent.md`

#### Step 5 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 6: Validación End-to-End

Este paso final verifica que toda la arquitectura de 3 capas funciona correctamente.

- [ ] Abrir VS Code y verificar que `@sap2000-scripter` aparece en el dropdown de agentes
- [ ] Invocar `@sap2000-scripter` con un mensaje simple (ej: "¿Qué puedes hacer?") y verificar que responde con el contexto correcto
- [ ] Verificar que `copilot-instructions.md` se carga como instrucciones globales (debe influir el comportamiento de Copilot Chat)
- [ ] Verificar que la skill `sap2000-api` se carga correctamente al preguntar sobre API de SAP2000

**Test de flujo completo (si SAP2000 está disponible):**
- [ ] Invocar: `@sap2000-scripter genera una viga simple con carga muerta de 10 kN/m`
- [ ] Verificar que el agente sigue el workflow de 10 pasos
- [ ] Verificar que consulta el registry antes de generar código
- [ ] Verificar que ejecuta y verifica el script
- [ ] Verificar que ofrece guardar y generar GUI al finalizar

**Verificación de estructura final:**
```
.github/
  copilot-instructions.md          ← CAPA 1: Router ligero (~70 líneas)
  agents/
    sap2000-scripter.agent.md      ← CAPA 2: Agente con workflow (~200 líneas)
  skills/sap2000-api/
    SKILL.md                       ← CAPA 3: Solo referencia técnica (~300 líneas)
    references/
      api-patterns.md              ← (sin cambios)
      enum-reference.md            ← (consolidado: TODOS los enums)
      common-workflows.md          ← (sin cambios)
      script-templates.md          ← (sin cambios)
      gui-generation.md            ← NUEVO: Guía de generación GUI
plans/
  consolidation-standardization/
    plan.md                        ← Plan original
    implementation.md              ← Este archivo
  _archive/
    workflow-script-creation.md    ← Archivado
    quick-reference-workflow.md    ← Archivado
    README.md                      ← Explica el archivado
```

##### Step 6 Verification Checklist
- [ ] Agente aparece en dropdown de VS Code Chat
- [ ] Agente responde con contexto correcto (menciona SAP2000, workflow, wrappers)
- [ ] SKILL.md se carga como skill al hacer preguntas sobre API de SAP2000
- [ ] No hay archivos huérfanos o enlaces rotos
- [ ] La estructura final coincide con el diagrama de arriba

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here to confirm everything works end-to-end. Stage and commit the final state.
