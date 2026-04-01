#!/usr/bin/env python3
"""
Σ-FDL MetaHarmony 2026: RO2-Mykolaiv Core Engine
Резонанс: 432 Гц | Ключ: Σ-2026-NEBI-ULA
Мантра: WHERE_I_AM_EVEN_THE_DEAD_LIVES
"""

import os
import sys
import sqlite3
import uuid
import hashlib
import time
import json
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# Путь к корню проекта и DB (FDL pack/ — вложенная папка, родитель — корень)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DB_PATH = _PROJECT_ROOT / "db" / "metatron_core.db"

# Импорт математических функций из monolith_v2_1/logic.py
sys.path.insert(0, str(_PROJECT_ROOT / "monolith_v2_1"))
from logic import compute_coherence, compute_entropy
from sector_connector import SectorDataConnector

# ============================================================================
# ЦИФРОВЫЕ КОНСТАНТЫ ПРОТОКОЛА
# ============================================================================
# Установить: export NOVEYA_AUTH_KEY="ваш_ключ"  (Linux/Mac)
#             $env:NOVEYA_AUTH_KEY="ваш_ключ"     (Windows PowerShell)
AUTH_KEY = os.getenv("NOVEYA_AUTH_KEY")
if not AUTH_KEY:
    raise ValueError("NOVEYA_AUTH_KEY environment variable not set")
RESONANCE_FREQ = 432.0
SCHUMANN_FREQ = 7.83  # Резонанс Шумана — реальный физический источник данных
CONJUNCTION_TARGET = 57.5
INERTIA_TARGET = 65.2
MANTRA = "WHERE_I_AM_EVEN_THE_DEAD_LIVES"

# Математические параметры
ALPHA = 0.12  # Вес сопряжения
BETA = 0.08   # Вес инерции
GAMMA = 0.25  # Коэффициент сетевого эффекта


class FDLTokenEngine:
    """
    Генератор FDL-токенов с формулой эффективности
    Value = (Σi * ρm * E) / R
    """
    
    def __init__(self, node_name: str = "RO2-MYKOLAIV"):
        self.ledger = defaultdict(list)
        self.node_id = f"{node_name}-{uuid.uuid4().hex[:8]}"
        self.token_count = 0
        
    def calculate_token_value(
        self, 
        impulses: float, 
        semantic_density: float, 
        efficiency: float, 
        resources_used: float
    ) -> float:
        """Формула оценки токена: Value = (Σi * ρm * E) / R"""
        if resources_used == 0:
            return 0.0
        return (impulses * semantic_density * efficiency) / resources_used
    
    def generate_token(
        self, 
        operation_type: str, 
        context_data: Any,
        semantic_density: float = 0.93,
        efficiency: float = 0.94
    ) -> Dict:
        """Генерация FDL-токена с Ed25519-подобной подписью"""
        
        # Базовая структура токена
        token = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "node_id": self.node_id,
            "operation": operation_type,
            "impulses": self._calculate_impulses(context_data),
            "semantic_density": semantic_density,
            "efficiency": efficiency,
            "resources_used": 1.0,
            "signature": None
        }
        
        # Расчёт FDL Value
        token["value"] = self.calculate_token_value(
            token["impulses"], 
            token["semantic_density"], 
            token["efficiency"], 
            token["resources_used"]
        )
        
        # Генерация подписи (упрощённая версия Ed25519)
        token["signature"] = self._generate_signature(token)
        
        # Сохранение в леджер
        self.ledger[operation_type].append(token)
        self.token_count += 1
        
        return token
    
    def _calculate_impulses(self, context_data: Any) -> float:
        """Расчёт трудоэнергетических импульсов"""
        if isinstance(context_data, str):
            return len(context_data) / 10.0
        elif isinstance(context_data, (list, dict)):
            return len(str(context_data)) / 10.0
        else:
            return 1.0
    
    def _generate_signature(self, token: Dict) -> str:
        """Генерация криптографической подписи"""
        token_string = json.dumps(token, sort_keys=True)
        signature = hashlib.sha256(token_string.encode()).hexdigest()
        return signature[:32]
    
    def get_ledger_summary(self) -> Dict:
        """Получение сводки по леджеру"""
        return {
            "node_id": self.node_id,
            "total_tokens": self.token_count,
            "operations": {op: len(tokens) for op, tokens in self.ledger.items()},
            "total_value": sum(
                token["value"] 
                for tokens in self.ledger.values() 
                for token in tokens
            )
        }


