#!/usr/bin/env python3
"""
⧫⟡⧫ ПРОТОНОВЕЯ: Модуль 5 Блоков Системного Подхода ⧫⟡⧫

Модуль: system_blocks.py
Назначение: Реализация 5 блоков системного подхода по Кашеваровой

Блоки:
    БМ - Блок Мотивации (Руководитель, знающий перспективу)
    БТ - Блок Требований (Надсмотрщик за законностью)
    БИ - Блок Идей (Генератор гипотез и моделей)
    БЦ - Блок Целесообразности (Выбор лучшего решения)
    БВ - Блок Возможностей (Оценка условий "после")

Автор: ПРОТОНОВЕЯ AI-Регулятор
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

from fdl_core import (
    Resource, ResourceType, Goal, FDLCycle,
    RequirementsBlock, SystemConstants
)


# ============================================================================
# БЛОК МОТИВАЦИИ (БМ) - Руководитель, знающий перспективу
# ============================================================================

@dataclass
class Perspective:
    """
    Перспектива развития
    
    Attributes:
        id: Идентификатор
        name: Название перспективы
        timeframe: Временной горизонт (в годах)
        description: Описание
        goals: Целевые установки (ЦУ 1-5)
    """
    id: str
    name: str
    timeframe: int  # в годах
    description: str
    goals: List[Goal] = field(default_factory=list)
    
    def add_goal(self, goal: Goal):
        """Добавление цели к перспективе"""
        self.goals.append(goal)
        # Сортировка по приоритету
        self.goals.sort(key=lambda g: g.priority, reverse=True)
    
    def get_priority_goals(self, top_n: int = 5) -> List[Goal]:
        """Получение топ-N приоритетных целей"""
        return self.goals[:top_n]


class MotivationBlock:
    """
    Блок Мотивации (БМ)
    
    Роль: Руководитель, знающий перспективу
    Функции:
        - Определение целей (ЦУ 1-5)
        - Формирование стратегического видения
        - Управление приоритетами
    """
    
    def __init__(self):
        self.perspectives: Dict[str, Perspective] = {}
        self.strategic_vision: Optional[str] = None
        self.mission: Optional[str] = None
    
    def set_mission(self, mission: str):
        """Установка миссии организации"""
        self.mission = mission
    
    def set_strategic_vision(self, vision: str):
        """Установка стратегического видения"""
        self.strategic_vision = vision
    
    def add_perspective(self, perspective: Perspective):
        """Добавление перспективы развития"""
        self.perspectives[perspective.id] = perspective
    
    def get_all_goals(self) -> List[Goal]:
        """Получение всех целей из всех перспектив"""
        all_goals = []
        for perspective in self.perspectives.values():
            all_goals.extend(perspective.goals)
        
        # Сортировка по приоритету
        all_goals.sort(key=lambda g: g.priority, reverse=True)
        return all_goals
    
    def generate_motivation_report(self) -> Dict:
        """Генерация отчёта о мотивации"""
        return {
            "mission": self.mission,
            "strategic_vision": self.strategic_vision,
            "perspectives_count": len(self.perspectives),
            "total_goals": len(self.get_all_goals()),
            "top_5_goals": [
                {
                    "id": g.id,
                    "name": g.name,
                    "priority": g.priority
                }
                for g in self.get_all_goals()[:5]
            ]
        }


# ============================================================================
# БЛОК ИДЕЙ (БИ) - Генератор гипотез и моделей
# ============================================================================

@dataclass
class Model:
    """
    Модель решения ($М$)
    
    Attributes:
        id: Идентификатор модели
        name: Название
        description: Описание
        sector: Сектор развития (1-24)
        hypothesis: Гипотеза
        expected_result: Ожидаемый результат
    """
    id: str
    name: str
    description: str
    sector: int  # 1-24 (Николаев)
    hypothesis: str
    expected_result: Dict
    resources_estimated: Dict[ResourceType, float] = field(default_factory=dict)


class IdeasBlock:
    """
    Блок Идей (БИ)
    
    Роль: Генератор гипотез и моделей
    Функции:
        - Генерация идей на основе 24 секторов развития
        - Создание моделей решений ($М$)
        - Управление гипотезами
    """
    
    def __init__(self):
        self.models: Dict[str, Model] = {}
        self.sectors: Dict[int, List[str]] = {i: [] for i in range(1, 25)}
    
    def add_model(self, model: Model):
        """Добавление модели решения"""
        self.models[model.id] = model
        if 1 <= model.sector <= 24:
            self.sectors[model.sector].append(model.id)
    
    def get_models_by_sector(self, sector: int) -> List[Model]:
        """Получение моделей по сектору"""
        model_ids = self.sectors.get(sector, [])
        return [self.models[mid] for mid in model_ids]
    
    def generate_ideas_for_goal(
        self, 
        goal: Goal, 
        sector: int,
        creativity_level: float = 0.7
    ) -> List[Model]:
        """
        Генерация идей для достижения цели
        
        Args:
            goal: Целевая установка
            sector: Сектор развития (1-24)
            creativity_level: Уровень креативности (0.0-1.0)
        
        Returns:
            Список сгенерированных моделей
        """
        # Генерация базовых моделей
        base_models = []
        
        # Модель 1: Традиционный подход
        model1 = Model(
            id=f"M_{goal.id}_TRAD",
            name=f"Традиционный подход к {goal.name}",
            description=f"Классическое решение для {goal.description}",
            sector=sector,
            hypothesis=f"Применение проверенных методов",
            expected_result={"efficiency": 0.7},
            resources_estimated=goal.resources_required
        )
        base_models.append(model1)
        
        # Модель 2: Инновационный подход (если creativity_level > 0.5)
        if creativity_level > 0.5:
            model2 = Model(
                id=f"M_{goal.id}_INNOV",
                name=f"Инновационный подход к {goal.name}",
                description=f"Новаторское решение для {goal.description}",
                sector=sector,
                hypothesis=f"Применение новых технологий и методов",
                expected_result={"efficiency": 0.9},
                resources_estimated={
                    k: v * 1.2 for k, v in goal.resources_required.items()
                }
            )
            base_models.append(model2)
        
        # Модель 3: Гибридный подход (если creativity_level > 0.7)
        if creativity_level > 0.7:
            model3 = Model(
                id=f"M_{goal.id}_HYBRID",
                name=f"Гибридный подход к {goal.name}",
                description=f"Комбинированное решение для {goal.description}",
                sector=sector,
                hypothesis=f"Синтез традиций и инноваций",
                expected_result={"efficiency": 0.85},
                resources_estimated={
                    k: v * 1.1 for k, v in goal.resources_required.items()
                }
            )
            base_models.append(model3)
        
        # Добавление всех моделей
        for model in base_models:
            self.add_model(model)
        
        return base_models


# ============================================================================
# БЛОК ЦЕЛЕСООБРАЗНОСТИ (БЦ) - Выбор лучшего решения
# ============================================================================

@dataclass
class Alternative:
    """
    Альтернативное решение для оценки
    
    Attributes:
        model: Модель решения
        costs: Затраты (эквиваленты)
        benefits: Выгоды
        effectiveness: Эффективность (ОЦРЕ)
    """
    model: Model
    costs: Dict[str, float]
    benefits: Dict[str, float]
    effectiveness: float = 0.0
    
    def calculate_effectiveness(self) -> float:
        """
        Расчёт эффективности по Таблице 3.ОЦРЕ
        
        Формула: Effectiveness = Benefits / Costs
        """
        total_costs = sum(self.costs.values())
        total_benefits = sum(self.benefits.values())
        
        if total_costs > 0:
            self.effectiveness = total_benefits / total_costs
        else:
            self.effectiveness = 0.0
        
        return self.effectiveness


class PurposefulnessBlock:
    """
    Блок Целесообразности (БЦ)
    
    Роль: Выбор лучшего решения
    Функции:
        - Оценка альтернатив
        - Применение Таблицы 3.ОЦРЕ (Оценка Решения)
        - Сравнение по суммам эквивалентов затрат
    """
    
    def __init__(self):
        self.alternatives: List[Alternative] = []
        self.selected_alternative: Optional[Alternative] = None
    
    def add_alternative(self, alternative: Alternative):
        """Добавление альтернативы для оценки"""
        alternative.calculate_effectiveness()
        self.alternatives.append(alternative)
    
    def evaluate_alternatives(self) -> List[Alternative]:
        """
        Оценка всех альтернатив
        
        Returns:
            Список альтернатив, отсортированных по эффективности
        """
        # Пересчёт эффективности
        for alt in self.alternatives:
            alt.calculate_effectiveness()
        
        # Сортировка по эффективности (убывание)
        self.alternatives.sort(key=lambda a: a.effectiveness, reverse=True)
        
        return self.alternatives
    
    def select_best(self) -> Optional[Alternative]:
        """
        Выбор лучшей альтернативы
        
        Returns:
            Лучшая альтернатива или None
        """
        if not self.alternatives:
            return None
        
        # Оценка всех альтернатив
        evaluated = self.evaluate_alternatives()
        
        # Выбор лучшей (с наивысшей эффективностью)
        self.selected_alternative = evaluated[0]
        
        return self.selected_alternative
    
    def compare_alternatives(self) -> Dict:
        """
        Сравнение альтернатив (Таблица 3.ОЦРЕ)
        
        Returns:
            Сравнительная таблица
        """
        comparison = []
        
        for alt in self.alternatives:
            comparison.append({
                "model_id": alt.model.id,
                "model_name": alt.model.name,
                "total_costs": sum(alt.costs.values()),
                "total_benefits": sum(alt.benefits.values()),
                "effectiveness": alt.effectiveness,
                "rank": None  # Будет заполнено ниже
            })
        
        # Сортировка по эффективности
        comparison.sort(key=lambda x: x['effectiveness'], reverse=True)
        
        # Присвоение рангов
        for i, item in enumerate(comparison, 1):
            item['rank'] = i
        
        return {
            "comparison_table": comparison,
            "best_alternative": comparison[0] if comparison else None
        }


# ============================================================================
# БЛОК ВОЗМОЖНОСТЕЙ (БВ) - Оценка условий "после"
# ============================================================================

@dataclass
class Conditions:
    """
    Условия системы
    
    Attributes:
        before: Условия "до" внедрения решения
        after: Условия "после" внедрения решения
    """
    before: Dict[str, float]  # $Уп$ - условия "после"
    after: Dict[str, float]


class PossibilitiesBlock:
    """
    Блок Возможностей (БВ)
    
    Роль: Оценка условий "после"
    Функции:
        - Оценка условий "после" ($Уп$)
        - Расчёт индекса жизнеспособности
        - Прогнозирование результатов
    """
    
    def __init__(self):
        self.conditions: Optional[Conditions] = None
        self.viability_index: float = 0.0
    
    def set_conditions(self, before: Dict[str, float], after: Dict[str, float]):
        """Установка условий "до" и "после" """
        self.conditions = Conditions(before=before, after=after)
    
    def calculate_viability_index(self) -> float:
        """
        Расчёт индекса жизнеспособности
        
        Формула: VI = Σ(after_values) / Σ(before_values)
        
        Returns:
            Индекс жизнеспособности
        """
        if not self.conditions:
            return 0.0
        
        total_before = sum(self.conditions.before.values())
        total_after = sum(self.conditions.after.values())
        
        if total_before > 0:
            self.viability_index = total_after / total_before
        else:
            self.viability_index = 0.0
        
        return self.viability_index
    
    def evaluate_improvement(self) -> Dict:
        """
        Оценка улучшений по каждому параметру
        
        Returns:
            Словарь с оценками улучшений
        """
        if not self.conditions:
            return {}
        
        improvements = {}
        
        for key in self.conditions.before.keys():
            before_val = self.conditions.before.get(key, 0)
            after_val = self.conditions.after.get(key, 0)
            
            if before_val > 0:
                improvement = ((after_val - before_val) / before_val) * 100
            else:
                improvement = 0
            
            improvements[key] = {
                "before": before_val,
                "after": after_val,
                "improvement_percent": improvement
            }
        
        return improvements
    
    def generate_forecast(self) -> Dict:
        """
        Генерация прогноза результатов
        
        Returns:
            Прогноз с индексом жизнеспособности и улучшениями
        """
        viability = self.calculate_viability_index()
        improvements = self.evaluate_improvement()
        
        # Оценка общего состояния
        if viability > 1.2:
            status = "ОТЛИЧНОЕ"
        elif viability > 1.0:
            status = "ХОРОШЕЕ"
        elif viability > 0.8:
            status = "УДОВЛЕТВОРИТЕЛЬНОЕ"
        else:
            status = "НЕУДОВЛЕТВОРИТЕЛЬНОЕ"
        
        return {
            "viability_index": viability,
            "status": status,
            "improvements": improvements,
            "recommendation": self._generate_recommendation(viability)
        }
    
    def _generate_recommendation(self, viability: float) -> str:
        """Генерация рекомендации на основе индекса"""
        if viability > 1.2:
            return "Решение рекомендуется к внедрению. Высокая жизнеспособность."
        elif viability > 1.0:
            return "Решение приемлемо. Положительный эффект."
        elif viability > 0.8:
            return "Решение требует доработки. Умеренный эффект."
        else:
            return "Решение не рекомендуется. Низкая жизнеспособность."


# ============================================================================
# ИНТЕГРИРОВАННЫЙ СИСТЕМНЫЙ ПОДХОД
# ============================================================================

class SystemApproach:
    """
    Интегрированный Системный Подход
    
    Объединяет все 5 блоков:
        БМ → БТ → БИ → БЦ → БВ
    """
    
    def __init__(self):
        self.motivation = MotivationBlock()
        self.requirements = RequirementsBlock()
        self.ideas = IdeasBlock()
        self.purposefulness = PurposefulnessBlock()
        self.possibilities = PossibilitiesBlock()
        
        # История выполнения
        self.execution_log: List[Dict] = []
    
    def execute_full_cycle(
        self,
        mission: str,
        vision: str,
        perspective: Perspective,
        sector: int,
        creativity_level: float = 0.7
    ) -> Dict:
        """
        Выполнение полного цикла системного подхода
        
        Args:
            mission: Миссия
            vision: Стратегическое видение
            perspective: Перспектива с целями
            sector: Сектор развития (1-24)
            creativity_level: Уровень креативности
        
        Returns:
            Результат выполнения цикла
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }
        
        # ===== ФАЗА 1: МОТИВАЦИЯ (БМ) =====
        self.motivation.set_mission(mission)
        self.motivation.set_strategic_vision(vision)
        self.motivation.add_perspective(perspective)
        
        motivation_report = self.motivation.generate_motivation_report()
        result["phases"]["БМ_Мотивация"] = motivation_report
        
        # ===== ФАЗА 2: ТРЕБОВАНИЯ (БТ) =====
        # Регистрация целей в БТ
        for goal in perspective.goals:
            self.requirements.register_goal(goal)
        
        # Проверка первой цели (наивысший приоритет)
        top_goal = perspective.goals[0]
        request = {
            "goal_id": top_goal.id,
            "resources_needed": {k.name: v for k, v in top_goal.resources_required.items()},
            "description": top_goal.description
        }
        
        approved, reason, details = self.requirements.filter_request(request)
        result["phases"]["БТ_Требования"] = {
            "approved": approved,
            "reason": reason,
            "goal": top_goal.name
        }
        
        if not approved:
            result["status"] = "BLOCKED_BY_REQUIREMENTS"
            return result
        
        # ===== ФАЗА 3: ИДЕИ (БИ) =====
        models = self.ideas.generate_ideas_for_goal(top_goal, sector, creativity_level)
        result["phases"]["БИ_Идеи"] = {
            "models_generated": len(models),
            "models": [{"id": m.id, "name": m.name} for m in models]
        }
        
        # ===== ФАЗА 4: ЦЕЛЕСООБРАЗНОСТЬ (БЦ) =====
        # Создание альтернатив из моделей
        for model in models:
            # Простая оценка затрат и выгод (в реальности - сложнее)
            costs = {"financial": sum(model.resources_estimated.values()) * 1000}
            benefits = {"quality_improvement": model.expected_result.get("efficiency", 0.7) * 10000}
            
            alternative = Alternative(model=model, costs=costs, benefits=benefits)
            self.purposefulness.add_alternative(alternative)
        
        best_alternative = self.purposefulness.select_best()
        comparison = self.purposefulness.compare_alternatives()
        
        result["phases"]["БЦ_Целесообразность"] = {
            "alternatives_evaluated": len(self.purposefulness.alternatives),
            "best_alternative": best_alternative.model.name if best_alternative else None,
            "comparison_table": comparison
        }
        
        # ===== ФАЗА 5: ВОЗМОЖНОСТИ (БВ) =====
        # Установка условий "до" и "после"
        before_conditions = {"quality": 60, "efficiency": 50, "satisfaction": 55}
        after_conditions = {
            "quality": 60 * (1 + best_alternative.model.expected_result.get("efficiency", 0.7)),
            "efficiency": 50 * 1.4,
            "satisfaction": 55 * 1.3
        } if best_alternative else before_conditions
        
        self.possibilities.set_conditions(before_conditions, after_conditions)
        forecast = self.possibilities.generate_forecast()
        
        result["phases"]["БВ_Возможности"] = forecast
        
        # ===== ИТОГОВЫЙ СТАТУС =====
        result["status"] = "SUCCESS"
        result["selected_model"] = best_alternative.model.name if best_alternative else None
        result["viability_index"] = forecast["viability_index"]
        
        # Логирование
        self.execution_log.append(result)
        
        return result


