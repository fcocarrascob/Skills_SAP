# Contributing to the SAP2000 AI-Assisted Framework

Thank you for helping grow the library of verified SAP2000 scripts and functions!

---

## Ways to Contribute

1. **Add a wrapper script** for a SAP2000 API function not yet covered
2. **Improve an existing wrapper** with better error handling or documentation
3. **Add a complete model script** to the script library
4. **Improve API documentation** in the `API/` directory
5. **Fix bugs** in the MCP server modules
6. **Improve tests** for the framework components

---

## Adding a Wrapper Script

A wrapper script is a self-contained, minimal Python script that demonstrates
the correct usage of a single SAP2000 API function via the COM bridge.

### Naming Convention

```
scripts/wrappers/func_{ObjectType}_{FunctionName}.py
```

Examples:
- `func_FrameObj_AddByCoord.py`
- `func_PropMaterial_SetMPIsotropic.py`
- `func_Results_JointDispl.py`

### Wrapper Template

```python
# SAP2000 wrapper: {ObjectType}.{FunctionName}
# Verified: YYYY-MM-DD
# Category: {API Category}
#
# Function signature (Python COM bridge):
#   raw = SapModel.{ObjectType}.{FunctionName}(arg1, arg2, ...)
#   → raw[-1] is the return code (0 = success)
#   → raw[0..n-2] are ByRef output parameters (if any)
#
# Parameter notes:
#   arg1: description and type
#   arg2: description and type

# Initialize a fresh model
ret = SapModel.InitializeNewModel()
assert ret == 0, f"InitializeNewModel failed: {ret}"
ret = SapModel.File.NewBlank()
assert ret == 0, f"NewBlank failed: {ret}"

# Set units
ret = SapModel.SetPresentUnits(6)  # 6 = kN_m_C
assert ret == 0

# --- Call the target function ---
raw = SapModel.{ObjectType}.{FunctionName}(arg1, arg2, ...)
ret_code = raw[-1] if isinstance(raw, (list, tuple)) else raw
assert ret_code == 0, f"{FunctionName} failed: {ret_code}"

# Write results for verification
result["success"] = True
result["return_code"] = ret_code
# result["output"] = raw[0]  # Include any ByRef outputs
```

### Wrapper Requirements

- **Self-contained:** initializes a fresh blank model at the start
- **Single function focus:** tests only one API function
- **Asserts success:** uses `assert ret_code == 0`
- **Writes to `result`:** documents outputs in the `result` dict
- **Documents ByRef layout:** comments explain what each element of `raw` contains

---

## Running Tests

Before submitting, run the unit tests to make sure nothing is broken:

```bash
cd mcp_server
python -m pytest tests/ -v
```

All tests must pass. Integration tests (requiring SAP2000) are automatically
skipped on non-Windows platforms.

---

## Registering a New Function

After verifying a wrapper runs successfully, register the function in the registry
either via the MCP tool or by editing `scripts/registry.json` directly:

```json
{
  "SapModel.ObjectType.FunctionName": {
    "category": "API Category",
    "description": "Brief description of what the function does",
    "signature": "FunctionName(arg1 As Type, arg2 As Type) As Long",
    "verified": true,
    "wrapper_script": "func_ObjectType_FunctionName",
    "parameter_notes": "arg1: ..., arg2: ...",
    "notes": "ByRef layout: raw[0]=output1, raw[-1]=ret_code"
  }
}
```

---

## Code Style

- Follow the existing code style in each module
- Use descriptive variable names (`ret_code` not `r`)
- Add docstrings to new functions/classes
- Keep wrapper scripts under ~50 lines

---

## Submitting a Pull Request

1. Fork the repository and create a feature branch
2. Add your wrapper(s) and/or improvements
3. Run `python -m pytest mcp_server/tests/ -v` and confirm all tests pass
4. Submit a PR with a clear description of what function(s) you are adding

---

## Questions?

Open an issue in the repository with your question or use the GitHub Copilot
agent with this repository to get AI-assisted guidance.
