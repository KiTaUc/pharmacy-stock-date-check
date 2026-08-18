from __future__ import annotations
import argparse,csv,json
from datetime import date
from pathlib import Path
def scan(csv_path, today, days=30):
 today=date.fromisoformat(today); result=[]
 with csv_path.open(encoding="utf-8",newline="") as f:
  for row in csv.DictReader(f):
   required={"item_code","expires_on","quantity"}
   if not required.issubset(row): raise ValueError("CSV должен содержать item_code, expires_on, quantity")
   left=(date.fromisoformat(row["expires_on"])-today).days
   if left<=days: result.append({**row,"days_left":left,"state":"expired" if left<0 else "attention"})
 return sorted(result,key=lambda r:r["days_left"])
def main():
 p=argparse.ArgumentParser(); p.add_argument("csv",type=Path); p.add_argument("--today",required=True); p.add_argument("--days",type=int,default=30); x=p.parse_args(); print(json.dumps(scan(x.csv,x.today,x.days),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
