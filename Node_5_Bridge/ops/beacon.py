import sqlite3
import datetime
import os

DB_PATH = r"C:\Protonoveya-Noveya\db\metatron_core.db"

def launch_beacon():
    if not os.path.exists(DB_PATH):
        print("❌ Ошибка: Ядро не обнаружено. Маяк невозможен.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    beacon_msg = f"BEACON_SIGNAL_SENT at {now} | Frequency: 7.83Hz"
    
    try:
        # Фиксация маяка в ядре
        cursor.execute("INSERT OR REPLACE INTO system_laws (id, title, content) VALUES (?, ?, ?)", 
                       ("Σ-BEACON", "ACTIVE_EMISSION", beacon_msg))
        conn.commit()
        print(f"📡 МАЯК ЗАПУЩЕН: {beacon_msg}")
        print("💠 Система вещает в режиме STABLE_RESONANCE.")
    except Exception as e:
        print(f"⚠️ Искажение сигнала: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    launch_beacon()
