# ============================================================
# Wrapper: SapModel.PropFrame.SetPipe
# Category: PropFrame
# Description: Define a circular hollow section (pipe/HSS round)
# Verified: 2026-03-21
# Prerequisites: Model open, material defined
# ============================================================
"""
Usage: Creates a circular hollow structural section (pipe/CHS).
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
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)  # Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# --- Target function ---
# Pipe D=0.3m, t=0.010m
ret = SapModel.PropFrame.SetPipe("PIPE_D300x10", "STEEL_TEST", 0.300, 0.010)
assert ret == 0, f"SetPipe(PIPE_D300x10) failed: {ret}"

# Smaller pipe
ret = SapModel.PropFrame.SetPipe("PIPE_D168x8", "STEEL_TEST", 0.168, 0.008)
assert ret == 0, f"SetPipe(PIPE_D168x8) failed: {ret}"

# --- Verification ---
raw = SapModel.PropFrame.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
section_names = list(raw[1])

assert "PIPE_D300x10" in section_names, f"PIPE_D300x10 not found in: {section_names}"
assert "PIPE_D168x8" in section_names, f"PIPE_D168x8 not found in: {section_names}"

# --- Result ---
result["function"] = "SapModel.PropFrame.SetPipe"
result["sections_created"] = ["PIPE_D300x10", "PIPE_D168x8"]
result["section_count"] = raw[0]
result["status"] = "verified"
