"""
Report model - data structure for field reports
"""

from datetime import datetime
from typing import List, Optional

class Report:
    """Represents a field report"""
    
    def __init__(
        self,
        project_name: str,
        location: str,
        report_type: str = "Site Inspection",
        date: Optional[str] = None,
        id: Optional[int] = None,
        status: str = "draft",
        issues: Optional[List] = None,
        photos: Optional[List] = None,
        notes: str = "",
    ):
        self.id = id
        self.project_name = project_name
        self.location = location
        self.report_type = report_type
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.status = status  # draft, completed, archived
        self.issues = issues or []
        self.photos = photos or []
        self.notes = notes
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'project_name': self.project_name,
            'location': self.location,
            'report_type': self.report_type,
            'date': self.date,
            'status': self.status,
            'issues': self.issues,
            'photos': self.photos,
            'notes': self.notes,
            'created_at': self.created_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Report':
        """Create from dictionary"""
        return Report(
            id=data.get('id'),
            project_name=data.get('project_name', ''),
            location=data.get('location', ''),
            report_type=data.get('report_type', 'Site Inspection'),
            date=data.get('date'),
            status=data.get('status', 'draft'),
            issues=data.get('issues', []),
            photos=data.get('photos', []),
            notes=data.get('notes', ''),
        )
    
    def add_issue(self, issue):
        """Add an issue to the report"""
        self.issues.append(issue)
    
    def add_photo(self, photo_path: str):
        """Add a photo to the report"""
        self.photos.append(photo_path)
    
    def mark_complete(self):
        """Mark report as complete"""
        self.status = "completed"
    
    def mark_draft(self):
        """Mark report as draft"""
        self.status = "draft"
    
    def __repr__(self):
        return f"Report({self.project_name}, {self.location}, {self.status})"
