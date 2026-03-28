# Expansión del Registry de Funciones Verificadas

**Branch:** `expand-verified-registry`
**Description:** Agregar ~33 funciones SAP2000 de alto valor al registry verificado, cubriendo los gaps más críticos para modelamiento estructural diario.

## Goal

El registry actual tiene 97 funciones verificadas, pero faltan operaciones clave para workflows completos de modelamiento: asignación de cargas a frames/áreas, releases de momento, grupos, diafragmas, links lineales, y extracción ampliada de resultados (incluyendo modal completo). Este plan agrega funciones priorizadas por frecuencia de uso real, llevando la cobertura de ~32% a ~44% de la API documentada.

## Decisiones de Alcance

| # | Pregunta | Respuesta |
|---|----------|-----------|
| 1 | Links | ✅ Solo nivel **lineal** (conexiones simples y contacto entre elementos) — sin aisladores ni no-lineal |
| 2 | Resultados | ✅ Las 4 propuestas **+ suite completa de análisis modal** (período, masa participante, formas modales) |
| 3 | File templates | ❌ No — omitir `New2DFrame`, `New3DFrame`, `NewWall` |
| 4 | Ejecución | ✅ **Wrapper por wrapper** — un script a la vez, verificación incremental |

## Análisis del Estado Actual

| Categoría | Registradas | Gaps Críticos |
|-----------|-------------|---------------|
| Cargas en objetos | 2 parciales (`SetLoadDistributed`, `SetLoadForce` en registry pero SIN wrapper) | `AreaObj.SetLoadUniform`, `AreaObj.SetLoadGravity`, `FrameObj.SetLoadPoint` |
| Releases / conexiones | 0 | `FrameObj.SetReleases`, `FrameObj.GetReleases` |
| Grupos | 0 | `GroupDef.SetGroup_2`, `GroupDef.GetAssignments` |
| Links lineales | 0 | `LinkObj.AddByPoint`, `LinkObj.AddByCoord`, `PropLink.SetLinear` |
| Constraints avanzados | 1 (`SetBody`) | `ConstraintDef.SetDiaphragm` |
| Resultados — general | 4 | `Results.BaseReact`, `Results.AreaStressShell` |
| Resultados — modal | 0 | `Results.ModalPeriod`, `Results.ModalParticipatingMassRatios`, `Results.ModeShape` |
| Modelo / Análisis | 2 | `Analyze.SetActiveDOF`, `Analyze.GetActiveDOF`, `Analyze.GetCaseStatus` |
| Propiedades de área (query) | 0 | `PropArea.GetShell_1`, `AreaObj.SetProperty` |

## Implementation Steps

---

### Step 1: Cargas en Objetos — Core Loading (6 wrappers)
**Files:**
- `scripts/wrappers/func_FrameObj_SetLoadDistributed.py` (wrapper nuevo — ya está en registry pero sin wrapper dedicado)
- `scripts/wrappers/func_FrameObj_SetLoadPoint.py` (nuevo)
- `scripts/wrappers/func_FrameObj_GetLoadDistributed.py` (nuevo)
- `scripts/wrappers/func_PointObj_SetLoadForce.py` (wrapper nuevo — ya está en registry pero sin wrapper dedicado)
- `scripts/wrappers/func_AreaObj_SetLoadUniform.py` (nuevo)
- `scripts/wrappers/func_AreaObj_SetLoadGravity.py` (nuevo)
- `scripts/registry.json` (actualizar con las 4 funciones nuevas + actualizar 2 existentes)

**What:** Crear wrappers verificados para las 6 funciones de asignación de carga más usadas. Dos ya existen en el registry (`SetLoadDistributed`, `SetLoadForce`) pero no tienen wrapper dedicado. Cuatro son completamente nuevas.

