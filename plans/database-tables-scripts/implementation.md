# Database Tables — Complete Implementation Plan

## Goal
Create 18 verified wrapper scripts covering all 37 DatabaseTables API functions, register them in registry.json, build a reusable backend class, and deliver a PySide6 GUI with conditional editing based on model lock state.

## Prerequisites
Make sure you are on the `feature/database-tables-wrappers` branch before beginning implementation.
If not, create the branch from main:

```powershell
git checkout main
git pull
git checkout -b feature/database-tables-wrappers
```

Also ensure the directory exists:
```powershell
New-Item -ItemType Directory -Path "scripts/database_tables" -Force
```

---

### Step-by-Step Instructions

---

#### Step 1: Metadata Wrappers (GetAllTables, GetAvailableTables, GetAllFieldsInTable, GetObsoleteTableKeyList)

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetAllTables.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetAllTables
# Category: Database_Tables
# Description: Returns all tables with import type and empty status
# Verified: pending
# Prerequisites: Connected to SAP2000, model with at least one frame
# ============================================================
"""
Usage: Enumerates every table available in the current model, including
       whether each table is importable and whether it contains data.

API Signature (VBA):
  SapModel.DatabaseTables.GetAllTables(NumberTables, TableKey(), TableName(), ImportType(), IsEmpty())

ByRef Output (COM Python):
  raw[0] = NumberTables (int)
  raw[1] = TableKey[]   (tuple of str)
  raw[2] = TableName[]  (tuple of str)
  raw[3] = ImportType[] (tuple of int: 0=not importable, 1=importable non-interactive,
                         2=interactive unlocked, 3=interactive any)
  raw[4] = IsEmpty[]    (tuple of bool)
  raw[-1] = ret_code    (0=success)

Parameters:
  (none — all outputs are ByRef)
"""

# --- Minimal setup: model with at least one element ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Add a material + section + frame so tables have data
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# --- Target function ---
raw = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
num_tables = raw[0]
table_keys = list(raw[1])
table_names = list(raw[2])
import_types = list(raw[3])
is_empty = list(raw[4])
ret_code = raw[-1]
assert ret_code == 0, f"GetAllTables failed: {ret_code}"

# --- Verification ---
assert num_tables > 0, f"Expected tables > 0, got {num_tables}"
assert len(table_keys) == num_tables, "TableKey count mismatch"
assert len(table_names) == num_tables, "TableName count mismatch"
assert len(import_types) == num_tables, "ImportType count mismatch"
assert len(is_empty) == num_tables, "IsEmpty count mismatch"

# Check known tables exist
known_tables = [k for k in table_keys if "Material" in k or "Frame" in k]
assert len(known_tables) > 0, "Expected material/frame tables in model with elements"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetAllTables"
result["num_tables"] = num_tables
result["sample_keys"] = table_keys[:10]
result["sample_names"] = table_names[:10]
result["sample_import_types"] = import_types[:10]
result["non_empty_count"] = sum(1 for e in is_empty if not e)
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetAvailableTables.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetAvailableTables
# Category: Database_Tables
# Description: Returns available tables with their import type
# Verified: pending
# Prerequisites: Connected to SAP2000, model with at least one frame
# ============================================================
"""
Usage: Returns tables available for display (similar to GetAllTables but
       without the IsEmpty array — lighter query).

API Signature (VBA):
  SapModel.DatabaseTables.GetAvailableTables(NumberTables, TableKey(), TableName(), ImportType())

ByRef Output (COM Python):
  raw[0] = NumberTables (int)
  raw[1] = TableKey[]   (tuple of str)
  raw[2] = TableName[]  (tuple of str)
  raw[3] = ImportType[] (tuple of int)
  raw[-1] = ret_code    (0=success)

Parameters:
  (none — all outputs are ByRef)
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

# --- Target function ---
raw = SapModel.DatabaseTables.GetAvailableTables(0, [], [], [])
num_tables = raw[0]
table_keys = list(raw[1])
table_names = list(raw[2])
import_types = list(raw[3])
ret_code = raw[-1]
assert ret_code == 0, f"GetAvailableTables failed: {ret_code}"

# --- Verification ---
assert num_tables > 0, f"Expected tables > 0, got {num_tables}"
assert len(table_keys) == num_tables, "TableKey count mismatch"
assert len(table_names) == num_tables, "TableName count mismatch"
assert len(import_types) == num_tables, "ImportType count mismatch"

# All import types should be 0, 1, 2, or 3
for it in import_types:
    assert it in (0, 1, 2, 3), f"Invalid ImportType: {it}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetAvailableTables"
result["num_tables"] = num_tables
result["sample_keys"] = table_keys[:10]
result["sample_names"] = table_names[:10]
result["importable_count"] = sum(1 for it in import_types if it > 0)
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetAllFieldsInTable.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetAllFieldsInTable
# Category: Database_Tables
# Description: Returns all fields (columns) for a specific table
# Verified: pending
# Prerequisites: Connected to SAP2000, model with at least one frame
# ============================================================
"""
Usage: Retrieves metadata about every field (column) in a specific table.
       Returns field keys, names, descriptions, units, and importability.

API Signature (VBA):
  SapModel.DatabaseTables.GetAllFieldsInTable(TableKey, TableVersion,
      NumberFields, FieldKey(), FieldName(), Description(), UnitsString(),
      IsImportable())

ByRef Output (COM Python):
  raw[0] = TableVersion  (int)
  raw[1] = NumberFields   (int)
  raw[2] = FieldKey[]     (tuple of str)
  raw[3] = FieldName[]    (tuple of str)
  raw[4] = Description[]  (tuple of str)
  raw[5] = UnitsString[]  (tuple of str)
  raw[6] = IsImportable[] (tuple of bool)
  raw[-1] = ret_code      (0=success)

Parameters:
  TableKey : str — The table key to query (e.g. "Material Properties 01 - General")
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

# --- Discover a valid table key ---
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0, f"GetAllTables failed: {raw_tables[-1]}"
all_keys = list(raw_tables[1])
# Pick a table that should exist in any model with materials
test_key = None
for k in all_keys:
    if "Material Properties" in k:
        test_key = k
        break
assert test_key is not None, "Could not find a Material Properties table"

# --- Target function ---
raw = SapModel.DatabaseTables.GetAllFieldsInTable(
    test_key, 0, 0, [], [], [], [], []
)
table_version = raw[0]
num_fields = raw[1]
field_keys = list(raw[2])
field_names = list(raw[3])
descriptions = list(raw[4])
units_strings = list(raw[5])
is_importable = list(raw[6])
ret_code = raw[-1]
assert ret_code == 0, f"GetAllFieldsInTable failed: {ret_code}"

# --- Verification ---
assert num_fields > 0, f"Expected fields > 0, got {num_fields}"
assert len(field_keys) == num_fields, "FieldKey count mismatch"
assert len(field_names) == num_fields, "FieldName count mismatch"
assert len(descriptions) == num_fields, "Description count mismatch"
assert len(units_strings) == num_fields, "UnitsString count mismatch"
assert len(is_importable) == num_fields, "IsImportable count mismatch"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetAllFieldsInTable"
result["table_key"] = test_key
result["table_version"] = table_version
result["num_fields"] = num_fields
result["field_keys"] = field_keys
result["field_names"] = field_names
result["sample_units"] = units_strings[:5]
result["importable_count"] = sum(1 for v in is_importable if v)
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetObsoleteTableKeyList.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetObsoleteTableKeyList
# Category: Database_Tables
# Description: Returns list of obsolete table keys and associated notes
# Verified: pending
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
```

- [x] Execute each wrapper via `run_sap_script` (MCP tool) and verify `ret_code == 0`
- [x] Once verified, register the 4 functions in `scripts/registry.json` by running `register_verified_function` for each:
  - `SapModel.DatabaseTables.GetAllTables` → category: `Database_Tables`, wrapper: `func_DatabaseTables_GetAllTables`
  - `SapModel.DatabaseTables.GetAvailableTables` → category: `Database_Tables`, wrapper: `func_DatabaseTables_GetAvailableTables`
  - `SapModel.DatabaseTables.GetAllFieldsInTable` → category: `Database_Tables`, wrapper: `func_DatabaseTables_GetAllFieldsInTable`
  - `SapModel.DatabaseTables.GetObsoleteTableKeyList` → category: `Database_Tables`, wrapper: `func_DatabaseTables_GetObsoleteTableKeyList`

##### Step 1 Verification Checklist
- [x] All 4 wrappers execute without errors (ret_code == 0)
- [x] `GetAllTables` returns num_tables > 0 and array lengths match
- [x] `GetAvailableTables` returns valid ImportType values (0–3)
- [x] `GetAllFieldsInTable` returns field metadata for a known table
- [x] `GetObsoleteTableKeyList` returns without error (count may be 0)
- [x] All 4 functions appear in `registry.json` under category `Database_Tables`

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add metadata wrappers (GetAllTables, GetAvailableTables, GetAllFieldsInTable, GetObsoleteTableKeyList)`

