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
