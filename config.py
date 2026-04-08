import os
import logging
from pathlib import Path

# Centralized Configuration Management
class Config:
    # Database Paths
    DATABASE_PATH = Path(os.getenv('DATABASE_PATH', '/default/path/to/database.db'))

    # Logging Setup
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOGGING_FILE = Path(os.getenv('LOGGING_FILE', 'site_track.log'))

    logging.basicConfig(level=LOGGING_LEVEL,
                        format=LOGGING_FORMAT,
                        handlers=[logging.FileHandler(LOGGING_FILE), logging.StreamHandler()])

    # Validation Constants
    MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2 MB
    SUPPORTED_FILE_TYPES = {'json', 'csv'}

# Load Configuration
config = Config()