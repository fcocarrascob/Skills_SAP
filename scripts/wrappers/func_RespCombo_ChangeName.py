# ============================================================
# Wrapper: SapModel.RespCombo.ChangeName
# Category: RespCombo
# Description: Rename an existing load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Changes the name of an existing load combination.
       The new name must be unique across all combos and load cases.

API Signature:
  SapModel.RespCombo.ChangeName(Name, NewName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name    : str — Existing load combination name
  NewName : str — New name for the combination
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("OLD_NAME", 0)
assert ret == 0

# --- Target function ---
ret = SapModel.RespCombo.ChangeName("OLD_NAME", "NEW_NAME")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"ChangeName failed: {ret_code}"

# Verify
raw = SapModel.RespCombo.GetNameList(0, [])
assert raw[-1] == 0
combo_names = list(raw[1])
assert "NEW_NAME" in combo_names, f"NEW_NAME not found in: {combo_names}"
assert "OLD_NAME" not in combo_names, f"OLD_NAME still exists in: {combo_names}"

# --- Result ---
result["function"] = "SapModel.RespCombo.ChangeName"
result["old_name"] = "OLD_NAME"
result["new_name"] = "NEW_NAME"
result["status"] = "verified"
