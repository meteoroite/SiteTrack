"""
Report service - business logic for report operations
"""

import os
import json
from datetime import datetime
from typing import List, Optional, Dict
from src.models.report import Report

class ReportService:
    """Service for report operations"""
    
    def __init__(self, database, file_storage):
        self.db = database
        self.file_storage = file_storage
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def create_report(self, report_data: dict) -> int:
        """Create new report and save to database"""
        try:
            report = Report(
                project_name=report_data.get('project_name'),
                location=report_data.get('location'),
                report_type=report_data.get('report_type', 'Site Inspection'),
            )
            return self.db.add_report(report.to_dict())
        except Exception as e:
            print(f"Error creating report: {e}")
            return None
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """Get report by ID"""
        try:
            return self.db.get_report(report_id)
        except Exception as e:
            print(f"Error getting report: {e}")
            return None
    
    def get_all_reports(self) -> List[Dict]:
        """Get all reports"""
        try:
            return self.db.get_all_reports()
        except Exception as e:
            print(f"Error getting all reports: {e}")
            return []
    
    def update_report(self, report_id: int, report_data: dict) -> bool:
        """Update report"""
        try:
            return self.db.update_report(report_id, report_data)
        except Exception as e:
            print(f"Error updating report: {e}")
            return False
    
    def delete_report(self, report_id: int) -> bool:
        """Delete report"""
        try:
            return self.db.delete_report(report_id)
        except Exception as e:
            print(f"Error deleting report: {e}")
            return False
    
    def save_draft(self, report_data: dict) -> str:
        """Save report as draft JSON"""
        try:
            if not report_data.get('id'):
                report_data['id'] = self.create_report(report_data)
            
            draft_path = os.path.join(self.reports_dir, f"draft_{report_data['id']}.json")
            with open(draft_path, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            return draft_path
        except Exception as e:
            print(f"Error saving draft: {e}")
            return None
    
    def load_draft(self, report_id: int) -> Optional[Dict]:
        """Load draft report"""
        try:
            draft_path = os.path.join(self.reports_dir, f"draft_{report_id}.json")
            if os.path.exists(draft_path):
                with open(draft_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading draft: {e}")
        return None
    
    def get_drafts(self) -> List[Dict]:
        """Get all draft reports"""
        drafts = []
        try:
            for filename in os.listdir(self.reports_dir):
                if filename.startswith('draft_') and filename.endswith('.json'):
                    path = os.path.join(self.reports_dir, filename)
                    with open(path, 'r') as f:
                        drafts.append(json.load(f))
        except Exception as e:
            print(f"Error getting drafts: {e}")
        return drafts
    
    def complete_report(self, report_id: int, report_data: dict) -> str:
        """Complete report and generate PDF"""
        try:
            report_data['status'] = 'completed'
            self.update_report(report_id, report_data)
            
            # Generate PDF
            pdf_path = self.file_storage.pdf_service.generate_pdf(report_data)
            
            # Delete draft
            draft_path = os.path.join(self.reports_dir, f"draft_{report_id}.json")
            if os.path.exists(draft_path):
                os.remove(draft_path)
            
            return pdf_path
        except Exception as e:
            print(f"Error completing report: {e}")
            return None
    
    def search_reports(self, query: str) -> List[Dict]:
        """Search reports by project name or location"""
        try:
            all_reports = self.get_all_reports()
            query_lower = query.lower()
            return [
                r for r in all_reports
                if query_lower in r.get('project_name', '').lower() or
                   query_lower in r.get('location', '').lower()
            ]
        except Exception as e:
            print(f"Error searching reports: {e}")
            return []
    
    def get_reports_by_date(self, start_date: str, end_date: str) -> List[Dict]:
        """Get reports within date range"""
        all_reports = self.get_all_reports()
        return [
            r for r in all_reports
            if start_date <= r.get('date', '') <= end_date
        ]
    
    def archive_report(self, report_id: int) -> bool:
        """Archive report"""
        report = self.get_report(report_id)
        if report:
            report['status'] = 'archived'
            return self.update_report(report_id, report)
        return False
