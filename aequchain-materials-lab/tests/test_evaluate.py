"""Tests for efemat.evaluate — EFE scoring, ladder, risk classes."""

import unittest

from efemat import evaluate
from efemat.registry import load_materials, load_pillars


class TestEvaluate(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()
        self.pillars = load_pillars()

    def test_efe_score_dlgc(self):
        sc = evaluate.efe_score(self.materials.get("dlgc"), self.pillars)
        # (10*.2 + 9*.15 + 9*.15 + 9*.15 + 9*.1 + 8*.1 + 9*.15) * 10 = 91.0
        self.assertAlmostEqual(sc["score"], 91.0, places=1)
        self.assertEqual(sc["grade"], "A+")

    def test_efe_bounds_all_materials(self):
        for m in self.materials.records.values():
            sc = evaluate.efe_score(m, self.pillars)
            self.assertGreaterEqual(sc["score"], 0.0)
            self.assertLessEqual(sc["score"], 100.0)

    def test_ladder(self):
        lad = evaluate.ladder_info(self.materials.get("dlgc"))
        self.assertEqual(lad["primary_rung"], 1)
        self.assertEqual(lad["primary_label"], "SUBSTITUTE")
        self.assertIn(3, lad["supporting_rungs"])

    def test_risk_class(self):
        rc = evaluate.risk_class(self.materials.get("dlgc"))
        self.assertEqual(rc["class"], "HIGH")  # worst 3x4 = 12
        self.assertEqual(rc["n_risks"], 3)

    def test_risk_critical_and_none(self):
        synthetic = {"id": "x", "risks": [{"risk": "worst", "likelihood": 5, "impact": 5}]}
        self.assertEqual(evaluate.risk_class(synthetic)["class"], "CRITICAL")
        empty = {"id": "y", "risks": []}
        self.assertEqual(evaluate.risk_class(empty)["class"], "NONE")


if __name__ == "__main__":
    unittest.main()
