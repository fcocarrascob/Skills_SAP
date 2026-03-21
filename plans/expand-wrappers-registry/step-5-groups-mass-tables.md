# Step 5: Groups, Mass Source & Database Tables

## Goal
Add 6 wrapper scripts for group management (`GroupDef.SetGroup_1`, `GroupDef.GetNameList`, `GroupDef.GetAssignments`), mass source configuration (`SourceMass.SetDefault`), database-table extraction (`DatabaseTables.GetTableForDisplayArray`), and nodal mass assignment (`PointObj.SetLoadMass`). Register all in `registry.json`.

## Prerequisites
Make sure you are on the `expand-wrappers-registry` branch and Steps 1-4 are committed.

### Step-by-Step Instructions

#### Step 5.1: Create `func_GroupDef_SetGroup_1.py`
- [ ] Create file `scripts/wrappers/func_GroupDef_SetGroup_1.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_GroupDef_SetGroup_1.py`:

```python
# ============================================================
# Wrapper: SapModel.GroupDef.SetGroup_1
# Category: Groups
# Description: Create or modify a group definition
# Verified: pending
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new group or modifies an existing group definition.
       Groups are used to organize objects for selection, design,
       output, and load assignment.

API Signature:
  SapModel.GroupDef.SetGroup_1(Name, Color, SpecifiedForSelection,
      SpecifiedForSectionCutDefinition, SpecifiedForSteelDesign,
      SpecifiedForConcreteDesign, SpecifiedForAluminumDesign,
      SpecifiedForStaticNLActiveStage, SpecifiedForAutoSeismicOutput,
      SpecifiedForAutoWindOutput, SpecifiedForMassAndWeight,
      SpecifiedForColorByGroup) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name                               : str  — Group name
  Color                              : int  — Display color (-1=default)
  SpecifiedForSelection              : bool — Available for selection (True)
  SpecifiedForSectionCutDefinition   : bool — Section cut group (True)
  SpecifiedForSteelDesign            : bool — Steel design group (True)
  SpecifiedForConcreteDesign         : bool — Concrete design group (True)
  SpecifiedForAluminumDesign         : bool — Aluminum design group (False)
  SpecifiedForStaticNLActiveStage    : bool — NL staged construction (False)
  SpecifiedForAutoSeismicOutput      : bool — Seismic output group (False)
  SpecifiedForAutoWindOutput         : bool — Wind output group (False)
  SpecifiedForMassAndWeight          : bool — Mass & weight group (True)
  SpecifiedForColorByGroup           : bool — Color by group display (False)
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# --- Target function: create multiple groups ---
# Structural groups
ret = SapModel.GroupDef.SetGroup_1(
    "COLUMNS", -1,
    True, True, False, True, False, False, True, False, True, False
)
assert ret == 0, f"SetGroup_1(COLUMNS) failed: {ret}"

ret = SapModel.GroupDef.SetGroup_1(
    "BEAMS", -1,
    True, True, True, False, False, False, False, False, True, False
)
assert ret == 0, f"SetGroup_1(BEAMS) failed: {ret}"

ret = SapModel.GroupDef.SetGroup_1(
    "FOUNDATION", -1,
    True, False, False, True, False, False, True, True, True, False
)
assert ret == 0, f"SetGroup_1(FOUNDATION) failed: {ret}"

# --- Verification ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

group_count = raw[0]
group_names = list(raw[1])
assert "COLUMNS" in group_names, f"COLUMNS not in groups: {group_names}"
assert "BEAMS" in group_names, f"BEAMS not in groups: {group_names}"
assert "FOUNDATION" in group_names

# --- Result ---
result["function"] = "SapModel.GroupDef.SetGroup_1"
result["groups_created"] = ["COLUMNS", "BEAMS", "FOUNDATION"]
result["total_groups"] = group_count
result["all_groups"] = group_names
result["status"] = "verified"
```

#### Step 5.2: Create `func_GroupDef_GetNameList.py`
- [ ] Create file `scripts/wrappers/func_GroupDef_GetNameList.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_GroupDef_GetNameList.py`:

