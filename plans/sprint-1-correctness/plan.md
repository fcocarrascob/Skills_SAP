# Sprint 1 — Correctness Fixes

**Branch:** `fix/sprint-1-correctness`
**Description:** Fix critical bugs in execute_function ByRef parsing, hardcoded paths in wrappers, add syntax pre-validation, create Example 1-001, and close test gaps.

## Goal

Eliminar los bugs de correctitud que impiden que el MCP server funcione de forma fiable en máquinas distintas a la del desarrollador original. Estos fixes son prerrequisito para cualquier distribución del skill a otros usuarios.

## Implementation Steps

### Step 1: Fix ByRef parsing in `execute_function`
**Files:** `mcp_server/sap_executor.py`
**What:** The `execute_function()` method (lines 113-130) incorrectly treats `result[0]` as the return code. SAP2000 COM convention is `result[-1]` = ret_code, `result[:-1]` = ByRef outputs. Fix the tuple/list unpacking to match the convention already documented in SKILL.md and used correctly by all wrappers.

Current (WRONG):
```python
if isinstance(result, tuple):
    return_value = result[0]           # ← First ByRef output, NOT ret_code
    output_params = list(result[1:])   # ← Includes ret_code mixed in
```

Target (CORRECT):
```python
if isinstance(result, (list, tuple)):
    return_value = result[-1]          # ret_code is ALWAYS last
    output_params = list(result[:-1])  # All ByRef outputs before it
```

Also update the `success` check to handle the case where `return_value` is not an int (some COM calls return strings or None).

**Testing:**
- Unit test: mock a COM call returning `("FrameName", 0)` → verify `return_value=0`, `output_params=["FrameName"]`
- Unit test: mock a COM call returning `(0,)` → verify `return_value=0`, `output_params=[]`
- Unit test: mock a COM call returning `0` (plain int) → verify `return_value=0`, `output_params=None`
- Integration test (SAP2000 required): `execute_sap_function("SapModel.FrameObj.AddByCoord", [...])` → verify `output_params[0]` is a string (frame name), `return_value=0`

### Step 2: Add `ast.parse()` pre-validation before `exec()`
**Files:** `mcp_server/sap_executor.py`
**What:** Add `import ast` at the top. In `run_script()`, before the threading/exec block (around line 247), insert an `ast.parse(script)` call wrapped in try/except SyntaxError. This fails fast with a clear error message including line number, without spawning a thread.

Target insertion:
```python
# Pre-validate syntax before spawning thread
try:
    ast.parse(script)
except SyntaxError as e:
    return {
        "success": False,
        "error": f"Syntax error at line {e.lineno}: {e.msg}",
        "stdout": "",
        "stderr": "",
        "result": {},
        "execution_time_s": 0,
        "description": description,
    }
```

**Testing:**
- Unit test: `run_script("x = ")` → `success=False`, error contains "line 1"
- Unit test: `run_script("def f():\n  x = 1\n x = 2")` → `success=False`, error contains "indentation"
- Unit test: `run_script("x = 1\ny = 2")` → does NOT trigger syntax error (passes through to exec)

### Step 3: Inject `sap_temp_dir` into sandbox and fix hardcoded wrapper paths
**Files:** `mcp_server/sap_executor.py`, 7 wrapper scripts in `scripts/wrappers/`
**What:** Two changes:

**3a)** In `_build_sandbox_globals()`, inject a `sap_temp_dir` variable pointing to `os.path.join(tempfile.gettempdir(), "sap2000_scripts")`. Create the directory if it doesn't exist. This uses `os` and `tempfile` in the server code (allowed), not in the sandboxed script. Scripts can then use `sap_temp_dir` to build save paths.

```python
import tempfile as _tempfile
import os as _os

def _build_sandbox_globals() -> dict:
    # ... existing code ...
    temp_dir = _os.path.join(_tempfile.gettempdir(), "sap2000_scripts")
    _os.makedirs(temp_dir, exist_ok=True)
    sandbox["sap_temp_dir"] = temp_dir
    return sandbox
```

**3b)** Update the 7 wrapper scripts with hardcoded paths:

| File | Old Path | New Path |
|------|----------|----------|
| `func_DesignConcrete_StartDesign.py` | `r"C:\Temp\sap_design_concrete.sdb"` | `sap_temp_dir + r"\sap_design_concrete.sdb"` |
| `func_DesignSteel_StartDesign.py` | `r"C:\Temp\sap_design_steel.sdb"` | `sap_temp_dir + r"\sap_design_steel.sdb"` |
| `func_Results_AreaForceShell.py` | `r"C:\Temp\sap_results_areaforceshell.sdb"` | `sap_temp_dir + r"\sap_results_areaforceshell.sdb"` |
| `func_Results_FrameForce.py` | `r"C:\Temp\sap_results_frameforce.sdb"` | `sap_temp_dir + r"\sap_results_frameforce.sdb"` |
| `func_Results_JointDispl.py` | `r"C:\Temp\sap_results_jointdispl.sdb"` | `sap_temp_dir + r"\sap_results_jointdispl.sdb"` |
| `func_Results_JointReact.py` | `r"C:\Temp\sap_results_jointreact.sdb"` | `sap_temp_dir + r"\sap_results_jointreact.sdb"` |
| `func_File_OpenFile.py` | `r"C:\Users\fcoca\AppData\Local\Temp\test_open_file.sdb"` | `sap_temp_dir + r"\test_open_file.sdb"` |

