"""
SAP2000 Function Executor — Generic execution of any SAP2000 API function.

Navigates the COM object hierarchy using a dot-separated path, calls the
target function with the provided arguments, and returns the result
including any ByRef output parameters.
"""

import io
import re
import sys
import time
import math
import json
import datetime
import decimal
import fractions
import collections
import itertools
import functools
import threading
import logging
import ast

from sap_bridge import bridge
from script_library import save_script
from function_registry import registry as function_registry

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

    if isinstance(result, (list, tuple)):
        return_value = result[-1]           # ret_code is ALWAYS last
        output_params = list(result[:-1])   # All ByRef outputs before it

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


# ── Sandbox configuration ────────────────────────────────────────────────

ALLOWED_MODULES = frozenset({
    "math", "json", "datetime", "decimal", "fractions",
    "collections", "itertools", "functools", "typing",
})

BLOCKED_MODULES = frozenset({
    "os", "subprocess", "sys", "shutil", "pathlib",
    "socket", "http", "urllib", "importlib", "ctypes",
    "pickle", "shelve", "tempfile", "glob", "signal",
    "multiprocessing", "threading", "webbrowser",
})

SCRIPT_TIMEOUT_S = 120


def _safe_import(name, globals_=None, locals_=None, fromlist=(), level=0):
    """Restricted __import__ that only allows ALLOWED_MODULES."""
    top_level = name.split(".")[0]
    if top_level in BLOCKED_MODULES:
        raise ImportError(
            f"Module '{name}' is blocked in the SAP2000 script sandbox."
        )
    if top_level not in ALLOWED_MODULES:
        raise ImportError(
            f"Module '{name}' is not available in the SAP2000 script sandbox. "
            f"Allowed: {', '.join(sorted(ALLOWED_MODULES))}"
        )
    return __builtins__.__import__(name, globals_, locals_, fromlist, level)


def _safe_open(*args, **kwargs):
    """Block all file I/O inside scripts."""
    raise PermissionError("File I/O is not allowed in the SAP2000 script sandbox.")


def _build_sandbox_globals() -> dict:
    """
    Build the globals dict for script execution.

    Pre-injects SapModel, SapObject, result dict, safe builtins,
    and allowed modules.
    """
    safe_builtins = dict(__builtins__.__dict__) if hasattr(__builtins__, '__dict__') else dict(__builtins__)
    safe_builtins["__import__"] = _safe_import
    safe_builtins["open"] = _safe_open

    sandbox = {
        "__builtins__": safe_builtins,
        # Pre-injected SAP2000 references
        "SapModel": bridge.sap_model,
        "SapObject": bridge.sap_object,
        # Output dict — scripts write results here
        "result": {},
        # Pre-imported allowed modules for convenience
        "math": math,
        "json": json,
        "datetime": datetime,
        "decimal": decimal,
        "fractions": fractions,
        "collections": collections,
        "itertools": itertools,
        "functools": functools,
    }
    return sandbox


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


def run_script(script: str, description: str = "", save_as: str | None = None) -> dict:
    """
    Execute a Python script string in the SAP2000 sandbox.

    The script receives pre-injected variables:
      - SapModel   : COM reference to the active model
      - SapObject  : COM reference to the SAP2000 application
      - result     : dict — write output values here

    Sandbox restrictions:
      - Only allowed modules can be imported
      - No file I/O (open is blocked)
      - Blocked dangerous modules (os, subprocess, etc.)
      - Timeout: 120 seconds

    Returns
    -------
    dict with keys:
      success, stdout, stderr, result, execution_time_s, error
    """
    if not bridge.is_connected:
        return {
            "success": False,
            "error": "Not connected to SAP2000. Call connect_sap2000 first.",
        }

    sandbox_globals = _build_sandbox_globals()
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()

    exec_error = [None]
    start_time = time.perf_counter()

    def _run():
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        try:
            sys.stdout = captured_stdout
            sys.stderr = captured_stderr
            exec(compile(script, "<sap_script>", "exec"), sandbox_globals)
        except Exception as exc:
            exec_error[0] = exc
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

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

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout=SCRIPT_TIMEOUT_S)

    elapsed = time.perf_counter() - start_time

    if thread.is_alive():
        return {
            "success": False,
            "error": f"Script timed out after {SCRIPT_TIMEOUT_S}s.",
            "stdout": captured_stdout.getvalue(),
            "stderr": captured_stderr.getvalue(),
            "result": sandbox_globals.get("result", {}),
            "execution_time_s": round(elapsed, 3),
            "description": description,
        }

    if exec_error[0] is not None:
        return {
            "success": False,
            "error": str(exec_error[0]),
            "stdout": captured_stdout.getvalue(),
            "stderr": captured_stderr.getvalue(),
            "result": sandbox_globals.get("result", {}),
            "execution_time_s": round(elapsed, 3),
            "description": description,
        }

    response = {
        "success": True,
        "stdout": captured_stdout.getvalue(),
        "stderr": captured_stderr.getvalue(),
        "result": sandbox_globals.get("result", {}),
        "execution_time_s": round(elapsed, 3),
        "description": description,
    }

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
