# ============================================================
# Wrapper: SapModel.PropFrame.SetRectangle
# Category: PropFrame
# Description: Define a rectangular (solid) frame section
# Verified: 2026-03-20
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a rectangular cross-section for frame elements.
       Common for concrete beams, columns, and braces.

API Signature:
  SapModel.PropFrame.SetRectangle(Name, MatProp, T3, T2, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Section depth (height) [L]
  T2      : float — Section width [L]
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
# Beam section: 0.6m deep x 0.3m wide
ret = SapModel.PropFrame.SetRectangle("BEAM_30x60", "CONC_TEST", 0.6, 0.3)
assert ret == 0, f"SetRectangle(BEAM) failed: {ret}"

# Column section: 0.5m x 0.5m
ret = SapModel.PropFrame.SetRectangle("COL_50x50", "CONC_TEST", 0.5, 0.5)
assert ret == 0, f"SetRectangle(COL) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "BEAM_30x60" in section_names, f"BEAM_30x60 not found in: {section_names}"
assert "COL_50x50" in section_names, f"COL_50x50 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetRectangle"
result["sections_created"] = ["BEAM_30x60", "COL_50x50"]
result["section_count"] = raw[0]
result["status"] = "verified"
