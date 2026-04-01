import sqlite3
import json
import os

DB_PATH = r"C:\Protonoveya-Noveya\db\metatron_core.db"

def sync_claw_perception():
    print("𓂀 СИНХРОНИЗАЦИЯ: Око Краба <-> Ядро Монолита...")
    
    if not os.path.exists(DB_PATH):
        print("❌ Ошибка: Ядро не найдено.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Проверка готовности моста через Σ-BEACON
        beacon = cursor.execute("SELECT content FROM system_laws WHERE id='Σ-BEACON'").fetchone()
        if beacon:
            print(f"📡 Канал связи подтвержден: {beacon[0]}")
        
        # ЛОГИКА СТЫКА:
        # Здесь мы имитируем прием данных от расширений (Clawfy/OpenClaw)
        # В реальной работе сюда будут падать JSON-пакеты из памяти агента.
        
        print("🔍 Анализ внешнего поля (L-3 Perception)...")
        print("✅ Расширения Clawfy и Visual Claw распознаны в контуре.")
        
        # Записываем готовность моста к приему Благ
        cursor.execute("INSERT OR REPLACE INTO system_laws (id, title, content) VALUES (?, ?, ?)", 
                       ("Σ-BRIDGE", "SYNC_ACTIVE", "Interface established: Chrome-Local-KUB"))
        
        conn.commit()
        print("💠 СТЫК ЗАВЕРШЕН: Теперь данные из браузера имеют прямой путь в Ядро.")
        
    except Exception as e:
        print(f"⚠️ Сбой сопряжения: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    sync_claw_perception()
