# ─── SAP2000 Script ─────────────────────────────────────────────
# Name:        test_blockly_workflow_portico_py
# Description: 
# Created:     2026-04-05 01:23:31 UTC
# Status:      ✓ Verified (executed successfully)
# Result:      {"phases_completed": 8, "model": "Portico 2D 2cols+viga, Blockly simulation", "col_izq": "COL_IZQ", "col_der": "COL_DER", "viga": "VIGA_TOP", "num_results": 11, "dead_V2_min": -25.36, "dead_M3_min": -28.16, "status": "OK"}
# Tags:        
# ──────────────────────────────────────────────────────────────


# ============================================================
# TEST: Blockly Visual Scripter — Simulación Workflow Completo
# ============================================================
# Simula el Python que BlocklyTranspiler._block_to_python() genera
# Pórtico 2D: 2 columnas 4m + 1 viga 6m (acero, DEAD+LIVE)
# ============================================================

# Fase 1: Init
ret = SapModel.File.NewBlank()
assert ret == 0
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# Fase 2: Materiales
ret = SapModel.PropMaterial.SetMaterial("ACERO_A36", 1)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("ACERO_A36", 2.0e8, 0.3, 1.2e-5)
assert ret == 0

# Fase 3: Secciones
ret = SapModel.PropFrame.SetRectangle("COLUMNA_30x30", "ACERO_A36", 0.3, 0.3)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("VIGA_30x50", "ACERO_A36", 0.5, 0.3)
assert ret == 0

# Fase 4: Geometría
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 4, "", "COLUMNA_30x30", "COL_IZQ")
col_izq = raw[0]; assert raw[-1] == 0

raw = SapModel.FrameObj.AddByCoord(6, 0, 0, 6, 0, 4, "", "COLUMNA_30x30", "COL_DER")
col_der = raw[0]; assert raw[-1] == 0

raw = SapModel.FrameObj.AddByCoord(0, 0, 4, 6, 0, 4, "", "VIGA_30x50", "VIGA_TOP")
viga = raw[0]; assert raw[-1] == 0

# Fase 5: Restricciones
raw = SapModel.FrameObj.GetPoints(col_izq, "", "")
pt_base_izq = raw[0]; assert raw[-1] == 0
raw = SapModel.FrameObj.GetPoints(col_der, "", "")
pt_base_der = raw[0]; assert raw[-1] == 0
raw = SapModel.PointObj.SetRestraint(pt_base_izq, [True, True, True, True, True, True])
assert raw[-1] == 0
raw = SapModel.PointObj.SetRestraint(pt_base_der, [True, True, True, True, True, True])
assert raw[-1] == 0

# Fase 6: Cargas
ret = SapModel.LoadPatterns.Add("LIVE", 3, 0)
assert ret == 0
ret = SapModel.FrameObj.SetLoadDistributed(viga, "DEAD", 1, 10, 0, 1, -20, -20, "Global", True, True)
assert ret == 0
ret = SapModel.FrameObj.SetLoadDistributed(viga, "LIVE", 1, 10, 0, 1, -15, -15, "Global", True, True)
assert ret == 0

# Fase 7: Análisis
ret = SapModel.File.Save(sap_temp_dir + r"\blockly_test_portico.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

# Fase 8: Resultados
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0
raw = SapModel.Results.FrameForce(viga, 0, 0, [], [], [], [], [], [], [], [], [], [], [])
assert raw[-1] == 0

result["phases_completed"] = 8
result["model"] = "Portico 2D 2cols+viga, Blockly simulation"
result["col_izq"] = col_izq
result["col_der"] = col_der
result["viga"] = viga
result["num_results"] = raw[0]
result["dead_V2_min"] = round(min(list(raw[9])), 2)
result["dead_M3_min"] = round(min(list(raw[13])), 2)
result["status"] = "OK"