**Funciones objetivo:**
| Función | Estado actual | Prioridad |
|---------|---------------|-----------|
| `FrameObj.SetLoadDistributed` | En registry, sin wrapper | ALTA |
| `FrameObj.SetLoadPoint` | No registrada | ALTA |
| `FrameObj.GetLoadDistributed` | No registrada | MEDIA |
| `PointObj.SetLoadForce` | En registry, sin wrapper | ALTA |
| `AreaObj.SetLoadUniform` | No registrada | ALTA |
| `AreaObj.SetLoadGravity` | No registrada | ALTA |

**Testing:** Ejecutar cada wrapper via `run_sap_script`. Verificar ret_code == 0 y que las cargas asignadas se reflejen en el modelo (query back o count).

---

### Step 2: Releases y Propiedades de Frame Avanzadas (4 wrappers)
**Files:**
- `scripts/wrappers/func_FrameObj_SetReleases.py` (nuevo)
- `scripts/wrappers/func_FrameObj_GetReleases.py` (nuevo)
- `scripts/wrappers/func_FrameObj_SetInsertionPoint.py` (nuevo)
- `scripts/wrappers/func_FrameObj_SetLocalAxes.py` (nuevo)
- `scripts/registry.json`

**What:** Agregar releases de momento (articulaciones) y propiedades geométricas avanzadas de frames. `SetReleases` es esencial para modelar conexiones reales (vigas articuladas, rótulas plásticas). `SetInsertionPoint` para offsets de sección. `SetLocalAxes` para orientación de secciones no estándar.

**Funciones objetivo:**
| Función | Uso | Prioridad |
|---------|-----|-----------|
| `FrameObj.SetReleases` | Articulaciones en extremos de vigas | ALTA |
| `FrameObj.GetReleases` | Verificar releases asignados | MEDIA |
| `FrameObj.SetInsertionPoint` | Offsets Top/Bottom/Left/Right | MEDIA |
| `FrameObj.SetLocalAxes` | Rotación de ejes locales | MEDIA |

**Testing:** Crear frame → asignar releases → query GetReleases → comparar arrays booleanos [True, True, True, False, False, False].

---

### Step 3: Grupos y Asignaciones Masivas (4 wrappers)
**Files:**
- `scripts/wrappers/func_GroupDef_SetGroup_2.py` (nuevo)
- `scripts/wrappers/func_GroupDef_GetNameList.py` (nuevo)
- `scripts/wrappers/func_FrameObj_SetGroupAssign.py` (nuevo)
- `scripts/wrappers/func_AreaObj_SetGroupAssign.py` (nuevo)
- `scripts/registry.json`

**What:** Los grupos son fundamentales para organización del modelo, batch operations, y diseño por grupos. Sin grupos no se pueden asignar diseños selectivos ni extraer resultados filtrados.

**Funciones objetivo:**
| Función | Uso | Prioridad |
|---------|-----|-----------|
| `GroupDef.SetGroup_2` | Crear/definir grupo con propiedades | ALTA |
| `GroupDef.GetNameList` | Listar grupos existentes | MEDIA |
| `FrameObj.SetGroupAssign` | Asignar frames a grupo | ALTA |
| `AreaObj.SetGroupAssign` | Asignar áreas a grupo | ALTA |

**Testing:** Crear grupo → asignar frames → verificar con GetNameList y conteo de elementos en grupo.

---

### Step 4: Constraints Avanzados — Diafragma (2 wrappers)
**Files:**
- `scripts/wrappers/func_ConstraintDef_SetDiaphragm.py` (nuevo)
- `scripts/wrappers/func_ConstraintDef_GetDiaphragm.py` (nuevo)
- `scripts/registry.json`

**What:** El diafragma rígido es el constraint más usado en edificios (losas rígidas). Sin esta función es imposible automatizar modelos multi-piso correctamente.

**Funciones objetivo:**
| Función | Uso | Prioridad |
|---------|-----|-----------|
| `ConstraintDef.SetDiaphragm` | Definir diafragma rígido por piso | ALTA |
| `ConstraintDef.GetDiaphragm` | Verificar tipo diafragma | MEDIA |

**Testing:** Crear diafragma → asignar a puntos de un piso → query back → verificar axis y DOFs.

