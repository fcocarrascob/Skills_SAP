# ============================================================
# Wrapper: SapModel.PropFrame.SetPipe
# Category: PropFrame
# Description: Define a circular pipe (hollow) frame section
# Verified: 2026-03-28
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a circular pipe (hollow tube) section.
       Common for columns, braces, and truss elements.

API Signature:
  SapModel.PropFrame.SetPipe(Name, MatProp, T3, TW, Color, Notes, GUID)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name    : str   — Section name
  MatProp : str   — Material property name
  T3      : float — Outer diameter [L]
  TW      : float — Wall thickness [L]
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
ret = SapModel.PropMaterial.SetMaterial("STEEL_PIPE", 1)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_PIPE", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# Pipe 200x8 (OD=200mm, t=8mm)
ret = SapModel.PropFrame.SetPipe(
    "PIPE_200x8", "STEEL_PIPE",
    0.200,   # T3 — outer diameter
    0.008    # TW — wall thickness
)
assert ret == 0, f"SetPipe(200x8) failed: {ret}"

# Pipe 300x10
ret = SapModel.PropFrame.SetPipe(
    "PIPE_300x10", "STEEL_PIPE",
    0.300,   # T3
    0.010    # TW
)
assert ret == 0, f"SetPipe(300x10) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])
assert "PIPE_200x8" in section_names, f"PIPE_200x8 not found in: {section_names}"
assert "PIPE_300x10" in section_names, f"PIPE_300x10 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetPipe"
result["sections_created"] = ["PIPE_200x8", "PIPE_300x10"]
result["section_count"] = raw[0]
result["status"] = "verified"
