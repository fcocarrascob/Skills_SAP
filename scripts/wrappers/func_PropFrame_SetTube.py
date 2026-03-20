# ============================================================
# Wrapper: SapModel.PropFrame.SetTube
# Category: PropFrame
# Description: Define a rectangular tube (HSS) frame section
# Verified: 2026-03-20
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a rectangular hollow structural section (HSS/tube).
       Common for braces, columns, and truss elements.

API Signature:
  SapModel.PropFrame.SetTube(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Overall depth (outer height) [L]
  T2      : float — Overall width (outer width) [L]
  TF      : float — Flange thickness (top/bottom wall) [L]
  TW      : float — Web thickness (left/right wall) [L]
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
# HSS 200x200x8 (in meters)
ret = SapModel.PropFrame.SetTube(
    "HSS_200x200x8", "STEEL_TEST",
    0.200,   # T3 — outer depth
    0.200,   # T2 — outer width
    0.008,   # TF — flange wall thickness
    0.008    # TW — web wall thickness
)
assert ret == 0, f"SetTube(HSS_200x200x8) failed: {ret}"

# HSS 300x150x10 (rectangular)
ret = SapModel.PropFrame.SetTube(
    "HSS_300x150x10", "STEEL_TEST",
    0.300,   # T3
    0.150,   # T2
    0.010,   # TF
    0.010    # TW
)
assert ret == 0, f"SetTube(HSS_300x150x10) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "HSS_200x200x8" in section_names, f"HSS_200x200x8 not found in: {section_names}"
assert "HSS_300x150x10" in section_names, f"HSS_300x150x10 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetTube"
result["sections_created"] = ["HSS_200x200x8", "HSS_300x150x10"]
result["section_count"] = raw[0]
result["status"] = "verified"
