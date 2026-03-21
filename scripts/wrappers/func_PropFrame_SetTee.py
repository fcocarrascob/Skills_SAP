# ============================================================
# Wrapper: SapModel.PropFrame.SetTee
# Category: PropFrame
# Description: Define a T-shape section
# Verified: 2026-03-21
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a T-shape cross-section for frame elements.
       Common for cut W-shapes and composite construction.

API Signature:
  SapModel.PropFrame.SetTee(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth (stem + flange) [L]
  T2      : float — Flange width [L]
  TF      : float — Flange thickness [L]
  TW      : float — Stem (web) thickness [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define steel material ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# WT155x33 equivalent (cut from W310)
ret = SapModel.PropFrame.SetTee(
    "WT155x33", "STEEL_TEST",
    0.154,   # T3 — overall depth
    0.205,   # T2 — flange width
    0.0154,  # TF — flange thickness
    0.00991  # TW — stem thickness
)
assert ret == 0, f"SetTee(WT155x33) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "WT155x33" in section_names, f"WT155x33 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetTee"
result["sections_created"] = ["WT155x33"]
result["section_count"] = raw[0]
result["status"] = "verified"
