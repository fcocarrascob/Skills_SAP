# Step 8: End-to-End Workflow Test

## Goal
Create example scripts and integration tests that validate the complete workflow: connection → model creation → load assignment → analysis → result extraction → comparison with reference values. These examples also populate the initial script library.

## Prerequisites
Steps 1–7 must be committed. The full system (MCP server, SKILL.md, VS Code config) must be in place.

### Step-by-Step Instructions

#### Step 8.1: Create the examples directory
- [x] Create the `examples/` directory in the workspace root.

#### Step 8.2: Create the Example 1-001 verification script
- [x] Copy and paste code below into `examples/example_1001_verification.py`:

```python
"""
SAP2000 Verification Example 1-001

Port of the official SAP2000 Example 1-001 verification problem.
Creates a model from scratch, runs analysis, extracts results, and
compares with hand-calculated values.

Run via: run_sap_script (this script expects SapModel, SapObject, result pre-injected)
"""

# ── Step 1: Initialize model ──────────────────────────────────────────

ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"

ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

# ── Step 2: Define material ───────────────────────────────────────────

ret = SapModel.PropMaterial.SetMaterial("CONC", 2)  # 2 = Concrete
assert ret == 0, f"SetMaterial failed: {ret}"

ret = SapModel.PropMaterial.SetMPIsotropic("CONC", 3600, 0.2, 0.0000055)
assert ret == 0, f"SetMPIsotropic failed: {ret}"

# ── Step 3: Define frame section ──────────────────────────────────────

ret = SapModel.PropFrame.SetRectangle("R1", "CONC", 12, 12)
assert ret == 0, f"SetRectangle failed: {ret}"

# Set section modifiers: Area=1000, AS2=0, AS3=0, rest=1
ModValue = [1000, 0, 0, 1, 1, 1, 1, 1]
ret = SapModel.PropFrame.SetModifiers("R1", ModValue)
assert ret == 0, f"SetModifiers failed: {ret}"

# ── Step 4: Switch to kip-ft units ────────────────────────────────────

ret = SapModel.SetPresentUnits(4)  # kip_ft_F
assert ret == 0, f"SetPresentUnits failed: {ret}"

# ── Step 5: Create geometry ───────────────────────────────────────────

# Frame 1: Column (0,0,0) → (0,0,10)
ret1 = SapModel.FrameObj.AddByCoord(0, 0, 0, 0, 0, 10, "", "R1", "1")
FrameName0 = ret1[1] if isinstance(ret1, tuple) else ""

# Frame 2: Inclined beam (0,0,10) → (8,0,16)
ret2 = SapModel.FrameObj.AddByCoord(0, 0, 10, 8, 0, 16, "", "R1", "2")
FrameName1 = ret2[1] if isinstance(ret2, tuple) else ""

# Frame 3: Cantilever (-4,0,10) → (0,0,10)
ret3 = SapModel.FrameObj.AddByCoord(-4, 0, 10, 0, 0, 10, "", "R1", "3")
FrameName2 = ret3[1] if isinstance(ret3, tuple) else ""

# ── Step 6: Set restraints ────────────────────────────────────────────

# Base of column: fixed (Ux, Uy, Uz, Rx free Ry, Rz)
ret = SapModel.FrameObj.GetPoints(FrameName0, "", "")
BasePt = ret[1]
Restraint_base = [True, True, True, True, False, False]
ret = SapModel.PointObj.SetRestraint(BasePt, Restraint_base)
assert ret == 0, f"SetRestraint(base) failed: {ret}"

# Top of inclined beam: roller (Ux, Uy)
ret = SapModel.FrameObj.GetPoints(FrameName1, "", "")
TopPt = ret[2]
Restraint_top = [True, True, False, False, False, False]
ret = SapModel.PointObj.SetRestraint(TopPt, Restraint_top)
assert ret == 0, f"SetRestraint(top) failed: {ret}"

# ── Step 7: Refresh view ──────────────────────────────────────────────

ret = SapModel.View.RefreshView(0, False)

# ── Step 8: Add load patterns ─────────────────────────────────────────

ret = SapModel.LoadPatterns.Add("1", 8, 1)   # type=8 (Other), selfweight=1
ret = SapModel.LoadPatterns.Add("2", 8)
ret = SapModel.LoadPatterns.Add("3", 8)
ret = SapModel.LoadPatterns.Add("4", 8)
ret = SapModel.LoadPatterns.Add("5", 8)
ret = SapModel.LoadPatterns.Add("6", 8)
ret = SapModel.LoadPatterns.Add("7", 8)

# ── Step 9: Assign loads ──────────────────────────────────────────────

# Load pattern 2: point load + distributed load on cantilever
ret = SapModel.FrameObj.GetPoints(FrameName2, "", "")
CantPt_i = ret[1]
PointLoadValue_2 = [0, 0, -10, 0, 0, 0]
ret = SapModel.PointObj.SetLoadForce(CantPt_i, "2", PointLoadValue_2)
ret = SapModel.FrameObj.SetLoadDistributed(FrameName2, "2", 1, 10, 0, 1, 1.8, 1.8)

# Load pattern 3: point load at end of inclined beam
ret = SapModel.FrameObj.GetPoints(FrameName2, "", "")
CantPt_j = ret[2]  # This is the junction point
PointLoadValue_3 = [0, 0, -17.2, 0, -54.4, 0]
ret = SapModel.PointObj.SetLoadForce(CantPt_j, "3", PointLoadValue_3)

# Load pattern 4: distributed load on inclined beam
ret = SapModel.FrameObj.SetLoadDistributed(FrameName1, "4", 1, 11, 0, 1, 2, 2)

# Load pattern 5: local distributed loads
ret = SapModel.FrameObj.SetLoadDistributed(FrameName0, "5", 1, 2, 0, 1, 2, 2, "Local")
ret = SapModel.FrameObj.SetLoadDistributed(FrameName1, "5", 1, 2, 0, 1, -2, -2, "Local")

# Load pattern 6: trapezoidal local loads
ret = SapModel.FrameObj.SetLoadDistributed(
    FrameName0, "6", 1, 2, 0, 1, 0.9984, 0.3744, "Local"
)
ret = SapModel.FrameObj.SetLoadDistributed(
    FrameName1, "6", 1, 2, 0, 1, -0.3744, 0, "Local"
)

# Load pattern 7: point load at midspan of inclined beam
ret = SapModel.FrameObj.SetLoadPoint(FrameName1, "7", 1, 2, 0.5, -15, "Local")

# ── Step 10: Switch to kip-in and save ────────────────────────────────

ret = SapModel.SetPresentUnits(3)  # kip_in_F

# ── Step 11: Run analysis ─────────────────────────────────────────────

ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# ── Step 12: Extract results ──────────────────────────────────────────

# Get endpoint of inclined beam for vertical displacement results
ret = SapModel.FrameObj.GetPoints(FrameName1, "", "")
ResultPt_beam = ret[2]

# Get I-end of column for horizontal displacement results
ret = SapModel.FrameObj.GetPoints(FrameName0, "", "")
ResultPt_col = ret[1]

SapResult = []
for i in range(7):
    ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
    ret = SapModel.Results.Setup.SetCaseSelectedForOutput(str(i + 1))

    if i <= 3:
        # Vertical displacement at beam end
        ret = SapModel.Results.JointDispl(
            ResultPt_beam, 0,
            0, [], [], [], [], [], [], [], [], [], []
        )
        if ret[0] == 0 and len(ret[9]) > 0:
            SapResult.append(ret[9][0])  # U3
        else:
            SapResult.append(None)
    else:
        # Horizontal displacement at column base
        ret = SapModel.Results.JointDispl(
            ResultPt_col, 0,
            0, [], [], [], [], [], [], [], [], [], []
        )
        if ret[0] == 0 and len(ret[7]) > 0:
            SapResult.append(ret[7][0])  # U1
        else:
            SapResult.append(None)

# ── Step 13: Compare with reference values ────────────────────────────

IndResult = [
    -0.02639,   # LC1: vertical displacement
     0.06296,   # LC2
     0.06296,   # LC3
    -0.02639,   # LC4
     0.06296,   # LC5
     0.06296,   # LC6
     0.06296,   # LC7
]

result["sap_values"] = SapResult
result["reference_values"] = IndResult
result["load_cases"] = list(range(1, 8))

# Calculate percent difference
percent_diff = []
for sap_val, ref_val in zip(SapResult, IndResult):
    if sap_val is not None and ref_val != 0:
        diff = (sap_val / ref_val) - 1
        percent_diff.append(round(diff * 100, 2))
    else:
        percent_diff.append(None)

result["percent_diff"] = percent_diff
result["all_pass"] = all(
    d is not None and abs(d) < 1.0  # within 1%
    for d in percent_diff
)

print("Example 1-001 Verification Results:")
print(f"{'LC':<4} {'SAP2000':<12} {'Reference':<12} {'%Diff':<8}")
for i in range(7):
    sap_str = f"{SapResult[i]:.5f}" if SapResult[i] is not None else "N/A"
    ref_str = f"{IndResult[i]:.5f}"
    diff_str = f"{percent_diff[i]:.2f}%" if percent_diff[i] is not None else "N/A"
    print(f"{i+1:<4} {sap_str:<12} {ref_str:<12} {diff_str:<8}")

print(f"\nAll within 1%: {result['all_pass']}")
```

