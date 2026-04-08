 url=https://github.com/meteoroite/SiteTrack/blob/main/init_app.py
"""
Initialize application - create required directories and database
Run this once before starting the app
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logger
from config import Config
from src.storage.database import Database
from src.storage.file_storage import FileStorage
from src.services.pdf_service import PDFService
from src.utils.exceptions import DatabaseError, FileStorageError

logger = setup_logger(__name__)


def initialize_app():
    """Initialize app directories and database"""
    
    logger.info("=" * 60)
    logger.info("🚀 Initializing SiteTrack Application...")
    logger.info("=" * 60)
    
    try:
        # Create directory structure
        dirs = [
            "data",
            "data/reports",
            "data/reports/photos",
            "data/reports/backups",
            "data/reports/exports",
            "logs",
            "assets",
        ]
        
        for dir_path in dirs:
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                logger.info(f"✓ Created directory: {dir_path}")
            except OSError as e:
                logger.error(f"✗ Failed to create directory {dir_path}: {e}")
                raise FileStorageError(f"Failed to create directory: {e}")
        
        # Initialize database
        try:
            logger.info("Initializing database...")
            db = Database("data/field_reports.db")
            db.close()
            logger.info("✓ Database initialized successfully")
        except DatabaseError as e:
            logger.error(f"✗ Database initialization failed: {e}")
            raise
        
        # Test file storage
        try:
            logger.info("Initializing file storage...")
            storage = FileStorage("data/reports")
            logger.info("✓ File storage initialized successfully")
        except FileStorageError as e:
            logger.error(f"✗ File storage initialization failed: {e}")
            raise
        
        # Test PDF service
        try:
            logger.info("Initializing PDF service...")
            pdf_service = PDFService("data/reports")
            logger.info("✓ PDF service initialized successfully")
        except Exception as e:
            logger.error(f"✗ PDF service initialization failed: {e}")
            raise
        
        logger.info("=" * 60)
        logger.info("✅ Application initialized successfully!")
        logger.info("=" * 60)
        logger.info("\n📝 You can now run the app with: python main.py\n")
        
        return True
        
    except (DatabaseError, FileStorageError) as e:
        logger.error("=" * 60)
        logger.error(f"❌ Initialization failed: {e}")
        logger.error("=" * 60)
        return False
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"❌ Unexpected error during initialization: {e}")
        logger.error("=" * 60)
        return False


if __name__ == "__main__":
    try:
        success = initialize_app()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.critical(f"Fatal initialization error: {e}")
        sys.exit(1)