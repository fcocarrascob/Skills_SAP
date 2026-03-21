# ============================================================
# Wrapper: SapModel.Results.AreaForceShell
# Category: Analysis_Results
# Description: Extract shell element forces and moments
# Verified: 2026-03-21
# Prerequisites: Model analyzed, area (shell) elements exist
# ============================================================
"""
Usage: Extracts shell forces and moments (F11, F22, F12, M11, M22, M12,
       V13, V23, etc.) for area elements. Results are per unit width.

API Signature:
  SapModel.Results.AreaForceShell(Name, ItemTypeElm,
      NumberResults, Obj, Elm,
      PointElm, LoadCase, StepType, StepNum,
      F11, F22, F12, FMax, FMin, FAngle, FVM,
      M11, M22, M12, MMax, MMin, MAngle,
      V13, V23, VMax, VAngle) -> ret_code

ByRef Output (25 values):
  NumberResults : int     — number of result rows
  Obj[]         : str[]   — area object names
  Elm[]         : str[]   — area element names
  PointElm[]    : str[]   — point element names at corners
  LoadCase[]    : str[]   — load case/combo names
  StepType[]    : str[]   — step type
  StepNum[]     : float[] — step number
  F11[]..VAngle[]: float[] — force/moment result arrays

Parameters:
  Name        : str — Area name ("All" for all)
  ItemTypeElm : int — 0=Object, 1=Element, 2=GroupElm, 3=SelectionElm
"""

# --- Minimal setup: simple slab ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material
ret = SapModel.PropMaterial.SetMaterial("CONC_SLAB", 2)  # Concrete
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_SLAB", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

# Shell section (150mm slab)
ret = SapModel.PropArea.SetShell_1("SLAB_150", 1, False, "CONC_SLAB", 0, 0.150, 0.150)
assert ret == 0

# Create a 4x4m slab (single area)
area = SapModel.AreaObj.AddByCoord(
    4,  # NumPoints
    [0, 4, 4, 0],   # X
    [0, 0, 4, 4],   # Y
    [0, 0, 0, 0],   # Z
    "", "SLAB_150"
)
# AreaObj.AddByCoord returns [X_coords, Y_coords, Z_coords, Name_str, ret_code]
area_name = area[3]
assert area[-1] == 0

# Restraints at all four corners (supported slab)
for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret == 0, f"Restraint at node {i} failed: {ret}"

# Uniform area load
ret = SapModel.AreaObj.SetLoadUniform(area_name, "DEAD", -5, 10, True, "Global")
assert ret == 0

# Save model before analysis (required by SAP2000)
ret = SapModel.File.Save(r"C:\Temp\sap_results_areaforceshell.sdb")
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
# NOTE: "All" may not work as wildcard — use specific area name
raw = SapModel.Results.AreaForceShell(
    area_name, 0,
    0, [], [], [],     # NumberResults, Obj, Elm, PointElm
    [], [], [],        # LoadCase, StepType, StepNum
    [], [], [], [], [], [], [],   # F11..FVM
    [], [], [], [], [], [],       # M11..MAngle
    [], [], [], []                # V13, V23, VMax, VAngle
)
ret_code = raw[-1]
assert ret_code == 0, f"AreaForceShell failed: {ret_code}"

num_results = raw[0]
assert num_results > 0, f"No shell results returned"

# --- Result ---
result["function"] = "SapModel.Results.AreaForceShell"
result["area_name"] = area_name
result["num_results"] = num_results
result["status"] = "verified"
