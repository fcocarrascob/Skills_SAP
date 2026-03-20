# Function Registry — Implementation Plan

## Goal
Create a system that catalogs verified SAP2000 API functions, wraps them in reusable scripts, auto-registers on successful execution, and exposes the registry via MCP tools so the agent can look up verified functions before generating scripts.

## Prerequisites
Make sure that you are currently on the `feature/function-registry` branch before beginning implementation.
If not, move to the correct branch. If the branch does not exist, create it from main.

---

### Step-by-Step Instructions

---

#### Step 1: Data Model and Registry Module (`function_registry.py` + `registry.json`)

- [x] Create the initial empty registry JSON file at `scripts/registry.json`:

```json
{
  "version": "1.0",
  "functions": {},
  "summary": {
    "total_registered": 0,
    "total_verified": 0,
    "last_updated": null
  }
}
```

- [x] Create the registry module at `mcp_server/function_registry.py`:

```python
"""
SAP2000 Function Registry — Catalog of verified API functions.

Tracks which SAP2000 API functions have been verified, in which scripts
they are used, and provides search/filter capabilities for the agent.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# registry.json lives in scripts/ at the workspace root
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "scripts" / "registry.json"

_EMPTY_REGISTRY = {
    "version": "1.0",
    "functions": {},
    "summary": {
        "total_registered": 0,
        "total_verified": 0,
        "last_updated": None,
    },
}


class FunctionRegistry:
    """
    Manages a JSON file that catalogs verified SAP2000 API functions.

    Each function entry records its category, description, verification
    status, wrapper script, and which user scripts use it.
    """

    def __init__(self, registry_path: Path | None = None):
        self._path = registry_path or REGISTRY_PATH
        self._data: dict | None = None

    # ── Persistence ───────────────────────────────────────────────────

    def _load(self) -> dict:
        """Load the registry from disk, or return empty if missing."""
        if self._data is not None:
            return self._data

        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to read registry, starting empty: %s", exc)
                self._data = json.loads(json.dumps(_EMPTY_REGISTRY))
        else:
            self._data = json.loads(json.dumps(_EMPTY_REGISTRY))

        return self._data

    def _save(self) -> None:
        """Persist the registry atomically (write to tmp then rename)."""
        data = self._load()
        self._update_summary(data)

        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._path.with_suffix(".tmp")
        try:
            tmp_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            tmp_path.replace(self._path)
        except OSError as exc:
            logger.exception("Failed to save registry: %s", exc)
            raise

    @staticmethod
    def _update_summary(data: dict) -> None:
        """Recompute the summary counters."""
        funcs = data.get("functions", {})
        data["summary"] = {
            "total_registered": len(funcs),
            "total_verified": sum(1 for f in funcs.values() if f.get("verified")),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    # ── Public API ────────────────────────────────────────────────────

    def register_function(
        self,
        function_path: str,
        category: str,
        description: str = "",
        signature: str = "",
        wrapper_script: str = "",
        parameter_notes: str = "",
        notes: str = "",
    ) -> dict:
        """
        Register a new function or update an existing one.

        Parameters
        ----------
        function_path : str
            Dot-path like "SapModel.FrameObj.AddByCoord".
        category : str
            API category (e.g. "Object_Model", "Properties").
        description : str
            Human-readable description.
        signature : str
            VB6/API signature string.
        wrapper_script : str
            Name of the wrapper script (without .py).
        parameter_notes : str
            Brief notes about parameters.
        notes : str
            Extra notes (e.g. ByRef layout).

        Returns
        -------
        dict  {registered: True, function_path, is_new}
        """
        data = self._load()
        funcs = data.setdefault("functions", {})

        is_new = function_path not in funcs
        now = datetime.now(timezone.utc).isoformat()

        if is_new:
            funcs[function_path] = {
                "category": category,
                "description": description,
                "signature": signature,
                "verified": False,
                "first_verified": None,
                "last_verified": None,
                "verification_count": 0,
                "wrapper_script": wrapper_script,
                "used_in_scripts": [],
                "parameter_notes": parameter_notes,
                "known_errors": [],
                "notes": notes,
            }
        else:
            entry = funcs[function_path]
            if category:
                entry["category"] = category
            if description:
                entry["description"] = description
            if signature:
                entry["signature"] = signature
            if wrapper_script:
                entry["wrapper_script"] = wrapper_script
            if parameter_notes:
                entry["parameter_notes"] = parameter_notes
            if notes:
                entry["notes"] = notes

        self._save()
        return {
            "registered": True,
            "function_path": function_path,
            "is_new": is_new,
        }

    def mark_verified(
        self,
        function_path: str,
        script_name: str = "",
    ) -> dict:
        """
        Mark a function as verified and optionally link it to a script.

        If the function is not yet registered, it is auto-registered with
        minimal metadata.

        Parameters
        ----------
        function_path : str
            Dot-path of the function.
        script_name : str
            Name of the script that verified this function.

        Returns
        -------
        dict  {verified: True, function_path, verification_count}
        """
        data = self._load()
        funcs = data.setdefault("functions", {})

        now = datetime.now(timezone.utc).isoformat()

        if function_path not in funcs:
            funcs[function_path] = {
                "category": "",
                "description": "",
                "signature": "",
                "verified": True,
                "first_verified": now,
                "last_verified": now,
                "verification_count": 1,
                "wrapper_script": "",
                "used_in_scripts": [script_name] if script_name else [],
                "parameter_notes": "",
                "known_errors": [],
                "notes": "",
            }
        else:
            entry = funcs[function_path]
            entry["verified"] = True
            entry["last_verified"] = now
            entry["verification_count"] = entry.get("verification_count", 0) + 1
            if not entry.get("first_verified"):
                entry["first_verified"] = now
            if script_name and script_name not in entry.get("used_in_scripts", []):
                entry.setdefault("used_in_scripts", []).append(script_name)

        self._save()
        return {
            "verified": True,
            "function_path": function_path,
            "verification_count": funcs[function_path]["verification_count"],
        }

    def get_function(self, function_path: str) -> dict:
        """
        Get the full detail of a registered function.

        Returns
        -------
        dict  The function entry, or {error} if not found.
        """
        data = self._load()
        entry = data.get("functions", {}).get(function_path)
        if entry is None:
            return {"error": f"Function '{function_path}' not found in registry."}
        return {"function_path": function_path, **entry}

    def list_functions(
        self,
        category: str | None = None,
        verified_only: bool = False,
        query: str | None = None,
    ) -> list[dict]:
        """
        List functions with optional filters.

        Parameters
        ----------
        category : str | None
            Filter by category (case-insensitive substring match).
        verified_only : bool
            If True, return only verified functions.
        query : str | None
            Keyword search across function_path, description, notes.

        Returns
        -------
        list[dict]  Each dict: {function_path, category, description, verified, verification_count, wrapper_script}
        """
        data = self._load()
        results = []

        for fpath, entry in data.get("functions", {}).items():
            if verified_only and not entry.get("verified"):
                continue
            if category:
                if category.lower() not in entry.get("category", "").lower():
                    continue
            if query:
                q = query.lower()
                searchable = (
                    fpath.lower()
                    + " " + entry.get("description", "").lower()
                    + " " + entry.get("notes", "").lower()
                    + " " + entry.get("parameter_notes", "").lower()
                )
                if q not in searchable:
                    continue

            results.append({
                "function_path": fpath,
                "category": entry.get("category", ""),
                "description": entry.get("description", ""),
                "verified": entry.get("verified", False),
                "verification_count": entry.get("verification_count", 0),
                "wrapper_script": entry.get("wrapper_script", ""),
            })

        return results

    def get_summary(self) -> dict:
        """
        Return a coverage summary of the registry.

        Returns
        -------
        dict  {total_registered, total_verified, last_updated, categories}
        """
        data = self._load()
        self._update_summary(data)

        # Count per category
        cat_counts: dict[str, dict] = {}
        for entry in data.get("functions", {}).values():
            cat = entry.get("category", "Uncategorized")
            if cat not in cat_counts:
                cat_counts[cat] = {"registered": 0, "verified": 0}
            cat_counts[cat]["registered"] += 1
            if entry.get("verified"):
                cat_counts[cat]["verified"] += 1

        return {
            **data["summary"],
            "categories": cat_counts,
        }

    def reload(self) -> None:
        """Force reload from disk on next access."""
        self._data = None


# Module-level singleton
registry = FunctionRegistry()
```

