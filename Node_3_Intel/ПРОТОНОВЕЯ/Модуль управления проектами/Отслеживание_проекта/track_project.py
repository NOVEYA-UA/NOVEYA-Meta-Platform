# Протоновея/Модуль управления проектами/Отслеживание_проекта/track_project.py

class ProjectTracker:
    def __init__(self, project):
        self.project = project
        self.tasks = {}

    def add_task_status(self, task_id, status):
        # Добавление статуса для задачи
        if task_id in self.tasks:
            self.tasks[task_id].append(status)
        else:
            self.tasks[task_id] = [status]
        print(f"Status '{status}' added for task {task_id}.")

    def get_task_statuses(self, task_id):
        # Получение всех статусов для задачи
        if task_id in self.tasks:
            return self.tasks[task_id]
        else:
            return []

# Пример использования
if __name__ == "__main__":
    # Создаем проект
    project = Project(name="Sample Project", description="This is a sample project", start_date="2024-03-15", end_date="2024-05-30", budget=10000, participants=["John", "Alice", "Bob"])

    # Инициализируем трекер проекта
    tracker = ProjectTracker(project)

    # Добавляем статусы задач
    tracker.add_task_status(task_id=1, status="In Progress")
    tracker.add_task_status(task_id=1, status="Completed")
    tracker.add_task_status(task_id=2, status="To Do")

    # Получаем статусы для задачи
    task_id = 1
    task_statuses = tracker.get_task_statuses(task_id)
    print(f"Statuses for task {task_id}: {task_statuses}")
