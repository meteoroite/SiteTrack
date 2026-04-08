 url=https://github.com/meteoroite/SiteTrack/blob/main/logger.py
"""
Logging configuration for SiteTrack application
"""
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_LEVEL, LOG_FORMAT, LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT, LOGS_DIR

def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured Logger instance
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # File Handler with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_handler.setFormatter(console_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger