import sqlite3
import json
import os
from datetime import datetime

DB_FILE = "scanner.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            results JSON
        )
    """)
    conn.commit()
    conn.close()

def save_scan(target, status, results):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results_json = json.dumps(results) if results else "[]"
    
    cursor.execute("""
        INSERT INTO scans (target, date, status, results)
        VALUES (?, ?, ?, ?)
    """, (target, date_str, status, results_json))
    
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id

def get_scan_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, target, date, status FROM scans ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "target": row[1],
            "date": row[2],
            "status": row[3]
        })
    return history

def get_scan_results(scan_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT results FROM scans WHERE id = ?", (scan_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0]:
        return json.loads(row[0])
    return []

# Initialize immediately when imported
if not os.path.exists(DB_FILE):
    init_db()