#### Step 8.3: Create a simple beam example
- [x] Copy and paste code below into `examples/simple_beam.py`:

```python
"""
Simple Beam Example

Creates a simply-supported beam with a uniform distributed load,
runs analysis, and extracts the midpoint displacement.

Run via: run_sap_script (expects SapModel, SapObject, result pre-injected)
"""

# ── Initialize ────────────────────────────────────────────────────────

ret = SapModel.InitializeNewModel()
ret = SapModel.File.NewBlank()

# ── Units: kN, m, C ──────────────────────────────────────────────────

ret = SapModel.SetPresentUnits(6)  # kN_m_C

# ── Material: Steel ───────────────────────────────────────────────────

ret = SapModel.PropMaterial.SetMaterial("STEEL", 1)  # 1 = Steel
ret = SapModel.PropMaterial.SetMPIsotropic("STEEL", 200000000, 0.3, 0.0000117)

# ── Section: W310x60 approximated as rectangle ───────────────────────

ret = SapModel.PropFrame.SetRectangle("BEAM_SECT", "STEEL", 0.302, 0.203)

# ── Create beam: 6m span along X ─────────────────────────────────────

ret = SapModel.FrameObj.AddByCoord(0, 0, 0, 6, 0, 0, "", "BEAM_SECT", "1")
beam_name = ret[1] if isinstance(ret, tuple) else "1"

# ── Supports ──────────────────────────────────────────────────────────

# Get end points
ret = SapModel.FrameObj.GetPoints(beam_name, "", "")
pt_i = ret[1]
pt_j = ret[2]

# Pin at left end (all translations fixed)
ret = SapModel.PointObj.SetRestraint(pt_i, [True, True, True, False, False, False])

# Roller at right end (Uy and Uz fixed)
ret = SapModel.PointObj.SetRestraint(pt_j, [False, True, True, False, False, False])

# ── Load ──────────────────────────────────────────────────────────────

# Add a live load pattern
ret = SapModel.LoadPatterns.Add("LIVE", 3)  # 3 = Live

# Uniform distributed load: 10 kN/m downward (gravity projected)
ret = SapModel.FrameObj.SetLoadDistributed(beam_name, "LIVE", 1, 10, 0, 1, 10, 10)

# ── Analysis ──────────────────────────────────────────────────────────

ret = SapModel.Analyze.RunAnalysis()
assert ret == 0, f"RunAnalysis failed: {ret}"

# ── Results ───────────────────────────────────────────────────────────

ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
ret = SapModel.Results.Setup.SetCaseSelectedForOutput("LIVE")

# Get displacement at both joints to check
for pt_name, label in [(pt_i, "left"), (pt_j, "right")]:
    ret = SapModel.Results.JointDispl(
        pt_name, 0, 0, [], [], [], [], [], [], [], [], [], []
    )
    if ret[0] == 0 and len(ret[9]) > 0:
        result[f"U3_{label}"] = ret[9][0]

result["beam_name"] = beam_name
result["span_m"] = 6.0
result["load_kN_per_m"] = 10.0
result["num_frames"] = SapModel.FrameObj.Count()
result["num_points"] = SapModel.PointObj.Count()

print(f"Simple beam created: span = 6m, load = 10 kN/m")
print(f"Frames: {result['num_frames']}, Points: {result['num_points']}")
```

