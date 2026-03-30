# ============================================================
# Wrapper: SapModel.AreaObj.SetGroupAssign
# Category: Object_Model
# Description: Add or remove area objects from a group
# Verified: 2026-03-28
# Prerequisites: Model open, area and group exist
# ============================================================
"""
Usage: Adds area objects to (or removes from) a specified group.

API Signature:
  SapModel.AreaObj.SetGroupAssign(Name, GroupName, Remove,
      ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str  — Area object name
  GroupName : str  — Target group name (must exist)
  Remove    : bool — False=add, True=remove
  ItemType  : int  — 0=Object, 1=Group, 2=SelectedObjects
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
ret = SapModel.PropArea.SetShell_1("SLAB_20", 1, False, "CONC_TEST", 0, 0.20, 0.20)
assert ret == 0

# Create two areas
raw1 = SapModel.AreaObj.AddByCoord(
    4, [0, 4, 4, 0], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
a1 = raw1[3]
assert raw1[-1] == 0

raw2 = SapModel.AreaObj.AddByCoord(
    4, [4, 8, 8, 4], [0, 0, 4, 4], [0, 0, 0, 0], "", "SLAB_20"
)
a2 = raw2[3]
assert raw2[-1] == 0

# Create group
ret = SapModel.GroupDef.SetGroup("SLABS_FLOOR1")
assert ret == 0

# --- Target function ---
ret = SapModel.AreaObj.SetGroupAssign(a1, "SLABS_FLOOR1")
assert ret == 0, f"SetGroupAssign(a1) failed: {ret}"

ret = SapModel.AreaObj.SetGroupAssign(a2, "SLABS_FLOOR1")
assert ret == 0, f"SetGroupAssign(a2) failed: {ret}"

# --- Verification ---
raw = SapModel.GroupDef.GetAssignments("SLABS_FLOOR1", 0, [], [])
ret_code = raw[-1]
assert ret_code == 0
num_items = raw[0]
obj_types = list(raw[1])
assert num_items == 2, f"Expected 2, got {num_items}"
# ObjectType 5 = Area object
assert all(t == 5 for t in obj_types), f"Expected all type=5(Area), got {obj_types}"

# --- Result ---
result["function"] = "SapModel.AreaObj.SetGroupAssign"
result["group_name"] = "SLABS_FLOOR1"
result["items_in_group"] = num_items
result["object_types"] = obj_types
result["status"] = "verified"
