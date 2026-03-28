# ============================================================
# Wrapper: SapModel.AreaObj.SetProperty
# Category: Object_Model
# Description: Assign or change area section property on an area object
# Verified: 2026-03-28
# Prerequisites: Model open, area object and property exist
# ============================================================
"""
Usage: Assigns a shell/plate/membrane section property to an area object,
       or changes the property of an existing area.

API Signature:
  SapModel.AreaObj.SetProperty(Name, PropName, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str — Area object name
  PropName : str — Area property name (or "None" to clear)
  ItemType : int — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0
ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0

# Two different shell sections
ret = SapModel.PropArea.SetShell_1("SLAB_15", 1, False, "CONC_TEST", 0, 0.15, 0.15)
assert ret == 0
ret = SapModel.PropArea.SetShell_1("SLAB_25", 1, False, "CONC_TEST", 0, 0.25, 0.25)
assert ret == 0

# Create area with SLAB_15
raw = SapModel.AreaObj.AddByCoord(
    4, [0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_15"
)
area_name = raw[3]
assert raw[-1] == 0

# Verify initial property
# GetProperty(Name, PropName_ByRef) -> [PropName, ret_code]
raw_get = SapModel.AreaObj.GetProperty(area_name, "")
assert raw_get[-1] == 0
initial_prop = raw_get[0]
assert initial_prop == "SLAB_15", f"Initial prop should be SLAB_15, got {initial_prop}"

# --- Target function: change property ---
ret = SapModel.AreaObj.SetProperty(area_name, "SLAB_25")
assert ret == 0, f"SetProperty failed: {ret}"

# --- Verification ---
raw_get = SapModel.AreaObj.GetProperty(area_name, "")
assert raw_get[-1] == 0
new_prop = raw_get[0]
assert new_prop == "SLAB_25", f"Expected SLAB_25, got {new_prop}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetProperty"
result["area_name"] = area_name
result["initial_property"] = initial_prop
result["new_property"] = new_prop
result["status"] = "verified"
