import logging
import os
import sqlite3

from config import DB_PATH, DATA_DIR

logger = logging.getLogger(__name__)

os.makedirs(DATA_DIR, exist_ok=True)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total INTEGER NOT NULL DEFAULT 0,
                    current INTEGER NOT NULL DEFAULT 0,
                    entered INTEGER NOT NULL DEFAULT 0,
                    exited INTEGER NOT NULL DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
    except sqlite3.Error as exc:
        logger.exception("Database initialization failed: %s", exc)


def insert_stats(total, current, entered=0, exited=0) -> None:
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO stats (total, current, entered, exited) VALUES (?, ?, ?, ?)",
                (total, current, entered, exited),
            )
            conn.commit()
    except sqlite3.Error as exc:
        logger.exception("Failed to write stats: %s", exc)


def get_recent_stats(limit: int = 20):
    try:
        with get_db_connection() as conn:
            rows = conn.execute(
                """
                SELECT strftime('%H:%M', timestamp) AS label, AVG(current) AS value
                FROM stats
                GROUP BY label
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        labels = [row["label"] for row in rows]
        values = [int(row["value"] or 0) for row in rows]
        return {"labels": labels[::-1], "values": values[::-1]}
    except sqlite3.Error as exc:
        logger.exception("Failed to read analytics: %s", exc)
        return {"labels": [], "values": []}
