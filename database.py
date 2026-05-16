import sqlite3

conn = sqlite3.connect("farmers.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feedback_text TEXT,
    sentiment TEXT,
    confidence REAL,
    issues TEXT
)
""")

conn.commit()