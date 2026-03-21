# ============================================================
# Wrapper: SapModel.AreaObj.SetLoadGravity
# Category: Load_Assignment
# Description: Apply gravity multiplier on area self-weight
# Verified: pending
# Prerequisites: Model open, area exists, load pattern defined
# ============================================================
"""
Usage: Assigns gravity load multipliers to an area element.
       This acts as a multiplier on the element's self-weight,
       applying loads in the specified global direction.

API Signature:
  SapModel.AreaObj.SetLoadGravity(Name, LoadPat, x, y, z,
      Replace, CSys, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str   — Area object name
  LoadPat  : str   — Load pattern name
  x        : float — Gravity multiplier in global X
  y        : float — Gravity multiplier in global Y
  z        : float — Gravity multiplier in global Z
  Replace  : bool  — True=replace existing (default=True)
  CSys     : str   — Coordinate system (default="Global")
  ItemType : int   — 0=Object, 1=Group, 2=SelectedObjects (default=0)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0
ret = SapModel.PropMaterial.SetWeightAndMass("CONC_TEST", 1, 23.56)
assert ret == 0

ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, True, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

x = [0.0, 6.0, 6.0, 0.0]
y = [0.0, 0.0, 4.0, 4.0]
z = [3.0, 3.0, 3.0, 3.0]
raw = SapModel.AreaObj.AddByCoord(4, x, y, z, "", "SLAB_20", "")
area_name = raw[3]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

ret = SapModel.LoadPatterns.Add("SW_GRAV", 1, 0)  # Dead
assert ret == 0

# --- Target function: gravity multiplier (1g downward) ---
ret = SapModel.AreaObj.SetLoadGravity(area_name, "SW_GRAV", 0, 0, -1)
assert ret == 0, f"SetLoadGravity failed: {ret}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetLoadGravity"
result["area_name"] = area_name
result["gravity_multiplier"] = [0, 0, -1]
result["status"] = "verified"
