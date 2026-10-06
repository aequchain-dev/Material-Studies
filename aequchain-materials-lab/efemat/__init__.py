"""efemat — EFE Materials Environment Toolkit.

Simulate, evaluate, synthesize, prototype, detail, and research
sustainable EFE-compliant materials for the aequchain program.

Doctrine (Four-Rung Materials Ladder):
    1. SUBSTITUTE         eliminate demand for the critical material
    2. REDESIGN           change the machine so the substitute suffices
    3. CLOSE-LOOP RECYCLE one industrial metabolism: E4 -> E1 -> product
    4. TRACK EVERY GRAM   NFC passports, isotope verification, on-chain

Dev policy: extensible | modular | scriptable | programmable | scalable |
reliable | robust | refined | replicable.
Stdlib-only by design: zero third-party dependencies, runs anywhere >=3.9.

Data backbone: versioned JSON registries (human+agent editable, diffable).
Simulation fidelity: hybrid — deterministic analytic core + seeded
Monte-Carlo uncertainty layer (reproducible via fixed seed).
"""

__version__ = "1.0.0"

from .registry import Registry, load_materials, load_processes, load_pillars
from . import simulate, evaluate, synthesize, prototype, research, detail

__all__ = [
    "Registry",
    "load_materials",
    "load_processes",
    "load_pillars",
    "simulate",
    "evaluate",
    "synthesize",
    "prototype",
    "research",
    "detail",
    "__version__",
]