---

#### Step 2: Core Array R/W Wrappers (GetTableForEditingArray, SetTableForEditingArray, GetTableForDisplayArray, ApplyEditedTables, CancelTableEditing)

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForEditingArray.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForEditingArray
# Category: Database_Tables
# Description: Read a table as flat array for interactive editing
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Retrieves table data in a flat string array, suitable for
       editing and re-importing via SetTableForEditingArray.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForEditingArray(TableKey, GroupName,
      TableVersion, FieldKeysIncluded(), NumberRecords, TableData())

ByRef Output (COM Python):
  raw[0] = TableVersion       (int)
  raw[1] = FieldKeysIncluded[] (tuple of str — column headers)
  raw[2] = NumberRecords       (int — row count)
  raw[3] = TableData[]         (tuple of str — flat row-by-row data)
  raw[-1] = ret_code           (0=success)

Parameters:
  TableKey  : str — Table key to read
  GroupName : str — Group filter ("All" or "" for all objects)
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

# --- Discover an editable table ---
raw_tables = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
assert raw_tables[-1] == 0, f"GetAllTables failed"
all_keys = list(raw_tables[1])
all_import = list(raw_tables[3])
all_empty = list(raw_tables[4])

# Find a non-empty, editable table
test_key = None
for i, k in enumerate(all_keys):
    if all_import[i] >= 2 and not all_empty[i]:
        test_key = k
        break
if test_key is None:
    for i, k in enumerate(all_keys):
        if not all_empty[i]:
            test_key = k
            break
assert test_key is not None, "No non-empty table found"

# --- Target function ---
raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
table_version = raw[0]
field_keys = list(raw[1])
num_records = raw[2]
table_data = list(raw[3]) if raw[3] else []
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForEditingArray failed: {ret_code}"

# --- Verification ---
assert len(field_keys) > 0, "Expected at least one field"
assert num_records >= 0, f"Unexpected negative records: {num_records}"
if num_records > 0:
    expected_len = len(field_keys) * num_records
    assert len(table_data) == expected_len, (
        f"TableData length {len(table_data)} != fields({len(field_keys)}) * records({num_records})"
    )

# Cancel editing to clean state
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForEditingArray"
result["table_key"] = test_key
result["table_version"] = table_version
result["field_keys"] = field_keys
result["num_records"] = num_records
result["sample_data"] = table_data[:20]
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_SetTableForEditingArray.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.SetTableForEditingArray
# Category: Database_Tables
# Description: Write edited table data back for import
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Stores modified table data for later import via ApplyEditedTables.
       The data format matches GetTableForEditingArray output (flat array).

API Signature (VBA):
  SapModel.DatabaseTables.SetTableForEditingArray(TableKey, TableVersion,
      FieldKeysIncluded(), NumberRecords, TableData())

ByRef Output (COM Python):
  raw[-1] = ret_code (0=success)

Parameters:
  TableKey           : str     — Table key to write
  TableVersion       : int     — Version from GetTableForEditingArray
  FieldKeysIncluded  : str[]   — Column headers (field keys)
  NumberRecords      : int     — Number of data rows
  TableData          : str[]   — Flat row-by-row data
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

# --- Read an editable table first ---
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
assert test_key is not None, "No editable non-empty table found"

raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
table_version = raw[0]
field_keys = list(raw[1])
num_records = raw[2]
table_data = list(raw[3]) if raw[3] else []
assert raw[-1] == 0, f"GetTableForEditingArray failed: {raw[-1]}"
assert num_records > 0, "Need at least one record to test SetTableForEditingArray"

# Cancel the get — clean state before set
SapModel.DatabaseTables.CancelTableEditing()

# --- Target function: write the same data back (round-trip) ---
raw = SapModel.DatabaseTables.SetTableForEditingArray(
    test_key, table_version, field_keys, num_records, table_data
)
ret_code = raw[-1] if isinstance(raw, tuple) else raw
assert ret_code == 0, f"SetTableForEditingArray failed: {ret_code}"

# Cancel to clean up (don't apply changes for this test)
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.SetTableForEditingArray"
result["table_key"] = test_key
result["table_version"] = table_version
result["field_keys"] = field_keys
result["num_records"] = num_records
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_ApplyEditedTables.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.ApplyEditedTables
# Category: Database_Tables
# Description: Apply all pending table edits to the model
# Verified: pending
# Prerequisites: Connected to SAP2000, pending table edits via SetTableForEditing*
# ============================================================
"""
Usage: Imports all tables stored via SetTableForEditing* functions.
       Returns error/warning/info message counts and optional log.

API Signature (VBA):
  SapModel.DatabaseTables.ApplyEditedTables(FillImportLog,
      NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

ByRef Output (COM Python):
  raw[0] = NumFatalErrors (int)
  raw[1] = NumErrorMsgs   (int)
  raw[2] = NumWarnMsgs    (int)
  raw[3] = NumInfoMsgs    (int)
  raw[4] = ImportLog      (str)
  raw[-1] = ret_code      (0=success)

Parameters:
  FillImportLog : bool — True to populate the ImportLog string
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

# --- Read→Set round trip to stage a pending edit ---
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
assert test_key is not None, "No editable non-empty table found"

raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
table_version = raw[0]
field_keys = list(raw[1])
num_records = raw[2]
table_data = list(raw[3]) if raw[3] else []
assert raw[-1] == 0
SapModel.DatabaseTables.CancelTableEditing()

# Stage the same data back
raw = SapModel.DatabaseTables.SetTableForEditingArray(
    test_key, table_version, field_keys, num_records, table_data
)
set_ret = raw[-1] if isinstance(raw, tuple) else raw
assert set_ret == 0, f"SetTableForEditingArray failed: {set_ret}"

# --- Target function ---
raw = SapModel.DatabaseTables.ApplyEditedTables(True, 0, 0, 0, 0, "")
num_fatal = raw[0]
num_errors = raw[1]
num_warnings = raw[2]
num_info = raw[3]
import_log = raw[4]
ret_code = raw[-1]
assert ret_code == 0, f"ApplyEditedTables failed: {ret_code}"

# --- Verification ---
assert num_fatal == 0, f"Fatal errors during import: {num_fatal}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.ApplyEditedTables"
result["num_fatal_errors"] = num_fatal
result["num_error_msgs"] = num_errors
result["num_warn_msgs"] = num_warnings
result["num_info_msgs"] = num_info
result["import_log_length"] = len(import_log) if import_log else 0
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_CancelTableEditing.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.CancelTableEditing
# Category: Database_Tables
# Description: Cancel all pending table edits
# Verified: pending
# Prerequisites: Connected to SAP2000
# ============================================================
"""
Usage: Clears all tables stored via SetTableForEditing* functions
       without applying them. Acts as a rollback.

API Signature (VBA):
  SapModel.DatabaseTables.CancelTableEditing()

ByRef Output (COM Python):
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  (none)
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

# --- Stage a pending edit to cancel ---
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
assert test_key is not None, "No editable non-empty table found"

# Read then stage
raw = SapModel.DatabaseTables.GetTableForEditingArray(test_key, "All", 0, [], 0, [])
assert raw[-1] == 0
SapModel.DatabaseTables.CancelTableEditing()

raw = SapModel.DatabaseTables.SetTableForEditingArray(
    test_key, raw[0], list(raw[1]), raw[2], list(raw[3]) if raw[3] else []
)
set_ret = raw[-1] if isinstance(raw, tuple) else raw
assert set_ret == 0, f"SetTableForEditingArray failed: {set_ret}"

# --- Target function ---
ret = SapModel.DatabaseTables.CancelTableEditing()
assert ret == 0, f"CancelTableEditing failed: {ret}"

