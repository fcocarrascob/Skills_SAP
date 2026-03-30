# ============================================================
# Wrapper: SapModel.DesignSteel.GetCode
# Category: Design
# Description: Retrieve current steel design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the currently set steel design code name.

API Signature:
  SapModel.DesignSteel.GetCode(CodeName)

ByRef Output:
  [CodeName, ret_code]

Parameters:
  CodeName : str — (ByRef out) Steel design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
raw = SapModel.DesignSteel.GetCode("")
ret_code = raw[-1]
assert ret_code == 0, f"GetCode failed: {ret_code}"
code_name = raw[0]

# --- Result ---
result["function"] = "SapModel.DesignSteel.GetCode"
result["code_name"] = code_name
result["byref_layout"] = "[CodeName, ret_code]"
result["status"] = "verified"
