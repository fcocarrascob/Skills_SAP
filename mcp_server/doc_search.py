"""
SAP2000 API Documentation Search — Keyword search across API/*.md files.

Parses the markdown documentation files and provides search by keyword,
category, or description. Returns relevant snippets with function signatures,
parameters, and examples.
"""

import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# API/ lives at the workspace root, one level up from mcp_server/
API_DIR = Path(__file__).resolve().parent.parent / "API"

# Pre-defined category mapping (filename stem → category label)
CATEGORIES = {
    "Analysis_Model": "Analysis Model",
    "Analysis_Results": "Analysis Results",
    "Analyze": "Analysis Execution",
    "Combinations": "Response Combinations",
    "Constraints": "Joint Constraints",
    "Coordinate_Systems": "Coordinate Systems",
    "Database_Tables": "Database Tables",
    "Definitions": "Definitions",
    "Design": "Design",
    "Edit": "Edit Operations",
    "Example_Code": "Example Code",
    "File": "File Operations",
    "Functions": "Functions (Time History)",
    "General_Functions": "General / Connection",
    "Getting_Started": "Getting Started",
    "Groups": "Groups",
    "Joint_Patterns": "Joint Patterns",
    "Load_Cases": "Load Cases",
    "Load_Patterns": "Load Patterns",
    "Mass_Source": "Mass Source",
    "Object_Model": "Object Model (Geometry)",
    "Options": "Program Options",
    "Properties": "Properties (Materials/Sections)",
    "Select": "Selection",
    "View": "View / Display",
}


class DocIndex:
    """
    In-memory index of all API documentation sections.

    Each section corresponds to a top-level heading (# FunctionName) and
    contains the full text under that heading until the next one.
    """

    def __init__(self):
        self._sections: list[dict] = []
        self._loaded = False

    def _load(self):
        """Parse all API/*.md files into sections."""
        if self._loaded:
            return

        if not API_DIR.is_dir():
            logger.warning("API documentation directory not found: %s", API_DIR)
            self._loaded = True
            return

        for md_file in sorted(API_DIR.glob("*.md")):
            category = CATEGORIES.get(md_file.stem, md_file.stem)
            self._parse_file(md_file, category)

        logger.info("Indexed %d API doc sections.", len(self._sections))
        self._loaded = True

    def _parse_file(self, file_path: Path, category: str):
        """Split a markdown file into sections by top-level heading."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            logger.warning("Could not read %s", file_path)
            return

        # Split on top-level headings (# Title)
        parts = re.split(r"^(?=# )", content, flags=re.MULTILINE)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Extract the heading
            first_line = part.split("\n", 1)[0].strip()
            if first_line.startswith("# "):
                function_name = first_line[2:].strip()
            else:
                function_name = first_line

            # Extract syntax line (e.g., "SapObject.SapModel.FrameObj.AddByCoord")
            syntax = ""
            syntax_match = re.search(
                r"##\s*Syntax\s*\n+(.+?)(?:\n\n|\n##)", part, re.DOTALL
            )
            if syntax_match:
                syntax = syntax_match.group(1).strip()

            # Extract VB6 procedure signature
            signature = ""
            sig_match = re.search(
                r"##\s*VB6 Procedure\s*\n+(.+?)(?:\n\n|\n##)", part, re.DOTALL
            )
            if sig_match:
                signature = sig_match.group(1).strip()

            # Extract parameters section
            params = ""
            params_match = re.search(
                r"##\s*Parameters\s*\n(.+?)(?:\n##)", part, re.DOTALL
            )
            if params_match:
                params = params_match.group(1).strip()

            # Extract remarks
            remarks = ""
            remarks_match = re.search(
                r"##\s*Remarks\s*\n(.+?)(?:\n##)", part, re.DOTALL
            )
            if remarks_match:
                remarks = remarks_match.group(1).strip()

            # Extract VBA example
            example = ""
            example_match = re.search(
                r"##\s*(?:VBA )?Example\s*\n(.+?)(?:\n##|$)", part, re.DOTALL
            )
            if example_match:
                example = example_match.group(1).strip()

            self._sections.append({
                "file": file_path.name,
                "category": category,
                "function_name": function_name,
                "syntax": syntax,
                "signature": signature,
                "parameters": params,
                "remarks": remarks,
                "example_snippet": example[:1500] if example else "",
                "_full_text": part.lower(),  # for search matching
            })

    def search(
        self, query: str, category: str | None = None, max_results: int = 10
    ) -> list[dict]:
        """
        Search the API docs by keyword and optional category.

        Parameters
        ----------
        query : str
            Keywords to search for (case-insensitive). Matched against
            function name, syntax, signature, parameters, and remarks.
        category : str | None
            Restrict search to a specific file/category.
            Can be a filename stem (e.g. "File", "Object_Model") or
            a category label (e.g. "File Operations").
        max_results : int
            Maximum number of results to return.

        Returns
        -------
        list[dict]  Each with: file, category, function_name, syntax,
                    signature, parameters (truncated), remarks (truncated),
                    example_snippet (truncated)
        """
        self._load()

        query_lower = query.lower()
        query_terms = query_lower.split()
        scored: list[tuple[int, dict]] = []

        for section in self._sections:
            # Category filter
            if category:
                cat_lower = category.lower().replace("_", " ")
                if (
                    cat_lower not in section["category"].lower()
                    and cat_lower not in section["file"].lower().replace("_", " ")
                ):
                    continue

            # Score: how many query terms appear in the section
            score = 0
            for term in query_terms:
                # Higher weight for function name match
                if term in section["function_name"].lower():
                    score += 5
                if term in section["syntax"].lower():
                    score += 3
                if term in section["signature"].lower():
                    score += 2
                if term in section["_full_text"]:
                    score += 1

            if score > 0:
                # Return a clean copy without the internal search field
                result = {k: v for k, v in section.items() if not k.startswith("_")}
                # Truncate long fields
                if len(result.get("parameters", "")) > 800:
                    result["parameters"] = result["parameters"][:800] + "\n..."
                if len(result.get("remarks", "")) > 500:
                    result["remarks"] = result["remarks"][:500] + "\n..."
                scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:max_results]]

    def list_categories(self) -> list[dict]:
        """Return available categories with section counts."""
        self._load()
        cat_counts: dict[str, int] = {}
        for section in self._sections:
            cat = section["category"]
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        return [{"category": k, "sections": v} for k, v in sorted(cat_counts.items())]


# Module-level singleton
doc_index = DocIndex()
