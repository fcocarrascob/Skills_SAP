# ============================================================
# Wrapper: SapModel.PropMaterial.ChangeName
# Category: PropMaterial
# Description: Rename a material property
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Changes the name of an existing material property.

API Signature:
  SapModel.PropMaterial.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing material name
  NewName : str — New name for the material
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("OLD_MAT", 1)
assert ret == 0

# --- Target function ---
ret = SapModel.PropMaterial.ChangeName("OLD_MAT", "NEW_MAT")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify
raw = SapModel.PropMaterial.GetNameList(0, [])
assert raw[-1] == 0
mat_names = list(raw[1])
assert "NEW_MAT" in mat_names, f"NEW_MAT not found in: {mat_names}"
assert "OLD_MAT" not in mat_names, f"OLD_MAT still exists in: {mat_names}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.ChangeName"
result["old_name"] = "OLD_MAT"
result["new_name"] = "NEW_MAT"
result["status"] = "verified"
