"""
Integration tests for the SAP2000 MCP Server.

These tests require a running SAP2000 instance or the ability to launch one.
They are NOT meant to run in CI — only locally on a Windows machine with
SAP2000 installed.

Run with: python -m pytest mcp_server/tests/test_bridge.py -v
"""

import sys
from pathlib import Path

# Add mcp_server to path so imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

# comtypes is now lazy-loaded in sap_bridge so these modules can be imported
# on Linux/macOS for pure-Python unit tests.

from function_registry import FunctionRegistry


class TestSapBridgeUnit:
    """Unit tests that don't require SAP2000."""

    def test_bridge_initial_state(self):
        """Bridge starts disconnected."""
        from sap_bridge import SapBridge
        b = SapBridge()
        assert b.is_connected is False
        assert b.sap_object is None
        assert b.sap_model is None

    def test_get_model_info_not_connected(self):
        """get_model_info returns error when not connected."""
        from sap_bridge import SapBridge
        b = SapBridge()
        info = b.get_model_info()
        assert info["connected"] is False
        assert "error" in info

    def test_disconnect_when_not_connected(self):
        """disconnect is safe to call when not connected."""
        from sap_bridge import SapBridge
        b = SapBridge()
        result = b.disconnect()
        assert result["disconnected"] is True


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="SAP2000 COM only available on Windows",
)
class TestSapBridgeIntegration:
    """Integration tests that require SAP2000 installed."""

    @pytest.fixture
    def bridge_connected(self):
        """Connect to SAP2000 and yield the bridge, then disconnect."""
        b = SapBridge()
        result = b.connect()
        if not result.get("connected"):
            pytest.skip(f"Could not connect to SAP2000: {result.get('error')}")
        yield b
        b.disconnect(save_model=False)

    def test_connect_and_get_info(self, bridge_connected):
        """Connect and verify model info is returned."""
        info = bridge_connected.get_model_info()
        assert info["connected"] is True
        assert "version" in info

    def test_initialize_new_model(self, bridge_connected):
        """Initialize a new blank model."""
        ret = bridge_connected.sap_model.InitializeNewModel()
        assert ret == 0
        ret = bridge_connected.sap_model.File.NewBlank()
        assert ret == 0

    def test_create_frame_and_count(self, bridge_connected):
        """Create a frame and verify count increases."""
        model = bridge_connected.sap_model
        ret = model.InitializeNewModel()
        ret = model.File.NewBlank()

        ret = model.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, "", "Default", "1")
        count = model.FrameObj.Count()
        actual_count = count if isinstance(count, int) else count[0]
        assert actual_count >= 1


class TestSapExecutorUnit:
    """Unit tests for the function executor (no SAP2000 needed)."""

    def test_execute_not_connected(self):
        """execute_function returns error when not connected."""
        from sap_executor import execute_function
        result = execute_function("SapModel.FrameObj.Count", [])
        assert result["success"] is False
        assert "Not connected" in result["error"]

    def test_run_script_not_connected(self):
        """run_script returns error when not connected."""
        from sap_executor import run_script
        result = run_script("x = 1")
        assert result["success"] is False
        assert "Not connected" in result["error"]


class TestDocSearch:
    """Tests for the API documentation search."""

    def test_search_frame(self):
        """Search for 'frame' finds relevant functions."""
        from doc_search import doc_index
        results = doc_index.search("AddByCoord frame")
        assert len(results) > 0
        names = [r["function_name"] for r in results]
        assert any("AddByCoord" in n for n in names)

    def test_search_analysis(self):
        """Search for 'run analysis' returns RunAnalysis."""
        from doc_search import doc_index
        results = doc_index.search("run analysis")
        assert len(results) > 0
        names = [r["function_name"] for r in results]
        assert any("RunAnalysis" in n for n in names)

    def test_list_categories(self):
        """list_categories returns non-empty list."""
        from doc_search import doc_index
        cats = doc_index.list_categories()
        assert len(cats) > 0
        assert any("File" in c["category"] for c in cats)

    def test_search_with_category_filter(self):
        """Search with category filter narrows results."""
        from doc_search import doc_index
        all_results = doc_index.search("new")
        filtered = doc_index.search("new", category="File")
        assert len(filtered) <= len(all_results)


class TestScriptLibrary:
    """Tests for the script library (filesystem-based, no SAP2000 needed)."""

    def test_list_scripts_empty(self, tmp_path, monkeypatch):
        """list_scripts returns empty list for empty directory."""
        import script_library
        monkeypatch.setattr(script_library, "SCRIPTS_DIR", tmp_path)
        results = script_library.list_scripts()
        assert results == []

    def test_save_and_load_script(self, tmp_path, monkeypatch):
        """Save a script and load it back."""
        import script_library
        monkeypatch.setattr(script_library, "SCRIPTS_DIR", tmp_path)

        save_result = script_library.save_script(
            name="test_script",
            script="result['x'] = 42",
            description="A test script",
            result={"x": 42},
            tags=["test"],
        )
        assert save_result["saved"] is True

        loaded = script_library.load_script("test_script")
        assert "error" not in loaded
        assert loaded["name"] == "test_script"
        assert "result['x'] = 42" in loaded["script_code"]

    def test_list_scripts_with_query(self, tmp_path, monkeypatch):
        """list_scripts filters by query."""
        import script_library
        monkeypatch.setattr(script_library, "SCRIPTS_DIR", tmp_path)

        script_library.save_script("alpha_beam", "x=1", description="Create a beam")
        script_library.save_script("beta_column", "x=2", description="Create a column")

        results = script_library.list_scripts(query="beam")
        assert len(results) == 1
        assert results[0]["name"] == "alpha_beam"

    def test_load_nonexistent(self, tmp_path, monkeypatch):
        """load_script returns error for missing script."""
        import script_library
        monkeypatch.setattr(script_library, "SCRIPTS_DIR", tmp_path)

        loaded = script_library.load_script("nonexistent")
        assert "error" in loaded


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
