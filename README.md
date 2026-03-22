# SAP2000 AI-Assisted Framework

> **Framework for creating verified Python applications for SAP2000 structural analysis via AI assistance.**

This repository provides a complete environment for generating, executing, and verifying SAP2000 automation scripts using GitHub Copilot as an AI coding assistant. The MCP (Model Context Protocol) server connects Copilot directly to your local SAP2000 instance, enabling an iterative workflow where AI-generated scripts are executed, verified, and saved to a growing library of reusable, tested code.

---

## What This Framework Does

- **Connects Copilot to SAP2000** via a local COM bridge, so the AI can run and test scripts in real time.
- **Verifies every script** by executing it against a live SAP2000 instance and checking return codes.
- **Builds a library of verified scripts** that can be reused, composed, and adapted for new tasks.
- **Tracks verified API functions** in a registry, so already-proven call signatures are never re-guessed.
- **Provides AI with structured context** — 25 API documentation files, pattern references, enum values, and verified wrapper scripts — reducing hallucination and increasing correctness.

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | Windows (SAP2000 only runs on Windows) |
| **Python** | 3.10 or newer |
| **SAP2000** | Any version with API support installed locally |
| **VS Code** | With GitHub Copilot (agent mode) |

---

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/fcocarrascob/Skills_SAP.git
cd Skills_SAP

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows

# Install dependencies
pip install -r mcp_server/requirements.txt
```

### 2. Configure VS Code

The MCP server is already configured in `.vscode/mcp.json`. Open the project in VS Code with Copilot enabled — the server starts automatically when Copilot needs it.

### 3. Start a SAP2000 session with Copilot

Open GitHub Copilot chat in agent mode and type:

```
@sap2000 Create a simple 2-story steel frame and run a dead load analysis
```

Copilot will:
1. Connect to SAP2000 (or launch it)
2. Check the function registry for verified functions
3. Generate a Python script using verified patterns
4. Execute it against the live SAP2000 instance
5. Verify results and save the script to the library

---

## Architecture

```
Skills_SAP/
├── mcp_server/                # MCP server (core of the framework)
│   ├── server.py              # Tool definitions — entry point
│   ├── sap_bridge.py          # COM connection manager (singleton)
│   ├── sap_executor.py        # Script sandbox + function executor
│   ├── script_library.py      # Persistent script library
│   ├── doc_search.py          # API documentation search engine
│   ├── function_registry.py   # Verified function catalog
│   └── tests/                 # Unit and integration tests
├── scripts/                   # Auto-managed script library
│   ├── registry.json          # Verified function registry (JSON)
│   └── wrappers/              # 30+ single-function wrapper scripts
├── API/                       # SAP2000 API documentation (25 Markdown files)
├── .github/
│   ├── skills/sap2000-api/    # Copilot skill definition + references
│   └── prompts/               # Structured autonomy prompts
└── .vscode/mcp.json           # MCP server configuration
```

---

## MCP Tools

The MCP server exposes these tools to Copilot:

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

---

## The Verification Workflow

The core idea of this framework is **iterative verification**:

```
1. check registry  →  2. load wrapper/script  →  3. generate script
        ↑                                               ↓
6. save to library  ←  5. register functions  ←  4. execute & verify
```

Every script that successfully executes against SAP2000:
- Is saved to `scripts/` for future reuse
- Has its API function calls automatically registered in `scripts/registry.json`
- Can be used as a building block for more complex models

---

## Script Sandbox

Scripts run in a restricted Python environment for safety:

- **Pre-injected variables:** `SapModel`, `SapObject`, `result` (dict)
- **Allowed imports:** `math`, `json`, `datetime`, `decimal`, `fractions`, `collections`, `itertools`, `functools`, `typing`
- **Blocked:** `os`, `subprocess`, `sys`, `shutil`, `pathlib`, `socket`, `http`, `urllib`, `importlib`, `ctypes`, `pickle`, file I/O
- **Timeout:** 120 seconds

---

## Function Registry

The function registry (`scripts/registry.json`) tracks every SAP2000 API function that has been successfully tested. Before generating a new script, Copilot checks this registry to reuse proven call signatures and avoid re-discovering ByRef conventions.

```bash
# Query via Copilot:
# "Which frame functions are already verified?"
# → query_function_registry(category="Object_Model", verified_only=True)
```

---

## Wrapper Scripts

The `scripts/wrappers/` directory contains 30+ minimal, self-contained scripts that each demonstrate one SAP2000 API function. These are the **single source of truth** for:
- Argument count and order (COM bridge vs. VBA docs can differ)
- ByRef output parameter layout
- Return code conventions

See [scripts/README.md](scripts/README.md) for details.

---

## Running Tests

Unit tests (no SAP2000 required):

```bash
cd mcp_server
python -m pytest tests/test_function_registry.py tests/test_bridge.py -v
```

Integration tests (Windows + SAP2000 required):

```bash
cd mcp_server
python -m pytest tests/test_bridge.py -v -k "Integration"
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new wrapper scripts, API documentation, and framework improvements.

---

## License

This project is open source. See repository license for details.
