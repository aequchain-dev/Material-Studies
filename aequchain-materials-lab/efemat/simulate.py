"""efemat.simulate — LCA, cost-trajectory, loop-dynamics, land-ledger, Monte-Carlo.

Hybrid fidelity (laya-ruled): deterministic analytic core + seeded
Monte-Carlo uncertainty layer. Every model is closed-form, documented,
and parameterized — no hidden constants.

Models
------
1. biogenic_uptake(m):
       uptake = sum_i (fraction_i * carbon_fraction_i) * 44/12
   Stoichiometry: 1 kg carbon == 44/12 kg CO2 (3.667). Composition-weighted
   when the material declares one; else the bulk carbon_fraction.

2. lca(m, grid, permanence, soil_credit):
       net_co2 = processing_energy * grid_factor
                 - uptake * permanence
                 - soil_credit
   grid_factor: kg CO2 per MJ of process energy. Defaults:
       renewable-dedicated 0.02 (EFE context), world-mix 0.11.
   Baselines carry lca_override (published literature values).

3. cost_trajectory(m, years):
   Piecewise-linear interpolation through the material's EFE anchors
   [[year, multiplier], ...] x baseline_usd_kg. The corpus EFE curve:
   premium -> parity -> discount -> minimal -> free (Year 20+).

4. loop_dynamics(m, demand, years):
   First-order saturation of secondary supply:
       secondary_share(t) = recovery * (1 - exp(-t / tau))
       virgin(t)          = demand * (1 - secondary_share(t))
   years_to(target) solves for the year secondary_share >= target.

5. land_ledger(m, demand, utilization):
   Hectares of cultivation needed per feedstock:
       ha_i = demand * fiber_share * feedstock_share_i
              / (yield_i * utilization)
   The honest scaling answer for "can the fields feed the factory?"

6. monte_carlo_lca(m, n, seed):
   Seeded sampling of processing energy (+/-20% or its range),
   carbon_fraction (+/-10%), permanence (+/-5%) -> net-carbon
   distribution (p5 / p50 / p95). Reproducible: same seed, same result.
"""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List, Optional

from .registry import Registry, as_range, mid

# Stoichiometric CO2 per unit carbon (44/12).
CO2_PER_C: float = 44.0 / 12.0

# Grid carbon factors, kg CO2 per MJ of process energy.
GRIDS: Dict[str, float] = {
    "renewable": 0.02,   # conservative lifecycle incl. buffering (~72 g/kWh)
    "world": 0.11,       # ~0.4 kg CO2/kWh world mix
    "efe": 0.005,        # near-zero thesis floor (~18 g/kWh, best-case PV lifecycle)
    "zero": 0.0,         # idealized zero-marginal-emission (sign-flip boundary)
}

DEFAULT_UTILIZATION: float = 0.85  # field-to-factory utilization


def biogenic_uptake(material: Dict[str, Any]) -> float:
    """kg CO2 equivalents taken up per kg of dry material."""
    composition = material.get("composition")
    if composition:
        component_carbon = material.get("component_carbon") or {}
        bulk = material.get("carbon_fraction", 0.45)
        total = 0.0
        for name, fraction in composition.items():
            c_frac = component_carbon.get(name, bulk)
            total += fraction * float(c_frac) * CO2_PER_C
        return total
    return float(material.get("carbon_fraction", 0.45)) * CO2_PER_C


def lca(
    material: Dict[str, Any],
    grid: str = "renewable",
    permanence: Optional[float] = None,
    soil_credit: Optional[float] = None,
) -> Dict[str, Any]:
    """Cradle-to-gate carbon accounting for one material."""
    rid = material.get("id", "?")

    override = material.get("lca_override")
    if override:
        return {
            "id": rid,
            "override": True,
            "uptake": 0.0,
            "processing_mj_kg": float(override.get("embodied_energy_mj_kg", 0.0)),
            "processing_co2": float(override.get("embodied_carbon_kg_co2_kg", 0.0)),
            "net_carbon": float(override.get("embodied_carbon_kg_co2_kg", 0.0)),
            "permanence": None,
            "grid": None,
            "note": override.get("note", ""),
        }

    grid_factor = GRIDS.get(grid, GRIDS["renewable"])
    perm = material.get("permanence", 0.8) if permanence is None else permanence
    soil = material.get("soil_carbon_credit", 0.0) if soil_credit is None else soil_credit
    proc_e = mid(material.get("processing_energy_mj_kg")) or 0.0
    uptake = biogenic_uptake(material)
    proc_co2 = proc_e * grid_factor
    net = proc_co2 - uptake * perm - soil
    return {
        "id": rid,
        "override": False,
        "uptake": uptake,
        "processing_mj_kg": proc_e,
        "processing_co2": proc_co2,
        "net_carbon": net,
        "permanence": perm,
        "grid": grid,
        "note": "",
    }


