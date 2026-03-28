# ============================================================
# Wrapper: SapModel.DesignSteel.SetComboStrength
# Category: Design
# Description: Select/deselect a combo for steel strength design
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Selects or deselects a load combination for steel strength
       design. Must be called after creating combinations.

API Signature:
  SapModel.DesignSteel.SetComboStrength(Name, Selected)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str  — Existing load combination name
  Selected : bool — True=select for strength design, False=deselect
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: create combos ---
ret = SapModel.RespCombo.Add("LRFD_1", 0)
assert ret == 0, f"RespCombo.Add(LRFD_1) failed: {ret}"
ret = SapModel.RespCombo.Add("LRFD_2", 0)
assert ret == 0, f"RespCombo.Add(LRFD_2) failed: {ret}"

# --- Target function: select combos for strength design ---
ret = SapModel.DesignSteel.SetComboStrength("LRFD_1", True)
assert ret == 0, f"SetComboStrength(LRFD_1, True) failed: {ret}"

ret = SapModel.DesignSteel.SetComboStrength("LRFD_2", True)
assert ret == 0, f"SetComboStrength(LRFD_2, True) failed: {ret}"

# Deselect one
ret = SapModel.DesignSteel.SetComboStrength("LRFD_2", False)
assert ret == 0, f"SetComboStrength(LRFD_2, False) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignSteel.SetComboStrength"
result["combos_selected"] = ["LRFD_1"]
result["combos_deselected"] = ["LRFD_2"]
result["status"] = "verified"
