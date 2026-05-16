"""
VictorReconForge — Persistent Runtime
"""
import sqlite3
import json
import time
import os
from rich.console import Console

console = Console()

class ReconRuntime:
    def __init__(self, db_path: str = "data/victor_recon_runtime.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS scans (id INTEGER PRIMARY KEY, target TEXT, data TEXT, timestamp REAL)")
        self.conn.commit()

    def save_scan_result(self, target: str, data: dict):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO scans (target, data, timestamp) VALUES (?, ?, ? )", (target, json.dumps(data), time.time()))
        self.conn.commit()

    def get_last_scan(self, target: str):
        cur = self.conn.cursor()
        cur.execute("SELECT data FROM scans WHERE target=? ORDER BY timestamp DESC LIMIT 1", (target,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None

    def close(self):
        self.conn.close()