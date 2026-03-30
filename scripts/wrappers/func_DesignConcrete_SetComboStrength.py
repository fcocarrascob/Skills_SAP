# ============================================================
# Wrapper: SapModel.DesignConcrete.SetComboStrength
# Category: Design
# Description: Select/deselect a combo for concrete strength design
# Verified: 2026-03-28
# Prerequisites: Model open, combo defined
# ============================================================
"""
Usage: Selects or deselects a load combination for concrete strength
       design. Similar to DesignSteel.SetComboStrength but for concrete.

API Signature:
  SapModel.DesignConcrete.SetComboStrength(Name, Selected)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str  — Existing load combination name
  Selected : bool — True=select for concrete strength design
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites ---
ret = SapModel.RespCombo.Add("CONC_STR1", 0)
assert ret == 0
ret = SapModel.RespCombo.Add("CONC_STR2", 0)
assert ret == 0

# --- Target function ---
ret = SapModel.DesignConcrete.SetComboStrength("CONC_STR1", True)
assert ret == 0, f"SetComboStrength(CONC_STR1) failed: {ret}"

ret = SapModel.DesignConcrete.SetComboStrength("CONC_STR2", True)
assert ret == 0, f"SetComboStrength(CONC_STR2) failed: {ret}"

# Deselect
ret = SapModel.DesignConcrete.SetComboStrength("CONC_STR2", False)
assert ret == 0, f"SetComboStrength(deselect) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.DesignConcrete.SetComboStrength"
result["combos_selected"] = ["CONC_STR1"]
result["status"] = "verified"
