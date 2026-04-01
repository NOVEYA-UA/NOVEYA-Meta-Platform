class Project:
    def __init__(self, name, description, start_date, end_date, budget, participants):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.participants = participants
        self.progress = 0  # Добавим поле для отслеживания прогресса проекта

    def __str__(self):
        return f"Project: {self.name}\nDescription: {self.description}\nStart Date: {self.start_date}\nEnd Date: {self.end_date}\nBudget: {self.budget}\nParticipants: {', '.join(self.participants)}\nProgress: {self.progress}%"

    def update_progress(self, progress):
        if 0 <= progress <= 100:
            self.progress = progress
            print(f"Progress for project '{self.name}' updated to {self.progress}%")
        else:
            print("Invalid progress value. Progress should be between 0 and 100.")

    def allocate_resources(self, resource):
        # Логика распределения ресурсов
        print(f"Resources allocated for project '{self.name}': {resource}")


def create_project(name, description, start_date, end_date, budget, participants):
    # Создание нового проекта
    project = Project(name, description, start_date, end_date, budget, participants)
    return project

# Пример использования
if __name__ == "__main__":
    project_name = input("Enter project name: ")
    project_description = input("Enter project description: ")
    project_start_date = input("Enter project start date: ")
    project_end_date = input("Enter project end date: ")
    project_budget = float(input("Enter project budget: "))
    project_participants = input("Enter project participants (comma separated): ").split(',')

    project = create_project(project_name, project_description, project_start_date, project_end_date, project_budget, project_participants)
    print("Project created successfully:")
    print(project)

    # Обновление прогресса проекта
    project.update_progress(25)

    # Распределение ресурсов
    project.allocate_resources("10 developers, 5 designers")
