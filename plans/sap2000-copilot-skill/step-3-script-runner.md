# Step 3: Script Runner

## Goal
Implement `run_sap_script` — the primary tool for the agent's workflow. The agent generates complete Python scripts, and this tool executes them in a sandboxed environment with `SapModel` and `SapObject` pre-injected, capturing stdout, stderr, and a `result` dictionary.

## Prerequisites
Steps 1–2 must be committed. The MCP server, COM bridge, and function executor must be in place.

### Step-by-Step Instructions

#### Step 3.1: Add the script runner to sap_executor.py
- [ ] Open `mcp_server/sap_executor.py` and add the following imports at the top of the file, after the existing imports:

```python
import io
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
```

- [ ] Add the following constants and functions at the **end** of `mcp_server/sap_executor.py`:

```python
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


def run_script(script: str, description: str = "") -> dict:
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

    return {
        "success": True,
        "stdout": captured_stdout.getvalue(),
        "stderr": captured_stderr.getvalue(),
        "result": sandbox_globals.get("result", {}),
        "execution_time_s": round(elapsed, 3),
        "description": description,
    }
```

#### Step 3.2: Register the run_sap_script tool in server.py
- [ ] Add the import in `mcp_server/server.py`. Update the existing import line from `sap_executor`:

Change:
```python
from sap_executor import execute_function
```
To:
```python
from sap_executor import execute_function, run_script
```

- [ ] Add the following tool function at the end of the `# ── Tools` section (before the `# ── Run` section):

```python
@mcp.tool()
def run_sap_script(
    script: str,
    description: str = "",
) -> dict:
    """Execute a Python script against the connected SAP2000 instance.

    The script runs in a sandbox with pre-injected variables:
      - SapModel: COM reference to the active model
      - SapObject: COM reference to the SAP2000 application
      - result: dict — write output values here for the agent to read

    Sandbox restrictions:
      - Only safe modules allowed (math, json, datetime, decimal, etc.)
      - No file I/O, no os/subprocess/sys access
      - 120 second timeout

    Returns: {success, stdout, stderr, result, execution_time_s, error}

    Workflow:
      1. Agent generates script based on API docs
      2. This tool executes it
      3. Agent reads result to verify or correct
    """
    return run_script(script=script, description=description)
```

##### Step 3 Verification Checklist
- [ ] `sap_executor.py` has both `execute_function` and `run_script` functions
- [ ] `server.py` now has 5 tools: `connect_sap2000`, `disconnect_sap2000`, `get_model_info`, `execute_sap_function`, `run_sap_script`
- [ ] Running `python mcp_server/server.py` starts without import errors
- [ ] No lint errors

#### Step 3 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