- [x] Create the unit test file at `mcp_server/tests/test_function_registry.py`:

```python
"""
Unit tests for the Function Registry.

Run with: python -m pytest mcp_server/tests/test_function_registry.py -v
"""

import sys
from pathlib import Path

# Add mcp_server to path so imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from function_registry import FunctionRegistry


@pytest.fixture
def registry(tmp_path):
    """Create a FunctionRegistry backed by a temporary JSON file."""
    path = tmp_path / "registry.json"
    return FunctionRegistry(registry_path=path)


class TestRegisterFunction:
    """Tests for register_function."""

    def test_register_new_function(self, registry):
        """Registering a new function creates an entry."""
        result = registry.register_function(
            function_path="SapModel.FrameObj.AddByCoord",
            category="Object_Model",
            description="Add a frame by coordinates",
        )
        assert result["registered"] is True
        assert result["is_new"] is True
        assert result["function_path"] == "SapModel.FrameObj.AddByCoord"

    def test_register_existing_function_updates(self, registry):
        """Re-registering updates fields without creating a duplicate."""
        registry.register_function(
            function_path="SapModel.FrameObj.AddByCoord",
            category="Object_Model",
            description="Original description",
        )
        result = registry.register_function(
            function_path="SapModel.FrameObj.AddByCoord",
            category="Object_Model",
            description="Updated description",
        )
        assert result["registered"] is True
        assert result["is_new"] is False

        entry = registry.get_function("SapModel.FrameObj.AddByCoord")
        assert entry["description"] == "Updated description"

    def test_register_with_all_fields(self, registry):
        """All optional fields are stored correctly."""
        registry.register_function(
            function_path="SapModel.PropMaterial.SetMaterial",
            category="Properties",
            description="Define a material",
            signature="Function SetMaterial(ByVal Name As String, ByVal MatType As Long) As Long",
            wrapper_script="func_PropMaterial_SetMaterial",
            parameter_notes="Name=material name, MatType=eMatType enum",
            notes="MatType: 1=Steel, 2=Concrete",
        )
        entry = registry.get_function("SapModel.PropMaterial.SetMaterial")
        assert entry["category"] == "Properties"
        assert entry["signature"].startswith("Function SetMaterial")
        assert entry["wrapper_script"] == "func_PropMaterial_SetMaterial"
        assert "MatType" in entry["parameter_notes"]
        assert "Steel" in entry["notes"]


class TestMarkVerified:
    """Tests for mark_verified."""

    def test_mark_existing_verified(self, registry):
        """Marking a registered function as verified updates flags."""
        registry.register_function(
            function_path="SapModel.FrameObj.Count",
            category="Object_Model",
        )
        result = registry.mark_verified("SapModel.FrameObj.Count", "simple_beam")
        assert result["verified"] is True
        assert result["verification_count"] == 1

        entry = registry.get_function("SapModel.FrameObj.Count")
        assert entry["verified"] is True
        assert entry["first_verified"] is not None
        assert "simple_beam" in entry["used_in_scripts"]

    def test_mark_unregistered_auto_registers(self, registry):
        """Marking a non-existent function auto-registers it."""
        result = registry.mark_verified(
            "SapModel.NewFunction.DoSomething", "test_script"
        )
        assert result["verified"] is True
        assert result["verification_count"] == 1

        entry = registry.get_function("SapModel.NewFunction.DoSomething")
        assert entry["verified"] is True
        assert "test_script" in entry["used_in_scripts"]

    def test_verification_count_increments(self, registry):
        """Each call to mark_verified increments the count."""
        registry.mark_verified("SapModel.FrameObj.Count", "script_a")
        registry.mark_verified("SapModel.FrameObj.Count", "script_b")
        result = registry.mark_verified("SapModel.FrameObj.Count", "script_c")
        assert result["verification_count"] == 3

        entry = registry.get_function("SapModel.FrameObj.Count")
        assert set(entry["used_in_scripts"]) == {"script_a", "script_b", "script_c"}

    def test_duplicate_script_not_added_twice(self, registry):
        """Same script name is not duplicated in used_in_scripts."""
        registry.mark_verified("SapModel.FrameObj.Count", "same_script")
        registry.mark_verified("SapModel.FrameObj.Count", "same_script")

        entry = registry.get_function("SapModel.FrameObj.Count")
        assert entry["used_in_scripts"].count("same_script") == 1


class TestGetFunction:
    """Tests for get_function."""

    def test_get_existing(self, registry):
        """Retrieving a registered function returns full details."""
        registry.register_function(
            function_path="SapModel.Analyze.RunAnalysis",
            category="Analyze",
            description="Run the analysis",
        )
        entry = registry.get_function("SapModel.Analyze.RunAnalysis")
        assert entry["function_path"] == "SapModel.Analyze.RunAnalysis"
        assert entry["category"] == "Analyze"

    def test_get_nonexistent(self, registry):
        """Retrieving a non-existent function returns error."""
        entry = registry.get_function("SapModel.Does.NotExist")
        assert "error" in entry


class TestListFunctions:
    """Tests for list_functions."""

    @pytest.fixture(autouse=True)
    def setup_functions(self, registry):
        """Populate registry with test data."""
        registry.register_function(
            "SapModel.FrameObj.AddByCoord", "Object_Model", "Add frame by coords"
        )
        registry.mark_verified("SapModel.FrameObj.AddByCoord", "simple_beam")

        registry.register_function(
            "SapModel.FrameObj.Count", "Object_Model", "Count frames"
        )
        registry.mark_verified("SapModel.FrameObj.Count", "simple_beam")

        registry.register_function(
            "SapModel.PropMaterial.SetMaterial", "Properties", "Define material"
        )
        # Not verified

        registry.register_function(
            "SapModel.Analyze.RunAnalysis", "Analyze", "Run analysis"
        )
        registry.mark_verified("SapModel.Analyze.RunAnalysis", "simple_beam")

    def test_list_all(self, registry):
        """List all functions without filters."""
        results = registry.list_functions()
        assert len(results) == 4

    def test_list_by_category(self, registry):
        """Filter by category."""
        results = registry.list_functions(category="Object_Model")
        assert len(results) == 2
        assert all(r["category"] == "Object_Model" for r in results)

    def test_list_verified_only(self, registry):
        """Filter to verified functions only."""
        results = registry.list_functions(verified_only=True)
        assert len(results) == 3
        assert all(r["verified"] for r in results)

    def test_list_by_query(self, registry):
        """Search by keyword."""
        results = registry.list_functions(query="frame")
        assert len(results) >= 2  # AddByCoord and Count both match "frame" in path

    def test_list_combined_filters(self, registry):
        """Category + verified_only combined."""
        results = registry.list_functions(category="Properties", verified_only=True)
        assert len(results) == 0  # SetMaterial is not verified


class TestGetSummary:
    """Tests for get_summary."""

    def test_empty_summary(self, registry):
        """Empty registry returns zero counts."""
        summary = registry.get_summary()
        assert summary["total_registered"] == 0
        assert summary["total_verified"] == 0

    def test_summary_with_data(self, registry):
        """Summary reflects registered and verified counts."""
        registry.register_function("SapModel.A.B", "Cat1")
        registry.register_function("SapModel.C.D", "Cat1")
        registry.register_function("SapModel.E.F", "Cat2")
        registry.mark_verified("SapModel.A.B")
        registry.mark_verified("SapModel.E.F")

        summary = registry.get_summary()
        assert summary["total_registered"] == 3
        assert summary["total_verified"] == 2
        assert summary["categories"]["Cat1"]["registered"] == 2
        assert summary["categories"]["Cat1"]["verified"] == 1
        assert summary["categories"]["Cat2"]["registered"] == 1
        assert summary["categories"]["Cat2"]["verified"] == 1


class TestPersistence:
    """Tests for save/load lifecycle."""

    def test_data_persists_across_instances(self, tmp_path):
        """Data is preserved when creating a new registry from the same file."""
        path = tmp_path / "registry.json"

        reg1 = FunctionRegistry(registry_path=path)
        reg1.register_function("SapModel.FrameObj.Count", "Object_Model")
        reg1.mark_verified("SapModel.FrameObj.Count", "test")

        reg2 = FunctionRegistry(registry_path=path)
        entry = reg2.get_function("SapModel.FrameObj.Count")
        assert entry["verified"] is True
        assert entry["verification_count"] == 1

    def test_reload_clears_cache(self, tmp_path):
        """reload() forces re-read from disk."""
        path = tmp_path / "registry.json"
        reg = FunctionRegistry(registry_path=path)
        reg.register_function("SapModel.X.Y", "Cat")

        reg.reload()
        entry = reg.get_function("SapModel.X.Y")
        assert "error" not in entry  # still there after reload
```

