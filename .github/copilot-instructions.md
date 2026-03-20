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
