# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadGravity
# Category: Object_Model
# Description: Assign gravity load multipliers to area objects
# Verified: 2026-03-28
# Prerequisites: Model open, area object exists, load pattern defined
# ============================================================
"""
Usage: Assigns gravity load multipliers (x, y, z) to area objects.
       Multiplier of -1 in Z means full self-weight downward.

API Signature:
  SapModel.AreaObj.SetLoadGravity(Name, LoadPat, x, y, z,
      Replace, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str   — Area object name (or group)
  LoadPat : str   — Load pattern name
  x, y, z : float — Gravity multipliers in specified CSys
  Replace : bool  — True=replace previous gravity loads
  CSys    : str   — Coordinate system (default "Global")
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
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_TEST", 1, 24.0)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_15", 1, False, "CONC_TEST", 0, 0.15, 0.15)
assert ret == 0

# Create 3m x 3m slab
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 3, 3, 0], [0, 0, 3, 3], [0, 0, 0, 0], "", "SLAB_15"
)
area_name = raw[3]
assert raw[-1] == 0

for i in range(1, 5):
    ret = SapModel.PointObj.SetRestraint(
        str(i), [True, True, True, False, False, False]
    )
    assert ret[-1] == 0

# --- Target function ---
# Full self-weight: z = -1
ret = SapModel.AreaObj.SetLoadGravity(area_name, "DEAD", 0, 0, -1)
assert ret == 0, f"SetLoadGravity failed: {ret}"

# --- Verification ---
ret = SapModel.File.Save(sap_temp_dir + r"\sap_areaobj_setloadgravity.sdb")
assert ret == 0
ret = SapModel.Analyze.RunAnalysis()
assert ret == 0

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
assert ret == 0
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("DEAD")
assert ret == 0

raw = SapModel.Results.BaseReact(
    0, [], [], [], [], [], [], [], [], [], 0.0, 0.0, 0.0
)
assert raw[-1] == 0
total_Fz = sum(list(raw[5]))

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadGravity"
result["area_name"] = area_name
result["total_base_Fz"] = total_Fz
result["status"] = "verified"
