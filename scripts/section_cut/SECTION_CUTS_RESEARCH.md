# Section Cuts en SAP2000 — Investigación Completa

> **Fuentes:** API local (`API/Definitions.md`, `API/Analysis_Results.md`), documentación oficial CSI Americas (`csiamerica.com/products/sap2000/features`).  
> **Fecha:** Abril 2026

---

## 1. ¿Qué es un Section Cut?

Un **Section Cut** (corte de sección) es una herramienta de post-proceso que permite obtener la **resultante de fuerzas y momentos** en cualquier plano imaginario que atraviesa la estructura. El programa integra las fuerzas internas de todos los elementos que cruzan ese plano y entrega un único vector de fuerzas/momentos resultante.

Desde la documentación oficial de CSI:

> *"The resultant (free-body) forces and moments across any cut in the structure can be defined using section cuts. A section cut can have any shape and can be used to compute story shears, connecting forces, and design forces in shear walls, as well as for many other purposes. Section cut results may be obtained for all types of load cases and combinations."*

### Usos típicos

| Caso de uso | Descripción |
|---|---|
| **Story shear (corte de piso)** | Cortante total en cada nivel de un edificio |
| **Design forces en muros** | Fuerzas de diseño en muros de corte tipo *wall*, *spandrel*, *slab* |
| **Fuerzas de conexión** | Verificar transferencia de carga entre subsistemas |
| **Equilibrio libre de cuerpo** | Comprobar equilibrio en secciones arbitrarias |
| **Revisión de modelos** | Validar que la transferencia de cargas sea correcta |

---

## 2. Concepto de Equilibrio (Free Body Cut)

El programa calcula la resultante sumando algebraicamente las fuerzas internas en los extremos de cada elemento que intersecta el plano de corte. El resultado es expresado en el **sistema de ejes locales del Section Cut**, que el usuario puede orientar libremente.

```
  Elementos a izquierda ──► Plano de corte ◄── Elementos a derecha
                               ↕ F1, F2, F3
                               ↕ M1, M2, M3
                         (resultante en ejes locales)
```

Dependiendo del **tipo de resultado (MyType)**, la convención de nomenclatura de componentes cambia:

| MyType | Tipo | Componentes de fuerza | Componentes de momento |
|---|---|---|---|
| 1 | Analysis | F1, F2, F3 (local 1,2,3) | M1, M2, M3 |
| 2 | Design – Wall | P, V2, V3 | T, M2, M3 |
| 3 | Design – Spandrel | P, V2, V3 | T, M2, M3 |
| 4 | Design – Slab | P, V2, V3 | T, M2, M3 |

> **Nota:** `Analysis` reporta las fuerzas directamente en los ejes locales del corte (F1, F2, F3). Los tipos `Design` usan la convención de marcos (P, V2, V3, T, M2, M3), análoga a `FrameForce`.

---

## 3. Métodos de Definición

Un Section Cut puede definirse de **dos maneras**:

### 3.1 Por Grupo (`SetByGroup`)

El corte queda asociado a un grupo de objetos. La resultante se calcula directamente sobre todos los elementos del grupo, independientemente de su geometría.

```
SapModel.SectCut.SetByGroup(Name, GroupName, MyType)
```

- Requiere que el grupo exista previamente (`GroupDef.SetGroup`).
- El grupo puede marcarse con `SpecifiedForSectionCutDefinition = True` en `GroupDef.SetGroup`.
- Si el número de cuadriláteros es 0, se usa esta modalidad.

### 3.2 Por Cuadrilátero(s) (`SetByQuad` + `AddQuad`)

El plano de corte se define geométricamente mediante uno o más cuadriláteros en el espacio 3D. SAP2000 detecta qué elementos cruzan esos planos y acumula las resultantes.

```
SapModel.SectCut.SetByQuad(Name, GroupName, MyType, X(3), Y(3), Z(3))
SapModel.SectCut.AddQuad(Name, X(3), Y(3), Z(3))
```

- `X(3), Y(3), Z(3)`: Arrays de 4 valores con las coordenadas de los 4 vértices del cuadrilátero.
- Se pueden concatenar múltiples cuadriláteros para cortes no planos o discontinuos.
- El `GroupName` actúa como filtro: solo se consideran elementos del grupo que intersecten el plano.

