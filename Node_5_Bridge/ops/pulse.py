import sqlite3
import os

DB_PATH = r"C:\Protonoveya-Noveya\db\metatron_core.db"

def emit_pulse():
    if not os.path.exists(DB_PATH):
        print("❌ Ошибка: Ядро не найдено.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Прошивка статуса ACTIVE_RESONANCE
        cursor.execute("INSERT OR REPLACE INTO system_laws (id, title, content) VALUES (?, ?, ?)", 
                       ("Σ-STATUS", "ACTIVE_RESONANCE", "First Pulse Recorded: 12V | 7.83Hz | Sync"))
        conn.commit()
        print("✅ ИМПУЛЬС ПРИНЯТ ЯДРОМ: СТАТУС ОБНОВЛЕН ДО ACTIVE_RESONANCE")
    except Exception as e:
        print(f"⚠️ Сбой резонанса: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    emit_pulse()
