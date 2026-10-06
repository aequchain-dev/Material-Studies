"""Tests for efemat.synthesize — rule-of-mixtures + honest calibration.

The calibration test encodes the honesty pattern: tensile and carbon
reproduce the corpus spec; the modulus gap MUST be flagged rather than
hidden (the corpus's own [IN-CORPUS-DISPUTE] discipline).
"""

import unittest

from efemat import synthesize
from efemat.registry import load_materials


class TestSynthesize(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()

    def test_single_component_identity(self):
        result = synthesize.composite(
            {"cellulose_fiber": 1.0}, alignment=1.0, densification=1.0
        )
        self.assertAlmostEqual(result["tensile_mpa"], 950.0, places=1)
        self.assertAlmostEqual(result["density_g_cm3"], 1.50, places=3)

    def test_fraction_validation(self):
        with self.assertRaises(ValueError):
            synthesize.composite({"cellulose_fiber": 0.5, "lignin_resin": 0.2})
        with self.assertRaises(KeyError):
            synthesize.composite({"unobtainium": 1.0})

    def test_calibrate_dlgc(self):
        cal = synthesize.calibrate_dlgc(self.materials)
        by_prop = {c["property"]: c for c in cal["checks"]}
        self.assertTrue(by_prop["tensile_mpa"]["within_10pct"])
        self.assertTrue(by_prop["net_carbon_kg_co2_kg"]["within_10pct"])
        self.assertTrue(by_prop["density_g_cm3"]["within_10pct"])
        self.assertFalse(by_prop["modulus_gpa"]["within_10pct"])  # honest flag
        self.assertFalse(cal["calibrated"])  # the modulus gap keeps it honest
        self.assertIn("IN-CORPUS-DISPUTE", by_prop["modulus_gpa"]["flag"])


if __name__ == "__main__":
    unittest.main()
