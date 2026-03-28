# ============================================================
# Wrapper: SapModel.PropMaterial.Delete
# Category: PropMaterial
# Description: Delete a material property
# Verified: 2026-03-28
# Prerequisites: Model open, material defined, not in use
# ============================================================
"""
Usage: Deletes a material property. Cannot delete if in use
       by any section or element.

API Signature:
  SapModel.PropMaterial.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of material to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TO_DEL", 1)
assert ret == 0

count_before = SapModel.PropMaterial.Count()

# --- Target function ---
ret = SapModel.PropMaterial.Delete("MAT_TO_DEL")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.PropMaterial.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.PropMaterial.Delete"
result["deleted"] = "MAT_TO_DEL"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