##### Step 1 Verification Checklist
- [x] File `scripts/registry.json` exists and is valid JSON
- [x] File `mcp_server/function_registry.py` exists with `FunctionRegistry` class
- [x] File `mcp_server/tests/test_function_registry.py` has all tests
- [x] Run tests: `cd mcp_server && python -m pytest tests/test_function_registry.py -v`
- [x] All tests pass with no errors

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 2: Wrapper Scripts Format and Initial Wrappers

- [x] Create the wrappers directory README at `scripts/wrappers/README.md`:

```markdown
# SAP2000 Function Wrappers

Minimal, self-contained scripts that demonstrate the correct usage of a single
SAP2000 API function. Each wrapper:

- Targets **one** API function
- Sets up all prerequisites (model, material, section)
- Calls the function and asserts success
- Writes verification output to `result`

## Naming Convention

`func_{ObjectName}_{FunctionName}.py`

Examples:
- `func_FrameObj_AddByCoord.py`
- `func_PointObj_SetRestraint.py`
- `func_LoadPatterns_Add.py`

## Execution

Run any wrapper directly via the `run_sap_script` MCP tool. They are designed
to be self-contained — each one initializes a fresh model.

## Header Format

```
# ============================================================
# Wrapper: SapModel.{Object}.{Function}
# Category: {API_Category}
# Description: {What the function does}
# Verified: {YYYY-MM-DD}
# Prerequisites: {What must exist before calling}
# ============================================================
```
```

