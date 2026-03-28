# ============================================================
# Wrapper: SapModel.PropFrame.SetAngle
# Category: PropFrame
# Description: Define an angle (L-shape) frame section
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates an angle (L) cross-section for frame elements.
       Common for bracing and secondary structural members.

API Signature:
  SapModel.PropFrame.SetAngle(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Vertical leg depth [L]
  T2      : float — Horizontal leg width [L]
  TF      : float — Flange thickness (horizontal leg) [L]
  TW      : float — Web thickness (vertical leg) [L]
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
ret = SapModel.PropMaterial.SetMaterial("STEEL_ANG", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_ANG", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# L75x75x6 (in meters)
ret = SapModel.PropFrame.SetAngle(
    "L75x75x6", "STEEL_ANG",
    0.075,   # T3 — vertical leg
    0.075,   # T2 — horizontal leg
    0.006,   # TF — flange thickness
    0.006,   # TW — web thickness
    -1, "", ""
)
assert ret == 0, f"SetAngle(L75x75x6) failed: {ret}"

# L100x75x8 (unequal legs)
ret = SapModel.PropFrame.SetAngle(
    "L100x75x8", "STEEL_ANG",
    0.100,   # T3
    0.075,   # T2
    0.008,   # TF
    0.008,   # TW
    -1, "", ""
)
assert ret == 0, f"SetAngle(L100x75x8) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])
assert "L75x75x6" in section_names, f"L75x75x6 not found in: {section_names}"
assert "L100x75x8" in section_names, f"L100x75x8 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetAngle"
result["sections_created"] = ["L75x75x6", "L100x75x8"]
result["section_count"] = raw[0]
result["status"] = "verified"