```python
# ============================================================
# Wrapper: SapModel.GroupDef.GetNameList
# Category: Groups
# Description: Get list of all defined group names
# Verified: pending
# Prerequisites: Model open
# ============================================================
"""
Usage: Returns the names and count of all groups defined in the model.
       The "All" group always exists by default.

API Signature:
  SapModel.GroupDef.GetNameList(NumberNames, MyName) -> ret_code

ByRef Output (2 values):
  NumberNames : int   — total number of groups
  MyName[]    : str[] — array of group names

Parameters:
  NumberNames : int   — placeholder (pass 0)
  MyName      : list  — placeholder (pass [])
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()

# Create some groups first
SapModel.GroupDef.SetGroup_1(
    "LEVEL_1", -1, True, False, False, False, False, False, False, False, False, False
)
SapModel.GroupDef.SetGroup_1(
    "LEVEL_2", -1, True, False, False, False, False, False, False, False, False, False
)

# --- Target function ---
raw = SapModel.GroupDef.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"

num_groups = raw[0]
group_names = list(raw[1])

assert num_groups >= 3, f"Expected >=3 groups (All + 2 custom), got {num_groups}"
assert "All" in group_names, f"Default 'All' group missing: {group_names}"
assert "LEVEL_1" in group_names
assert "LEVEL_2" in group_names

# --- Result ---
result["function"] = "SapModel.GroupDef.GetNameList"
result["num_groups"] = num_groups
result["group_names"] = group_names
result["status"] = "verified"
```

#### Step 5.3: Create `func_GroupDef_GetAssignments.py`
- [ ] Create file `scripts/wrappers/func_GroupDef_GetAssignments.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_GroupDef_GetAssignments.py`:

```python
# ============================================================
# Wrapper: SapModel.GroupDef.GetAssignments
# Category: Groups
# Description: Get objects assigned to a group
# Verified: pending
# Prerequisites: Model open, group with assigned objects
# ============================================================
"""
Usage: Retrieves the objects assigned to a specified group.
       Returns object types and names for each member.

API Signature:
  SapModel.GroupDef.GetAssignments(Name,
      NumberItems, ObjectType, ObjectName) -> ret_code

ByRef Output (3 values):
  NumberItems  : int   — number of objects in group
  ObjectType[] : int[] — object type codes:
                         1=Point, 2=Frame, 3=Cable, 4=Tendon,
                         5=Area, 6=Solid, 7=Link
  ObjectName[] : str[] — object names

Parameters:
  Name         : str  — Group name
  NumberItems  : int  — placeholder (pass 0)
  ObjectType   : list — placeholder (pass [])
  ObjectName   : list — placeholder (pass [])
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# Material & section
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Create structural elements
col1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 3, "", "SEC_TEST", "")
assert col1[-1] == 0
col2 = SapModel.FrameObj.AddByCoord(5, 0, 0, 5, 0, 3, "", "SEC_TEST", "")
assert col2[-1] == 0
beam = SapModel.FrameObj.AddByCoord(0, 0, 3, 5, 0, 3, "", "SEC_TEST", "")
assert beam[-1] == 0

# Create groups and assign objects
SapModel.GroupDef.SetGroup_1(
    "MY_COLUMNS", -1, True, False, False, False, False, False, False, False, False, False
)
ret = SapModel.FrameObj.SetGroupAssign(col1[0], "MY_COLUMNS")
assert ret == 0
ret = SapModel.FrameObj.SetGroupAssign(col2[0], "MY_COLUMNS")
assert ret == 0

# --- Target function ---
raw = SapModel.GroupDef.GetAssignments("MY_COLUMNS", 0, [], [])
ret_code = raw[-1]
assert ret_code == 0, f"GetAssignments failed: {ret_code}"

num_items = raw[0]
obj_types = list(raw[1])
obj_names = list(raw[2])

assert num_items == 2, f"Expected 2 items, got {num_items}"
assert all(t == 2 for t in obj_types), f"Expected all Frame (2), got: {obj_types}"

# --- Result ---
result["function"] = "SapModel.GroupDef.GetAssignments"
result["group_name"] = "MY_COLUMNS"
result["num_items"] = num_items
result["object_types"] = obj_types
result["object_names"] = obj_names
result["status"] = "verified"
```

#### Step 5.4: Create `func_SourceMass_SetDefault.py`
- [ ] Create file `scripts/wrappers/func_SourceMass_SetDefault.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_SourceMass_SetDefault.py`:

