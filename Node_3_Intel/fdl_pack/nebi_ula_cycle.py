#!/usr/bin/env python3
"""
⧫⟡⧫ ΠΡΟΤΟΝΟΒΕΑ: Цикл Nebi-Ula ⧫⟡⧫
Диалектический процесс обработки запросов

Этапы:
1. ТЕЗИС (T) - Фиксация состояния
2. АНТИТЕЗИС (A) - Выявление противоречий/преград
3. СИНТЕЗ (S) - Решение/новая модель
4. ТЕСТ - Проверка решения
5. СТОП - Завершение или новый цикл

Принцип: Биологическая нормализация через снятие противоречий
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from block_requirements import BlockRequirements, FilterResult, TargetGoal
import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class CycleStage(Enum):
    """Этапы цикла Nebi-Ula"""
    THESIS = "Тезис"
    ANTITHESIS = "Антитезис"
    SYNTHESIS = "Синтез"
    TEST = "Тест"
    STOP = "Стоп"


class CycleStatus(Enum):
    """Статусы завершения цикла"""
    APPROVED = "УТВЕРЖДЕНО"
    REJECTED = "ОТКЛОНЕНО"
    NEEDS_CORRECTION = "ТРЕБУЕТ_КОРРЕКТИРОВКИ"
    IN_PROGRESS = "В_ПРОЦЕССЕ"


@dataclass
class ThesisData:
    """Данные Тезиса"""
    request: str
    cu_id: str
    timestamp: float
    classification: str
    length: int


@dataclass
class AntithesisData:
    """Данные Антитезиса"""
    verdict: str
    lawful: bool
    resources_available: bool
    significance: float
    contradiction: Optional[str] = None
    filter_result: Optional[Dict] = None


@dataclass
class SynthesisData:
    """Данные Синтеза"""
    status: str
    cycle_complete: bool
    next_step: str
    significance: float = 0.0
    recommendation: str = ""
    solution: str = ""


@dataclass
class TestData:
    """Данные Теста"""
    passed: bool
    message: str
    validation_score: float = 0.0


@dataclass
class CycleResult:
    """Полный результат цикла Nebi-Ula"""
    thesis: ThesisData
    antithesis: AntithesisData
    synthesis: SynthesisData
    test: Optional[TestData]
    stop: bool
    next_block: str
    cycle_duration: float
    
    def to_dict(self):
        """Конвертация в словарь"""
        return {
            "thesis": asdict(self.thesis),
            "antithesis": asdict(self.antithesis),
            "synthesis": asdict(self.synthesis),
            "test": asdict(self.test) if self.test else None,
            "stop": self.stop,
            "next_block": self.next_block,
            "cycle_duration": self.cycle_duration
        }


class NebiUlaCycle:
    """
    Цикл Nebi-Ula - диалектический процессор
    
    Функция: Обработка любого запроса через полный цикл ФДЛ
    
    Архитектура:
    1. Блок Требований (БТ) - фильтрация по законности
    2. Блок Идей (БИ) - генерация решений (будет добавлен)
    3. Блок Целесообразности (БЦ) - выбор лучшего (будет добавлен)
    4. Блок Возможностей (БВ) - оценка условий (будет добавлен)
    """
    
    def __init__(self):
        self.block_requirements = BlockRequirements()
        self.cycle_history: List[CycleResult] = []
        self.current_stage = None
    
    def execute_cycle(self, request: str, cu_id: str) -> CycleResult:
        """
        Выполнение полного цикла Nebi-Ula
        
        Args:
            request: Текст запроса
            cu_id: ID Целевой Установки (CU1-CU5)
        
        Returns:
            CycleResult с полной информацией о прохождении цикла
        """
        start_time = time.time()
        
        # ====================================================================
        # ЭТАП 1: ТЕЗИС - Фиксация состояния
        # ====================================================================
        self.current_stage = CycleStage.THESIS
        
        thesis = self._create_thesis(request, cu_id)
        
        # ====================================================================
        # ЭТАП 2: АНТИТЕЗИС - Выявление противоречий через БТ
        # ====================================================================
        self.current_stage = CycleStage.ANTITHESIS
        
        filter_result = self.block_requirements.filter_impulse(request, cu_id)
        antithesis = self._create_antithesis(filter_result)
        
        # ====================================================================
        # ЭТАП 3: СИНТЕЗ - Разрешение противоречия
        # ====================================================================
        self.current_stage = CycleStage.SYNTHESIS
        
        synthesis = self._create_synthesis(antithesis, filter_result)
        
        # ====================================================================
        # ЭТАП 4: ТЕСТ - Проверка синтеза
        # ====================================================================
        self.current_stage = CycleStage.TEST
        
        test = self._test_synthesis(synthesis, filter_result)
        
        # ====================================================================
        # ЭТАП 5: СТОП - Определение завершения цикла
        # ====================================================================
        self.current_stage = CycleStage.STOP
        
        stop_condition, next_block = self._evaluate_stop(synthesis, test)
        
        # Формирование результата
        cycle_duration = time.time() - start_time
        
        result = CycleResult(
            thesis=thesis,
            antithesis=antithesis,
            synthesis=synthesis,
            test=test,
            stop=stop_condition,
            next_block=next_block,
            cycle_duration=cycle_duration
        )
        
        # Сохранение в историю
        self.cycle_history.append(result)
        
        return result
    
    def _create_thesis(self, request: str, cu_id: str) -> ThesisData:
        """
        Создание Тезиса
        
        Тезис - это фиксация текущего состояния и запроса.
        Классификация запроса по типу (strategic/tactical/operational).
        """
        classification = self._classify_request(request)
        
        return ThesisData(
            request=request,
            cu_id=cu_id,
            timestamp=time.time(),
            classification=classification,
            length=len(request)
        )
    
    def _create_antithesis(self, filter_result: FilterResult) -> AntithesisData:
        """
        Создание Антитезиса
        
        Антитезис - это выявление противоречий:
        - Есть ли ресурсы?
        - Достаточна ли значимость?
        - Законен ли запрос?
        """
        if not filter_result.lawful:
            contradiction = filter_result.reason
        else:
            contradiction = None
        
        return AntithesisData(
            verdict=filter_result.verdict,
            lawful=filter_result.lawful,
            resources_available=filter_result.resources_available,
            significance=filter_result.significance,
            contradiction=contradiction,
            filter_result=asdict(filter_result)
        )
    
    def _create_synthesis(
        self, 
        antithesis: AntithesisData, 
        filter_result: FilterResult
    ) -> SynthesisData:
        """
        Создание Синтеза
        
        Синтез - это разрешение противоречия:
        - Если нет ресурсов → ОТКЛОНЕНО, нужна корректировка
        - Если низкая значимость → ТРЕБУЕТ_КОРРЕКТИРОВКИ
        - Если всё ОК → УТВЕРЖДЕНО, передача в БИ
        """
        
        # Случай 1: Отклонено из-за отсутствия ресурсов
        if not antithesis.resources_available:
            return SynthesisData(
                status=CycleStatus.REJECTED.value,
                cycle_complete=True,
                next_step="Обеспечить ресурсы",
                significance=filter_result.significance,
                recommendation=f"Необходимо обеспечить ресурсы: {filter_result.resources_missing}",
                solution="БЛОКИРОВКА: Авантюра недопустима"
            )
        
        # Случай 2: Требует корректировки (есть ресурсы, но низкая значимость)
        if antithesis.lawful and antithesis.significance < 0.5:
            return SynthesisData(
                status=CycleStatus.NEEDS_CORRECTION.value,
                cycle_complete=False,
                next_step="БТ_корректировка",
                significance=antithesis.significance,
                recommendation="Повысить значимость запроса (уточнить формулировку)",
                solution="ОЖИДАНИЕ: Требуется переформулировка"
            )
        
        # Случай 3: Утверждено (есть ресурсы + достаточная значимость)
        if antithesis.lawful and antithesis.significance >= 0.5:
            return SynthesisData(
                status=CycleStatus.APPROVED.value,
                cycle_complete=True,
                next_step="БИ (Блок Идей)",
                significance=antithesis.significance,
                recommendation="Передать в Блок Идей для генерации решений",
                solution="УТВЕРЖДЕНО: Законность и значимость подтверждены"
            )
        
        # Случай 4: По умолчанию (не должно произойти)
        return SynthesisData(
            status=CycleStatus.IN_PROGRESS.value,
            cycle_complete=False,
            next_step="БТ_анализ",
            significance=antithesis.significance,
            recommendation="Требуется дополнительный анализ"
        )
    
    def _test_synthesis(
        self, 
        synthesis: SynthesisData, 
        filter_result: FilterResult
    ) -> TestData:
        """
        Тестирование Синтеза
        
        Проверка корректности синтеза:
        - Логическая целостность
        - Соответствие ФДЛ
        - Биологическая нормализация (снятие шума)
        """
        
        # Критерии валидации
        validation_score = 0.0
        
        # Критерий 1: Статус определён корректно
        if synthesis.status in [s.value for s in CycleStatus]:
            validation_score += 0.25
        
        # Критерий 2: Есть рекомендация
        if synthesis.recommendation:
            validation_score += 0.25
        
        # Критерий 3: Логическое соответствие
        if synthesis.status == CycleStatus.APPROVED.value:
            if filter_result.lawful and filter_result.significance >= 0.5:
                validation_score += 0.25
        elif synthesis.status == CycleStatus.REJECTED.value:
            if not filter_result.resources_available:
                validation_score += 0.25
        
        # Критерий 4: Следующий шаг определён
        if synthesis.next_step:
            validation_score += 0.25
        
        # Определение результата теста
        passed = validation_score >= 0.75
        
        if passed:
            message = f"✅ Синтез корректен (score: {validation_score:.2f})"
        else:
            message = f"⚠️ Синтез требует доработки (score: {validation_score:.2f})"
        
        return TestData(
            passed=passed,
            message=message,
            validation_score=validation_score
        )
    
    def _evaluate_stop(
        self, 
        synthesis: SynthesisData, 
        test: TestData
    ) -> tuple[bool, str]:
        """
        Оценка условий остановки цикла
        
        Останавливаем если:
        - Синтез утверждён и тест пройден → передача в следующий блок
        - Синтез отклонён → завершение с блокировкой
        
        Продолжаем если:
        - Требуется корректировка → возврат в БТ
        """
        
        # Утверждено и тест пройден
        if synthesis.status == CycleStatus.APPROVED.value and test.passed:
            return True, synthesis.next_step
        
        # Отклонено
        if synthesis.status == CycleStatus.REJECTED.value:
            return True, "Завершение (блокировка)"
        
        # Требует корректировки
        if synthesis.status == CycleStatus.NEEDS_CORRECTION.value:
            return False, synthesis.next_step
        
        # По умолчанию
        return False, "БТ_повтор"
    
    def _classify_request(self, request: str) -> str:
        """Классификация запроса"""
        request_lower = request.lower()
        
        strategic_kw = ["стратег", "план", "долгосрочн", "перспектив"]
        tactical_kw = ["задача", "этап", "проект", "тактик"]
        
        if any(kw in request_lower for kw in strategic_kw):
            return "strategic"
        elif any(kw in request_lower for kw in tactical_kw):
            return "tactical"
        else:
            return "operational"
    
    def get_cycle_history(self) -> List[Dict]:
        """Получение истории циклов"""
        return [cycle.to_dict() for cycle in self.cycle_history]
    
    def export_history(self, filepath: str):
        """Экспорт истории циклов в файл"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.get_cycle_history(), f, indent=2, ensure_ascii=False)
        return f"✅ История экспортирована: {filepath}"


