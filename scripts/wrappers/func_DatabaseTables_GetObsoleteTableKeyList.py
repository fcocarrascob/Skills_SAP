# ============================================================
# Wrapper: SapModel.DatabaseTables.GetObsoleteTableKeyList
# Category: Database_Tables
# Description: Returns list of obsolete table keys and associated notes
# Verified: true
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Retrieves all obsolete table keys in the program.
       Useful for migration and compatibility checks.

API Signature (VBA):
  SapModel.DatabaseTables.GetObsoleteTableKeyList(NumberTableKeys,
      TableKeyList(), NotesList())

ByRef Output (COM Python):
  raw[0] = NumberTableKeys (int)
  raw[1] = TableKeyList[]  (tuple of str)
  raw[2] = NotesList[]     (tuple of str)
  raw[-1] = ret_code       (0=success)

Parameters:
  (none — all outputs are ByRef)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Add minimal model content
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# --- Target function ---
raw = SapModel.DatabaseTables.GetObsoleteTableKeyList(0, [], [])
num_keys = raw[0]
table_key_list = list(raw[1]) if raw[1] else []
notes_list = list(raw[2]) if raw[2] else []
ret_code = raw[-1]
assert ret_code == 0, f"GetObsoleteTableKeyList failed: {ret_code}"

# --- Verification ---
# num_keys may be 0 if no obsolete tables exist — that's valid
assert num_keys >= 0, f"Unexpected negative count: {num_keys}"
assert len(table_key_list) == num_keys, "TableKeyList count mismatch"
assert len(notes_list) == num_keys, "NotesList count mismatch"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetObsoleteTableKeyList"
result["num_obsolete_keys"] = num_keys
result["sample_keys"] = table_key_list[:10]
result["sample_notes"] = notes_list[:10]
result["status"] = "verified"