- [x] Create wrapper script `scripts/wrappers/func_FrameObj_AddByCoord.py`:

```python
# ============================================================
# Wrapper: SapModel.FrameObj.AddByCoord
# Category: Object_Model
# Description: Add a frame element defined by endpoint coordinates
# Verified: 2026-03-20
# Prerequisites: Model open, material and section defined
# ============================================================
"""
Usage: Creates a frame (beam/column) between two coordinate points.
       Returns the name assigned to the frame.

API Signature:
  SapModel.FrameObj.AddByCoord(x1, y1, z1, x2, y2, z2, Name, PropName, UserName, CSys)

ByRef Output:
  raw[0] = Name (name assigned by SAP2000)
  raw[-1] = ret_code (0=success)

Parameters:
  x1,y1,z1 : float — Coordinates of point i [L]
  x2,y2,z2 : float — Coordinates of point j [L]
  Name     : str   — Name (empty="auto-assign")
  PropName : str   — Frame section property name
  UserName : str   — User-defined name (empty=use Name)
  CSys     : str   — Coordinate system (default="Global")
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material and section ---
MATERIAL_NAME = "MAT_TEST"
ret = SapModel.PropMaterial.SetMaterial(MATERIAL_NAME, 2)  # 2=Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

SECTION_NAME = "SEC_TEST"
ret = SapModel.PropFrame.SetRectangle(SECTION_NAME, MATERIAL_NAME, 0.5, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

# --- Target function ---
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", SECTION_NAME, "")
frame_name = raw[0]
ret_code = raw[-1]
assert ret_code == 0, f"AddByCoord failed: {ret_code}"

# --- Verification ---
count = SapModel.FrameObj.Count()
assert count >= 1, f"Expected at least 1 frame, got {count}"

# --- Result ---
result["function"] = "SapModel.FrameObj.AddByCoord"
result["frame_name"] = frame_name
result["frame_count"] = count
result["status"] = "verified"
```

- [x] Create wrapper script `scripts/wrappers/func_PointObj_SetRestraint.py`:

```python
# ============================================================
# Wrapper: SapModel.PointObj.SetRestraint
# Category: Object_Model
# Description: Assign translational and rotational restraints to a joint
# Verified: 2026-03-20
# Prerequisites: Model open, at least one point object exists
# ============================================================
"""
Usage: Sets support restraints (boundary conditions) on a joint point.
       The restraint is a 6-element boolean array [Ux, Uy, Uz, Rx, Ry, Rz].

API Signature:
  SapModel.PointObj.SetRestraint(Name, Value, ItemType)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name     : str        — Name of the point object
  Value    : bool[6]    — [Ux, Uy, Uz, Rx, Ry, Rz] True=fixed, False=free
  ItemType : int        — 0=Object (default), 1=Group, 2=SelectedObjects
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Prerequisites: material, section, and a frame to get points ---
ret = SapModel.PropMaterial.SetMaterial("MAT_TEST", 1)  # 1=Steel
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropFrame.SetRectangle("SEC_TEST", "MAT_TEST", 0.3, 0.3)
assert ret == 0, f"SetRectangle failed: {ret}"

raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "SEC_TEST", "")
frame_name = raw[0]
assert raw[-1] == 0, f"AddByCoord failed: {raw[-1]}"

# Get endpoint names
raw = SapModel.FrameObj.GetPoints(frame_name, "", "")
pt_i = raw[0]
pt_j = raw[1]
assert raw[-1] == 0, f"GetPoints failed: {raw[-1]}"

# --- Target function: pin at left, roller at right ---
# Pin: all translations fixed, all rotations free
ret = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])
assert ret == 0, f"SetRestraint(pin) failed: {ret}"

# Roller: only Uy and Uz fixed
ret = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])
assert ret == 0, f"SetRestraint(roller) failed: {ret}"

# --- Verification ---
point_count = SapModel.PointObj.Count()
assert point_count >= 2, f"Expected at least 2 points, got {point_count}"

# --- Result ---
result["function"] = "SapModel.PointObj.SetRestraint"
result["point_i"] = pt_i
result["point_j"] = pt_j
result["point_count"] = point_count
result["status"] = "verified"
```

- [x] Create wrapper script `scripts/wrappers/func_LoadPatterns_Add.py`:

```python
# ============================================================
# Wrapper: SapModel.LoadPatterns.Add
# Category: Load_Patterns
# Description: Add a new load pattern to the model
# Verified: 2026-03-20
# Prerequisites: Model open
# ============================================================
"""
Usage: Creates a new load pattern with a specified name, type,
       and optional self-weight multiplier.

API Signature:
  SapModel.LoadPatterns.Add(Name, MyType, SelfWTMultiplier, AddCase)

ByRef Output:
  ret_code (0=success) — returned directly (no ByRef outputs)

Parameters:
  Name              : str   — Load pattern name
  MyType            : int   — eLoadPatternType enum:
                               1=Dead, 2=SuperDead, 3=Live, 4=ReduceLive,
                               5=Quake, 6=Wind, 7=Snow, 8=Other
  SelfWTMultiplier  : float — Self-weight multiplier (default=0)
  AddCase           : bool  — True=auto-create matching load case (default=True)
"""

# --- Minimal setup (fresh model) ---
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)  # kN_m_C
assert ret == 0, f"SetPresentUnits failed: {ret}"

# --- Target function: add multiple load patterns ---
# Dead load with self-weight multiplier = 1
ret = SapModel.LoadPatterns.Add("DEAD_CUSTOM", 1, 1)
assert ret == 0, f"Add(DEAD_CUSTOM) failed: {ret}"

# Live load (no self-weight)
ret = SapModel.LoadPatterns.Add("LIVE_CUSTOM", 3)
assert ret == 0, f"Add(LIVE_CUSTOM) failed: {ret}"

# Wind load
ret = SapModel.LoadPatterns.Add("WIND_X", 6)
assert ret == 0, f"Add(WIND_X) failed: {ret}"

# --- Verification ---
# Count load patterns (includes default "DEAD" pattern)
raw = SapModel.LoadPatterns.GetNameList(0, [])
ret_code = raw[-1]
assert ret_code == 0, f"GetNameList failed: {ret_code}"
num_patterns = raw[0]
pattern_names = list(raw[1])

assert "DEAD_CUSTOM" in pattern_names, "DEAD_CUSTOM not found in load patterns"
assert "LIVE_CUSTOM" in pattern_names, "LIVE_CUSTOM not found in load patterns"
assert "WIND_X" in pattern_names, "WIND_X not found in load patterns"

# --- Result ---
result["function"] = "SapModel.LoadPatterns.Add"
result["num_patterns"] = num_patterns
result["pattern_names"] = pattern_names
result["status"] = "verified"
```

##### Step 2 Verification Checklist
- [x] Directory `scripts/wrappers/` exists with `README.md` and 3 `.py` files
- [x] Each wrapper has the standard header comment block
- [x] Each wrapper is self-contained (initializes a fresh model)
- [x] Each wrapper writes to `result["status"] = "verified"` on success
- [x] (Optional, requires SAP2000) Execute each wrapper via `run_sap_script` and confirm `result["status"] == "verified"`

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 3: MCP Tools for the Registry

- [ ] Edit `mcp_server/server.py` to add the import for the registry. Add the following line after the existing imports (after `from doc_search import doc_index`):

```python
from function_registry import registry
```

- [ ] Add 3 new MCP tool functions to `mcp_server/server.py`. Insert them **before** the `# ── Run ──` section at the bottom of the file, after the `list_api_categories` tool:

