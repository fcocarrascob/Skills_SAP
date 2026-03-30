"""
SAP2000 Function Registry — Catalog of verified API functions.

Tracks which SAP2000 API functions have been verified, in which scripts
they are used, and provides search/filter capabilities for the agent.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# registry.json lives in scripts/ at the workspace root
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "scripts" / "registry.json"

_EMPTY_REGISTRY = {
    "version": "1.0",
    "functions": {},
    "summary": {
        "total_registered": 0,
        "total_verified": 0,
        "last_updated": None,
    },
}


class FunctionRegistry:
    """
    Manages a JSON file that catalogs verified SAP2000 API functions.

    Each function entry records its category, description, verification
    status, wrapper script, and which user scripts use it.
    """

    def __init__(self, registry_path: Path | None = None):
        self._path = registry_path or REGISTRY_PATH
        self._data: dict | None = None
        self._last_mtime: float = 0

    # ── Persistence ───────────────────────────────────────────────────

    def _reload_if_changed(self) -> None:
        """Reload from disk if the file was modified externally."""
        if self._data is None:
            return
        try:
            disk_mtime = self._path.stat().st_mtime
            if disk_mtime > self._last_mtime:
                self._data = None  # Force full reload on next _load()
        except OSError:
            pass

    def _load(self) -> dict:
        """Load the registry, respecting external disk changes."""
        self._reload_if_changed()
        if self._data is not None:
            return self._data

        if self._path.exists():
            try:
                self._data = json.loads(self._path.read_text(encoding="utf-8"))
                self._last_mtime = self._path.stat().st_mtime
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to read registry, starting empty: %s", exc)
                self._data = json.loads(json.dumps(_EMPTY_REGISTRY))
                self._last_mtime = 0
        else:
            self._data = json.loads(json.dumps(_EMPTY_REGISTRY))
            self._last_mtime = 0

        return self._data

    def _save(self) -> None:
        """Persist the registry atomically (write to tmp then rename)."""
        data = self._load()
        self._update_summary(data)

        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._path.with_suffix(".tmp")
        try:
            tmp_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False, default=str),
                encoding="utf-8",
            )
            tmp_path.replace(self._path)
            # Update mtime after successful write to avoid unnecessary reload
            self._last_mtime = self._path.stat().st_mtime
        except OSError as exc:
            logger.exception("Failed to save registry: %s", exc)
            raise

    @staticmethod
    def _update_summary(data: dict) -> None:
        """Recompute the summary counters."""
        funcs = data.get("functions", {})
        data["summary"] = {
            "total_registered": len(funcs),
            "total_verified": sum(1 for f in funcs.values() if f.get("verified")),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    # ── Public API ────────────────────────────────────────────────────

    def register_function(
        self,
        function_path: str,
        category: str,
        description: str = "",
        signature: str = "",
        wrapper_script: str = "",
        parameter_notes: str = "",
        notes: str = "",
    ) -> dict:
        """
        Register a new function or update an existing one.

        Parameters
        ----------
        function_path : str
            Dot-path like "SapModel.FrameObj.AddByCoord".
        category : str
            API category (e.g. "Object_Model", "Properties").
        description : str
            Human-readable description.
        signature : str
            VB6/API signature string.
        wrapper_script : str
            Name of the wrapper script (without .py).
        parameter_notes : str
            Brief notes about parameters.
        notes : str
            Extra notes (e.g. ByRef layout).

        Returns
        -------
        dict  {registered: True, function_path, is_new}
        """
        data = self._load()
        funcs = data.setdefault("functions", {})

        is_new = function_path not in funcs
        now = datetime.now(timezone.utc).isoformat()

        # Determine verification_type based on registration path
        v_type = "wrapper" if wrapper_script else "manual"

        if is_new:
            funcs[function_path] = {
                "category": category,
                "description": description,
                "signature": signature,
                "verified": False,
                "first_verified": None,
                "last_verified": None,
                "verification_count": 0,
                "verification_type": v_type,
                "wrapper_script": wrapper_script,
                "used_in_scripts": [],
                "parameter_notes": parameter_notes,
                "known_errors": [],
                "notes": notes,
            }
        else:
            entry = funcs[function_path]
            if category:
                entry["category"] = category
            if description:
                entry["description"] = description
            if signature:
                entry["signature"] = signature
            if wrapper_script:
                entry["wrapper_script"] = wrapper_script
            if parameter_notes:
                entry["parameter_notes"] = parameter_notes
            if notes:
                entry["notes"] = notes
            # Upgrade verification_type (never downgrade)
            current_type = entry.get("verification_type", "auto")
            type_rank = {"auto": 0, "manual": 1, "wrapper": 2}
            if type_rank.get(v_type, 0) > type_rank.get(current_type, 0):
                entry["verification_type"] = v_type

        self._save()
        return {
            "registered": True,
            "function_path": function_path,
            "is_new": is_new,
        }

    def mark_verified(
        self,
        function_path: str,
        script_name: str = "",
    ) -> dict:
        """
        Mark a function as verified and optionally link it to a script.

        If the function is not yet registered, it is auto-registered with
        minimal metadata.

        Parameters
        ----------
        function_path : str
            Dot-path of the function.
        script_name : str
            Name of the script that verified this function.

        Returns
        -------
        dict  {verified: True, function_path, verification_count}
        """
        data = self._load()
        funcs = data.setdefault("functions", {})

        now = datetime.now(timezone.utc).isoformat()

        if function_path not in funcs:
            funcs[function_path] = {
                "category": "",
                "description": "",
                "signature": "",
                "verified": True,
                "first_verified": now,
                "last_verified": now,
                "verification_count": 1,
                "verification_type": "auto",
                "wrapper_script": "",
                "used_in_scripts": [script_name] if script_name else [],
                "parameter_notes": "",
                "known_errors": [],
                "notes": "",
            }
        else:
            entry = funcs[function_path]
            entry["verified"] = True
            entry["last_verified"] = now
            entry["verification_count"] = entry.get("verification_count", 0) + 1
            if not entry.get("first_verified"):
                entry["first_verified"] = now
            if script_name and script_name not in entry.get("used_in_scripts", []):
                entry.setdefault("used_in_scripts", []).append(script_name)
            # Only set verification_type to "auto" if not already higher
            if not entry.get("verification_type"):
                entry["verification_type"] = "auto"

        self._save()
        return {
            "verified": True,
            "function_path": function_path,
            "verification_count": funcs[function_path]["verification_count"],
        }

    def get_function(self, function_path: str) -> dict:
        """
        Get the full detail of a registered function.

        Returns
        -------
        dict  The function entry, or {error} if not found.
        """
        data = self._load()
        entry = data.get("functions", {}).get(function_path)
        if entry is None:
            return {"error": f"Function '{function_path}' not found in registry."}
        return {"function_path": function_path, **entry}

    def list_functions(
        self,
        category: str | None = None,
        verified_only: bool = False,
        query: str | None = None,
    ) -> list[dict]:
        """
        List functions with optional filters.

        Parameters
        ----------
        category : str | None
            Filter by category (case-insensitive substring match).
        verified_only : bool
            If True, return only verified functions.
        query : str | None
            Keyword search across function_path, description, notes.

        Returns
        -------
        list[dict]  Each dict: {function_path, category, description, verified, verification_count, wrapper_script}
        """
        data = self._load()
        results = []

        for fpath, entry in data.get("functions", {}).items():
            if verified_only and not entry.get("verified"):
                continue
            if category:
                if category.lower() not in entry.get("category", "").lower():
                    continue
            if query:
                q = query.lower()
                searchable = (
                    fpath.lower()
                    + " " + entry.get("description", "").lower()
                    + " " + entry.get("notes", "").lower()
                    + " " + entry.get("parameter_notes", "").lower()
                )
                if q not in searchable:
                    continue

            results.append({
                "function_path": fpath,
                "category": entry.get("category", ""),
                "description": entry.get("description", ""),
                "verified": entry.get("verified", False),
                "verification_count": entry.get("verification_count", 0),
                "verification_type": entry.get("verification_type", "auto"),
                "wrapper_script": entry.get("wrapper_script", ""),
            })

        return results

    def get_summary(self) -> dict:
        """
        Return a coverage summary of the registry.

        Returns
        -------
        dict  {total_registered, total_verified, last_updated, categories}
        """
        data = self._load()
        self._update_summary(data)

        # Count per category
        cat_counts: dict[str, dict] = {}
        for entry in data.get("functions", {}).values():
            cat = entry.get("category", "Uncategorized")
            if cat not in cat_counts:
                cat_counts[cat] = {"registered": 0, "verified": 0}
            cat_counts[cat]["registered"] += 1
            if entry.get("verified"):
                cat_counts[cat]["verified"] += 1

        return {
            **data["summary"],
            "categories": cat_counts,
        }

    def reload(self) -> None:
        """Force reload from disk on next access."""
        self._data = None
        self._last_mtime = 0


# Module-level singleton
registry = FunctionRegistry()
