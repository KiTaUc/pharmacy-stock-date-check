import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "src" / "pharmacy_stock_date_check.py"
spec = importlib.util.spec_from_file_location("tool", MODULE)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)

class ToolTests(unittest.TestCase):
    def test_add_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "records.json"
            record = tool.add_record(store, {
  "item_code": "MED-24",
  "expires_on": "2026-09-01",
  "quantity": "12",
  "status": "review"
})
            self.assertEqual(record["status"], "review")
            report = tool.build_report(store)
            self.assertEqual(report["total"], 1)
            self.assertEqual(report["by_status"], {"review": 1})

    def test_rejects_unknown_status(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                tool.add_record(Path(directory) / "records.json", {field: "x" for field in tool.FIELDS} | {"status": "unknown"})

if __name__ == "__main__":
    unittest.main()
