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
