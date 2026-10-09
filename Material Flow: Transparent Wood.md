# Material Flow: Transparent Wood
### The glazing that regrows — product dossier, companion to study #9

**Dossier date:** 2026-10-07 · **Revision:** v1.1 (2026-10-07 — added §III baseline comparison, §VII gate test-methods, §VIII feedstock ledger, §X documentation map)
**Series:** product-level companion to *Material Flow: Replenishable Materials* (study #9)
**Subject:** `transparent_wood` — Transparent Wood (bio-resin infiltrated delignified cellulose glazing) `[SPEC [LITERATURE-ANCHORED]]`
**Provenance:** hand-written dossier per series doctrine; every computed number cited from the `efemat` registries and simulation models (regenerate study #9: `python3 -m efemat detail study`; per-material: `python3 -m efemat detail scoresheet transparent_wood`)
**Status tags:** `[SPEC]` `[BLUEPRINT]` `[LITERATURE]` `[LITERATURE-SCOUTED]` `[UNVALIDATED]` `[MODELLED]`

---

## §I — PURPOSE & POSITION

Transparent Wood is the program's **only glazing that regrows**. It exists to replace two
things at once: the recycled-PC double-wall panels of the AEQUACROP grow-core (spec:
>=85% PAR transmittance) and, at building scale, the glass/PC window stock of the aequcity
envelope. Its feedstock is the *offcut stream* — poplar/balsa SRWC thinnings and bamboo
culm sections unsuited to structural use — so its demand is **panel-area-bound, not
tonnage-bound**: no plantation ever expands for a window.

**Position finding (EFE-DB cross-check, 2026-10-07):** the EFE materials database (15
materials: metals, polymers, ceramics, composites, bio-based) contains **no glazing class
at all** — glass and PC are not even represented as baselines. Transparent Wood is not a
better entry in an existing class; it is the **first glazing the EFE scoring system has
ever been asked to grade**. Its registry EFE seed score: **77.5 / B** `[SEED-ESTIMATE]`,
strongest pillar `sustainable_materials`, weakest `renewable_energy` (processing energy
16.5 MJ/kg mid).

## §II — OPERATING MODEL (the replenishable loop, instantiated)

The class doctrine — *if a field can regrow it on a known cycle, never run a furnace for
it* — specializes here into a five-hop loop with two internal circulations:

```
 SRWC ROTATION (3-8 yr; offcut + thinning stream, harvest without plantation expansion)
        |
        v  DELIGNIFY (NaClO2/NaOH or organosolv)
        |--------------> LIGNIN LIQUOR --> DLGC lignin_resin stream (38% of DLGC)   [LOOP 1]
        v  DEHYDRATE (solvent exchange)
        v  INFILTRATE (vacuum-assisted bio-resin + lignin-derived UV absorber)      [LOOP 2]
        v  CURE (UV/thermal; solar-thermal doctrine) + COAT (geopolymer, no-lime)
        v  PANEL IN SERVICE (AEQUACROP glazing | aequcity windows | solar substrate)
        |            85-90% transmittance · 60-80% haze = diffuse light (CEA feature)
        v  EoL: REGRIND -> cellulose + resin separation -> lignin back to resin stream
        v
 BACK TO FIELD (compost) AND BACK TO DLGC (resin) — the panel feeds two regrowth loops
```

**Operating numbers** (all `efemat`-computed, renewable grid 0.02 kg CO2/MJ):

| quantity | value | model |
|---|---|---|
| net carbon | **-0.99 kg CO2/kg** (uptake 1.65, processing 16.5 MJ/kg) | `simulate.lca` |
| uncertainty band | p5 -1.20 / p50 -0.97 / p95 -0.79 (n=500, seed 42) | `simulate.monte_carlo_lca` |
| delta vs virgin steel | -3.09 kg CO2/kg | `simulate.compare` |
| cost trajectory | $8.00/kg -> $1.20 (yr 5) -> $0.50 (yr 10) -> $0.10/kg (yr 20) | `simulate.cost_trajectory` |
| loop | recovery 0.6, tau 5 yr | `simulate.loop_dynamics` |
| ladder | rung 1 SUBSTITUTE + supporting CLOSE-LOOP RECYCLE, TRACK EVERY GRAM | `evaluate.ladder` |
| permanence | 0.8 (biogenic carbon held in service + cascade) | registry |

*The double loop (FINDINGS F8) is the operating signature: the delignification waste is
the flagship's resin feed (loop 1), and the removed lignin is itself the UV blocker that
mitigates the panel's yellowing (loop 2) — the glazing's flaw is treated by its own waste
stream.*

## §III — BASELINE COMPARISON (what is being substituted; baselines `[LITERATURE]`, TW registry-cited)

| property | Transparent Wood | soda-lime glass `[LITERATURE]` | recycled-PC multiwall `[LITERATURE]` |
|---|---|---|---|
| density | 1.0-1.2 g/cm3 | ~2.5 g/cm3 | ~1.2 g/cm3 |
| transmittance | 85-90% | 85-92% (clear, low haze) | ~80-85% (multiwall wall losses) |
| haze | 60-80% (diffuse = CEA feature) | <1-3% | high (rib + wall scattering) |
| tensile | 40-120 MPa | 30-50 MPa (brittle, no yield) | 55-75 MPa |
| impact | 3-10x glass toughness `[LITERATURE]` | shatters (safety glass laminates add mass/cost) | very high (PC signature) |
| thermal | unquantified (gap 8; `tw_aerogel` targets insulation) | ~0.8-1.0 W/mK (conductor, single pane) | multiwall air-gap U ~2.5-3.5 W/m2K |
| net carbon | **-0.99 kg CO2/kg** (renewable grid) | ~+0.8-1.2 kg CO2/kg (float process) | ~+2.5-3.5 virgin / lower recycled |
| feedstock | regrown (SRWC offcuts, 3-8 yr) | mined (silica/soda/lime, furnace ~1500 C) | fossil (BPA/phosgene route) |
| EoL | REGRIND -> cellulose + resin separation; lignin to resin | recyclable, frequently downcycled | recyclable thermoplastic |
| loop closure | co-produces DLGC resin feed (38%) | none | none |

**Honest reading:** TW wins on carbon, toughness-per-weight, feedstock renewal and loop
closure; it loses (today) on view-grade haze and unquantified thermal performance — which
is exactly what the gap ledger (§IV) and the `tw_aerogel` concept (§V) exist to close.
The comparison is the substitution case, not a victory lap.

## §IV — GAP LEDGER (conceptualized; every gap carries its evidence class + closure route)

| # | gap | class | closure route |
|---|---|---|---|
| 1 | Panel-scale infiltration unvalidated industrially (lab-demonstrated only) | `[UNVALIDATED]` | MEASURED gate ladder (§VI); the gate to everything else |
| 2 | UV yellowing over service life; lignin-absorber mitigation unproven at panel scale | `[UNVALIDATED]` | `lignin_uv_absorber` concept -> 1000 h accelerated weathering MEASURED |
| 3 | Fire performance vs glass; FR formulation needed | `[UNVALIDATED]` | `fr_bio_resin` concept -> UL94 MEASURED on infiltrated panel |
| 4 | Delignification liquor must close (reagent recovery: chlorite/organosolv) | **top registry risk [HIGH]** (L3xI4) | liquor-closure SOP in `transparent_wood_line` [BLUEPRINT]; chemical recovery MEASURED |
| 5 | Haze 60-80% unacceptable for view glazing | `[LITERATURE]` property | two-product family split (§IX): CEA-grade vs low-haze view-grade variant |
| 6 | Moisture-driven dimensional stability of cellulose unaddressed | `[UNVALIDATED]` | swelling-cycle MEASURED (§VII) + edge-seal spec (geopolymer coat assists) |
| 7 | No building-code approval path for wood glazing in the envelope | corpus-flagged (mirrors geopolymer approval gap) | SCM-bridge strategy: CEA interiors first, envelope later |
| 8 | Thermal U-value vs double-wall PC unquantified | `[UNVALIDATED]` | `tw_aerogel` concept -> thermal conductivity MEASURED (§VII) |
| 9 | EoL recovery >=95% not verified | frm_gap_detect HIGH blind spot | regrind + separation yield MEASURED (mass balance, §VII) |
| 10 | Repair procedure undocumented | frm_gap_detect HIGH blind spot | patch/replace SOP per panel class; passport on-chain (rung 4) |
| 11 | EFE-DB has no glazing class — no compliance-scoring infrastructure for ANY glazing | environment finding | register glazing baselines (glass, PC) + grade Transparent Wood against them |

*Anti-gaming note: gaps 1-4 and 6-10 are all real and open; none is closed by thesis.
The dossier claims no plateau — it claims a ranked, gated path.*

## §V — NEW MATERIALS (the conceptual advances; all registered in `concepts.json` with MEASURED gates)

1. **`lignin_uv_absorber`** `[LITERATURE-SCOUTED]` — lignin chromophores as bio-based
   UV-filter additive, extracted from the delignification liquor. Closes loop 2
   formally; also serves DLGC resin and PLA/PHA films. Gate: UV absorbance spectrum +
   delta-b* yellowing reduction at 1000 h accelerated weathering.
2. **`tw_aerogel`** `[LITERATURE-SCOUTED]` — aerogel-infiltrated delignified wood =
   **transparent insulation** (low thermal conductivity with retained transmittance).
   The cold-climate glazing variant; hooks the `ricehusk_silica` concept for the silica
   sol. Gate: thermal conductivity + transmittance on 100 cm2 panel.
3. **`fr_bio_resin`** `[LITERATURE-SCOUTED]` — linseed bio-polyol (flax co-product)
   epoxidized to bio-epoxy with P/mineral fillers. Closes the fire gap; shared
   formulation family with DLGC's resin tier. Gate: UL94 rating at target transmittance.
4. **`bacterial_cellulose`** (existing tier-1) — the *microbial route to transparent
   cellulose without delignification*: purest cellulose, no lignin/hemicellulose, high
   crystallinity, optically transparent films. The companion that makes the delignify
   route optional. Gate: film tensile + transmittance at 10 L fermenter on waste sugar.

**Feedstock variant (no new record needed):** bamboo-culm Transparent Wood — the
registry feedstock list already carries bamboo sections unsuited to structural use;
bamboo's hollow geometry suits lamination panels and shortens the feedstock cycle to the
3-5 yr culm rotation.

## §VI — PROCESS (the manufacture line; registered as `transparent_wood_line` `[BLUEPRINT]`)

| step | operation | spec | energy note |
|---|---|---|---|
| 0 | Feedstock intake | SRWC offcuts (poplar, balsa) + bamboo culm sections; 3-8 yr rotation | 0 MJ/kg (residue stream) |
| 1 | Delignify | NaClO2/NaOH or organosolv; lignin -> DLGC resin stream; **reagent recovery loop required** | dominant energy share |
| 2 | Dehydrate | solvent exchange (ethanol/water gradient) | — |
| 3 | Infiltrate | vacuum-assisted bio-resin + lignin-derived UV absorber | — |
| 4 | Cure + coat | UV/thermal cure (solar-thermal doctrine); geopolymer no-lime coat (0.5-1.5 MJ/kg, ceramics study) | — |
| 5 | QC | transmittance >=85% PAR, haze, impact (3-10x glass `[LITERATURE]`) | in-line |
| 6 | EoL | REGRIND -> cellulose + resin separation; lignin to resin stream | recovery 0.6, tau 5 yr |

**Line energy: 8-25 MJ/kg** (registry, matches material `processing_energy_mj_kg`).
**MEASURED gate ladder:** lab panel (100 cm2) -> m2 panel -> pilot line -> AEQUACROP
retrofit trial (side-by-side vs recycled-PC double-wall: PAR, canopy uniformity, kWh/kg
of produce delta). Nothing scales before its gate is MEASURED (AEFRI discipline).

## §VII — MEASURED GATE TEST-METHODS (the standards behind every gate; methods `[LITERATURE]`, results pending)

| gate | property | method (standard) | acceptance target |
|---|---|---|---|
| optical | PAR transmittance | spectroradiometer, 400-700 nm integrated (ASTM E903 / ISO 9050 class) | >=85% (grow-core spec) |
| optical | haze | ASTM D1003 (transparent-plastics haze) | CEA-grade: no floor (feature); view-grade: target TBD after variant work |
| durability | UV yellowing | accelerated weathering (ASTM G154 / ISO 4892-3 class), Delta-b* colorimetry (CIELAB) | Delta-b* reduction vs unmodified control at 1000 h (`lignin_uv_absorber` gate) |
| fire | flame rating | UL94 vertical burn (V-0/V-1/V-2); cone calorimetry (ISO 5660 class) for research depth | UL94 rating at target transmittance (`fr_bio_resin` gate) |
| thermal | conductivity / U-value | guarded hot plate (ISO 8301 class) or hot-wire (ISO 8894-1 class); panel U via hot-box (ASTM C1363 class) | beat double-wall PC U; `tw_aerogel` stretch: transparent-insulation class |
| mechanical | impact toughness | falling-weight (ASTM D5628 class) or Izod (ASTM D256 class) — the "3-10x glass" claim gets its defined test | >=3x glass on the chosen test |
| stability | moisture swelling | dimensional-stability cycling (ASTM D1037 class, wood-panel protocol) | in-plane swelling within window-glazing tolerance (TBD by variant) |
| circularity | EoL recovery yield | mass-balance protocol on regrind + separation | >=95% (gap 9) |
| circularity | repair | patch/replace SOP per panel class + on-chain passport (rung 4) | documented procedure (gap 10) |

*Method citations are to standard classes `[LITERATURE]`; no result values are claimed —
every acceptance cell is a MEASURED gate, not a result. This table is the anti-fabrication
companion to §IV: a gap without a test method is a wish; a gap with one is a schedule.*

## §VIII — FEEDSTOCK LEDGER (registry-cited; the fields behind the panel)

| feedstock | registry record | cycle | yield | role for TW |
|---|---|---|---|---|
| poplar (SRWC coppice) | `poplar_timber` `[LITERATURE]` | 10-15 yr rotation; **coppice regrows without replanting** | 8-15 t/ha/yr | primary offcut/thinning stream |
| bamboo (non-structural sections) | `bamboo` `[LITERATURE]` | culm 3-5 yr; stand 5-7 yr; then annual selective harvest | 20-30 t/ha/yr | culm sections unsuited to structural use; hollow geometry suits lamination |
| balsa (fastest SRWC) | `[LITERATURE]` (not yet registered) | ~4-5 yr plantation rotation | fastest of the commercial light hardwoods | low-density laminate core; candidate for registry promotion after MEASURED |

**Doctrine:** offcut + thinning streams only — demand is panel-area-bound, so the
rotation is never mined, only pruned. SRWC grows on marginal land (no food competition,
per the land-ledger finding F4). **The co-product that makes the line a loop, not a
chain:** delignification liquor -> DLGC `lignin_resin` stream (38% of DLGC composition)
— every panel milled pays a resin dividend to the flagship.

## §IX — APPLICATIONS (registered four + the conceptualized extensions)

**Registered (materials.json):**
1. AEQUACROP grow-core glazing — replaces recycled-PC double-wall, >=85% PAR; haze =
   diffuse light improves canopy uniformity (a CEA feature, not a defect)
2. aequcity windows + skylights (building stock)
3. solar-cell substrates (diffuse-light tolerant)
4. diffuse-light luminaires + display substrates

**Extensions (this dossier; status per item):**
5. **Greenhouse-wall structural glazing** `[BLUEPRINT]` — at 40-120 MPa tensile the
   panel carries load glass cannot at equal weight (1.0-1.2 g/cm3 vs ~2.5): wall + light
   in one element for AEQUACROP habitat-integration and living architecture.
6. **AEQUIGROW enclosure panels** `[BLUEPRINT]` — tower glazing/enclosure printed or
   framed from offcut-grade panels; T2 mycelium-insulated towers pair naturally.
7. **Transparent insulation envelope** `[LITERATURE-SCOUTED]` — the `tw_aerogel` variant
   as aequcity's thermal-envelope glazing: light in, heat in.
8. **Solar stills / evaporation covers** `[BLUEPRINT]` — XEROSIL adjacency: diffuse
   light + hydrophilic cellulose surface for AEQUAQUA-adjacent water work.
9. **Ephemeral display architecture** `[BLUEPRINT]` — aequcity event structures:
   luminous wood walls (backlit panels double as the diffuse luminaires of item 4).

**The two-product family (gap 5 resolution):** CEA-grade panels keep haze 60-80% as a
feature; view-grade windows require a low-haze variant (thinner sections, higher resin
refractive-index matching, or bacterial-cellulose films) — one process line, two optical
grades, honestly separated.

## §X — DOCUMENTATION MAP (where everything lives; every artifact regenerable or versioned)

| artifact | location | regenerate / verify |
|---|---|---|
| registry record | `aequchain-materials-lab/efemat/data/materials.json` -> `transparent_wood` | `python3 -m efemat registry show transparent_wood` |
| process record | `efemat/data/processes.json` -> `transparent_wood_line` | `python3 -m efemat prototype card transparent_wood_line` |
| concepts (TW family) | `efemat/data/concepts.json` -> `lignin_uv_absorber` · `tw_aerogel` · `fr_bio_resin` | `python3 -m efemat concepts show <id>` |
| per-material scoresheet | computed live | `python3 -m efemat detail scoresheet transparent_wood` |
| study #9 (generated) | `Material Flow: Replenishable Materials.md` (492 lines) | `python3 -m efemat detail study` (run-twice-diff-zero) |
| this dossier (hand-written) | `Material Flow: Transparent Wood.md` v1.1 | versioned; not generated |
| findings ledger | `aequchain-materials-lab/FINDINGS.md` — F8, F12, D8, D9, E9 | additive protocol |
| master index | `Material Flow: 00 Master Index.md` row 10 | hand-maintained |
| program memory | harness slot `aequchain/materials-program` (19 entities, 32 edges) | read-back verified |
| capability glyph | `glyphs/aequ_caliber_efe_engineer.graph.json` v1.1 (validated spec) | b64 via `points_encode_graph_str` |
| public repo | `github.com/aequchain-dev/Material-Studies` @ `main` | push pending (FINDINGS item 1) |
| test suite | `tests/` — 58 tests, mutation-checked | `python3 -m unittest discover -s tests -t .` |

## §XI — RESIDUAL LEDGER

1. Web-search surround offline at authoring (count 0, consistent with FINDINGS E8): all
   `[LITERATURE-SCOUTED]` claims stand on internal knowledge and carry their MEASURED
   gates; re-verify when the surround is live.
2. EFE seed scores remain `[SEED-ESTIMATE]`; the EFE-DB glazing-class absence (gap 11)
   means no external scoring exists yet — registering glass/PC baselines is the fix.
3. The dossier itself is hand-written (unlike study #9): its numbers are cited from the
   registries, but its prose is not generated. Promotion of any §V concept into
   `materials.json` happens only after its MEASURED gate — the no-fabrication boundary.
4. Everything waits on gap 1: panel-scale infiltration. The line is `[BLUEPRINT]` until
   a m2 panel exists.
5. Balsa feedstock is `[LITERATURE]` only — candidate for registry promotion after its
   own MEASURED gate (yield + offcut availability at pilot scale).

---

*Doctrine applied without exception: SUBSTITUTE (glass/PC demand deleted) -> REDESIGN
(the grow-core takes diffuse light as a feature) -> CLOSE-LOOP RECYCLE (lignin to DLGC,
cellulose to regrind) -> TRACK EVERY GRAM (panel passports on-chain). The window is a
field; the field regrows the window.*

---

## §XII — SUITE v3 CYCLE (2026-10-09): GRADED, REFINED, LOOP-QUANTIFIED

*The Material Engineering Suite (efemat 2.0) applied to this material. Every number
below is computed by a named suite command and cross-checked in-session; evidence
classes per AEFRI v0.2. Full ledger: FINDINGS.md F17–F20, D14–D15.*

### §XII.1 — Class grading (gap 11 CLOSED) `[MEASURED]`

Glazing baselines registered (`glass_soda_lime`, `pc_polycarbonate`, `[LITERATURE]`,
category `glazing_baseline`); first-ever class grading via multi-category select
(`engineered_wood_glazing,glazing_baseline`):

| view | ranking | numbers |
|---|---|---|
| **strength-limited (σ^⅔/ρ)** | **TW wins doctrine AND pure performance** | TW 16.88 > PC 13.47 > glass 5.43 |
| stiffness-limited (E^½/ρ) | glass wins pure performance | glass 3.35 > TW 1.93 > PC 1.29 |
| carbon (net kg CO₂/kg) | **TW only net-negative in class** | TW −0.99 · glass +1.2 · PC +6.5 |
| EFE | TW 77.5 (B) · glass 64.0 (C) · PC 34.5 (E) | weakest TW pillar: renewable_energy (6) |

**Reading:** for impact/wind/hail-limited glazing — the AEQUACROP grow-core case —
TW dominates its class with no doctrine lever invoked. Deflection-limited spans stay
glass; framing compensates. The doctrine lever is now measured, not assumed.

### §XII.2 — Refinement (evidence-gated) `[MODELLED]`

| goal | best evidence-passing chain | result |
|---|---|---|
| strength | `align_fiber → densify_press` | tensile 80 → 124.8 MPa (+56%), modulus 4.5 → 7.67 GPa |
| carbon | `thermal_cure` | net −0.99 → −1.003 kg CO₂/kg (the permanence lever, F14 generalized) |
| efe | **plateau — seed-locked by design** | pillar estimates move only on MEASURED data |

The `[LITERATURE-SCOUTED]` UV-absorber scenario outranks every improvement on carbon
(u 0.03 > 0.0131): its 1000 h weathering gate (§VII) is this material's
highest-leverage experiment.

### §XII.3 — The lignin loop, quantified `[MODELLED]`

Declared parameters: hardwood lignin 0.20–0.25 `[LITERATURE]` × liquor recovery
0.85–0.95 `[LITERATURE]`; DLGC lignin_resin share 0.38 `[SPEC]`:

**1 t TW panels → 0.17–0.24 t lignin liquor → co-feeds 0.45–0.63 t DLGC.**
A 100 kt/yr glazing line carries resin for 45–63 kt/yr of flagship. The glazing
program and the DLGC program are one industrial metabolism, now with numbers.

### §XII.4 — Family extension `[LITERATURE-SCOUTED]`

Concept 14 `transparent_bamboo` registered (tier-2, field source, extraction route):
delignified bamboo + bio-resin — literature claims higher strength than TW (natural
axial fiber alignment) + UV-blocking retained lignin; `transparent_wood_line` already
lists bamboo culm sections as feedstock. **MEASURED gate:** transmittance ≥80%,
tensile ≥100 MPa full-culm panels, 1000 h UV vs TW control. Carries no LCA numbers
(no-fabrication boundary, tested).

### §XII.5 — Residual ledger update

- Gap 11 (glazing baselines) **CLOSED** — §XII.1.
- Gap 1 (panel-scale infiltration) remains the master gate; §XII.2's refinement
  chains are `[MODELLED]` scenarios until MEASURED.
- The renewable_energy pillar (6/10) is the weakest: the 8–25 MJ/kg
  delignification+infiltration energy is a *measurement* problem — no pathway moves
  a seed (F20).
