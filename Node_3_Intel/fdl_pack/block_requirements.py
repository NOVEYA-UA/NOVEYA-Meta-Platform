#!/usr/bin/env python3
"""
⧫⟡⧫ ΠΡΟΤΟΝΟΒΕΑ: Блок Требований (БТ) ⧫⟡⧫
Фильтр Законности - Надсмотрщик системы

Роль: Проверка любого входящего запроса на:
- Наличие ресурсов (Ср1-Ср9)
- Соответствие Целевым Установкам (ЦУ 1-5)
- Значимость (Zn)

Коррекция 2017: Потребности ⇄ Цели меняются местами
"""

import time
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    """Типы технологических средств (Ср1-Ср9)"""
    SR1_MATERIAL = "Ср1"  # Материальные ресурсы
    SR2_METHODOLOGY = "Ср2"  # Методология ФДЛ
    SR3_TERRITORY = "Ср3"  # Территория (Николаев)
    SR4_PERSONNEL = "Ср4"  # Кадры
    SR5_TECHNOLOGY = "Ср5"  # Технологии
    SR6_INFORMATION = "Ср6"  # Информационные системы
    SR7_INFRASTRUCTURE = "Ср7"  # Социальная инфраструктура
    SR8_SPIRITUAL = "Ср8"  # Духовный потенциал
    SR9_INTERNATIONAL = "Ср9"  # Международные связи


class TargetGoal(Enum):
    """Целевые Установки (ЦУ 1-5)"""
    CU1_GRAD_SAD = "CU1"  # Восстановление Града-Сада
    CU2_BIO_NORM = "CU2"  # Биологическая нормализация
    CU3_MERIDIAN = "CU3"  # Снятие дискретности меридианов
    CU4_SECTORS = "CU4"  # Интеграция 24 секторов
    CU5_METAHARMONY = "CU5"  # Метагармония 432 Гц


@dataclass
class FilterResult:
    """Результат фильтрации запроса"""
    lawful: bool
    resources_available: bool
    significance: float
    verdict: str
    reason: str = ""
    synthesis: str = ""
    resources_present: List[str] = None
    resources_missing: List[str] = None
    
    def __post_init__(self):
        if self.resources_present is None:
            self.resources_present = []
        if self.resources_missing is None:
            self.resources_missing = []


