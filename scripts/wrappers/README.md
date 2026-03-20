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
