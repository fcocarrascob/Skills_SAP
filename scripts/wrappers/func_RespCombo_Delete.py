# ============================================================
# Wrapper: SapModel.RespCombo.Delete
# Category: RespCombo
# Description: Delete an existing load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Deletes a specified load combination from the model.

API Signature:
  SapModel.RespCombo.Delete(Name)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Name of existing load combination to delete
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("TEMP_COMBO", 0)
assert ret == 0

# Verify it exists
raw = SapModel.RespCombo.GetNameList(0, [])
assert raw[-1] == 0
assert "TEMP_COMBO" in list(raw[1])

# --- Target function ---
ret = SapModel.RespCombo.Delete("TEMP_COMBO")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"Delete failed: {ret_code}"

# Verify it's gone
raw2 = SapModel.RespCombo.GetNameList(0, [])
if raw2[-1] == 0 and raw2[0] > 0:
    combo_names = list(raw2[1])
    assert "TEMP_COMBO" not in combo_names, f"TEMP_COMBO still exists after delete"

# --- Result ---
result["function"] = "SapModel.RespCombo.Delete"
result["deleted"] = "TEMP_COMBO"
result["status"] = "verified"
