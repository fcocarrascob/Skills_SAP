# ============================================================
# Wrapper: SapModel.DatabaseTables.SetTableForEditingCSVFile
# Category: Database_Tables
# Description: Import table data from a CSV file for editing
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data, CSV file exists
# ============================================================
"""
Usage: Reads a table from a CSV file and stages it for import via
       ApplyEditedTables.

API Signature (VBA):
  SapModel.DatabaseTables.SetTableForEditingCSVFile(TableKey,
      TableVersion, csvFilePath, sepChar)

ByRef Output (COM Python):
  raw[0] = TableVersion (int)
  raw[-1] = ret_code    (0=success)

Parameters:
  TableKey    : str — Table key
  csvFilePath : str — Full path to CSV file
  sepChar     : str — Delimiter (default ",")
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

# Export first so we have a valid CSV to re-import
csv_path = sap_temp_dir + "\\roundtrip_csvfile.csv"
raw = SapModel.DatabaseTables.GetTableForEditingCSVFile(
    test_key, "All", 0, csv_path, ","
)
assert raw[-1] == 0, f"GetTableForEditingCSVFile failed: {raw[-1]}"
SapModel.DatabaseTables.CancelTableEditing()

# --- Target function: re-import the same CSV ---
raw = SapModel.DatabaseTables.SetTableForEditingCSVFile(
    test_key, 0, csv_path, ","
)
table_version = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"SetTableForEditingCSVFile failed: {ret_code}"

# Clean up
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.SetTableForEditingCSVFile"
result["table_key"] = test_key
result["table_version"] = table_version
result["csv_path"] = csv_path
result["status"] = "verified"