```python
@mcp.tool()
def query_function_registry(
    function_path: str | None = None,
    category: str | None = None,
    verified_only: bool = False,
    query: str | None = None,
) -> dict:
    """Query the registry of verified SAP2000 API functions.

    Use this BEFORE generating a script to check if a function has already
    been verified and has a wrapper script available.

    Modes:
      - No arguments: returns registry summary (total registered, verified, categories)
      - function_path: returns full detail of that specific function
      - category / query / verified_only: returns filtered list of functions

    Returns: {summary} or {function detail} or {functions: [...]}
    """
    if function_path:
        return registry.get_function(function_path)

    if category or query or verified_only:
        functions = registry.list_functions(
            category=category,
            verified_only=verified_only,
            query=query,
        )
        return {"count": len(functions), "functions": functions}

    return registry.get_summary()


@mcp.tool()
def register_verified_function(
    function_path: str,
    category: str,
    description: str = "",
    wrapper_script: str = "",
    parameter_notes: str = "",
    notes: str = "",
) -> dict:
    """Register or update a verified SAP2000 API function in the registry.

    Call this after successfully running a script that uses a new API function.
    If wrapper_script is provided, it links the function to its wrapper in
    scripts/wrappers/.

    function_path: Dot-path like "SapModel.FrameObj.AddByCoord"
    category: API category (e.g. "Object_Model", "Properties", "Analyze")
    description: What the function does
    wrapper_script: Name of wrapper script (without .py) in scripts/wrappers/
    parameter_notes: Brief parameter documentation
    notes: Extra notes (e.g. ByRef output layout)

    Returns: {registered, function_path, is_new}
    """
    result = registry.register_function(
        function_path=function_path,
        category=category,
        description=description,
        wrapper_script=wrapper_script,
        parameter_notes=parameter_notes,
        notes=notes,
    )
    # Also mark as verified since this tool is for verified functions
    registry.mark_verified(function_path)
    return result


@mcp.tool()
def list_registry_categories() -> list[dict]:
    """List API categories with counts of registered vs verified functions.

    Use this to see coverage of the function registry — which categories
    have been explored and which still need work.

    Returns: [{category, registered, verified}]
    """
    summary = registry.get_summary()
    categories = summary.get("categories", {})

    return [
        {
            "category": cat,
            "registered": counts["registered"],
            "verified": counts["verified"],
        }
        for cat, counts in sorted(categories.items())
    ]
```

- [ ] Update `mcp_server/tests/test_bridge.py` to add tests for the new MCP tools. Append the following test class at the end of the file:

```python
class TestFunctionRegistryTools:
    """Tests for the registry MCP tools (no SAP2000 needed)."""

    @pytest.fixture(autouse=True)
    def setup_registry(self, tmp_path, monkeypatch):
        """Point the registry at a temporary file."""
        import function_registry
        test_path = tmp_path / "registry.json"
        monkeypatch.setattr(function_registry, "REGISTRY_PATH", test_path)
        # Reset the singleton to use the new path
        function_registry.registry = FunctionRegistry(registry_path=test_path)

    def test_query_empty_summary(self):
        """query_function_registry with no args returns empty summary."""
        from function_registry import registry
        summary = registry.get_summary()
        assert summary["total_registered"] == 0

    def test_register_and_query(self):
        """register_verified_function then query it back."""
        from function_registry import registry
        registry.register_function(
            "SapModel.FrameObj.AddByCoord",
            "Object_Model",
            "Add frame by coords",
        )
        registry.mark_verified("SapModel.FrameObj.AddByCoord", "test")
        entry = registry.get_function("SapModel.FrameObj.AddByCoord")
        assert entry["verified"] is True

    def test_list_registry_categories(self):
        """list_registry_categories returns category counts."""
        from function_registry import registry
        registry.register_function("SapModel.A.B", "Cat1")
        registry.register_function("SapModel.C.D", "Cat2")
        registry.mark_verified("SapModel.A.B")
        summary = registry.get_summary()
        assert summary["categories"]["Cat1"]["verified"] == 1
        assert summary["categories"]["Cat2"]["verified"] == 0
```

Also add the missing import at the top of test_bridge.py (after the existing imports):

```python
from function_registry import FunctionRegistry
```

##### Step 3 Verification Checklist
- [ ] `mcp_server/server.py` imports `registry` from `function_registry`
- [ ] Three new tools exist: `query_function_registry`, `register_verified_function`, `list_registry_categories`
- [ ] New test class `TestFunctionRegistryTools` exists in test_bridge.py
- [ ] Run tests: `cd mcp_server && python -m pytest tests/test_bridge.py -v -k "TestFunctionRegistryTools or TestDocSearch or TestScriptLibrary"`
- [ ] All tests pass with no errors
- [ ] No build/import errors in `server.py`

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 4: Auto-Registration on Successful Script Execution

- [ ] Edit `mcp_server/sap_executor.py` to add the import for the registry. Add after the existing `from script_library import save_script` line:

```python
from function_registry import registry as function_registry
```

- [ ] Add the API function extraction helper to `mcp_server/sap_executor.py`. Insert this function **before** the `run_script` function definition:

```python
# Regex to detect SAP2000 API calls: SapModel.Something.Something(...) or SapObject.Something(...)
_API_CALL_PATTERN = re.compile(
    r"\b((?:SapModel|SapObject)(?:\.\w+)+)\s*\(",
)


def _extract_api_functions(script: str) -> list[str]:
    """
    Extract SAP2000 API function paths from a script's source code.

    Finds all occurrences of SapModel.X.Y(...) and SapObject.X.Y(...)
    and returns unique function paths.

    Example:
        "SapModel.FrameObj.AddByCoord(0,0,0,...)"
        → ["SapModel.FrameObj.AddByCoord"]
    """
    matches = _API_CALL_PATTERN.findall(script)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for match in matches:
        if match not in seen:
            seen.add(match)
            unique.append(match)
    return unique
```

