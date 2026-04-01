class DataCollector:
    def __init__(self, project):
        self.project = project

    def collect_project_data(self):
        """
        Метод для сбора данных о проекте (выполнение задач, расходы, ресурсы и т.д.).
        """
        # Логика сбора данных о проекте
        print("Сбор данных о проекте...")

    def collect_external_data(self):
        """
        Метод для сбора внешних данных (экономические показатели, тренды рынка и т.д.).
        """
        # Логика сбора внешних данных
        print("Сбор внешних данных...")

# Пример использования
if __name__ == "__main__":
    from Протоновея.Модуль_управления_проектами.Создание_проекта.create_project import Project

    # Создаем проект
    project = Project(name="Sample Project", description="This is a sample project", start_date="2024-03-15", end_date="2024-05-30", budget=10000, participants=["John", "Alice", "Bob"])

    # Инициализируем сборщик данных
    data_collector = DataCollector(project)

    # Собираем данные о проекте
    data_collector.collect_project_data()

    # Собираем внешние данные
    data_collector.collect_external_data()