#### Step 8.4: Create basic integration tests
- [x] Create the `mcp_server/tests/` directory.
- [x] Copy and paste code below into `mcp_server/tests/__init__.py`:

```python
"""Tests for the SAP2000 MCP Server."""
```

- [x] Copy and paste code below into `mcp_server/tests/test_bridge.py`:

```python
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
from sap_bridge import SapBridge


class TestSapBridgeUnit:
    """Unit tests that don't require SAP2000."""

    def test_bridge_initial_state(self):
        """Bridge starts disconnected."""
        b = SapBridge()
        assert b.is_connected is False
        assert b.sap_object is None
        assert b.sap_model is None

    def test_get_model_info_not_connected(self):
        """get_model_info returns error when not connected."""
        b = SapBridge()
        info = b.get_model_info()
        assert info["connected"] is False
        assert "error" in info

    def test_disconnect_when_not_connected(self):
        """disconnect is safe to call when not connected."""
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
```

##### Step 8 Verification Checklist
- [x] `examples/example_1001_verification.py` exists
- [x] `examples/simple_beam.py` exists
- [x] `mcp_server/tests/test_bridge.py` exists
- [x] Unit tests pass (no SAP2000 needed): `cd mcp_server && python -m pytest tests/test_bridge.py -v -k "not Integration"`
- [x] Doc search tests find `AddByCoord` and `RunAnalysis`
- [x] Script library tests pass (save, load, list, query)
- [ ] If SAP2000 is available: integration tests pass with `python -m pytest tests/test_bridge.py -v`

#### Step 8 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