# --- Verification ---
# After cancel, ApplyEditedTables should have nothing to apply
raw_apply = SapModel.DatabaseTables.ApplyEditedTables(False, 0, 0, 0, 0, "")
# Should succeed with 0 records imported
assert raw_apply[-1] == 0, f"ApplyEditedTables after cancel failed: {raw_apply[-1]}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.CancelTableEditing"
result["cancel_ret_code"] = ret
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForDisplayArray.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayArray
# Category: Database_Tables
# Description: Read table data for display (read-only) as flat array
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Retrieves table data for display purposes. Unlike GetTableForEditingArray,
       allows specifying which fields to include and works for read-only tables.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList(),
      GroupName, TableVersion, FieldKeysIncluded(), NumberRecords, TableData())

ByRef Output (COM Python):
  raw[0] = TableVersion        (int)
  raw[1] = FieldKeysIncluded[] (tuple of str)
  raw[2] = NumberRecords       (int)
  raw[3] = TableData[]         (tuple of str — flat row-by-row data)
  raw[-1] = ret_code           (0=success)

Parameters:
  TableKey     : str   — Table key to read
  FieldKeyList : str[] — Fields to include ([""] for all)
  GroupName    : str   — Group filter ("All" or "" for all)
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

# --- Discover a non-empty table ---
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

# --- Target function: get ALL fields ---
raw = SapModel.DatabaseTables.GetTableForDisplayArray(
    test_key, [""], "All", 0, [], 0, []
)
table_version = raw[0]
field_keys = list(raw[1])
num_records = raw[2]
table_data = list(raw[3]) if raw[3] else []
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayArray failed: {ret_code}"

# --- Verification ---
assert len(field_keys) > 0, "Expected at least one field"
if num_records > 0:
    expected_len = len(field_keys) * num_records
    assert len(table_data) == expected_len, (
        f"TableData length {len(table_data)} != fields({len(field_keys)}) * records({num_records})"
    )

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayArray"
result["table_key"] = test_key
result["table_version"] = table_version
result["field_keys"] = field_keys
result["num_records"] = num_records
result["sample_data"] = table_data[:20]
result["status"] = "verified"
```

- [x] Execute each wrapper via `run_sap_script` and verify
- [x] Register 5 functions in `registry.json` via `register_verified_function`:
  - `SapModel.DatabaseTables.GetTableForEditingArray`
  - `SapModel.DatabaseTables.SetTableForEditingArray`
  - `SapModel.DatabaseTables.GetTableForDisplayArray`
  - `SapModel.DatabaseTables.ApplyEditedTables`
  - `SapModel.DatabaseTables.CancelTableEditing`

##### Step 2 Verification Checklist
- [x] `GetTableForEditingArray` returns data with field_keys and table_data
- [x] `SetTableForEditingArray` accepts round-trip data without error
- [x] `ApplyEditedTables` completes with 0 fatal errors
- [x] `CancelTableEditing` clears pending edits
- [x] `GetTableForDisplayArray` reads display data successfully
- [x] All 5 functions registered in `registry.json`

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add core array R/W wrappers (Get/Set/Apply/Cancel/Display)`

---

#### Step 3: CSV/XML I/O Wrappers (7 functions)

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForDisplayCSVFile.py`:

```python
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
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForDisplayCSVString.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayCSVString
# Category: Database_Tables
# Description: Export table display data as a CSV string
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Returns table data as a CSV-formatted string.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForDisplayCSVString(TableKey,
      FieldKeyList(), GroupName, TableVersion, csvString, sepChar)

ByRef Output (COM Python):
  raw[0] = TableVersion (int)
  raw[1] = csvString    (str)
  raw[-1] = ret_code    (0=success)

Parameters:
  TableKey     : str   — Table key
  FieldKeyList : str[] — Fields ([""] for all)
  GroupName    : str   — Group filter
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
assert test_key is not None

# --- Target function ---
raw = SapModel.DatabaseTables.GetTableForDisplayCSVString(
    test_key, [""], "All", 0, "", ","
)
table_version = raw[0]
csv_string = raw[1]
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayCSVString failed: {ret_code}"

# --- Verification ---
assert csv_string and len(csv_string) > 0, "CSV string is empty"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayCSVString"
result["table_key"] = test_key
result["table_version"] = table_version
result["csv_length"] = len(csv_string)
result["csv_preview"] = csv_string[:500]
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForDisplayXMLString.py`:

```python
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
  raw[0] = TableVersion  (int)
  raw[1] = XMLTableData  (str)
  raw[-1] = ret_code     (0=success)

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
table_version = raw[0]
xml_string = raw[1]
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayXMLString failed: {ret_code}"

# --- Verification ---
assert xml_string and len(xml_string) > 0, "XML string is empty"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForDisplayXMLString"
result["table_key"] = test_key
result["table_version"] = table_version
result["xml_length"] = len(xml_string)
result["xml_preview"] = xml_string[:500]
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForEditingCSVFile.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForEditingCSVFile
# Category: Database_Tables
# Description: Export editable table data to a CSV file
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Exports editable table data to a CSV file on disk.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForEditingCSVFile(TableKey, GroupName,
      TableVersion, csvFilePath, sepChar)

ByRef Output (COM Python):
  raw[0] = TableVersion (int)
  raw[-1] = ret_code    (0=success)

Parameters:
  TableKey    : str — Table key
  GroupName   : str — Group filter
  csvFilePath : str — Full output file path
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
assert test_key is not None, "No editable non-empty table found"

# --- Target function ---
csv_path = sap_temp_dir + "\\editing_test.csv"
raw = SapModel.DatabaseTables.GetTableForEditingCSVFile(
    test_key, "All", 0, csv_path, ","
)
table_version = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForEditingCSVFile failed: {ret_code}"

# Clean up pending state
SapModel.DatabaseTables.CancelTableEditing()

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForEditingCSVFile"
result["table_key"] = test_key
result["table_version"] = table_version
result["csv_path"] = csv_path
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_GetTableForEditingCSVString.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForEditingCSVString
# Category: Database_Tables
# Description: Export editable table data as a CSV string
# Verified: pending
# Prerequisites: Connected to SAP2000, model with data
# ============================================================
"""
Usage: Returns editable table data as a CSV-formatted string.

API Signature (VBA):
  SapModel.DatabaseTables.GetTableForEditingCSVString(TableKey, GroupName,
      TableVersion, csvString, sepChar)

ByRef Output (COM Python):
  raw[0] = TableVersion (int)
  raw[1] = csvString    (str)
  raw[-1] = ret_code    (0=success)

Parameters:
  TableKey  : str — Table key
  GroupName : str — Group filter
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

# --- Target function ---
raw = SapModel.DatabaseTables.GetTableForEditingCSVString(
    test_key, "All", 0, "", ","
)
table_version = raw[0]
csv_string = raw[1]
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForEditingCSVString failed: {ret_code}"

# Clean up
SapModel.DatabaseTables.CancelTableEditing()

# --- Verification ---
assert csv_string and len(csv_string) > 0, "CSV string is empty"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.GetTableForEditingCSVString"
result["table_key"] = test_key
result["table_version"] = table_version
result["csv_length"] = len(csv_string)
result["csv_preview"] = csv_string[:500]
result["status"] = "verified"
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_SetTableForEditingCSVFile.py`:

```python
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
```

- [x] Create file `scripts/wrappers/func_DatabaseTables_SetTableForEditingCSVString.py`:

```python
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
```

- [x] Execute all 7 wrappers via `run_sap_script` and verify
- [x] Register all 7 functions in `registry.json`

##### Step 3 Verification Checklist
- [x] CSV file export produces a non-zero-length file at the specified path
- [x] CSV string exports return non-empty strings with comma-delimited content
- [x] XML string export returns valid XML content
- [x] CSV file round-trip (export → import) completes without error
- [x] CSV string round-trip (export → import) completes without error
- [x] All 7 functions registered in `registry.json`

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add CSV/XML I/O wrappers (7 functions)`

---

#### Step 4: Display Selection Consolidated Wrapper (20 functions)

- [ ] Create file `scripts/wrappers/func_DatabaseTables_DisplaySelection_Consolidated.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables — Display Selection (Consolidated)
# Category: Database_Tables
# Description: Tests all 10 Get/Set pairs for display selection config
# Verified: pending
# Prerequisites: Connected to SAP2000, model with load patterns and cases
# ============================================================
"""
Usage: Consolidated wrapper that exercises all 20 display selection
       functions (10 Get/Set pairs). Each pair controls which items
       are included when displaying analysis results.

