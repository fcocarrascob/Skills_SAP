# Workflow para Crear Scripts Complejos de SAP2000

Este documento describe el procedimiento paso a paso para construir scripts complejos
de SAP2000 (como `example_placabase_parametric.py`) usando el skill `sap2000-api`
y el MCP bridge.

## 📋 Tabla de Contenidos

1. [Fase 1: Planificación y Descomposición](#fase-1-planificación-y-descomposición)
2. [Fase 2: Investigación de API Functions](#fase-2-investigación-de-api-functions)
3. [Fase 3: Desarrollo Iterativo por Tareas](#fase-3-desarrollo-iterativo-por-tareas)
4. [Fase 4: Integración y Refinamiento](#fase-4-integración-y-refinamiento)
5. [Fase 5: Documentación y Guardado](#fase-5-documentación-y-guardado)
6. [Ejemplo Práctico: Placa Base](#ejemplo-práctico-placa-base)

---

## Fase 1: Planificación y Descomposición

### 1.1 Definir el Objetivo Final

**Pregunta clave:** ¿Qué debe hacer el script?

**Ejemplo - Placa Base:**
> Generar un modelo parametrizado de placa base con pernos de anclaje, silla opcional,
> body constraints, TC limits, y resortes de balasto.

### 1.2 Identificar Variables de Configuración

Listar TODAS las variables que el usuario debe poder modificar:

```python
# Geometría
bolt_dia = 25.0
n_pernos = 4
H_col = 300.0
B_col = 250.0

# Propiedades
plate_thickness = 20.0
flange_thickness = 15.0
web_thickness = 10.0

# Opcionales
include_anchor_chair = False
ks_balasto = 5.0

# Auto-generados
bolt_centers = []  # Se calcula si está vacío
```

### 1.3 Descomponer en Tareas (Tasks)

Dividir el script en **tareas independientes** que se pueden implementar incrementalmente:

| # | Tarea | Descripción | Dependencias |
|---|-------|-------------|--------------|
| 1 | Initialize & Units | `InitializeNewModel()`, `File.NewBlank()`, `SetPresentUnits()` | Ninguna |
| 2 | Materiales | `PropMaterial.SetMaterial()`, `SetMPIsotropic()` | 1 |
| 3 | Propiedades Shell | `PropArea.SetShell_1()` para PLACA_BASE, ALA, ALMA | 2 |
| 4 | Geometría Columna | `AreaObj.AddByCoord()` para flanges y web | 3 |
| 5 | Puntos Geométricos | Funciones auxiliares: `create_circle_points()`, `create_square_points()` | 1 |
| 6 | Mesh de Pernos | `create_ring_mesh()` — conectar círculo → interior → exterior | 4, 5 |
| 7 | Frames de Pernos | `PropFrame.SetCircle()`, `FrameObj.AddByPoint()` | 3, 6 |
| 8 | Body Constraints | `ConstraintDef.SetBody()`, `PointObj.SetConstraint()` | 6, 7 |
| 9 | TC Limits | `FrameObj.SetTCLimits()` | 7 |
| 10 | Pin Restraints | `PointObj.SetRestraint()` | 7 |
| 11 | Silla de Anclaje | Repetir 5-10 a otra altura | 6, 7, 8 |
| 12 | Área de Enlace | `AreaObj.AddByPoint()` para A_outer_link | 6 |
| 13 | Mesh Refinement | `SelectObj.CoordinateRange()`, `EditArea.Divide()` | 4, 6, 12 |
| 14 | Balasto | `AreaObj.SetSpring()` con `SimpleSpringType=2` | 6, 12, 13 |
| 15 | Save & Refresh | `File.Save()`, `View.RefreshView()` | 1-14 |

**Criterio de Independencia:**
- Cada tarea debe ser **verificable** por sí sola (ejecutar → ver resultado)
- Minimizar dependencias entre tareas para iteración paralela

---

## Fase 2: Investigación de API Functions

### 2.1 Verificar Conexión al MCP Bridge

**Siempre empezar con:**

```
Herramienta: get_model_info
```

- ✅ Conectado → Continuar
- ❌ No conectado → Ejecutar `connect_sap2000`

### 2.2 Buscar Funciones en el Registry

Para CADA función de API que necesites, **primero buscar en el registry**:

```
Herramienta: query_function_registry
Parámetros:
  function_path: "SapModel.PropFrame.SetCircle"  # o usar query="circle frame"
```

**Casos posibles:**

| Resultado | Acción |
|-----------|--------|
| ✅ **Verified=true + wrapper_script** | Cargar wrapper con `load_script("func_PropFrame_SetCircle")`, copiar llamada exacta |
| ⚠️ **Registered, verified=false** | Buscar en API docs con `search_api_docs`, marcar como no confiable |
| ❌ **No existe** | Buscar en API docs, será la primera vez que se verifica |

### 2.3 Cargar Wrappers Existentes

Si el wrapper existe, **cargarlo SIEMPRE antes de usar la función**:

```
Herramienta: load_script
Parámetros:
  script_name: "func_PropFrame_SetCircle"
```

**Beneficio:** El wrapper tiene:
- ✅ Signature exacta verificada contra COM bridge
- ✅ Orden correcto de argumentos
- ✅ Layout de ByRef outputs
- ✅ Manejo de return codes

**Ejemplo - Comparación:**

```python
# ❌ INCORRECTO (inventado, no verificado):
ret = SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0, 0)

# ✅ CORRECTO (copiado del wrapper):
ret = SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0)
assert ret == 0, f"SetCircle failed: {ret}"
```

### 2.4 Buscar Scripts Similares en la Librería

```
Herramienta: list_scripts
Parámetros:
  query: "frame" | "area" | "bolt" | "plate" | etc.
```

**Objetivo:** Encontrar patrones reutilizables (ej: otro script que usa `SetTCLimits`).

### 2.5 Buscar en API Docs (SOLO si no hay wrapper)

```
Herramienta: search_api_docs
Parámetros:
  query: "SetCircle" | "tension compression limit" | etc.
```

**⚠️ ADVERTENCIA:**
- API docs describen la interfaz VBA, **NO el comportamiento COM en Python**
- Diferencias comunes:
  - Argumentos faltantes (ej: `ItemType` omitido en Python)
  - Orden diferente de coordenadas
  - ByRef layout invertido

**Regla de Oro:**
> **WRAPPER > API DOCS**  
> Si hay wrapper verificado, ignorar API docs para esa función.

---

## Fase 3: Desarrollo Iterativo por Tareas

### 3.1 Implementar una Tarea a la Vez

**Template de iteración:**

```markdown
## Task N: [Nombre de la Tarea]

### 3.1.1 Escribir el código
- Copiar llamadas de wrappers verificados
- Usar `assert` para validar return codes
- Escribir a `result[]` para verificación

### 3.1.2 Ejecutar con MCP
Herramienta: run_sap_script
Parámetros:
  script: [código Python]

### 3.1.3 Verificar Resultado
- ✅ `success=true`: Revisar `result`, continuar
- ❌ `success=false`: Analizar `error`, corregir, re-ejecutar

### 3.1.4 Guardar versión (opcional)
Herramienta: run_sap_script
Parámetros:
  script: [mismo código]
  save_as: "task_N_[nombre].py"
```

### 3.2 Estrategia de Testing Incremental

**Principio:** Cada tarea debe **ejecutarse independientemente** para detectar errores temprano.

```python
# ── Task 1: Initialize ────────────────────────────────────────────────
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

result["initialized"] = True

# ✅ EJECUTAR → Verificar result["initialized"] == True
```

```python
# ── Task 3: Propiedades Shell ─────────────────────────────────────────
ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

ret = SapModel.PropArea.SetShell_1(
    "PLACA_BASE", 1, True, "A992Fy50", 0.0, 20.0, 20.0
)
assert ret == 0, f"SetShell_1 failed: {ret}"

result["shell_prop_created"] = True

# ✅ EJECUTAR → Verificar result["shell_prop_created"] == True
```

### 3.3 Patrón de Funciones Auxiliares

**Cuándo crear una función auxiliar:**
- Lógica repetida ≥3 veces → Extraer a función
- Lógica compleja (ej: alinear anillos) → Función separada
- Operación geométrica reutilizable → Función genérica

**Template:**

```python
def create_circle_points(cx, cy, z, radius, num_points=16, prefix="P_c"):
    """Genera puntos en círculo en sentido horario (visto desde +Z).
    
    Args:
        cx, cy: Coordenadas del centro.
        z: Cota Z.
        radius: Radio del círculo.
        num_points: Número de puntos a generar.
        prefix: Prefijo para nombrar puntos.
        
    Returns:
        Lista de nombres de puntos creados.
    """
    names = []
    for j in range(num_points):
        angle = -math.radians(j * (360.0 / num_points))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        ret = SapModel.PointObj.AddCartesian(x, y, z, "", f"{prefix}{j+1}")
        point_name = ret[0] if isinstance(ret, tuple) else f"{prefix}{j+1}"
        names.append(point_name)
    return names
```

**Testing de función auxiliar:**

```python
# Test: Crear círculo de 8 puntos
ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

points = create_circle_points(0, 0, 0, 50.0, 8, "TEST_C")
result["num_points"] = len(points)
result["first_point"] = points[0]

# ✅ EJECUTAR → Verificar result["num_points"] == 8
```

### 3.4 Manejo de Errores y Debugging

**Errores más comunes:**

| Error | Causa Probable | Solución |
|-------|----------------|----------|
| `return_code != 0` | Parámetros incorrectos | Verificar wrapper o API docs |
| `IndexError: list index out of range` | ByRef layout incorrecto | Revisar wrapper: `ret[0]` vs `ret[-1]` |
| `AttributeError: 'int' object...` | Asumiste tuple, pero es int | Usar `isinstance(ret, tuple)` antes de indexar |
| `COMError` | SAP2000 crasheó | Reconectar: `connect_sap2000` |
| `AssertionError` | Validación falló | Leer mensaje del assert, ajustar params |

**Estrategia de debugging:**

1. **Agregar prints:**
   ```python
   raw = SapModel.FrameObj.AddByCoord(...)
   print(f"AddByCoord returned: {raw}")  # Ver estructura exacta
   frame_name = raw[0]
   ret_code = raw[-1]
   ```

2. **Validar cada paso:**
   ```python
   ret = SapModel.PropFrame.SetCircle("SEC1", "STEEL", 50.0)
   print(f"SetCircle return code: {ret}")
   assert ret == 0, f"SetCircle failed with code {ret}"
   ```

3. **Escribir a result para inspección:**
   ```python
   result["raw_return"] = str(raw)  # Convertir a string para JSON
   result["frame_name"] = frame_name
   result["ret_code"] = ret_code
   ```

---

## Fase 4: Integración y Refinamiento

### 4.1 Combinar Tareas en Script Completo

Una vez que TODAS las tareas funcionan individualmente:

1. **Copiar todas las funciones auxiliares al inicio**
2. **Ordenar tareas según dependencias** (usar gráfico de Fase 1.3)
3. **Agregar separadores visuales:**
   ```python
   # ═════════════════════════════════════════════════════════════════════
   # ╔═══════════════════════════════════════════════════════════════════╗
   # ║                    CONFIGURACION DE VARIABLES                      ║
   # ╚═══════════════════════════════════════════════════════════════════╝
   # ═════════════════════════════════════════════════════════════════════
   ```
4. **Eliminar código de testing redundante** (mantener solo asserts esenciales)

### 4.2 Verificación End-to-End

**Ejecutar el script completo:**

```
Herramienta: run_sap_script
Parámetros:
  script: [script completo integrado]
```

**Checklist de verificación:**

- [ ] `success = true`
- [ ] `result` contiene todas las métricas esperadas
- [ ] `stdout` no tiene errores críticos
- [ ] Modelo se guarda correctamente en `sap_temp_dir`
- [ ] Vista se refresca sin crashes

### 4.3 Refinamiento de Código

**Optimizaciones opcionales:**

1. **Reducir redundancia:**
   ```python
   # ❌ Antes:
   ret = SapModel.PropArea.SetShell_1("PLACA", 1, True, "A992Fy50", 0.0, 20.0, 20.0)
   assert ret == 0
   ret = SapModel.PropArea.SetShell_1("ALA", 1, True, "A992Fy50", 0.0, 15.0, 15.0)
   assert ret == 0
   ret = SapModel.PropArea.SetShell_1("ALMA", 1, True, "A992Fy50", 0.0, 10.0, 10.0)
   assert ret == 0
   
   # ✅ Después:
   def create_shell_prop(name, thickness, mat="A992Fy50"):
       ret = SapModel.PropArea.SetShell_1(name, 1, True, mat, 0.0, thickness, thickness)
       assert ret == 0, f"SetShell_1 failed for {name}: {ret}"
   
   create_shell_prop("PLACA_BASE", plate_thickness)
   create_shell_prop("ALA", flange_thickness)
   create_shell_prop("ALMA", web_thickness)
   ```

2. **Mejorar legibilidad:**
   - Agregar comentarios descriptivos
   - Usar nombres de variables auto-documentados
   - Agrupar operaciones relacionadas

3. **Agregar resumen final:**
   ```python
   # ── 12. Resultados Finales ───────────────────────────────────────────
   result["bolt_count"] = len(bolt_centers)
   result["bolt_frame_count"] = len(bolt_frame_names)
   result["include_anchor_chair"] = include_anchor_chair
   result["success"] = True
   
   print("\n" + "═"*70)
   print("🎉 GENERACION DE PLACA BASE COMPLETADA EXITOSAMENTE 🎉")
   print("═"*70)
   print(f"  • Pernos creados: {len(bolt_centers)}")
   print(f"  • Frames de pernos: {len(bolt_frame_names)}")
   ```

---

## Fase 5: Documentación y Guardado

### 5.1 Agregar Header Completo

```python
# ─── SAP2000 [Nombre del Script] — [Descripción Corta] ────────────────
# Description: [Descripción detallada de qué hace el script]
#
# Features:
#   - [Feature 1]
#   - [Feature 2]
#   - [Feature 3]
#
# Reference:
#   [Cualquier referencia técnica, fórmulas, normas]
#
# Units: [Sistema de unidades usado, ej: kgf_cm_C (14)]
# ─────────────────────────────────────────────────────────────────────
```

### 5.2 Guardar en la Librería

```
Herramienta: run_sap_script
Parámetros:
  script: [script final]
  save_as: "example_placabase_parametric.py"
```

**Naming convention:**
- `example_*` → Scripts de demostración completos
- `func_*` → Wrappers de funciones individuales
- `test_*` → Scripts de testing/validación

### 5.3 Registrar Funciones Nuevas (si aplica)

Si usaste funciones que NO estaban en el registry, registrarlas manualmente:

```
Herramienta: register_verified_function
Parámetros:
  function_path: "SapModel.AreaObj.SetSpring"
  category: "AreaObj - Spring Support"
  description: "Assigns spring support (balasto) to area objects"
  parameter_notes: "MyType=1 (simple), SimpleSpringType=2 (compression only), Face=-1 (bottom)"
  verified: true
  wrapper_script: "func_AreaObj_SetSpring.py"  # Si creaste wrapper
```

**Beneficio:** La próxima vez que tú (o alguien más) necesite esta función,
ya estará documentada y verificada.

---

## Ejemplo Práctico: Placa Base

### Desglose de Tareas Aplicado

#### Task 1: Initialize & Materials ✅
```python
# Variables configurables
bolt_dia = 25.0
H_col = 300.0
# ... (resto de variables)

# Initialize
ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

# Materials
ret = SapModel.PropMaterial.SetMaterial("A992Fy50", 1)  # Steel
```

**Verificación:** ✅ result["initialized"] = True

---

#### Task 2: Shell Properties ✅
```python
# Verificar wrapper primero:
# query_function_registry("SapModel.PropArea.SetShell_1")
# load_script("func_PropArea_SetShell_1")  # Si existe

ret = SapModel.PropArea.SetShell_1(
    "PLACA_BASE", 1, True, "A992Fy50", 0.0, 20.0, 20.0
)
assert ret == 0
```

**Verificación:** ✅ Modelo tiene propiedad "PLACA_BASE"

---

#### Task 3: Column Geometry ✅
```python
# Crear función auxiliar
def create_area_by_coord(xs, ys, zs, prop_name, user_name):
    ret = SapModel.AreaObj.AddByCoord(len(xs), xs, ys, zs, "", prop_name, user_name, "Global")
    assert ret[-1] == 0
    return ret[0]

# Usar función
create_area_by_coord(
    [-B_col/2, B_col/2, B_col/2, -B_col/2],
    [H_col/2, H_col/2, H_col/2, H_col/2],
    [0, 0, z_col, z_col],
    "ALA", "COL_FLANGE_TOP"
)
```

**Verificación:** ✅ Vista 3D muestra ala de columna

---

#### Task 4: Bolt Geometry (Círculos + Cuadrados) ✅
```python
# Función auxiliar de círculo
def create_circle_points(cx, cy, z, radius, num_points=16, prefix="P_c"):
    names = []
    for j in range(num_points):
        angle = -math.radians(j * (360.0 / num_points))
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        ret = SapModel.PointObj.AddCartesian(x, y, z, "", f"{prefix}{j+1}")
        names.append(ret[0] if isinstance(ret, tuple) else f"{prefix}{j+1}")
    return names

# Crear puntos del primer perno
cx, cy, cz = bolt_centers[0]
c_pts = create_circle_points(cx, cy, cz, circle_radius, 16, "P_c1_")
```

**Verificación:** ✅ Vista muestra 16 puntos en círculo

---

#### Task 5: Ring Mesh ✅
```python
# Función de mesh (requiere alinear rings primero)
def create_ring_mesh(inner_pts, outer_pts, center, prop_name, prefix):
    inner, outer = align_rings(inner_pts, outer_pts, center)
    n = min(len(inner), len(outer))
    for i in range(n):
        p1 = inner[i]
        p2 = inner[(i+1) % n]
        p3 = outer[(i+1) % n]
        p4 = outer[i]
        ret = SapModel.AreaObj.AddByPoint(4, [p1, p2, p3, p4], "", prop_name, f"{prefix}_{i+1}")

# Usar
create_ring_mesh(c_pts, in_pts, (cx, cy), "PLACA_BASE", "A_ring_in1")
```

**Verificación:** ✅ Vista muestra áreas conectando círculo → cuadrado

---

#### Task 6: Bolt Frames ✅
```python
# Verificar wrapper:
# query_function_registry("SapModel.PropFrame.SetCircle")
# load_script("func_PropFrame_SetCircle")

# Sección
section_name = f"BOLT_{int(bolt_dia)}"
ret = SapModel.PropFrame.SetCircle(section_name, "A36", bolt_dia)

# Frame
frame_name = create_bolt_frame(center_point_name, bottom_point, section_name, f"BOLT_FRAME_{idx}")
```

**Verificación:** ✅ Frame vertical visible en vista 3D

---

#### Task 7: TC Limits ✅
```python
# Verificar wrapper:
# query_function_registry("SapModel.FrameObj.SetTCLimits")
# load_script("func_FrameObj_SetTCLimits")

# ⚠️ NOTA: Wrapper tiene 5 args, NO 6 (ItemType omitido en Python)
ret = SapModel.FrameObj.SetTCLimits(
    frame_name,   # Name
    True,         # LimitCompressionExists
    0.0,          # LimitCompression
    False,        # LimitTensionExists
    0.0           # LimitTension
    # NO ItemType — omitido en Python COM
)
assert ret == 0
```

**Verificación:** ✅ Perno solo trabaja a tracción

---

#### Task 8: Body Constraints ✅
```python
# Verificar wrapper:
# query_function_registry("SapModel.ConstraintDef.SetBody")

def create_body_constraint(name, center_pt, circle_pts, dof_values):
    # Definir
    ret = SapModel.ConstraintDef.SetBody(name, dof_values, "Global")
    assert ret == 0
    
    # Asignar al centro
    ret = SapModel.PointObj.SetConstraint(center_pt, name)
    
    # Asignar a cada punto del círculo
    for pt in circle_pts:
        SapModel.PointObj.SetConstraint(pt, name)

# Usar
dof_values = [True, True, True, True, True, True]  # Todos restringidos
create_body_constraint("BOLT_BODY_1", center_point_name, c_pts, dof_values)
```

**Verificación:** ✅ Constraint visible en modelo

---

#### Task 9: Mesh Refinement ✅
```python
# Verificar wrapper:
# query_function_registry("SapModel.SelectObj.CoordinateRange")
# load_script("func_SelectObj_CoordinateRange")  # Ver orden de args

# ⚠️ NOTA: CSys viene ÚLTIMO, no en medio
ok = coordinate_range_select(
    -B_col/2, B_col/2,    # Xmin, Xmax
    H_col/2, H_col/2,     # Ymin, Ymax
    0.0, 0.0,             # Zmin, Zmax (plano base)
    point=True
)

if ok:
    new_areas = divide_area_by_selection("COL_FLANGE_TOP")
```

**Verificación:** ✅ Ala dividida en múltiples áreas donde hay puntos

---

#### Task 10: Balasto Spring ✅
```python
# Verificar wrapper:
# query_function_registry("SapModel.AreaObj.SetSpring")
# load_script("func_AreaObj_SetSpring")

current_units = SapModel.GetPresentUnits()
SapModel.SetPresentUnits(14)  # kgf_cm_C

# Seleccionar áreas en z=0
SapModel.SelectObj.ClearSelection()
coordinate_range_select(-1e10, 1e10, -1e10, 1e10, 0.0, 0.0, point=False, area=True)

# Asignar spring
vec = [0.0, 0.0, 0.0]
ret = SapModel.AreaObj.SetSpring(
    "ALL",        # Name (ignorado con ItemType=2)
    1,            # MyType: simple spring
    float(ks),    # s: rigidez
    2,            # SimpleSpringType: compression only
    "",           # LinkProp
    -1,           # Face: bottom
    2,            # SpringLocalOneType: normal to face
    1, True, vec, 0.0, True, "Local",
    2             # ItemType: SelectedObjects
)

SapModel.SetPresentUnits(current_units)
```

**Verificación:** ✅ Áreas en z=0 tienen resorte de balasto

---

### Resumen de Iteraciones

| Iteración | Tareas Completadas | Script Output | Próximo Paso |
|-----------|-------------------|---------------|--------------|
| 1 | Task 1-2 | ✅ Materiales OK | Agregar geometría |
| 2 | Task 3 | ✅ Columna visible | Agregar pernos |
| 3 | Task 4-6 | ✅ Pernos con frames | Agregar constraints |
| 4 | Task 7-8 | ✅ TC limits + body | Agregar mesh refinement |
| 5 | Task 9 | ✅ Mesh refinado | Agregar balasto |
| 6 | Task 10 | ✅ Balasto asignado | Integrar todo |
| 7 | Integración | ✅ Script completo funciona | Documentar y guardar |

---

## Resumen de Reglas Clave

### ✅ DO (Hacer)

1. **Siempre** verificar conexión con `get_model_info` antes de empezar
2. **Siempre** buscar wrappers con `query_function_registry` ANTES de inventar llamadas
3. **Siempre** cargar wrapper con `load_script` si existe
4. **Siempre** usar `assert ret == 0` después de llamadas API
5. **Siempre** escribir a `result[]` para verificación
6. **Siempre** usar `sap_temp_dir` para `File.Save()`
7. **Siempre** desarrollar por tareas incrementales
8. **Siempre** ejecutar cada tarea individualmente antes de integrar

### ❌ DON'T (No Hacer)

1. **Nunca** inventar signatures de funciones sin verificar wrapper/docs
2. **Nunca** ignorar return codes (`ret`)
3. **Nunca** hardcodear paths (usar `sap_temp_dir`)
4. **Nunca** asumir layout de ByRef outputs sin verificar
5. **Nunca** escribir scripts monolíticos sin testing incremental
6. **Nunca** mezclar signatures de API docs con wrappers verificados
7. **Nunca** omitir `InitializeNewModel()` + `File.NewBlank()` en cada tarea aislada
8. **Nunca** olvidar guardar con `save_as` cuando la iteración final funciona

---

## Plantilla de Checklist por Script

```markdown
## Checklist: [Nombre del Script]

### Planificación
- [ ] Objetivo definido claramente
- [ ] Variables identificadas
- [ ] Tareas descompuestas en grafo de dependencias

### Investigación
- [ ] Conexión MCP verificada (`get_model_info`)
- [ ] Funciones buscadas en registry (`query_function_registry`)
- [ ] Wrappers cargados (`load_script`)
- [ ] Scripts similares revisados (`list_scripts`)
- [ ] API docs consultadas solo para funciones sin wrapper

### Desarrollo
- [ ] Task 1 implementada y verificada
- [ ] Task 2 implementada y verificada
- [ ] Task 3 implementada y verificada
- [ ] ... (una por tarea)
- [ ] Funciones auxiliares extraídas y testeadas
- [ ] Errores debuggeados con prints y asserts

### Integración
- [ ] Todas las tareas combinadas en script completo
- [ ] Script ejecutado end-to-end exitosamente
- [ ] `result` contiene todas las métricas esperadas
- [ ] Código refinado (redundancia eliminada)

### Documentación
- [ ] Header completo agregado
- [ ] Comentarios descriptivos en cada sección
- [ ] Variables configurables documentadas
- [ ] Script guardado con `save_as`
- [ ] Funciones nuevas registradas (`register_verified_function`)

### Verificación Final
- [ ] `success = true`
- [ ] Modelo se visualiza correctamente en SAP2000
- [ ] Sin warnings críticos en `stdout`
- [ ] Script puede re-ejecutarse con diferentes parámetros
```

---

## Herramientas MCP Relevantes

| Herramienta | Cuándo Usar | Ejemplo |
|-------------|-------------|---------|
| `get_model_info` | Al inicio de cada sesión | Verificar conexión |
| `connect_sap2000` | Si model_info falla | Reconectar al bridge |
| `query_function_registry` | Para CADA función API | Buscar wrappers |
| `load_script` | Cuando hay wrapper | Copiar signature |
| `search_api_docs` | Solo si NO hay wrapper | Fallback de API |
| `list_scripts` | Buscar ejemplos similares | Inspiración |
| `run_sap_script` | Testing de cada tarea | Iteración |
| `run_sap_script` + `save_as` | Scripts finales | Guardar en librería |
| `register_verified_function` | Funciones nuevas | Documentar |

---

## Conclusión

Este workflow te permite construir scripts complejos de SAP2000 de manera **sistemática**,
**verificable** y **reutilizable**. La clave es:

1. **Descomponer** el problema en tareas pequeñas
2. **Investigar** funciones API usando registry y wrappers
3. **Iterar** tarea por tarea con verificación constante
4. **Integrar** cuando todo funciona individualmente
5. **Documentar** para futura reutilización

Siguiendo este proceso, puedes construir scripts tan complejos como el de placa base
sin perderte en debugging imposible o signatures incorrectas.
