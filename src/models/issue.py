"""
Issue model - data structure for site issues/defects
"""

from datetime import datetime
from typing import Optional

class Issue:
    """Represents a site issue or defect"""
    
    def __init__(
        self,
        title: str,
        description: str,
        severity: str = "Medium",
        report_id: Optional[int] = None,
        id: Optional[int] = None,
        status: str = "open",
        photo_path: Optional[str] = None,
        assigned_to: Optional[str] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.severity = severity  # Low, Medium, High, Critical
        self.report_id = report_id
        self.status = status  # open, in_progress, resolved, closed
        self.photo_path = photo_path
        self.assigned_to = assigned_to
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'report_id': self.report_id,
            'status': self.status,
            'photo_path': self.photo_path,
            'assigned_to': self.assigned_to,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Issue':
        """Create from dictionary"""
        return Issue(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            severity=data.get('severity', 'Medium'),
            report_id=data.get('report_id'),
            status=data.get('status', 'open'),
            photo_path=data.get('photo_path'),
            assigned_to=data.get('assigned_to'),
        )
    
    def mark_resolved(self):
        """Mark issue as resolved"""
        self.status = "resolved"
        self.updated_at = datetime.now().isoformat()
    
    def mark_in_progress(self):
        """Mark issue as in progress"""
        self.status = "in_progress"
        self.updated_at = datetime.now().isoformat()
    
    def is_critical(self) -> bool:
        """Check if issue is critical"""
        return self.severity in ["High", "Critical"]
    
    def __repr__(self):
        return f"Issue({self.title}, {self.severity}, {self.status})"
