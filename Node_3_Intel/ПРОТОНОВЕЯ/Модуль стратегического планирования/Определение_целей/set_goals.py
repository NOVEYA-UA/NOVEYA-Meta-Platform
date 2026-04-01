class GoalSetter:
    def __init__(self):
        pass
    
    def set_goals(self, project, goals):
        """
        Метод для установки целей проекта.
        
        Parameters:
            project (Project): Объект проекта.
            goals (list): Список целей проекта.
        """
        project.set_goals(goals)
        print("Goals set for the project.")

# Пример использования
if __name__ == "__main__":
    # Создаем проект
    project = Project(name="Sample Project", description="This is a sample project", start_date="2024-03-15", end_date="2024-05-30", budget=10000, participants=["John", "Alice", "Bob"])
    
    # Инициализируем установщика целей
    goal_setter = GoalSetter()
    
    # Устанавливаем цели проекта
    goals = ["Complete Phase 1", "Achieve 90% customer satisfaction", "Stay within budget"]
    goal_setter.set_goals(project, goals)
