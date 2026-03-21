# ============================================================
# Wrapper: SapModel.Results.FrameForce
# Category: Analysis_Results
# Description: Extract frame element internal forces
# Verified: 2026-03-21
# Prerequisites: Model analyzed
# ============================================================
"""
Usage: Extracts internal forces (P, V2, V3, T, M2, M3) for a
       given frame element after analysis. Results are returned at
       multiple stations along the element length.

API Signature:
  SapModel.Results.FrameForce(Name, ItemTypeElm,
      NumberResults, Obj, ObjSta, Elm, ElmSta,
      LoadCase, StepType, StepNum,
      P, V2, V3, T, M2, M3) -> ret_code

ByRef Output (14 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — object names
  ObjSta[]      : float[] — station distances on object
  Elm[]         : str[]   — element names
  ElmSta[]      : float[] — station distances on element
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  P[]           : float[] — axial force
  V2[]          : float[] — shear in local-2
  V3[]          : float[] — shear in local-3
  T[]           : float[] — torsion
  M2[]          : float[] — moment about local-2
  M3[]          : float[] — moment about local-3

Parameters:
  Name        : str — Frame name (or "All" for all frames)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: simple beam with uniform load ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("BEAM_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Simply supported beam, 6m span
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SEC", "")
beam_name = beam[0]
assert beam[-1] == 0

# Supports (pin-roller)
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, False, False, False])
assert ret[-1] == 0
ret = SapModel.PointObj.SetRestraint("2", [True, True, True, False, False, False])
assert ret[-1] == 0

# Uniform load -10 kN/m on beam (gravity direction)
ret = SapModel.FrameObj.SetLoadDistributed(
    beam_name, "DEAD", 1, 10, 0, 1, -10, -10, "Global", True, True
)
assert ret == 0

# Save model before analysis (required by SAP2000)
ret = SapModel.File.Save(r"C:\Temp\sap_results_frameforce.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set results for DEAD case
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
raw = SapModel.Results.FrameForce(
    beam_name, 0,     # ObjectElm
    0, [], [], [], [], [], [], [],   # ByRef placeholders
    [], [], [], [], [], []
)
ret_code = raw[-1]
assert ret_code == 0, f"FrameForce failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No results returned"

obj_names   = list(raw[1])
obj_sta     = list(raw[2])
load_cases  = list(raw[5])
P_values    = list(raw[8])
V2_values   = list(raw[9])
M3_values   = list(raw[13])

# --- Result ---
result["function"] = "SapModel.Results.FrameForce"
result["frame_name"] = beam_name
result["num_results"] = num_results
result["sample_stations"] = obj_sta[:5]
result["sample_M3"] = M3_values[:5]
result["sample_V2"] = V2_values[:5]
result["status"] = "verified"
