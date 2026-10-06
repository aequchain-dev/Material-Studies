"""Tests for efemat.simulate — LCA, cost, loops, land, Monte-Carlo.

The DLGC tests are the calibration showcase: the analytic model must
reproduce the corpus spec (net -2.1 kg CO2/kg) from first principles.
"""

import unittest

from efemat import simulate
from efemat.registry import load_materials


class TestSimulate(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()
        self.dlgc = self.materials.get("dlgc")

    def test_biogenic_uptake_dlgc(self):
        uptake = simulate.biogenic_uptake(self.dlgc)
        # 0.52*0.44 + 0.38*0.61 + 0.05*0.70 + 0.05*0 = 0.4956 C; x 44/12
        self.assertAlmostEqual(uptake, 0.4956 * 44.0 / 12.0, places=3)

    def test_lca_dlgc_reproduces_corpus(self):
        row = simulate.lca(self.dlgc, grid="renewable")
        self.assertLess(row["net_carbon"], -1.8)
        self.assertGreater(row["net_carbon"], -2.5)
        self.assertLessEqual(abs(row["net_carbon"] - (-2.1)), 0.25)

    def test_lca_baseline_override(self):
        row = simulate.lca(self.materials.get("steel_virgin"))
        self.assertTrue(row["override"])
        self.assertAlmostEqual(row["net_carbon"], 2.1)

    def test_cost_trajectory(self):
        traj = simulate.cost_trajectory(self.dlgc, years=20)
        by_year = {p["year"]: p for p in traj}
        self.assertAlmostEqual(by_year[0]["multiplier"], 1.6)
        self.assertAlmostEqual(by_year[5]["multiplier"], 1.0)
        self.assertAlmostEqual(by_year[20]["multiplier"], 0.05)
        mults = [p["multiplier"] for p in traj]
        self.assertEqual(mults, sorted(mults, reverse=True))  # monotone decay

    def test_loop_dynamics(self):
        result = simulate.loop_dynamics(self.dlgc, 1_150_000, years=50)
        self.assertIsNotNone(result["years_to_80pct_secondary"])
        self.assertGreaterEqual(result["years_to_80pct_secondary"], 8)
        self.assertLessEqual(result["years_to_80pct_secondary"], 10)
        self.assertIsNone(result["years_to_95pct_secondary"])  # recovery 0.85 < 0.95
        self.assertAlmostEqual(result["steady_state_virgin_t_yr"], 1_150_000 * 0.15, places=-2)

    def test_land_ledger(self):
        land = simulate.land_ledger(self.dlgc, 1_150_000, self.materials)
        self.assertIsNotNone(land)
        self.assertEqual(len(land["rows"]), 2)
        self.assertGreater(land["total_hectares"], 100_000)
        for row in land["rows"]:
            self.assertGreater(row["hectares"], 0)

    def test_monte_carlo_reproducible(self):
        a = simulate.monte_carlo_lca(self.dlgc, n=500, seed=42)
        b = simulate.monte_carlo_lca(self.dlgc, n=500, seed=42)
        self.assertEqual(a, b)  # REPLICABLE: same seed, same result
        self.assertLessEqual(a["p5"], a["p50"])
        self.assertLessEqual(a["p50"], a["p95"])


if __name__ == "__main__":
    unittest.main()
