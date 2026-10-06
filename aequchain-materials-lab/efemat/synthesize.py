"""efemat.synthesize — composite synthesis + corpus calibration.

Rule-of-mixtures longitudinal model with explicit correction factors:

    sigma_composite = densification * alignment * sum_i (V_i * sigma_i)
    E_composite    = alignment * sum_i (V_i * E_i)
    rho_composite  = sum_i (V_i * rho_i)
    specific       = sigma / rho        [MPa per g/cm3]

Correction factors are declared, never hidden:
    alignment      fiber orientation efficiency (0.90-0.95 typical)
    densification  thermo-mechanical compression gain (1.4-1.6 typical)

calibrate_dlgc() reproduces the corpus DLGC spec from first principles
and reports every gap honestly (the corpus's own honesty pattern):
    tensile  ~1100 MPa  -> reproducible with hi-grade fiber + factors
    modulus  >=80 GPa   -> NOT reproducible by rule-of-mixtures;
                           flagged [IN-CORPUS-DISPUTE], carried to residual
    carbon   -2.1 kg/kg -> reproduced by simulate.lca within ~2%
"""

from __future__ import annotations

from typing import Any, Dict

from .registry import Registry, mid
from . import simulate

# Component property library — [LITERATURE] midpoints, hi-grade upper band.
COMPONENTS: Dict[str, Dict[str, float]] = {
    "cellulose_fiber": {
        "tensile_mpa": 950.0, "tensile_hi_mpa": 1100.0,
        "modulus_gpa": 40.0, "modulus_hi_gpa": 60.0,
        "density_g_cm3": 1.50, "carbon_fraction": 0.44,
    },
    "lignin_resin": {
        "tensile_mpa": 50.0, "tensile_hi_mpa": 60.0,
        "modulus_gpa": 2.5, "modulus_hi_gpa": 3.0,
        "density_g_cm3": 1.30, "carbon_fraction": 0.61,
    },
    "bio_graphene": {
        "tensile_mpa": 3000.0, "tensile_hi_mpa": 3500.0,
        "modulus_gpa": 250.0, "modulus_hi_gpa": 300.0,
        "density_g_cm3": 2.10, "carbon_fraction": 0.70,
    },
    "hemp_fiber": {
        "tensile_mpa": 700.0, "tensile_hi_mpa": 900.0,
        "modulus_gpa": 35.0, "modulus_hi_gpa": 45.0,
        "density_g_cm3": 1.48, "carbon_fraction": 0.45,
    },
    "flax_fiber": {
        "tensile_mpa": 650.0, "tensile_hi_mpa": 900.0,
        "modulus_gpa": 30.0, "modulus_hi_gpa": 40.0,
        "density_g_cm3": 1.40, "carbon_fraction": 0.44,
    },
    "biochar": {
        "tensile_mpa": 20.0, "tensile_hi_mpa": 30.0,
        "modulus_gpa": 5.0, "modulus_hi_gpa": 8.0,
        "density_g_cm3": 0.40, "carbon_fraction": 0.70,
    },
    "additives": {
        "tensile_mpa": 30.0, "tensile_hi_mpa": 30.0,
        "modulus_gpa": 1.0, "modulus_hi_gpa": 1.0,
        "density_g_cm3": 1.50, "carbon_fraction": 0.0,
    },
}

CORPUS_DLGC_SPEC: Dict[str, float] = {
    "tensile_mpa": 1100.0,
    "modulus_gpa": 80.0,
    "density_g_cm3": 1.35,
    "net_carbon_kg_co2_kg": -2.1,
}


def composite(
    fractions: Dict[str, float],
    alignment: float = 0.92,
    densification: float = 1.5,
    grade: str = "mid",
) -> Dict[str, Any]:
    """Synthesize a composite from component volume fractions."""
    total = sum(fractions.values())
    if abs(total - 1.0) > 0.02:
        raise ValueError(f"fractions must sum to 1.0 (+/-0.02), got {total:.4f}")
    unknown = [k for k in fractions if k not in COMPONENTS]
    if unknown:
        raise KeyError(f"unknown components: {', '.join(unknown)}; known: {', '.join(COMPONENTS)}")

    hi = grade == "hi"
    sigma = 0.0
    modulus = 0.0
    density = 0.0
    carbon_uptake = 0.0
    for name, frac in fractions.items():
        comp = COMPONENTS[name]
        s = comp["tensile_hi_mpa"] if hi else comp["tensile_mpa"]
        e = comp["modulus_hi_gpa"] if hi else comp["modulus_gpa"]
        sigma += frac * s
        modulus += frac * e
        density += frac * comp["density_g_cm3"]
        carbon_uptake += frac * comp["carbon_fraction"] * simulate.CO2_PER_C

    sigma *= densification * alignment
    modulus *= alignment

    return {
        "fractions": dict(fractions),
        "grade": grade,
        "alignment": alignment,
        "densification": densification,
        "tensile_mpa": round(sigma, 1),
        "modulus_gpa": round(modulus, 1),
        "density_g_cm3": round(density, 3),
        "specific_strength": round(sigma / density, 1),
        "biogenic_uptake_kg_co2_kg": round(carbon_uptake, 3),
        "model": "rule-of-mixtures (longitudinal) x densification x alignment",
    }


def calibrate_dlgc(materials: Registry) -> Dict[str, Any]:
    """Reproduce the corpus DLGC spec from the component library."""
    dlgc = materials.get("dlgc")
    composition = dlgc.get("composition", {})
    result = composite(
        composition,
        alignment=0.95,
        densification=1.5,
        grade="hi",
    )
    lca_row = simulate.lca(dlgc, grid="renewable")

    checks = []
    for key, model_value in (
        ("tensile_mpa", result["tensile_mpa"]),
        ("modulus_gpa", result["modulus_gpa"]),
        ("density_g_cm3", result["density_g_cm3"]),
        ("net_carbon_kg_co2_kg", lca_row["net_carbon"]),
    ):
        spec_value = CORPUS_DLGC_SPEC[key]
        delta_pct = (model_value - spec_value) / abs(spec_value) * 100.0
        ok = abs(delta_pct) <= 10.0
        checks.append(
            {
                "property": key,
                "corpus_spec": spec_value,
                "model": round(model_value, 2),
                "delta_pct": round(delta_pct, 1),
                "within_10pct": ok,
                "flag": "" if ok else "[IN-CORPUS-DISPUTE] rule-of-mixtures cannot reach spec; requires nanocellulose-graphene synergy beyond the model — carried to residual ledger",
            }
        )

    return {
        "material": "dlgc",
        "synthesis": result,
        "lca": lca_row,
        "checks": checks,
        "calibrated": all(c["within_10pct"] for c in checks),
    }
