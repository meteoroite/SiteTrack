 url=https://github.com/meteoroite/SiteTrack/blob/main/src/storage/database.py
"""
Database layer - SQLite database operations with proper connection management and security
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict
from contextlib import contextmanager
from pathlib import Path

# Import logger and exceptions
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from logger import setup_logger
from src.utils.exceptions import DatabaseError

logger = setup_logger(__name__)

# Whitelist allowed fields to prevent SQL injection
ALLOWED_REPORT_FIELDS = {
    'project_name', 'location', 'report_type', 'status', 
    'notes', 'date'
}
ALLOWED_ISSUE_FIELDS = {
    'title', 'description', 'severity', 'status', 
    'photo_path', 'assigned_to'
}

class Database:
    """SQLite database wrapper with context manager support and security measures"""
    
    def __init__(self, db_path: str = "field_reports.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to database with proper error handling"""
        try:
            self.conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            logger.debug(f"Database connected: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise DatabaseError(f"Failed to connect to database: {e}")
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor with automatic commit/rollback"""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
            logger.debug("Database transaction committed")
        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Database error, transaction rolled back: {e}")
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            cursor.close()
    
    def create_tables(self):
        """Create database tables with proper constraints"""
        try:
            with self.get_cursor() as cursor:
                # Reports table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        report_type TEXT DEFAULT 'Site Inspection',
                        date TEXT DEFAULT CURRENT_DATE,
                        status TEXT DEFAULT 'draft',
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Issues table with foreign key
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS issues (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_id INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        severity TEXT DEFAULT 'Medium',
                        status TEXT DEFAULT 'open',
                        photo_path TEXT,
                        assigned_to TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
                    )
                ''')
                
                # Templates table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        report_type TEXT NOT NULL,
                        description TEXT,
                        checklist_items TEXT DEFAULT '[]',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Projects table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            
            logger.info("Database tables created/verified successfully")
        except DatabaseError as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def add_report(self, report_data: dict) -> int:
        """Add new report to database"""
        try:
            date = report_data.get('date') or datetime.now().strftime("%Y-%m-%d")
            
            with self.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO reports 
                    (project_name, location, report_type, date, status, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    report_data.get('project_name'),
                    report_data.get('location'),
                    report_data.get('report_type', 'Site Inspection'),
                    date,
                    report_data.get('status', 'draft'),
                    report_data.get('notes', ''),
                ))
                
                report_id = cursor.lastrowid
                logger.info(f"Report created: ID={report_id}, Project={report_data.get('project_name')}")
                return report_id
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error adding report: {e}")
            raise DatabaseError(f"Failed to add report: {e}")
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """Get report by ID"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
                row = cursor.fetchone()
                result = dict(row) if row else None
                logger.debug(f"Report retrieved: ID={report_id}, Found={result is not None}")
                return result
        except Exception as e:
            logger.error(f"Error getting report {report_id}: {e}")
            raise DatabaseError(f"Failed to get report: {e}")
    
    def get_all_reports(self) -> List[Dict]:
        """Get all reports ordered by creation date"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM reports ORDER BY created_at DESC')
                reports = [dict(row) for row in cursor.fetchall()]
                logger.debug(f"Retrieved {len(reports)} reports")
                return reports
        except Exception as e:
            logger.error(f"Error getting all reports: {e}")
            raise DatabaseError(f"Failed to get reports: {e}")
    
    def update_report(self, report_id: int, report_data: dict) -> bool:
        """Update report with SQL injection prevention"""
        try:
            # Validate field names to prevent SQL injection
            invalid_fields = set(report_data.keys()) - ALLOWED_REPORT_FIELDS
            if invalid_fields:
                logger.warning(f"Attempted to update invalid fields: {invalid_fields}")
                raise DatabaseError(f"Invalid fields: {invalid_fields}")
            
            updates = []
            params = []
            
            for key, value in report_data.items():
                if key in ALLOWED_REPORT_FIELDS:
                    updates.append(f"{key} = ?")
                    params.append(value)
            
            if not updates:
                return True
            
            params.append(datetime.now().isoformat())
            params.append(report_id)
            
            query = f"UPDATE reports SET {', '.join(updates)}, updated_at = ? WHERE id = ?"
            
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                logger.info(f"Report updated: ID={report_id}")
                return True
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error updating report {report_id}: {e}")
            raise DatabaseError(f"Failed to update report: {e}")
    
    def delete_report(self, report_id: int) -> bool:
        """Delete report and associated issues (cascade)"""
        try:
            with self.get_cursor() as cursor:
                # Issues are automatically deleted due to ON DELETE CASCADE
                cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
                logger.info(f"Report deleted: ID={report_id}")
                return True
        except Exception as e:
            logger.error(f"Error deleting report {report_id}: {e}")
            raise DatabaseError(f"Failed to delete report: {e}")
    
    def add_issue(self, issue_data: dict) -> int:
        """Add new issue to database"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO issues 
                    (report_id, title, description, severity, status, photo_path, assigned_to)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    issue_data.get('report_id'),
                    issue_data.get('title'),
                    issue_data.get('description'),
                    issue_data.get('severity', 'Medium'),
                    issue_data.get('status', 'open'),
                    issue_data.get('photo_path'),
                    issue_data.get('assigned_to'),
                ))
                
                issue_id = cursor.lastrowid
                logger.info(f"Issue created: ID={issue_id}, Report={issue_data.get('report_id')}")
                return issue_id
        except Exception as e:
            logger.error(f"Error adding issue: {e}")
            raise DatabaseError(f"Failed to add issue: {e}")
    
    def get_issues_by_report(self, report_id: int) -> List[Dict]:
        """Get all issues for a specific report"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM issues WHERE report_id = ? ORDER BY created_at DESC',
                    (report_id,)
                )
                issues = [dict(row) for row in cursor.fetchall()]
                logger.debug(f"Retrieved {len(issues)} issues for report {report_id}")
                return issues
        except Exception as e:
            logger.error(f"Error getting issues for report {report_id}: {e}")
            raise DatabaseError(f"Failed to get issues: {e}")
    
    def get_all_issues(self) -> List[Dict]:
        """Get all issues from all reports"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM issues ORDER BY created_at DESC')
                issues = [dict(row) for row in cursor.fetchall()]
                logger.debug(f"Retrieved {len(issues)} total issues")
                return issues
        except Exception as e:
            logger.error(f"Error getting all issues: {e}")
            raise DatabaseError(f"Failed to get issues: {e}")
    
    def add_template(self, template_data: dict) -> int:
        """Add new template to database"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO templates (name, report_type, description, checklist_items)
                    VALUES (?, ?, ?, ?)
                ''', (
                    template_data.get('name'),
                    template_data.get('report_type'),
                    template_data.get('description', ''),
                    json.dumps(template_data.get('checklist_items', [])),
                ))
                
                template_id = cursor.lastrowid
                logger.info(f"Template created: ID={template_id}, Name={template_data.get('name')}")
                return template_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Template name already exists: {template_data.get('name')}")
            raise DatabaseError(f"Template name already exists")
        except Exception as e:
            logger.error(f"Error adding template: {e}")
            raise DatabaseError(f"Failed to add template: {e}")
    
    def get_template(self, template_id: int) -> Optional[Dict]:
        """Get template by ID"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM templates WHERE id = ?', (template_id,))
                row = cursor.fetchone()
                if row:
                    template = dict(row)
                    template['checklist_items'] = json.loads(template.get('checklist_items', '[]'))
                    logger.debug(f"Template retrieved: ID={template_id}")
                    return template
                return None
        except Exception as e:
            logger.error(f"Error getting template {template_id}: {e}")
            raise DatabaseError(f"Failed to get template: {e}")
    
    def get_all_templates(self) -> List[Dict]:
        """Get all templates"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM templates ORDER BY created_at DESC')
                templates = []
                for row in cursor.fetchall():
                    template = dict(row)
                    template['checklist_items'] = json.loads(template.get('checklist_items', '[]'))
                    templates.append(template)
                logger.debug(f"Retrieved {len(templates)} templates")
                return templates
        except Exception as e:
            logger.error(f"Error getting all templates: {e}")
            raise DatabaseError(f"Failed to get templates: {e}")
    
    def add_project(self, name: str) -> Optional[int]:
        """Add project"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('INSERT INTO projects (name) VALUES (?)', (name,))
                project_id = cursor.lastrowid
                logger.info(f"Project created: ID={project_id}, Name={name}")
                return project_id
        except sqlite3.IntegrityError:
            logger.debug(f"Project already exists: {name}")
            return None
        except Exception as e:
            logger.error(f"Error adding project: {e}")
            raise DatabaseError(f"Failed to add project: {e}")
    
    def get_all_projects(self) -> List[Dict]:
        """Get all projects"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('SELECT * FROM projects ORDER BY name')
                projects = [dict(row) for row in cursor.fetchall()]
                logger.debug(f"Retrieved {len(projects)} projects")
                return projects
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            raise DatabaseError(f"Failed to get projects: {e}")
    
    def close(self):
        """Close database connection properly"""
        if self.conn:
            try:
                self.conn.close()
                logger.debug("Database connection closed")
            except Exception as e:
                logger.error(f"Error closing database: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, *args):
        """Context manager exit"""
        self.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()