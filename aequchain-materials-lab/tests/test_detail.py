"""Tests for efemat.detail — study + scoresheet generation.

REPLICABLE gate is tested literally: generate twice, diff == 0.
"""

import tempfile
import unittest
from pathlib import Path

from efemat import detail
from efemat.registry import load_materials, load_pillars, load_processes


class TestDetail(unittest.TestCase):
    def setUp(self):
        self.materials = load_materials()
        self.processes = load_processes()
        self.pillars = load_pillars()

    def test_generate_study(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "study.md"
            stats = detail.generate_study(
                self.materials, self.processes, self.pillars, out_path=out
            )
            self.assertEqual(stats["validation_errors"], 0)
            self.assertGreater(stats["lines"], 200)
            content = out.read_text(encoding="utf-8")
            for marker in (
                "§I", "§II", "§III", "§IV", "§V", "§VI",
                "§VII", "§VIII", "§IX", "§X", "§XI",
            ):
                self.assertIn(marker, content)
            self.assertIn("REPLICABLE", content)
            self.assertIn("dlgc", content)

    def test_study_replicable(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.md"
            b = Path(tmp) / "b.md"
            detail.generate_study(self.materials, self.processes, self.pillars, out_path=a)
            detail.generate_study(self.materials, self.processes, self.pillars, out_path=b)
            self.assertEqual(
                a.read_text(encoding="utf-8"),
                b.read_text(encoding="utf-8"),
            )

    def test_scoresheet(self):
        sheet = detail.scoresheet("dlgc", self.materials, self.processes, self.pillars)
        self.assertIn("DLGC", sheet)
        self.assertIn("NET CARBON", sheet)
        self.assertIn("EFE", sheet)


if __name__ == "__main__":
    unittest.main()