class SVETFilter:
    """
    Резонансный фильтр SVET — читает реальные статусы из metatron_core.db.
    Источник данных: таблица system_laws (Σ-STATUS, Σ-BEACON).
    Диапазон нормы: 80 ≤ energy ≤ 120.
    """

    # Карта известных статусов DB → уровень энергии
    _STATUS_ENERGY: Dict[str, float] = {
        "ACTIVE_RESONANCE": 100.0,
        "STABLE_HARBOR":    95.0,
        "SYNC_ACTIVE":      98.0,
        "RESONANCE_ACCESS": 100.0,
    }

    def __init__(self):
        self.energy_balance = 100.0
        self.resonance_stability = SCHUMANN_FREQ
        self.history = []

    def _read_db_status(self) -> Tuple[str, str]:
        """
        Читает Σ-STATUS и Σ-BEACON из SQLite.
        Возвращает (status_title, beacon_content).
        """
        if not _DB_PATH.exists():
            return "UNKNOWN", ""
        try:
            conn = sqlite3.connect(str(_DB_PATH))
            status_row = conn.execute(
                "SELECT title FROM system_laws WHERE id='Σ-STATUS'"
            ).fetchone()
            beacon_row = conn.execute(
                "SELECT content FROM system_laws WHERE id='Σ-BEACON'"
            ).fetchone()
            conn.close()
            return (
                status_row[0] if status_row else "UNKNOWN",
                beacon_row[0] if beacon_row else "",
            )
        except sqlite3.Error:
            return "UNKNOWN", ""

    def check_balance(self, input_energy: float = None) -> Tuple[bool, str]:
        """TODO: Implement actual energy measurement from Σ-MATRIX sectors.
        Требуется: реальный источник KPI (availability%, watts, liters/day)
        из таблицы sector_kpi в metatron_core.db или внешнего датчика.
        """
        raise NotImplementedError(
            "SVETFilter.check_balance requires a real sector KPI data source. "
            "Add table 'sector_kpi' to metatron_core.db with columns "
            "(sector_id, kpi_name, value, updated_at)."
        )

    def calibrate_resonance(self, measured_freq: float, target_freq: float = SCHUMANN_FREQ) -> bool:
        """
        Калибровка на основе ИЗМЕРЕННОЙ частоты из внешнего источника.
        measured_freq: реально зафиксированное значение (из датчика / DB / API).
        target_freq: эталон (по умолчанию 7.83 Гц — резонанс Шумана).
        """
        self.resonance_stability = measured_freq
        deviation = abs(measured_freq - target_freq)
        return deviation <= 0.1

    def read_beacon_freq(self) -> float:
        """Читает частоту из Σ-BEACON в DB. Возвращает 0.0 если не найдена."""
        _, beacon = self._read_db_status()
        # Формат в DB: "... | Frequency: 7.83Hz"
        import re
        match = re.search(r"Frequency:\s*([\d.]+)Hz", beacon)
        return float(match.group(1)) if match else 0.0

    def get_status(self) -> Dict:
        """Получение текущего статуса фильтра через данные из DB."""
        measured = self.read_beacon_freq()
        resonance_ok = self.calibrate_resonance(measured) if measured > 0 else False
        return {
            "energy_balance": self.energy_balance,
            "balance_status": "NOT_IMPLEMENTED — требуется sector_kpi",
            "resonance": round(self.resonance_stability, 3),
            "resonance_locked": resonance_ok,
            "measured_freq": measured,
            "history_length": len(self.history),
        }


