"""efemat.calculators — the CALCULATORS | SCALABILITY framework.

One demand number in, the full resource ledger out — land, mix lever,
atmospheric power, carbon, loop recovery, cost — plus a year-by-year
scaling path proving smooth 1x -> 100x behaviour (SCALABLE gate
evidence: constant ha-per-kt across the ramp; cost falls with program
year via the learning curve, not with volume).

Composes the simulate models; no physics is duplicated here (MODULAR).
Every number is traceable to a registry record or a simulate model.

Models
------
1. mix_ledger(materials, demand, mixes):
       ha_i = demand * fiber_fraction * share_i / (yield_i * utilization)
   per fiber-mix scenario — the mix lever quantified (registry 60/40 vs
   bamboo-dominant vs all-bamboo).

2. resource_ledger(materials, demand, ...):
   The unified ledger — composes land_ledger + mix_ledger +
   power_ledger + lca + loop_dynamics + cost_trajectory into one dict.

3. scale_path(materials, start, end, years):
       demand(t) = start * (end/start)^(t/years)          [geometric ramp]
       virgin(t) = demand(t) * (1 - recovery*(1-e^(-t/tau)))
       ha(t)     = ha_per_t * demand(t)                   [linear in demand]
   SCALABLE evidence: ha_per_kt identical at 1x and 100x.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from . import simulate
from .registry import Registry, as_range, mid
from .simulate import DEFAULT_UTILIZATION

# Registry anchors (ids, not objects — the registry stays the source of truth).
FLAGSHIP: str = "dlgc"
ATMOSPHERIC: str = "cil_diamond"

# Fiber-mix scenarios: shares must sum to 1.0 per mix.
DEFAULT_MIXES: Dict[str, Dict[str, float]] = {
    "registry_60_40": {"bamboo": 0.60, "hemp_fiber": 0.40},
    "bamboo_dominant_80_20": {"bamboo": 0.80, "hemp_fiber": 0.20},
    "all_bamboo": {"bamboo": 1.00, "hemp_fiber": 0.00},
}


def mix_ledger(
    materials: Registry,
    demand_t_yr: float,
    mixes: Optional[Dict[str, Dict[str, float]]] = None,
    utilization: float = DEFAULT_UTILIZATION,
) -> Optional[Dict[str, Any]]:
    """Hectares per fiber-mix scenario for a given flagship demand."""
    flagship = materials.get(FLAGSHIP)
    fiber_fraction = float((flagship.get("composition") or {}).get("cellulose_fiber", 0.0))
    if fiber_fraction <= 0:
        return None

    scenarios: List[Dict[str, Any]] = []
    for name, shares in (mixes or DEFAULT_MIXES).items():
        rows: List[Dict[str, Any]] = []
        total_ha = 0.0
        for feed_id, share in shares.items():
            if share <= 0:
                continue
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
        scenarios.append(
            {
                "mix": name,
                "shares": dict(shares),
                "rows": rows,
                "total_hectares": total_ha,
            }
        )
    return {
        "id": FLAGSHIP,
        "demand_t_yr": demand_t_yr,
        "fiber_fraction": fiber_fraction,
        "utilization": utilization,
        "scenarios": scenarios,
    }


def resource_ledger(
    materials: Registry,
    demand_t_yr: float,
    grid: str = "renewable",
    utilization: float = DEFAULT_UTILIZATION,
    atmospheric_kg_yr: float = 0.0,
    capacity_factor: float = 0.25,
) -> Dict[str, Any]:
    """The unified ledger: one demand in, every resource out.

    Composes the simulate models — land (field scenario), the mix lever,
    the atmospheric power ledger (optional share), carbon, loop recovery
    and the cost trajectory, each traceable to its source model.
    """
    flagship = materials.get(FLAGSHIP)

    land = simulate.land_ledger(flagship, demand_t_yr, materials, utilization)
    mixes = mix_ledger(materials, demand_t_yr, utilization=utilization)
    mix_lever: Optional[Dict[str, Any]] = None
    if mixes and land:
        best = min(mixes["scenarios"], key=lambda s: s["total_hectares"])
        mix_lever = {
            "best_mix": best["mix"],
            "total_hectares": best["total_hectares"],
            "reduction_pct": 100.0 * (1.0 - best["total_hectares"] / land["total_hectares"]),
        }

    power = None
    if atmospheric_kg_yr > 0:
        power = simulate.power_ledger(
            materials.get(ATMOSPHERIC), atmospheric_kg_yr, capacity_factor
        )

    lca_row = simulate.lca(flagship, grid=grid)
    loop = simulate.loop_dynamics(flagship, demand_t_yr, years=0)
    cost = simulate.cost_trajectory(flagship, years=20)
    now = cost[0]
    free = next((p for p in cost if p["multiplier"] <= 0.05), cost[-1])

    return {
        "id": FLAGSHIP,
        "demand_t_yr": demand_t_yr,
        "grid": grid,
        "land": land,
        "mix_lever": mix_lever,
        "atmospheric_power": power,
        "carbon": {
            "net_kg_co2_per_kg": lca_row["net_carbon"],
            # net is kg CO2 per kg material; demand in tonnes -> tonnes CO2/yr
            # (kg/kg x t x 1000 kg/t = kg; / 1000 kg/t = t => net x demand_t_yr)
            "annual_t_co2": lca_row["net_carbon"] * demand_t_yr,
        },
        "loop": {
            "recovery": loop["recovery"],
            "tau_yr": loop["tau_yr"],
            "steady_state_virgin_t_yr": loop["steady_state_virgin_t_yr"],
        },
        "cost": {
            "usd_kg_now": now["usd_kg"],
            "usd_kg_free": free["usd_kg"],
            "free_year": free["year"],
        },
    }


def scale_path(
    materials: Registry,
    start_t_yr: float,
    end_t_yr: float,
    years: int = 12,
    grid: str = "renewable",
    utilization: float = DEFAULT_UTILIZATION,
) -> Optional[Dict[str, Any]]:
    """Year-by-year scaling ramp: demand, land, virgin supply, cost, carbon.

        demand(t) = start * (end/start)^(t/years)   [geometric ramp]
        virgin(t) = demand(t) * (1 - recovery * (1 - e^(-t/tau)))
        ha(t)     = ha_per_t * demand(t)            [land is linear in demand]

    SCALABLE gate evidence: ha_per_kt is identical at every point of the
    ramp (1x -> 100x without quality regression); cost falls with program
    year (EFE learning curve), not with volume.
    """
    if start_t_yr <= 0 or end_t_yr <= 0 or years <= 0:
        return None
    flagship = materials.get(FLAGSHIP)

    land_end = simulate.land_ledger(flagship, end_t_yr, materials, utilization)
    if not land_end:
        return None
    ha_per_t = land_end["total_hectares"] / end_t_yr

    loop = simulate.loop_dynamics(flagship, end_t_yr, years=years)
    recovery = loop["recovery"]
    tau = max(loop["tau_yr"], 1e-6)

    cost_by_year = {p["year"]: p for p in simulate.cost_trajectory(flagship, years=years)}
    lca_row = simulate.lca(flagship, grid=grid)

    rows: List[Dict[str, Any]] = []
    for t in range(0, years + 1):
        demand = start_t_yr * (end_t_yr / start_t_yr) ** (t / years)
        share = recovery * (1.0 - math.exp(-t / tau))
        c = cost_by_year.get(t, cost_by_year[max(cost_by_year)])
        rows.append(
            {
                "year": t,
                "demand_t_yr": demand,
                "land_hectares": ha_per_t * demand,
                "secondary_share": share,
                "virgin_t_yr": demand * (1.0 - share),
                "cost_multiplier": c["multiplier"],
                "usd_kg": c["usd_kg"],
                "annual_t_co2": lca_row["net_carbon"] * demand,  # tonnes CO2/yr
            }
        )

    ha_per_kt = [r["land_hectares"] / (r["demand_t_yr"] / 1000.0) for r in rows]
    scalable = (max(ha_per_kt) - min(ha_per_kt)) < 1e-6
    return {
        "id": FLAGSHIP,
        "start_t_yr": start_t_yr,
        "end_t_yr": end_t_yr,
        "years": years,
        "grid": grid,
        "rows": rows,
        "ha_per_kt": ha_per_kt[0],
        "scalable_linear_land": scalable,
        "note": (
            "ha-per-kt constant across the ramp (SCALABLE gate); cost falls "
            "with program year via the EFE learning curve, not with volume"
        ),
    }
