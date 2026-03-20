# Step 4: Script Library — Storage and Reuse

## Goal
Implement the script persistence system: `list_scripts` and `load_script` tools, plus the save mechanism invoked by `run_sap_script` via the `save_as` parameter. Successfully executed scripts are stored in `scripts/` with embedded metadata for future reuse.

## Prerequisites
Steps 1–3 must be committed. The MCP server, COM bridge, and script runner must be in place.

### Step-by-Step Instructions

#### Step 4.1: Create the Script Library module
- [x] Create the `scripts/` directory in the workspace root.
- [x] Copy and paste code below into `scripts/README.md`:

```markdown
# SAP2000 Script Library

Auto-managed collection of verified SAP2000 API scripts.

Scripts are saved here automatically when the agent runs them successfully with `save_as`.
Use `list_scripts` to browse and `load_script` to reload any script.

## Usage

Scripts are designed to be executed via the `run_sap_script` MCP tool.
They expect `SapModel`, `SapObject`, and `result` to be pre-injected.
```

- [x] Copy and paste code below into `mcp_server/script_library.py`:

```python
"""
SAP2000 Script Library — Persistence, search, and reuse of verified scripts.

Scripts are stored as .py files in the scripts/ folder with embedded metadata
in a header comment block.
"""

import os
import re
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# scripts/ lives at the workspace root, one level up from mcp_server/
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


def _ensure_scripts_dir():
    """Create scripts/ if it doesn't exist."""
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def save_script(
    name: str,
    script: str,
    description: str = "",
    result: dict | None = None,
    tags: list[str] | None = None,
) -> dict:
    """
    Save a script to the library with metadata header.

    Parameters
    ----------
    name : str
        Script name (without .py extension). Used as the filename.
    script : str
        The Python source code.
    description : str
        What this script does.
    result : dict | None
        Execution result summary to embed in header.
    tags : list[str] | None
        Optional tags for categorization.

    Returns
    -------
    dict  {saved, path, error}
    """
    _ensure_scripts_dir()

    # Sanitize name: only allow alphanumeric, underscore, hyphen
    safe_name = re.sub(r"[^\w\-]", "_", name).strip("_")
    if not safe_name:
        return {"saved": False, "error": "Invalid script name."}

    file_path = SCRIPTS_DIR / f"{safe_name}.py"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    result_str = json.dumps(result, default=str) if result else "{}"
    tags_str = ", ".join(tags) if tags else ""

    header = (
        f'# {"─" * 3} SAP2000 Script {"─" * 45}\n'
        f"# Name:        {safe_name}\n"
        f"# Description: {description}\n"
        f"# Created:     {now}\n"
        f"# Status:      ✓ Verified (executed successfully)\n"
        f"# Result:      {result_str}\n"
        f"# Tags:        {tags_str}\n"
        f'# {"─" * 62}\n'
        f"\n"
    )
    full_content = header + script

    try:
        file_path.write_text(full_content, encoding="utf-8")
        logger.info("Saved script '%s' to %s", safe_name, file_path)
        return {"saved": True, "path": str(file_path)}
    except Exception as exc:
        logger.exception("Failed to save script '%s'", safe_name)
        return {"saved": False, "error": str(exc)}


def list_scripts(query: str | None = None, tag: str | None = None) -> list[dict]:
    """
    List scripts in the library, optionally filtered by keyword or tag.

    Parameters
    ----------
    query : str | None
        Search term matched against name and description (case-insensitive).
    tag : str | None
        Filter by tag.

    Returns
    -------
    list[dict]  Each dict: {name, description, created, status, tags, path}
    """
    _ensure_scripts_dir()

    results = []
    for py_file in sorted(SCRIPTS_DIR.glob("*.py")):
        meta = _parse_header(py_file)
        if meta is None:
            continue

        # Apply filters
        if query:
            q = query.lower()
            if q not in meta["name"].lower() and q not in meta["description"].lower():
                continue
        if tag:
            if tag.lower() not in [t.lower() for t in meta.get("tags", [])]:
                continue

        meta["path"] = str(py_file)
        results.append(meta)

    return results


def load_script(name: str) -> dict:
    """
    Load a script by name and return its code + metadata.

    Parameters
    ----------
    name : str
        Script name (without .py).

    Returns
    -------
    dict  {name, description, script_code, metadata} or {error}
    """
    _ensure_scripts_dir()

    safe_name = re.sub(r"[^\w\-]", "_", name).strip("_")
    file_path = SCRIPTS_DIR / f"{safe_name}.py"

    if not file_path.exists():
        return {"error": f"Script '{safe_name}' not found in library."}

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        return {"error": f"Failed to read script: {exc}"}

    meta = _parse_header(file_path) or {}

    # Strip the header block to get just the script code
    lines = content.split("\n")
    code_start = 0
    for i, line in enumerate(lines):
        if not line.startswith("#") and line.strip() != "":
            code_start = i
            break
        if line.strip() == "" and i > 0 and not lines[i - 1].startswith("#"):
            code_start = i
            break

    script_code = "\n".join(lines[code_start:]).strip()

    return {
        "name": meta.get("name", safe_name),
        "description": meta.get("description", ""),
        "script_code": script_code,
        "metadata": meta,
    }


def _parse_header(file_path: Path) -> dict | None:
    """Parse the metadata header from a saved script file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    meta = {
        "name": file_path.stem,
        "description": "",
        "created": "",
        "status": "",
        "tags": [],
    }

    for line in content.split("\n"):
        if not line.startswith("#"):
            break
        line_clean = line.lstrip("# ").strip()

        if line_clean.startswith("Name:"):
            meta["name"] = line_clean[len("Name:"):].strip()
        elif line_clean.startswith("Description:"):
            meta["description"] = line_clean[len("Description:"):].strip()
        elif line_clean.startswith("Created:"):
            meta["created"] = line_clean[len("Created:"):].strip()
        elif line_clean.startswith("Status:"):
            meta["status"] = line_clean[len("Status:"):].strip()
        elif line_clean.startswith("Tags:"):
            raw_tags = line_clean[len("Tags:"):].strip()
            meta["tags"] = [t.strip() for t in raw_tags.split(",") if t.strip()]
        elif line_clean.startswith("Result:"):
            try:
                meta["result_summary"] = json.loads(
                    line_clean[len("Result:"):].strip()
                )
            except (json.JSONDecodeError, ValueError):
                meta["result_summary"] = line_clean[len("Result:"):].strip()

    return meta
```

