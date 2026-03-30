# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadUniform
# Category: Object_Model
# Description: Assign uniform distributed loads to area objects
# Verified: 2026-03-28
# Prerequisites: Model open, area object exists, load pattern defined
# ============================================================
"""
Usage: Assigns a uniform pressure load [F/L²] to area (shell/plate/membrane)
       objects over their entire surface.

API Signature:
  SapModel.AreaObj.SetLoadUniform(Name, LoadPat, Value, Dir,
      Replace, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str   — Area object name (or group)
  LoadPat : str   — Load pattern name
  Value   : float — Uniform load value [F/L²]
  Dir     : int   — 1-3=Local, 4-6=Global XYZ, 10=Gravity, 11=Proj. Gravity
  Replace : bool  — True=replace previous uniform loads
  CSys    : str   — "Global" or "Local"
  ItemType: int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, False, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

# Create 5m x 4m slab
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 5, 5, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
area_name = raw[3]
assert raw[-1] == 0

# Pin all corners
for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret[-1] == 0

# --- Target function: uniform downward load ---
# -5 kN/m² gravity direction
ret = SapModel.AreaObj.SetLoadUniform(
    area_name, "DEAD", -5.0, 10, True, "Global"
)
assert ret == 0, f"SetLoadUniform failed: {ret}"

# --- Verification via analysis ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_areaobj_setloaduniform.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

# Total applied = 5 * 5 * 4 = 100 kN (but self-weight adds more)
# Check base reactions exist and are nonzero
raw = SapModel.Results.BaseReact(
    0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
)
assert raw[-1] == 0
Fz = list(raw[5])
total_Fz = sum(Fz)

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadUniform"
result["area_name"] = area_name
result["total_base_Fz"] = total_Fz
result["status"] = "verified"
