from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

FIELDS = [
    "item_code",
    "expires_on",
    "quantity",
    "status"
]
STATUSES = [
    "active",
    "review",
    "removed"
]
RECORD_NAME = "позиция остатка"

def load_records(store: Path) -> list[dict[str, str]]:
    if not store.exists():
        return []
    content = json.loads(store.read_text(encoding="utf-8"))
    if not isinstance(content, list):
        raise ValueError("Файл хранилища должен содержать JSON-массив")
    return content

def save_records(store: Path, records: list[dict[str, str]]) -> None:
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def add_record(store: Path, payload: dict[str, str]) -> dict[str, str]:
    missing = [field for field in FIELDS if not str(payload.get(field, "")).strip()]
    if missing:
        raise ValueError("Не заполнены поля: " + ", ".join(missing))
    if payload["status"] not in STATUSES:
        raise ValueError("Недопустимый статус: " + payload["status"])
    record = {field: str(payload[field]).strip() for field in FIELDS}
    records = load_records(store)
    records.append(record)
    save_records(store, records)
    return record

def build_report(store: Path) -> dict[str, object]:
    records = load_records(store)
    statuses = Counter(record["status"] for record in records)
    return {"record_name": RECORD_NAME, "total": len(records), "by_status": dict(sorted(statuses.items()))}

def main() -> None:
    parser = argparse.ArgumentParser(description=f"Локальный реестр: {RECORD_NAME}")
    parser.add_argument("--store", type=Path, default=Path("data/records.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Добавить запись")
    for field in FIELDS:
        add.add_argument(f"--{field.replace('_', '-')}", dest=field, required=True)
    commands.add_parser("report", help="Показать сводку")
    args = parser.parse_args()
    if args.command == "add":
        record = add_record(args.store, {field: getattr(args, field) for field in FIELDS})
        print(json.dumps(record, ensure_ascii=False))
    else:
        print(json.dumps(build_report(args.store), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
