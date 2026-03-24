# ============================================================
# Wrapper: SapModel.DatabaseTables.ShowTablesInExcel
# Category: Database_Tables
# Description: Export specified tables to Excel
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data, Excel installed
# ============================================================
"""
Usage: Exports one or more tables directly to Excel. Excel must be
       installed on the machine. A window handle can optionally be
       provided to position the Excel window.

API Signature (VBA):
  SapModel.DatabaseTables.ShowTablesInExcel(TableKeyList(), WindowHandle)

ByRef Output (COM Python):
  ret_code (0=success) — returned directly

Parameters:
  TableKeyList : str[] — Array of table keys to export
  WindowHandle : int   — Window handle (0 for no parent)
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

# Discover a non-empty table
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0
all_keys = list(raw_tables[1])
all_empty = list(raw_tables[4])
test_keys = []
for i, k in enumerate(all_keys):
    if not all_empty[i]:
        test_keys.append(k)
    if len(test_keys) >= 2:
        break
assert len(test_keys) > 0, "No non-empty tables found"

# --- Target function ---
ret = SapModel.DatabaseTables.ShowTablesInExcel(test_keys, 0)
ret_code = ret[-1] if isinstance(ret, (tuple, list)) else ret
assert ret_code == 0, f"ShowTablesInExcel failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.ShowTablesInExcel"
result["tables_exported"] = test_keys
result["status"] = "verified"
