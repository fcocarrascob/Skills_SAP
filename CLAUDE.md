# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Skills_SAP** is a SAP2000 automation framework that bridges GitHub Copilot to SAP2000 structural analysis software via Model Context Protocol (MCP) and COM automation. It enables engineers to generate structural models, assign loads, run analyses, and extract results programmatically through conversational AI.

Architecture: User → GitHub Copilot → MCP Server (Python) → SAP2000 COM objects → Results

## Core Architecture

### MCP Server Layer (`mcp_server/`)

The server exposes 12 MCP tools that Copilot invokes. Key modules:

- **`server.py`** — FastMCP entry point; registers all tools with `.mcp.tool()` decorator
- **`sap_bridge.py`** — Singleton COM connection manager to SAP2000; handles connection/disconnection and version detection
- **`sap_executor.py`** — Executes API functions and scripts in restricted sandbox (blocked imports: `os`, `subprocess`, `sys`, `pathlib`, `socket`, etc.; timeout: 120s). Navigates COM object hierarchy via dot-path resolution
- **`script_library.py`** — Persists executed scripts to `scripts/` with metadata headers; enables script search/reload
- **`doc_search.py`** — Full-text search over API documentation files in `API/` directory
- **`function_registry.py`** — Manages `scripts/registry.json` (catalog of 200+ verified functions); tracks verification status, wrapper scripts, and usage metadata

### Script Execution Model

Scripts passed to `run_sap_script` run in restricted Python environment with **pre-injected variables**:
- `SapModel` — Active model COM object
- `SapObject` — SAP2000 application COM object
- `result` — Dict for writing output (for verification)
- `sap_temp_dir` — Temp directory for `File.Save()` calls

All scripts follow the **Universal Pattern**:
1. Initialize model (`InitializeNewModel`, `NewBlank`)
2. Define materials (`PropMaterial.SetMaterial`, `SetMPIsotropic`)
3. Define sections (`PropFrame.Set*`, `PropArea.SetShell_1`)
4. Create geometry (`FrameObj.AddByCoord`, `AreaObj.AddByCoord`)
5. Add constraints (`PointObj.SetRestraint`, `ConstraintDef.*`)
6. Add loads (`LoadPatterns.Add`, `SetLoadDistributed`)
7. Run analysis (`File.Save`, `Analyze.RunAnalysis`)
8. Extract results (`Results.JointDispl`, `Results.AreaForceShell`)
9. Verify with assertions and populate `result`

### Function Registry Organization

**`scripts/registry.json`** tracks 200 verified functions across **22 categories**:
- File, PropMaterial, PropFrame, PropArea, Properties
- FrameObj, AreaObj, Object_Model
- Load_Patterns, Load_Cases, RespCombo
- Constraints, Groups, Design
- Analyze, Analysis_Results
- Database_Tables, Edit, Functions, Mass_Source, Select

Each entry includes: category, description, verification status, wrapper script path, usage notes.

### ByRef Convention (Critical)

SAP2000 API heavily uses ByRef parameters. In Python via COM, functions return **tuples** where:
- All ByRef outputs appear **first**
- Last element `raw[-1]` is **always the return code** (Long)
- Return code 0 = success, nonzero = error

**Pattern:**
```python
raw = SapModel.PointObj.AddCartesian(5, 3, 2, "", "PT1")
point_name = raw[0]   # ByRef Name output
ret_code = raw[-1]    # return code (ALWAYS last)
assert ret_code == 0, f"AddCartesian failed: {ret_code}"
```

Verified layouts in `scripts/registry.json` and documented in `.github/skills/sap2000-api/references/enum-reference.md`.

## Development Commands

### Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r mcp_server/requirements.txt
```

### Running the MCP Server

**Manual test (for debugging):**
```bash
python mcp_server/server.py
```

**Automatic (via VS Code):** Configured in `.vscode/mcp.json`; server auto-starts when Copilot invokes MCP tools.

### Running Scripts

Scripts are executed via `run_sap_script` MCP tool. Example wrappers in `scripts/wrappers/func_*.py` demonstrate usage of individual API functions.

To test a wrapper manually (requires SAP2000 running):
```python
# Within VS Code with MCP bridge:
# Use: run_sap_script tool with code from scripts/wrappers/func_FrameObj_AddByCoord.py
```

### Testing

Unit tests live in `mcp_server/tests/`. Run with pytest:
```bash
cd mcp_server
pytest tests/ -v
```

## Important Files & Their Roles

### Documentation
- **`README.md`** — Project overview, architecture diagram, component summary
- **`.github/copilot-instructions.md`** — Copilot-facing instructions; tool mapping; when to use agent vs. skill
- **`.github/agents/sap2000-scripter.agent.md`** — Copilot agent workflow (research → plan → code → execute → verify → save)
- **`.github/skills/sap2000-api/SKILL.md`** — API technical reference (ByRef layouts, templates, registry patterns)
- **`.github/skills/sap2000-api/references/common-workflows.md`** — Step-by-step patterns (simple beam, portal frame, verification problem)
- **`scripts/README.md`** — Script library usage
- **`scripts/wrappers/README.md`** — Wrapper script naming and format
- **`scripts/database_tables/README.md`** — Database Tables module backend + GUI API

### Examples & Notebooks
- **`scripts/example_1001_simple_beam.py`** — End-to-end verification (beam analysis with hand-calculated comparison)
- **`scripts/example_ring_areas_parametric.py`** — Parametric geometry (circular ring with 3 zones)
- **`scripts/modelo_complejo_mixto.py`** — Complex industrial model (columns, beams, braces, slabs, seismic analysis)
- **`scripts/domo_elipsoidal_parametrico_py.py`** — Double-curved dome geometry
- **`scripts/CASE_COMBO.ipynb`** — Jupyter notebook for load case and combination management workflows

### In-Development Features
- **`scripts/section_cut/`** — Section Cut automation (branch: `feat/section_cut`); research in `SECTION_CUTS_RESEARCH.md`. Section cuts compute resultant forces/moments across any plane — used for story shear, wall design forces, and free-body equilibrium checks. API: `SapModel.Definitions.SectionCuts.*`, results via `SapModel.Results.SectionCut.*`.

### Configuration
- **`.vscode/mcp.json`** — MCP server configuration; Python venv path; auto-start settings
- **`.claude/settings.local.json`** — Local Claude Code settings (permissions allowlist)
- **`scripts/registry.json`** — Verified function catalog (DO NOT edit directly; use `register_verified_function` tool)

## Key Conventions & Rules

### NEVER

1. **Edit `scripts/registry.json` directly** — The MCP server caches in memory and overwrites manual edits. Always use `register_verified_function` tool after successful `run_sap_script`.

2. **Create pre-injected variables in scripts** — Do not define `SapModel`, `SapObject`, `result`, or `sap_temp_dir`; they are auto-injected.

3. **Import blocked modules** — Sandbox blocks: `os`, `subprocess`, `sys`, `shutil`, `pathlib`, `importlib`, `socket`, `http`, `urllib`, `ctypes`, `pickle`. Allowed: `math`, `json`, `datetime`, `decimal`, `fractions`, `collections`, `itertools`, `functools`, `typing`.

4. **Hardcode file paths** — Use `sap_temp_dir + r"\filename.sdb"` for `File.Save()`.

5. **Assume verified=true has wrapper** — Check the `wrapper_script` field in registry entry.

### ALWAYS

1. **Query `query_function_registry` before writing API calls** — Verify function exists, check ByRef layout, find wrapper if available.

2. **Copy wrapper code verbatim** — If wrapper exists, load it with `load_script` and reuse the exact API call pattern.

3. **Assert return codes: `assert raw[-1] == 0`** — Every API call must check return code.

4. **Use `sap_temp_dir` for model paths** — Never hardcode paths; e.g., `SapModel.File.Save(sap_temp_dir + r"\model.sdb")`.

5. **Populate `result` dict with key outputs** — Write values for verification/debugging.

6. **Register after success** — Only call `register_verified_function` AFTER `run_sap_script` succeeds for new functions.

7. **Follow the Universal Pattern** — All scripts follow the 9-phase sequence (Init → Materials → Sections → Geometry → Constraints → Loads → Analysis → Results → Verify).

## Wrapper Script Location & Purpose

**Path:** `scripts/wrappers/func_{ObjectName}_{FunctionName}.py`

Each wrapper:
- Targets **one** API function
- Sets up all prerequisites (model, materials, sections)
- Calls the function and asserts success
- Writes verification output to `result`
- Includes metadata header with category, description, verification date

**127 wrappers** currently documented; covers all 21 API categories.

## GUI Applications

Five standalone PySide6 applications in `scripts/`:
- **`modelo_base/`** — Model base generator (materials, load patterns, sections, spectra)
- **`placabase/`** — Parametric base plate generator (bolts, anchor chair, Winkler springs)
- **`ring_areas/`** — Circular ring generator (parametric zones)
- **`database_tables/`** — SAP2000 database table browser (read, edit, export CSV/XML)
- **`post_proceso/`** — Results extractor (joint displacements, area shell forces)

Each uses worker threads for async operation without blocking UI.

## Copilot Workflow (Agent: @sap2000-scripter)

When using the agent, follow this sequence:

1. **Research (conditional)** — Triggered if script uses unverified API functions, complex analysis, or parametric geometry. Uses Explore subagent.

2. **Plan** — Decompose into 9 phases; identify which functions are verified vs. unverified; consult registry.

3. **Code Generation** — Generate script following Universal Pattern; use wrappers as templates.

4. **Execution** — Run `run_sap_script`; check return codes.

5. **Verification** — Confirm output in `result` dict; compare against hand calculations if applicable.

6. **Registration** — Call `register_verified_function` for any new functions discovered.

7. **Save** — Script auto-saves on success via `save_script`.

8. **GUI Offer** — Agent offers to generate standalone GUI if workflow is complete.

## Common Queries

### "How do I find a verified function?"

```python
# Query registry for specific function
query_function_registry(function_path="SapModel.FrameObj.AddByCoord")

# Search by keyword
query_function_registry(query="beam")

# Get summary
query_function_registry()
```

### "What's the ByRef layout for X function?"

1. Check `scripts/registry.json` for the function
2. Look at `verified` entry and consult `wrapper_script` path
3. Load the wrapper with `load_script(name)`
4. Study how return values are unpacked

### "How do I add a new API function to the registry?"

1. Write script using the function via `run_sap_script`
2. After success, call `register_verified_function` with full metadata
3. Include category, description, wrapper script path, ByRef layout

### "What imports are allowed in scripts?"

Allowed: `math`, `json`, `datetime`, `decimal`, `fractions`, `collections`, `itertools`, `functools`, `typing`

Blocked: `os`, `subprocess`, `sys`, `shutil`, `pathlib`, `socket`, `http`, `urllib`, `importlib`, `ctypes`, `pickle`

## References

- **MCP Protocol:** https://modelcontextprotocol.io
- **SAP2000 API:** Covered in 25+ markdown files in `API/` directory
- **COM Bridge Details:** `mcp_server/sap_bridge.py` (connection management)
- **Sandbox Details:** `mcp_server/sap_executor.py` (restriction enforcement)