#### Step 4.2: Add save_as parameter to run_sap_script
- [x] Open `mcp_server/sap_executor.py`. Add the following import at the top, after the existing imports:

```python
from script_library import save_script
```

- [x] In `mcp_server/sap_executor.py`, update the `run_script` function signature and add save logic. Replace the function signature:

Change:
```python
def run_script(script: str, description: str = "") -> dict:
```
To:
```python
def run_script(script: str, description: str = "", save_as: str | None = None) -> dict:
```

- [x] At the end of `run_script`, just before the final `return` statement (the success case), add the save logic. Replace:

```python
    return {
        "success": True,
        "stdout": captured_stdout.getvalue(),
        "stderr": captured_stderr.getvalue(),
        "result": sandbox_globals.get("result", {}),
        "execution_time_s": round(elapsed, 3),
        "description": description,
    }
```

With:

```python
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

    return response
```

#### Step 4.3: Register library tools in server.py
- [x] Add the import in `mcp_server/server.py`. Add after the existing sap_executor import:

```python
from script_library import list_scripts as _list_scripts, load_script as _load_script
```

- [x] Update the existing `run_sap_script` tool to include `save_as`. Replace:

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

With:

```python
@mcp.tool()
def run_sap_script(
    script: str,
    description: str = "",
    save_as: str | None = None,
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

    save_as: If provided and script succeeds, saves to scripts/{save_as}.py
             for future reuse via list_scripts / load_script.

    Returns: {success, stdout, stderr, result, execution_time_s, saved_path, error}

    Workflow:
      1. Agent generates script based on API docs
      2. This tool executes it
      3. Agent reads result to verify or correct
      4. If successful, saves for reuse
    """
    return run_script(script=script, description=description, save_as=save_as)
```

- [x] Add the two library tools at the end of the `# ── Tools` section:

```python
@mcp.tool()
def list_scripts(
    query: str | None = None,
    tag: str | None = None,
) -> list[dict]:
    """List saved SAP2000 scripts in the library.

    query: Search by name or description keyword (case-insensitive).
    tag: Filter by tag (e.g. "loads", "analysis", "results").

    Returns: List of {name, description, created, status, tags, path}.

    Use this to find existing scripts before generating a new one.
    """
    return _list_scripts(query=query, tag=tag)


@mcp.tool()
def load_script(name: str) -> dict:
    """Load a saved script by name from the library.

    name: Script name without .py extension.

    Returns: {name, description, script_code, metadata}

    Use this to retrieve an existing script, modify it, and re-execute.
    """
    return _load_script(name=name)
```

##### Step 4 Verification Checklist
- [x] `mcp_server/script_library.py` exists with `save_script`, `list_scripts`, `load_script` functions
- [x] `scripts/README.md` exists
- [x] `server.py` now has 7 tools: `connect_sap2000`, `disconnect_sap2000`, `get_model_info`, `execute_sap_function`, `run_sap_script`, `list_scripts`, `load_script`
- [x] `run_sap_script` accepts `save_as` parameter
- [x] Running `python mcp_server/server.py` starts without import errors
- [x] No lint errors

#### Step 4 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
