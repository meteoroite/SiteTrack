"""
Database layer - SQLite database operations
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict

class Database:
    """SQLite database wrapper"""
    
    def __init__(self, db_path: str = "field_reports.db"):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
    
    def create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
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
        
        # Issues table
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
                FOREIGN KEY (report_id) REFERENCES reports(id)
            )
        ''')
        
        # Templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
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
        
        self.conn.commit()
    
    def add_report(self, report_data: dict) -> int:
        """Add new report"""
        try:
            cursor = self.conn.cursor()
            date = report_data.get('date') or datetime.now().strftime("%Y-%m-%d")
            cursor.execute('''
                INSERT INTO reports (project_name, location, report_type, date, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                report_data.get('project_name'),
                report_data.get('location'),
                report_data.get('report_type', 'Site Inspection'),
                date,
                report_data.get('status', 'draft'),
                report_data.get('notes', ''),
            ))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding report: {e}")
            return None
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """Get report by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reports WHERE id = ?', (report_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_reports(self) -> List[Dict]:
        """Get all reports"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reports ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    def update_report(self, report_id: int, report_data: dict) -> bool:
        """Update report"""
        cursor = self.conn.cursor()
        updates = []
        params = []
        
        for key, value in report_data.items():
            if key != 'id':
                updates.append(f"{key} = ?")
                params.append(value)
        
        params.append(report_id)
        
        if updates:
            query = f"UPDATE reports SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(query, params)
            self.conn.commit()
            return True
        return False
    
    def delete_report(self, report_id: int) -> bool:
        """Delete report"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM issues WHERE report_id = ?', (report_id,))
        cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
        self.conn.commit()
        return True
    
    def add_issue(self, issue_data: dict) -> int:
        """Add new issue"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO issues (report_id, title, description, severity, status, photo_path, assigned_to)
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
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_issues(self) -> List[Dict]:
        """Get all issues"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM issues ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]
    
    def add_template(self, template_data: dict) -> int:
        """Add template"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO templates (name, report_type, description, checklist_items)
            VALUES (?, ?, ?, ?)
        ''', (
            template_data.get('name'),
            template_data.get('report_type'),
            template_data.get('description', ''),
            json.dumps(template_data.get('checklist_items', [])),
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_templates(self) -> List[Dict]:
        """Get all templates"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM templates')
        templates = []
        for row in cursor.fetchall():
            template = dict(row)
            template['checklist_items'] = json.loads(template.get('checklist_items', '[]'))
            templates.append(template)
        return templates
    
    def update_template(self, template_id: int, template_data: dict) -> bool:
        """Update template"""
        cursor = self.conn.cursor()
        checklist = template_data.get('checklist_items')
        if isinstance(checklist, list):
            checklist = json.dumps(checklist)
        
        cursor.execute('''
            UPDATE templates SET name = ?, report_type = ?, description = ?, checklist_items = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            template_data.get('name'),
            template_data.get('report_type'),
            template_data.get('description', ''),
            checklist,
            template_id,
        ))
        self.conn.commit()
        return True
    
    def delete_template(self, template_id: int) -> bool:
        """Delete template"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM templates WHERE id = ?', (template_id,))
        self.conn.commit()
        return True
    
    def get_template(self, template_id: int) -> Optional[Dict]:
        """Get template by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM templates WHERE id = ?', (template_id,))
        row = cursor.fetchone()
        if row:
            template = dict(row)
            template['checklist_items'] = json.loads(template.get('checklist_items', '[]'))
            return template
        return None
    
    def add_project(self, name: str) -> Optional[int]:
        """Add project"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO projects (name) VALUES (?)', (name,))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
