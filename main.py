import flet as ft
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from logger import setup_logger
from config import Config
from src.main_app import FieldReportApp
from src.utils.exceptions import SiteTrackException

logger = setup_logger(__name__)


def main(page: ft.Page):
    """Main entry point for Flet application"""
    try:
        logger.info("=" * 60)
        logger.info("SiteTrack Application Starting")
        logger.info("=" * 60)
        
        # Initialize application
        app = FieldReportApp()
        
        # Setup routes
        app.setup_routes(page)
        
        logger.info("Application started successfully")
        
    except SiteTrackException as e:
        logger.critical(f"SiteTrack exception during startup: {e}")
        page.add(ft.Text(f"Fatal Error: {str(e)}", color=ft.colors.RED_700))
    except Exception as e:
        logger.critical(f"Unexpected error during startup: {e}")
        page.add(ft.Text(f"Critical Error: {str(e)}", color=ft.colors.RED_700))


if __name__ == "__main__":
    try:
        logger.info("Initializing Flet application...")
        ft.app(target=main, assets_dir="assets")
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        raise