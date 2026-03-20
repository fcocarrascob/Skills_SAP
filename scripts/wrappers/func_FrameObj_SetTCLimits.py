# ============================================================
# Wrapper: SapModel.FrameObj.SetTCLimits
# Category: Object_Model
# Description: Set tension/compression force limits for a frame
# Verified: 2026-03-20
# Prerequisites: Model open, frame object exists
# ============================================================
"""
Usage: Assigns tension and/or compression force limits to a frame
       element. Used to model tension-only members (cables, braces)
       or compression-only members (struts). Forces exceeding the
       limit cause the member to be deactivated in that direction.

API Signature:
  SapModel.FrameObj.SetTCLimits(Name, LimitCompressionExists,
      LimitCompression, LimitTensionExists, LimitTension, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name                    : str   — Frame object name
  LimitCompressionExists  : bool  — True = apply compression limit
  LimitCompression        : float — Max compression force [F] (negative value)
  LimitTensionExists      : bool  — True = apply tension limit
  LimitTension            : float — Max tension force [F] (positive value)
  ItemType                : int   — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, and frames ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("STEEL_TEST", 2.0e8, 0.3, 1.2e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_BR", "STEEL_TEST", 0.1, 0.1)
assert ret == 0, f"SetRectangle failed: {ret}"

# Create a tension-only brace (diagonal)
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 4, 0, 3, "", "SEC_BR", "BRACE_T")
brace_t = raw[0]
assert raw[-1] == 0, f"AddByCoord(BRACE_T) failed: {raw[-1]}"

# Create a compression-only strut (horizontal)
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_BR", "STRUT_C")
strut_c = raw[0]
assert raw[-1] == 0, f"AddByCoord(STRUT_C) failed: {raw[-1]}"

# --- Target function ---
# Tension-only: set compression limit to 0 (no compression allowed)
ret = SapModel.FrameObj.SetTCLimits(
    brace_t,
    True,    # LimitCompressionExists
    0.0,     # LimitCompression = 0 (compression-only member cannot carry compression)
    False,   # LimitTensionExists = False
    0.0,     # LimitTension (not used)
    0        # ItemType = Object
)
assert ret == 0, f"SetTCLimits(tension-only) failed: {ret}"

# Compression-only: set tension limit to 0 (no tension allowed)
ret = SapModel.FrameObj.SetTCLimits(
    strut_c,
    False,   # LimitCompressionExists = False
    0.0,     # LimitCompression (not used)
    True,    # LimitTensionExists
    0.0,     # LimitTension = 0 (cannot carry tension)
    0        # ItemType = Object
)
assert ret == 0, f"SetTCLimits(compression-only) failed: {ret}"

# --- Verification ---
# Read back TC limits for tension-only brace
raw = SapModel.FrameObj.GetTCLimits(brace_t, False, 0, False, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetTCLimits(brace) failed: {ret_code}"
comp_exists = raw[0]
assert comp_exists == True, f"Expected compression limit to exist on brace"

# Read back TC limits for compression-only strut
raw = SapModel.FrameObj.GetTCLimits(strut_c, False, 0, False, 0)
ret_code = raw[-1]
assert ret_code == 0, f"GetTCLimits(strut) failed: {ret_code}"
tension_exists = raw[2]
assert tension_exists == True, f"Expected tension limit to exist on strut"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetTCLimits"
result["tension_only_brace"] = brace_t
result["compression_only_strut"] = strut_c
result["status"] = "verified"
