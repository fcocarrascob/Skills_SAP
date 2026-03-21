# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayArray
# Category: Database_Tables
# Description: Extract data from SAP2000 display tables
# Verified: 2026-03-21
# Prerequisites: Model open (some tables need analysis)
# ============================================================
"""
Usage: Extracts data from any SAP2000 database table in array form.
       Tables contain model definition data, analysis results, and
       design results. Data is returned as a 1D array in row-major order.

API Signature:
  SapModel.DatabaseTables.GetTableForDisplayArray(
      TableKey, FieldKeyList, GroupName,
      TableVersion, FieldKeysIncluded,
      NumberRecords, TableData) -> ret_code

ByRef Output (4 values):
  TableVersion      : str   — table version string
  FieldKeysIncluded : str[] — field (column) names included
  NumberRecords     : int   — number of data rows
  TableData         : str[] — 1D array of all cell values
                              (row-major: row0col0, row0col1, ..., row1col0, ...)

Parameters:
  TableKey     : str  — Table identifier (e.g., "Frame Assignments - Summary",
                        "Joint Coordinates", "Material Properties - Summary")
  FieldKeyList : str  — Comma-separated field names to include (""=all fields)
  GroupName    : str  — Group filter (""=All)
"""

# --- Minimal setup: model with some objects ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Create a frame
beam = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "SEC_TEST", "")
assert beam[-1] == 0

# --- Target function: get joint coordinates table ---
# Return layout: [FieldKeyList_byref, TableVersion, FieldKeysIncluded, NumberRecords, TableData, ret_code]
# NOTE: TableVersion must be 0 (int), not "" (str)
# NOTE: FieldKeyList must be [] (array), not "" (str)
raw = SapModel.DatabaseTables.GetTableForDisplayArray(
    "Joint Coordinates",  # TableKey
    [],                   # FieldKeyList (array — all fields)
    "",                   # GroupName (all)
    0,                    # TableVersion (ByRef Integer)
    [],                   # FieldKeysIncluded (ByRef)
    0,                    # NumberRecords (ByRef)
    []                    # TableData (ByRef)
)
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayArray failed: {ret_code}"

table_version = raw[1]
field_keys    = list(raw[2])
num_records   = raw[3]
table_data    = list(raw[4])

assert num_records > 0, f"No records in Joint Coordinates table"
assert len(field_keys) > 0, f"No field keys returned"

# Parse: data is 1D array, num_columns = len(field_keys)
num_cols = len(field_keys)
rows = []
for i in range(num_records):
    row = table_data[i * num_cols : (i + 1) * num_cols]
    rows.append(dict(zip(field_keys, row)))

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayArray"
result["table_key"] = "Joint Coordinates"
result["field_keys"] = field_keys
result["num_records"] = num_records
result["sample_rows"] = rows[:3]
result["status"] = "verified"
