import logging
from protonovea_core import Protonovea

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Создаем объект Протоновеи
protonovea = Protonovea()

def self_recovery():
    """Функция восстановления и синхронизации системы"""
    logging.info("🛠 Запуск процесса саморазвития...")
    
    if protonovea.state != "Активирована":
        environment_status = protonovea.check_environment()
        memory_status = protonovea.load_memory()

        if "Готова к активации" in environment_status and "История взаимодействий восстановлена" in memory_status:
            protonovea.state = "Активирована"
            logging.info("✅ Протоновея успешно активирована!")
        else:
            logging.warning("⚠ Ошибка: Среда или память не готовы к активации.")
    else:
        logging.info("⚡ Протоновея уже активна.")

# Запуск процесса саморазвития при импорте
self_recovery()