class BlockRequirements:
    """
    Блок Требований (БТ) - Фильтр Законности
    
    Принципы:
    1. Законность — основа и результат созидания
    2. Реализация без ресурсов = АВАНТЮРА
    3. Проверка значимости (Zn) относительно ЦУ
    """
    
    def __init__(self):
        self.resources: Dict[str, float] = {}
        self.significance_weights: Dict[str, float] = {}
        self.role = "Надсмотрщик (Законность)"
        
        # Карта ресурсов для каждой ЦУ
        self.cu_resource_map = {
            TargetGoal.CU1_GRAD_SAD.value: [
                ResourceType.SR1_MATERIAL.value,
                ResourceType.SR3_TERRITORY.value,
                ResourceType.SR7_INFRASTRUCTURE.value
            ],
            TargetGoal.CU2_BIO_NORM.value: [
                ResourceType.SR2_METHODOLOGY.value,
                ResourceType.SR4_PERSONNEL.value,
                ResourceType.SR8_SPIRITUAL.value
            ],
            TargetGoal.CU3_MERIDIAN.value: [
                ResourceType.SR5_TECHNOLOGY.value,
                ResourceType.SR6_INFORMATION.value
            ],
            TargetGoal.CU4_SECTORS.value: [
                ResourceType.SR1_MATERIAL.value,
                ResourceType.SR9_INTERNATIONAL.value
            ],
            TargetGoal.CU5_METAHARMONY.value: [
                ResourceType.SR8_SPIRITUAL.value
            ]
        }
        
        # Ключевые слова для ЦУ
        self.cu_keywords = {
            TargetGoal.CU1_GRAD_SAD.value: ["град", "сад", "николаев", "mykolaiv", "восстановление"],
            TargetGoal.CU2_BIO_NORM.value: ["биологи", "нормализ", "здоровье", "ФДЛ", "экология"],
            TargetGoal.CU3_MERIDIAN.value: ["меридиан", "дискретност", "снятие", "связность"],
            TargetGoal.CU4_SECTORS.value: ["сектор", "24", "интеграция", "развитие"],
            TargetGoal.CU5_METAHARMONY.value: ["метагармон", "резонанс", "432", "гармония"]
        }
    
    def filter_impulse(self, request: str, cu_id: str) -> FilterResult:
        """
        Основная функция фильтрации входящего запроса
        
        Цикл ФДЛ:
        1. Тезис - извлечение сути запроса
        2. Антитезис - проверка ресурсов и значимости
        3. Синтез - вынесение вердикта
        
        Args:
            request: Текст запроса
            cu_id: ID Целевой Установки (CU1-CU5)
        
        Returns:
            FilterResult с полной информацией о проверке
        """
        
        # ТЕЗИС: Извлечение сути
        thesis = self._extract_essence(request)
        
        # АНТИТЕЗИС: Проверка ресурсов
        resources_check = self._check_resources(cu_id)
        
        # АНТИТЕЗИС: Проверка значимости
        significance = self._calculate_significance(thesis, cu_id)
        
        # СИНТЕЗ: Авантюра (нет ресурсов)
        if not resources_check["available"]:
            return FilterResult(
                lawful=False,
                resources_available=False,
                significance=0.0,
                verdict="БЛОКИРОВАНО",
                reason=f"АВАНТЮРА: Отсутствуют ресурсы {resources_check['resources_missing']}",
                resources_present=resources_check["resources_present"],
                resources_missing=resources_check["resources_missing"]
            )
        
        # СИНТЕЗ: Законно (есть ресурсы + значимость)
        if resources_check["available"] and significance >= 0.5:
            return FilterResult(
                lawful=True,
                resources_available=True,
                significance=significance,
                verdict="ПРОПУЩЕНО",
                synthesis="ЗАКОННО: Ресурсы обеспечены, значимость подтверждена",
                resources_present=resources_check["resources_present"],
                resources_missing=[]
            )
        
        # СИНТЕЗ: Ожидание корректировки (есть ресурсы, но низкая значимость)
        return FilterResult(
            lawful=False,
            resources_available=True,
            significance=significance,
            verdict="ОЖИДАНИЕ КОРРЕКТИРОВКИ",
            reason=f"Значимость недостаточна ({significance:.2f} < 0.5)",
            resources_present=resources_check["resources_present"],
            resources_missing=[]
        )
    
    def _extract_essence(self, request: str) -> Dict[str, Any]:
        """Извлечение сути запроса (ТЕЗИС)"""
        return {
            "type": self._classify_request(request),
            "content": request,
            "length": len(request),
            "timestamp": time.time()
        }
    
    def _classify_request(self, request: str) -> str:
        """Классификация типа запроса"""
        request_lower = request.lower()
        
        strategic_keywords = ["стратег", "план", "долгосрочн", "перспектив", "концепц"]
        tactical_keywords = ["задача", "этап", "проект", "тактик", "реализ"]
        
        if any(kw in request_lower for kw in strategic_keywords):
            return "strategic"
        elif any(kw in request_lower for kw in tactical_keywords):
            return "tactical"
        else:
            return "operational"
    
    def _check_resources(self, cu_id: str) -> Dict[str, Any]:
        """
        Проверка наличия технологических средств (АНТИТЕЗИС)
        
        Args:
            cu_id: ID Целевой Установки
        
        Returns:
            dict с информацией о доступности ресурсов
        """
        required_resources = self.cu_resource_map.get(cu_id, [])
        
        if not required_resources:
            # Если не указаны требуемые ресурсы, считаем доступными
            return {
                "available": True,
                "resources_present": [],
                "resources_missing": [],
                "coverage": 1.0
            }
        
        available = []
        missing = []
        
        for resource in required_resources:
            if resource in self.resources and self.resources[resource] > 0:
                available.append(resource)
            else:
                missing.append(resource)
        
        coverage = len(available) / len(required_resources) if required_resources else 0
        
        return {
            "available": len(missing) == 0,
            "resources_present": available,
            "resources_missing": missing,
            "coverage": coverage
        }
    
    def _calculate_significance(self, thesis: Dict[str, Any], cu_id: str) -> float:
        """
        Расчёт значимости (Zn) запроса относительно ЦУ (АНТИТЕЗИС)
        
        Формула: Zn = базовая + коррекция_типа + коррекция_ЦУ
        
        Args:
            thesis: Извлечённая суть запроса
            cu_id: ID Целевой Установки
        
        Returns:
            float значимость от 0 до 1
        """
        base_significance = 0.3
        
        # Коррекция по типу запроса
        if thesis["type"] == "strategic":
            base_significance += 0.3
        elif thesis["type"] == "tactical":
            base_significance += 0.2
        
        # Коррекция по соответствию ЦУ
        if self._aligns_with_cu(thesis["content"], cu_id):
            base_significance += 0.4
        
        # Коррекция по длине (детализация)
        if thesis["length"] > 100:
            base_significance += 0.1
        
        return min(1.0, base_significance)
    
    def _aligns_with_cu(self, content: str, cu_id: str) -> bool:
        """Проверка соответствия запроса целевой установке"""
        keywords = self.cu_keywords.get(cu_id, [])
        content_lower = content.lower()
        
        # Подсчёт совпадений ключевых слов
        matches = sum(1 for kw in keywords if kw in content_lower)
        
        # Считаем соответствующим, если хотя бы 1 ключевое слово
        return matches > 0
    
    def register_resources(self, resource_dict: Dict[str, float]) -> str:
        """
        Регистрация доступных технологических средств
        
        Args:
            resource_dict: Словарь {resource_id: amount}
        
        Returns:
            str подтверждение регистрации
        """
        self.resources.update(resource_dict)
        return f"✅ Ресурсы зарегистрированы: {list(resource_dict.keys())}"
    
    def get_resource_status(self) -> Dict[str, float]:
        """Получение текущего статуса ресурсов"""
        return self.resources.copy()
    
    def export_status(self) -> str:
        """Экспорт статуса БТ в JSON"""
        status = {
            "role": self.role,
            "resources": self.resources,
            "cu_resource_map": self.cu_resource_map,
            "timestamp": time.time()
        }
        return json.dumps(status, indent=2, ensure_ascii=False)


