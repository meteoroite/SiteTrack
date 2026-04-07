"""
Template model - data structure for report templates
"""

from datetime import datetime
from typing import List, Optional

class Template:
    """Represents a report template"""
    
    def __init__(
        self,
        name: str,
        report_type: str,
        checklist_items: Optional[List[str]] = None,
        id: Optional[int] = None,
        description: str = "",
    ):
        self.id = id
        self.name = name
        self.report_type = report_type
        self.description = description
        self.checklist_items = checklist_items or []
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'report_type': self.report_type,
            'description': self.description,
            'checklist_items': self.checklist_items,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Template':
        """Create from dictionary"""
        return Template(
            id=data.get('id'),
            name=data.get('name', ''),
            report_type=data.get('report_type', ''),
            description=data.get('description', ''),
            checklist_items=data.get('checklist_items', []),
        )
    
    def add_checklist_item(self, item: str):
        """Add checklist item"""
        if item not in self.checklist_items:
            self.checklist_items.append(item)
    
    def remove_checklist_item(self, item: str):
        """Remove checklist item"""
        if item in self.checklist_items:
            self.checklist_items.remove(item)
    
    def __repr__(self):
        return f"Template({self.name}, {self.report_type})"
