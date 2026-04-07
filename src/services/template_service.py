"""
Template service - business logic for report templates
"""

from typing import List, Optional, Dict
from src.models.template import Template

class TemplateService:
    """Service for template operations"""
    
    def __init__(self, database):
        self.db = database
    
    def create_template(self, template_data: dict) -> int:
        """Create new template"""
        template = Template(
            name=template_data.get('name'),
            report_type=template_data.get('report_type'),
            description=template_data.get('description', ''),
            checklist_items=template_data.get('checklist_items', []),
        )
        return self.db.add_template(template.to_dict())
    
    def get_template(self, template_id: int) -> Optional[Dict]:
        """Get template by ID"""
        return self.db.get_template(template_id)
    
    def get_all_templates(self) -> List[Dict]:
        """Get all templates"""
        return self.db.get_all_templates()
    
    def get_templates_by_type(self, report_type: str) -> List[Dict]:
        """Get templates by report type"""
        all_templates = self.get_all_templates()
        return [t for t in all_templates if t.get('report_type') == report_type]
    
    def update_template(self, template_id: int, template_data: dict) -> bool:
        """Update template"""
        return self.db.update_template(template_id, template_data)
    
    def delete_template(self, template_id: int) -> bool:
        """Delete template"""
        return self.db.delete_template(template_id)
    
    def add_checklist_item(self, template_id: int, item: str) -> bool:
        """Add checklist item to template"""
        template = self.get_template(template_id)
        if template:
            items = template.get('checklist_items', [])
            if item not in items:
                items.append(item)
                return self.update_template(template_id, {'checklist_items': items})
        return False
    
    def remove_checklist_item(self, template_id: int, item: str) -> bool:
        """Remove checklist item from template"""
        template = self.get_template(template_id)
        if template:
            items = template.get('checklist_items', [])
            if item in items:
                items.remove(item)
                return self.update_template(template_id, {'checklist_items': items})
        return False
    
    def duplicate_template(self, template_id: int, new_name: str) -> Optional[int]:
        """Duplicate a template"""
        template = self.get_template(template_id)
        if template:
            new_template = template.copy()
            new_template['name'] = new_name
            new_template.pop('id', None)
            return self.create_template(new_template)
        return None
