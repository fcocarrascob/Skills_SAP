# ============================================================
# Wrapper: SapModel.RespCombo.SetTypeOAPI
# Category: RespCombo
# Description: Set the type of a load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Sets or changes the type of an existing load combination.
       Types: 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=RangeAdd.

API Signature:
  SapModel.RespCombo.SetTypeOAPI(Name, ComboType)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name      : str — Existing load combination name
  ComboType : int — 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=RangeAdd
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create combo as linear ---
ret = SapModel.RespCombo.Add("TYPE_TEST", 0)  # LinearAdd
assert ret == 0

# --- Target function: change type to Envelope ---
ret = SapModel.RespCombo.SetTypeOAPI("TYPE_TEST", 1)  # Envelope
ret_code = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code == 0, f"SetTypeOAPI failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.RespCombo.SetTypeOAPI"
result["combo"] = "TYPE_TEST"
result["new_type"] = 1
result["status"] = "verified"
