# FINDINGS — aequchain Replenishable Materials Program

**Scope:** the lab build (`efemat`), study #9 generation, CEA product integration, the atmospheric family, Transparent Wood glazing, the calculators framework, and the possibility-space concept pipeline.
**Compiled:** 2026-10-07 · **Maintained by:** aequ>CALIBER|EFE Engineer
**Discipline:** every number below was computed by `efemat` and verified by execution in-session; every claim carries its evidence class. Nothing here is self-certified — the gates section records how each assertion was tested.

**Evidence classes (AEFRI v0.2):** `[MEASURED]` executed now, by us · `[MODELLED]` computed from stated parameters · `[LITERATURE]` external published ranges · `[SPEC]` corpus design specification · `[BLUEPRINT]` corpus design, unexecuted · `[UNVALIDATED]` claimed, not demonstrated · `[LITERATURE-SCOUTED]` concept-stage external range, no internal computation.

---

## Contents

1. [Program state](#1-program-state)
2. [Findings](#2-findings)
3. [Decisions ledger](#3-decisions-ledger)
4. [Verified numbers](#4-verified-numbers)
5. [Gates evidence](#5-gates-evidence)
6. [Errors caught + lessons](#6-errors-caught--lessons)
7. [Environment inventory](#7-environment-inventory)
8. [Pending items](#8-pending-items)

---

## 1. Program state

| component | state |
|---|---|
| Materials registry | **29** materials — 22 replenishable (21 biological + 1 atmospheric) + 7 baselines, status-tagged |
| Process registry | **27** processes — 12 cultivation (incl. AEQUACROP + AEQUIGROW) · 8 generation · 7 manufacture (incl. `transparent_wood_line`) |
| Concept ledger | **13** scouted concepts — 5 tier-1, 8 tier-2 (incl. the Transparent Wood family), across 7 source classes × 9 synthesis routes |
| Test suite | **58 tests, all green**; 3 mutation checks executed + E9 range-density regression |
| Study #9 | `Material Flow: Replenishable Materials.md` — **492 lines**, 0 validation errors, §I–§XII |
| Product dossier | `Material Flow: Transparent Wood.md` — operating model, 11-gap ledger, TW-family concepts, `transparent_wood_line` process, 9 applications (2026-10-07) |
| Replicability | run-twice-diff-zero proven locally **and** from a fresh clone of the public repo |
| Public repo | `github.com/aequchain-dev/Material-Studies` @ `main@6d515cd` (lab + studies + README); local is ahead (concepts, §XII, glyph v1.1, this document) |
| Capability glyph | POINTS glyph `aequ>CALIBER|EFE Engineer` **v1.1** — 28 entities, 36 edges, 8192 bytes |
| Memory | slot `aequchain/materials-program` — 17 entities, 28 edges (revision counter reset observed; content verified complete) |
| Skills bank | 282 skills indexed; draft skill `aequchain-efemat` audited PASS (id 283), awaiting evals + human confirm |

---

## 2. Findings

### F1 — The replenishable class has two families `[MODELLED]`
The *biological* family regrows in soil (fields); the *atmospheric* family regrows in the sky. **CIL diamond, grown from DAC CO₂, is as replenishable as bamboo once the feedstock is defined as air** — the seam refills nightly. Encoded as `family: biological | atmospheric` on registry records; the study thesis (§I) and conclusion (§XI) state both.

### F2 — CIL diamond's per-kg carbon sign is grid-dependent `[MODELLED]`
At the corpus floor of 285 kWh/kg (1026 MJ/kg), net CO₂ per kg of diamond:

| grid | kg CO₂/MJ | g/kWh | net CO₂ kg/kg |
|---|---|---|---|
| world | 0.110 | 396 | **+109.19** |
| renewable (lifecycle) | 0.020 | 72 | **+16.85** |
| efe (best-case PV) | 0.005 | 18 | **+1.46** |
| zero | 0.000 | 0 | **−3.67** |

The sign flips only below **~12.9 g/kWh** (uptake 3.667 kg ÷ 1026 MJ = 0.00357 kg/MJ) — beneath best-case PV lifecycle intensity. **The corpus's net-negative claim is FACILITY-level** (DAC surplus beyond diamond demand → BIOCHAR_STORAGE credits), not per-kg. Diamond's climate value is geological permanence + material displacement, not per-kg sequestration. Recorded in study §VII.g and residual item 6.

### F3 — The atmospheric family's "field" is the PV array `[MODELLED]`
Power ledger: **7,684 kg diamond per MW·yr** at 25% capacity factor; 1 t/yr needs **0.13 MW nameplate ≈ 0.195 ha PV**; a 60-chamber facility (~50 t/yr) needs **~6.5 MW ≈ ~10 ha PV**. Same order as bamboo's land intensity per tonne — the atmospheric family is land-cheap but power-bound. (An earlier 130 MW figure was a 1000× arithmetic error, caught and corrected before registration.)

### F4 — The land floor is real but soft: three honest levers `[MODELLED]`
Field scenario at `[LITERATURE]` yield midpoints for DLGC @ 1.15 Mt/yr: **129,449 ha** (bamboo 16,885 + hemp 112,565). Levers: (1) **mix** — all-bamboo fiber = **28,141 ha, −78%**, on marginal land; (2) **farmplex** — 15× footprint compression for food/algae/nursery only (demo: algae @ 100 kt/yr: 2,353 ha field → 157 ha at 5 floors × 3× uplift); (3) **atmospheric** — zero biological land (F3). The field baseline itself is unchanged — the levers are additive, not replacements.

### F5 — Vertical farming does NOT dissolve the fiber land floor `[LITERATURE]`
Structural fiber (20 m bamboo culms at 25 t/ha/yr) is field agronomy — stacking does not apply to it. AEFRI v0.2's own cautionary record stands: AeroFarms (Ch.11 2023), Bowery (ceased 2024), Plenty (Ch.11 2025) — all failed on grid electricity. Alas. Indoor staples only after **MEASURED kWh/kg**. Under EFE free-energy the land-for-energy trade inverts, but the gate is measurement, not thesis.

### F6 — The farmplex's best fiber-adjacent use is nursery propagation `[MODELLED]`
Bamboo nursery modules shorten the 5–7 yr stand lead time — the actual bottleneck the land ledger exposes — rather than pretending to grow structural biomass indoors.

### F7 — AEQUACROP + AEQUIGROW are certified corpus products, now registered `[CORPUS]`
**AEQUACROP** (3-module bio-integrated platform: A grow-core, B bio-converter — waste→biomaterial anaerobic digester, 15 m², C habitat-integration — rooftop farm, greenhouse wall, living architecture; passive climate; CC-BY-SA/OSHW). **AEQUIGROW v3.0** (vertical aeroponic tower: **264–403 plants/m² vs 20–40 soil**, 15–25 kg/tower/yr, 2–5 L/day recirculating with **<0.5 L/day net loss**, 100 W PV/tower, T1 Proto → T2 Advanced (mycelium, +20–30% yield) → T3 Apex (diamond/graphene — closes into the CIL family); 9 OPTIBEST cycles, CERTIFIED PREMIUM). The **bio-converter → AEQUFAB interface** formally specifies self-replication: waste becomes feedstock for fab-printed modules. Energy figures registered as `[MODELLED]` (AEQUIGROW 126–210 MJ/kg derived from 100 W/tower design spec) pending MEASURED.

### F8 — Transparent Wood closes a double loop `[SPEC, LITERATURE-ANCHORED]`
Transparent Wood (delignified cellulose + bio-resin): 85–90% transmittance meets AEQUACROP's ≥85% PAR glazing spec (replacing recycled-PC double-wall); haze 60–80% = **diffuse light, a CEA feature**. Loop 1: delignification's **lignin byproduct feeds DLGC's lignin_resin stream (38% of DLGC)** — the glazing co-produces the flagship's resin. Loop 2: the removed lignin is itself a UV absorber — the yellowing mitigation comes from the waste stream. Panel-scale infiltration remains `[UNVALIDATED]` industrially. Name: "Transparent Wood" — the D6 working-name coinage was retired per user confirmation (D8, 2026-10-07).

### F9 — Scaling is linear in land; cost falls by learning curve, not volume `[MODELLED]`
The calculators framework proves the SCALABLE gate: **112.6 ha per kt/yr, constant across the 115× ramp** (10 kt → 1.15 Mt over 12 yr, geometric). Cost falls with program year via the EFE anchors ($4.00/kg now → $0.75/kg at year 12 → $0.12/kg by year 20), independent of volume. Loop recovery 0.85 (τ = 3 yr) drops virgin demand to 190,404 t/yr at Y12 (steady state 172,500).

### F10 — The possibility space is 7 source classes × 9 routes `[LITERATURE-SCOUTED]`
Beyond the registered field + sky families: **ocean** (kelp — zero land/freshwater/fertilizer), **wastewater** (duckweed — AEQUAQUA's outflow becomes the farm), **subsurface sand** (MICP biocement — the one study category, masonry, with zero grown materials), **saline field** (salicornia — new land unlocked, not competed for), plus new routes: liquid fermentation (bacterial cellulose — Transparent Wood companion), gas fermentation (PHA-from-biogas — the AEQUACROP loop's missing material link; atmospheric protein). Tier-1 criterion: opens a new source class/route **and** hooks an existing corpus product.

### F11 — DLGC reproduces its corpus spec with one flagged dispute `[MODELLED]`
Calibration vs corpus: tensile **−0.1%**, carbon **+7.7%**, density +7.7%, modulus **−43.8% FLAGGED `[IN-CORPUS-DISPUTE]`** (rule-of-mixtures reaches ~45–60 GPa vs corpus ≥80 — requires aligned nanocellulose-graphene synergy modeling or a corpus spec revision). Monte-Carlo band (n=1000, seed=42): p5 −2.14 / p50 −1.95 / p95 −1.77 kg CO₂/kg.

### F12 — Transparent Wood is the first glazing in the EFE scoring universe `[MEASURED-ENVIRONMENT]`
The EFE materials database (15 materials) has **no glazing class at all** — glass and PC are not even baselines. The product dossier (`Material Flow: Transparent Wood.md`, 2026-10-07) records: the operating model (double loop: lignin → DLGC resin 38%; removed lignin = UV absorber); an 11-gap ledger (frm_gap_detect added two HIGH blind spots: EoL recovery ≥95% unverified, repair procedure undocumented); three new tier-2 concepts (`lignin_uv_absorber`, `tw_aerogel`, `fr_bio_resin` — all `[LITERATURE-SCOUTED]`, MEASURED-gated); the `transparent_wood_line` manufacture process `[BLUEPRINT]` (8–25 MJ/kg); and a two-product family split (CEA-grade haze-as-feature vs low-haze view-grade). Web surround still offline (count 0) — literature claims remain `[LITERATURE-SCOUTED]`.

---

## 3. Decisions ledger

| # | decision | rationale | engine signal | dissent |
|---|---|---|---|---|
| D1 | Hybrid sim fidelity (analytic core + seeded MC) | deterministic + uncertainty band | laya ACCEPTED | none |
| D2 | JSON data backbone (not YAML) | stdlib-only reliability (PyYAML = dependency) | — | **disclosed**: laya leaned YAML; overruled on the zero-dependency policy |
| D3 | Separate `concepts.json` ledger (not `[IDEA]` rows in materials.json) | **dominance**: in-registry concepts would force fabricating LCA/EFE numbers they don't have (never-fabricate) or two-tier validation | laya UNRESOLVED (0.39 vs 0.33, conf 0.0099) → sequential-thinking | laya's weak contrary lean documented as noise |
| D4 | Tier-1 = kelp, duckweed, bacterial cellulose, MICP, PHA-route | stated criterion: new source class/route + corpus hook (MICP fills the masonry gap; lignin CF stays in represented waste_stream) | laya UNRESOLVED (0.3732 vs 0.3674 — 0.006 margin) → sequential-thinking | laya's 0.006 lean overturned by criterion |
| D5 | Architecture = glyph index + repo artifacts + memory | portable index, executable substance | laya 0.62 (advisory) | none |
| D6 | user coinage (transparent-cellulose); no corpus collision | — | **RESOLVED 2026-10-07 — superseded by D8** |
| D8 | Material name = **"Transparent Wood"** (id `transparent_wood`) | user confirmation 2026-10-07: retire the coinage, keep the material; registries + generator + tests edited, study regenerated | — | none |
| D9 | Extend the possibility space with the Transparent Wood family: 3 tier-2 concepts + `transparent_wood_line` manufacture process + product dossier | user directive (conceptualize gaps \| new materials \| process \| applications); tier-2 is honest — no new source class/route opened, the product family deepens | — | none |
| D7 | Push lab + studies as one public repo | the repo becomes fully replicable (study + generator + tests) | — | none; fresh-clone verified |

---

## 4. Verified numbers

All computed by `efemat` and cross-checked in-session:

| quantity | value | source model |
|---|---|---|
| Land @ 1.15 Mt/yr (60/40 mix) | 129,449 ha | `simulate.land_ledger` |
| All-bamboo lever | 28,141 ha (−78%) | `calculators.mix_ledger` |
| 80/20 mix | 78,795 ha | `calculators.mix_ledger` |
| Fiber fraction / utilization | 0.52 / 0.85 | registry (dlgc composition) |
| Bamboo / hemp_fiber yield mid | 25 / 2.5 t/ha/yr | registry `[LITERATURE]` ranges |
| DLGC net carbon (renewable) | −1.94 kg CO₂/kg | `simulate.lca` |
| DLGC annual @ Y12 | −2,229 kt CO₂/yr | `calculators.resource_ledger` |
| DLGC MC band (p5/p50/p95) | −2.14 / −1.95 / −1.77 | `simulate.monte_carlo_lca` (seed 42) |
| DLGC cost curve | $4.00 → $0.75 (yr 12) → $0.12/kg (yr 20) | `simulate.cost_trajectory` |
| Loop (recovery / τ / steady virgin) | 0.85 / 3 yr / 172,500 t/yr | `simulate.loop_dynamics` |
| Scale path | 112.6 ha/kt constant; 115× ramp | `calculators.scale_path` |
| CIL diamond energy floor | 1026 MJ/kg (285 kWh/kg) | corpus `[SPEC]` |
| CIL uptake | 3.667 kg CO₂/kg (44/12) | stoichiometry |
| CIL sign-flip threshold | ~12.9 g/kWh (0.00357 kg/MJ) | derived |
| CIL power ledger | 7,684 kg/MW·yr; 0.13 MW + 0.195 ha PV per t/yr | `simulate.power_ledger` |
| Grid factors | renewable 0.02 (72 g/kWh) · world 0.11 (396) · efe 0.005 (18) · zero 0.0 | `simulate.GRIDS` |
| AEQUIGROW density | 264–403 plants/m²; 15–25 kg/tower/yr; <0.5 L/day net | corpus blueprint |
| AEQUIGROW energy (derived) | 126–210 MJ/kg `[MODELLED]` | 100 W × 8760 h ÷ 15–25 kg |
| Transparent Wood optical | 85–90% transmittance; 60–80% haze | `[LITERATURE]` |
| Transparent Wood net carbon / MC band (n=500) | −0.99 kg CO₂/kg; −1.20 / −0.97 / −0.79 | `simulate.lca` + `simulate.monte_carlo_lca` (seed 42) |
| Farmplex demo (algae 100 kt/yr) | 2,353 ha → 157 ha (15×) | `simulate.footprint_ledger` |

---

## 5. Gates evidence

- **TESTABLE:** 58/58 green. Mutation checks executed: (a) `CO2_PER_C` 44/12→3.0 → 3 red, restore → green; (b) calculators mix-math break → 4 red, restore → green; (c) concept schema break (removed `promotion_gate`) → test FAIL + `concepts validate` INVALID with the exact record/field named, restore → green.
- **REPLICABLE:** `detail study` run-twice-diff-zero locally; **fresh clone of the public repo regenerates the pushed study byte-for-byte**.
- **OPERABLE:** every declared command executed in-session: registry list/show/validate · simulate lca/compare/cost/loop/land/mc · calculate ledger/mix/scale · concepts list/show/validate · evaluate efe/ladder/risk · synthesize composite/calibrate · prototype list/card · research corpus/web · detail study/scoresheet.
- **VALIDATABLE:** `registry validate` + `concepts validate` = VALID (0 errors); study stats report `validation_errors: 0`.
- **SCALABLE:** 112.6 ha/kt constant across the 115× ramp (F9).
- **HONESTY:** every error found is recorded in §6; no green flag was accepted without its payload checked.

---

## 6. Errors caught + lessons

| # | error | how caught | fix + lesson |
|---|---|---|---|
| E1 | `annual_t_co2` computed kg, labeled tonnes — **1000× off** (CLI showed an absurd −2.2 Gt CO₂/yr) | critical read of my own CLI output (honesty invariant: verify the payload, not the status field) | formula corrected; **the consistency test had encoded the same bug** (self-consistent wrongness) — test fixed + physical sanity bound added (|annual| < 10 Mt) |
| E2 | g/kWh column inverted the conversion (0.02 kg/MJ shown as "6" instead of 72 g/kWh) — 12.96× error | review of the regenerated study table | ×3600 factor; unit conversions get a second read |
| E3 | Hand-transcribed glyph b64 decoded to 1753 bytes ≠ encoder's 8192 — truncated transcription | decode-verify after write | corrupted artifact **removed** (never archive a bad copy); the validated spec JSON is the durable source of truth; b64 regenerable on demand |
| E4 | Remote tip was 2 commits past the recorded `8840281` (user-side pushes) — stale memory | clone-before-push | stale facts corrected by touching ground truth; always clone before assuming remote state |
| E5 | Memory slot revision counter returned 1 (expected 6) — harness restart | immediate read-back verification | **content verified complete** (17 entities, 28 edges — the always-write-full-merged-graph discipline prevented loss); counter ≠ content |
| E6 | laya returned UNRESOLVED on concept-pipeline decisions (confidences 0.0099–0.0208, flat probabilities, 0.006 margins) | reading the confidence fields, not just the choices | R-C fallback to sequential-thinking; resolved by **dominance** (no-fabrication) and **stated criterion** — never follow a noise-level lean |
| E7 | Six consecutive "announcing the laya call" responses without making it | user's repeated "continue" | *the tool call IS the continuation* — announce-then-not-call is a failure mode; recorded in memory |
| E8 | Web-search surround offline all sessions | `count: 0` returns | cultivation yields remain `[LITERATURE]` midpoints, MODELLED until MEASURED — flagged in study residual item 3 |
| E9 | `detail scoresheet` crashed on range-valued `density_g_cm3` (`_fmt_num` float() on list) — transparent_wood is the first range-density material through the scoresheet path | executing the command post-rename (the OPERABLE gate is also the bug-finder) | density line switched to `_fmt_range`; regression test `test_scoresheet_range_density` added (58th test); range-typed fields get `_fmt_range` everywhere |

---

## 7. Environment inventory

```
aequchain-materials-lab/
  efemat/           registry · simulate · calculators · evaluate · synthesize ·
                    prototype · research · detail · cli (9 modules, stdlib-only)
   data/             materials.json (29) · processes.json (27) · concepts.json (13) ·
                     pillars.json (7, [CONFIGURABLE])
   tests/            58 tests across 8 files, mutation-checked
  glyphs/            aequ_caliber_efe_engineer.graph.json (glyph v1.1 spec, validated)
  FINDINGS.md        this document
  README.md · pyproject.toml · .gitignore
```

- **Capability glyph** (POINTS, v1.1): role + 8 capabilities + 9 resources (incl. the concept pipeline and the memory slot) + 6 products + 4 protocols; 28 entities, 36 edges, no dangling refs; live in session slot `main`; spec is the durable source of truth.
- **Memory slot** `aequchain/materials-program`: 17 entities, 28 edges — program state, all findings, all lessons (additive-only; DEF ENHANCEMENT for stale-fact refresh).
- **Skills bank**: draft `aequchain-efemat` (documents lab operation; audited PASS; ranks #1 for biomaterials queries) — promotion requires evals + human confirmation.
- **Public repo**: `github.com/aequchain-dev/Material-Studies` — studies + master index + README + the lab; fresh-clone-verified.

---

## 8. Pending items

1. **Push** — local is ahead of `main@6d515cd`: concepts.json + concept CLI + study §XII (492 lines) + glyph v1.1 + this FINDINGS.md + the Transparent Wood rename (D8) + the TW-family concepts/process (D9) + the product dossier.
2. **Material name — RESOLVED 2026-10-07:** renamed to "Transparent Wood" per user confirmation (D8); registries edited, tests re-run green, study regenerated.
3. **Skill promotion** — `aequchain-efemat` needs `evals/evals.json` + human confirm.
4. **GitLab sync** — `aequchain1/devzone@8772089` not updated since the studies-only push.
5. **MEASURED gates** — all 13 concepts carry their promotion experiment; tier-1 first (kelp raft, greywater pond, 10 L fermenter, MICP brick, bench biogas→PHA); TW-family next (1000 h weathering, 100 cm2 aerogel panel, UL94 panel).
6. **Web re-verification** of `[LITERATURE]` yields when the search surround is live.
7. **Climate-scenario yield deltas** for the land model (study residual item 5).
8. **DLGC modulus dispute** — aligned nanocellulose-graphene synergy modeling, or corpus spec revision (residual item 1).
9. **EFE-DB glazing baselines** — register glass + PC as glazing baselines so Transparent Wood can be graded against a class (dossier gap 11).

---

*This document is maintained by the aequ>CALIBER|EFE engineer environment. Findings are appended, never silently replaced (additive protocol). Every entry is traceable: to a registry record, a simulate model, a test, or a documented engine decision.*
