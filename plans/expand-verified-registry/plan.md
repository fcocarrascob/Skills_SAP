# Expansión del Registry Verificado de Funciones SAP2000

**Branch:** `expand-verified-registry`
**Description:** Ampliar la base de datos verificada (registry.json + wrappers) con funciones API esenciales para modelamiento estructural del día a día

## Goal
El registry actual cubre ~133 funciones verificadas con buena cobertura en geometría, cargas y resultados, pero tiene gaps significativos en: propiedades de diseño de materiales, tipos de secciones, gestión de combinaciones, configuración de diseño, fuentes de masa y funciones administrativas (rename/delete/count). Este plan agrega ~45 funciones priorizadas por su utilidad práctica en workflows de ingeniería cotidianos.

## Estado Actual

| Categoría | Funciones en Registry | Gaps Identificados |
|---|---|---|
| PropMaterial | 3 (Set básicos) | SetOSteel_1, SetOConcrete_1, GetMaterial, GetMPIsotropic, ChangeName, Delete, Count |
| PropFrame | 4 (Rect, Circle, I, Tube) | SetAngle, SetChannel, SetPipe, GetRectangle, GetCircle, ChangeName, Delete, Count |
| PropArea | 2 (SetShell_1, GetNameList) | GetShell_1, SetModifiers, GetModifiers, ChangeName, Delete, Count |
| Design | 2 (StartDesign x2) | Set/GetComboStrength, Set/GetComboDeflection, Get/SetCode, DeleteResults, GetComboAutoGenerate |
| RespCombo | 4 (Add, GetNameList, Set/GetCaseList) | Delete, ChangeName, Count, SetTypeOAPI, GetTypeOAPI, DeleteCase, AddDesignDefaultCombos |
| LoadCases | 3 (RS + GetNameList) | SetDampConstant, Count, Delete, ChangeName, SetInitialCase |
| LoadPatterns | 3 (Add, GetNameList, SetSelfWT) | Count, Delete, ChangeName |
| SourceMass | 0 | SetMassSource, GetMassSource, GetDefault, Count, Delete, ChangeName |
| ConstraintDef | 3 (Body, Diaphragm) | SetBeam, SetPlate, SetEqual, Count, Delete, ChangeName, GetNameList |
| FrameObj modifiers | 0 | SetModifiers, GetModifiers |
| AreaObj | básicos | SetProperty (asignar sección a área existente) |

## Implementation Steps

### Step 1: Material Design Properties (Tier 1 — Producción)
**Files:** `scripts/wrappers/func_PropMaterial_SetOSteel_1.py`, `func_PropMaterial_SetOConcrete_1.py`, `func_PropMaterial_GetMaterial.py`, `func_PropMaterial_GetMPIsotropic.py`, `scripts/registry.json`
**What:** Agregar wrappers para las funciones de propiedades de diseño de materiales. `SetOSteel_1` y `SetOConcrete_1` ya se usan en `scripts/modelo_base/backend_modelo_base.py` pero no están verificadas ni registradas. Incluir también los getters correspondientes para ciclo completo Set→Get→Verify.
**Funciones:**
- `SapModel.PropMaterial.SetOSteel_1(Name, Fy, Fu, EFy, EFu, SSType, SSHysType, StrainAtHardening, StrainAtMaxStress, StrainAtRupture, FinalSlope)` → ret_code
- `SapModel.PropMaterial.SetOConcrete_1(Name, fc, IsLightweight, FcsFactor, SSType, SSHysType, StrainAtfc, StrainUltimate, FinalSlope, FAngle, DAngle)` → ret_code
- `SapModel.PropMaterial.GetMaterial(Name)` → [MatType, Color, Notes, GUID, ret_code]
- `SapModel.PropMaterial.GetMPIsotropic(Name)` → [E, poisson, thermal, tempDep, ret_code]
**Testing:** Crear material acero/concreto con SetMaterial + SetOSteel_1/SetOConcrete_1, verificar con GetMaterial que existe. Registrar en registry.json con firma verificada.

