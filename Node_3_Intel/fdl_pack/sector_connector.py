#!/usr/bin/env python3
"""
SectorDataConnector: подключение logic.py к реальным KPI из metatron_core.db.

Нормализация: сырые значения хранятся в DB (audit trail читаем),
нормализация [0,1] применяется при вычислении когерентности/энтропии.
"""

import sys
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "monolith_v2_1"))
from logic import compute_coherence, compute_entropy, compute_eff

_DEFAULT_DB = _PROJECT_ROOT / "db" / "metatron_core.db"

# ------------------------------------------------------------------
# Нормализация KPI
# (kpi_name: (max_value, inverted))
# inverted=True: lower raw → higher normalized (меньше = лучше)
# inverted=False: higher raw → higher normalized (больше = лучше)
# KPI, которых нет здесь, считаются уже в [0,1]
# ------------------------------------------------------------------
KPI_NORMALIZERS: Dict[str, Tuple[float, bool]] = {
    "repair_time":            (168.0, True),   # часы, max 1 нед
    "time_to_resolve_h":      (240.0, True),   # часы, max 10 дней
    "anomaly_false_positive":  (1.0,  True),   # доля, инверсия
    "liters_per_day":         (200.0, False),  # л/день
    "days_of_supply":          (60.0, False),  # дни запаса
}

# Метрики, где нарушение = actual > threshold (меньше = лучше)
INVERTED_METRICS = {"repair_time", "time_to_resolve_h",
                    "anomaly_false_positive", "price_spread"}

# KPI-нормы по секторам Σ-MATRIX-24 (из Нотация.txt)
# Для INVERTED_METRICS threshold = максимум (нарушение если actual > threshold)
# Для остальных threshold = минимум (нарушение если actual < threshold)
SECTOR_NORMS: Dict[str, Dict[str, float]] = {
    "S1": {"energy_availability": 0.95, "repair_time": 24.0},
    "S2": {"water_access_pct": 1.0,     "liters_per_day": 50.0},
    "S3": {"regen_index": 0.7,          "organic_pct": 0.3},
    "S4": {"days_of_supply": 14.0,      "price_spread": 0.15},
    "S5": {"payment_trace_pct": 1.0},
    "S6": {"time_to_resolve_h": 72.0},
    "S7": {"anomaly_false_positive": 0.05},
    "S8": {"engagement_pct": 0.6,       "satisfaction": 0.7},
}


def normalize_kpi(kpi_name: str, raw_value: float) -> float:
    """
    Нормализует сырое значение KPI в [0, 1].
    KPI без записи в KPI_NORMALIZERS возвращается как есть (уже в [0,1]).
    """
    if kpi_name not in KPI_NORMALIZERS:
        return max(0.0, min(raw_value, 1.0))
    max_val, inverted = KPI_NORMALIZERS[kpi_name]
    ratio = max(0.0, min(raw_value / max_val, 1.0))
    return round(1.0 - ratio if inverted else ratio, 4)


