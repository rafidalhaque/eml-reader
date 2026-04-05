import sqlite3
from pathlib import Path
import os

class DatabaseOps():
    def __init__(self):
        project_root = Path(__file__).parent
        db_dir = project_root / "db"
        os.mkdir(db_dir) if not os.path.isdir(db_dir) else None
        self.conn = sqlite3.connect(f"{project_root}/db/recent_files.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def conn_close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS recent_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL UNIQUE,
            opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def save_recent_files(self, filename, file_path):
        self.cursor.execute("""
        INSERT OR REPLACE INTO recent_files (filename, file_path, opened_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (filename, file_path))
        self.conn.commit()

    def get_recent_files(self):
        self.cursor.execute("""SELECT * FROM recent_files ORDER BY opened_at DESC LIMIT 10""")
        return self.cursor.fetchall()