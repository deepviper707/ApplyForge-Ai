import sqlite3
import os
from datetime import datetime

DB_PATH = "../data/applyforge.db"

def init_db():
    os.makedirs("../data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT,
            location TEXT,
            salary TEXT,
            job_url TEXT UNIQUE NOT NULL,
            job_description TEXT,
            source TEXT,
            match_score REAL,
            keywords_matched TEXT,
            applied_date DATE,
            application_status TEXT DEFAULT 'Pending',
            resume_version TEXT,
            cover_letter_version TEXT,
            notes TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_job(**kwargs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    columns = ', '.join(kwargs.keys())
    placeholders = ', '.join('?' * len(kwargs))
    c.execute(f'INSERT INTO jobs ({columns}) VALUES ({placeholders})', tuple(kwargs.values()))
    conn.commit()
    conn.close()

# Add update/get functions as needed
