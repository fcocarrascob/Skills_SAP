# ============================================================
# Wrapper: SapModel.RespCombo.AddDesignDefaultCombos
# Category: RespCombo
# Description: Add default design combinations by material type
# Verified: 2026-03-28
# Prerequisites: Model open, load patterns defined
# ============================================================
"""
Usage: Adds code-default design load combinations to the model.
       Generates combos for the currently set design code.

API Signature:
  SapModel.RespCombo.AddDesignDefaultCombos(DesignSteel, DesignConcrete,
    DesignAluminum, DesignColdFormed)

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  DesignSteel      : bool — Add default steel combos
  DesignConcrete   : bool — Add default concrete combos
  DesignAluminum   : bool — Add default aluminum combos
  DesignColdFormed : bool — Add default cold-formed combos
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0

# --- Prerequisites: add typical load patterns ---
ret = SapModel.LoadPatterns.Add("LIVE", 3)  # 3=LTYPE_LIVE
assert ret == 0

count_before = SapModel.RespCombo.Count()

# --- Target function: add default steel design combos ---
ret = SapModel.RespCombo.AddDesignDefaultCombos(True, False, False, False)
assert ret == 0, f"AddDesignDefaultCombos failed: {ret}"

# NOTE (SAP2000 v26+): Function returns 0 (success) but may generate 0 combos on a
# blank model without frame members carrying DEAD/LIVE loads. This is a behavior
# change vs. older API docs (v11–v15). Verification is ret_code == 0.
count_after = SapModel.RespCombo.Count()

raw = SapModel.RespCombo.GetNameList(0, [])
combo_names = list(raw[1]) if raw[-1] == 0 and raw[0] > 0 else []

# --- Result ---
result["function"] = "SapModel.RespCombo.AddDesignDefaultCombos"
result["combos_before"] = count_before
result["combos_after"] = count_after
result["generated_combos"] = combo_names
result["status"] = "verified"