**3c)** Update SKILL.md script template section to document `sap_temp_dir` as a pre-injected variable alongside `SapModel`, `SapObject`, and `result`.

**Testing:**
- Unit test: verify `_build_sandbox_globals()` contains `sap_temp_dir` key pointing to a real directory
- Manual: run each modified wrapper via `run_sap_script` and verify it saves to temp dir
- Verify on a clean machine (no `C:\Temp\`) that wrappers still work

### Step 4: Create Example 1-001 verification script
**Files:** `scripts/example_1001_simple_beam.py` (new)
**What:** Create the Example 1-001 verification script (originally planned in step-8 but never created as a file). This is a complete end-to-end test that creates a model, applies loads, runs analysis, extracts results, and compares against known reference values. Key requirements:
- Use `raw[0]` / `raw[-1]` pattern consistently (NOT `ret[1]`)
- Use `sap_temp_dir` for File.Save paths
- Assert `raw[-1] == 0` for all ByRef functions
- Compare displacement results against hand-calculated values with tolerance
- Write all verification data to `result` dict

This script also serves as the canonical "how to write a SAP2000 script" reference.

**Testing:**
- Execute via `run_sap_script` with SAP2000 running
- Verify `result["verification_passed"]` is True
- Verify displacement values are within 1% of reference

### Step 5: Add unit tests for all Sprint 1 fixes
**Files:** `mcp_server/tests/test_executor.py` (new), updates to `mcp_server/tests/test_bridge.py`
**What:** Create a new test file focused on the executor, covering all Sprint 1 fixes:

**test_executor.py (new):**
```
TestExecuteFunctionByRef:
  - test_byref_tuple_parsing: mock COM call → verify return_value/output_params split
  - test_plain_int_result: mock COM call returning int → verify no output_params
  - test_single_element_tuple: mock COM call returning (0,) → verify handling

TestSyntaxPreValidation:
  - test_syntax_error_detected_early: bad script → error with line number
  - test_indentation_error: bad indent → early error
  - test_valid_script_passes_validation: good script → no syntax error

TestSandboxGlobals:
  - test_sap_temp_dir_injected: verify key exists and dir is real
  - test_sap_temp_dir_is_writable: verify directory exists on disk
  - test_blocked_modules_still_blocked: verify os/subprocess/sys still blocked
  - test_allowed_modules_available: verify math/json/datetime injected

TestApiExtraction:
  - test_extract_sapmodel_calls: script with SapModel.X.Y() → correct paths
  - test_extract_sapobject_calls: script with SapObject.X() → correct paths
  - test_no_duplicates: repeated calls → unique list
```

**Updates to test_bridge.py:**
- Add `test_execute_function_not_connected_returns_error` (if not already there)

**Testing:**
- `python -m pytest mcp_server/tests/ -v` — all tests pass
- No SAP2000 required for unit tests (mocked COM layer)

### Step 6: Update SKILL.md with `sap_temp_dir` documentation
**Files:** `.github/skills/sap2000-api/SKILL.md`
**What:** Update the "Pre-injected Variables" section to include `sap_temp_dir`:

```python
SapModel    # cSapModel — the active model reference
SapObject   # cOAPI — the SAP2000 application object
result      # dict — write output values here for verification
sap_temp_dir  # str — writable temp directory for File.Save() calls
```

Also update the "Basic Script Template" example to use `sap_temp_dir` when saving.

Update the "Results Extraction Template" to show usage of `sap_temp_dir`:

```python
ret = SapModel.File.Save(sap_temp_dir + r"\my_model.sdb")
```

**Testing:**
- Read SKILL.md and verify `sap_temp_dir` appears in pre-injected variables section
- Verify template examples use `sap_temp_dir` instead of hardcoded paths

## Commit Strategy

| Commit | Step | Message |
|--------|------|---------|
| 1 | Step 1 | `fix: correct ByRef return code parsing in execute_function` |
| 2 | Step 2 | `fix: add ast.parse() pre-validation before exec()` |
| 3 | Steps 3 + 6 | `fix: inject sap_temp_dir and remove hardcoded paths from wrappers` |
| 4 | Step 4 | `feat: add Example 1-001 verification script` |
| 5 | Step 5 | `test: add unit tests for Sprint 1 fixes` |

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| `execute_function` fix breaks existing caller expectations | No external callers found; MCP tool `execute_sap_function` is the only consumer. The fix aligns it with the convention already documented everywhere. |
| `sap_temp_dir` path differs across Windows versions | Using `tempfile.gettempdir()` which is OS-aware. Works on all Windows versions. |
| Wrappers that use `sap_temp_dir` fail when run outside sandbox | `sap_temp_dir` is only available inside the sandbox. Wrappers are designed to run only via `run_sap_script`. Document this clearly. |
| `ast.parse()` rejects valid scripts | `ast.parse()` only rejects syntactically invalid Python. No false positives possible. |

## Definition of Done

- [ ] `execute_function` returns `ret_code` as `return_value` and ByRef outputs in `output_params`
- [ ] `run_script` with syntax errors returns immediately with line number in error message
- [ ] All 7 wrappers use `sap_temp_dir` instead of hardcoded paths
- [ ] `sap_temp_dir` is documented in SKILL.md
- [ ] Example 1-001 script exists and runs successfully (with SAP2000)
- [ ] All new unit tests pass without SAP2000 installed
- [ ] `python -m pytest mcp_server/tests/ -v` passes 100%
