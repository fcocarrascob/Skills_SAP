# ============================================================
# Wrapper: SapModel.DesignSteel.SetCode
# Category: Design
# Description: Set the steel design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets the steel design code for the model. Valid code names
       include AISC 360-10, AISC-LRFD93, AISC-ASD89, EN 1993-1-1:2005, etc.

API Signature:
  SapModel.DesignSteel.SetCode(CodeName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  CodeName : str — Steel design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function: set and verify code ---
ret = SapModel.DesignSteel.SetCode("AISC 360-10")
assert ret == 0, f"SetCode('AISC 360-10') failed: {ret}"

# Verify via GetCode
raw = SapModel.DesignSteel.GetCode("")
assert raw[-1] == 0, f"GetCode failed: {raw[-1]}"
assert raw[0] == "AISC 360-10", f"Code mismatch: expected 'AISC 360-10', got '{raw[0]}'"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetCode"
result["code_set"] = "AISC 360-10"
result["code_verified"] = raw[0]
result["status"] = "verified"
