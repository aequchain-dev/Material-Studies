"""efemat.prototype — process spec cards from the process registry.

Renders a cultivation/generation/manufacture process as a structured,
human+agent readable spec card. The registry is the source of truth;
this module only formats (MODULAR gate: one concern per unit).
"""

from __future__ import annotations

from typing import Any, Dict, List

from .registry import Registry, as_range, mid


def _fmt_energy(value: Any) -> str:
    rng = as_range(value)
    if rng is None:
        return "n/a"
    if rng[0] == rng[1]:
        return f"{rng[0]:.1f} MJ/kg"
    return f"{rng[0]:.1f}-{rng[1]:.1f} MJ/kg"


def _fmt_params(params: Dict[str, Any], indent: str = "  ") -> List[str]:
    lines = []
    for key, value in params.items():
        if isinstance(value, bool):
            shown = "yes" if value else "no"
        elif isinstance(value, list):
            shown = f"{value[0]}-{value[1]}" if len(value) == 2 and all(
                isinstance(v, (int, float)) for v in value
            ) else ", ".join(str(v) for v in value)
        else:
            shown = str(value)
        lines.append(f"{indent}{key}: {shown}")
    return lines


def process_card(process: Dict[str, Any]) -> str:
    """Format one process record as a spec card."""
    lines = [
        f"=== {process['name']} [{process['id']}] ===",
        f"  stage     : {process['stage']}",
        f"  status    : [{process['status']}]",
        f"  inputs    : {', '.join(process.get('inputs', []))}",
        f"  outputs   : {', '.join(process.get('outputs', []))}",
        f"  energy    : {_fmt_energy(process.get('energy_mj_kg'))}",
        f"  throughput: {process.get('throughput', 'n/a')}",
        "  key params:",
    ]
    lines += _fmt_params(process.get("key_params", {}))
    lines.append(f"  EFE notes : {process.get('efe_notes', '')}")
    lines.append(f"  sources   : {', '.join(process.get('sources', []))}")
    return "\n".join(lines)


def stage_cards(processes: Registry, stage: str) -> List[str]:
    """Cards for every process in one stage (cultivation|generation|manufacture)."""
    return [process_card(p) for p in processes.by_stage(stage)]
