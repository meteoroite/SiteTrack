 url=https://github.com/meteoroite/SiteTrack/blob/main/src/services/template_service.py
"""
Template service - business logic for report templates
"""
from typing import List, Optional, Dict
from logger import setup_logger
from src.models.template import Template
from src.utils.exceptions import DatabaseError, ValidationError
from src.utils.validators import validate_template_data, raise_if_invalid

logger = setup_logger(__name__)

class TemplateService:
    """Service for template operations"""
    
    def __init__(self, database):
        """Initialize template service"""
        self.db = database
        logger.info("TemplateService initialized")
    
    def create_template(self, template_data: dict) -> int:
        """
        Create new template
        
        Args:
            template_data: Template data
        
        Returns:
            Template ID
        
        Raises:
            ValidationError: If data is invalid
            DatabaseError: If database operation fails
        """
        try:
            # Validate data
            is_valid, errors = validate_template_data(template_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Create template model
            template = Template(
                name=template_data.get('name'),
                report_type=template_data.get('report_type'),
                description=template_data.get('description', ''),
                checklist_items=template_data.get('checklist_items', []),
            )
            
            # Save to database
            template_id = self.db.add_template(template.to_dict())
            logger.info(f"Template created: ID={template_id}, Name={template.name}")
            return template_id
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error creating template: {e}")
            raise DatabaseError(f"Failed to create template: {e}")
    
    def get_template(self, template_id: int) -> Optional[Dict]:
        """Get template by ID"""
        try:
            template = self.db.get_template(template_id)
            if not template:
                logger.warning(f"Template not found: {template_id}")
            return template
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error getting template {template_id}: {e}")
            raise DatabaseError(f"Failed to get template: {e}")
    
    def get_all_templates(self) -> List[Dict]:
        """Get all templates"""
        try:
            templates = self.db.get_all_templates()
            logger.debug(f"Retrieved {len(templates)} templates")
            return templates
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error getting all templates: {e}")
            raise DatabaseError(f"Failed to get templates: {e}")
    
    def get_templates_by_type(self, report_type: str) -> List[Dict]:
        """Get templates by report type"""
        try:
            all_templates = self.get_all_templates()
            filtered = [t for t in all_templates if t.get('report_type') == report_type]
            logger.debug(f"Found {len(filtered)} templates for type: {report_type}")
            return filtered
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error getting templates by type {report_type}: {e}")
            return []
    
    def update_template(self, template_id: int, template_data: dict) -> bool:
        """
        Update template
        
        Args:
            template_id: Template ID
            template_data: Updated template data
        
        Returns:
            True if successful
        """
        try:
            # Validate data
            is_valid, errors = validate_template_data(template_data)
            raise_if_invalid(is_valid, errors, ValidationError)
            
            # Update in database
            result = self.db.update_template(template_id, template_data)
            logger.info(f"Template updated: ID={template_id}")
            return result
        except (ValidationError, DatabaseError):
            raise
        except Exception as e:
            logger.error(f"Error updating template {template_id}: {e}")
            raise DatabaseError(f"Failed to update template: {e}")
    
    def delete_template(self, template_id: int) -> bool:
        """Delete template"""
        try:
            result = self.db.delete_template(template_id)
            logger.info(f"Template deleted: ID={template_id}")
            return result
        except DatabaseError:
            raise
        except Exception as e:
            logger.error(f"Error deleting template {template_id}: {e}")
            raise DatabaseError(f"Failed to delete template: {e}")