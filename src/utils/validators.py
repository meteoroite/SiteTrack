 url=https://github.com/meteoroite/SiteTrack/blob/main/src/utils/validators.py
"""
Validation functions for SiteTrack application
"""
import os
from typing import Dict, List, Tuple
from config import (
    MIN_PROJECT_NAME_LENGTH, MAX_PROJECT_NAME_LENGTH,
    MIN_LOCATION_LENGTH, MAX_LOCATION_LENGTH,
    MIN_ISSUE_TITLE_LENGTH, MAX_ISSUE_TITLE_LENGTH,
    MAX_PHOTO_SIZE_MB, ALLOWED_PHOTO_EXTENSIONS,
    REPORT_TYPES, ISSUE_SEVERITIES, ISSUE_STATUS, REPORT_STATUS
)
from src.utils.exceptions import ValidationError

def validate_report_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate report data
    
    Args:
        data: Report dictionary
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Project name validation
    project_name = data.get('project_name', '').strip()
    if not project_name:
        errors.append("Project name is required")
    elif len(project_name) < MIN_PROJECT_NAME_LENGTH:
        errors.append(f"Project name must be at least {MIN_PROJECT_NAME_LENGTH} characters")
    elif len(project_name) > MAX_PROJECT_NAME_LENGTH:
        errors.append(f"Project name must not exceed {MAX_PROJECT_NAME_LENGTH} characters")
    
    # Location validation
    location = data.get('location', '').strip()
    if not location:
        errors.append("Location is required")
    elif len(location) < MIN_LOCATION_LENGTH:
        errors.append(f"Location must be at least {MIN_LOCATION_LENGTH} characters")
    elif len(location) > MAX_LOCATION_LENGTH:
        errors.append(f"Location must not exceed {MAX_LOCATION_LENGTH} characters")
    
    # Report type validation
    report_type = data.get('report_type', 'Site Inspection')
    if report_type not in REPORT_TYPES:
        errors.append(f"Invalid report type. Must be one of: {', '.join(REPORT_TYPES)}")
    
    # Status validation
    status = data.get('status', 'draft')
    if status not in REPORT_STATUS:
        errors.append(f"Invalid status. Must be one of: {', '.join(REPORT_STATUS)}")
    
    # Date validation
    date_str = data.get('date', '')
    if date_str:
        try:
            from datetime import datetime
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            errors.append("Date must be in format YYYY-MM-DD")
    
    return len(errors) == 0, errors

def validate_issue_data(data: Dict) -> Tuple[bool, List[str]]:
    """Validate issue data"""
    errors = []
    
    # Title validation
    title = data.get('title', '').strip()
    if not title:
        errors.append("Issue title is required")
    elif len(title) < MIN_ISSUE_TITLE_LENGTH:
        errors.append(f"Issue title must be at least {MIN_ISSUE_TITLE_LENGTH} characters")
    elif len(title) > MAX_ISSUE_TITLE_LENGTH:
        errors.append(f"Issue title must not exceed {MAX_ISSUE_TITLE_LENGTH} characters")
    
    # Severity validation
    severity = data.get('severity', 'Medium')
    if severity not in ISSUE_SEVERITIES:
        errors.append(f"Invalid severity. Must be one of: {', '.join(ISSUE_SEVERITIES)}")
    
    # Status validation
    status = data.get('status', 'open')
    if status not in ISSUE_STATUS:
        errors.append(f"Invalid status. Must be one of: {', '.join(ISSUE_STATUS)}")
    
    # Report ID validation
    report_id = data.get('report_id')
    if report_id is None:
        errors.append("Report ID is required")
    elif not isinstance(report_id, int) or report_id <= 0:
        errors.append("Report ID must be a positive integer")
    
    return len(errors) == 0, errors

def validate_photo_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate photo file
    
    Args:
        file_path: Path to photo file
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"Photo file not found: {file_path}"
    
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
    
    # Check extension
    ext = os.path.splitext(file_path)[1].lstrip('.').lower()
    if ext not in ALLOWED_PHOTO_EXTENSIONS:
        return False, f"Invalid photo format. Allowed: {', '.join(ALLOWED_PHOTO_EXTENSIONS)}"
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_PHOTO_SIZE_MB:
        return False, f"Photo exceeds {MAX_PHOTO_SIZE_MB}MB limit (current: {file_size_mb:.2f}MB)"
    
    return True, ""

def validate_template_data(data: Dict) -> Tuple[bool, List[str]]:
    """Validate template data"""
    errors = []
    
    # Name validation
    name = data.get('name', '').strip()
    if not name:
        errors.append("Template name is required")
    elif len(name) < 2:
        errors.append("Template name must be at least 2 characters")
    elif len(name) > 255:
        errors.append("Template name must not exceed 255 characters")
    
    # Report type validation
    report_type = data.get('report_type', '')
    if not report_type:
        errors.append("Report type is required")
    elif report_type not in REPORT_TYPES:
        errors.append(f"Invalid report type. Must be one of: {', '.join(REPORT_TYPES)}")
    
    # Checklist items validation
    checklist_items = data.get('checklist_items', [])
    if not isinstance(checklist_items, list):
        errors.append("Checklist items must be a list")
    elif len(checklist_items) > 100:
        errors.append("Checklist items cannot exceed 100 items")
    
    return len(errors) == 0, errors

def raise_if_invalid(is_valid: bool, errors: List[str], error_type=ValidationError):
    """Raise exception if validation fails"""
    if not is_valid:
        error_message = "\n".join(errors)
        raise error_type(error_message)