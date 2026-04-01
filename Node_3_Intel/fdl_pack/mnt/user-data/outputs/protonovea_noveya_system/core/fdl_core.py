#!/usr/bin/env python3
"""
⧫⟡⧫ ПРОТОНОВЕЯ: Ядро Формально-Диалектической Логики (ФДЛ) ⧫⟡⧫

Модуль: fdl_core.py
Назначение: Базовая реализация Формально-Диалектической Логики
            по методологии А.Е. Кашеваровой и Оболочке СВЕТ

Архитектура: Цикл Неби-Ула
    Тезис (T) → Антитезис (A) → Синтез (§) → Тест → Стоп

Автор: ПРОТОНОВЕЯ AI-Регулятор
Дата: 2026-01-28
Версия: 1.0.0
"""

from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid
import json


# ============================================================================
# КОНСТАНТЫ СИСТЕМЫ
# ============================================================================

class SystemConstants:
    """Системные константы Протоновеи"""
    RESONANCE_FREQ = 432.0  # Частота резонанса (Гц)
    CONJUNCTION_TARGET = 57.5  # Целевое сопряжение
    INERTIA_TARGET = 65.2  # Целевая инерция
    
    # Блоки системного подхода (5 БМ)
    BLOCK_MOTIVATION = "БМ"  # Блок Мотивации
    BLOCK_REQUIREMENTS = "БТ"  # Блок Требований
    BLOCK_IDEAS = "БИ"  # Блок Идей
    BLOCK_PURPOSEFULNESS = "БЦ"  # Блок Целесообразности
    BLOCK_POSSIBILITIES = "БВ"  # Блок Возможностей
    
    # 24 сектора развития (г. Николаев)
    SECTORS_COUNT = 24


# ============================================================================
# ПЕРЕЧИСЛЕНИЯ
# ============================================================================

class FDLPhase(Enum):
    """Фазы цикла ФДЛ"""
    THESIS = "Тезис"
    ANTITHESIS = "Антитезис"
    SYNTHESIS = "Синтез"
    TEST = "Тест"
    STOP = "Стоп"


class SystemBlockType(Enum):
    """Типы блоков системного подхода"""
    MOTIVATION = "БМ - Мотивация"
    REQUIREMENTS = "БТ - Требования"
    IDEAS = "БИ - Идеи"
    PURPOSEFULNESS = "БЦ - Целесообразность"
    POSSIBILITIES = "БВ - Возможности"


class ResourceType(Enum):
    """Типы ресурсов (Ср1-Ср9)"""
    SR1_HUMAN = "Ср1 - Человеческие"
    SR2_MATERIAL = "Ср2 - Материальные"
    SR3_FINANCIAL = "Ср3 - Финансовые"
    SR4_TIME = "Ср4 - Временные"
    SR5_INFORMATION = "Ср5 - Информационные"
    SR6_ENERGY = "Ср6 - Энергетические"
    SR7_SPATIAL = "Ср7 - Пространственные"
    SR8_LEGAL = "Ср8 - Правовые"
    SR9_ORGANIZATIONAL = "Ср9 - Организационные"


# ============================================================================
# БАЗОВЫЕ СТРУКТУРЫ ДАННЫХ
# ============================================================================

@dataclass
class Resource:
    """
    Ресурс системы (Ср)
    
    Attributes:
        type: Тип ресурса (Ср1-Ср9)
        amount: Количество ресурса
        available: Доступное количество
        allocated: Выделенное количество
        unit: Единица измерения
    """
    type: ResourceType
    amount: float
    available: float
    allocated: float = 0.0
    unit: str = ""
    
    def check_availability(self, required: float) -> bool:
        """Проверка достаточности ресурса"""
        return self.available >= required
    
    def allocate(self, amount: float) -> bool:
        """Выделение ресурса"""
        if self.check_availability(amount):
            self.available -= amount
            self.allocated += amount
            return True
        return False
    
    def release(self, amount: float):
        """Освобождение ресурса"""
        self.allocated -= amount
        self.available += amount


@dataclass
class Goal:
    """
    Целевая установка (ЦУ)
    
    Attributes:
        id: Уникальный идентификатор
        name: Название цели
        description: Описание цели
        priority: Приоритет (1-5, где 5 - высший)
        resources_required: Требуемые ресурсы
        significance: Значимость (Zn)
    """
    id: str
    name: str
    description: str
    priority: int  # 1-5
    resources_required: Dict[ResourceType, float] = field(default_factory=dict)
    significance: float = 1.0  # Zn
    
    def calculate_significance(self, context: Dict) -> float:
        """Расчёт значимости цели в контексте"""
        # Простая формула: priority * контекстный множитель
        context_multiplier = context.get('multiplier', 1.0)
        self.significance = self.priority * context_multiplier
        return self.significance