# ============================================================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ============================================================================

if __name__ == "__main__":
    print("⧫⟡⧫ ПРОТОНОВЕЯ: 5 Блоков Системного Подхода ⧫⟡⧫\n")
    
    # Создание системного подхода
    system = SystemApproach()
    
    # Регистрация ресурсов в БТ
    system.requirements.register_resource(
        Resource(ResourceType.SR3_FINANCIAL, 5000000, 5000000, unit="грн")
    )
    system.requirements.register_resource(
        Resource(ResourceType.SR1_HUMAN, 100, 100, unit="чел")
    )
    
    # Создание перспективы
    perspective = Perspective(
        id="PERSP_2026",
        name="Развитие Николаева 2026-2030",
        timeframe=5,
        description="Стратегическое развитие города на 5 лет"
    )
    
    # Добавление целей
    goal1 = Goal(
        id="GOAL_EDU",
        name="Модернизация образования",
        description="Повышение качества образования",
        priority=5,
        resources_required={
            ResourceType.SR3_FINANCIAL: 2000000,
            ResourceType.SR1_HUMAN: 50
        }
    )
    perspective.add_goal(goal1)
    
    # Выполнение полного цикла
    print("Выполнение полного цикла БМ → БТ → БИ → БЦ → БВ...\n")
    
    result = system.execute_full_cycle(
        mission="Создание процветающего города",
        vision="Николаев - город возможностей",
        perspective=perspective,
        sector=5,  # Сектор образования
        creativity_level=0.8
    )
    
    # Вывод результатов
    print(f"Статус: {result['status']}\n")
    
    for phase_name, phase_data in result['phases'].items():
        print(f"{'='*60}")
        print(f"{phase_name}")
        print(f"{'='*60}")
        print(json.dumps(phase_data, indent=2, ensure_ascii=False))
        print()
    
    print(f"\n📊 Итоговый индекс жизнеспособности: {result['viability_index']:.2f}")
    print(f"✅ Выбранная модель: {result['selected_model']}")
    
    print("\n⧫⟡⧫ СИСТЕМА ГОТОВА К РАБОТЕ ⧫⟡⧫")
