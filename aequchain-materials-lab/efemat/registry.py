"""efemat.registry — JSON-backed material, process, and pillar registries.

Data backbone: versioned JSON files (human+agent editable, diffable,
round-trippable). Behaviour is data: edit a JSON file and every
simulation, evaluation, and generated study changes accordingly —
no code changes (PROGRAMMABLE gate).

Schema (materials.json):
    id, name, class ('replenishable'|'baseline'), category, status,
    carbon_fraction, composition?, component_carbon?, feedstock_shares?,
    density_g_cm3, tensile_mpa (scalar or [lo,hi]), cultivation{},
    processing_energy_mj_kg (scalar or [lo,hi]), permanence,
    soil_carbon_credit?, lca_override?, cost{}, loop{}, applications[],
    eol_stream, ladder{}, efe_seed{}, risks[], sources[]

Required fields are enforced by validate() (TESTABLE gate).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent / "data"

REQUIRED_MATERIAL_FIELDS: Tuple[str, ...] = (
    "id",
    "name",
    "class",
    "category",
    "status",
    "carbon_fraction",
    "efe_seed",
    "risks",
    "sources",
)

# At least one field of each pair must be present.
MATERIAL_ALTERNATIVES: Tuple[Tuple[str, str], ...] = (
    ("processing_energy_mj_kg", "lca_override"),
)

REQUIRED_PROCESS_FIELDS: Tuple[str, ...] = (
    "id",
    "name",
    "stage",
    "status",
    "inputs",
    "outputs",
    "energy_mj_kg",
)


def _load_json(path: Path) -> Dict[str, Any]:
    """Read a JSON file with a helpful error on failure."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError as exc:  # pragma: no cover - path misuse
        raise FileNotFoundError(f"registry file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def as_range(value: Any) -> Optional[Tuple[float, float]]:
    """Normalize a scalar or [lo, hi] literal to a (lo, hi) tuple."""
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        if len(value) != 2:
            raise ValueError(f"range literal must be [lo, hi], got {value!r}")
        lo, hi = float(value[0]), float(value[1])
        if lo > hi:
            lo, hi = hi, lo
        return (lo, hi)
    v = float(value)
    return (v, v)


def mid(value: Any) -> Optional[float]:
    """Midpoint of a scalar-or-range value (None stays None)."""
    rng = as_range(value)
    return None if rng is None else (rng[0] + rng[1]) / 2.0


class Registry:
    """Generic id -> record registry with schema validation."""

    def __init__(
        self,
        records: List[Dict[str, Any]],
        required: Tuple[str, ...],
        source_path: Path,
        alternatives: Tuple[Tuple[str, str], ...] = (),
    ) -> None:
        self.records: Dict[str, Dict[str, Any]] = {r["id"]: r for r in records}
        self.required = required
        self.source_path = source_path
        self.alternatives = alternatives

    # -- access -----------------------------------------------------------
    def get(self, rid: str) -> Dict[str, Any]:
        if rid not in self.records:
            raise KeyError(f"unknown id {rid!r}; known: {', '.join(sorted(self.records))}")
        return self.records[rid]

    def ids(self) -> List[str]:
        return sorted(self.records)

    def filter(self, **eq: Any) -> List[Dict[str, Any]]:
        """Filter records by exact field equality, e.g. filter(class='baseline')."""
        return [
            r
            for r in self.records.values()
            if all(r.get(k) == v for k, v in eq.items())
        ]

    def by_stage(self, stage: str) -> List[Dict[str, Any]]:
        return [r for r in self.records.values() if r.get("stage") == stage]

    # -- validation (TESTABLE gate) ----------------------------------------
    def validate(self) -> List[str]:
        """Return a list of schema violations (empty list == valid)."""
        errors: List[str] = []
        for rid, rec in self.records.items():
            for field in self.required:
                if field not in rec:
                    errors.append(f"{rid}: missing required field {field!r}")
            for field_a, field_b in self.alternatives:
                if field_a not in rec and field_b not in rec:
                    errors.append(
                        f"{rid}: requires {field_a!r} or {field_b!r} (neither present)"
                    )
        return errors


def load_materials(path: Optional[Path] = None) -> Registry:
    """Load the material registry (replenishables + baselines)."""
    p = Path(path) if path else DATA_DIR / "materials.json"
    data = _load_json(p)
    return Registry(data["materials"], REQUIRED_MATERIAL_FIELDS, p, MATERIAL_ALTERNATIVES)


def load_processes(path: Optional[Path] = None) -> Registry:
    """Load the process registry (cultivation | generation | manufacture)."""
    p = Path(path) if path else DATA_DIR / "processes.json"
    data = _load_json(p)
    return Registry(data["processes"], REQUIRED_PROCESS_FIELDS, p)


def load_pillars(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load the EFE pillar configuration (weights, definitions, grade bands)."""
    p = Path(path) if path else DATA_DIR / "pillars.json"
    return _load_json(p)
