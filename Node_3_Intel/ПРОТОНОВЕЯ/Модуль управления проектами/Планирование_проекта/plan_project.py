# Протоновея/Модуль управления проектами/Планирование_проекта/plan_project.py

class ProjectPlanner:
    def __init__(self, project):
        self.project = project

    def add_task(self, task):
        # Добавление задачи к проекту
        pass

    def remove_task(self, task_id):
        # Удаление задачи из проекта
        pass

    def assign_task(self, task_id, assignee):
        # Назначение исполнителя на задачу
        pass

    def set_deadline(self, task_id, deadline):
        # Установка срока выполнения для задачи
        pass

    def update_progress(self, task_id, progress):
        # Обновление прогресса выполнения задачи
        pass

# Пример использования
if __name__ == "__main__":
    # Создаем проект
    project = Project(name="Sample Project", description="This is a sample project", start_date="2024-03-15", end_date="2024-05-30", budget=10000, participants=["John", "Alice", "Bob"])

    # Инициализируем планировщик проекта
    planner = ProjectPlanner(project)

    # Добавляем задачи
    task1 = Task(id=1, description="Task 1", status="To Do")
    task2 = Task(id=2, description="Task 2", status="In Progress")
    task3 = Task(id=3, description="Task 3", status="Done")

    # Добавляем задачи к проекту
    planner.add_task(task1)
    planner.add_task(task2)
    planner.add_task(task3)
