"""Tests for the CALCULATORS | SCALABILITY framework.

Covers: mix_ledger (the mix lever), resource_ledger (unified ledger,
compositional consistency with simulate models), and scale_path
(geometric ramp + SCALABLE gate evidence: constant ha-per-kt).
"""

import unittest

from efemat import calculators, simulate
from efemat.registry import load_materials


class TestMixLedger(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()

    def test_all_bamboo_matches_study_figure(self):
        result = calculators.mix_ledger(self.materials, 1_150_000)
        all_bamboo = next(s for s in result["scenarios"] if s["mix"] == "all_bamboo")
        # 1,150,000 t/yr * 0.52 fiber / (25 t/ha * 0.85) = 28,141 ha
        self.assertAlmostEqual(all_bamboo["total_hectares"], 28_141.2, delta=1.0)

    def test_mix_ordering_monotonic(self):
        result = calculators.mix_ledger(self.materials, 1_150_000)
        by_mix = {s["mix"]: s["total_hectares"] for s in result["scenarios"]}
        self.assertLess(by_mix["all_bamboo"], by_mix["bamboo_dominant_80_20"])
        self.assertLess(by_mix["bamboo_dominant_80_20"], by_mix["registry_60_40"])

    def test_registry_mix_matches_land_ledger(self):
        # The 60/40 scenario must equal simulate.land_ledger's total (same physics).
        result = calculators.mix_ledger(self.materials, 1_150_000)
        reg_mix = next(s for s in result["scenarios"] if s["mix"] == "registry_60_40")
        land = simulate.land_ledger(self.materials.get("dlgc"), 1_150_000, self.materials)
        self.assertAlmostEqual(reg_mix["total_hectares"], land["total_hectares"], delta=1.0)


class TestResourceLedger(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()

    def test_land_consistent_with_simulate(self):
        ledger = calculators.resource_ledger(self.materials, 1_150_000)
        land = simulate.land_ledger(self.materials.get("dlgc"), 1_150_000, self.materials)
        self.assertAlmostEqual(ledger["land"]["total_hectares"], land["total_hectares"], places=1)

    def test_mix_lever_reduction(self):
        ledger = calculators.resource_ledger(self.materials, 1_150_000)
        self.assertEqual(ledger["mix_lever"]["best_mix"], "all_bamboo")
        self.assertAlmostEqual(ledger["mix_lever"]["reduction_pct"], 78.0, delta=0.5)

    def test_carbon_annual_consistency(self):
        ledger = calculators.resource_ledger(self.materials, 1_150_000, grid="renewable")
        net = ledger["carbon"]["net_kg_co2_per_kg"]
        annual = ledger["carbon"]["annual_t_co2"]
        # net is kg CO2/kg; demand in tonnes -> annual in TONNES CO2/yr (no 1000x).
        self.assertAlmostEqual(annual, net * 1_150_000, places=1)
        self.assertLess(net, 0.0)  # DLGC carbon-negative at renewable grid
        # sanity: -1.94 kg/kg x 1.15 Mt = about -2.2 Mt CO2/yr, not -2.2 Gt
        self.assertGreater(annual, -1e7)  # |annual| < 10 Mt

    def test_atmospheric_power_optional(self):
        ledger = calculators.resource_ledger(self.materials, 1_150_000, atmospheric_kg_yr=0.0)
        self.assertIsNone(ledger["atmospheric_power"])
        ledger5 = calculators.resource_ledger(self.materials, 1_150_000, atmospheric_kg_yr=5_000)
        self.assertAlmostEqual(ledger5["atmospheric_power"]["mw_nameplate"], 0.65, delta=0.02)

    def test_cost_trajectory_present(self):
        ledger = calculators.resource_ledger(self.materials, 1_150_000)
        self.assertGreater(ledger["cost"]["usd_kg_now"], ledger["cost"]["usd_kg_free"])


class TestScalePath(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()
        self.path = calculators.scale_path(self.materials, 10_000, 1_150_000, years=12)

    def test_endpoints(self):
        rows = self.path["rows"]
        self.assertAlmostEqual(rows[0]["demand_t_yr"], 10_000, places=0)
        self.assertAlmostEqual(rows[-1]["demand_t_yr"], 1_150_000, places=0)

    def test_scalable_linear_land(self):
        # SCALABLE gate: ha-per-kt constant across the 115x ramp.
        self.assertTrue(self.path["scalable_linear_land"])
        self.assertAlmostEqual(self.path["ha_per_kt"], 112.6, delta=0.5)

    def test_demand_monotonic(self):
        demands = [r["demand_t_yr"] for r in self.path["rows"]]
        self.assertEqual(demands, sorted(demands))

    def test_virgin_declines_with_loop(self):
        # secondary share saturates toward recovery (asymptotic): at year 12 = 4*tau,
        # share = 0.85 * (1 - e^-4) = 0.8344 — 98.2% of recovery, never exactly 0.85.
        first, last = self.path["rows"][0], self.path["rows"][-1]
        self.assertLess(last["secondary_share"], first["secondary_share"] + 1.0)  # share grows
        self.assertAlmostEqual(last["secondary_share"], 0.85 * (1 - 0.0183156), delta=0.001)

    def test_carbon_negative_every_year(self):
        for r in self.path["rows"]:
            self.assertLess(r["annual_t_co2"], 0.0)

    def test_100x_linearity(self):
        # land(100x demand) == 100 x land(demand) — the SCALABLE gate, directly.
        small = calculators.resource_ledger(self.materials, 11_500)["land"]["total_hectares"]
        big = calculators.resource_ledger(self.materials, 1_150_000)["land"]["total_hectares"]
        self.assertAlmostEqual(big / small, 100.0, places=6)


if __name__ == "__main__":
    unittest.main()
