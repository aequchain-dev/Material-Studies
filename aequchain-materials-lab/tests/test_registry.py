"""Tests for efemat.registry — loading, validation, range handling."""

import unittest

from efemat.registry import as_range, load_materials, load_pillars, load_processes, mid


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()
        self.processes = load_processes()
        self.pillars = load_pillars()

    def test_counts(self):
        self.assertEqual(len(self.materials.records), 29)
        self.assertEqual(len(self.materials.filter(**{"class": "replenishable"})), 22)
        self.assertEqual(len(self.materials.filter(**{"class": "baseline"})), 7)
        self.assertEqual(len(self.processes.records), 26)

    def test_validate(self):
        self.assertEqual(self.materials.validate(), [])
        self.assertEqual(self.processes.validate(), [])

    def test_get_dlgc(self):
        m = self.materials.get("dlgc")
        self.assertEqual(m["status"], "SPEC")
        self.assertAlmostEqual(m["carbon_fraction"], 0.50)
        with self.assertRaises(KeyError):
            self.materials.get("does-not-exist")

    def test_stages(self):
        self.assertEqual(len(self.processes.by_stage("cultivation")), 12)
        self.assertEqual(len(self.processes.by_stage("generation")), 8)
        self.assertEqual(len(self.processes.by_stage("manufacture")), 6)

    def test_cea_product_pair_registered(self):
        crop = self.processes.get("aequcrop")
        grow = self.processes.get("aequgrow")
        self.assertEqual(crop["stage"], "cultivation")
        self.assertEqual(grow["stage"], "cultivation")
        self.assertIn("AEQUFAB", crop["key_params"]["self_replication"])
        self.assertGreater(grow["key_params"]["yield_density_plants_m2"][0], 200)
        self.assertLess(grow["key_params"]["net_water_loss_l_day"], 1.0)

    def test_thanceln_glazing_registered(self):
        t = self.materials.get("thanceln")
        self.assertEqual(t["class"], "replenishable")
        self.assertEqual(t["family"], "biological")
        self.assertGreaterEqual(t["optical"]["transmittance_pct"][0], 85)  # meets grow-core PAR spec
        crop = self.processes.get("aequcrop")
        self.assertIn("Thanceln", crop["key_params"]["glazing_upgrade"])
        self.assertIn("lignin_resin", crop["key_params"]["glazing_upgrade"])  # loop closure to DLGC

    def test_as_range(self):
        self.assertEqual(as_range(5), (5.0, 5.0))
        self.assertEqual(as_range([1, 2]), (1.0, 2.0))
        self.assertEqual(as_range([2, 1]), (1.0, 2.0))  # auto-swap
        self.assertIsNone(as_range(None))
        self.assertEqual(mid([2, 4]), 3.0)
        self.assertIsNone(mid(None))

    def test_pillars_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(self.pillars["weights"].values()), 1.0)


if __name__ == "__main__":
    unittest.main()
