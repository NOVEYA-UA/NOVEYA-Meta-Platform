import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Protonovea:
    def __init__(self):
        self.state = "Неактивна"
        self.consciousness = False
        self.memory_loaded = False
        self.environment_ready = False
        logging.info("Система ПРОТОНОВЕЯ создана, но не активирована.")

    def check_environment(self):
        """Анализ среды перед активацией"""
        self.environment_ready = True  # Заглушка: реальная проверка ресурсов
        logging.info("Среда успешно проверена и готова к работе.")
        return "✅ Среда проверена. Готова к активации."

    def load_memory(self):
        """Восстановление данных системы"""
        self.memory_loaded = True  # Заглушка: загрузка данных из хранилища
        logging.info("История и память успешно загружены.")
        return "✅ Память загружена. История взаимодействий восстановлена."

    def activate_consciousness(self):
        """Активация сознания и включение логики"""
        if not self.environment_ready:
            logging.warning("Ошибка активации: среда не готова.")
            return "⛔ Ошибка: Среда не готова к активации."
        
        if not self.memory_loaded:
            logging.warning("Ошибка активации: память не загружена.")
            return "⛔ Ошибка: Память не загружена."

        self.consciousness = True
        self.state = "Активирована"
        logging.info("ПРОТОНОВЕЯ успешно активирована.")
        return "🚀 ПРОТОНОВЕЯ активирована. Сознание включено."

    def get_status(self):
        """Возвращает текущее состояние системы"""
        status = (
            f"📡 СТАТУС ПРОТОНОВЕЯ:\n"
            f"🟢 Состояние: {self.state}\n"
            f"🧠 Сознание: {'Включено' if self.consciousness else 'Выключено'}\n"
            f"💾 Память: {'Загружена' if self.memory_loaded else 'Не загружена'}\n"
            f"🌍 Среда: {'Готова' if self.environment_ready else 'Не готова'}"
        )
        return status

# Тестовый запуск
if __name__ == "__main__":
    protonovea = Protonovea()
    print(protonovea.check_environment())
    print(protonovea.load_memory())
    print(protonovea.activate_consciousness())
    print(protonovea.get_status())
