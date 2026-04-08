 url=https://github.com/meteoroite/SiteTrack/blob/main/src/services/report_service.py
"""
Report service - business logic for report operations
"""
import os
import json
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path
from config import REPORTS_DIR
from logger import setup_logger
from src.models.report import Report
from src.utils.exceptions import DatabaseError, FileStorageError, ValidationError
from src.utils.validators import validate_report_data, validate_issue_data, raise_if_invalid

logger = setup_logger(__name__)

class ReportService:
    """Service for report operations with proper state management"""
    
    def __init__(self, database, file_storage):
        """Initialize report service"""
        self.db = database
        self.file_storage = file_storage
        self.reports_dir = Path(REPORTS_DIR)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        logger.info("ReportService initialized")
    
    def create_report(self, report_data: dict) -> int:
        """
        Create new report and save to database
        
        Args:
            report_data: Report data dictionary
        
        Returns:
            Report ID
        
        Raises:
            ValidationError: If data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate data
            is_valid, errors = validate_report_data(report_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Create report model
            report = Report(
                project_name=report_data.get('project_name'),
                location=report_data.get('location'),
                report_type=report_data.get('report_type', 'Site Inspection'),
                status=report_data.get('status', 'draft'),
                notes=report_data.get('notes', ''),
            )
            
            # Save to database
            report_id = self.db.add_report(report.to_dict())
            logger.info(f"Report created: ID={report_id}")
            return report_id
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error creating report: {e}")
            raise DatabaseError(f"Failed to create report: {e}")
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """Get report by ID"""
        try:
            report = self.db.get_report(report_id)
            if not report:
                logger.warning(f"Report not found: {report_id}")
                return None
            
            # Add issues to report
            issues = self.db.get_issues_by_report(report_id)
            report['issues'] = issues
            
            return report
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error getting report {report_id}: {e}")
            raise DatabaseError(f"Failed to get report: {e}")
    
    def get_all_reports(self) -> List[Dict]:
        """Get all reports"""
        try:
            reports = self.db.get_all_reports()
            
            # Add issues to each report
            for report in reports:
                report['issues'] = self.db.get_issues_by_report(report['id'])
            
            return reports
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error getting all reports: {e}")
            raise DatabaseError(f"Failed to get reports: {e}")
    
    def update_report(self, report_id: int, report_data: dict) -> bool:
        """Update report"""
        try:
            # Validate data
            is_valid, errors = validate_report_data(report_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Update in database
            result = self.db.update_report(report_id, report_data)
            logger.info(f"Report updated: ID={report_id}")
            return result
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating report {report_id}: {e}")
            raise DatabaseError(f"Failed to update report: {e}")
    
    def delete_report(self, report_id: int) -> bool:
        """Delete report"""
        try:
            # Delete photos
            photos = self.file_storage.get_report_photos(report_id)
            for photo_path in photos:
                self.file_storage.delete_photo(photo_path)
            
            # Delete draft file if exists
            draft_path = self.reports_dir / f"draft_{report_id}.json"
            if draft_path.exists():
                draft_path.unlink()
            
            # Delete from database
            result = self.db.delete_report(report_id)
            logger.info(f"Report deleted: ID={report_id}")
            return result
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error deleting report {report_id}: {e}")
            raise DatabaseError(f"Failed to delete report: {e}")
    
    def save_draft(self, report_data: dict) -> str:
        """
        Save report as draft in both JSON and database
        
        Args:
            report_data: Report data
        
        Returns:
            Draft file path
        """
        try:
            # Validate data
            is_valid, errors = validate_report_data(report_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Create/update database record
            if not report_data.get('id'):
                report_data['id'] = self.create_report({
                    'project_name': report_data.get('project_name'),
                    'location': report_data.get('location'),
                    'report_type': report_data.get('report_type', 'Site Inspection'),
                    'status': 'draft',
                    'notes': report_data.get('notes', ''),
                })
            else:
                # Update existing report
                self.db.update_report(report_data['id'], {
                    'status': 'draft',
                    'notes': report_data.get('notes', ''),
                })
            
            # Ensure timestamps
            report_data['updated_at'] = datetime.now().isoformat()
            if 'created_at' not in report_data:
                report_data['created_at'] = datetime.now().isoformat()
            
            # Save JSON file
            draft_path = self.reports_dir / f"draft_{report_data['id']}.json"
            with open(draft_path, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            logger.info(f"Draft saved: ID={report_data['id']}")
            return str(draft_path)
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error saving draft: {e}")
            raise FileStorageError(f"Failed to save draft: {e}")
    
    def load_draft(self, report_id: int) -> Optional[Dict]:
        """Load draft report"""
        try:
            draft_path = self.reports_dir / f"draft_{report_id}.json"
            if draft_path.exists():
                with open(draft_path, 'r') as f:
                    return json.load(f)
            logger.warning(f"Draft not found: {report_id}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in draft {report_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading draft {report_id}: {e}")
            return None
    
    def get_drafts(self) -> List[Dict]:
        """Get all draft reports"""
        drafts = []
        try:
            for draft_file in self.reports_dir.glob('draft_*.json'):
                try:
                    with open(draft_file, 'r') as f:
                        draft = json.load(f)
                        # Ensure timestamps exist
                        if 'updated_at' not in draft:
                            draft['updated_at'] = draft.get('date', datetime.now().isoformat())
                        drafts.append(draft)
                except json.JSONDecodeError as e:
                    logger.warning(f"Skipping invalid draft file {draft_file}: {e}")
                    continue
            
            logger.debug(f"Found {len(drafts)} drafts")
            return sorted(drafts, key=lambda x: x.get('updated_at', ''), reverse=True)
        except Exception as e:
            logger.error(f"Error getting drafts: {e}")
            return []
    
    def complete_report(self, report_id: int, report_data: dict) -> str:
        """
        Complete report and generate PDF
        
        Args:
            report_id: Report ID
            report_data: Report data
        
        Returns:
            Path to generated PDF
        """
        try:
            # Validate data
            is_valid, errors = validate_report_data(report_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Update status to completed
            report_data['status'] = 'completed'
            self.db.update_report(report_id, {'status': 'completed'})
            
            # Generate PDF
            pdf_path = self.file_storage.pdf_service.generate_report_pdf(report_data)
            
            # Delete draft JSON
            draft_path = self.reports_dir / f"draft_{report_id}.json"
            if draft_path.exists():
                draft_path.unlink()
                logger.debug(f"Draft file deleted: {draft_path}")
            
            logger.info(f"Report completed: ID={report_id}, PDF={pdf_path}")
            return pdf_path
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error completing report {report_id}: {e}")
            raise DatabaseError(f"Failed to complete report: {e}")
    
    def add_issue(self, report_id: int, issue_data: dict) -> int:
        """
        Add issue to report
        
        Args:
            report_id: Report ID
            issue_data: Issue data
        
        Returns:
            Issue ID
        """
        try:
            # Add report_id to issue data
            issue_data['report_id'] = report_id
            
            # Validate issue data
            is_valid, errors = validate_issue_data(issue_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Add to database
            issue_id = self.db.add_issue(issue_data)
            logger.info(f"Issue added: ID={issue_id}, Report={report_id}")
            return issue_id
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error adding issue to report {report_id}: {e}")
            raise DatabaseError(f"Failed to add issue: {e}")
    
    def search_reports(self, query: str) -> List[Dict]:
        """Search reports by project name or location"""
        try:
            all_reports = self.get_all_reports()
            query_lower = query.lower()
            results = [
                r for r in all_reports
                if query_lower in r.get('project_name', '').lower() or
                   query_lower in r.get('location', '').lower()
            ]
            logger.info(f"Search query '{query}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching reports: {e}")
            return []
    
    def get_reports_by_status(self, status: str) -> List[Dict]:
        """Get reports by status"""
        try:
            all_reports = self.get_all_reports()
            return [r for r in all_reports if r.get('status') == status]
        except Exception as e:
            logger.error(f"Error getting reports by status {status}: {e}")
            return []