- [ ] Add the `import re` to the imports at the top of `sap_executor.py` (it is not currently imported). Add it after the `import logging` line:

```python
import re
```

- [ ] Modify the `run_script` function in `mcp_server/sap_executor.py` to auto-register functions on success. Replace the section at the end of `run_script` that handles saving (the `# Save to library on success if name provided` block) with the following expanded version:

Find this block near the end of `run_script`:
```python
    # Save to library on success if name provided
    if save_as:
        save_result = save_script(
            name=save_as,
            script=script,
            description=description,
            result=sandbox_globals.get("result", {}),
        )
        response["saved_path"] = save_result.get("path")

    return response
```

Replace it with:
```python
    # Save to library on success if name provided
    if save_as:
        save_result = save_script(
            name=save_as,
            script=script,
            description=description,
            result=sandbox_globals.get("result", {}),
        )
        response["saved_path"] = save_result.get("path")

    # Auto-register API functions used in this successful script
    try:
        api_functions = _extract_api_functions(script)
        script_label = save_as or ""
        for func_path in api_functions:
            function_registry.mark_verified(func_path, script_label)
        if api_functions:
            response["registered_functions"] = api_functions
            logger.info(
                "Auto-registered %d API functions from script: %s",
                len(api_functions),
                api_functions,
            )
    except Exception as exc:
        logger.warning("Auto-registration failed (non-fatal): %s", exc)

    return response
```

- [ ] Add unit tests for the extraction function. Append this class to `mcp_server/tests/test_bridge.py`:

```python
class TestAutoRegistration:
    """Tests for auto-registration of API functions from scripts."""

    def test_extract_api_functions(self):
        """_extract_api_functions finds SapModel and SapObject calls."""
        from sap_executor import _extract_api_functions

        script = """
SapModel.InitializeNewModel()
SapModel.File.NewBlank()
ret = SapModel.SetPresentUnits(6)
ret = SapModel.PropMaterial.SetMaterial("CONC", 2)
raw = SapModel.FrameObj.AddByCoord(0, 0, 0, 5, 0, 0, "", "R1", "")
count = SapModel.FrameObj.Count()
# Duplicate call should not produce duplicate entry
raw2 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, "", "R1", "")
"""
        funcs = _extract_api_functions(script)
        assert "SapModel.InitializeNewModel" in funcs
        assert "SapModel.File.NewBlank" in funcs
        assert "SapModel.SetPresentUnits" in funcs
        assert "SapModel.PropMaterial.SetMaterial" in funcs
        assert "SapModel.FrameObj.AddByCoord" in funcs
        assert "SapModel.FrameObj.Count" in funcs
        # Should be deduplicated
        assert funcs.count("SapModel.FrameObj.AddByCoord") == 1

    def test_extract_no_matches(self):
        """_extract_api_functions returns empty for non-SAP code."""
        from sap_executor import _extract_api_functions

        script = "x = 1\ny = x + 2\nresult['value'] = y"
        funcs = _extract_api_functions(script)
        assert funcs == []

    def test_extract_sap_object_calls(self):
        """_extract_api_functions finds SapObject calls too."""
        from sap_executor import _extract_api_functions

        script = "SapObject.ApplicationExit(False)"
        funcs = _extract_api_functions(script)
        assert "SapObject.ApplicationExit" in funcs
```

##### Step 4 Verification Checklist
- [ ] `sap_executor.py` imports `re` and `function_registry`
- [ ] `_extract_api_functions()` function exists and returns unique API function paths
- [ ] `run_script()` calls `function_registry.mark_verified()` for each detected function on success
- [ ] `run_script()` adds `registered_functions` key to the response on success
- [ ] Auto-registration failure does not break script execution (wrapped in try/except)
- [ ] Run tests: `cd mcp_server && python -m pytest tests/test_bridge.py -v -k "TestAutoRegistration"`
- [ ] All tests pass with no errors

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.

---

#### Step 5: Update SKILL.md, Copilot Instructions, and Documentation

- [ ] Edit `.github/skills/sap2000-api/SKILL.md` to update the **Mandatory Workflow** section. Replace the existing 7-step workflow with this expanded version:

Find this block:
```markdown
## Mandatory Workflow

**ALWAYS follow this sequence for every SAP2000 task:**

1. **Check connection** — Call `get_model_info` to verify SAP2000 is connected.
   If not connected, call `connect_sap2000` first.
2. **Search for existing scripts** — Call `list_scripts` with a relevant query.
   If a matching script exists, use `load_script` to load it as a starting point.
3. **Search API docs** — Call `search_api_docs` to find the correct functions,
   parameter order, and return value conventions before writing any code.
4. **Generate the script** — Write a complete Python script following the
   patterns described below.
5. **Execute** — Call `run_sap_script` with the script.
6. **Verify** — Read the returned `result`, `stdout`, and `return_value`.
   If `success` is `false`, analyze the error, fix the script, and re-execute.
7. **Save** — When the script succeeds, re-run with `save_as` to store it
   in the script library for future reuse.
```

