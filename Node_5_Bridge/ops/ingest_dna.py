import sqlite3
import os

# Пути к системе
DB_PATH = r"C:\Protonoveya-Noveya\db\metatron_core.db"
NOTATION_PATH = r"C:\Protonoveya-Noveya\Справочник моральных преступлений\Нотация.txt"

def ingest_dna():
    if not os.path.exists(NOTATION_PATH):
        print(f"❌ Файл Нотации не найден: {NOTATION_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Создаем таблицу системных законов (Logos-слой)
    cursor.execute('''CREATE TABLE IF NOT EXISTS system_laws 
                      (id TEXT PRIMARY KEY, sector TEXT, level TEXT, title TEXT, content TEXT)''')

    print("⚙️ Резонанс: Анализ файла Нотация.txt...")
    
    with open(NOTATION_PATH, 'r', encoding='utf-8') as f:
        # Инъекция базовой структуры матрицы в ядро
        cursor.execute("INSERT OR REPLACE INTO system_laws (id, title, content) VALUES (?, ?, ?)", 
                       ("Σ-MATRIX-24", "Metatron-8 DNA", f.read()[:500] + "..."))
    
    conn.commit()
    conn.close()
    print("💠 СИНТЕЗ ЗАВЕРШЕН: Матрица 24 секторов прошита в локальное ядро SQLite.")

if __name__ == "__main__":
    ingest_dna()