class SectorDataConnector:
    """Подключение logic.py к реальным данным из metatron_core.db."""

    def __init__(self, db_path: Path = _DEFAULT_DB):
        self.db_path = Path(db_path)

    # ------------------------------------------------------------------
    # Инициализация таблицы
    # ------------------------------------------------------------------

    def init_table(self) -> None:
        """Создаёт sector_kpis если не существует."""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sector_kpis (
                sector_id   TEXT NOT NULL,
                kpi_name    TEXT NOT NULL,
                kpi_value   REAL NOT NULL,
                updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (sector_id, kpi_name)
            )
        """)
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Чтение данных (сырые значения из DB)
    # ------------------------------------------------------------------

    def get_sector_kpis(self, sector_id: str) -> Dict[str, float]:
        """Сырые KPI сектора из DB. Пустой dict если строк нет."""
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            "SELECT kpi_name, kpi_value FROM sector_kpis WHERE sector_id = ?",
            (sector_id,),
        ).fetchall()
        conn.close()
        return {name: value for name, value in rows}

    def get_all_sectors(self) -> Dict[str, float]:
        """
        {sector_id: mean_normalized_kpi} по всем секторам.
        Нормализация применяется перед усреднением — когерентность корректна.
        """
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            "SELECT sector_id, kpi_name, kpi_value FROM sector_kpis"
        ).fetchall()
        conn.close()

        buckets: Dict[str, List[float]] = {}
        for sector_id, kpi_name, raw_value in rows:
            buckets.setdefault(sector_id, []).append(
                normalize_kpi(kpi_name, raw_value)
            )

        return (
            {sid: round(sum(vals) / len(vals), 4) for sid, vals in buckets.items()}
            if buckets else {}
        )

    # ------------------------------------------------------------------
    # Вычисление здоровья сектора
    # ------------------------------------------------------------------

    def compute_sector_health(self, sector_id: str) -> Dict:
        """
        Применяет logic.py к нормализованным KPI сектора.
        Возвращает coherence, entropy, efficiency + raw_kpis для аудита.
        При отсутствии данных — явный флаг no_data=True.
        """
        raw_kpis = self.get_sector_kpis(sector_id)
        if not raw_kpis:
            return {
                "coherence": 0.0, "entropy": 0.0, "efficiency": 0.0,
                "no_data": True,
                "note": f"нет данных для {sector_id}",
            }

        norm_kpis = {k: normalize_kpi(k, v) for k, v in raw_kpis.items()}

        return {
            "coherence":  round(compute_coherence(norm_kpis), 4),
            "entropy":    round(compute_entropy(list(norm_kpis.values())), 4),
            "efficiency": round(compute_eff(
                recognition=norm_kpis.get("satisfaction", 0.0),
                costs=norm_kpis.get("resource_usage", 1.0),
            ), 4),
            "no_data":    False,
            "raw_kpis":   raw_kpis,
            "norm_kpis":  norm_kpis,
        }

    def compute_system_health(self) -> Dict:
        """Агрегат по всей системе. Использует нормализованные среднее."""
        all_sectors = self.get_all_sectors()
        if not all_sectors:
            return {"nodes": {}, "coherence": 0.0, "entropy": 0.0,
                    "note": "sector_kpis пуста"}

        coherence = compute_coherence(all_sectors)
        entropy   = compute_entropy(list(all_sectors.values()))
        return {
            "nodes":     all_sectors,
            "coherence": round(coherence, 4),
            "entropy":   round(entropy, 4),
            "sectors":   len(all_sectors),
        }

    # ------------------------------------------------------------------
    # Диагностика нарушений норм (сырые значения)
    # ------------------------------------------------------------------

    def find_violations(self) -> Dict[str, list]:
        """
        Сравнивает сырые KPI с нормами SECTOR_NORMS.
        INVERTED_METRICS: нарушение если actual > threshold (меньше = лучше).
        Остальные: нарушение если actual < threshold (больше = лучше).
        """
        violations: Dict[str, list] = {}
        for sector_id, norms in SECTOR_NORMS.items():
            kpis = self.get_sector_kpis(sector_id)
            issues = []
            for kpi_name, threshold in norms.items():
                actual = kpis.get(kpi_name)
                if actual is None:
                    issues.append(f"{kpi_name}: нет данных")
                elif kpi_name in INVERTED_METRICS:
                    if actual > threshold:
                        issues.append(
                            f"{kpi_name}: {actual:.3f} > макс {threshold:.3f} "
                            f"(меньше = лучше)"
                        )
                else:
                    if actual < threshold:
                        issues.append(
                            f"{kpi_name}: {actual:.3f} < норма {threshold:.3f}"
                        )
            if issues:
                violations[sector_id] = issues
        return violations


# ------------------------------------------------------------------
# Диагностика при прямом запуске
# ------------------------------------------------------------------
if __name__ == "__main__":
    c = SectorDataConnector()
    c.init_table()

    health = c.compute_system_health()
    if health.get("note"):
        print(f"Данных нет: {health['note']}")
    else:
        print(f"Секторов: {health['sectors']} | "
              f"Coherence: {health['coherence']} | Entropy: {health['entropy']}")

    violations = c.find_violations()
    if violations:
        print("\nНарушения норм Σ-MATRIX:")
        for sid, issues in violations.items():
            for issue in issues:
                print(f"  [{sid}] {issue}")
    else:
        print("Нарушений норм не обнаружено.")
