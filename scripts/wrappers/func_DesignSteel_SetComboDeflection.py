# ============================================================
# Wrapper: SapModel.DesignSteel.SetComboDeflection
# Category: Design
# Description: Select/deselect a combo for steel deflection design
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Selects or deselects a load combination for steel deflection
       design (serviceability check).

API Signature:
  SapModel.DesignSteel.SetComboDeflection(Name, Selected)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str  — Existing load combination name
  Selected : bool — True=select for deflection design, False=deselect
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("DEFL_SERV", 0)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignSteel.SetComboDeflection("DEFL_SERV", True)
assert ret == 0, f"SetComboDeflection(True) failed: {ret}"

ret = SapModel.DesignSteel.SetComboDeflection("DEFL_SERV", False)
assert ret == 0, f"SetComboDeflection(False) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetComboDeflection"
result["status"] = "verified"
