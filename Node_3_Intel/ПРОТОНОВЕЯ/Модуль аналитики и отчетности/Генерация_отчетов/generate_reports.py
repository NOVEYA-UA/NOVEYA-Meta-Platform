class ReportGenerator:
    def __init__(self, project):
        self.project = project

    def generate_project_report(self):
        """
        Метод для генерации отчета о проекте.
        """
        # Логика генерации отчета о проекте
        print("Генерация отчета о проекте...")

    def generate_external_report(self):
        """
        Метод для генерации внешнего отчета.
        """
        # Логика генерации внешнего отчета
        print("Генерация внешнего отчета...")

# Пример использования
if __name__ == "__main__":
    from Протоновея.Модуль_управления_проектами.Создание_проекта.create_project import Project

    # Создаем проект
    project = Project(name="Sample Project", description="This is a sample project", start_date="2024-03-15", end_date="2024-05-30", budget=10000, participants=["John", "Alice", "Bob"])

    # Инициализируем генератор отчетов
    report_generator = ReportGenerator(project)

    # Генерируем отчет о проекте
    report_generator.generate_project_report()

    # Генерируем внешний отчет
    report_generator.generate_external_report()