```python
# ============================================================
# Wrapper: SapModel.SourceMass.SetDefault
# Category: Mass_Source
# Description: Set the default mass source
# Verified: pending
# Prerequisites: Model open, mass source defined
# ============================================================
"""
Usage: Sets a named mass source as the default for analysis.
       The default mass source is used by SAP2000 to calculate
       seismic weight, modal mass, and mass participation.

IMPORTANT: The API path is SapModel.SourceMass (NOT SapModel.MassSource).

API Signature:
  SapModel.SourceMass.SetDefault(Name) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name : str — Mass source name to set as default
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites: create a mass source ---
# SetMassSource(Name, MassFromElements, MassFromMasses, MassFromLoads,
#               IsDefault, NumberLoads, LoadPat, SF)
ret = SapModel.SourceMass.SetMassSource(
    "SEISMIC_MASS",  # Name
    True,            # MassFromElements
    True,            # MassFromMasses
    True,            # MassFromLoads
    False,           # IsDefault (not yet)
    1,               # NumberLoads
    ["DEAD"],        # LoadPat[]
    [1.0]            # SF[] (scale factors)
)
assert ret == 0, f"SetMassSource failed: {ret}"

# --- Target function: set as default ---
ret = SapModel.SourceMass.SetDefault("SEISMIC_MASS")
assert ret == 0, f"SetDefault(SEISMIC_MASS) failed: {ret}"

# --- Verification: read back default ---
raw = SapModel.SourceMass.GetDefault("")
ret_code = raw[-1]
assert ret_code == 0, f"GetDefault failed: {ret_code}"
default_name = raw[0]
assert default_name == "SEISMIC_MASS", f"Expected SEISMIC_MASS, got: {default_name}"

# --- Result ---
result["function"] = "SapModel.SourceMass.SetDefault"
result["default_mass_source"] = default_name
result["status"] = "verified"
```

#### Step 5.5: Create `func_DatabaseTables_GetTableForDisplayArray.py`
- [ ] Create file `scripts/wrappers/func_DatabaseTables_GetTableForDisplayArray.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_DatabaseTables_GetTableForDisplayArray.py`:

```python
# ============================================================
# Wrapper: SapModel.DatabaseTables.GetTableForDisplayArray
# Category: Database_Tables
# Description: Extract data from SAP2000 display tables
# Verified: pending
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
raw = SapModel.DatabaseTables.GetTableForDisplayArray(
    "Joint Coordinates",  # TableKey
    "",                   # FieldKeyList (all fields)
    "",                   # GroupName (all)
    "",                   # TableVersion (ByRef)
    [],                   # FieldKeysIncluded (ByRef)
    0,                    # NumberRecords (ByRef)
    []                    # TableData (ByRef)
)
ret_code = raw[-1]
assert ret_code == 0, f"GetTableForDisplayArray failed: {ret_code}"

table_version = raw[0]
field_keys    = list(raw[1])
num_records   = raw[2]
table_data    = list(raw[3])

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
```

#### Step 5.6: Create `func_PointObj_SetLoadMass.py`
- [ ] Create file `scripts/wrappers/func_PointObj_SetLoadMass.py`
- [ ] Copy and paste code below into `scripts/wrappers/func_PointObj_SetLoadMass.py`:

```python
# ============================================================
# Wrapper: SapModel.PointObj.SetLoadMass
# Category: Object_Model
# Description: Assign concentrated mass to a joint
# Verified: pending
# Prerequisites: Model open, point object exists
# ============================================================
"""
Usage: Assigns a concentrated (lumped) mass to a point object.
       Used for equipment loads, non-structural mass, and dynamic
       analysis mass idealization. The mass is 6-DOF.

API Signature:
  SapModel.PointObj.SetLoadMass(Name, LoadPat, Value,
      Replace, CSys, ItemType) -> ret_code

ByRef Output:
  ret_code (0=success) — returned directly

Parameters:
  Name     : str      — Point object name
  LoadPat  : str      — Load pattern name (typically "DEAD" or mass pattern)
  Value    : float[6] — Mass values [M_UX, M_UY, M_UZ, M_RX, M_RY, M_RZ]
                         in [M] units (e.g., kg for kN_m_C)
  Replace  : bool     — True=replace existing, False=add to existing
  CSys     : str      — Coordinate system ("Global" or local)
  ItemType : int      — 0=Object, 1=Group, 2=SelectedObjects
"""

# --- Minimal setup ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0

# --- Prerequisites ---
ret = SapModel.PropMaterial.SetMaterial("STEEL_TEST", 1)
assert ret == 0
ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "STEEL_TEST", 0.3, 0.2)
assert ret == 0

# Create a column with a joint at the top
col = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 5, "", "SEC_TEST", "")
assert col[-1] == 0

# Support at base
ret = SapModel.PointObj.SetRestraint("1", [True, True, True, True, True, True])
assert ret == 0

# --- Target function: assign 5000 kg mass at top node ---
# Translational mass in all 3 directions, no rotational inertia
ret = SapModel.PointObj.SetLoadMass(
    "2", "DEAD",
    [5000, 5000, 5000, 0, 0, 0],  # 5 tonnes translational mass
    True,     # Replace
    "Global"  # CSys
)
assert ret == 0, f"SetLoadMass failed: {ret}"

# Add additional equipment mass
ret = SapModel.PointObj.SetLoadMass(
    "2", "DEAD",
    [1000, 1000, 0, 0, 0, 0],  # 1 tonne X/Y only (machine on vibration isolators)
    False,    # Add to existing (not replace)
    "Global"
)
assert ret == 0, f"SetLoadMass (add) failed: {ret}"

# --- Result ---
result["function"] = "SapModel.PointObj.SetLoadMass"
result["joint"] = "2"
result["mass_assigned"] = [5000, 5000, 5000, 0, 0, 0]
result["mass_added"]    = [1000, 1000, 0, 0, 0, 0]
result["status"] = "verified"
```

