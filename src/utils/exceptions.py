 url=https://github.com/meteoroite/SiteTrack/blob/main/src/utils/exceptions.py
"""
Custom exceptions for SiteTrack application
"""

class SiteTrackException(Exception):
    """Base exception for SiteTrack"""
    pass

class ValidationError(SiteTrackException):
    """Raised when data validation fails"""
    pass

class DatabaseError(SiteTrackException):
    """Raised when database operation fails"""
    pass

class FileStorageError(SiteTrackException):
    """Raised when file storage operation fails"""
    pass

class PDFGenerationError(SiteTrackException):
    """Raised when PDF generation fails"""
    pass

class PhotoProcessingError(SiteTrackException):
    """Raised when photo processing fails"""
    pass

class ConfigurationError(SiteTrackException):
    """Raised when configuration is invalid"""
    pass

class NotFoundError(SiteTrackException):
    """Raised when resource is not found"""
    pass

class DuplicateError(SiteTrackException):
    """Raised when duplicate resource is found"""
    pass