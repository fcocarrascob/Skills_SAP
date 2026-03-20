"""
SAP2000 MCP Server — Entry point.

Exposes tools to Copilot so it can connect to SAP2000, inspect the model,
and (in later steps) execute functions and scripts.

Transport: stdio (launched by VS Code via mcp.json).
"""

import logging
from mcp.server.fastmcp import FastMCP

from sap_bridge import bridge

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


# ── Run ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