Functions tested:
  1. Get/SetLoadCasesSelectedForDisplay
  2. Get/SetLoadCombinationsSelectedForDisplay
  3. Get/SetLoadPatternsSelectedForDisplay
  4. Get/SetElementVirtualWorkNamedSetsSelectedForDisplay
  5. Get/SetGeneralizedDisplacementsSelectedForDisplay
  6. Get/SetJointResponseSpectraNamedSetsSelectedForDisplay
  7. Get/SetPlotFunctionTracesNamedSetsSelectedForDisplay
  8. Get/SetPushoverNamedSetsSelectedForDisplay
  9. Get/SetSectionCutsSelectedForDisplay
 10. Get/SetTableOutputOptionsForDisplay

For pairs 1-9, the pattern is:
  Get: (NumberSelected, NameList[]) → ret_code
  Set: (NameList[]) → ret_code

Pair 10 (TableOutputOptions) has 18 ByRef parameters — special handling.
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
assert ret == 0, f"SetPresentUnits failed: {ret}"

# Create minimal model with a load pattern and frame
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 2)
assert ret == 0, f"SetMaterial failed: {ret}"
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "SEC_TEST", "")
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Add extra load patterns for testing display selection
ret = SapModel.LoadPatterns.Add("LIVE_TEST", 3)
assert ret == 0, f"LoadPatterns.Add failed: {ret}"

tested_functions = []

# ═══════════════════════════════════════════════════════════════
# Pair 1: LoadCasesSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadCasesSelectedForDisplay failed: {ret_code}"
num_selected_lc = raw[0]
lc_list = list(raw[1]) if raw[1] else []
tested_functions.append("GetLoadCasesSelectedForDisplay")