# ============================================================================
# ДЕМОНСТРАЦИЯ
# ============================================================================

if __name__ == "__main__":
    print("⧫⟡⧫ ΠΡΟΤΟΝΟΒΕΑ: Цикл Nebi-Ula ⧫⟡⧫\n")
    
    # Инициализация
    cycle = NebiUlaCycle()
    
    # Регистрация ресурсов
    resources = {
        "Ср1": 100, "Ср2": 80, "Ср3": 90, "Ср4": 70,
        "Ср5": 60, "Ср6": 50, "Ср7": 85, "Ср8": 95, "Ср9": 40
    }
    cycle.block_requirements.register_resources(resources)
    print(f"✅ Ресурсы зарегистрированы\n")
    
    # ТЕСТ 1: Законный запрос
    print("="*75)
    print("ТЕСТ 1: Законный стратегический запрос")
    print("="*75)
    
    request1 = "Создать стратегический план восстановления Града-Сада в Николаеве с интеграцией 24 секторов"
    result1 = cycle.execute_cycle(request1, "CU1")
    
    print(f"\n📝 Запрос: {request1[:60]}...")
    print(f"\n1️⃣ ТЕЗИС:")
    print(f"   Классификация: {result1.thesis.classification}")
    print(f"   ЦУ: {result1.thesis.cu_id}")
    
    print(f"\n2️⃣ АНТИТЕЗИС:")
    print(f"   Вердикт: {result1.antithesis.verdict}")
    print(f"   Законность: {result1.antithesis.lawful}")
    print(f"   Значимость: {result1.antithesis.significance:.2f}")
    
    print(f"\n3️⃣ СИНТЕЗ:")
    print(f"   Статус: {result1.synthesis.status}")
    print(f"   Решение: {result1.synthesis.solution}")
    print(f"   Рекомендация: {result1.synthesis.recommendation}")
    
    print(f"\n4️⃣ ТЕСТ:")
    print(f"   {result1.test.message}")
    print(f"   Валидация: {result1.test.validation_score:.2f}")
    
    print(f"\n5️⃣ СТОП:")
    print(f"   Завершено: {result1.stop}")
    print(f"   Следующий блок: {result1.next_block}")
    print(f"   Длительность: {result1.cycle_duration:.4f} сек")
    
    # ТЕСТ 2: Авантюрный запрос
    print("\n" + "="*75)
    print("ТЕСТ 2: Авантюрный запрос (без ресурсов)")
    print("="*75)
    
    cycle.block_requirements.resources["Ср9"] = 0
    
    request2 = "Запустить международную программу по 24 секторам"
    result2 = cycle.execute_cycle(request2, "CU4")
    
    print(f"\n📝 Запрос: {request2}")
    print(f"\n2️⃣ АНТИТЕЗИС:")
    print(f"   Вердикт: {result2.antithesis.verdict}")
    print(f"   Противоречие: {result2.antithesis.contradiction}")
    
    print(f"\n3️⃣ СИНТЕЗ:")
    print(f"   Статус: {result2.synthesis.status}")
    print(f"   Решение: {result2.synthesis.solution}")
    print(f"   Рекомендация: {result2.synthesis.recommendation}")
    
    print(f"\n5️⃣ СТОП:")
    print(f"   Завершено: {result2.stop}")
    print(f"   Причина: БЛОКИРОВКА (авантюра)")
    
    print("\n⧫⟡⧫ Демонстрация завершена ⧫⟡⧫")
