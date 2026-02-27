import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "database", "jobs.db")

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        link TEXT,
        min_salary INTEGER,
        max_salary INTEGER
    )
    """)

    conn.commit()
    conn.close()

def insert_all_jobs(all_jobs):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for job in all_jobs:
        cursor.execute("SELECT id FROM jobs WHERE link = ?", (job["link"],))
        exists = cursor.fetchone()
        if exists:
            print(f"Vacancy already exists: {job['title']}")
            continue  # skiping the duplicate
        cursor.execute("""
            INSERT INTO jobs (title, company, location, link, min_salary, max_salary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job["title"],
            job["company"],
            job["location"],
            job["link"],
            job["min_salary"],
            job["max_salary"]
        ))
        print(f"Inserted vacancy: {job['title']}")

    conn.commit()
    conn.close()