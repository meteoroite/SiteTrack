 url=https://github.com/meteoroite/SiteTrack/blob/main/src/main_app.py
"""
Main application controller - handles navigation and global state management
"""
import flet as ft
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import setup_logger
from src.ui.home_screen import HomeScreen
from src.ui.report_creation import ReportCreationScreen
from src.ui.analytics_screen import AnalyticsScreen
from src.ui.settings_screen import SettingsScreen
from src.storage.database import Database
from src.storage.file_storage import FileStorage
from src.services.report_service import ReportService
from src.services.template_service import TemplateService
from src.services.pdf_service import PDFService
from src.utils.exceptions import DatabaseError, FileStorageError

logger = setup_logger(__name__)


class FieldReportApp:
    """Main application class managing navigation and state"""
    
    def __init__(self):
        """Initialize application with all services"""
        try:
            logger.info("Initializing FieldReportApp...")
            
            # Initialize services
            self.db = Database()
            self.file_storage = FileStorage()
            self.pdf_service = PDFService()
            self.report_service = ReportService(self.db, self.file_storage)
            self.template_service = TemplateService(self.db)
            
            # Application state
            self.current_report = None
            self.current_report_id = None
            self.page = None
            
            logger.info("FieldReportApp initialized successfully")
        except (DatabaseError, FileStorageError) as e:
            logger.error(f"Failed to initialize application services: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during initialization: {e}")
            raise
    
    def setup_routes(self, page: ft.Page):
        """Configure navigation routes with error handling"""
        try:
            self.page = page
            page.title = "SiteTrack - Field Report Generator"
            page.padding = 0
            page.window.min_width = 300
            page.window.min_height = 600
            
            logger.info("Setting up application routes...")
            
            # Define route handler
            def route_change(route):
                """Handle route changes with error handling"""
                try:
                    self.page.views.clear()
                    logger.debug(f"Route changed to: {self.page.route}")
                    
                    if self.page.route == "/":
                        home = HomeScreen(self)
                        self.page.views.append(home.build())
                    elif self.page.route == "/new_report":
                        report_creation = ReportCreationScreen(self)
                        self.page.views.append(report_creation.build())
                    elif self.page.route == "/analytics":
                        analytics = AnalyticsScreen(self)
                        self.page.views.append(analytics.build())
                    elif self.page.route == "/settings":
                        settings = SettingsScreen(self)
                        self.page.views.append(settings.build())
                    else:
                        # Default to home if route not found
                        logger.warning(f"Unknown route: {self.page.route}, redirecting to home")
                        self.page.go("/")
                    
                    self.page.update()
                except Exception as e:
                    logger.error(f"Error during route change: {e}")
                    self._show_error_dialog(page, f"Navigation error: {str(e)}")
            
            def view_pop(view):
                """Handle back button navigation"""
                try:
                    if len(self.page.views) > 1:
                        self.page.views.pop()
                        top_view = self.page.views[-1]
                        self.page.go(top_view.route)
                except Exception as e:
                    logger.error(f"Error during back navigation: {e}")
            
            page.on_route_change = route_change
            page.on_view_pop = view_pop
            page.go(page.route)
            
            logger.info("Routes configured successfully")
        except Exception as e:
            logger.error(f"Error setting up routes: {e}")
            raise
    
    def navigate_to(self, route: str):
        """Navigate to a specific route with error handling"""
        try:
            logger.debug(f"Navigating to: {route}")
            self.page.go(route)
        except Exception as e:
            logger.error(f"Navigation error to {route}: {e}")
            self._show_error("Navigation Error", str(e))
    
    def save_draft(self, report_data: dict) -> bool:
        """Save current report as draft"""
        try:
            logger.info(f"Saving draft for report: {report_data.get('project_name')}")
            self.report_service.save_draft(report_data)
            self._show_success("Draft Saved", "Your report has been saved as a draft")
            return True
        except Exception as e:
            logger.error(f"Error saving draft: {e}")
            self._show_error("Save Error", str(e))
            return False
    
    def get_drafts(self) -> list:
        """Get all draft reports"""
        try:
            logger.debug("Retrieving draft reports...")
            drafts = self.report_service.get_drafts()
            logger.debug(f"Found {len(drafts)} drafts")
            return drafts
        except Exception as e:
            logger.error(f"Error getting drafts: {e}")
            return []
    
    def get_all_reports(self) -> list:
        """Get all reports"""
        try:
            logger.debug("Retrieving all reports...")
            reports = self.report_service.get_all_reports()
            logger.debug(f"Found {len(reports)} reports")
            return reports
        except Exception as e:
            logger.error(f"Error getting all reports: {e}")
            return []
    
    def get_completed_reports(self) -> list:
        """Get all completed reports"""
        try:
            all_reports = self.get_all_reports()
            completed = [r for r in all_reports if r.get('status') == 'completed']
            logger.debug(f"Found {len(completed)} completed reports")
            return completed
        except Exception as e:
            logger.error(f"Error getting completed reports: {e}")
            return []
    
    def _show_error(self, title: str, message: str):
        """Show error snackbar"""
        try:
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"{title}: {message}"),
                    bgcolor=ft.colors.RED_50,
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            logger.error(f"Error showing error dialog: {e}")
    
    def _show_success(self, title: str, message: str):
        """Show success snackbar"""
        try:
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"✓ {title}: {message}"),
                    bgcolor=ft.colors.GREEN_50,
                )
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as e:
            logger.error(f"Error showing success dialog: {e}")
    
    def _show_error_dialog(self, page: ft.Page, message: str):
        """Show error dialog"""
        try:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(message),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self._close_dialog(page, dialog))
                ],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
        except Exception as e:
            logger.error(f"Error showing dialog: {e}")
    
    def _close_dialog(self, page: ft.Page, dialog: ft.AlertDialog):
        """Close dialog"""
        dialog.open = False
        page.update()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            logger.info("Cleaning up application resources...")
            self.db.close()
            logger.info("Application cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __del__(self):
        """Destructor for cleanup"""
        self.cleanup()