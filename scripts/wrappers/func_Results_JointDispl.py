# ============================================================
# Wrapper: SapModel.Results.JointDispl
# Category: Analysis_Results
# Description: Extract joint displacements (translations/rotations)
# Verified: 2026-03-21
# Prerequisites: Model analyzed
# ============================================================
"""
Usage: Extracts joint displacement results (U1, U2, U3, R1, R2, R3)
       after analysis. Returns translations and rotations for each
       joint and load case.

API Signature:
  SapModel.Results.JointDispl(Name, ItemTypeElm,
      NumberResults, Obj, Elm,
      LoadCase, StepType, StepNum,
      U1, U2, U3, R1, R2, R3) -> ret_code

ByRef Output (12 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — joint object names
  Elm[]         : str[]   — joint element names
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  U1[]          : float[] — translation in global-X [L]
  U2[]          : float[] — translation in global-Y [L]
  U3[]          : float[] — translation in global-Z [L]
  R1[]          : float[] — rotation about global-X [rad]
  R2[]          : float[] — rotation about global-Y [rad]
  R3[]          : float[] — rotation about global-Z [rad]

Parameters:
  Name        : str — Joint name ("All" for all joints)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: cantilever with point load ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("CANT_SEC", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Cantilever beam, 4m long
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 4, 0, 0, "", "CANT_SEC", "")
assert beam[-1] == 0

# Fixed support at node 1
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret[-1] == 0

# Point load at free end (node 2): -50 kN in Z
ret = SapModel.PointObj.SetLoadForce("2", "DEAD", [0, 0, -50, 0, 0, 0])
assert ret[-1] == 0

# Save model before analysis (required by SAP2000)
ret = SapModel.File.Save(r"C:\Temp\sap_results_jointdispl.sdb")
assert ret == 0, f"File.Save failed: {ret}"

# Analyze
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# Set output selection
ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# --- Target function ---
# NOTE: "All" does not work as a wildcard — use specific joint names
raw = SapModel.Results.JointDispl(
    "2", 0,      # Free-end joint, ObjectElm
    0, [], [],   # ByRef: NumberResults, Obj, Elm
    [], [], [],  # ByRef: LoadCase, StepType, StepNum
    [], [], [], [], [], []  # ByRef: U1..R3
)
ret_code = raw[-1]
assert ret_code == 0, f"JointDispl failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No displacement results"

obj_names  = list(raw[1])
load_cases = list(raw[3])
U1_values  = list(raw[6])
U2_values  = list(raw[7])
U3_values  = list(raw[8])

# --- Result ---
result["function"] = "SapModel.Results.JointDispl"
result["num_results"] = num_results
result["joint_names"] = obj_names
result["U3_values"] = U3_values
result["status"] = "verified"
