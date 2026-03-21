# ============================================================
# Wrapper: SapModel.DesignSteel.SetCode
# Category: Design
# Description: Set the steel design code for the model
# Verified: 2026-03-21
# Prerequisites: Model open
# ============================================================
"""
Usage: Sets the steel frame design code used for design checks.
       Must be called before running steel design (StartDesign).

API Signature:
  SapModel.DesignSteel.SetCode(CodeName) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  CodeName : str — Design code name (e.g., "AISC 360-16",
                   "EN 1993-1-1:2005", "BS 5950-2000", "CSA S16-19")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# --- Target function ---
# Set AISC 360-16
ret = SapModel.DesignSteel.SetCode("AISC 360-16")
assert ret == 0, f"SetCode(AISC 360-16) failed: {ret}"

# Verify: read back code
raw = SapModel.DesignSteel.GetCode("")
ret_code = raw[-1]
assert ret_code == 0, f"GetCode failed: {ret_code}"
code_name = raw[0]
assert "AISC" in code_name, f"Expected AISC code, got: {code_name}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetCode"
result["code_set"] = "AISC 360-16"
result["code_read_back"] = code_name
result["status"] = "verified"
