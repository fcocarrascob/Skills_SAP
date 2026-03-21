# ============================================================
# Wrapper: SapModel.PropFrame.SetAngle
# Category: PropFrame
# Description: Define an L-shape angle section
# Verified: 2026-03-21
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates an angle (L-shape) cross-section for frame elements.
       Common for bracing, truss members, and connections.

API Signature:
  SapModel.PropFrame.SetAngle(Name, MatProp, T3, T2, TF, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Vertical leg depth [L]
  T2      : float — Horizontal leg width [L]
  TF      : float — Flange (horizontal leg) thickness [L]
  TW      : float — Web (vertical leg) thickness [L]
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
# L100x100x10 equal angle
ret = SapModel.PropFrame.SetAngle(
    "L100x100x10", "STEEL_TEST",
    0.100,   # T3 — vertical leg
    0.100,   # T2 — horizontal leg
    0.010,   # TF — flange thickness
    0.010    # TW — web thickness
)
assert ret == 0, f"SetAngle(L100x100x10) failed: {ret}"

# L150x75x10 unequal angle
ret = SapModel.PropFrame.SetAngle(
    "L150x75x10", "STEEL_TEST",
    0.150,   # T3
    0.075,   # T2
    0.010,   # TF
    0.010    # TW
)
assert ret == 0, f"SetAngle(L150x75x10) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "L100x100x10" in section_names, f"L100x100x10 not found in: {section_names}"
assert "L150x75x10" in section_names, f"L150x75x10 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetAngle"
result["sections_created"] = ["L100x100x10", "L150x75x10"]
result["section_count"] = raw[0]
result["status"] = "verified"
