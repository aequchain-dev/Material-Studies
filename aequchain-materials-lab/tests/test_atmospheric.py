"""Tests for the atmospheric family + footprint compression (concept upgrade).

Covers: CIL diamond as an atmospheric replenishable, the power ledger
(the PV array as the 'field'), grid-sensitivity of the per-kg carbon
sign, and farmplex footprint compression.
"""

import unittest

from efemat import simulate
from efemat.registry import load_materials


class TestAtmospheric(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()
        self.diamond = self.materials.get("cil_diamond")

    def test_diamond_is_replenishable_atmospheric(self):
        self.assertEqual(self.diamond["class"], "replenishable")
        self.assertEqual(self.diamond["family"], "atmospheric")
        self.assertAlmostEqual(self.diamond["carbon_fraction"], 1.0)

    def test_diamond_uptake_is_stoichiometric(self):
        # 1 kg diamond = 1 kg C = 44/12 kg CO2 consumed from the sky
        self.assertAlmostEqual(simulate.biogenic_uptake(self.diamond), 44.0 / 12.0, places=3)

    def test_diamond_carbon_sign_grid_dependent(self):
        # The honest finding: positive on realistic grids, negative only at ~zero
        self.assertAlmostEqual(simulate.lca(self.diamond, grid="renewable")["net_carbon"], 16.85, places=1)
        self.assertAlmostEqual(simulate.lca(self.diamond, grid="efe")["net_carbon"], 1.46, places=1)
        self.assertAlmostEqual(simulate.lca(self.diamond, grid="zero")["net_carbon"], -44.0 / 12.0, places=2)
        self.assertGreater(simulate.lca(self.diamond, grid="world")["net_carbon"], 100.0)

    def test_power_ledger(self):
        pl = simulate.power_ledger(self.diamond, 1_000)  # 1 t/yr
        self.assertAlmostEqual(pl["mw_nameplate"], 0.13, places=2)
        self.assertAlmostEqual(pl["pv_hectares"], 0.195, places=1)  # rounded to 2dp in output
        self.assertGreater(pl["kg_per_mw_yr"], 7000)
        self.assertLess(pl["kg_per_mw_yr"], 8500)

    def test_power_ledger_scales_linearly(self):
        a = simulate.power_ledger(self.diamond, 1_000)
        b = simulate.power_ledger(self.diamond, 50_000)
        ratio = b["mw_nameplate"] / a["mw_nameplate"]
        self.assertGreaterEqual(ratio, 49.0)  # 3dp rounding on a 0.13 base
        self.assertLessEqual(ratio, 51.0)

    def test_power_ledger_inapplicable_without_energy(self):
        self.assertIsNone(simulate.power_ledger({"id": "x"}, 1000))

    def test_footprint_ledger_compression(self):
        algae = self.materials.get("algae_biopolymer")
        fp = simulate.footprint_ledger(algae, 100_000, stacking=5, uplift=3.0)
        self.assertIsNotNone(fp)
        self.assertAlmostEqual(fp["compression_x"], 15.0)
        self.assertAlmostEqual(fp["footprint_hectares"], fp["field_hectares"] / 15.0, places=1)
        # structural fiber has no stacking applicability in the model's honest note
        self.assertIn("field agronomy", fp["note"])

    def test_footprint_ledger_needs_yield(self):
        dlgc = self.materials.get("dlgc")  # composite: no cultivation yield
        self.assertIsNone(simulate.footprint_ledger(dlgc, 1_000))

    def test_grids_include_efe_and_zero(self):
        self.assertIn("efe", simulate.GRIDS)
        self.assertIn("zero", simulate.GRIDS)
        self.assertAlmostEqual(simulate.GRIDS["zero"], 0.0)


if __name__ == "__main__":
    unittest.main()
