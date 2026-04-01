import os, json

SCAN_PATH = r'C:\СОЦИАЛЬНЫЙ ПРОЕКТ НОВЕЯ'
DB_PATH = r'C:\Protonoveya-Noveya\Core_Claw\Data\local_ro2_base.json'

def run_claw():
    print(f"🚀 КЛЕШНЯ [RO2]: Наблюдение за архивом {SCAN_PATH}")
    if os.path.exists(SCAN_PATH):
        # Рекурсивный подсчет объектов для проверки связи
        files_count = sum([len(files) for r, d, files in os.walk(SCAN_PATH)])
        print(f"✅ Резонанс установлен. Обнаружено объектов: {files_count}")
    else:
        print(f"❌ ОШИБКА: Архив не найден по пути {SCAN_PATH}")

if __name__ == "__main__":
    run_claw()