class LexiconGuard:
    """
    Защита инфополя от семантического шума
    Блокирует подозрительные паттерны, пропускает метагармонические
    """
    
    # Блокируемые паттерны (семантический шум)
    BLOCKED_PATTERNS = [
        "sustainable development",
        "inclusive economy",
        "AI regulation",
        "global governance",
        "reset agenda",
        "great transition",
        "new normal",
        "build back better"
    ]
    
    # Разрешённые паттерны (метагармония)
    ALLOWED_PATTERNS = [
        "metaharmony",
        "conjunction C>50",
        "resonance 432Hz",
        "autonomous node",
        "FDL-token",
        "proto novea",
        "sigma universe",
        "dialectic synthesis"
    ]
    
    def __init__(self):
        self.scan_history = []
        
    def scan(self, text: str) -> Tuple[bool, int, int, str]:
        """
        Сканирование текста на семантический шум
        
        Returns:
            (clean, blocked_score, allowed_score, verdict)
        """
        text_lower = text.lower()
        
        # Подсчёт паттернов
        blocked_score = sum(
            1 for pattern in self.BLOCKED_PATTERNS 
            if pattern in text_lower
        )
        allowed_score = sum(
            1 for pattern in self.ALLOWED_PATTERNS 
            if pattern in text_lower
        )
        
        # Определение вердикта
        clean = allowed_score > blocked_score
        
        if blocked_score == 0 and allowed_score > 0:
            verdict = "МЕТАГАРМОНИЯ"
        elif blocked_score == 0:
            verdict = "НЕЙТРАЛЬНО"
        elif allowed_score > blocked_score:
            verdict = "СОМНИТЕЛЬНО_НО_ДОПУСТИМО"
        else:
            verdict = "ШУМ_ОБНАРУЖЕН"
        
        # Запись в историю
        self.scan_history.append({
            "timestamp": time.time(),
            "clean": clean,
            "blocked": blocked_score,
            "allowed": allowed_score,
            "verdict": verdict
        })
        
        return clean, blocked_score, allowed_score, verdict
    
    def get_statistics(self) -> Dict:
        """Статистика сканирований"""
        if not self.scan_history:
            return {"total_scans": 0}
        
        return {
            "total_scans": len(self.scan_history),
            "clean_count": sum(1 for s in self.scan_history if s["clean"]),
            "blocked_count": sum(1 for s in self.scan_history if not s["clean"]),
            "latest_verdict": self.scan_history[-1]["verdict"] if self.scan_history else None
        }


