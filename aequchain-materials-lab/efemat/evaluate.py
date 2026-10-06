"""efemat.evaluate — EFE pillar scoring, ladder classification, risk classes.

EFE Filter: seven sustainable-design pillars, corpus-aligned seed
([CONFIGURABLE] in data/pillars.json). Scores are seeded per-material
as [SEED-ESTIMATE] pending measured data — the environment never
presents them as measured.

Four-Rung Materials Ladder (doctrine):
    1 SUBSTITUTE | 2 REDESIGN | 3 CLOSE-LOOP RECYCLE | 4 TRACK EVERY GRAM
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

RUNG_LABELS: Dict[int, str] = {
    1: "SUBSTITUTE",
    2: "REDESIGN",
    3: "CLOSE-LOOP RECYCLE",
    4: "TRACK EVERY GRAM",
}

# Risk severity classes: likelihood x impact on a 1-5 x 1-5 grid.
RISK_CLASSES: List[Tuple[int, str]] = [
    (20, "CRITICAL"),
    (12, "HIGH"),
    (7, "MEDIUM"),
    (0, "LOW"),
]


def _grade_bands(pillars: Dict[str, Any]) -> List[Tuple[int, str]]:
    bands = pillars.get("grade_bands") or [[90, "A+"], [80, "A"], [70, "B"], [60, "C"], [50, "D"], [0, "E"]]
    return [(int(b[0]), str(b[1])) for b in bands]


def efe_score(
    material: Dict[str, Any],
    pillars: Dict[str, Any],
) -> Dict[str, Any]:
    """Weighted seven-pillar score -> 0-100 + grade + weakest pillar."""
    weights: Dict[str, float] = pillars.get("weights", {})
    seed: Dict[str, Any] = material.get("efe_seed", {})

    per_pillar: Dict[str, float] = {}
    weighted_sum = 0.0
    weight_total = 0.0
    for pillar, weight in weights.items():
        score = float(seed.get(pillar, 5.0))  # missing pillar -> neutral 5
        per_pillar[pillar] = score
        weighted_sum += score * float(weight)
        weight_total += float(weight)

    score100 = (weighted_sum / weight_total) * 10.0 if weight_total else 0.0

    grade = "E"
    for threshold, label in _grade_bands(pillars):
        if score100 >= threshold:
            grade = label
            break

    weakest = min(per_pillar, key=per_pillar.get) if per_pillar else None
    strongest = max(per_pillar, key=per_pillar.get) if per_pillar else None

    return {
        "id": material.get("id", "?"),
        "score": round(score100, 1),
        "grade": grade,
        "per_pillar": per_pillar,
        "weakest_pillar": weakest,
        "strongest_pillar": strongest,
        "basis": "[SEED-ESTIMATE] pending measured data",
    }


def ladder_info(material: Dict[str, Any]) -> Dict[str, Any]:
    """Four-Rung Ladder classification for a material."""
    lad = material.get("ladder") or {"primary": 3, "supporting": []}
    primary = int(lad.get("primary", 3))
    supporting = [int(r) for r in lad.get("supporting", [])]
    return {
        "id": material.get("id", "?"),
        "primary_rung": primary,
        "primary_label": RUNG_LABELS.get(primary, "?"),
        "supporting_rungs": supporting,
        "supporting_labels": [RUNG_LABELS.get(r, "?") for r in supporting],
    }


def risk_class(material: Dict[str, Any]) -> Dict[str, Any]:
    """Worst-case risk severity for a material (likelihood x impact)."""
    risks: List[Dict[str, Any]] = material.get("risks", [])
    worst: Optional[Dict[str, Any]] = None
    worst_severity = -1
    for r in risks:
        severity = int(r.get("likelihood", 1)) * int(r.get("impact", 1))
        if severity > worst_severity:
            worst_severity = severity
            worst = {**r, "severity": severity}

    label = "NONE"
    for threshold, name in RISK_CLASSES:
        if worst_severity >= threshold:
            label = name
            break

    return {
        "id": material.get("id", "?"),
        "n_risks": len(risks),
        "worst": worst,
        "worst_severity": worst_severity if worst else 0,
        "class": label,
    }
