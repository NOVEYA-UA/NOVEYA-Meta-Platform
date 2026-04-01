import json
import os

class EvaluationModule:
    def __init__(self):
        self.means = {
            "Ср1": "Средства производства",
            "Ср2": "Орудия труда",
            "Ср3": "Финансы",
            "Ср4": "Ресурсы",
            "Ср5": "Информационные средства",
            "Ср6": "Social processes",
            "Ср7": "Potential of education",
            "Ср8": "Potential of creativity",
            "Ср9": "Potential of health"
        }

    def calculate_vitality_index(self, goal_weights):
        print("🔍 [ФДЛ] Анализ тензоров решения через ОЦРЕ...")
        if not goal_weights: return 0
        total_rank = sum(goal_weights.values())
        return round(total_rank, 3)

if __name__ == "__main__":
    evaluator = EvaluationModule()
    test_weights = {"Ср3": 0.85, "Ср9": 0.95, "Ср7": 0.70}
    print(f"✅ РЕЗУЛЬТАТ: Индекс жизнеспособности: {evaluator.calculate_vitality_index(test_weights)}")
