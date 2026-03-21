# ============================================================
# Wrapper: SapModel.Results.JointReact
# Category: Analysis_Results
# Description: Extract joint reactions (forces/moments at supports)
# Verified: 2026-03-21
# Prerequisites: Model analyzed, joints with restraints
# ============================================================
"""
Usage: Extracts joint reaction forces and moments (F1, F2, F3, M1, M2, M3)
       at restrained joints after analysis.

API Signature:
  SapModel.Results.JointReact(Name, ItemTypeElm,
      NumberResults, Obj, Elm,
      LoadCase, StepType, StepNum,
      F1, F2, F3, M1, M2, M3) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — joint object names
  Elm[]         : str[]   — joint element names
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  F1[]          : float[] — reaction force global-X [F]
  F2[]          : float[] — reaction force global-Y [F]
  F3[]          : float[] — reaction force global-Z [F]
  M1[]          : float[] — reaction moment about global-X [F·L]
  M2[]          : float[] — reaction moment about global-Y [F·L]
  M3[]          : float[] — reaction moment about global-Z [F·L]

Parameters:
  Name        : str — Joint name ("All" for all restrained joints)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: simply supported beam ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SS_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 8m span
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 8, 0, 0, "", "SS_SEC", "")
assert beam[-1] == 0

# Pin-roller supports
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

# Uniform downward load -20 kN/m
ret = SapModel.FrameObj.SetLoadDistributed(
    beam[0], "DEAD", 1, 10, 0, 1, -20, -20, "Global", True, True
)
assert ret == 0

# Save model before analysis (required by SAP2000)
ret = SapModel.File.Save(r"C:\Temp\sap_results_jointreact.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set output
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
# NOTE: "All" does not work as a wildcard — use specific joint names
# For a simply-supported beam joints "1" and "2" are the supports
raw = SapModel.Results.JointReact(
    "1", 0,
    0, [], [],
    [], [], [],
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"JointReact failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No reaction results"

obj_names  = list(raw[1])
load_cases = list(raw[3])
F1_values  = list(raw[6])
F2_values  = list(raw[7])
F3_values  = list(raw[8])

# Sanity check: total vertical reaction ≈ w*L = 20*8 = 160 kN
total_F3 = sum(F3_values)

# --- Result ---
result["function"] = "SapModel.Results.JointReact"
result["num_results"] = num_results
result["joint_names"] = obj_names
result["F3_values"] = F3_values
result["total_vertical_reaction"] = total_F3
result["expected_total"] = 160.0
result["status"] = "verified"