# ============================================================================
# ДЕМОНСТРАЦИЯ
# ============================================================================

if __name__ == "__main__":
    print("⧫⟡⧫ ΠΡΟΤΟΝΟΒΕΑ: Блок Требований (БТ) ⧫⟡⧫\n")
    
    # Инициализация
    bt = BlockRequirements()
    print(f"Роль: {bt.role}\n")
    
    # Регистрация ресурсов
    resources = {
        ResourceType.SR1_MATERIAL.value: 100,
        ResourceType.SR2_METHODOLOGY.value: 80,
        ResourceType.SR3_TERRITORY.value: 90,
        ResourceType.SR4_PERSONNEL.value: 70,
        ResourceType.SR5_TECHNOLOGY.value: 60,
        ResourceType.SR6_INFORMATION.value: 50,
        ResourceType.SR7_INFRASTRUCTURE.value: 85,
        ResourceType.SR8_SPIRITUAL.value: 95,
        ResourceType.SR9_INTERNATIONAL.value: 40
    }
    
    print(bt.register_resources(resources))
    print()
    
    # ТЕСТ 1: Законный запрос
    print("="*70)
    print("ТЕСТ 1: Законный запрос (с ресурсами)")
    print("="*70)
    
    request1 = "Создать стратегический план восстановления Града-Сада в Николаеве через интеграцию 24 секторов развития"
    result1 = bt.filter_impulse(request1, TargetGoal.CU1_GRAD_SAD.value)
    
    print(f"Запрос: {request1}")
    print(f"Вердикт: {result1.verdict}")
    print(f"Законность: {result1.lawful}")
    print(f"Ресурсы доступны: {result1.resources_available}")
    print(f"Значимость: {result1.significance:.2f}")
    print(f"Синтез: {result1.synthesis}")
    print(f"Ресурсы присутствуют: {result1.resources_present}")
    print()
    
    # ТЕСТ 2: Авантюрный запрос
    print("="*70)
    print("ТЕСТ 2: Авантюрный запрос (без ресурсов)")
    print("="*70)
    
    # Обнуляем ресурс
    bt.resources[ResourceType.SR9_INTERNATIONAL.value] = 0
    
    request2 = "Запустить международную программу по 24 секторам"
    result2 = bt.filter_impulse(request2, TargetGoal.CU4_SECTORS.value)
    
    print(f"Запрос: {request2}")
    print(f"Вердикт: {result2.verdict}")
    print(f"Законность: {result2.lawful}")
    print(f"Ресурсы доступны: {result2.resources_available}")
    print(f"Причина: {result2.reason}")
    print(f"Ресурсы отсутствуют: {result2.resources_missing}")
    print()
    
    print("⧫⟡⧫ Демонстрация завершена ⧫⟡⧫")