---

### Step 2: Section Property Getters + Nuevos Tipos (Tier 1)
**Files:** `scripts/wrappers/func_PropFrame_SetAngle.py`, `func_PropFrame_SetChannel.py`, `func_PropFrame_SetPipe.py`, `func_PropFrame_GetRectangle.py`, `func_PropFrame_GetCircle.py`, `func_PropFrame_GetISection.py`, `scripts/registry.json`
**What:** Completar la familia de secciones frame con ángulos (L), canales (C) y tubos circulares (Pipe), más los getters de las secciones ya existentes. `SetAngle` y `SetChannel` se usan en modelo_base pero sin wrapper.
**Funciones:**
- `SapModel.PropFrame.SetAngle(Name, MatProp, T3, T2, TF, TW, ...)` → ret_code
- `SapModel.PropFrame.SetChannel(Name, MatProp, T3, T2, TF, TW, ...)` → ret_code
- `SapModel.PropFrame.SetPipe(Name, MatProp, T3, TW)` → ret_code
- `SapModel.PropFrame.GetRectangle(Name)` → [FileName, MatProp, T3, T2, Color, Notes, GUID, ret_code]
- `SapModel.PropFrame.GetCircle(Name)` → [FileName, MatProp, T3, Color, Notes, GUID, ret_code]
- `SapModel.PropFrame.GetISection(Name)` → [FileName, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID, ret_code]
**Testing:** Crear sección → Get → verificar parámetros coinciden. Ejecutar vía MCP y confirmar ret_code=0.

---

### Step 3: Design Workflow Functions (Tier 1 — Producción)
**Files:** `scripts/wrappers/func_DesignSteel_SetComboStrength.py`, `func_DesignSteel_GetComboStrength.py`, `func_DesignSteel_SetComboDeflection.py`, `func_DesignSteel_GetCode.py`, `func_DesignSteel_SetCode.py`, `func_DesignConcrete_SetComboStrength.py`, `func_DesignConcrete_GetCode.py`, `func_DesignConcrete_SetCode.py`, `scripts/registry.json`
**What:** Registrar funciones de diseño que permiten asignar combinaciones de resistencia/deflexión y configurar código de diseño. Esenciales para workflows de diseño automatizado. `SetComboStrength` ya se usa en modelo_base.
**Funciones:**
- `SapModel.DesignSteel.SetComboStrength(Name, Selected)` → ret_code
- `SapModel.DesignSteel.GetComboStrength()` → [NumberItems, MyName[], ret_code]
- `SapModel.DesignSteel.SetComboDeflection(Name, Selected)` → ret_code
- `SapModel.DesignSteel.GetCode()` → [CodeName, ret_code]
- `SapModel.DesignSteel.SetCode(CodeName)` → ret_code
- `SapModel.DesignSteel.DeleteResults()` → ret_code
- `SapModel.DesignConcrete.SetComboStrength(Name, Selected)` → ret_code
- `SapModel.DesignConcrete.GetCode()` → [CodeName, ret_code]
- `SapModel.DesignConcrete.SetCode(CodeName)` → ret_code
**Testing:** Crear modelo con frame template → agregar combos → SetComboStrength → GetComboStrength → verificar lista. SetCode → GetCode → verificar match.

---

