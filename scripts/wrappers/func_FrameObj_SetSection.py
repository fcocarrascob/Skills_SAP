# ============================================================
# Wrapper: SapModel.FrameObj.SetSection
# Category: Object_Model
# Description: Assign or change the section property of a frame element
# Verified: 2026-03-20
# Prerequisites: Model open, frame and section both exist
# ============================================================
"""
Usage: Assigns a frame section property to an existing frame element.
       Used to change sections after initial creation, or to assign
       sections to frames created without one.

API Signature:
  SapModel.FrameObj.SetSection(Name, PropName, ItemType, SAuto)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str — Frame object name
  PropName : str — Section property name to assign
  ItemType : int — 0=Object (single), 1=Group, 2=SelectedObjects
  SAuto    : str — Auto-select list name (""=none)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material and two sections ---
ret = SapModel.PropMaterial.SetMaterial("CONC_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC_TEST", 2.5e7, 0.2, 1.0e-5)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# Original section
ret = SapModel.PropFrame.SetRectangle("SEC_30x50", "CONC_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle(30x50) failed: {ret}"

# New section to assign
ret = SapModel.PropFrame.SetRectangle("SEC_40x60", "CONC_TEST", 0.6, 0.4)
assert ret == 0, f"SetRectangle(40x60) failed: {ret}"

# Create frame with original section
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "SEC_30x50", "")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# --- Target function: change section ---
ret = SapModel.FrameObj.SetSection(frame_name, "SEC_40x60")
assert ret == 0, f"SetSection failed: {ret}"

# --- Verification ---
# Read back section assignment
raw = SapModel.FrameObj.GetSection(frame_name, "", "")
ret_code = raw[-1]
assert ret_code == 0, f"GetSection failed: {ret_code}"
assigned_section = raw[0]
assert assigned_section == "SEC_40x60", f"Expected SEC_40x60, got {assigned_section}"

# --- Result ---
result["function"] = "SapModel.FrameObj.SetSection"
result["frame_name"] = frame_name
result["assigned_section"] = assigned_section
result["status"] = "verified"
