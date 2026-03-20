# Step 2: Generic Function Executor

## Goal
Implement `execute_sap_function` — a tool that receives an API path (e.g. `"SapModel.FrameObj.AddByCoord"`), navigates the COM object hierarchy, executes the function with the given arguments, and returns the result.

## Prerequisites
Step 1 must be committed. The MCP server and COM bridge must be in place.

### Step-by-Step Instructions

#### Step 2.1: Create the SAP Executor module
- [ ] Copy and paste code below into `mcp_server/sap_executor.py`:

```python
"""
SAP2000 Function Executor — Generic execution of any SAP2000 API function.

Navigates the COM object hierarchy using a dot-separated path, calls the
target function with the provided arguments, and returns the result
including any ByRef output parameters.
"""

import logging

from sap_bridge import bridge

logger = logging.getLogger(__name__)


def _resolve_com_path(root, path: str):
    """
    Walk a dot-separated path starting from *root*.

    Example: _resolve_com_path(SapModel, "FrameObj.AddByCoord")
    returns (SapModel.FrameObj, "AddByCoord")
    """
    parts = path.split(".")
    obj = root
    for part in parts[:-1]:
        obj = getattr(obj, part)
    return obj, parts[-1]


def execute_function(function_path: str, args: list, description: str = "") -> dict:
    """
    Execute a single SAP2000 API function.

    Parameters
    ----------
    function_path : str
        Dot path relative to SapModel or SapObject.
        Examples:
          "SapModel.InitializeNewModel"
          "SapModel.FrameObj.AddByCoord"
          "SapObject.ApplicationExit"
    args : list
        Positional arguments to pass to the function.
    description : str
        Human-readable note about what this call does.

    Returns
    -------
    dict with keys: success, return_value, description, error
    """
    if not bridge.is_connected:
        return {
            "success": False,
            "error": "Not connected to SAP2000. Call connect_sap2000 first.",
        }

    # Determine root object
    if function_path.startswith("SapObject."):
        root = bridge.sap_object
        relative_path = function_path[len("SapObject."):]
    elif function_path.startswith("SapModel."):
        root = bridge.sap_model
        relative_path = function_path[len("SapModel."):]
    else:
        # Assume SapModel if no prefix
        root = bridge.sap_model
        relative_path = function_path

    try:
        parent, method_name = _resolve_com_path(root, relative_path)
        method = getattr(parent, method_name)
    except AttributeError as exc:
        return {
            "success": False,
            "error": f"Could not resolve path '{function_path}': {exc}",
            "description": description,
        }

    try:
        result = method(*args)
    except Exception as exc:
        logger.exception("Error executing %s", function_path)
        return {
            "success": False,
            "error": str(exc),
            "description": description,
        }

    # Interpret result — SAP2000 typically returns an int (0 = success)
    # or a tuple when ByRef params are present.
    return_value = result
    output_params = None

    if isinstance(result, tuple):
        return_value = result[0]
        output_params = list(result[1:])

    success = (return_value == 0) if isinstance(return_value, int) else True

    response = {
        "success": success,
        "return_value": return_value,
        "description": description,
    }
    if output_params is not None:
        response["output_params"] = output_params

    logger.info(
        "execute_sap_function: %s → %s (success=%s)",
        function_path,
        return_value,
        success,
    )
    return response
```

#### Step 2.2: Register the tool in server.py
- [ ] Add the import and tool definition. Open `mcp_server/server.py` and add the following import near the top, after the existing imports:

```python
from sap_executor import execute_function
```

- [ ] Add the following tool function at the end of the `# ── Tools` section (before the `# ── Run` section):

```python
@mcp.tool()
def execute_sap_function(
    function_path: str,
    args: list | None = None,
    description: str = "",
) -> dict:
    """Execute any SAP2000 API function by its dot-path.

    function_path: Dot-separated path like "SapModel.FrameObj.AddByCoord"
                   or "SapModel.File.New2DFrame".
    args: List of positional arguments for the function.
    description: Human-readable note about what this call does.

    Returns: {success, return_value, output_params (if any), description, error}

    SAP2000 convention: return_value 0 = success, nonzero = error.
    When the function has ByRef (output) parameters, they appear in output_params.
    """
    return execute_function(
        function_path=function_path,
        args=args or [],
        description=description,
    )
```

##### Step 2 Verification Checklist
- [ ] `mcp_server/sap_executor.py` exists and has no syntax errors
- [ ] `python -c "import mcp_server.sap_executor"` runs without import errors (from workspace root)
- [ ] `server.py` now has 4 tools: `connect_sap2000`, `disconnect_sap2000`, `get_model_info`, `execute_sap_function`
- [ ] No lint errors

#### Step 2 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
