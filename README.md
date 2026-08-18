# Pharmacy Stock Date Check

**Pharmacy Stock Date Check** — автономный локальный инструмент для сферы «Аптеки». Ведёт локальный список остатков с датой годности и позволяет выделять позиции для дополнительной проверки.

## Возможности

Программа хранит записи в обычном JSON-файле, проверяет обязательные поля и допустимые статусы, а затем выводит сводку по статусам. Запуск не требует учётной записи, внешнего API или фоновой передачи данных.

## Быстрый старт

```bash
python src/pharmacy_stock_date_check.py --store data/records.json add --item-code "MED-24" --expires-on "2026-09-01" --quantity "12" --status "review"
python src/pharmacy_stock_date_check.py --store data/records.json report
```

## Проверка

```bash
python -m unittest discover -s tests -v
python -m compileall src
```

## Ограничения

Это рабочий журнал для организационных задач, а не замена профильному программному обеспечению, юридической документации, медицинской системе или системе расчётов.
