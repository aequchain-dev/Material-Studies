"""efemat.research — corpus search + web-search adapter protocol.

Two research surrounds:
1. corpus_search — local full-corpus keyword search across the material
   flow studies and the aequchain corpus files. Zero dependencies,
   deterministic, agent-friendly (file + line + text).
2. web_search_protocol — the documented contract for agent-side web
   search. The environment itself never calls the network; an agent
   (or human) runs the search and pipes results back in. This keeps
   the package offline-reliable while remaining research-capable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

# Projects root: efemat/research.py -> efemat -> lab -> projects
PROJECTS_ROOT: Path = Path(__file__).resolve().parents[2]

STUDIES_DIR_NAME: str = "aequchain material flow studies"

# Corpus files searched alongside the studies (top-level corpus).
CORPUS_FILES: List[str] = [
    "aequcity.md",
    "aequvivum.md",
    "evermateria.md",
    "aequmoto.md",
    "aequphone.md",
    "aequscaff.md",
    "aequgen omege.md",
    "aquegen omega.md",
    "aequvivium.md",
]


def _search_paths(root: Path) -> List[Path]:
    paths: List[Path] = []
    studies = root / STUDIES_DIR_NAME
    if studies.is_dir():
        paths.extend(sorted(studies.glob("*.md")))
    for name in CORPUS_FILES:
        candidate = root / name
        if candidate.is_file():
            paths.append(candidate)
    return paths


def corpus_search(
    query: str,
    root: Optional[Path] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Case-insensitive substring search across the local corpus.

    Returns [{file, line_no, text}, ...] capped at `limit`.
    """
    base = Path(root) if root else PROJECTS_ROOT
    needle = query.lower()
    matches: List[Dict[str, Any]] = []
    for path in _search_paths(base):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if needle in line.lower():
                matches.append(
                    {
                        "file": str(path.relative_to(base)),
                        "line_no": line_no,
                        "text": line.strip()[:240],
                    }
                )
                if len(matches) >= limit:
                    return matches
    return matches


def web_search_protocol(query: str) -> Dict[str, Any]:
    """The documented agent-side web-search contract (offline-safe).

    Protocol:
      1. Agent runs its own web-search tool for `query`.
      2. Agent saves results as JSON: [{"title", "url", "content"}, ...]
         to a file.
      3. Agent/human re-runs the pipeline with the file as input
         (e.g. efemat research web --results-file path.json).
    The package itself performs zero network calls (RELIABLE gate).
    """
    return {
        "protocol": "efemat-web-search/1.0",
        "query": query,
        "steps": [
            "agent executes web search for the query",
            "agent writes JSON array [{title, url, content}, ...] to a file",
            "results are consumed downstream (study generation, registry updates)",
        ],
        "results_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "fields": ["title", "url", "content"],
            },
        },
        "network_calls_by_package": 0,
    }
