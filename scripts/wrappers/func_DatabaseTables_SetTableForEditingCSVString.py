# ============================================================
# Wrapper: SapModel.DatabaseTables.SetTableForEditingCSVString
# Category: Database_Tables
# Description: Import table data from a CSV string for editing
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Reads a table from a CSV-formatted string and stages it for
       import via ApplyEditedTables.

API Signature (VBA):
  SapModel.DatabaseTables.SetTableForEditingCSVString(TableKey,
      TableVersion, csvString, sepChar)

ByRef Output (COM Python):
  raw[0] = TableVersion (int)
  raw[-1] = ret_code    (0=success)

Parameters:
  TableKey  : str — Table key
  csvString : str — CSV-formatted data string
  sepChar   : str — Delimiter (default ",")
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0, f"SetPresentUnits failed: {ret}"

ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Discover editable non-empty table
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0
all_keys = list(raw_tables[1])
all_import = list(raw_tables[3])
all_empty = list(raw_tables[4])
test_key = None
for i, k in enumerate(all_keys):
    if all_import[i] >= 2 and not all_empty[i]:
        test_key = k
        break
assert test_key is not None

# Export as CSV string first
raw = SapModel.DatabaseTables.GetTableForEditingCSVString(
    test_key, "All", 0, "", ","
)
assert raw[-1] == 0, f"GetTableForEditingCSVString failed: {raw[-1]}"
csv_string = raw[1]
SapModel.DatabaseTables.CancelTableEditing()

assert csv_string and len(csv_string) > 0, "CSV string is empty"

# --- Target function: re-import the CSV string ---
raw = SapModel.DatabaseTables.SetTableForEditingCSVString(
    test_key, 0, csv_string, ","
)
table_version = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"SetTableForEditingCSVString failed: {ret_code}"

# Clean up
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.SetTableForEditingCSVString"
result["table_key"] = test_key
result["table_version"] = table_version
result["csv_string_length"] = len(csv_string)
result["status"] = "verified"
