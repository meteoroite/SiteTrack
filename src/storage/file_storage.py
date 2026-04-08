 url=https://github.com/meteoroite/SiteTrack/blob/main/src/storage/file_storage.py
"""
File storage layer - file management with proper error handling and validation
"""
import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from logger import setup_logger
from src.utils.exceptions import FileStorageError, PhotoProcessingError, ValidationError
from src.utils.validators import validate_photo_file

logger = setup_logger(__name__)

class FileStorage:
    """File storage management with comprehensive error handling"""
    
    def __init__(self, base_dir: str = "reports"):
        """Initialize file storage directories"""
        self.base_dir = Path(base_dir)
        self.photos_dir = self.base_dir / "photos"
        self.backups_dir = self.base_dir / "backups"
        self.exports_dir = self.base_dir / "exports"
        
        self._ensure_directories()
        self.pdf_service = None  # Lazy loading to avoid circular imports
        logger.info("FileStorage initialized")
    
    def _ensure_directories(self):
        """Create required directories"""
        try:
            for directory in [self.photos_dir, self.backups_dir, self.exports_dir]:
                directory.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Directory ensured: {directory}")
        except OSError as e:
            logger.error(f"Failed to create directory: {e}")
            raise FileStorageError(f"Failed to create directory: {e}")
    
    def _get_pdf_service(self):
        """Lazy load PDF service to avoid circular imports"""
        if self.pdf_service is None:
            from src.services.pdf_service import PDFService
            self.pdf_service = PDFService(str(self.base_dir))
        return self.pdf_service
    
    def process_image(self, path: str, max_width: int = 800) -> str:
        """Process and optimize image for storage"""
        try:
            if not os.path.exists(path):
                raise PhotoProcessingError(f"Image file not found: {path}")
            
            img = PILImage.open(path)
            logger.debug(f"Processing image: {path} (size: {img.size})")
            
            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), PILImage.Resampling.LANCZOS)
                logger.debug(f"Image resized to: {(max_width, new_height)}")
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = PILImage.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img)
                img = rgb_img
            
            # Save optimized version
            img.save(path, 'JPEG', quality=85, optimize=True)
            logger.info(f"Image optimized: {path}")
            return path
        except PhotoProcessingError:
            raise
        except Exception as e:
            logger.error(f"Error processing image {path}: {e}")
            raise PhotoProcessingError(f"Failed to process image: {e}")
    
    def save_photo(self, photo_path: str, report_id: int) -> str:
        """Save and optimize photo for report"""
        try:
            # Validate photo file
            is_valid, error_msg = validate_photo_file(photo_path)
            if not is_valid:
                raise ValidationError(error_msg)
            
            # Process image
            self.process_image(photo_path)
            
            # Generate unique filename
            filename = f"report_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            dest_path = self.photos_dir / filename
            
            # Copy file
            shutil.copy2(photo_path, dest_path)
            logger.info(f"Photo saved: {dest_path}")
            return str(dest_path)
        except (ValidationError, PhotoProcessingError):
            raise
        except Exception as e:
            logger.error(f"Error saving photo: {e}")
            raise PhotoProcessingError(f"Failed to save photo: {e}")
    
    def get_report_photos(self, report_id: int) -> list:
        """Get all photos for a report"""
        try:
            photos = []
            pattern = f"report_{report_id}_"
            
            if self.photos_dir.exists():
                for filename in self.photos_dir.iterdir():
                    if filename.is_file() and filename.name.startswith(pattern):
                        photos.append(str(filename))
            
            logger.debug(f"Found {len(photos)} photos for report {report_id}")
            return sorted(photos)
        except Exception as e:
            logger.error(f"Error getting photos for report {report_id}: {e}")
            return []
    
    def delete_photo(self, photo_path: str) -> bool:
        """Delete a photo"""
        try:
            path = Path(photo_path)
            if path.exists():
                path.unlink()
                logger.info(f"Photo deleted: {photo_path}")
                return True
            logger.warning(f"Photo not found: {photo_path}")
            return False
        except Exception as e:
            logger.error(f"Error deleting photo {photo_path}: {e}")
            return False
    
    def backup_database(self, db_path: str = "field_reports.db") -> str:
        """Backup database file"""
        try:
            if not os.path.exists(db_path):
                raise FileStorageError(f"Database not found: {db_path}")
            
            backup_name = f"field_reports_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            dest = self.backups_dir / backup_name
            
            shutil.copy2(db_path, dest)
            logger.info(f"Database backed up: {dest}")
            return str(dest)
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            raise FileStorageError(f"Failed to backup database: {e}")
    
    def restore_database(self, backup_path: str, db_path: str = "field_reports.db") -> bool:
        """Restore database from backup"""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                raise FileStorageError(f"Backup file not found: {backup_path}")
            
            shutil.copy2(backup_file, db_path)
            logger.info(f"Database restored from: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error restoring database: {e}")
            raise FileStorageError(f"Failed to restore database: {e}")
    
    def export_reports(self, reports: list) -> str:
        """Export reports to JSON"""
        try:
            export_file = self.exports_dir / f"reports_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(export_file, 'w') as f:
                json.dump(reports, f, indent=2, default=str)
            
            logger.info(f"Reports exported: {export_file}")
            return str(export_file)
        except Exception as e:
            logger.error(f"Error exporting reports: {e}")
            raise FileStorageError(f"Failed to export reports: {e}")
    
    def import_reports(self, import_file: str) -> List[dict]:
        """Import reports from JSON file"""
        try:
            file_path = Path(import_file)
            if not file_path.exists():
                raise FileStorageError(f"Import file not found: {import_file}")
            
            with open(file_path, 'r') as f:
                reports = json.load(f)
            
            logger.info(f"Reports imported from: {import_file}")
            return reports if isinstance(reports, list) else [reports]
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in import file: {e}")
            raise FileStorageError(f"Invalid JSON format: {e}")
        except Exception as e:
            logger.error(f"Error importing reports: {e}")
            raise FileStorageError(f"Failed to import reports: {e}")
    
    def get_storage_stats(self) -> dict:
        """Get storage statistics"""
        try:
            def get_dir_size(path: Path) -> float:
                total = 0
                if path.exists():
                    for filepath in path.rglob('*'):
                        if filepath.is_file():
                            total += filepath.stat().st_size
                return total / 1024
            
            stats = {
                'total_kb': get_dir_size(self.base_dir),
                'photos_kb': get_dir_size(self.photos_dir),
                'backups_kb': get_dir_size(self.backups_dir),
                'exports_kb': get_dir_size(self.exports_dir),
            }
            
            logger.debug(f"Storage stats: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error calculating storage stats: {e}")
            return {}
    
    def cleanup_old_backups(self, days: int = 30) -> int:
        """Delete backups older than N days"""
        try:
            import time
            current_time = time.time()
            count = 0
            
            if self.backups_dir.exists():
                for filepath in self.backups_dir.iterdir():
                    if filepath.is_file():
                        file_age = current_time - filepath.stat().st_mtime
                        if file_age > days * 86400:
                            filepath.unlink()
                            count += 1
                            logger.info(f"Deleted old backup: {filepath.name}")
            
            logger.info(f"Cleaned up {count} old backups")
            return count
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            return 0
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, *args):
        """Context manager cleanup"""
        pass