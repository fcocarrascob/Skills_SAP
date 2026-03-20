# ============================================================
# Wrapper: SapModel.PropFrame.SetCircle
# Category: PropFrame
# Description: Define a solid circular frame section
# Verified: 2026-03-20
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a solid circular cross-section for frame elements.
       Common for piles, drilled shafts, and circular columns.

API Signature:
  SapModel.PropFrame.SetCircle(Name, MatProp, T3, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Diameter [L]
  Color   : int   — Display color (optional, -1=default)
  Notes   : str   — Notes (optional, ""=none)
  GUID    : str   — GUID (optional, ""=auto)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: define material ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)  # Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# Circular column: diameter 0.6m
ret = SapModel.PropFrame.SetCircle("CIRC_D60", "CONC_TEST", 0.6)
assert ret == 0, f"SetCircle failed: {ret}"

# Pile: diameter 0.4m
ret = SapModel.PropFrame.SetCircle("PILE_D40", "CONC_TEST", 0.4)
assert ret == 0, f"SetCircle(PILE) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "CIRC_D60" in section_names, f"CIRC_D60 not found in: {section_names}"
assert "PILE_D40" in section_names, f"PILE_D40 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetCircle"
result["sections_created"] = ["CIRC_D60", "PILE_D40"]
result["section_count"] = raw[0]
result["status"] = "verified"
