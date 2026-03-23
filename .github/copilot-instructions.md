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

### SAP2000 Scripter Agent

For **interactive script generation**, use the **SAP2000 Scripter** custom agent 
(available in the agents dropdown). This agent specializes in:

- Asking clarifying questions before generating scripts
- Searching for verified functions and wrappers
- Generating clean, parametric scripts following established conventions
- Executing scripts and verifying results
- Saving successful scripts to the library

**When to use the agent:**
- User asks to "generate a script" for a specific SAP2000 model
- User describes a structural element in natural language (e.g., "create a 
  parametric plate with holes")
- User needs step-by-step guidance through the scripting process

**How to invoke:** Select "SAP2000 Scripter" from the agents dropdown in Chat, or 
mention `@sap2000-scripter` in your prompt

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
| `query_function_registry` | Query verified functions by path, category, or keyword |
| `register_verified_function` | Register or update a verified API function |
| `list_registry_categories` | List categories with registered/verified counts |

### Requirements

- Windows OS (SAP2000 only runs on Windows)
- Python 3.10+
- SAP2000 installed locally
- Python packages: `comtypes`, `mcp[cli]`

### GUI Standalone Generation

The agent can also generate **standalone GUIs** (PySide6 + direct COM) from
verified scripts. These GUIs do NOT depend on the MCP server.

**When to offer:**
- After a script has been successfully verified and saved
- When the user asks for a "GUI", "standalone app", or "desktop tool"

**Structure:** `scripts/{nombre}/gui_{nombre}.py` + `backend_{nombre}.py`

**Templates:** See `scripts/templates/` for base templates.

**Workflow:** See Phase 6 in `plans/workflow-script-creation.md`.
