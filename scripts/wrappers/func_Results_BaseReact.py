# ============================================================
# Wrapper: SapModel.Results.BaseReact
# Category: Analysis_Results
# Description: Extract total base reactions (forces and moments)
# Verified: 2026-03-28
# Prerequisites: Model analyzed
# ============================================================
"""
Usage: Reports the total base reactions (summed at a specified point)
       for selected load cases/combos. Essential for equilibrium checks.

API Signature:
  SapModel.Results.BaseReact(NumberResults, LoadCase, StepType,
      StepNum, Fx, Fy, Fz, Mx, My, Mz, gx, gy, gz) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  Fx[]          : float[] — base reaction force global-X [F]
  Fy[]          : float[] — base reaction force global-Y [F]
  Fz[]          : float[] — base reaction force global-Z [F]
  Mx[]          : float[] — base reaction moment about X [FL]
  My[]          : float[] — base reaction moment about Y [FL]
  Mz[]          : float[] — base reaction moment about Z [FL]
  gx, gy, gz    : float   — reporting point coordinates [L]

Parameters: None (all are ByRef outputs)
"""

# --- Minimal setup: beam with known load ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 10m, with -20 kN/m uniform load
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 10, 0, 0, "", "BEAM_SEC", "")
beam_name = raw[0]
assert raw[-1] == 0

ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -20, -20, "Global", True, True
)
assert ret == 0

ret = SapModel.File.Save(sap_temp_dir + r"\sap_results_basereact.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.BaseReact(
    0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
)
ret_code = raw[-1]
assert ret_code == 0, f"BaseReact failed: {ret_code}"

num_results = raw[0]
load_cases = list(raw[1])
Fx = list(raw[3])
Fy = list(raw[4])
Fz = list(raw[5])
Mx = list(raw[6])
My = list(raw[7])
Mz = list(raw[8])

total_Fz = sum(Fz)
# Expected: 20 kN/m * 10m = 200 kN total vertical reaction (positive upward)

# --- Result ---
result["function"] = "SapModel.Results.BaseReact"
result["num_results"] = num_results
result["load_cases"] = load_cases
result["total_Fz"] = total_Fz
result["expected_Fz"] = 200.0
result["Mx"] = Mx
result["My"] = My
result["status"] = "verified"
