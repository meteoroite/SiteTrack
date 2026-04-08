<<<<<<< HEAD
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
=======
 url=https://github.com/meteoroite/SiteTrack/blob/main/config.py
"""
Central configuration file for SiteTrack application
"""
import os
from pathlib import Path

# Application
APP_NAME = "SiteTrack"
APP_VERSION = "2.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
PHOTOS_DIR = REPORTS_DIR / "photos"
BACKUPS_DIR = REPORTS_DIR / "backups"
EXPORTS_DIR = REPORTS_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

# Database
DB_PATH = DATA_DIR / "field_reports.db"
DB_TIMEOUT = 30
DB_CHECK_SAME_THREAD = False

# Logging
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "sitetrack.log"
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# Validation
MIN_PROJECT_NAME_LENGTH = 2
MAX_PROJECT_NAME_LENGTH = 255
MIN_LOCATION_LENGTH = 2
MAX_LOCATION_LENGTH = 255
MIN_ISSUE_TITLE_LENGTH = 3
MAX_ISSUE_TITLE_LENGTH = 200
MAX_PHOTO_SIZE_MB = 50  # Per photo
MAX_PHOTOS_PER_REPORT = 50

# Photo Processing
PHOTO_MAX_WIDTH = 1200
PHOTO_QUALITY = 85
ALLOWED_PHOTO_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

# Report Types
REPORT_TYPES = [
    "Site Inspection",
    "Safety Audit",
    "Quality Control",
    "Maintenance Report",
    "Final Inspection",
    "Progress Report",
    "Incident Report",
]

# Issue Severity
ISSUE_SEVERITIES = ["Low", "Medium", "High", "Critical"]

# Issue Status
ISSUE_STATUS = ["open", "in_progress", "resolved", "closed"]

# Report Status
REPORT_STATUS = ["draft", "completed", "archived"]

# Checklist Items (Default)
DEFAULT_CHECKLIST_ITEMS = [
    "Safety Equipment Available",
    "Site Access Clear",
    "Proper Signage Posted",
    "Emergency Exits Accessible",
    "Equipment Properly Maintained",
    "Documentation Complete",
    "Environmental Hazards Assessed",
    "Quality Standards Met",
]

def ensure_directories():
    """Create required directories if they don't exist"""
    for directory in [DATA_DIR, REPORTS_DIR, PHOTOS_DIR, BACKUPS_DIR, EXPORTS_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    print(f"✓ SiteTrack {APP_VERSION} configuration initialized")
>>>>>>> 7b47a52 (Fix Flet API issues, implement step navigation, add error handling)
