# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayXMLString
# Category: Database_Tables
# Description: Export table display data as an XML string
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Returns table data as an XML-formatted string, optionally with schema.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForDisplayXMLString(TableKey,
      FieldKeyList(), GroupName, IncludeSchema, TableVersion, XMLTableData)

ByRef Output (COM Python):
  raw[0] = FieldKeysIncluded[] (tuple of str)
  raw[1] = NumberRecords       (int)
  raw[2] = XMLTableData        (str)
  raw[-1] = ret_code           (0=success)

Parameters:
  TableKey      : str   — Table key
  FieldKeyList  : str[] — Fields ([""] for all)
  GroupName     : str   — Group filter
  IncludeSchema : bool  — Whether to include XML schema
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
assert test_key is not None

# --- Target function ---
raw = SapModel.DatabaseTables.GetTableForDisplayXMLString(
    test_key, [""], "All", True, 0, ""
)
field_keys = list(raw[0])
num_records = raw[1]
xml_string = raw[2]
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayXMLString failed: {ret_code}"

# --- Verification ---
assert xml_string and len(xml_string) > 0, "XML string is empty"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayXMLString"
result["table_key"] = test_key
result["field_keys"] = field_keys
result["num_records"] = num_records
result["xml_length"] = len(xml_string)
result["xml_preview"] = xml_string[:500]
result["status"] = "verified"