### Step 4: Combo Management Completo (Tier 1)
**Files:** `scripts/wrappers/func_RespCombo_Delete.py`, `func_RespCombo_ChangeName.py`, `func_RespCombo_Count.py`, `func_RespCombo_SetTypeOAPI.py`, `func_RespCombo_GetTypeOAPI.py`, `func_RespCombo_DeleteCase.py`, `func_RespCombo_AddDesignDefaultCombos.py`, `scripts/registry.json`
**What:** Completar el CRUD de combinaciones. `SetTypeOAPI`, `GetTypeOAPI` y `DeleteCase` ya se usan en `scripts/comb_cargas/combos_backend.py` sin estar registrados. `Delete` y `ChangeName` son operaciones administrativas esenciales.
**Funciones:**
- `SapModel.RespCombo.Delete(Name)` → ret_code
- `SapModel.RespCombo.ChangeName(Name, NewName)` → ret_code
- `SapModel.RespCombo.Count()` → count (directo)
- `SapModel.RespCombo.SetTypeOAPI(Name, ComboType)` → ret_code
- `SapModel.RespCombo.GetTypeOAPI(Name)` → [ComboType, ret_code]
- `SapModel.RespCombo.DeleteCase(Name, CType, CName)` → ret_code
- `SapModel.RespCombo.AddDesignDefaultCombos(DesignSteel, DesignConcrete, DesignAluminum, DesignColdFormed)` → ret_code (usar con `DesignSteel=True, DesignConcrete=True, DesignAluminum=False, DesignColdFormed=False`)
**Testing:** Add → Count → ChangeName → GetNameList verify → SetTypeOAPI → GetTypeOAPI verify → DeleteCase → Delete → Count verify.

---

### Step 5: LoadCases & LoadPatterns Admin (Tier 2)
**Files:** `scripts/wrappers/func_LoadCases_ResponseSpectrum_SetDampConstant.py`, `func_LoadCases_Count.py`, `func_LoadCases_Delete.py`, `func_LoadCases_ChangeName.py`, `func_LoadPatterns_Count.py`, `func_LoadPatterns_Delete.py`, `func_LoadPatterns_ChangeName.py`, `scripts/registry.json`
**What:** Completar funciones administrativas de load cases y patterns. `SetDampConstant` se usa en modelo_base para definir amortiguamiento en response spectrum.
**Funciones:**
- `SapModel.LoadCases.ResponseSpectrum.SetDampConstant(Name, Damp)` → ret_code
- `SapModel.LoadCases.Count(CaseType)` → count
- `SapModel.LoadCases.Delete(Name)` → ret_code
- `SapModel.LoadCases.ChangeName(Name, NewName)` → ret_code
- `SapModel.LoadPatterns.Count()` → count
- `SapModel.LoadPatterns.Delete(Name)` → ret_code
- `SapModel.LoadPatterns.ChangeName(Name, NewName)` → ret_code
**Testing:** Crear patterns/cases → Count → ChangeName → verify → Delete → Count verify.

---

### Step 6: Mass Source (Tier 2 — Workflow sísmico)
**Files:** `scripts/wrappers/func_SourceMass_SetMassSource.py`, `func_SourceMass_GetMassSource.py`, `func_SourceMass_GetDefault.py`, `func_SourceMass_Count.py`, `scripts/registry.json`
**What:** Agregar soporte de fuente de masa, esencial para análisis sísmicos y modales donde se necesita definir qué load patterns contribuyen a la masa del modelo.
**Funciones:**
- `SapModel.SourceMass.SetMassSource(Name, MassFromElements, MassFromMasses, MassFromLoads, IsDefault, NumberLoads, LoadPat[], SF[])` → ret_code
- `SapModel.SourceMass.GetMassSource(Name)` → [MassFromElements, MassFromMasses, MassFromLoads, IsDefault, NumberLoads, LoadPat[], SF[], ret_code]
- `SapModel.SourceMass.GetDefault()` → [Name, ret_code]
- `SapModel.SourceMass.Count()` → count
**Testing:** SetMassSource con DEAD×1.0 → GetMassSource → verify flags y SF. GetDefault → verify nombre.

---

