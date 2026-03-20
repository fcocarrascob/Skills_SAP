# ============================================================
# Wrapper: SapModel.RespCombo.Add
# Category: RespCombo
# Description: Create a new response combination
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a named load combination. Combos can later be populated
       with load cases and scale factors via SetCaseList. Combo types
       include linear, envelope, absolute, and SRSS.

API Signature:
  SapModel.RespCombo.Add(Name, ComboType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name      : str — Combination name
  ComboType : int — 0=LinearAdd, 1=Envelope, 2=AbsoluteAdd, 3=SRSS,
                     4=RangeAdd
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: create combinations of different types ---
# Linear add combination (1.2D + 1.6L)
ret = SapModel.RespCombo.Add("COMB_1.2D+1.6L", 0)  # 0=LinearAdd
assert ret == 0, f"RespCombo.Add(linear) failed: {ret}"

# Envelope combination
ret = SapModel.RespCombo.Add("ENV_GRAVITY", 1)  # 1=Envelope
assert ret == 0, f"RespCombo.Add(envelope) failed: {ret}"

# SRSS combination (for seismic)
ret = SapModel.RespCombo.Add("SRSS_SISMO", 3)  # 3=SRSS
assert ret == 0, f"RespCombo.Add(SRSS) failed: {ret}"

# --- Verification ---
raw = SapModel.RespCombo.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
combo_names = list(raw[1])

assert "COMB_1.2D+1.6L" in combo_names, f"COMB_1.2D+1.6L not found in: {combo_names}"
assert "ENV_GRAVITY" in combo_names, f"ENV_GRAVITY not found in: {combo_names}"
assert "SRSS_SISMO" in combo_names, f"SRSS_SISMO not found in: {combo_names}"

# --- Result ---
result["function"] = "SapModel.RespCombo.Add"
result["combos_created"] = ["COMB_1.2D+1.6L", "ENV_GRAVITY", "SRSS_SISMO"]
result["combo_count"] = raw[0]
result["status"] = "verified"
