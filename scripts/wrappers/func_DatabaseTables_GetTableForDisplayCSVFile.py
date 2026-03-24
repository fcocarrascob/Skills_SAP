# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayCSVFile
# Category: Database_Tables
# Description: Export table display data to a CSV file
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Exports table data to a CSV file on disk.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForDisplayCSVFile(TableKey,
      FieldKeyList(), GroupName, TableVersion, csvFilePath, sepChar)

ByRef Output (COM Python):
  raw[0] = TableVersion (int)
  raw[-1] = ret_code    (0=success)

Parameters:
  TableKey     : str   — Table key
  FieldKeyList : str[] — Fields ([""] for all)
  GroupName    : str   — Group filter
  csvFilePath  : str   — Full output file path
  sepChar      : str   — Delimiter (default ",")
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

# Discover non-empty table
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0
all_keys = list(raw_tables[1])
all_empty = list(raw_tables[4])
test_key = None
for i, k in enumerate(all_keys):
    if not all_empty[i]:
        test_key = k
        break
assert test_key is not None, "No non-empty table found"

# --- Target function ---
csv_path = sap_temp_dir + "\\display_test.csv"
raw = SapModel.DatabaseTables.GetTableForDisplayCSVFile(
    test_key, [""], "All", 0, csv_path, ","
)
table_version = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayCSVFile failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayCSVFile"
result["table_key"] = test_key
result["table_version"] = table_version
result["csv_path"] = csv_path
result["status"] = "verified"
