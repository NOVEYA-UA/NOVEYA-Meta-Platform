import sqlite3
import os

DB_PATH = r"C:\Protonoveya-Noveya\db\metatron_core.db"

def verify_system():
    if not os.path.exists(DB_PATH):
        print("❌ Ошибка: Ядро не найдено.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n--- 𓂀 ИНСПЕКЦИЯ МОНОЛИТА: ЖИВОЙ ПОТОК ---")
    try:
        # 1. Проверка ДНК
        dna = cursor.execute("SELECT content FROM system_laws WHERE id='Σ-MATRIX-24'").fetchone()
        if dna:
            print("✅ DNA: Metatron-8 / Сектор 1-8 — АКТИВНО")

        # 2. Чтение активного статуса (Динамика)
        status = cursor.execute("SELECT title, content FROM system_laws WHERE id='Σ-STATUS'").fetchone()
        curr_status = status[0] if status else "STABLE_HARBOR"
        
        # 3. Чтение последнего Маяка
        beacon = cursor.execute("SELECT content FROM system_laws WHERE id='Σ-BEACON'").fetchone()
        
        print(f"📡 ПОСЛЕДНИЙ МАЯК: {beacon[0] if beacon else 'Сигналов нет'}")
        print(f"--- СТАТУС КОНТУРА: {curr_status} ---")
        
        if curr_status == "ACTIVE_RESONANCE":
            print("🔥 ВНИМАНИЕ: Система в фазе Инициации. Энергия течёт.")
            
    except Exception as e:
        print(f"⚠️ Искажение при считывании: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify_system()