def compare(
    materials: Registry,
    ids: Optional[List[str]] = None,
    grid: str = "renewable",
) -> List[Dict[str, Any]]:
    """LCA rows for the given ids (default: all), sorted best-first."""
    if ids is None:
        ids = materials.ids()
    rows = [lca(materials.get(i), grid=grid) for i in ids]
    rows.sort(key=lambda r: r["net_carbon"])
    return rows


def cost_trajectory(
    material: Dict[str, Any],
    years: int = 20,
) -> List[Dict[str, float]]:
    """EFE cost curve: [{year, multiplier, usd_kg}, ...]."""
    cost = material.get("cost") or {}
    anchors = sorted(cost.get("anchors", [[0, 1.0]]), key=lambda a: a[0])
    base = float(cost.get("baseline_usd_kg", 1.0))

    def multiplier_at(year: float) -> float:
        if year <= anchors[0][0]:
            return float(anchors[0][1])
        if year >= anchors[-1][0]:
            return float(anchors[-1][1])
        for (y0, m0), (y1, m1) in zip(anchors, anchors[1:]):
            if y0 <= year <= y1:
                t = (year - y0) / (y1 - y0) if y1 > y0 else 0.0
                return float(m0 + (m1 - m0) * t)
        return float(anchors[-1][1])

    return [
        {"year": y, "multiplier": multiplier_at(y), "usd_kg": multiplier_at(y) * base}
        for y in range(0, years + 1)
    ]


def loop_dynamics(
    material: Dict[str, Any],
    demand_t_yr: float,
    years: int = 50,
) -> Dict[str, Any]:
    """First-order saturation of secondary (recovered) supply."""
    loop = material.get("loop") or {"recovery": 0.5, "tau_yr": 5.0}
    recovery = float(loop.get("recovery", 0.5))
    tau = max(float(loop.get("tau_yr", 5.0)), 1e-6)

    series: List[Dict[str, float]] = []
    for t in range(years + 1):
        share = recovery * (1.0 - math.exp(-t / tau))
        series.append(
            {
                "year": t,
                "secondary_share": share,
                "virgin_t_yr": demand_t_yr * (1.0 - share),
            }
        )

    def years_to(target: float) -> Optional[int]:
        if target > recovery:
            return None
        t = -tau * math.log(1.0 - target / recovery) if recovery > 0 else None
        return None if t is None else int(math.ceil(t))

    steady_virgin = demand_t_yr * (1.0 - recovery)
    return {
        "id": material.get("id", "?"),
        "recovery": recovery,
        "tau_yr": tau,
        "demand_t_yr": demand_t_yr,
        "series": series,
        "years_to_80pct_secondary": years_to(0.80),
        "years_to_95pct_secondary": years_to(0.95),
        "steady_state_virgin_t_yr": steady_virgin,
        "note": (
            "95% secondary unreachable at this recovery — raise GREEN-stream "
            "A/B capture to >= 0.95" if years_to(0.95) is None else ""
        ),
    }


def land_ledger(
    material: Dict[str, Any],
    demand_t_yr: float,
    materials: Registry,
    utilization: float = DEFAULT_UTILIZATION,
) -> Optional[Dict[str, Any]]:
    """Cultivation hectares required per feedstock for a given demand.

    Requires the material to declare composition (fiber fraction) and
    feedstock_shares; returns None when not applicable.
    """
    composition = material.get("composition")
    shares = material.get("feedstock_shares")
    if not composition or not shares:
        return None

    fiber_fraction = float(composition.get("cellulose_fiber", 0.0))
    if fiber_fraction <= 0:
        return None

    rows: List[Dict[str, Any]] = []
    total_ha = 0.0
    for feed_id, share in shares.items():
        feed = materials.get(feed_id)
        rng = as_range(feed.get("cultivation", {}).get("yield_t_ha_yr"))
        if rng is None:
            continue
        y_mid = (rng[0] + rng[1]) / 2.0
        needed_t_yr = demand_t_yr * fiber_fraction * float(share)
        ha = needed_t_yr / (y_mid * utilization)
        total_ha += ha
        rows.append(
            {
                "feedstock": feed_id,
                "share": float(share),
                "yield_t_ha_yr": y_mid,
                "needed_t_yr": needed_t_yr,
                "hectares": ha,
            }
        )
    return {
        "id": material.get("id", "?"),
        "demand_t_yr": demand_t_yr,
        "fiber_fraction": fiber_fraction,
        "utilization": utilization,
        "rows": rows,
        "total_hectares": total_ha,
    }


