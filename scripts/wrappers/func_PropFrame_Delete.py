# ============================================================
# Wrapper: SapModel.PropFrame.Delete
# Category: PropFrame
# Description: Delete a frame section property
# Verified: 2026-03-28
# Prerequisites: Model open, frame section defined, not in use
# ============================================================
"""
Usage: Deletes a frame section property. Cannot delete if in use
       by any frame object.

API Signature:
  SapModel.PropFrame.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of frame section to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_DEL", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TO_DEL", "MAT_DEL", 0.3, 0.3)
assert ret == 0

count_before = SapModel.PropFrame.Count()

# --- Target function ---
ret = SapModel.PropFrame.Delete("SEC_TO_DEL")
assert ret == 0, f"Delete failed: {ret}"

count_after = SapModel.PropFrame.Count()
assert count_after == count_before - 1, f"Count mismatch: before={count_before}, after={count_after}"

# --- Result ---
result["function"] = "SapModel.PropFrame.Delete"
result["deleted"] = "SEC_TO_DEL"
result["count_before"] = count_before
result["count_after"] = count_after
result["status"] = "verified"