### Step 7: Constraint Types + Admin (Tier 2)
**Files:** `scripts/wrappers/func_ConstraintDef_SetBeam.py`, `func_ConstraintDef_SetPlate.py`, `func_ConstraintDef_SetEqual.py`, `func_ConstraintDef_Count.py`, `func_ConstraintDef_Delete.py`, `func_ConstraintDef_GetNameList.py`, `scripts/registry.json`
**What:** Ampliar tipos de constraints más allá de Body/Diaphragm. Beam constraint para vigas rígidas, Plate para losas, Equal para desplazamientos iguales. Agregar admin (Count, Delete, GetNameList).
**Funciones:**
- `SapModel.ConstraintDef.SetBeam(Name, DOF[], CSys)` → ret_code
- `SapModel.ConstraintDef.SetPlate(Name, DOF[], CSys)` → ret_code
- `SapModel.ConstraintDef.SetEqual(Name, DOF[], CSys)` → ret_code
- `SapModel.ConstraintDef.Count(ConstraintType)` → count
- `SapModel.ConstraintDef.Delete(Name)` → ret_code
- `SapModel.ConstraintDef.GetNameList()` → [NumberNames, MyName[], ret_code]
**Testing:** Set cada tipo → Count por tipo → GetNameList → Delete → Count verify.

---

### Step 8: Frame/Area Modifiers + Property Admin (Tier 2)
**Files:** `scripts/wrappers/func_FrameObj_SetModifiers.py`, `func_FrameObj_GetModifiers.py`, `func_PropArea_SetModifiers.py`, `func_PropArea_GetModifiers.py`, `func_PropFrame_ChangeName.py`, `func_PropFrame_Delete.py`, `func_PropFrame_Count.py`, `func_PropMaterial_ChangeName.py`, `func_PropMaterial_Delete.py`, `func_PropMaterial_Count.py`, `scripts/registry.json`
**What:** Stiffness modifiers (esenciales para diseño sísmico — reducción de rigidez agrietada) y funciones administrativas de properties para gestión programática de modelos.
**Funciones:**
- `SapModel.FrameObj.SetModifiers(Name, Value[8])` → ret_code
- `SapModel.FrameObj.GetModifiers(Name)` → [Value[8], ret_code]
- `SapModel.PropArea.SetModifiers(Name, Value[10])` → ret_code
- `SapModel.PropArea.GetModifiers(Name)` → [Value[10], ret_code]
- `SapModel.PropFrame.ChangeName(Name, NewName)` → ret_code
- `SapModel.PropFrame.Delete(Name)` → ret_code
- `SapModel.PropFrame.Count(PropType)` → count
- `SapModel.PropMaterial.ChangeName(Name, NewName)` → ret_code
- `SapModel.PropMaterial.Delete(Name)` → ret_code
- `SapModel.PropMaterial.Count(MatType)` → count
**Testing:** Crear frame → SetModifiers con factores de agrietamiento (0.35 vigas, 0.70 columnas) → GetModifiers → verify.

---

## Resumen de Impacto

| Métrica | Antes | Después |
|---|---|---|
| Funciones en registry | ~133 | ~178 (+45) |
| Wrappers verificados | 71 | ~116 (+45) |
| Cobertura de workflows de diseño | Parcial | Completa |
| Funciones usadas en scripts sin registrar | ~15 | 0 |
| Soporte Mass Source | Ninguno | Completo |
| Tipos de secciones frame | 4 | 7 |
| Tipos de constraints | 2 | 5 |

## Priorización

- **Steps 1-4** (Tier 1): Funciones ya usadas en producción → prioridad máxima
- **Steps 5-8** (Tier 2): Funciones de alto valor para completar workflows → siguiente iteración

## Notas

- Cada wrapper sigue el patrón estándar existente (header, prerequisites, test script completo)
- Cada función se registra en `registry.json` con `verified: true` y fecha
- El workflow por función es: escribir wrapper → ejecutar vía MCP → verificar ret_code → registrar
- Los steps son independientes entre sí, se pueden ejecutar en cualquier orden
- **Scope de diseño:** Solo acero (`DesignSteel`) y concreto (`DesignConcrete`); aluminio y cold-formed quedan fuera del alcance