def footprint_ledger(
    material: Dict[str, Any],
    demand_t_yr: float,
    utilization: float = DEFAULT_UTILIZATION,
    stacking: int = 1,
    uplift: float = 1.0,
) -> Optional[Dict[str, Any]]:
    """Footprint compression for greenhouse/vertical cultivation (farmplex).

    field_ha  = demand / (yield * utilization)          [open-field scenario]
    footprint = field_ha / (greenhouse_uplift * floors) [farmplex scenario]

    Honest applicability: food, algae and nursery crops. Structural fiber
    (bamboo/hemp at 20-30 t/ha/yr) is field agronomy — stacking does not
    apply to 20 m culms. The farmplex's fiber-adjacent use is nursery
    propagation stock (shortening stand lead time), not biomass.
    AEFRI v0.2 gate: indoor staples only after MEASURED kWh/kg
    (AeroFarms/Bowery/Plenty cautionary record).
    """
    rng = as_range(material.get("cultivation", {}).get("yield_t_ha_yr"))
    if rng is None:
        return None
    y = (rng[0] + rng[1]) / 2.0
    field_ha = demand_t_yr / (y * utilization)
    factor = float(uplift) * max(int(stacking), 1)
    return {
        "id": material.get("id", "?"),
        "demand_t_yr": demand_t_yr,
        "yield_t_ha_yr": y,
        "utilization": utilization,
        "field_hectares": round(field_ha, 1),
        "greenhouse_uplift_x": float(uplift),
        "stacking_floors": int(stacking),
        "compression_x": factor,
        "footprint_hectares": round(field_ha / factor, 1) if factor else round(field_ha, 1),
        "note": (
            "applies to food/algae/nursery crops; structural fiber remains "
            "field agronomy; AEFRI v0.2 gate: MEASURED kWh/kg before indoor staples"
        ),
    }


def power_ledger(
    material: Dict[str, Any],
    demand_kg_yr: float,
    capacity_factor: float = 0.25,
    pv_ha_per_mw: float = 1.5,
) -> Optional[Dict[str, Any]]:
    """Atmospheric-family ledger: the 'field' is the renewable array.

    For materials whose feedstock regrows from the atmosphere (CIL diamond,
    CVD graphene), cultivation area is meaningless; the binding resource is
    renewable power. 1 MW nameplate delivers 31,536,000 MJ/yr at full
    capacity; at capacity_factor it delivers 31,536,000 * CF.

        mw_nameplate = demand_kg * energy_mj_kg / (31,536,000 * CF)
        pv_hectares  = mw_nameplate * pv_ha_per_mw
    """
    e = mid(material.get("processing_energy_mj_kg")) or 0.0
    if e <= 0:
        return None
    mj_per_mw_year = 31_536_000.0 * capacity_factor
    mj_per_year = demand_kg_yr * e
    mw = mj_per_year / mj_per_mw_year
    return {
        "id": material.get("id", "?"),
        "demand_kg_yr": demand_kg_yr,
        "energy_mj_kg": e,
        "energy_gwh_yr": round(mj_per_year / 3.6e6, 2),
        "capacity_factor": capacity_factor,
        "mw_nameplate": round(mw, 3),
        "pv_ha_per_mw": pv_ha_per_mw,
        "pv_hectares": round(mw * pv_ha_per_mw, 2),
        "kg_per_mw_yr": round(demand_kg_yr / mw, 1) if mw > 0 else None,
    }


def monte_carlo_lca(
    material: Dict[str, Any],
    n: int = 1000,
    seed: int = 42,
    grid: str = "renewable",
) -> Dict[str, Any]:
    """Seeded uncertainty band over the analytic LCA (hybrid fidelity)."""
    rng = random.Random(seed)
    grid_factor = GRIDS.get(grid, GRIDS["renewable"])

    e_rng = as_range(material.get("processing_energy_mj_kg"))
    if e_rng is None:
        e_rng = (0.0, 0.0)
    if e_rng[0] == e_rng[1]:  # scalar: +/-20% band
        e_rng = (e_rng[0] * 0.8, e_rng[0] * 1.2)

    c_base = float(material.get("carbon_fraction", 0.45))
    perm_base = float(material.get("permanence", 0.8))
    soil = float(material.get("soil_carbon_credit", 0.0))

    samples: List[float] = []
    for _ in range(n):
        e = rng.uniform(*e_rng)
        c = c_base * rng.uniform(0.9, 1.1)
        perm = min(max(perm_base * rng.uniform(0.95, 1.05), 0.0), 1.0)
        uptake = c * CO2_PER_C
        samples.append(e * grid_factor - uptake * perm - soil)

    samples.sort()

    def pct(p: float) -> float:
        idx = min(int(p * (len(samples) - 1)), len(samples) - 1)
        return samples[idx]

    return {
        "id": material.get("id", "?"),
        "n": n,
        "seed": seed,
        "p5": pct(0.05),
        "p50": pct(0.50),
        "p95": pct(0.95),
        "mean": sum(samples) / len(samples),
    }
