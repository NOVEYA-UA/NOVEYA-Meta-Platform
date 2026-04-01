import random
from Отслеживание_проекта.track_project import ProjectTracker
from Управление_ресурсами.manage_resources import ResourceManager

class SolutionEvaluator:
    def __init__(self, project_tracker, resource_manager):
        self.project_tracker = project_tracker
        self.resource_manager = resource_manager
    
    def evaluate(self, solution):
        """
        Метод для оценки решения.
        
        Parameters:
            solution (dict): Словарь с информацией о решении.
        
        Returns:
            float: Оценка решения.
        """
        # Пример: оценка решения как сумма случайных значений параметров
        evaluation = sum(solution.values())
        return evaluation
    
    def visualize(self, solution):
        """
        Метод для визуализации решения.
        
        Parameters:
            solution (dict): Словарь с информацией о решении.
        """
        print("Визуализация решения:")
        for key, value in solution.items():
            print(f"{key}: {value}")

    def track_solution(self, solution):
        """
        Метод для отслеживания реализации решения.
        
        Parameters:
            solution (dict): Словарь с информацией о решении.
        """
        # Предположим, что реализация решения приводит к добавлению задачи в проект
        task_description = "Implement solution"
        task_id = random.randint(1000, 9999)  # Генерируем уникальный идентификатор задачи
        self.project_tracker.add_task_status(task_id, "To Do")
        self.project_tracker.add_task_status(task_id, "In Progress")
        self.project_tracker.add_task_status(task_id, "Completed")
        print(f"Task '{task_description}' added to project and tracked.")

    def allocate_resources(self, solution):
        """
        Метод для выделения ресурсов для реализации решения.
        
        Parameters:
            solution (dict): Словарь с информацией о решении.
        """
        # Предположим, что реализация решения требует определенного количества ресурсов
        for resource, quantity in solution.items():
            self.resource_manager.add_resource(resource, quantity)
            print(f"{quantity} units of resource '{resource}' allocated.")
        print("Resources allocated.")

# Пример использования
if __name__ == "__main__":
    # Инициализируем трекер проекта и менеджер ресурсов
    project_tracker = ProjectTracker(project)
    resource_manager = ResourceManager()

    # Инициализируем оценщика решений с трекером проекта и менеджером ресурсов
    evaluator = SolutionEvaluator(project_tracker, resource_manager)

    # Пример решения, которое нужно оценить и реализовать
    solution = {"param1": random.randint(1, 10), "param2": random.randint(1, 10)}

    # Оцениваем решение
    evaluation = evaluator.evaluate(solution)
    print("Evaluation result:", evaluation)

    # Визуализируем решение
    evaluator.visualize(solution)

    # Отслеживаем реализацию решения
    evaluator.track_solution(solution)

    # Выделяем ресурсы для реализации решения
    evaluator.allocate_resources(solution)
