# Step 7: MCP Configuration + Integration

## Goal
Configure VS Code to recognize and launch the MCP server, create a README with installation instructions, and add global Copilot instructions that point to the SAP2000 skill.

## Prerequisites
Steps 1–6 must be committed. The MCP server and SKILL.md must be in place.

### Step-by-Step Instructions

#### Step 7.1: Create the VS Code MCP configuration
- [ ] Create the `.vscode/` directory if it doesn't exist.
- [ ] Copy and paste code below into `.vscode/mcp.json`:

```json
{
  "servers": {
    "sap2000": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${workspaceFolder}/mcp_server/server.py"
      ],
      "env": {}
    }
  }
}
```

#### Step 7.2: Create global Copilot instructions
- [ ] Copy and paste code below into `.github/copilot-instructions.md`:

```markdown
# Copilot Instructions

## SAP2000 API Skill

This workspace contains a **SAP2000 API skill** (`sap2000-api`) that enables
Copilot to create, execute, and verify SAP2000 scripts via a local COM bridge.

### When to use

Use the `sap2000-api` skill for ANY task involving:
- SAP2000 modeling, automation, or scripting
- Creating structural models (frames, areas, joints)
- Assigning loads (dead, live, seismic, wind)
- Running structural analysis
- Extracting analysis or design results
- Debugging SAP2000 API errors

### Available MCP tools

The `sap2000` MCP server provides these tools:

| Tool | Purpose |
|------|---------|
| `connect_sap2000` | Connect to a local SAP2000 instance |
| `disconnect_sap2000` | Disconnect and release COM resources |
| `get_model_info` | Check connection status and model summary |
| `execute_sap_function` | Execute a single API function by dot-path |
| `run_sap_script` | Execute a full Python script in sandbox |
| `list_scripts` | Browse saved scripts in the library |
| `load_script` | Load a saved script for modification |
| `search_api_docs` | Search API documentation for functions |
| `list_api_categories` | List API documentation categories |

### Requirements

- Windows OS (SAP2000 only runs on Windows)
- Python 3.10+
- SAP2000 installed locally
- Python packages: `comtypes`, `mcp[cli]`
```

#### Step 7.3: Create the MCP server README
- [ ] Copy and paste code below into `mcp_server/README.md`:

```markdown
# SAP2000 MCP Server

MCP (Model Context Protocol) server that bridges Copilot to a local SAP2000
instance via COM. Allows Copilot to generate, execute, and verify SAP2000 API
scripts.

## Requirements

- **Windows** (required — SAP2000 only runs on Windows)
- **Python 3.10+**
- **SAP2000** installed locally (any version with API support)
- **comtypes** — Python COM interface
- **mcp[cli]** — MCP server SDK

## Installation

```bash
cd mcp_server
pip install -r requirements.txt
```

## Usage

### Automatic (via VS Code)

The MCP server is configured in `.vscode/mcp.json` and starts automatically
when Copilot needs it. No manual action required.

### Manual (for testing)

```bash
python mcp_server/server.py
```

The server communicates via stdio (standard input/output) using the MCP protocol.

## Architecture

```
mcp_server/
├── server.py          # MCP server entry point — tool registration
├── sap_bridge.py      # COM connection management (singleton)
├── sap_executor.py    # Function executor + script runner (sandbox)
├── script_library.py  # Script persistence and search
├── doc_search.py      # API documentation search engine
├── requirements.txt   # Python dependencies
└── __init__.py
```

## Tools

| Tool | Description |
|------|-------------|
| `connect_sap2000` | Connect to SAP2000 (new or existing instance) |
| `disconnect_sap2000` | Disconnect and release COM resources |
| `get_model_info` | Get connection status and model summary |
| `execute_sap_function` | Execute any API function by dot-path |
| `run_sap_script` | Execute a Python script in sandbox |
| `list_scripts` | Browse the script library |
| `load_script` | Load a script by name |
| `search_api_docs` | Search API documentation |
| `list_api_categories` | List API doc categories |

## Sandbox

Scripts executed via `run_sap_script` run in a restricted environment:

**Allowed imports:** math, json, datetime, decimal, fractions, collections,
itertools, functools, typing

**Blocked:** os, subprocess, sys, shutil, pathlib, socket, http, urllib,
importlib, ctypes, pickle, and all file I/O

**Timeout:** 120 seconds

**Pre-injected variables:** `SapModel`, `SapObject`, `result` (dict)

## Script Library

Successfully executed scripts are saved in `scripts/` with metadata headers.
Use `list_scripts` to browse and `load_script` to reload any saved script.
```

##### Step 7 Verification Checklist
- [ ] `.vscode/mcp.json` exists with the `sap2000` server configuration
- [ ] `.github/copilot-instructions.md` exists and lists all 9 tools
- [ ] `mcp_server/README.md` exists with installation and architecture docs
- [ ] The command path in `mcp.json` correctly references `server.py`
- [ ] No JSON syntax errors in `mcp.json`

#### Step 7 STOP & COMMIT
**STOP & COMMIT:** Agent must stop here and wait for the user to test, stage, and commit the change.