# Set: select all available load cases
ret = SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(lc_list if lc_list else [""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetLoadCasesSelectedForDisplay failed: {ret_val}"
tested_functions.append("SetLoadCasesSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 2: LoadCombinationsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetLoadCombinationsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadCombinationsSelectedForDisplay failed: {ret_code}"
tested_functions.append("GetLoadCombinationsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetLoadCombinationsSelectedForDisplay failed: {ret_val}"
tested_functions.append("SetLoadCombinationsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 3: LoadPatternsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetLoadPatternsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetLoadPatternsSelectedForDisplay failed: {ret_code}"
num_patterns = raw[0]
pattern_list = list(raw[1]) if raw[1] else []
tested_functions.append("GetLoadPatternsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay(
    pattern_list if pattern_list else [""]
)
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetLoadPatternsSelectedForDisplay failed: {ret_val}"
tested_functions.append("SetLoadPatternsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 4: ElementVirtualWorkNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetElementVirtualWorkNamedSets failed: {ret_code}"
tested_functions.append("GetElementVirtualWorkNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetElementVirtualWorkNamedSets failed: {ret_val}"
tested_functions.append("SetElementVirtualWorkNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 5: GeneralizedDisplacementsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetGeneralizedDisplacements failed: {ret_code}"
tested_functions.append("GetGeneralizedDisplacementsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetGeneralizedDisplacements failed: {ret_val}"
tested_functions.append("SetGeneralizedDisplacementsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 6: JointResponseSpectraNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetJointResponseSpectraNamed failed: {ret_code}"
tested_functions.append("GetJointResponseSpectraNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetJointResponseSpectraNamed failed: {ret_val}"
tested_functions.append("SetJointResponseSpectraNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 7: PlotFunctionTracesNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetPlotFunctionTracesNamed failed: {ret_code}"
tested_functions.append("GetPlotFunctionTracesNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetPlotFunctionTracesNamed failed: {ret_val}"
tested_functions.append("SetPlotFunctionTracesNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 8: PushoverNamedSetsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetPushoverNamedSets failed: {ret_code}"
tested_functions.append("GetPushoverNamedSetsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetPushoverNamedSets failed: {ret_val}"
tested_functions.append("SetPushoverNamedSetsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 9: SectionCutsSelectedForDisplay
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetSectionCuts failed: {ret_code}"
tested_functions.append("GetSectionCutsSelectedForDisplay")

ret = SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay([""])
ret_val = ret[-1] if isinstance(ret, tuple) else ret
assert ret_val == 0, f"SetSectionCuts failed: {ret_val}"
tested_functions.append("SetSectionCutsSelectedForDisplay")

# ═══════════════════════════════════════════════════════════════
# Pair 10: TableOutputOptionsForDisplay (18 ByRef params)
# ═══════════════════════════════════════════════════════════════
raw = SapModel.DatabaseTables.GetTableOutputOptionsForDisplay(
    0.0, 0.0, 0.0,      # BaseReactionGX/GY/GZ
    True, 1, 12,         # IsAllModes, StartMode, EndMode
    True, 1, 6,          # IsAllBucklingModes, Start, End
    1, 1, 1, 1,          # ModalHistory, DirectHistory, NonlinearStatic, MultistepStatic
    1, 1, 1, 1, 1        # SteadyState, SteadyStateOption, PSD, Combo, BridgeDesign
)
ret_code = raw[-1]
assert ret_code == 0, f"GetTableOutputOptionsForDisplay failed: {ret_code}"
tested_functions.append("GetTableOutputOptionsForDisplay")

# Set with known good values
ret = SapModel.DatabaseTables.SetTableOutputOptionsForDisplay(
    0.0, 0.0, 0.0,      # BaseReactionGX/GY/GZ
    True, 1, 12,         # IsAllModes, StartMode, EndMode
    True, 1, 6,          # IsAllBucklingModes, Start, End
    1, 1, 2, 2,          # ModalHistory, DirectHistory, NonlinearStatic, MultistepStatic
    1, 1, 2, 2, 1        # SteadyState, SteadyStateOption, PSD, Combo, BridgeDesign
)
ret_val = ret if isinstance(ret, int) else ret[-1]
assert ret_val == 0, f"SetTableOutputOptionsForDisplay failed: {ret_val}"
tested_functions.append("SetTableOutputOptionsForDisplay")

# --- Summary ---
assert len(tested_functions) == 20, f"Expected 20 functions, got {len(tested_functions)}"

result["function"] = "SapModel.DatabaseTables — Display Selection (Consolidated)"
result["functions_tested"] = tested_functions
result["total_tested"] = len(tested_functions)
result["status"] = "verified"
```

- [ ] Execute the consolidated wrapper via `run_sap_script`
- [ ] Register all 20 individual functions in `registry.json` (all pointing to the same wrapper `func_DatabaseTables_DisplaySelection_Consolidated`):

The 20 function paths to register:
```
SapModel.DatabaseTables.GetLoadCasesSelectedForDisplay
SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay
SapModel.DatabaseTables.GetLoadCombinationsSelectedForDisplay
SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay
SapModel.DatabaseTables.GetLoadPatternsSelectedForDisplay
SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay
SapModel.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay
SapModel.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay
SapModel.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay
SapModel.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay
SapModel.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay
SapModel.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay
SapModel.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay
SapModel.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay
SapModel.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay
SapModel.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay
SapModel.DatabaseTables.GetSectionCutsSelectedForDisplay
SapModel.DatabaseTables.SetSectionCutsSelectedForDisplay
SapModel.DatabaseTables.GetTableOutputOptionsForDisplay
SapModel.DatabaseTables.SetTableOutputOptionsForDisplay
```

##### Step 4 Verification Checklist
- [ ] All 20 functions execute without error in the consolidated wrapper
- [ ] Get/Set pairs for LoadCases, LoadCombinations, LoadPatterns work
- [ ] All named set pairs (VirtualWork, Generalized, JointResponse, PlotFunction, Pushover, SectionCuts) return `ret_code == 0`
- [ ] TableOutputOptions Get/Set works with 18 parameters
- [ ] All 20 functions appear in `registry.json`

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add Display Selection consolidated wrapper (20 functions)`

---

#### Step 5: ShowTablesInExcel Wrapper + Registry Validation

- [ ] Create file `scripts/wrappers/func_DatabaseTables_ShowTablesInExcel.py`:

```python
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
ret_code = ret[-1] if isinstance(ret, tuple) else ret
assert ret_code == 0, f"ShowTablesInExcel failed: {ret_code}"

# --- Result ---
result["function"] = "SapModel.DatabaseTables.ShowTablesInExcel"
result["tables_exported"] = test_keys
result["status"] = "verified"
```

- [ ] Execute via `run_sap_script` (note: Excel will open — this is visual verification)
- [ ] Register `SapModel.DatabaseTables.ShowTablesInExcel` in `registry.json`
- [ ] Validate total registry count: run `query_function_registry(category="Database_Tables")` and confirm **37 functions** are returned

##### Step 5 Verification Checklist
- [ ] `ShowTablesInExcel` opens Excel with requested tables
- [ ] `query_function_registry(category="Database_Tables")` returns 37 entries
- [ ] All wrapper filenames match the expected naming convention

#### Step 5 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add ShowTablesInExcel wrapper + complete registry (37 functions)`

---

#### Step 6: Backend Class (DatabaseTablesBackend)

- [ ] Create file `scripts/database_tables/backend_database_tables.py`:

```python
"""
Backend — SAP2000 Database Tables Explorer (Standalone)
========================================================
Provides high-level methods to list, read, write, and export SAP2000
database tables via direct COM connection (no MCP dependency).

Connection: COM directo vía comtypes.client
"""

import math
import tempfile
import comtypes.client
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple


# ══════════════════════════════════════════════════════════════════════════════
# SAP2000 Connection (COM directo)
# ══════════════════════════════════════════════════════════════════════════════

class SapConnection:
    """Conexión directa a SAP2000 vía COM — sin MCP."""

    def __init__(self):
        self.sap_object = None
        self.sap_model = None

    @property
    def is_connected(self) -> bool:
        return self.sap_model is not None

    def connect(self, attach_to_existing: bool = True) -> dict:
        try:
            if attach_to_existing:
                self.sap_object = comtypes.client.GetActiveObject(
                    "CSI.SAP2000.API.SapObject"
                )
            else:
                helper = comtypes.client.CreateObject("SAP2000v1.Helper")
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
                self.sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
                self.sap_object.ApplicationStart()

            self.sap_model = self.sap_object.SapModel
            version = str(self.sap_object.GetOAPIVersionNumber())
            model_path = str(self.sap_model.GetModelFilename())
            return {"connected": True, "version": version, "model_path": model_path}
        except Exception as exc:
            self.sap_object = None
            self.sap_model = None
            return {"connected": False, "error": str(exc)}

    def disconnect(self) -> dict:
        self.sap_model = None
        self.sap_object = None
        return {"disconnected": True}


# ══════════════════════════════════════════════════════════════════════════════
# Backend
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseTablesBackend:
    """Backend standalone para explorar y editar Database Tables de SAP2000."""

    IMPORT_TYPE_LABELS = {
        0: "Not importable",
        1: "Importable (non-interactive)",
        2: "Interactive (unlocked only)",
        3: "Interactive (unlocked + locked)",
    }

    def __init__(self, connection: SapConnection):
        self._conn = connection

    @property
    def sap_model(self):
        if not self._conn.is_connected:
            raise RuntimeError("No hay conexión con SAP2000.")
        return self._conn.sap_model

    # ── Metadata ──────────────────────────────────────────────────────────

    def list_tables(self, include_empty: bool = True) -> List[Dict[str, Any]]:
        """Returns all tables with metadata.

        Args:
            include_empty: If False, filters out tables with no data.

        Returns:
            List of dicts with keys: table_key, table_name, import_type,
            import_label, is_empty.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetAllTables(0, [], [], [], [])
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetAllTables failed: {ret_code}")

        num = raw[0]
        keys = list(raw[1])
        names = list(raw[2])
        imports = list(raw[3])
        empties = list(raw[4])

        tables = []
        for i in range(num):
            if not include_empty and empties[i]:
                continue
            tables.append({
                "table_key": keys[i],
                "table_name": names[i],
                "import_type": imports[i],
                "import_label": self.IMPORT_TYPE_LABELS.get(imports[i], "Unknown"),
                "is_empty": empties[i],
            })
        return tables

    def get_table_fields(self, table_key: str) -> List[Dict[str, Any]]:
        """Returns field metadata for a specific table.

        Returns:
            List of dicts with keys: field_key, field_name, description,
            units, is_importable.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetAllFieldsInTable(
            table_key, 0, 0, [], [], [], [], []
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetAllFieldsInTable failed: {ret_code}")

        num = raw[1]
        fields = []
        for i in range(num):
            fields.append({
                "field_key": raw[2][i],
                "field_name": raw[3][i],
                "description": raw[4][i],
                "units": raw[5][i],
                "is_importable": raw[6][i],
            })
        return fields

    # ── Read ──────────────────────────────────────────────────────────────

    def read_table(
        self, table_key: str, group: str = "All", for_editing: bool = False
    ) -> Dict[str, Any]:
        """Reads a table and returns structured data.

        Args:
            table_key: The table key to read.
            group: Group filter ("All" for everything).
            for_editing: If True, uses GetTableForEditingArray (editable).
                         If False, uses GetTableForDisplayArray (read-only).

        Returns:
            Dict with keys: table_version, field_keys, num_records, rows
            where rows is a list of dicts (one per record).
        """
        SapModel = self.sap_model

        if for_editing:
            raw = SapModel.DatabaseTables.GetTableForEditingArray(
                table_key, group, 0, [], 0, []
            )
        else:
            raw = SapModel.DatabaseTables.GetTableForDisplayArray(
                table_key, [""], group, 0, [], 0, []
            )

        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(
                f"{'GetTableForEditingArray' if for_editing else 'GetTableForDisplayArray'} "
                f"failed: {ret_code}"
            )

        table_version = raw[0]
        field_keys = list(raw[1])
        num_records = raw[2]
        table_data = list(raw[3]) if raw[3] else []

        # Convert flat array to list of dicts
        num_fields = len(field_keys)
        rows = []
        for r in range(num_records):
            row = {}
            for c in range(num_fields):
                row[field_keys[c]] = table_data[r * num_fields + c]
            rows.append(row)

        return {
            "table_version": table_version,
            "field_keys": field_keys,
            "num_records": num_records,
            "rows": rows,
        }

    # ── Write ─────────────────────────────────────────────────────────────

    def write_table(
        self,
        table_key: str,
        field_keys: List[str],
        rows: List[Dict[str, str]],
        table_version: int = 0,
    ) -> Dict[str, Any]:
        """Writes table data and applies changes.

        Args:
            table_key: The table key to write.
            field_keys: Column headers (field key names).
            rows: List of dicts (one per record, keys matching field_keys).
            table_version: Table version (from previous read, or 0).

        Returns:
            Dict with import results (fatal_errors, errors, warnings, info, log).
        """
        SapModel = self.sap_model

        # Flatten rows to flat array
        num_records = len(rows)
        table_data = []
        for row in rows:
            for fk in field_keys:
                table_data.append(str(row.get(fk, "")))

        raw = SapModel.DatabaseTables.SetTableForEditingArray(
            table_key, table_version, field_keys, num_records, table_data
        )
        set_ret = raw[-1] if isinstance(raw, tuple) else raw
        if set_ret != 0:
            raise RuntimeError(f"SetTableForEditingArray failed: {set_ret}")

        # Apply
        raw = SapModel.DatabaseTables.ApplyEditedTables(True, 0, 0, 0, 0, "")
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"ApplyEditedTables failed: {ret_code}")

        return {
            "fatal_errors": raw[0],
            "errors": raw[1],
            "warnings": raw[2],
            "info_msgs": raw[3],
            "import_log": raw[4],
        }

    def cancel_editing(self) -> int:
        """Cancels any pending table edits."""
        return self.sap_model.DatabaseTables.CancelTableEditing()

    # ── Export ────────────────────────────────────────────────────────────

    def export_csv(
        self,
        table_key: str,
        filepath: str,
        group: str = "All",
        separator: str = ",",
    ) -> Dict[str, Any]:
        """Exports a table to a CSV file.

        Args:
            table_key: Table key to export.
            filepath: Full output file path.
            group: Group filter.
            separator: CSV delimiter.

        Returns:
            Dict with table_version and filepath.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetTableForDisplayCSVFile(
            table_key, [""], group, 0, filepath, separator
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetTableForDisplayCSVFile failed: {ret_code}")

        return {"table_version": raw[0], "filepath": filepath}

    def export_csv_string(
        self, table_key: str, group: str = "All", separator: str = ","
    ) -> str:
        """Exports a table as a CSV string."""
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetTableForDisplayCSVString(
            table_key, [""], group, 0, "", separator
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetTableForDisplayCSVString failed: {ret_code}")
        return raw[1]

    def export_xml_string(
        self,
        table_key: str,
        group: str = "All",
        include_schema: bool = True,
    ) -> str:
        """Exports a table as an XML string."""
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.GetTableForDisplayXMLString(
            table_key, [""], group, include_schema, 0, ""
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"GetTableForDisplayXMLString failed: {ret_code}")
        return raw[1]

    def import_csv(
        self,
        table_key: str,
        filepath: str,
        separator: str = ",",
        apply_immediately: bool = True,
    ) -> Dict[str, Any]:
        """Imports table data from a CSV file.

        Args:
            table_key: Table key to import into.
            filepath: Path to CSV file.
            separator: CSV delimiter.
            apply_immediately: If True, calls ApplyEditedTables after import.

        Returns:
            Dict with import results (if applied) or staging confirmation.
        """
        SapModel = self.sap_model
        raw = SapModel.DatabaseTables.SetTableForEditingCSVFile(
            table_key, 0, filepath, separator
        )
        ret_code = raw[-1]
        if ret_code != 0:
            raise RuntimeError(f"SetTableForEditingCSVFile failed: {ret_code}")

        if apply_immediately:
            raw = SapModel.DatabaseTables.ApplyEditedTables(True, 0, 0, 0, 0, "")
            if raw[-1] != 0:
                raise RuntimeError(f"ApplyEditedTables failed: {raw[-1]}")
            return {
                "fatal_errors": raw[0],
                "errors": raw[1],
                "warnings": raw[2],
                "info_msgs": raw[3],
                "import_log": raw[4],
            }

        return {"staged": True, "table_version": raw[0]}

    # ── Model State ───────────────────────────────────────────────────────

    def is_model_locked(self) -> bool:
        """Returns True if the model is locked (analysis has been run)."""
        return bool(self.sap_model.GetModelIsLocked())


# ══════════════════════════════════════════════════════════════════════════════
# Standalone test
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json

    conn = SapConnection()
    res = conn.connect(attach_to_existing=True)
    print(f"Conexión: {res}")

    if res.get("connected"):
        backend = DatabaseTablesBackend(conn)

        try:
            # List tables
            tables = backend.list_tables(include_empty=False)
            print(f"\n═══ Tablas con datos: {len(tables)} ═══")
            for t in tables[:15]:
                print(f"  [{t['import_type']}] {t['table_key']}: {t['table_name']}")

            # Read first non-empty table
            if tables:
                key = tables[0]["table_key"]
                print(f"\n═══ Leyendo tabla: {key} ═══")
                data = backend.read_table(key)
                print(f"  Fields: {data['field_keys']}")
                print(f"  Records: {data['num_records']}")
                for row in data["rows"][:3]:
                    print(f"  → {row}")

                # Get fields
                fields = backend.get_table_fields(key)
                print(f"\n═══ Campos de {key} ═══")
                for f in fields[:5]:
                    print(f"  {f['field_key']}: {f['field_name']} [{f['units']}]")

                # Export CSV string
                csv_str = backend.export_csv_string(key)
                print(f"\n═══ CSV preview ═══")
                print(csv_str[:500])

            # Lock state
            print(f"\nModelo bloqueado: {backend.is_model_locked()}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.disconnect()
```

- [ ] Create file `scripts/database_tables/README.md`:

```markdown
# Database Tables — SAP2000 Module

Module for exploring and editing SAP2000 database tables via direct COM connection.

## Components

| File | Description |
|------|-------------|
| `backend_database_tables.py` | Backend class with high-level table operations |
| `gui_database_tables.py` | PySide6 GUI with table browser and conditional editing |

## Backend API

```python
from backend_database_tables import SapConnection, DatabaseTablesBackend

conn = SapConnection()
conn.connect()
backend = DatabaseTablesBackend(conn)

# List all tables with data
tables = backend.list_tables(include_empty=False)

# Read table as structured rows
data = backend.read_table("Material Properties 01 - General")

# Get field metadata
fields = backend.get_table_fields("Material Properties 01 - General")

# Export to CSV file
backend.export_csv("Material Properties 01 - General", "C:\\temp\\materials.csv")

# Export as CSV/XML strings
csv_str = backend.export_csv_string("Material Properties 01 - General")
xml_str = backend.export_xml_string("Material Properties 01 - General")

# Write table (edit model)
result = backend.write_table(table_key, field_keys, rows)

# Import from CSV file
result = backend.import_csv(table_key, "C:\\temp\\materials.csv")

# Check model lock state
locked = backend.is_model_locked()

conn.disconnect()
```

## GUI Features

- **Table browser**: TreeView with all available tables (filterable)
- **Data viewer**: QTableWidget showing table data with field headers and units
- **Export**: CSV file, XML string export
- **Import**: CSV file import with Apply/Cancel
- **Conditional editing**: Inline editing when model is unlocked; read-only when locked
- **Lock indicator**: Real-time 🔒/🔓 status with 2-second polling

## Wrapper Coverage

18 wrapper scripts in `scripts/wrappers/func_DatabaseTables_*.py` covering all 37 API functions.
See `scripts/registry.json` for the complete registry (category: `Database_Tables`).

## Table Data Format

TableData is a **flat array** stored row-by-row:
```
[field1_row1, field2_row1, ..., fieldN_row1, field1_row2, ...]
```

The backend's `read_table()` converts this to a list of dicts for easy manipulation.

## Import Types

| Code | Meaning |
|------|---------|
| 0 | Not importable |
| 1 | Importable (non-interactive) |
| 2 | Interactive import when model is unlocked |
| 3 | Interactive import when model is unlocked or locked |
```

- [ ] Test standalone: `python scripts/database_tables/backend_database_tables.py` (requires SAP2000 running)

##### Step 6 Verification Checklist
- [ ] `list_tables()` returns tables with metadata
- [ ] `read_table()` returns structured rows from a known table
- [ ] `get_table_fields()` returns field metadata
- [ ] `export_csv()` creates a valid CSV file
- [ ] `export_csv_string()` returns non-empty CSV content
- [ ] `export_xml_string()` returns non-empty XML content
- [ ] `is_model_locked()` returns correct boolean
- [ ] Standalone test (`__main__`) runs and prints results

#### Step 6 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add DatabaseTablesBackend class with high-level API`

---

#### Step 7: PySide6 GUI (gui_database_tables.py)

- [ ] Create file `scripts/database_tables/gui_database_tables.py`:

```python
"""
GUI — SAP2000 Database Tables Explorer (PySide6 Standalone)
============================================================
Browse, view, export and edit SAP2000 database tables.

Features:
    - Left panel: filterable table list with import type indicators
    - Central panel: QTableWidget showing table data
    - Toolbar: Export CSV, Export XML, Import CSV, Refresh, Apply Changes
    - Lock state indicator with 2s polling
    - Conditional editing: enabled only when model is unlocked

Requires: PySide6, comtypes
"""

import sys
import json
import os

from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QToolBar,
    QStatusBar,
    QMainWindow,
)

from backend_database_tables import SapConnection, DatabaseTablesBackend


# ══════════════════════════════════════════════════════════════════════════════
# Workers
# ══════════════════════════════════════════════════════════════════════════════

class ConnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.connect(attach_to_existing=True)
        self.finished.emit(result)


class DisconnectWorker(QThread):
    finished = Signal(dict)

    def __init__(self, connection: SapConnection):
        super().__init__()
        self._conn = connection

    def run(self):
        result = self._conn.disconnect()
        self.finished.emit(result)


class ListTablesWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, backend: DatabaseTablesBackend):
        super().__init__()
        self._backend = backend

    def run(self):
        try:
            tables = self._backend.list_tables(include_empty=True)
            self.finished.emit(tables)
        except Exception as e:
            self.error.emit(str(e))


class ReadTableWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, backend: DatabaseTablesBackend, table_key: str):
        super().__init__()
        self._backend = backend
        self._table_key = table_key

    def run(self):
        try:
            data = self._backend.read_table(self._table_key)
            data["table_key"] = self._table_key
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class WriteTableWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, backend, table_key, field_keys, rows, table_version):
        super().__init__()
        self._backend = backend
        self._table_key = table_key
        self._field_keys = field_keys
        self._rows = rows
        self._table_version = table_version

    def run(self):
        try:
            result = self._backend.write_table(
                self._table_key,
                self._field_keys,
                self._rows,
                self._table_version,
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ExportCsvWorker(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, backend, table_key, filepath):
        super().__init__()
        self._backend = backend
        self._table_key = table_key
        self._filepath = filepath

    def run(self):
        try:
            self._backend.export_csv(self._table_key, self._filepath)
            self.finished.emit(self._filepath)
        except Exception as e:
            self.error.emit(str(e))


class ImportCsvWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, backend, table_key, filepath):
        super().__init__()
        self._backend = backend
        self._table_key = table_key
        self._filepath = filepath

    def run(self):
        try:
            result = self._backend.import_csv(self._table_key, self._filepath)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ══════════════════════════════════════════════════════════════════════════════
# Main Window
# ══════════════════════════════════════════════════════════════════════════════

class DatabaseTablesGUI(QMainWindow):
    """GUI standalone para explorar Database Tables de SAP2000."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAP2000 — Database Tables Explorer")
        self.setMinimumSize(1100, 700)

        # State
        self._conn = SapConnection()
        self._backend = DatabaseTablesBackend(self._conn)
        self._worker = None
        self._current_table_key = None
        self._current_table_version = 0
        self._current_field_keys = []
        self._model_locked = True
        self._tables_cache = []

        # Lock state polling timer
        self._lock_timer = QTimer()
        self._lock_timer.setInterval(2000)
        self._lock_timer.timeout.connect(self._poll_lock_state)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(6)

        # ── Top bar: connection ──────────────────────────────────────────
        top_row = QHBoxLayout()
        self._btn_connect = QPushButton("Conectar a SAP2000")
        self._btn_connect.setFixedHeight(30)
        self._btn_connect.clicked.connect(self._on_connect)
        top_row.addWidget(self._btn_connect)

        self._status_lbl = QLabel("Desconectado")
        self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
        top_row.addWidget(self._status_lbl)

        self._lock_lbl = QLabel("")
        self._lock_lbl.setStyleSheet("font-size: 14px;")
        top_row.addWidget(self._lock_lbl)

        top_row.addStretch()

        self._btn_disconnect = QPushButton("Desconectar")
        self._btn_disconnect.setFixedHeight(30)
        self._btn_disconnect.setEnabled(False)
        self._btn_disconnect.clicked.connect(self._on_disconnect)
        top_row.addWidget(self._btn_disconnect)
        root.addLayout(top_row)

        # ── Main splitter ────────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)

        # Left panel: table list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self._filter_input = QLineEdit()
        self._filter_input.setPlaceholderText("Filtrar tablas...")
        self._filter_input.textChanged.connect(self._on_filter_changed)
        left_layout.addWidget(self._filter_input)

        self._table_tree = QTreeWidget()
        self._table_tree.setHeaderLabels(["Tabla", "Import"])
        self._table_tree.setColumnWidth(0, 280)
        self._table_tree.setColumnWidth(1, 40)
        self._table_tree.itemClicked.connect(self._on_table_selected)
        left_layout.addWidget(self._table_tree)

        splitter.addWidget(left_panel)

        # Right panel: data view + actions
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Action buttons
        btn_row = QHBoxLayout()
        self._btn_refresh = QPushButton("Refrescar")
        self._btn_refresh.setEnabled(False)
        self._btn_refresh.clicked.connect(self._on_refresh_table)
        btn_row.addWidget(self._btn_refresh)

        self._btn_export_csv = QPushButton("Exportar CSV")
        self._btn_export_csv.setEnabled(False)
        self._btn_export_csv.clicked.connect(self._on_export_csv)
        btn_row.addWidget(self._btn_export_csv)

        self._btn_import_csv = QPushButton("Importar CSV")
        self._btn_import_csv.setEnabled(False)
        self._btn_import_csv.clicked.connect(self._on_import_csv)
        btn_row.addWidget(self._btn_import_csv)

        self._btn_apply = QPushButton("Aplicar Cambios")
        self._btn_apply.setEnabled(False)
        self._btn_apply.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; font-weight: bold; }"
            "QPushButton:disabled { background-color: #95a5a6; color: #ecf0f1; }"
        )
        self._btn_apply.clicked.connect(self._on_apply_changes)
        btn_row.addWidget(self._btn_apply)

        btn_row.addStretch()
        right_layout.addLayout(btn_row)

        # Table info label
        self._info_lbl = QLabel("Seleccione una tabla del panel izquierdo")
        self._info_lbl.setStyleSheet("color: #7f8c8d; font-style: italic;")
        right_layout.addWidget(self._info_lbl)

        # Data table
        self._data_table = QTableWidget()
        self._data_table.setFont(QFont("Consolas", 9))
        self._data_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self._data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        right_layout.addWidget(self._data_table)

        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        root.addWidget(splitter)

        # ── Log output ───────────────────────────────────────────────────
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setFont(QFont("Consolas", 8))
        self._log.setMaximumHeight(120)
        root.addWidget(self._log)

    # ══════════════════════════════════════════════════════════════════════
    # Helpers
    # ══════════════════════════════════════════════════════════════════════

    def _log_append(self, text: str):
        self._log.append(text)

    def _set_connected(self, connected: bool):
        self._btn_connect.setEnabled(not connected)
        self._btn_disconnect.setEnabled(connected)
        if connected:
            self._status_lbl.setText("Conectado ✔")
            self._status_lbl.setStyleSheet("color: #27ae60; font-weight: bold;")
            self._lock_timer.start()
        else:
            self._status_lbl.setText("Desconectado")
            self._status_lbl.setStyleSheet("color: #c0392b; font-weight: bold;")
            self._lock_lbl.setText("")
            self._lock_timer.stop()
            self._table_tree.clear()
            self._data_table.setRowCount(0)
            self._data_table.setColumnCount(0)
            self._btn_refresh.setEnabled(False)
            self._btn_export_csv.setEnabled(False)
            self._btn_import_csv.setEnabled(False)
            self._btn_apply.setEnabled(False)

    def _busy(self, is_busy: bool):
        self._btn_connect.setEnabled(not is_busy and not self._conn.is_connected)
        self._btn_disconnect.setEnabled(not is_busy and self._conn.is_connected)
        self._btn_refresh.setEnabled(not is_busy and self._current_table_key is not None)
        self._btn_export_csv.setEnabled(not is_busy and self._current_table_key is not None)
        self._btn_import_csv.setEnabled(
            not is_busy and self._current_table_key is not None and not self._model_locked
        )
        self._btn_apply.setEnabled(
            not is_busy and self._current_table_key is not None and not self._model_locked
        )

    def _update_lock_ui(self):
        if self._model_locked:
            self._lock_lbl.setText("🔒 Modelo bloqueado")
            self._lock_lbl.setToolTip("El modelo está bloqueado — edición deshabilitada")
            self._data_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self._btn_apply.setEnabled(False)
            self._btn_apply.setToolTip("Modelo bloqueado — desbloquee para editar")
            self._btn_import_csv.setEnabled(False)
        else:
            self._lock_lbl.setText("🔓 Modelo desbloqueado")
            self._lock_lbl.setToolTip("El modelo está desbloqueado — edición habilitada")
            self._data_table.setEditTriggers(
                QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed
            )
            if self._current_table_key:
                self._btn_apply.setEnabled(True)
                self._btn_import_csv.setEnabled(True)
            self._btn_apply.setToolTip("")

    def _poll_lock_state(self):
        if not self._conn.is_connected:
            return
        try:
            locked = self._backend.is_model_locked()
            if locked != self._model_locked:
                self._model_locked = locked
                self._update_lock_ui()
        except Exception:
            pass

    # ══════════════════════════════════════════════════════════════════════
    # Connect / Disconnect
    # ══════════════════════════════════════════════════════════════════════

    def _on_connect(self):
        self._log_append("Conectando a SAP2000...")
        self._busy(True)
        self._worker = ConnectWorker(self._conn)
        self._worker.finished.connect(self._on_connect_done)
        self._worker.start()

    def _on_connect_done(self, result: dict):
        self._busy(False)
        if result.get("connected"):
            ver = result.get("version", "?")
            path = result.get("model_path") or "(sin modelo)"
            self._log_append(f"✔ Conectado — v{ver}  |  {path}")
            self._set_connected(True)
            self._poll_lock_state()
            self._update_lock_ui()
            self._load_table_list()
        else:
            self._log_append(f"✘ Error: {result.get('error', '?')}")
            self._set_connected(False)

    def _on_disconnect(self):
        self._busy(True)
        self._worker = DisconnectWorker(self._conn)
        self._worker.finished.connect(self._on_disconnect_done)
        self._worker.start()

    def _on_disconnect_done(self, _):
        self._busy(False)
        self._log_append("✔ Desconectado")
        self._set_connected(False)
        self._current_table_key = None

    # ══════════════════════════════════════════════════════════════════════
    # Table List
    # ══════════════════════════════════════════════════════════════════════

    def _load_table_list(self):
        self._log_append("Cargando lista de tablas...")
        self._worker = ListTablesWorker(self._backend)
        self._worker.finished.connect(self._on_tables_loaded)
        self._worker.error.connect(lambda e: self._log_append(f"✘ Error: {e}"))
        self._worker.start()

    def _on_tables_loaded(self, tables: list):
        self._tables_cache = tables
        self._populate_tree(tables)
        self._log_append(f"✔ {len(tables)} tablas cargadas")

    def _populate_tree(self, tables: list):
        self._table_tree.clear()
        import_icons = {0: "○", 1: "◐", 2: "●", 3: "◉"}

        filter_text = self._filter_input.text().lower()

        for t in tables:
            key = t["table_key"]
            name = t["table_name"]
            imp = t["import_type"]
            empty = t["is_empty"]

            if filter_text and filter_text not in key.lower() and filter_text not in name.lower():
                continue

            item = QTreeWidgetItem([name, import_icons.get(imp, "?")])
            item.setData(0, Qt.UserRole, key)
            item.setToolTip(0, f"Key: {key}\nImport: {t['import_label']}")
            if empty:
                item.setForeground(0, QColor("#95a5a6"))
            self._table_tree.addTopLevelItem(item)

    def _on_filter_changed(self, text: str):
        self._populate_tree(self._tables_cache)

    # ══════════════════════════════════════════════════════════════════════
    # Table Selection & Display
    # ══════════════════════════════════════════════════════════════════════

    def _on_table_selected(self, item: QTreeWidgetItem, column: int):
        table_key = item.data(0, Qt.UserRole)
        if not table_key:
            return
        self._current_table_key = table_key
        self._load_table_data(table_key)

    def _load_table_data(self, table_key: str):
        self._log_append(f"Leyendo: {table_key}...")
        self._busy(True)
        self._worker = ReadTableWorker(self._backend, table_key)
        self._worker.finished.connect(self._on_table_data_loaded)
        self._worker.error.connect(self._on_table_data_error)
        self._worker.start()

    def _on_table_data_loaded(self, data: dict):
        self._busy(False)
        self._current_table_version = data.get("table_version", 0)
        self._current_field_keys = data.get("field_keys", [])
        rows = data.get("rows", [])
        num_records = data.get("num_records", 0)

        self._info_lbl.setText(
            f"Tabla: {data.get('table_key', '?')}  |  "
            f"Registros: {num_records}  |  Campos: {len(self._current_field_keys)}"
        )

        # Populate QTableWidget
        self._data_table.setRowCount(num_records)
        self._data_table.setColumnCount(len(self._current_field_keys))
        self._data_table.setHorizontalHeaderLabels(self._current_field_keys)

        for r, row in enumerate(rows):
            for c, fk in enumerate(self._current_field_keys):
                val = str(row.get(fk, ""))
                cell = QTableWidgetItem(val)
                self._data_table.setItem(r, c, cell)

        self._log_append(
            f"✔ {data.get('table_key')}: {num_records} registros, "
            f"{len(self._current_field_keys)} campos"
        )
        self._update_lock_ui()

    def _on_table_data_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error leyendo tabla: {error}")

    def _on_refresh_table(self):
        if self._current_table_key:
            self._load_table_data(self._current_table_key)

    # ══════════════════════════════════════════════════════════════════════
    # Export CSV
    # ══════════════════════════════════════════════════════════════════════

    def _on_export_csv(self):
        if not self._current_table_key:
            return
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Exportar CSV", "", "CSV Files (*.csv)"
        )
        if not filepath:
            return

        self._log_append(f"Exportando CSV: {self._current_table_key}...")
        self._busy(True)
        self._worker = ExportCsvWorker(
            self._backend, self._current_table_key, filepath
        )
        self._worker.finished.connect(self._on_export_done)
        self._worker.error.connect(self._on_export_error)
        self._worker.start()

    def _on_export_done(self, filepath: str):
        self._busy(False)
        self._log_append(f"✔ CSV exportado: {filepath}")

    def _on_export_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error exportando: {error}")

    # ══════════════════════════════════════════════════════════════════════
    # Import CSV
    # ══════════════════════════════════════════════════════════════════════

    def _on_import_csv(self):
        if not self._current_table_key or self._model_locked:
            return
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Importar CSV", "", "CSV Files (*.csv)"
        )
        if not filepath:
            return

        reply = QMessageBox.question(
            self,
            "Confirmar importación",
            f"¿Importar datos desde:\n{filepath}\n\n"
            f"a la tabla: {self._current_table_key}?\n\n"
            "Los cambios se aplicarán inmediatamente al modelo.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self._log_append(f"Importando CSV: {filepath}...")
        self._busy(True)
        self._worker = ImportCsvWorker(
            self._backend, self._current_table_key, filepath
        )
        self._worker.finished.connect(self._on_import_done)
        self._worker.error.connect(self._on_import_error)
        self._worker.start()

    def _on_import_done(self, result: dict):
        self._busy(False)
        fatal = result.get("fatal_errors", 0)
        errors = result.get("errors", 0)
        warnings = result.get("warnings", 0)
        self._log_append(
            f"✔ Importación completada — Fatal: {fatal}, Errors: {errors}, Warnings: {warnings}"
        )
        if fatal > 0 or errors > 0:
            QMessageBox.warning(
                self,
                "Errores en importación",
                f"Fatal: {fatal}\nErrors: {errors}\nWarnings: {warnings}\n\n"
                f"Revise el log para detalles.",
            )
        # Refresh table
        self._on_refresh_table()

    def _on_import_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error importando: {error}")

    # ══════════════════════════════════════════════════════════════════════
    # Apply Changes (from in-place editing)
    # ══════════════════════════════════════════════════════════════════════

    def _on_apply_changes(self):
        if not self._current_table_key or self._model_locked:
            return
        if not self._current_field_keys:
            return

        reply = QMessageBox.question(
            self,
            "Confirmar cambios",
            f"¿Aplicar cambios editados a la tabla:\n{self._current_table_key}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        # Collect data from QTableWidget
        rows = []
        for r in range(self._data_table.rowCount()):
            row = {}
            for c, fk in enumerate(self._current_field_keys):
                item = self._data_table.item(r, c)
                row[fk] = item.text() if item else ""
            rows.append(row)

        self._log_append(f"Aplicando {len(rows)} registros a {self._current_table_key}...")
        self._busy(True)
        self._worker = WriteTableWorker(
            self._backend,
            self._current_table_key,
            self._current_field_keys,
            rows,
            self._current_table_version,
        )
        self._worker.finished.connect(self._on_apply_done)
        self._worker.error.connect(self._on_apply_error)
        self._worker.start()

    def _on_apply_done(self, result: dict):
        self._busy(False)
        fatal = result.get("fatal_errors", 0)
        errors = result.get("errors", 0)
        warnings = result.get("warnings", 0)
        self._log_append(
            f"✔ Cambios aplicados — Fatal: {fatal}, Errors: {errors}, Warnings: {warnings}"
        )
        if fatal > 0 or errors > 0:
            QMessageBox.warning(
                self, "Errores al aplicar",
                f"Fatal: {fatal}\nErrors: {errors}\nWarnings: {warnings}",
            )
        self._on_refresh_table()

    def _on_apply_error(self, error: str):
        self._busy(False)
        self._log_append(f"✘ Error aplicando cambios: {error}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = DatabaseTablesGUI()
    win.show()
    sys.exit(app.exec())
```

- [ ] Test GUI: `python scripts/database_tables/gui_database_tables.py`

##### Step 7 Verification Checklist
- [ ] GUI opens without errors
- [ ] Connect button attaches to running SAP2000
- [ ] Table list populates in left panel
- [ ] Filter input narrows the table list
- [ ] Clicking a table loads data in the right panel
- [ ] Column headers show field keys
- [ ] Lock indicator shows 🔒 when model is locked (after running analysis)
- [ ] Lock indicator shows 🔓 when model is unlocked
- [ ] When unlocked: double-click enables cell editing, Apply Changes is active
- [ ] When locked: cells are read-only, Apply Changes is grayed out with tooltip
- [ ] Export CSV produces a valid file
- [ ] Import CSV (when unlocked) imports data and refreshes table
- [ ] Disconnect button works and resets UI

#### Step 7 STOP & COMMIT
**STOP & COMMIT:** `feat(db-tables): add PySide6 GUI with conditional editing and lock state monitoring`
