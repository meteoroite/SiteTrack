"""
Initialize application - create required directories and database
Run this once before starting the app
"""

import os
from src.storage.database import Database
from src.storage.file_storage import FileStorage
from src.services.pdf_service import PDFService

def initialize_app():
    """Initialize app directories and database"""
    
    print("🚀 Initializing SiteTrack Application...")
    
    # Create directory structure
    dirs = [
        "reports",
        "reports/photos",
        "reports/backups", 
        "reports/exports",
        "outputs",
        "assets",
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")
    
    # Initialize database
    db = Database("field_reports.db")
    print("✓ Database initialized")
    
    # Test file storage
    storage = FileStorage("reports")
    print("✓ File storage initialized")
    
    # Test PDF service
    pdf_service = PDFService("reports")
    print("✓ PDF service initialized")
    
    print("\n✅ Application initialized successfully!")
    print("\nYou can now run the app with: python main.py")

if __name__ == "__main__":
    try:
        initialize_app()
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
