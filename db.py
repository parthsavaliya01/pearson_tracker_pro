import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total INTEGER,
    current INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def insert_stats(total, current):
    cursor.execute(
        "INSERT INTO stats (total, current) VALUES (?, ?)",
        (total, current)
    )
    conn.commit()