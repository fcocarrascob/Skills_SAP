# ============================================================
# Wrapper: SapModel.PropFrame.SetChannel
# Category: PropFrame
# Description: Define a channel (C-shape) frame section
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a channel (C) cross-section for frame elements.
       Common for purlins, girts, and secondary framing.

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
ret = SapModel.PropMaterial.SetMaterial("STEEL_CH", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_CH", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# C200x75 (in meters)
ret = SapModel.PropFrame.SetChannel(
    "C200x75", "STEEL_CH",
    0.200,   # T3 — depth
    0.075,   # T2 — flange width
    0.0109,  # TF — flange thickness
    0.0059,  # TW — web thickness
    -1, "", ""
)
assert ret == 0, f"SetChannel(C200x75) failed: {ret}"

# C150x50
ret = SapModel.PropFrame.SetChannel(
    "C150x50", "STEEL_CH",
    0.150, 0.050, 0.009, 0.005,
    -1, "", ""
)
assert ret == 0, f"SetChannel(C150x50) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])
assert "C200x75" in section_names, f"C200x75 not found in: {section_names}"
assert "C150x50" in section_names, f"C150x50 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetChannel"
result["sections_created"] = ["C200x75", "C150x50"]
result["section_count"] = raw[0]
result["status"] = "verified"
