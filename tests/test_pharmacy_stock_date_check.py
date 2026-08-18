import importlib.util,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("tool",Path(__file__).parents[1]/"src/pharmacy_stock_date_check.py"); tool=importlib.util.module_from_spec(spec); spec.loader.exec_module(tool)
class Tests(unittest.TestCase):
 def test_flags_expiring_and_expired_stock(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/"stock.csv"; f.write_text("item_code,expires_on,quantity\nA,2026-08-01,2\nB,2026-08-25,4\nC,2026-11-01,1\n",encoding="utf-8"); rows=tool.scan(f,"2026-08-18",30); self.assertEqual([r["item_code"] for r in rows],["A","B"]); self.assertEqual(rows[0]["state"],"expired")
if __name__=="__main__": unittest.main()
