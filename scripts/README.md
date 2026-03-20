# SAP2000 Script Library

Auto-managed collection of verified SAP2000 API scripts.

Scripts are saved here automatically when the agent runs them successfully with `save_as`.
Use `list_scripts` to browse and `load_script` to reload any script.

## Usage

Scripts are designed to be executed via the `run_sap_script` MCP tool.
They expect `SapModel`, `SapObject`, and `result` to be pre-injected.

## Wrappers

The `wrappers/` subdirectory contains minimal, self-contained scripts that
demonstrate the correct usage of individual API functions. See
[wrappers/README.md](wrappers/README.md) for details.

## Registry

The file `registry.json` tracks all verified API functions across all scripts.
Query it via the `query_function_registry` MCP tool, or inspect the JSON directly.
