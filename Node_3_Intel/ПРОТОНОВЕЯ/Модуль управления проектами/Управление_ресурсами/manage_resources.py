# Протоновея/Модуль управления проектами/Управление_ресурсами/manage_resources.py

class ResourceManager:
    def __init__(self):
        self.resources = {}

    def add_resource(self, resource_name, quantity):
        # Добавление ресурса
        if resource_name in self.resources:
            self.resources[resource_name] += quantity
        else:
            self.resources[resource_name] = quantity
        print(f"Resource '{resource_name}' added.")

    def remove_resource(self, resource_name, quantity):
        # Удаление ресурса
        if resource_name in self.resources:
            if self.resources[resource_name] >= quantity:
                self.resources[resource_name] -= quantity
                print(f"{quantity} units of resource '{resource_name}' removed.")
            else:
                print(f"Not enough {resource_name} available.")
        else:
            print(f"Resource '{resource_name}' not found.")

# Пример использования
if __name__ == "__main__":
    # Инициализируем менеджер ресурсов
    resource_manager = ResourceManager()

    # Добавляем ресурсы
    resource_manager.add_resource("Labor", 10)
    resource_manager.add_resource("Materials", 100)
    resource_manager.add_resource("Equipment", 5)

    # Удаляем ресурсы
    resource_manager.remove_resource("Materials", 50)
