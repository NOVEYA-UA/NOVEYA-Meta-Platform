#!/usr/bin/env python3
"""
Эталонные значения KPI для всех 8 секторов Σ-MATRIX-24.
Источник норм: Нотация.txt (Metatron-8 / NOVEYA).

Запуск: python seed_sector_kpis.py
Данные вставляются с INSERT OR REPLACE — безопасно перезапускать.

Хранятся СЫРЫЕ значения (не нормализованные) — нормализация
происходит в SectorDataConnector при вычислении.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "metatron_core.db"

# ------------------------------------------------------------------
# Эталонные значения по секторам (реалистичные стартовые данные)
#
# S1 — Энергия/ТЭЦ/Микросети
#   energy_availability: доля времени работы (0–1)
#   repair_time: среднее время ремонта, часы (меньше = лучше, норма ≤ 24)
#
# S2 — Вода/Источники/Санитария
#   water_access_pct: доля домохозяйств с доступом (0–1, цель 1.0)
#   liters_per_day: литров на чел/день (норма ≥ 50)
#
# S3 — Почва/Экология/Регенерация
#   regen_index: индекс регенерации почвы (0–1, норма ≥ 0.7)
#   organic_pct: доля органического слоя (0–1, норма ≥ 0.3)
#
# S4 — Агро/Фермеры/Логистика
#   days_of_supply: запас дней продовольствия (норма ≥ 14)
#   price_spread: разброс цен на рынке (0–1, меньше = лучше, норма ≤ 0.15)
#
# S5 — Экономика/Тариф/Прозрачность
#   payment_trace_pct: доля платежей со следом/квитанцией (0–1, цель 1.0)
#
# S6 — Право/Претензии/Арбитраж
#   time_to_resolve_h: среднее время разрешения претензии, часы (норма ≤ 72)
#
# S7 — Безопасность/Аудит
#   anomaly_false_positive: доля ложных срабатываний (0–1, норма ≤ 0.05)
#
# S8 — Громада/Культура/Синхронизация
#   engagement_pct: доля участвующих граждан (0–1, норма ≥ 0.6)
#   satisfaction: индекс удовлетворённости (0–1, норма ≥ 0.7)
# ------------------------------------------------------------------

SEED_DATA = [
    # (sector_id, kpi_name, kpi_value)
    ("S1", "energy_availability",    0.97),
    ("S1", "repair_time",           16.0),   # часы — хорошо, < 24

    ("S2", "water_access_pct",       0.92),
    ("S2", "liters_per_day",        58.0),

    ("S3", "regen_index",            0.68),  # чуть ниже нормы 0.7
    ("S3", "organic_pct",            0.31),

    ("S4", "days_of_supply",        18.0),
    ("S4", "price_spread",           0.11),

    ("S5", "payment_trace_pct",      0.89),  # 89% — есть куда расти

    ("S6", "time_to_resolve_h",     52.0),   # часы — хорошо, < 72

    ("S7", "anomaly_false_positive", 0.032), # хорошо, < 0.05

    ("S8", "engagement_pct",         0.65),
    ("S8", "satisfaction",           0.74),
]


def seed(db_path: Path = DB_PATH) -> None:
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sector_kpis (
            sector_id   TEXT NOT NULL,
            kpi_name    TEXT NOT NULL,
            kpi_value   REAL NOT NULL,
            updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (sector_id, kpi_name)
        )
    """)
    conn.executemany(
        "INSERT OR REPLACE INTO sector_kpis (sector_id, kpi_name, kpi_value) VALUES (?,?,?)",
        SEED_DATA,
    )
    conn.commit()
    conn.close()
    print(f"Загружено {len(SEED_DATA)} KPI по 8 секторам → {db_path}")


if __name__ == "__main__":
    seed()

    # Быстрая проверка через SectorDataConnector
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from sector_connector import SectorDataConnector

    c = SectorDataConnector(DB_PATH)
    health = c.compute_system_health()
    print(f"\nСостояние системы после seed:")
    print(f"  Секторов: {health['sectors']}")
    print(f"  Coherence: {health['coherence']}")
    print(f"  Entropy:   {health['entropy']}")

    print("\nПроверка нормализации S1:")
    s1 = c.compute_sector_health("S1")
    for k, v in s1["norm_kpis"].items():
        raw = s1["raw_kpis"][k]
        print(f"  {k}: raw={raw} → norm={v}")

    violations = c.find_violations()
    if violations:
        print("\nНарушения норм:")
        for sid, issues in violations.items():
            for issue in issues:
                print(f"  [{sid}] {issue}")
    else:
        print("\nНарушений норм не обнаружено.")
