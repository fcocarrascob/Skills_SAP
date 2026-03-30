# Common SAP2000 Workflows

## Workflow 1: Simple Beam Analysis

1. Initialize model → `SapModel.InitializeNewModel()`
2. Create blank model → `SapModel.File.NewBlank()`
3. Set units → `SapModel.SetPresentUnits(4)` (kip_ft_F)
4. Define material → `PropMaterial.SetMaterial` + `SetMPIsotropic`
5. Define section → `PropFrame.SetRectangle`
6. Create beam → `FrameObj.AddByCoord` (one horizontal member)
7. Set supports → `PointObj.SetRestraint` on both ends
8. Add load pattern → `LoadPatterns.Add`
9. Assign loads → `FrameObj.SetLoadDistributed`
10. Save → `File.Save`
11. Run analysis → `Analyze.RunAnalysis`
12. Extract results → `Results.Setup` + `Results.JointDispl`

## Workflow 2: Portal Frame from Template

1. Initialize → `SapModel.InitializeNewModel()`
2. Create from template → `File.New2DFrame(0, stories, height, bays, width)`
3. Assign additional loads if needed
4. Save and run analysis
5. Extract results

## Workflow 3: Verification Problem (Example 1-001)

This is the standard SAP2000 verification problem:

1. Create blank model
2. Define concrete material (E=3600 ksi, ν=0.2, α=0.0000055)
3. Define rectangular frame section (12×12 in)
4. Set section modifiers: Area=1000, AS2=0, AS3=0
5. Switch to kip-ft units
6. Add three frame members by coordinates:
   - Column: (0,0,0) → (0,0,10)
   - Beam: (0,0,10) → (8,0,16)
   - Cantilever: (-4,0,10) → (0,0,10)
7. Set base restraint (fixed: Ux, Uy, Uz, Rx)
8. Set top restraint (roller: Ux, Uy)
9. Add 7 load patterns with various load types
10. Save and run analysis
11. Compare results with hand-calculated values

## Workflow 4: Design Check

1. Create/load model with analysis results
2. Select design code → `DesignSteel.SetCode` or `DesignConcrete.SetCode`
3. Start design → `DesignSteel.StartDesign`
4. Extract design results

## Workflow 5: Modify Existing Model

1. Connect to existing SAP2000 instance → `connect_sap2000(attach_to_existing=True)`
2. Check model state → `get_model_info`
3. Make modifications via script
4. Save → `File.Save`
5. Re-run analysis if needed

## Patrón Universal de Scripts SAP2000

Todo script sigue esta secuencia de fases (omitir las que no apliquen):

| # | Fase | Funciones Típicas | Prerequisito |
|---|------|-------------------|-------------|
| 1 | Inicialización | InitializeNewModel, File.NewBlank, SetPresentUnits | — |
| 2 | Materiales | PropMaterial.SetMaterial, SetMPIsotropic | Fase 1 |
| 3 | Secciones | PropFrame.Set*, PropArea.SetShell_1 | Fase 2 |
| 4 | Geometría | FrameObj.AddByCoord, AreaObj.AddByCoord | Fase 3 |
| 5 | Restricciones | PointObj.SetRestraint, ConstraintDef.* | Fase 4 |
| 6 | Cargas | LoadPatterns.Add, SetLoadDistributed, SetLoadUniform | Fase 4-5 |
| 7 | Análisis | File.Save, Analyze.SetActiveDOF, RunAnalysis | Fase 5-6 |
| 8 | Resultados | Results.Setup.*, Results.JointDispl | Fase 7 |
| 9 | Verificación | Asserts, result{} | Fase 8 |

### Lógica Geométrica Común

| Patrón | Uso | Funciones math |
|--------|-----|----------------|
| Grilla rectangular | Pórticos, edificios | `range(nx) × range(ny)` |
| Circular/anular | Domos, tanques | `sin(θ)`, `cos(θ)` |
| Helicoidal | Escaleras, rampas | `sin(θ)`, `cos(θ)`, `pitch × θ/(2π)` |
| Superficie paramétrica | Shells, paraboloides | `f(u,v)` → `(x,y,z)` |
| Rotación progresiva | Torres twisted | `cos(α)·x - sin(α)·y`, `sin(α)·x + cos(α)·y` |
