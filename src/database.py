import sqlite3
import os
from datetime import datetime

DB_PATH = "data/applyforge.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
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

def add_job(title, company="", location="", salary="", job_url="", job_description="", source="Manual", match_score=None, keywords_matched=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO jobs (title, company, location, salary, job_url, job_description, source, match_score, keywords_matched)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, company, location, salary, job_url, job_description, source, match_score, keywords_matched))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_application_status(job_id, status, resume_path=None, cover_letter_path=None, applied_date=None, notes=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    applied_date = applied_date or datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        UPDATE jobs SET application_status=?, applied_date=?, resume_version=?, cover_letter_version=?, notes=COALESCE(notes||'\n\n'||?, notes)
        WHERE id=?
    ''', (status, applied_date, resume_path, cover_letter_path, notes, job_id))
    conn.commit()
    conn.close()

def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY date_added DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