#### Diferencia clave

| Criterio | Por Grupo | Por Cuadrilátero |
|---|---|---|
| Geometría | No explícita | Planos definidos en coordenadas absolutas |
| Flexibilidad | Rápida para grupos ya definidos | Control total de la geometría del corte |
| Uso típico | Muros, losas por grupos | Cortes oblicuos, Story shears a Z=cte |

---

## 4. Tipos de Resultado (MyType)

### 4.1 Analysis (MyType = 1)

Reporta las componentes en los **ejes locales del Section Cut** (L1, L2, L3). Apropiado para análisis general de equilibrio.

- Los ejes locales se orientan mediante rotaciones secuenciales (Z → Y' → X'') o con "Advanced Local Axes".
- La función de resultado es `SapModel.Results.SectionCutAnalysis(...)`.

### 4.2 Design – Wall (MyType = 2)

Pensado para **muros de corte verticales**. Los resultados se expresan con la convención de diseño de marcos (P, V2, V3, T, M2, M3).

- Eje local **2** = dirección vertical del muro (eje de diseño para momento).
- El ángulo de orientación (`Angle`) va del eje global X al **eje local 2**.
- `Side`: 1 = Top, 2 = Bottom del muro.

### 4.3 Design – Spandrel (MyType = 3)

Para **vigas banda** (spandrels) horizontales en muros o losas.

- Eje local **1** = eje longitudinal del spandrel.
- El ángulo (`Angle`) va del eje global X al **eje local 1**.
- `Side`: 1 = Right, 2 = Left.

### 4.4 Design – Slab (MyType = 4)

Para **losas**. Convención igual a Spandrel.

- `Side`: 1 = Right, 2 = Left.

---

## 5. Orientación de Ejes Locales

### 5.1 Para tipo Analysis

**Rotaciones simples (SetLocalAxesAnalysis):**

```python
# Rotación Z → Y' → X'' (sekuencial, análogo a Euler)
SapModel.SectCut.SetLocalAxesAnalysis(Name, RotZ, RotY_prima, RotX_prima_prima)
```

**Ejes avanzados (SetLocalAxesAdvancedAnalysis):**  
Permite definir el eje 1 y el plano 1-2 mediante:
- Dirección de coordenadas (`AxVectOpt = 1`)
- Dos juntas (`AxVectOpt = 2`)
- Vector usuario (`AxVectOpt = 3`)

```python
MyAxVect = [0.707, 0.707, 0.0]   # eje 1 a 45° en plano XY
MyPlDir  = [2, 3]                  # plano 1-2 definido por +Y, +Z
SapModel.SectCut.SetLocalAxesAdvancedAnalysis(
    Name, True, 3, "Global", MyAxDir, MyAxPt, MyAxVect,
    12, 1, "Global", MyPlDir, MyPlPt, MyPlVect
)
```

### 5.2 Para tipos Design (Wall / Spandrel / Slab)

Un único ángulo en grados:

```python
# Para Wall: ángulo de X global al eje local 2
# Para Spandrel/Slab: ángulo de X global al eje local 1
SapModel.SectCut.SetLocalAxesAngleDesign(Name, Angle_deg)
```

---

## 6. Lado de Resultado (ResultsSide)

Controla desde qué lado de los elementos se obtiene la resultante.

| Tipo | Side = 1 | Side = 2 |
|---|---|---|
| Analysis (quad) | Positivo del eje 3 del cuadrilátero | Negativo del eje 3 |
| Design Wall | Top | Bottom |
| Design Spandrel / Slab | Right | Left |

```python
SapModel.SectCut.SetResultsSide(Name, Side)   # 1 o 2
SapModel.SectCut.GetResultsSide(Name, Side)
```

---

## 7. Ubicación del Resultado (ResultLocation)

Por defecto, los momentos se reportan respecto al centroide automático del corte. Puede especificarse un punto arbitrario:

```python
SapModel.SectCut.SetResultLocation(Name, IsDefault=False, X, Y, Z)
SapModel.SectCut.GetResultLocation(Name, IsDefault, X, Y, Z)
```

Cuando `IsDefault = True`, los argumentos X, Y, Z son ignorados.

---

## 8. API de Definición — Referencia Completa (`SapModel.SectCut`)

| Función API | Descripción | Introduced |
|---|---|---|
| `SetByGroup(Name, GroupName, MyType)` | Crear/reinicializar corte por grupo | v16.0.0 |
| `SetByQuad(Name, GroupName, MyType, X, Y, Z)` | Crear/reinicializar corte por cuadrilátero | v16.0.0 |
| `AddQuad(Name, X, Y, Z)` | Agregar cuadrilátero a corte existente | v16.0.0 |
| `Delete(Name)` | Eliminar corte | v23.4.0 |
| `GetCutInfo(Name, GroupName, MyType, Num)` | Info básica del corte | v16.0.0 |
| `GetNameList(NumberNames, MyName)` | Lista todos los Section Cuts | v16.0.0 |
| `GetQuad(Name, Num, X, Y, Z)` | Obtener coords de cuadrilátero N | v16.0.0 |
| `GetResultLocation(Name, IsDefault, X, Y, Z)` | Punto de reporte de resultados | v16.0.0 |
| `SetResultLocation(Name, IsDefault, X, Y, Z)` | Definir punto de reporte | v16.0.0 |
| `GetResultsSide(Name, Side)` | Obtener lado activo | v16.0.0 |
| `SetResultsSide(Name, Side)` | Definir lado activo | v16.0.0 |
| `GetLocalAxesAnalysis(Name, Z, Y, X, IsAdv)` | Ángulos ejes locales (Analysis) | v16.0.0 |
| `SetLocalAxesAnalysis(Name, Z, Y, X)` | Definir ángulos ejes locales (Analysis) | v16.0.0 |
| `GetLocalAxesAdvancedAnalysis(Name, ...)` | Ejes locales avanzados (Analysis) | v16.0.0 |
| `SetLocalAxesAdvancedAnalysis(Name, ...)` | Definir ejes locales avanzados (Analysis) | v16.0.0 |
| `GetLocalAxesAngleDesign(Name, Angle)` | Ángulo ejes locales (Design) | v16.0.0 |
| `SetLocalAxesAngleDesign(Name, Angle)` | Definir ángulo ejes locales (Design) | v16.0.0 |

---

## 9. API de Resultados — Referencia Completa

### 9.1 `SectionCutAnalysis` — Tipo Analysis

```
SapModel.Results.SectionCutAnalysis(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    F1, F2, F3, M1, M2, M3
)
```

- Solo para cortes con `MyType = 1`.
- Retorna fuerzas en ejes locales del corte: `F1, F2, F3` [F] y `M1, M2, M3` [FL].
- Disponible desde v11.00.

### 9.2 `SectionCutDesign` — Tipos Wall / Spandrel / Slab

```
SapModel.Results.SectionCutDesign(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    P, V2, V3, T, M2, M3
)
```

- Solo para cortes con `MyType = 2, 3 o 4`.
- Convención de diseño de marco: `P` (axial), `V2, V3` (cortantes), `T` (torsión), `M2, M3` (momentos) [F] y [FL].
- Disponible desde v11.00.

### 9.3 Control de Output

```python
# Activar/desactivar un corte específico para output
SapModel.Results.Setup.SetSectionCutSelectedForOutput(Name, Selected)
SapModel.Results.Setup.GetSectionCutSelectedForOutput(Name, Selected)

# Activar/desactivar TODOS los cortes
SapModel.Results.Setup.SelectAllSectionCutsForOutput(Selected)
```

> **Nota:** Por defecto, todos los Section Cuts están **seleccionados para output** al momento de su creación.

### 9.4 Control de Tablas de Base de Datos

```python
# Para visualización en tablas de resultados de análisis
SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay(N, SectionCutList)
SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay(SectionCutList)
```

---

## 10. Ejes Locales — Convención Visual

### Type Analysis

```
      L3 (normal al plano del corte)
       ↑
       │
       │──────► L1
      ╱
    L2

Rotación para llegar a esta orientación:
  1. Rotar RotZ alrededor del eje Z global
  2. Rotar RotY' alrededor del nuevo eje Y'
  3. Rotar RotX'' alrededor del nuevo eje X''
```

### Type Wall (MyType=2)

```
  Muro                ↑ L2 (vertical, eje de momento)
  │──────────────│    │
  │              │    └────── desde X global rotado por Angle
  │──────────────│
  L3 (normal al muro, hacia fuera)
```

### Type Spandrel / Slab (MyType=3,4)

```
  ════════════════════  L1 (longitudinal, eje de diseño)
                         └── desde X global rotado por Angle
```

---

## 11. Interacción con Grupos (GroupDef)

Los grupos pueden marcarse para usarse en definición de Section Cuts:

```python
SapModel.GroupDef.SetGroup(
    "MiGrupo",
    ...,
    SpecifiedForSectionCutDefinition=True,
    ...
)
```

Al recuperar información de un grupo:
```python
SapModel.GroupDef.GetGroup("MiGrupo", ..., SpecifiedForSectionCutDefinition, ...)
```

---

## 12. Workflow Típico de Implementación (Python / API)

```python
# ─── 1. CREAR GRUPO Y ASIGNAR OBJETOS ───────────────────────────────────────
ret = SapModel.GroupDef.SetGroup("Muro_P1")
# Asignar shell objects al grupo
ret = SapModel.AreaObj.SetGroupAssign("1", "Muro_P1")
ret = SapModel.AreaObj.SetGroupAssign("2", "Muro_P1")
ret = SapModel.AreaObj.SetGroupAssign("3", "Muro_P1")

# ─── 2A. DEFINIR SECTION CUT POR GRUPO ──────────────────────────────────────
ret = SapModel.SectCut.SetByGroup("SCut_Muro", "Muro_P1", 2)  # Design Wall

# ─── 2B. DEFINIR SECTION CUT POR CUADRILÁTERO ───────────────────────────────
X = [-500.0, 500.0, 500.0, -500.0]
Y = [10.0, 10.0, -10.0, -10.0]
Z = [300.0, 300.0, 300.0, 300.0]
ret = SapModel.SectCut.SetByQuad("SCut_Nivel3", "TodosLosElementos", 1, X, Y, Z)

# ─── 3. CONFIGURAR EJES LOCALES ─────────────────────────────────────────────
# Para Wall:  ángulo del eje local 2 con respecto a X global
ret = SapModel.SectCut.SetLocalAxesAngleDesign("SCut_Muro", 90.0)

# Para Analysis: rotaciones Z, Y', X''
ret = SapModel.SectCut.SetLocalAxesAnalysis("SCut_Nivel3", 0.0, 0.0, 0.0)

# ─── 4. CONFIGURAR LADO Y UBICACIÓN ─────────────────────────────────────────
ret = SapModel.SectCut.SetResultsSide("SCut_Muro", 1)   # Top para Wall
ret = SapModel.SectCut.SetResultLocation("SCut_Muro", True)  # Usar default

# ─── 5. ANÁLISIS ─────────────────────────────────────────────────────────────
ret = SapModel.File.Save(r"C:\modelo.sdb")
ret = SapModel.Analyze.RunAnalysis()

# ─── 6. CONFIGURAR OUTPUT ────────────────────────────────────────────────────
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
ret = SapModel.Results.Setup.SelectAllSectionCutsForOutput(True)

# ─── 7A. OBTENER RESULTADOS TIPO ANALYSIS ────────────────────────────────────
NumberResults = 0
SCut = []
LoadCase = []
StepType = []
StepNum = []
F1 = []
F2 = []
F3 = []
M1 = []
M2 = []
M3 = []

ret = SapModel.Results.SectionCutAnalysis(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    F1, F2, F3, M1, M2, M3
)
# ret[0] == 0 → éxito; ret[1] = NumberResults

# ─── 7B. OBTENER RESULTADOS TIPO DESIGN ──────────────────────────────────────
P = []; V2 = []; V3 = []; T = []; M2_d = []; M3_d = []
ret = SapModel.Results.SectionCutDesign(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    P, V2, V3, T, M2_d, M3_d
)
```

---

## 13. Firmas VBA Completas (Reference)

### Definición

```vba
' Por grupo
Function SetByGroup(ByVal Name As String, ByVal GroupName As String, ByVal MyType As Long) As Long

' Por cuadrilátero
Function SetByQuad(ByVal Name As String, ByVal GroupName As String, ByVal MyType As Long,
                   ByRef X() As Double, ByRef Y() As Double, ByRef Z() As Double) As Long

' Agregar cuadrilátero
Function AddQuad(ByVal Name As String, ByRef X() As Double, ByRef Y() As Double, ByRef Z() As Double) As Long

' Eliminar
Function Delete(ByVal Name As String) As Long

' Info del corte
Function GetCutInfo(ByVal Name As String, ByRef GroupName As String, ByRef MyType As Long,
                    ByRef Num As Long) As Long

' Lista de nombres
Function GetNameList(ByRef NumberNames As Long, ByRef MyName() As String) As Long

' Ejes locales Analysis
Function SetLocalAxesAnalysis(ByVal Name As String, ByVal Z As Double, ByVal Y As Double, ByVal X As Double) As Long
Function GetLocalAxesAnalysis(ByVal Name As String, ByRef Z As Double, ByRef Y As Double,
                               ByRef X As Double, ByRef IsAdvanced As Boolean) As Long

' Ejes locales Design
Function SetLocalAxesAngleDesign(ByVal Name As String, ByVal Angle As Double) As Long
Function GetLocalAxesAngleDesign(ByVal Name As String, ByRef Angle As Double) As Long

' Lado de resultado
Function SetResultsSide(ByVal Name As String, ByVal Side As Long) As Long
Function GetResultsSide(ByVal Name As String, ByRef Side As Long) As Long

' Ubicación de resultado
Function SetResultLocation(ByVal Name As String, ByVal IsDefault As Boolean,
                            Optional ByVal X As Double = 0, Optional ByVal Y As Double = 0,
                            Optional ByVal Z As Double = 0) As Long
Function GetResultLocation(ByVal Name As String, ByRef IsDefault As Boolean,
                            ByRef X As Double, ByRef Y As Double, ByRef Z As Double) As Long
```

### Resultados

```vba
' Analysis
Function SectionCutAnalysis(ByRef NumberResults As Long, ByRef SCut() As String, ByRef LoadCase() As String,
    ByRef StepType() As String, ByRef StepNum() As Double,
    ByRef F1() As Double, ByRef F2() As Double, ByRef F3() As Double,
    ByRef M1() As Double, ByRef M2() As Double, ByRef M3() As Double) As Long

' Design
Function SectionCutDesign(ByRef NumberResults As Long, ByRef SCut() As String, ByRef LoadCase() As String,
    ByRef StepType() As String, ByRef StepNum() As Double,
    ByRef P() As Double, ByRef V2() As Double, ByRef V3() As Double,
    ByRef T() As Double, ByRef M2() As Double, ByRef M3() As Double) As Long

' Control de output
Function SetSectionCutSelectedForOutput(ByVal Name As String, ByVal Selected As Boolean) As Long
Function GetSectionCutSelectedForOutput(ByVal Name As String, ByRef Selected As Boolean) As Long
Function SelectAllSectionCutsForOutput(Selected As Boolean) As Long

' Tablas de base de datos
Function GetSectionCutsSelectedForDisplay(ByRef NumberSelectedSectionCuts As Integer,
    ByRef SectionCutList() As String) As Integer
Function SetSectionCutsSelectedForDisplay(ByRef SectionCutList() As String) As Integer
```

---

## 14. Consideraciones de Implementación en Python (COM Bridge)

### Pattern ByRef en Python

Las firmas Python con COM bridge difieren de VBA en cómo se manejan los parámetros `ByRef`. El patrón general para `SectionCutAnalysis` es:

```python
# Inicializar variables ByRef
NumberResults = int()
SCut = []
LoadCase = []
StepType = []
StepNum = []
F1 = []; F2 = []; F3 = []
M1 = []; M2 = []; M3 = []

[ret, NumberResults, SCut, LoadCase, StepType, StepNum,
 F1, F2, F3, M1, M2, M3] = SapModel.Results.SectionCutAnalysis(
    NumberResults, SCut, LoadCase, StepType, StepNum,
    F1, F2, F3, M1, M2, M3
)
```

### SetByQuad — Arrays de 4 puntos

```python
import comtypes  # disponible en sandbox sin import explícito

X = [float(x) for x in [-500, 500, 500, -500]]
Y = [float(y) for y in [5, 5, -5, -5]]
Z = [float(z) for z in [300, 300, 300, 300]]

ret = SapModel.SectCut.SetByQuad("SCut1", "Group1", 1, X, Y, Z)
```

### Verificación típica

```python
if ret == 0:
    print(f"Section cut 'SCut1' creado correctamente")
else:
    print(f"Error al crear section cut: ret={ret}")
```

---

## 15. Casos de Uso Avanzados

### 15.1 Story Shear por pisos (cortante de piso)

Definir un plano horizontal a la cota Z de cada piso:

```python
pisos = {"P01": 300, "P02": 600, "P03": 900}  # nombre: Z en cm
for nombre, z in pisos.items():
    X = [-5000, 5000, 5000, -5000]
    Y = [5000, 5000, -5000, -5000]
    Z_arr = [z, z, z, z]
    SapModel.SectCut.SetByQuad(f"Story_{nombre}", "ALL", 1, X, Y, Z_arr)
    SapModel.SectCut.SetLocalAxesAnalysis(f"Story_{nombre}", 0, 0, 0)
```

### 15.2 Fuerzas de diseño en muro

```python
# Grupo del muro ya definido
SapModel.SectCut.SetByGroup("SCut_MuroA", "MURO_A", 2)  # Design Wall
SapModel.SectCut.SetLocalAxesAngleDesign("SCut_MuroA", 0.0)    # Muro paralelo a X
SapModel.SectCut.SetResultsSide("SCut_MuroA", 1)               # Top
```

### 15.3 Corte oblicuo con múltiples cuadriláteros

```python
# Plano inclinado con dos cuadriláteros adyacentes
X1 = [0, 200, 200, 0]
Y1 = [10, 10, -10, -10]
Z1 = [0, 0, 300, 300]
SapModel.SectCut.SetByQuad("SCut_Inclinado", "Estructura", 1, X1, Y1, Z1)

X2 = [200, 400, 400, 200]
Y2 = [10, 10, -10, -10]
Z2 = [300, 300, 600, 600]
SapModel.SectCut.AddQuad("SCut_Inclinado", X2, Y2, Z2)
```

---

## 16. Resumen de Enumeraciones

```
MyType (tipo de resultado):
  1 → Analysis      (F1, F2, F3, M1, M2, M3 en ejes locales del corte)
  2 → Design Wall   (P, V2, V3, T, M2, M3 convención de marco)
  3 → Design Spandrel
  4 → Design Slab

Side (lado de resultado):
  Analysis: 1=Positivo eje-3 quad  | 2=Negativo eje-3 quad
  Wall:      1=Top                  | 2=Bottom
  Spandrel/Slab: 1=Right            | 2=Left

AxVectOpt / PlVectOpt (ejes avanzados):
  1 → Coordinate direction
  2 → Two joints
  3 → User vector

Plane2 (plano de los ejes avanzados):
  12, 13, 21, 23, 31, 32
```

---

## 17. Notas y Advertencias

> ⚠️ **Default output activo:** Al crear un Section Cut, queda habilitado por defecto para output. Si se tienen muchos cortes, filtrar explícitamente con `SetSectionCutSelectedForOutput`.

> ⚠️ **Reinicialización:** Si se llama `SetByGroup` o `SetByQuad` con un nombre que ya existe, **todos los datos anteriores se pierden** y el corte se reinicializa completamente.

> ⚠️ **Tipo de resultado vs función de resultado:** `SectionCutAnalysis` solo retorna datos para cortes con `MyType=1`. `SectionCutDesign` solo retorna datos para `MyType=2,3,4`. Si se mezclan tipos, los resultados de un tipo no aparecen en la función del otro.

> ⚠️ **Unidades:** Las fuerzas están en [F] y los momentos en [FL], donde el sistema de unidades es el activo en el modelo al momento de correr el análisis.

> ℹ️ **Version mínima:** La mayoría de funciones `SectCut` fueron introducidas en v16.0.0. La función `Delete` requiere v23.4.0. Las funciones de output (`Setup`) requieren v16.0.2.

---

## 18. Referencias

| Recurso | Ubicación |
|---|---|
| API Definitions | `API/Definitions.md` → sección `SectCut` |
| API Analysis Results | `API/Analysis_Results.md` → `SectionCutAnalysis`, `SectionCutDesign` |
| API Database Tables | `API/Database_Tables.md` → `GetSectionCutsSelectedForDisplay` |
| CSI Features | https://www.csiamerica.com/products/sap2000/features (sección Output and Display) |
