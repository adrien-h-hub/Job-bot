"""
Job Database - Store and manage found jobs
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


class JobDatabase:
    def __init__(self, db_path: str = "jobs_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE,
                title TEXT,
                company TEXT,
                location TEXT,
                salary TEXT,
                description TEXT,
                url TEXT,
                source TEXT,
                posted_date TEXT,
                found_date TEXT,
                status TEXT DEFAULT 'new',
                match_score REAL,
                applied_date TEXT,
                notes TEXT
            )
        ''')
        
        # Applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT,
                applied_date TEXT,
                status TEXT,
                response_date TEXT,
                response TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            )
        ''')
        
        # Queued applications for smart timing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queued_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT,
                scheduled_time TEXT,
                status TEXT DEFAULT 'pending',
                created_date TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(job_id)
            )
        ''')
        
        # Search history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_date TEXT,
                keywords TEXT,
                location TEXT,
                source TEXT,
                jobs_found INTEGER,
                jobs_applied INTEGER,
                duration INTEGER
            )
        ''')
        
        # Contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                name TEXT,
                email TEXT UNIQUE,
                position TEXT,
                source TEXT,
                confidence REAL,
                found_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_job(self, job_data: dict) -> bool:
        """Add a new job to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO jobs 
                (job_id, title, company, location, salary, description, url, source, posted_date, found_date, match_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data.get('job_id'),
                job_data.get('title'),
                job_data.get('company'),
                job_data.get('location'),
                job_data.get('salary'),
                job_data.get('description'),
                job_data.get('url'),
                job_data.get('source'),
                job_data.get('posted_date'),
                datetime.now().isoformat(),
                job_data.get('match_score', 0)
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error adding job: {e}")
            return False
        finally:
            conn.close()
    
    def get_new_jobs(self) -> list:
        """Get all jobs with 'new' status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE status = "new" ORDER BY match_score DESC')
        columns = [description[0] for description in cursor.description]
        jobs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return jobs
    
    def update_job_status(self, job_id: str, status: str):
        """Update job status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE jobs SET status = ? WHERE job_id = ?', (status, job_id))
        conn.commit()
        conn.close()
    
    def mark_as_applied(self, job_id: str):
        """Mark a job as applied"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE jobs SET status = 'applied', applied_date = ? WHERE job_id = ?
        ''', (datetime.now().isoformat(), job_id))
        
        cursor.execute('''
            INSERT INTO applications (job_id, applied_date, status)
            VALUES (?, ?, 'pending')
        ''', (job_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> dict:
        """Get application statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute('SELECT COUNT(*) FROM jobs')
        stats['total_jobs'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = "new"')
        stats['new_jobs'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = "applied"')
        stats['applied'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = "rejected"')
        stats['rejected'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = "interview"')
        stats['interviews'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def get_jobs_by_source(self, source: str) -> list:
        """Get jobs from a specific source"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE source = ?', (source,))
        columns = [description[0] for description in cursor.description]
        jobs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return jobs
    
    def add_contact(self, contact_data: dict) -> bool:
        """Add a new contact to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO contacts 
                (company_name, name, email, position, source, confidence, found_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                contact_data.get('company_name'),
                contact_data.get('name'),
                contact_data.get('email'),
                contact_data.get('position'),
                contact_data.get('source'),
                contact_data.get('confidence', 0.5),
                contact_data.get('found_date', datetime.now().isoformat())
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error adding contact: {e}")
            return False
        finally:
            conn.close()
    
    def get_contacts_by_company(self, company_name: str) -> list:
        """Get all contacts for a specific company"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM contacts 
            WHERE company_name LIKE ?
            ORDER BY confidence DESC
        ''', (f'%{company_name}%',))
        
        contacts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return contacts
    
    def add_search_history(self, search_data: dict) -> bool:
        """Add a search history entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO search_history 
                (search_date, keywords, location, source, jobs_found, jobs_applied, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                search_data.get('keywords'),
                search_data.get('location'),
                search_data.get('source'),
                search_data.get('jobs_found', 0),
                search_data.get('jobs_applied', 0),
                search_data.get('duration', 0)
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding search history: {e}")
            return False
        finally:
            conn.close()
    
    def get_recent_applications(self, days: int = 30) -> list:
        """Get jobs applied to in the last N days"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE status = 'applied' 
            AND applied_date >= date('now', '-' || ? || ' days')
            ORDER BY applied_date DESC
        ''', (days,))
        
        jobs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jobs
    
    def add_queued_application(self, job_id: str, scheduled_time: str):
        """Add application to queue for smart timing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(''' 
            INSERT INTO queued_applications (job_id, scheduled_time, created_date)
            VALUES (?, ?, ?)
        ''', (job_id, scheduled_time, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_pending_applications(self, current_time: str = None) -> list:
        """Get applications ready to be submitted"""
        if current_time is None:
            current_time = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(''' 
            SELECT qa.*, j.* 
            FROM queued_applications qa
            JOIN jobs j ON qa.job_id = j.job_id
            WHERE qa.status = 'pending' 
            AND qa.scheduled_time <= ?
            ORDER BY qa.scheduled_time
        ''', (current_time,))
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def mark_queue_completed(self, queue_id: int):
        """Mark queued application as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(''' 
            UPDATE queued_applications 
            SET status = 'completed'
            WHERE id = ?
        ''', (queue_id,))
        
        conn.commit()
        conn.close()
    
    def export_to_csv(self, filepath: str = 'jobs_export.csv'):
        """Export jobs to CSV file"""
        import csv
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs')
        jobs = cursor.fetchall()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Job ID', 'Title', 'Company', 'Location', 'Salary', 
                           'Description', 'URL', 'Source', 'Posted Date', 'Found Date', 
                           'Status', 'Match Score', 'Applied Date', 'Notes'])
            writer.writerows(jobs)
        
        conn.close()
        print(f"Exported {len(jobs)} jobs to {filepath}")