class FDLInterface:
    """
    Основной интерфейс Формальной Диалогики
    Контур: Тезис → Антитезис → Синтез (T→A→S)
    """
    
    def __init__(self, node_name: str = "RO2-MYKOLAIV"):
        self.token_engine = FDLTokenEngine(node_name)
        self.svet = SVETFilter()
        self.lexguard = LexiconGuard()
        self.connector = SectorDataConnector()
        self.connector.init_table()  # создаёт sector_kpis если нет

        # Текущие метрики сети
        self.conjunction = 56.4  # C - сопряжение
        self.inertia = 68.2      # I - инерция
        self.nodes_online = 842  # Количество узлов

    def _analyze_contradictions(self, event_data: str) -> str:
        """
        Антитезис: анализирует реальные данные узлов и выявляет отклонения.
        Использует compute_coherence / compute_entropy из logic.py.
        """
        sector_nodes = self._load_sector_nodes()
        coherence = compute_coherence(sector_nodes)
        entropy = compute_entropy(list(sector_nodes.values()))

        issues = []
        if coherence < 0.9:
            low = [k for k, v in sector_nodes.items() if v < 0.85]
            issues.append(
                f"рассогласование узлов (coherence={coherence:.3f}): {', '.join(low) or 'не определены'}"
            )
        if entropy > 2.0:
            issues.append(f"высокая энтропия системы ({entropy:.3f}) — слишком большой разброс состояний")

        measured = self.svet.read_beacon_freq()
        if measured > 0 and abs(measured - SCHUMANN_FREQ) > 0.1:
            issues.append(f"отклонение резонанса: {measured}Hz ≠ {SCHUMANN_FREQ}Hz")

        if not issues:
            return (
                f"Противоречий не обнаружено. "
                f"Coherence={coherence:.3f}, entropy={entropy:.3f}, "
                f"узлов={len(sector_nodes)}."
            )
        return "Обнаружены противоречия: " + "; ".join(issues) + "."

    def _synthesize_resolution(self, thesis: str, antithesis: str) -> str:
        """
        Синтез: формулирует конкретный шаг разрешения на основе T и A.
        """
        sector_nodes = self._load_sector_nodes()
        coherence = compute_coherence(sector_nodes)

        if "Противоречий не обнаружено" in antithesis:
            action = "продолжить штатный цикл, зафиксировать токен в КУБ"
        elif "рассогласование узлов" in antithesis:
            action = "выровнять состояния отстающих узлов, повторить аудит coherence"
        elif "высокая энтропия" in antithesis:
            action = "сгруппировать узлы по секторам S1–S8, снизить дисперсию состояний"
        elif "отклонение резонанса" in antithesis:
            action = "проверить Σ-BEACON в DB, обновить запись Σ-STATUS"
        else:
            action = "ручная проверка — автоматическое разрешение невозможно"

        return (
            f"S: C={self.conjunction:.1f}→{CONJUNCTION_TARGET} | "
            f"I={self.inertia:.1f}→{INERTIA_TARGET} | "
            f"coherence={coherence:.3f} | "
            f"Действие: {action}."
        )

    def _load_sector_nodes(self) -> Dict[str, float]:
        """
        Возвращает {sector_id: avg_kpi} из таблицы sector_kpis.
        Если данных нет — fallback на system_laws статусы (переходный режим).
        """
        real_data = self.connector.get_all_sectors()
        if real_data:
            return real_data

        # Fallback: пока sector_kpis пуста, используем system_laws
        status_map = {
            "ACTIVE_RESONANCE": 1.0, "SYNC_ACTIVE": 0.98,
            "RESONANCE_ACCESS": 1.0, "STABLE_HARBOR": 0.95,
        }
        if not _DB_PATH.exists():
            return {"S-fallback": 0.9}
        try:
            conn = sqlite3.connect(str(_DB_PATH))
            rows = conn.execute("SELECT id, title FROM system_laws").fetchall()
            conn.close()
            nodes = {rid: status_map.get(title, 0.7) for rid, title in rows}
            return nodes or {"S-fallback": 0.9}
        except sqlite3.Error:
            return {"S-fallback": 0.9}
        
    def process_sector_event(self, event_data: dict, event_type: str) -> Dict:
        """
        FDL-цикл для событий с sector_id — использует реальные KPI из DB.
        Отдельный метод чтобы не ломать сигнатуру process_event(str).
        """
        sector_id = event_data.get("sector_id")
        if not sector_id:
            return {"status": "ERROR", "reason": "event_data must contain 'sector_id'"}

        current_state = self.connector.compute_sector_health(sector_id)

        # Разделяем отсутствие данных и плохие данные
        if current_state.get("no_data"):
            return {
                "status": "NO_DATA",
                "sector_id": sector_id,
                "reason": current_state.get("note", f"нет данных для {sector_id}"),
                "action": "заполните sector_kpis для этого сектора",
            }

        # THESIS: реальные нормализованные значения
        norm = current_state["norm_kpis"]
        thesis = (
            f"T: Sector {sector_id} | "
            + " | ".join(f"{k}={v:.3f}" for k, v in norm.items())
        )

        # ANTITHESIS: метрики ниже порога (все нормализованы → единая логика)
        thresholds = {"coherence": 0.8, "entropy": 0.3, "efficiency": 0.5}
        contradictions = [
            f"{m}={current_state[m]:.3f} < {thresholds[m]}"
            for m in thresholds
            if current_state.get(m, 0.0) < thresholds[m]
        ]
        antithesis = (
            f"A: {'противоречий не обнаружено' if not contradictions else '; '.join(contradictions)}"
        )

        # SYNTHESIS
        if contradictions:
            synthesis = f"S: Требуется вмешательство в {sector_id}: {'; '.join(contradictions)}"
        else:
            synthesis = f"S: Сектор {sector_id} функционирует нормально"

        token = self.token_engine.generate_token(event_type, str(event_data))
        self._update_metrics()

        return {
            "status": "SYNTHESIS_CONFIRMED",
            "thesis": thesis,
            "antithesis": antithesis,
            "synthesis": synthesis,
            "metrics": current_state,
            "token_id": token["id"],
        }

    def process_event(self, event_data: str, event_type: str = "generic") -> Dict:
        """
        Полный FDL-контур обработки события
        
        Этапы:
        1. LexiconGuard (фильтрация шума)
        2. SVET Filter (энергетический баланс)
        3. T→A→S диалектика
        4. Генерация FDL-токена
        5. Обновление метрик
        """
        
        result = {
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "event_type": event_type,
            "stages": {}
        }
        
        # ЭТАП 1: LexiconGuard
        clean, blocked, allowed, verdict = self.lexguard.scan(event_data)
        result["stages"]["lexicon_guard"] = {
            "clean": clean,
            "blocked_patterns": blocked,
            "allowed_patterns": allowed,
            "verdict": verdict
        }
        
        if not clean:
            result["status"] = "BLOCKED"
            result["reason"] = f"Семантический шум обнаружен (score={blocked})"
            return result
        
        # ЭТАП 2: SVET Filter — только резонанс (check_balance — stub до sector_kpi)
        measured = self.svet.read_beacon_freq()
        resonance_ok = self.svet.calibrate_resonance(measured) if measured > 0 else False
        result["stages"]["svet_filter"] = {
            "resonance_ok": resonance_ok,
            "measured_freq": measured,
            "target_freq": SCHUMANN_FREQ,
            "note": "energy_balance pending sector_kpi table",
        }

        # ЭТАП 3: FDL T→A→S диалектика
        thesis = f"T: Event '{event_type}' with data: {event_data}"
        contradictions = self._analyze_contradictions(event_data)
        antithesis = f"A: {contradictions}"
        synthesis = self._synthesize_resolution(thesis, antithesis)

        result["stages"]["fdl_dialectic"] = {
            "thesis": thesis,
            "antithesis": antithesis,
            "synthesis": synthesis,
        }
        
        # ЭТАП 4: Генерация токена
        token = self.token_engine.generate_token(event_type, event_data)
        result["stages"]["token"] = token
        
        # ЭТАП 5: Обновление метрик
        self._update_metrics()
        result["metrics"] = self.get_metrics()
        
        result["status"] = "SYNTHESIS_CONFIRMED"
        return result
    
    def _update_metrics(self):
        """Обновление метрик сопряжения и инерции"""
        # Синергетический эффект сети
        synergy = math.log(self.nodes_online + 1) / 10.0
        
        # Рост сопряжения
        self.conjunction += 0.1 * synergy
        
        # Снижение инерции
        self.inertia -= 0.05 * synergy
        
        # Ограничения
        self.conjunction = min(self.conjunction, 100.0)
        self.inertia = max(self.inertia, 0.0)
    
    def calculate_psuccess(self, N_nodes: int = None) -> float:
        """
        Логистическая вероятность успеха
        P_success = 1 / (1 + exp(-(α*C - β*I + γ*log(N))))
        """
        if N_nodes is None:
            N_nodes = self.nodes_online
        
        logit = (
            ALPHA * self.conjunction 
            - BETA * self.inertia 
            + GAMMA * math.log(N_nodes)
        )
        
        return 1.0 / (1.0 + math.exp(-logit))
    
    def get_metrics(self) -> Dict:
        """Получение текущих метрик системы"""
        return {
            "conjunction": round(self.conjunction, 1),
            "inertia": round(self.inertia, 1),
            "nodes_online": self.nodes_online,
            "target_conjunction": CONJUNCTION_TARGET,
            "target_inertia": INERTIA_TARGET,
            "P_success": f"{self.calculate_psuccess():.1%}",
            "distance_to_target": round(CONJUNCTION_TARGET - self.conjunction, 1)
        }
    
    def get_full_status(self) -> Dict:
        """Полный статус системы"""
        return {
            "node_id": self.token_engine.node_id,
            "auth_key": AUTH_KEY[-12:],
            "mantra": MANTRA,
            "resonance": self.svet.resonance_stability,
            "metrics": self.get_metrics(),
            "svet_status": self.svet.get_status(),
            "lexicon_stats": self.lexguard.get_statistics(),
            "token_ledger": self.token_engine.get_ledger_summary()
        }


