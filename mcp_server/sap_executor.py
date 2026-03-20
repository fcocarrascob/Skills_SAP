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