---

### Step 5a: Resultados Generales (2 wrappers)
**Files:**
- `scripts/wrappers/func_Results_BaseReact.py` (nuevo)
- `scripts/wrappers/func_Results_AreaStressShell.py` (nuevo)
- `scripts/registry.json`

**What:** Reacciones globales de base (esencial para verificación de equilibrio) y esfuerzos en elementos área (losas y muros de corte).

**Funciones objetivo:**
| Función | Uso | Prioridad |
|---------|-----|----------|
| `Results.BaseReact` | Reacciones globales FX, FY, FZ en la base del modelo | ALTA |
| `Results.AreaStressShell` | Esfuerzos S11, S22, S12 en elementos shell/losa | ALTA |

**Testing:** Crear modelo con cargas → ejecutar análisis → extraer BaseReact → verificar suma FZ = carga total aplicada. AreaStressShell: extraer esfuerzos de losa → arrays no vacíos, ret_code == 0.

---

### Step 5b: Suite de Resultados Modales (3 wrappers)
**Files:**
- `scripts/wrappers/func_Results_ModalPeriod.py` (nuevo)
- `scripts/wrappers/func_Results_ModalParticipatingMassRatios.py` (nuevo)
- `scripts/wrappers/func_Results_ModeShape.py` (nuevo)
- `scripts/registry.json`

**What:** Suite completa para análisis dinámico modal. `ModalPeriod` extrae períodos y frecuencias por modo. `ModalParticipatingMassRatios` verifica que se capture ≥90% de masa modal (requisito ASCE/NSR). `ModeShape` extrae vectores propios (desplazamientos modales por punto).

**Funciones objetivo:**
| Función | Uso | Notas |
|---------|-----|-------|
| `Results.ModalPeriod` | Período T[i] y frecuencia f[i] por modo | Requiere caso modal activo en output |
| `Results.ModalParticipatingMassRatios` | Masa participante UX, UY, UZ por modo (%) | Crítico para verificación NSR/ASCE |
| `Results.ModeShape` | Desplazamiento modal U1,U2,U3,R1,R2,R3 por punto por modo | Array grande — filtrar por punto o modo |

**Prerequisito del modelo:** Requiere un `LoadCase` de tipo Modal con `Analyze.RunAnalysis()` exitoso.

**Testing:** Configurar caso modal mínimo (EigenVector, 6 modos) → RunAnalysis → ModalPeriod → verificar T[0] > 0. ModalParticipatingMassRatios → suma acumulada UX+UY > 0.9 en modo 6+. ModeShape → ret_code == 0, arrays con dimensiones correctas.

---

### Step 6: Análisis y Control de Modelo (4 wrappers)
**Files:**
- `scripts/wrappers/func_Analyze_SetActiveDOF.py` (nuevo)
- `scripts/wrappers/func_Analyze_GetActiveDOF.py` (nuevo)
- `scripts/wrappers/func_Analyze_GetCaseStatus.py` (nuevo)
- `scripts/wrappers/func_File_OpenFile.py` (wrapper ya existe — verificar/actualizar en registry si falta)
- `scripts/registry.json`

**What:** Control de DOFs activos (esencial para modelos 2D vs 3D) y estado de casos de análisis (para verificar si un caso ya fue resuelto).

**Funciones objetivo:**
| Función | Uso | Prioridad |
|---------|-----|-----------|
| `Analyze.SetActiveDOF` | Activar/desactivar DOFs (UX,UY,UZ,RX,RY,RZ) | ALTA |
| `Analyze.GetActiveDOF` | Query DOFs activos | MEDIA |
| `Analyze.GetCaseStatus` | Verificar si caso ya corrió | MEDIA |
| `File.OpenFile` | Abrir modelo existente | MEDIA |

**Testing:** SetActiveDOF([True,True,True,True,True,True]) → GetActiveDOF → comparar. GetCaseStatus antes/después de RunAnalysis.

---

