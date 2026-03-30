# ============================================================
# Wrapper: SapModel.RespCombo.DeleteCase
# Category: RespCombo
# Description: Remove a load case or combo from a combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo with cases assigned
# ============================================================
"""
Usage: Deletes one load case or load combination from the list
       of cases included in a specified load combination.

API Signature:
  SapModel.RespCombo.DeleteCase(Name, CType, CName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name  : str — Load combination name
  CType : int — 0=LoadCase, 1=LoadCombo
  CName : str — Name of the case/combo to remove
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create combo with cases ---
ret = SapModel.RespCombo.Add("DELCASE_TEST", 0)
assert ret == 0

# Add DEAD case to combo (DEAD is auto-created in blank model as a load case)
ret = SapModel.RespCombo.SetCaseList("DELCASE_TEST", 0, "DEAD", 1.4)
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"SetCaseList failed: {ret_code}"

# --- Target function: delete DEAD from combo ---
ret = SapModel.RespCombo.DeleteCase("DELCASE_TEST", 0, "DEAD")
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"DeleteCase failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.RespCombo.DeleteCase"
result["combo"] = "DELCASE_TEST"
result["deleted_case"] = "DEAD"
result["status"] = "verified"