#### Step 5.7: Execute & Verify All Wrappers
- [ ] Ensure SAP2000 is connected (`connect_sap2000`)
- [ ] Execute each wrapper via `run_sap_script` and verify success:
  - `func_GroupDef_SetGroup_1` → save as `func_GroupDef_SetGroup_1`
  - `func_GroupDef_GetNameList` → save as `func_GroupDef_GetNameList`
  - `func_GroupDef_GetAssignments` → save as `func_GroupDef_GetAssignments`
  - `func_SourceMass_SetDefault` → save as `func_SourceMass_SetDefault`
  - `func_DatabaseTables_GetTableForDisplayArray` → save as `func_DatabaseTables_GetTableForDisplayArray`
  - `func_PointObj_SetLoadMass` → save as `func_PointObj_SetLoadMass`

#### Step 5.8: Register Functions in Registry
- [ ] Call `register_verified_function` for each of the 6 functions:

**SapModel.GroupDef.SetGroup_1:**
```json
{
  "function_path": "SapModel.GroupDef.SetGroup_1",
  "category": "Groups",
  "description": "Create or modify a group definition with all flags",
  "signature": "(Name, Color, SpecifiedForSelection, SpecifiedForSectionCutDefinition, SpecifiedForSteelDesign, SpecifiedForConcreteDesign, SpecifiedForAluminumDesign, SpecifiedForStaticNLActiveStage, SpecifiedForAutoSeismicOutput, SpecifiedForAutoWindOutput, SpecifiedForMassAndWeight, SpecifiedForColorByGroup) -> ret_code",
  "parameter_notes": "Name: str; Color: int (-1=default); 10 bool flags for selection, section cuts, design contexts, mass/weight, etc. Typically set SpecifiedForSelection=True, others as needed.",
  "wrapper_script": "func_GroupDef_SetGroup_1",
  "notes": "Returns ret_code (0=success). 'All' group always exists. Use FrameObj.SetGroupAssign / AreaObj.SetGroupAssign to add objects."
}
```

**SapModel.GroupDef.GetNameList:**
```json
{
  "function_path": "SapModel.GroupDef.GetNameList",
  "category": "Groups",
  "description": "Get list of all defined group names",
  "signature": "(NumberNames, MyName) -> ret_code",
  "parameter_notes": "NumberNames: int (pass 0, ByRef); MyName: list (pass [], ByRef returns str[])",
  "wrapper_script": "func_GroupDef_GetNameList",
  "notes": "Returns ret_code=raw[-1], count=raw[0], names=raw[1]. Default 'All' group always present."
}
```

**SapModel.GroupDef.GetAssignments:**
```json
{
  "function_path": "SapModel.GroupDef.GetAssignments",
  "category": "Groups",
  "description": "Get objects assigned to a group",
  "signature": "(Name, NumberItems, ObjectType, ObjectName) -> ret_code",
  "parameter_notes": "Name: str (group name); NumberItems: int (pass 0, ByRef); ObjectType: list (ByRef int[] — 1=Point, 2=Frame, 3=Cable, 4=Tendon, 5=Area, 6=Solid, 7=Link); ObjectName: list (ByRef str[])",
  "wrapper_script": "func_GroupDef_GetAssignments",
  "notes": "Returns ret_code=raw[-1], count=raw[0], types=raw[1], names=raw[2]. Use with SetGroupAssign on object types."
}
```