### Step 7: Links Lineales y Propiedades Área (5 wrappers)
**Files:**
- `scripts/wrappers/func_PropLink_SetLinear.py` (nuevo)
- `scripts/wrappers/func_LinkObj_AddByPoint.py` (nuevo)
- `scripts/wrappers/func_LinkObj_AddByCoord.py` (nuevo)
- `scripts/wrappers/func_AreaObj_SetProperty.py` (nuevo)
- `scripts/wrappers/func_PropArea_GetShell_1.py` (nuevo)
- `scripts/registry.json`

**What:** Links **exclusivamente lineales** para modelar conexiones simples entre elementos: apoyos elásticos, conectores rígidos/flexibles, modelado de contacto simplificado. `PropLink.SetLinear` define las 6 rigideces del link (U1,U2,U3,R1,R2,R3). `AddByPoint` y `AddByCoord` son las dos formas de crear el elemento. Las funciones de área completan el ciclo Set/Get de propiedades shell.

**Alcance excluido:** propiedades no-lineales (`SetMultiLinearElastic`, `SetPlastic`, `SetFrictionPendulum`, `SetDamper`), aisladores sísmicos — quedan fuera de este plan.

**Funciones objetivo:**
| Función | Uso | Notas |
|---------|-----|-------|
| `PropLink.SetLinear` | Definir rigidez lineal (stiffness: U1..R3) | Definir ANTES de crear el elemento |
| `LinkObj.AddByPoint` | Crear link uniendo 2 puntos existentes | Retorna `[Name_out, ret_code]` |
| `LinkObj.AddByCoord` | Crear link por coordenadas (crea puntos automáticamente) | Retorna `[Name_out, ret_code]` |
| `AreaObj.SetProperty` | Reasignar sección a área ya creada | Análogo a `FrameObj.SetSection` |
| `PropArea.GetShell_1` | Leer propiedades de una sección shell | ByRef: `[ShellType, ..., ret_code]` |

**Testing paso a paso:**
1. `PropLink.SetLinear` → ret_code == 0
2. `LinkObj.AddByPoint` con 2 puntos existentes → `Name_out` asignado, count += 1
3. `LinkObj.AddByCoord` por coordenadas → count += 1
4. `AreaObj.SetProperty` en área existente → GetProperty confirma cambio
5. `PropArea.GetShell_1` en sección conocida → ShellType == valor definido en SetShell_1

---

## Resumen Cuantitativo

| Métrica | Actual | Post-Plan |
|---------|--------|-----------|
| Funciones en registry | 97 | ~130 |
| Wrappers verificados | ~50 | ~83 |
| Cobertura de workflows diarios | ~60% | ~90% |
| Categorías cubiertas | 12 | 17 |

**Total de wrappers nuevos:** 33 (28 completamente nuevos + 2 ya en registry sin wrapper + 3 suite modal)

## Orden de Ejecución

> Ejecución: **wrapper por wrapper** — un script a la vez con verificación incremental antes de avanzar.

```
Step 1 (Cargas)          ████████████  6 wrappers  ← Mayor impacto inmediato
Step 2 (Releases)        ████████      4 wrappers  ← Completa modelado frame
Step 3 (Grupos)          ████████      4 wrappers  ← Habilita batch ops
Step 4 (Diafragmas)      ██████        2 wrappers  ← Edificios multi-piso
Step 5a (Resultados)     ████████      2 wrappers  ← BaseReact + AreaStress
Step 5b (Modal)          ████████████  3 wrappers  ← Suite modal completa
Step 6 (Análisis/DOF)    ██████        4 wrappers  ← Control de modelo
Step 7 (Links lineales)  ██████        5 wrappers  ← Conexiones simples
```

## Criterios de Verificación (por wrapper)

Cada wrapper se considera **verificado** cuando:
1. `ret_code == 0` al ejecutar la función
2. Query de confirmación (Get/Count) devuelve el valor esperado
3. `register_verified_function` ejecutado con metadatos completos
4. `wrapper_script` apuntando al archivo `.py` correcto en el registry