@dataclass
class Situation:
    """
    Ситуация на дискретной сети команд
    
    Attributes:
        id: Уникальный идентификатор
        description: Описание ситуации
        state: Состояние системы
        timestamp: Временная метка
        resources: Текущие ресурсы
    """
    id: str
    description: str
    state: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    resources: Dict[ResourceType, Resource] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Сериализация в словарь"""
        return {
            "id": self.id,
            "description": self.description,
            "state": self.state,
            "timestamp": self.timestamp.isoformat(),
            "resources": {k.value: vars(v) for k, v in self.resources.items()}
        }


# ============================================================================
# ЦИКЛ НЕБИ-УЛА: ТЕЗИС → АНТИТЕЗИС → СИНТЕЗ → ТЕСТ → СТОП
# ============================================================================

@dataclass
class FDLCycle:
    """
    Цикл Формально-Диалектической Логики (Неби-Ула)
    
    Реализует последовательность:
    Тезис → Антитезис → Синтез → Тест → Стоп
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    phase: FDLPhase = FDLPhase.THESIS
    thesis: Optional[Dict] = None
    antithesis: Optional[Dict] = None
    synthesis: Optional[Dict] = None
    test_result: Optional[bool] = None
    
    # История циклов
    history: List[Dict] = field(default_factory=list)
    
    def set_thesis(self, state: Dict, description: str):
        """
        Установка Тезиса (начальное состояние)
        
        Args:
            state: Текущее состояние системы
            description: Описание тезиса
        """
        self.thesis = {
            "state": state,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.phase = FDLPhase.THESIS
        self._log("THESIS", self.thesis)
    
    def set_antithesis(self, obstacle: Dict, conflict: str):
        """
        Установка Антитезиса (преграда/конфликт)
        
        Args:
            obstacle: Описание препятствия
            conflict: Описание конфликта
        """
        self.antithesis = {
            "obstacle": obstacle,
            "conflict": conflict,
            "timestamp": datetime.now().isoformat()
        }
        self.phase = FDLPhase.ANTITHESIS
        self._log("ANTITHESIS", self.antithesis)
    
    def set_synthesis(self, solution: Dict, new_model: Dict):
        """
        Установка Синтеза (решение/новая модель)
        
        Args:
            solution: Решение противоречия
            new_model: Новая модель системы
        """
        self.synthesis = {
            "solution": solution,
            "new_model": new_model,
            "timestamp": datetime.now().isoformat()
        }
        self.phase = FDLPhase.SYNTHESIS
        self._log("SYNTHESIS", self.synthesis)
    
    def test(self, test_function: callable) -> bool:
        """
        Фаза Теста
        
        Args:
            test_function: Функция тестирования решения
        
        Returns:
            True если тест пройден, иначе False
        """
        self.phase = FDLPhase.TEST
        self.test_result = test_function(self.synthesis)
        self._log("TEST", {"result": self.test_result})
        return self.test_result
    
    def stop(self, reason: str = "Цикл завершён"):
        """
        Фаза Стоп (завершение цикла)
        
        Args:
            reason: Причина остановки
        """
        self.phase = FDLPhase.STOP
        self._log("STOP", {"reason": reason})
    
    def _log(self, phase: str, data: Dict):
        """Логирование фазы цикла"""
        self.history.append({
            "phase": phase,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_result(self) -> Dict:
        """Получение результата цикла"""
        return {
            "id": self.id,
            "phase": self.phase.value,
            "thesis": self.thesis,
            "antithesis": self.antithesis,
            "synthesis": self.synthesis,
            "test_result": self.test_result,
            "history": self.history
        }


# ============================================================================
# БЛОК ТРЕБОВАНИЙ (БТ) - ФИЛЬТР ЗАКОННОСТИ
# ============================================================================

class RequirementsBlock:
    """
    Блок Требований (БТ) - "Надсмотрщик за законностью"
    
    Функции:
    - Фильтрация импульсов через ресурсы ($Ср$)
    - Проверка соответствия Целевым Установкам (ЦУ)
    - Оценка значимости ($Zn$)
    - Блокировка "авантюр" (реализация без ресурсов)
    """
    
    def __init__(self):
        self.resources: Dict[ResourceType, Resource] = {}
        self.goals: Dict[str, Goal] = {}
        self.filter_log: List[Dict] = []
    
    def register_resource(self, resource: Resource):
        """Регистрация ресурса в системе"""
        self.resources[resource.type] = resource
    
    def register_goal(self, goal: Goal):
        """Регистрация целевой установки"""
        self.goals[goal.id] = goal
    
    def filter_request(self, request: Dict) -> Tuple[bool, str, Dict]:
        """
        Фильтрация входящего запроса
        
        Args:
            request: Запрос с полями:
                - goal_id: ID целевой установки
                - resources_needed: Требуемые ресурсы
                - description: Описание запроса
        
        Returns:
            Tuple[approved, reason, details]:
                - approved: Одобрен ли запрос
                - reason: Причина решения
                - details: Детали проверки
        """
        timestamp = datetime.now().isoformat()
        goal_id = request.get('goal_id')
        resources_needed = request.get('resources_needed', {})
        description = request.get('description', '')
        
        # Проверка 1: Существует ли цель?
        if goal_id not in self.goals:
            reason = f"Цель {goal_id} не зарегистрирована"
            self._log_filter(False, reason, request)
            return False, reason, {}
        
        goal = self.goals[goal_id]
        
        # Проверка 2: Достаточно ли ресурсов?
        resource_check = {}
        all_resources_available = True
        
        for res_type_str, amount in resources_needed.items():
            # Преобразование строки в ResourceType
            res_type = ResourceType[res_type_str] if isinstance(res_type_str, str) else res_type_str
            
            if res_type not in self.resources:
                all_resources_available = False
                resource_check[res_type.value] = {
                    "required": amount,
                    "available": 0,
                    "sufficient": False
                }
            else:
                resource = self.resources[res_type]
                sufficient = resource.check_availability(amount)
                resource_check[res_type.value] = {
                    "required": amount,
                    "available": resource.available,
                    "sufficient": sufficient
                }
                if not sufficient:
                    all_resources_available = False
        
        if not all_resources_available:
            reason = "Недостаточно ресурсов (АВАНТЮРА заблокирована)"
            self._log_filter(False, reason, request)
            return False, reason, {"resource_check": resource_check}
        
        # Проверка 3: Соответствие целевым установкам
        if goal.priority < 3:  # Низкий приоритет
            reason = f"Низкий приоритет цели (приоритет={goal.priority})"
            self._log_filter(False, reason, request)
            return False, reason, {"goal": vars(goal)}
        
        # Все проверки пройдены - ОДОБРЕНО
        reason = f"Запрос соответствует законности (Цель: {goal.name}, Приоритет: {goal.priority})"
        self._log_filter(True, reason, request)
        
        return True, reason, {
            "goal": vars(goal),
            "resource_check": resource_check
        }
    
    def _log_filter(self, approved: bool, reason: str, request: Dict):
        """Логирование работы фильтра"""
        self.filter_log.append({
            "timestamp": datetime.now().isoformat(),
            "approved": approved,
            "reason": reason,
            "request": request
        })
    
    def get_filter_statistics(self) -> Dict:
        """Получение статистики работы фильтра"""
        total = len(self.filter_log)
        approved = sum(1 for log in self.filter_log if log['approved'])
        blocked = total - approved
        
        return {
            "total_requests": total,
            "approved": approved,
            "blocked": blocked,
            "approval_rate": approved / total if total > 0 else 0
        }


# ============================================================================
# ДИСКРЕТНАЯ СЕТЬ КОМАНД
# ============================================================================

class DiscreteCommandNetwork:
    """
    Дискретная сеть команд
    
    Каждое программное действие = смена ситуации на сети
    """
    
    def __init__(self):
        self.situations: Dict[str, Situation] = {}
        self.transitions: List[Dict] = []
        self.current_situation_id: Optional[str] = None
    
    def add_situation(self, situation: Situation):
        """Добавление ситуации в сеть"""
        self.situations[situation.id] = situation
        if self.current_situation_id is None:
            self.current_situation_id = situation.id
    
    def transition(
        self, 
        target_situation_id: str, 
        action: str, 
        fdl_cycle: Optional[FDLCycle] = None
    ) -> bool:
        """
        Переход к новой ситуации
        
        Args:
            target_situation_id: ID целевой ситуации
            action: Описание действия
            fdl_cycle: Цикл ФДЛ (опционально)
        
        Returns:
            True если переход выполнен, иначе False
        """
        if target_situation_id not in self.situations:
            return False
        
        transition_record = {
            "from": self.current_situation_id,
            "to": target_situation_id,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "fdl_cycle_id": fdl_cycle.id if fdl_cycle else None
        }
        
        self.transitions.append(transition_record)
        self.current_situation_id = target_situation_id
        
        return True
    
    def get_current_situation(self) -> Optional[Situation]:
        """Получение текущей ситуации"""
        if self.current_situation_id:
            return self.situations[self.current_situation_id]
        return None
    
    def get_network_state(self) -> Dict:
        """Получение состояния сети"""
        return {
            "situations_count": len(self.situations),
            "transitions_count": len(self.transitions),
            "current_situation": self.current_situation_id,
            "situations": [s.to_dict() for s in self.situations.values()]
        }


# ============================================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("⧫⟡⧫ ПРОТОНОВЕЯ: FDL Core Engine ⧫⟡⧫\n")
    
    # 1. Создание Блока Требований (БТ)
    print("1. Инициализация Блока Требований (БТ)...")
    requirements = RequirementsBlock()
    
    # Регистрация ресурсов
    requirements.register_resource(
        Resource(ResourceType.SR3_FINANCIAL, 1000000, 1000000, unit="грн")
    )
    requirements.register_resource(
        Resource(ResourceType.SR1_HUMAN, 50, 50, unit="чел")
    )
    requirements.register_resource(
        Resource(ResourceType.SR4_TIME, 365, 365, unit="дни")
    )
    
    # Регистрация целей
    goal1 = Goal(
        id="GOAL_001",
        name="Развитие сектора образования",
        description="Повышение качества образования в Николаевском регионе",
        priority=5
    )
    requirements.register_goal(goal1)
    
    print("   ✅ Ресурсы и цели зарегистрированы\n")
    
    # 2. Тестирование фильтра
    print("2. Тестирование фильтра законности...")
    
    # Запрос с достаточными ресурсами
    request1 = {
        "goal_id": "GOAL_001",
        "resources_needed": {
            "SR3_FINANCIAL": 500000,
            "SR1_HUMAN": 20,
            "SR4_TIME": 180
        },
        "description": "Создание образовательного центра"
    }
    
    approved, reason, details = requirements.filter_request(request1)
    print(f"   Запрос 1: {'✅ ОДОБРЕН' if approved else '❌ БЛОКИРОВАН'}")
    print(f"   Причина: {reason}\n")
    
    # Запрос с недостаточными ресурсами (АВАНТЮРА)
    request2 = {
        "goal_id": "GOAL_001",
        "resources_needed": {
            "SR3_FINANCIAL": 2000000,  # Больше, чем доступно!
        },
        "description": "Глобальная реформа"
    }
    
    approved, reason, details = requirements.filter_request(request2)
    print(f"   Запрос 2: {'✅ ОДОБРЕН' if approved else '❌ БЛОКИРОВАН'}")
    print(f"   Причина: {reason}\n")
    
    # 3. Демонстрация цикла ФДЛ
    print("3. Демонстрация цикла Неби-Ула (T→A→§→Test→Stop)...")
    
    cycle = FDLCycle()
    
    # Тезис
    cycle.set_thesis(
        state={"education_quality": 60, "teachers": 100},
        description="Текущее состояние образования"
    )
    print(f"   Фаза: {cycle.phase.value}")
    
    # Антитезис
    cycle.set_antithesis(
        obstacle={"funding_shortage": 0.4, "teacher_shortage": 0.3},
        conflict="Недостаток финансирования и кадров"
    )
    print(f"   Фаза: {cycle.phase.value}")
    
    # Синтез
    cycle.set_synthesis(
        solution={"partnership_model": "государство-частный сектор"},
        new_model={"education_quality": 85, "teachers": 150}
    )
    print(f"   Фаза: {cycle.phase.value}")
    
    # Тест
    def test_solution(synthesis):
        new_quality = synthesis['new_model']['education_quality']
        return new_quality > 80
    
    test_passed = cycle.test(test_solution)
    print(f"   Фаза: {cycle.phase.value} - {'✅ ПРОЙДЕН' if test_passed else '❌ НЕ ПРОЙДЕН'}")
    
    # Стоп
    cycle.stop("Решение найдено и протестировано")
    print(f"   Фаза: {cycle.phase.value}\n")
    
    # 4. Статистика
    print("4. Статистика работы системы:")
    stats = requirements.get_filter_statistics()
    print(f"   Всего запросов: {stats['total_requests']}")
    print(f"   Одобрено: {stats['approved']}")
    print(f"   Блокировано: {stats['blocked']}")
    print(f"   Процент одобрения: {stats['approval_rate']:.1%}\n")
    
    print("⧫⟡⧫ FDL CORE ENGINE: OPERATIONAL ⧫⟡⧫")