**SapModel.SourceMass.SetDefault:**
```json
{
  "function_path": "SapModel.SourceMass.SetDefault",
  "category": "Mass_Source",
  "description": "Set the default mass source for analysis",
  "signature": "(Name) -> ret_code",
  "parameter_notes": "Name: str — mass source name to set as default",
  "wrapper_script": "func_SourceMass_SetDefault",
  "notes": "IMPORTANT: API path is SapModel.SourceMass (NOT SapModel.MassSource). Use SetMassSource to define mass sources before setting default. Use GetDefault to verify."
}
```

**SapModel.DatabaseTables.GetTableForDisplayArray:**
```json
{
  "function_path": "SapModel.DatabaseTables.GetTableForDisplayArray",
  "category": "Database_Tables",
  "description": "Extract data from SAP2000 display tables as 1D array",
  "signature": "(TableKey, FieldKeyList, GroupName, TableVersion, FieldKeysIncluded, NumberRecords, TableData) -> ret_code",
  "parameter_notes": "TableKey: str (e.g., 'Joint Coordinates', 'Frame Assignments - Summary'); FieldKeyList: str (comma-separated or '' for all); GroupName: str ('' for all); 4 ByRef: TableVersion, FieldKeysIncluded[], NumberRecords, TableData[]",
  "wrapper_script": "func_DatabaseTables_GetTableForDisplayArray",
  "notes": "Data returned as 1D row-major array. num_cols=len(FieldKeysIncluded), parse rows: tableData[i*num_cols:(i+1)*num_cols]. Use GetAllTables to discover available TableKeys."
}
```

**SapModel.PointObj.SetLoadMass:**
```json
{
  "function_path": "SapModel.PointObj.SetLoadMass",
  "category": "Object_Model",
  "description": "Assign concentrated (lumped) mass to a joint",
  "signature": "(Name, LoadPat, Value, Replace, CSys, ItemType) -> ret_code",
  "parameter_notes": "Name: str; LoadPat: str (e.g., 'DEAD'); Value: float[6] [M_UX, M_UY, M_UZ, M_RX, M_RY, M_RZ] in mass units; Replace: bool; CSys: str ('Global'); ItemType: int (0)",
  "wrapper_script": "func_PointObj_SetLoadMass",
  "notes": "Returns ret_code (0=success). Use Replace=True to overwrite, False to add to existing mass. For kN_m_C units, mass is in kg."
}
```

##### Step 5 Verification Checklist
- [ ] All 6 wrappers exist in `scripts/wrappers/`
- [ ] All 6 wrappers executed successfully via `run_sap_script` (status=verified)
- [ ] All 6 functions registered in `registry.json` with full metadata
- [ ] Final registry count ≈ 89 (58 original + 31 new)

#### Step 5 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
```powershell
git add scripts/wrappers/func_GroupDef_SetGroup_1.py scripts/wrappers/func_GroupDef_GetNameList.py scripts/wrappers/func_GroupDef_GetAssignments.py scripts/wrappers/func_SourceMass_SetDefault.py scripts/wrappers/func_DatabaseTables_GetTableForDisplayArray.py scripts/wrappers/func_PointObj_SetLoadMass.py scripts/registry.json
git commit -m "feat: add groups, mass source, database tables, and nodal mass wrappers"
```

---

## Final PR Summary

After all 5 steps are committed, the PR should contain:

| Step | Wrappers | Functions |
|------|----------|-----------|
| 1 — File Operations & Templates | 5 | OpenFile, New2DFrame, New3DFrame, NewBeam, NewWall |
| 2 — Load Assignments | 6 | PointObj.SetLoadForce, FrameObj.SetLoadDistributed, FrameObj.SetLoadPoint, AreaObj.SetLoadUniform, AreaObj.SetLoadGravity, FrameObj.SetLoadTemperature |
| 3 — Frame Properties & Releases | 7 | PropFrame.SetPipe/SetChannel/SetAngle/SetTee, FrameObj.SetReleases/SetEndLengthOffset, PropFrame.SetModifiers |
| 4 — Design & Results | 7 | DesignSteel.StartDesign/SetCode, DesignConcrete.StartDesign, Results.FrameForce/JointDispl/JointReact/AreaForceShell |
| 5 — Groups, Mass & Tables | 6 | GroupDef.SetGroup_1/GetNameList/GetAssignments, SourceMass.SetDefault, DatabaseTables.GetTableForDisplayArray, PointObj.SetLoadMass |
| **Total** | **31** | |

Final commit to merge into `main`:
```powershell
git push origin expand-wrappers-registry
```
