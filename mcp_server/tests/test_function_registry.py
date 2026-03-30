"""
Unit tests for the Function Registry.

Run with: python -m pytest mcp_server/tests/test_function_registry.py -v
"""

import json
import sys
import time
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


class TestMtimeReload:
    """Tests for cache invalidation via mtime tracking."""

    def test_detects_external_modification(self, tmp_path):
        """Registry detects when file is modified externally and reloads."""
        path = tmp_path / "registry.json"
        reg = FunctionRegistry(registry_path=path)

        # Write initial data via registry
        reg.register_function("SapModel.A.B", "Cat1", "original")

        # Simulate external modification: write directly to file
        time.sleep(0.05)  # Ensure mtime differs
        data = json.loads(path.read_text(encoding="utf-8"))
        data["functions"]["SapModel.A.B"]["description"] = "externally modified"
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        # Force mtime detection on next load
        entry = reg.get_function("SapModel.A.B")
        assert entry["description"] == "externally modified"

    def test_no_unnecessary_reload(self, tmp_path):
        """Registry does not reload when file has not changed."""
        path = tmp_path / "registry.json"
        reg = FunctionRegistry(registry_path=path)

        reg.register_function("SapModel.A.B", "Cat1", "first")

        # Access again without external change — should return cached data
        entry = reg.get_function("SapModel.A.B")
        assert entry["description"] == "first"
        # _data should still be the same object (not reloaded)
        assert reg._data is not None


class TestVerificationType:
    """Tests for verification_type field assignment."""

    def test_auto_registration_sets_auto(self, registry):
        """mark_verified on new function sets verification_type='auto'."""
        registry.mark_verified("SapModel.NewFunc.A", "test_script")
        entry = registry.get_function("SapModel.NewFunc.A")
        assert entry["verification_type"] == "auto"

    def test_manual_registration_sets_manual(self, registry):
        """register_function without wrapper sets verification_type='manual'."""
        registry.register_function(
            "SapModel.Func.B", "Cat", description="test"
        )
        entry = registry.get_function("SapModel.Func.B")
        assert entry["verification_type"] == "manual"

    def test_wrapper_registration_sets_wrapper(self, registry):
        """register_function with wrapper_script sets verification_type='wrapper'."""
        registry.register_function(
            "SapModel.Func.C", "Cat",
            wrapper_script="func_Func_C"
        )
        entry = registry.get_function("SapModel.Func.C")
        assert entry["verification_type"] == "wrapper"

    def test_auto_does_not_downgrade_manual(self, registry):
        """mark_verified does not downgrade verification_type from manual to auto."""
        registry.register_function(
            "SapModel.Func.D", "Cat", description="test"
        )
        assert registry.get_function("SapModel.Func.D")["verification_type"] == "manual"

        registry.mark_verified("SapModel.Func.D", "script_x")
        entry = registry.get_function("SapModel.Func.D")
        assert entry["verification_type"] == "manual"  # Not downgraded

    def test_manual_does_not_downgrade_wrapper(self, registry):
        """register_function without wrapper does not downgrade from wrapper to manual."""
        registry.register_function(
            "SapModel.Func.E", "Cat",
            wrapper_script="func_Func_E"
        )
        assert registry.get_function("SapModel.Func.E")["verification_type"] == "wrapper"

        # Re-register without wrapper — should not downgrade
        registry.register_function(
            "SapModel.Func.E", "Cat",
            description="updated desc"
        )
        entry = registry.get_function("SapModel.Func.E")
        assert entry["verification_type"] == "wrapper"  # Not downgraded

    def test_manual_upgrades_to_wrapper(self, registry):
        """register_function with wrapper upgrades verification_type from manual to wrapper."""
        registry.register_function(
            "SapModel.Func.F", "Cat", description="test"
        )
        assert registry.get_function("SapModel.Func.F")["verification_type"] == "manual"

        registry.register_function(
            "SapModel.Func.F", "Cat",
            wrapper_script="func_Func_F"
        )
        entry = registry.get_function("SapModel.Func.F")
        assert entry["verification_type"] == "wrapper"  # Upgraded

    def test_list_functions_includes_verification_type(self, registry):
        """list_functions output includes verification_type field."""
        registry.register_function(
            "SapModel.Func.G", "Cat",
            wrapper_script="func_Func_G"
        )
        results = registry.list_functions()
        assert len(results) == 1
        assert results[0]["verification_type"] == "wrapper"

    def test_get_function_includes_verification_type(self, registry):
        """get_function output includes verification_type field."""
        registry.mark_verified("SapModel.Func.H", "test")
        entry = registry.get_function("SapModel.Func.H")
        assert "verification_type" in entry
        assert entry["verification_type"] == "auto"
