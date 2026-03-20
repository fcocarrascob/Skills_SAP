# ============================================================
# Wrapper: SapModel.PropFrame.SetISection
# Category: PropFrame
# Description: Define a general I-section (W-shape / H-beam)
# Verified: 2026-03-20
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a general I/H section for frame elements.
       Allows different top/bottom flanges (asymmetric I-shape).
       For standard W-shapes use equal flanges (t2=t2b, tf=tfb).

API Signature:
  SapModel.PropFrame.SetISection(Name, MatProp, T3, T2, TF, TW, T2B, TFB, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth [L]
  T2      : float — Top flange width [L]
  TF      : float — Top flange thickness [L]
  TW      : float — Web thickness [L]
  T2B     : float — Bottom flange width [L]
  TFB     : float — Bottom flange thickness [L]
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
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# W310x97 equivalent (approximate dimensions in meters):
#   T3=0.308m, T2=0.305m, TF=0.0154m, TW=0.00991m, T2B=0.305m, TFB=0.0154m
ret = SapModel.PropFrame.SetISection(
    "W310x97", "STEEL_TEST",
    0.308,    # T3 — overall depth
    0.305,    # T2 — top flange width
    0.0154,   # TF — top flange thickness
    0.00991,  # TW — web thickness
    0.305,    # T2B — bottom flange width
    0.0154    # TFB — bottom flange thickness
)
assert ret == 0, f"SetISection(W310x97) failed: {ret}"

# Asymmetric I-section (different bottom flange)
ret = SapModel.PropFrame.SetISection(
    "ASYM_I", "STEEL_TEST",
    0.500,    # T3
    0.200,    # T2  — narrow top flange
    0.015,    # TF
    0.010,    # TW
    0.300,    # T2B — wider bottom flange
    0.020     # TFB — thicker bottom flange
)
assert ret == 0, f"SetISection(ASYM_I) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "W310x97" in section_names, f"W310x97 not found in: {section_names}"
assert "ASYM_I" in section_names, f"ASYM_I not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetISection"
result["sections_created"] = ["W310x97", "ASYM_I"]
result["section_count"] = raw[0]
result["status"] = "verified"