Replace with:
```markdown
## Mandatory Workflow

**ALWAYS follow this sequence for every SAP2000 task:**

1. **Check connection** — Call `get_model_info` to verify SAP2000 is connected.
   If not connected, call `connect_sap2000` first.
2. **Check function registry** — Call `query_function_registry` with the function
   name or a keyword query to see if the needed functions have already been
   verified. If a wrapper script exists, use `load_script` to load it as a
   reference for correct usage patterns.
3. **Search for existing scripts** — Call `list_scripts` with a relevant query.
   If a matching full script exists, use `load_script` to load it as a starting point.
4. **Search API docs** — Call `search_api_docs` to find the correct functions,
   parameter order, and return value conventions before writing any code.
5. **Generate the script** — Write a complete Python script following the
   patterns described below. Use verified wrapper scripts as building blocks
   when available.
6. **Execute** — Call `run_sap_script` with the script. On success, any new
   API functions used are automatically registered in the function registry.
7. **Verify** — Read the returned `result`, `stdout`, and `return_value`.
   If `success` is `false`, analyze the error, fix the script, and re-execute.
8. **Save** — When the script succeeds, re-run with `save_as` to store it
   in the script library for future reuse.
9. **Register new functions** — For any new API functions not yet in the
   registry, call `register_verified_function` to add full metadata
   (category, description, parameter notes). Auto-registration captures
   the function path, but manual registration adds richer documentation.
```

- [ ] Add a new section to `.github/skills/sap2000-api/SKILL.md` about the function registry. Insert this block **after** the `## Script Patterns` section and **before** the `## SAP2000 API Conventions` section:

```markdown
## Function Registry

The function registry (`scripts/registry.json`) tracks which API functions
have been successfully tested. Use it to avoid re-discovering function
signatures and ByRef conventions from scratch.

### Querying the Registry

```python
# Check if a specific function has been verified:
query_function_registry(function_path="SapModel.FrameObj.AddByCoord")
# → {function_path, category, description, verified, wrapper_script, ...}

# Search by keyword:
query_function_registry(query="frame")
# → {count, functions: [{function_path, category, verified, ...}, ...]}

# List verified functions only:
query_function_registry(verified_only=True)

# Get registry summary:
query_function_registry()
# → {total_registered, total_verified, categories: {...}}
```

### Wrapper Scripts

Verified functions have wrapper scripts in `scripts/wrappers/` that demonstrate
correct usage. Each wrapper:
- Targets a single API function
- Is self-contained (initializes a fresh model)
- Documents the ByRef output layout
- Asserts success and writes to `result`

To use a wrapper as reference:
```
load_script("func_FrameObj_AddByCoord")
```

### Auto-Registration

When a script executes successfully via `run_sap_script`, all SAP2000 API
functions called in the script are automatically detected and registered
as verified in the registry. The response includes a `registered_functions`
list showing what was captured.
```

- [ ] Update `.github/copilot-instructions.md` to add the 3 new tools to the table. Replace the existing tool table:

Find:
```markdown
| Tool | Purpose |
|------|---------|
| `connect_sap2000` | Connect to a local SAP2000 instance |
| `disconnect_sap2000` | Disconnect and release COM resources |
| `get_model_info` | Check connection status and model summary |
| `execute_sap_function` | Execute a single API function by dot-path |
| `run_sap_script` | Execute a full Python script in sandbox |
| `list_scripts` | Browse saved scripts in the library |
| `load_script` | Load a saved script for modification |
| `search_api_docs` | Search API documentation for functions |
| `list_api_categories` | List API documentation categories |
```

Replace with:
```markdown
| Tool | Purpose |
|------|---------|
| `connect_sap2000` | Connect to a local SAP2000 instance |
| `disconnect_sap2000` | Disconnect and release COM resources |
| `get_model_info` | Check connection status and model summary |
| `execute_sap_function` | Execute a single API function by dot-path |
| `run_sap_script` | Execute a full Python script in sandbox |
| `list_scripts` | Browse saved scripts in the library |
| `load_script` | Load a saved script for modification |
| `search_api_docs` | Search API documentation for functions |
| `list_api_categories` | List API documentation categories |
| `query_function_registry` | Query verified functions by path, category, or keyword |
| `register_verified_function` | Register or update a verified API function |
| `list_registry_categories` | List categories with registered/verified counts |
```

- [ ] Update `scripts/README.md` to mention wrappers. Replace the entire file with:

```markdown
# SAP2000 Script Library

Auto-managed collection of verified SAP2000 API scripts.

Scripts are saved here automatically when the agent runs them successfully with `save_as`.
Use `list_scripts` to browse and `load_script` to reload any script.

## Usage

Scripts are designed to be executed via the `run_sap_script` MCP tool.
They expect `SapModel`, `SapObject`, and `result` to be pre-injected.

## Wrappers

The `wrappers/` subdirectory contains minimal, self-contained scripts that
demonstrate the correct usage of individual API functions. See
[wrappers/README.md](wrappers/README.md) for details.

## Registry

The file `registry.json` tracks all verified API functions across all scripts.
Query it via the `query_function_registry` MCP tool, or inspect the JSON directly.
```

##### Step 5 Verification Checklist
- [ ] SKILL.md workflow has 9 steps (added steps 2 and 9)
- [ ] SKILL.md has a new "Function Registry" section with query examples, wrapper docs, and auto-registration info
- [ ] `copilot-instructions.md` tool table has 12 rows (3 new tools)
- [ ] `scripts/README.md` mentions wrappers and registry
- [ ] No markdown formatting errors in any edited file
- [ ] Run all tests to verify nothing is broken: `cd mcp_server && python -m pytest tests/ -v`
- [ ] All tests pass with no errors

#### Step 5 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
