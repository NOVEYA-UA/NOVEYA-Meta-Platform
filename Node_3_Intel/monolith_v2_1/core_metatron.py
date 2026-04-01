import sqlite3

DB_SQL = 'monolith.db'

def init_db():
    conn = sqlite3.connect(DB_SQL)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS meridian_sync (id TEXT PRIMARY KEY, node TEXT, state TEXT, resonance REAL, coherence REAL, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)')
    cursor.execute('CREATE TABLE IF NOT EXISTS zn_matrix (id TEXT PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, state TEXT, resonance REAL, coherence REAL, eff REAL, entropy REAL, decision TEXT)')
    conn.commit()
    conn.close()
