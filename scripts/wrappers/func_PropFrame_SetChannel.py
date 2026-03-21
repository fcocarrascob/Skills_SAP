# ============================================================
# Wrapper: SapModel.PropFrame.SetChannel
# Category: PropFrame
# Description: Define a C-shape channel section
# Verified: 2026-03-21
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a channel (C-shape) cross-section for frame elements.
       Common for purlins, girts, and light structural members.

API Signature:
  SapModel.PropFrame.SetChannel(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth [L]
  T2      : float — Flange width [L]
  TF      : float — Flange thickness [L]
  TW      : float — Web thickness [L]
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
# C250x30 equivalent (approximate dimensions in meters)
ret = SapModel.PropFrame.SetChannel(
    "C250x30", "STEEL_TEST",
    0.254,   # T3 — overall depth
    0.076,   # T2 — flange width
    0.011,   # TF — flange thickness
    0.006    # TW — web thickness
)
assert ret == 0, f"SetChannel(C250x30) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "C250x30" in section_names, f"C250x30 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetChannel"
result["sections_created"] = ["C250x30"]
result["section_count"] = raw[0]
result["status"] = "verified"
