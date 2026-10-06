# aequchain-materials-lab

**`efemat` — EFE Materials Environment Toolkit.** Simulate, evaluate, synthesize, prototype, detail, and research sustainable EFE-compliant materials for the aequchain program. Stdlib-only Python (>=3.9, zero dependencies), JSON data backbone, hybrid simulation fidelity (deterministic analytic core + seeded Monte-Carlo uncertainty layer).

**Doctrine (Four-Rung Materials Ladder):** SUBSTITUTE → REDESIGN → CLOSE-LOOP RECYCLE → TRACK EVERY GRAM.

---

## Quickstart

```bash
cd aequchain-materials-lab

# tests (24) — all green, mutation-checked
python3 -m unittest discover -s tests -t . -v

# explore
python3 -m efemat registry list --value replenishable
python3 -m efemat registry show dlgc
python3 -m efemat registry validate

# simulate
python3 -m efemat simulate lca dlgc                 # carbon accounting
python3 -m efemat simulate compare                  # full LCA table
python3 -m efemat simulate cost dlgc --years 20     # EFE cost curve
python3 -m efemat simulate loop dlgc                # secondary-supply saturation
python3 -m efemat simulate land dlgc --demand 1150000   # hectares per feedstock
python3 -m efemat calculate ledger --demand 1150000    # one number in, every resource out
python3 -m efemat calculate mix --demand 1150000       # fiber-mix scenarios (the mix lever)
python3 -m efemat calculate scale --from 10000 --to 1150000 --years 12  # 1x -> 100x evidence
python3 -m efemat simulate mc dlgc --n 2000         # Monte-Carlo band (seeded)

# evaluate
python3 -m efemat evaluate efe dlgc     # seven-pillar score + grade
python3 -m efemat evaluate ladder dlgc   # four-rung classification
python3 -m efemat evaluate risk dlgc     # worst-case risk class

# synthesize
python3 -m efemat synthesize composite --cellulose 0.52 --lignin 0.38 --graphene 0.05 --additives 0.05
python3 -m efemat synthesize calibrate  # reproduce corpus DLGC spec (honest gaps flagged)

# prototype + research
python3 -m efemat prototype card solar_thermal_pultrusion
python3 -m efemat research corpus "DLGC"            # local corpus search
python3 -m efemat research web "hemp yield"         # agent-side web protocol

# detail — the deliverable generator
python3 -m efemat detail scoresheet dlgc
python3 -m efemat detail study      # regenerates the Replenishable Materials study
```

Most data commands accept `--json` for machine-readable output (AUTOMATABLE).

---

## Architecture (one concern per module — MODULAR gate)

```
efemat/
  registry.py     JSON registries: materials (29), processes (26), pillars (7)
  simulate.py     LCA · cost trajectory · loop dynamics · land ledger ·
                  footprint ledger (farmplex stacking) · power ledger
                  (atmospheric family) · Monte-Carlo
  calculators.py  CALCULATORS | SCALABILITY framework: mix ledger (the mix
                  lever) · unified resource ledger · year-by-year scaling
                  path (1x -> 100x evidence)
  evaluate.py     EFE seven-pillar scoring · ladder classification · risk classes
  synthesize.py   rule-of-mixtures composite synthesis + corpus calibration
  prototype.py    process spec cards (cultivation | generation | manufacture)
  research.py     corpus search + agent-side web-search protocol (0 network calls)
  detail.py       study + scoresheet GENERATION (the study is an artifact of the data)
  cli.py          every capability a named command (SCRIPTABLE gate)
  data/
    materials.json   22 replenishables (21 biological incl. thanceln glazing
                     + cil_diamond atmospheric) + 7 baselines, status-tagged
    processes.json   12 cultivation (incl. AEQUACROP + AEQUIGROW CEA product
                     pair, OPTIBEST-certified corpus blueprints) · 8 generation ·
                     6 manufacture processes
    pillars.json     EFE weights + definitions ([CONFIGURABLE])
tests/            mutation-checked (TEST THE TESTS)
```

## Simulation models (documented, no hidden constants)

| Model | Equation | Notes |
|---|---|---|
| Biogenic uptake | `sum(f_i · C_i) · 44/12` | composition-weighted stoichiometry |
| Net carbon | `E_proc · grid − uptake · permanence − soil_credit` | renewable grid 0.02, world 0.11 kg CO₂/MJ |
| Cost trajectory | piecewise-linear through EFE anchors | premium → parity → discount → minimal → free |
| Loop dynamics | `secondary(t) = recovery·(1−e^(−t/τ))` | first-order saturation; years-to-target solved |
| Land ledger | `ha_i = demand·fiber_share·feed_share_i / (yield_i·utilization)` | the fields-vs-factory answer |
| Composite | `σ = densification·alignment·Σ(V_i·σ_i)` | factors declared, never hidden |
| Monte-Carlo | seeded sampling of energy ±20%, C ±10%, permanence ±5% | reproducible: same seed → same band |

**Calibration showcase (honesty pattern):** `synthesize calibrate` reproduces the corpus DLGC spec — tensile 1099 vs 1100 MPa (−0.1%), carbon −1.94 vs −2.1 (+7.7%), density +7.7% — and **flags the modulus gap (45 vs ≥80 GPa) as [IN-CORPUS-DISPUTE]** rather than hiding it. The corpus's own honesty discipline, encoded.

## Dev-policy compliance

| Gate | How |
|---|---|
| EXTENSIBLE | new capability = new file; registries accept new records with zero code change |
| MODULAR | one concern per module; no cross-import outside declared interfaces |
| SCRIPTABLE | every procedure is a named CLI command reproducing its result |
| INTEROPERABLE | JSON in/out; `--json` on data commands; round-trippable registries |
| PROGRAMMABLE | behaviour is data: edit `data/*.json`, everything (incl. the study) changes |
| SCALABLE | same result at 1 t/yr and 1 Mt/yr (linear models, no hidden state) |
| REPLICABLE | seeded MC; study generation run-twice-diff-zero (tested) |
| TESTABLE | 24 tests; mutation check executed (break → red, restore → green) |
| VALIDATABLE | `registry validate` schema gate; calibration vs corpus spec recorded |
| OPERABLE | 100% of CLI commands executed this session, outputs shown |

## Extending

1. **Add a material:** append a record to `data/materials.json` (schema in `registry.py` docstring), run `python3 -m efemat registry validate`.
2. **Add a process:** append to `data/processes.json` with `stage` = cultivation | generation | manufacture.
3. **Retune EFE weights:** edit `data/pillars.json` — scores and grades shift with zero code changes.
4. **Regenerate the study:** `python3 -m efemat detail study` — the markdown is an artifact of the registries.

## Provenance

Built for the aequchain materials program (2026-10-06). Companion artifacts: the 8-category Material Flow studies + master index (`../aequchain material flow studies/`), GitLab `aequchain-dev` branch, GitHub `aequchain-dev/Material-Studies`. Deliberation: laya decision engine (schema-corrected this session) — hybrid sim fidelity + companion-study scope accepted; JSON-over-YAML dissent disclosed (stdlib reliability).
