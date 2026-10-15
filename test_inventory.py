import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = {
            "P1": {"name": "Apple", "quantity": 2},
            "P2": {"name": "Pear", "quantity": 0},
        }

    def test_add_product(self):
        ok, _ = main.add_product(self.inventory, "P3", "Orange", 5)
        self.assertTrue(ok)
        self.assertEqual(self.inventory["P3"]["quantity"], 5)

    def test_duplicate_id_rejected(self):
        ok, _ = main.add_product(self.inventory, "P1", "Another Apple", 1)
        self.assertFalse(ok)

    def test_update_stock(self):
        ok, _ = main.update_stock(self.inventory, "P1", 3)
        self.assertTrue(ok)
        self.assertEqual(self.inventory["P1"]["quantity"], 5)

    def test_stock_cannot_be_negative(self):
        ok, _ = main.update_stock(self.inventory, "P1", -5)
        self.assertFalse(ok)
        self.assertEqual(self.inventory["P1"]["quantity"], 2)

    def test_remove_product(self):
        ok, _ = main.remove_product(self.inventory, "P1")
        self.assertTrue(ok)
        self.assertNotIn("P1", self.inventory)

    def test_out_of_stock(self):
        self.assertEqual(main.get_out_of_stock(self.inventory), ["P2"])

    def test_export_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "summary.json"
            summary = main.export_summary(self.inventory, target)
            saved = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(summary[0]["id"], "P1")
            self.assertEqual(saved["inventory"][1]["id"], "P2")


if __name__ == "__main__":
    unittest.main()
