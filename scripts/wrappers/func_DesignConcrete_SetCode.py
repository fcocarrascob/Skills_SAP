# ============================================================
# Wrapper: SapModel.DesignConcrete.SetCode
# Category: Design
# Description: Set the concrete design code
# Verified: 2026-03-28
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets the concrete design code for the model. Valid codes
       include ACI 318-14, ACI 318-11, EN 2-2004, CSA A23.3-14, etc.

API Signature:
  SapModel.DesignConcrete.SetCode(CodeName)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  CodeName : str — Concrete design code name
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignConcrete.SetCode("ACI 318-14")
assert ret == 0, f"SetCode('ACI 318-14') failed: {ret}"

# Verify via GetCode
raw = SapModel.DesignConcrete.GetCode("")
assert raw[-1] == 0, f"GetCode failed: {raw[-1]}"
assert raw[0] == "ACI 318-14", f"Code mismatch: expected 'ACI 318-14', got '{raw[0]}'"

# --- Result ---
result["function"] = "SapModel.DesignConcrete.SetCode"
result["code_set"] = "ACI 318-14"
result["code_verified"] = raw[0]
result["status"] = "verified"