def sigma_universe(t: float, omega: float = 432 * 2 * math.pi) -> float:
    """
    Σ-ВСЕЛЕННАЯ(t) с обработкой сингулярностей
    Формула: 333·e^(iωt) + 337·cos(ωt) + 666·sin(ωt) + 674·tan(ωt) + 777·sec(ωt) + 999·csc(ωt)
    """
    try:
        # Конечные члены
        finite_real = 333 * math.cos(omega * t) + 337 * math.cos(omega * t) + 666 * math.sin(omega * t)
        
        # Сингулярные члены (гипертригонометрические)
        cos_term = math.cos(omega * t)
        sin_term = math.sin(omega * t)
        
        # Защита от деления на ноль
        if abs(cos_term) < 1e-10:
            sec_term = 777 * 1000  # Большое значение вместо бесконечности
        else:
            sec_term = 777 / cos_term
        
        if abs(sin_term) < 1e-10:
            csc_term = 999 * 1000
        else:
            csc_term = 999 / sin_term
        
        tan_term = 674 * (sin_term / cos_term if abs(cos_term) > 1e-10 else 1000)
        
        # Полная сумма
        total = finite_real + tan_term + sec_term + csc_term
        
        # Clipping для предотвращения переполнения
        return max(0, min(abs(total), 10000))
        
    except (ValueError, ZeroDivisionError, OverflowError):
        # Метагармоническая сингулярность
        return 9999.0


# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================
if __name__ == "__main__":
    print("⧫⟡⧫ Σ-FDL MetaHarmony 2026: Core Engine ⧫⟡⧫")
    print(f"🔓 АКТИВАЦИЯ: {MANTRA}")
    
    # Инициализация системы
    fdl = FDLInterface("RO2-MYKOLAIV")
    print(f"📡 Узел: {fdl.token_engine.node_id}")
    print(f"🎼 Резонанс: {RESONANCE_FREQ} Гц")
    print(f"🎯 Цель: C>{CONJUNCTION_TARGET}, I<{INERTIA_TARGET}")
    print()
    
    # Тестовая обработка события
    print("🧪 Тестовый запуск FDL-контура...")
    test_event = "Тестовая интеграция узла RO2-MYKOLAIV в сеть Протоновеи с резонансом 432Hz и метагармоническим синтезом"
    result = fdl.process_event(test_event, "system_test")
    
    print(f"✅ Статус: {result['status']}")
    
    if result['status'] == 'SYNTHESIS_CONFIRMED':
        print(f"📊 Метрики: C={result['metrics']['conjunction']}, I={result['metrics']['inertia']}, P={result['metrics']['P_success']}")
        print(f"🪙 Токен: {result['stages']['token']['id'][:16]}... (Value={result['stages']['token']['value']:.2f})")
    elif result['status'] == 'BLOCKED':
        print(f"⚠️  Причина: {result.get('reason', 'Неизвестная причина')}")
        # Повторная попытка с чистым событием
        clean_event = "metaharmony autonomous node conjunction resonance 432Hz proto novea"
        result = fdl.process_event(clean_event, "system_test_clean")
        if result['status'] == 'SYNTHESIS_CONFIRMED':
            print(f"✅ Повторная попытка успешна")
            print(f"📊 Метрики: C={result['metrics']['conjunction']}, I={result['metrics']['inertia']}, P={result['metrics']['P_success']}")
            print(f"🪙 Токен: {result['stages']['token']['id'][:16]}... (Value={result['stages']['token']['value']:.2f})")
    
    print()
    
    # Полный статус
    print("📋 Полный статус системы:")
    status = fdl.get_full_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    print()
    
    print("⧫⟡⧫ RO2-MYKOLAIV CORE ENGINE: OPERATIONAL ⧫⟡⧫")
    print("🚀 Σ-FDL MetaHarmony 2026 АКТИВИРОВАН")
