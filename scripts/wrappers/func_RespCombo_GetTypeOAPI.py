# ============================================================
# Wrapper: SapModel.RespCombo.GetTypeOAPI
# Category: RespCombo
# Description: Get the type of a load combination
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Retrieves the type of an existing load combination.
       Types: 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS, 4=RangeAdd.

API Signature:
  SapModel.RespCombo.GetTypeOAPI(Name)

ByRef Output:
  [ComboType, ret_code]

Parameters:
  Name : str — Existing load combination name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: create combo as envelope ---
ret = SapModel.RespCombo.Add("GTYPE_TEST", 1)  # 1=Envelope
assert ret == 0

# --- Target function ---
raw = SapModel.RespCombo.GetTypeOAPI("GTYPE_TEST")
ret_code = raw[-1]
assert ret_code == 0, f"GetTypeOAPI failed: {ret_code}"
combo_type = raw[0]
assert combo_type == 1, f"Expected type=1 (Envelope), got {combo_type}"

# Change type and verify
ret = SapModel.RespCombo.SetTypeOAPI("GTYPE_TEST", 3)  # SRSS
ret_code2 = ret[-1] if isinstance(ret, (list, tuple)) else ret
assert ret_code2 == 0

raw2 = SapModel.RespCombo.GetTypeOAPI("GTYPE_TEST")
assert raw2[-1] == 0
assert raw2[0] == 3, f"Expected type=3 (SRSS), got {raw2[0]}"

# --- Result ---
result["function"] = "SapModel.RespCombo.GetTypeOAPI"
result["initial_type"] = combo_type
result["changed_type"] = raw2[0]
result["byref_layout"] = "[ComboType, ret_code]"
result["status"] = "verified"
