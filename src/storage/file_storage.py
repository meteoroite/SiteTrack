"""
File storage layer - file management operations
"""

import os
import shutil
import json
from datetime import datetime
from PIL import Image as PILImage
from src.services.pdf_service import PDFService

class FileStorage:
    """File storage and management"""
    
    def __init__(self, base_dir: str = "reports"):
        self.base_dir = base_dir
        self.photos_dir = os.path.join(base_dir, "photos")
        self.backups_dir = os.path.join(base_dir, "backups")
        self.exports_dir = os.path.join(base_dir, "exports")
        
        os.makedirs(self.photos_dir, exist_ok=True)
        os.makedirs(self.backups_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)
        
        self.pdf_service = PDFService(base_dir)
    
    def process_image(self, path: str, max_width: int = 800) -> str:
        """Process and optimize image"""
        try:
            img = PILImage.open(path)
            
            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), PILImage.Resampling.LANCZOS)
            
            # Save optimized version
            img.save(path, quality=85)
            return path
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def save_photo(self, photo_path: str, report_id: int) -> str:
        """Save photo for report"""
        try:
            if not os.path.exists(photo_path):
                raise FileNotFoundError(f"Photo not found: {photo_path}")
            
            # Process image first
            self.process_image(photo_path)
            
            filename = f"report_{report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            dest_path = os.path.join(self.photos_dir, filename)
            shutil.copy2(photo_path, dest_path)
            return dest_path
        except Exception as e:
            print(f"Error saving photo: {e}")
            return None
    
    def get_report_photos(self, report_id: int) -> list:
        """Get all photos for report"""
        photos = []
        try:
            for filename in os.listdir(self.photos_dir):
                if filename.startswith(f"report_{report_id}_"):
                    photos.append(os.path.join(self.photos_dir, filename))
        except Exception as e:
            print(f"Error getting photos: {e}")
        return photos
    
    def delete_photo(self, photo_path: str) -> bool:
        """Delete photo"""
        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
                return True
        except Exception as e:
            print(f"Error deleting photo: {e}")
        return False
    
    def generate_pdf(self, report_data: dict) -> str:
        """Generate PDF report"""
        return self.pdf_service.generate_report_pdf(report_data)
    
    def backup_database(self) -> str:
        """Backup database"""
        src = "field_reports.db"
        if os.path.exists(src):
            backup_name = f"field_reports_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            dest = os.path.join(self.backups_dir, backup_name)
            shutil.copy2(src, dest)
            return dest
        return None
    
    def restore_database(self, backup_path: str) -> bool:
        """Restore database from backup"""
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, "field_reports.db")
            return True
        return False
    
    def export_reports(self) -> str:
        """Export all reports to JSON"""
        from src.storage.database import Database
        
        db = Database()
        reports = db.get_all_reports()
        
        export_file = os.path.join(
            self.exports_dir,
            f"reports_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(export_file, 'w') as f:
            json.dump(reports, f, indent=2)
        
        db.close()
        return export_file
    
    def export_templates(self) -> str:
        """Export all templates to JSON"""
        from src.storage.database import Database
        
        db = Database()
        templates = db.get_all_templates()
        
        export_file = os.path.join(
            self.exports_dir,
            f"templates_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(export_file, 'w') as f:
            json.dump(templates, f, indent=2)
        
        db.close()
        return export_file
    
    def import_reports(self, import_file: str) -> int:
        """Import reports from JSON"""
        from src.storage.database import Database
        
        if not os.path.exists(import_file):
            raise FileNotFoundError(f"Import file not found: {import_file}")
        
        db = Database()
        
        with open(import_file, 'r') as f:
            reports = json.load(f)
        
        count = 0
        for report in reports:
            report.pop('id', None)  # Remove ID to create new records
            db.add_report(report)
            count += 1
        
        db.close()
        return count
    
    def get_storage_size(self) -> dict:
        """Get storage statistics"""
        def get_dir_size(path):
            total = 0
            if os.path.exists(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        total += os.path.getsize(filepath)
            return total
        
        return {
            'reports': get_dir_size(self.base_dir) / 1024,  # KB
            'photos': get_dir_size(self.photos_dir) / 1024,
            'backups': get_dir_size(self.backups_dir) / 1024,
        }
    
    def cleanup_old_backups(self, days: int = 30) -> int:
        """Delete backups older than N days"""
        import time
        
        current_time = time.time()
        count = 0
        
        for filename in os.listdir(self.backups_dir):
            filepath = os.path.join(self.backups_dir, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > days * 86400:  # Convert days to seconds
                    os.remove(filepath)
                    count += 1
        
        return count
