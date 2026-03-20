"""
SAP2000 MCP Server — Entry point.

Exposes tools to Copilot so it can connect to SAP2000, inspect the model,
and (in later steps) execute functions and scripts.

Transport: stdio (launched by VS Code via mcp.json).
"""

import logging
from mcp.server.fastmcp import FastMCP

from sap_bridge import bridge
from sap_executor import execute_function, run_script
from script_library import list_scripts as _list_scripts, load_script as _load_script

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "sap2000",
    instructions="Bridge to SAP2000 structural analysis software via local COM.",
)


# ── Tools ────────────────────────────────────────────────────────────────


@mcp.tool()
def connect_sap2000(
    program_path: str | None = None,
    attach_to_existing: bool = False,
) -> dict:
    """Connect to a local SAP2000 instance.

    Use attach_to_existing=True to connect to an already-running SAP2000.
    When program_path is provided, SAP2000 is launched from that path.
    When both are omitted, the latest installed version is launched.

    Returns connection status, SAP2000 version, and active model info.
    """
    return bridge.connect(
        program_path=program_path,
        attach_to_existing=attach_to_existing,
    )


@mcp.tool()
def disconnect_sap2000(save_model: bool = False) -> dict:
    """Disconnect from SAP2000 and optionally save the current model.

    Always call this when done to release COM resources.
    """
    return bridge.disconnect(save_model=save_model)


@mcp.tool()
def get_model_info() -> dict:
    """Get current SAP2000 connection status and model summary.

    Returns: connected, version, model_path, units, num_frames, num_points, num_areas.
    Use this to verify state before or after running scripts.
    """
    return bridge.get_model_info()


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


# ── Run ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
