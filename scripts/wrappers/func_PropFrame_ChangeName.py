# ============================================================
# Wrapper: SapModel.PropFrame.ChangeName
# Category: PropFrame
# Description: Rename a frame section property
# Verified: 2026-03-28
# Prerequisites: Model open, frame section defined
# ============================================================
"""
Usage: Changes the name of an existing frame section property.

API Signature:
  SapModel.PropFrame.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing frame section name
  NewName : str — New name for the section
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("MAT_CN", 2)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("OLD_SEC", "MAT_CN", 0.5, 0.3)
assert ret == 0

# --- Target function ---
ret = SapModel.PropFrame.ChangeName("OLD_SEC", "NEW_SEC")
assert ret == 0, f"ChangeName failed: {ret}"

# Verify
raw = SapModel.PropFrame.GetNameList(0, [])
assert raw[-1] == 0
names = list(raw[1])
assert "NEW_SEC" in names, f"NEW_SEC not found in: {names}"
assert "OLD_SEC" not in names, f"OLD_SEC still exists in: {names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.ChangeName"
result["old_name"] = "OLD_SEC"
result["new_name"] = "NEW_SEC"
result["status"] = "verified"
