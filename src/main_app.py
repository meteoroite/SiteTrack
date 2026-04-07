"""
Main application controller
Handles navigation and global state management
"""

import flet as ft
from src.ui.home_screen import HomeScreen
from src.ui.report_creation import ReportCreationScreen
from src.ui.analytics_screen import AnalyticsScreen
from src.ui.settings_screen import SettingsScreen
from src.storage.database import Database
from src.storage.file_storage import FileStorage
from src.services.report_service import ReportService
from src.services.template_service import TemplateService

class FieldReportApp:
    """Main application class managing navigation and state"""
    
    def __init__(self):
        self.db = Database()
        self.file_storage = FileStorage()
        self.report_service = ReportService(self.db, self.file_storage)
        self.template_service = TemplateService(self.db)
        self.current_report = None
        self.current_report_id = None
        self.page = None
        
    def setup_routes(self, page: ft.Page):
        """Configure navigation routes"""
        self.page = page
        page.title = "SiteTrack"
        page.padding = 0
        page.window.icon = "assets/SiteTrack.ico"
        
        # Define route handlers
        def route_change(route):
            self.page.views.clear()
            
            # Create appropriate view based on route
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
            
            self.page.update()
        
        def view_pop(view):
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        
        self.page.on_route_change = route_change
        self.page.on_view_pop = view_pop
        self.page.go(self.page.route)
    
    def navigate_to(self, route: str):
        """Navigate to a specific route"""
        self.page.go(route)
    
    def save_draft(self, report_data: dict):
        """Save current report as draft"""
        self.report_service.save_draft(report_data)
    
    def get_drafts(self):
        """Get all draft reports"""
        return self.report_service.get_drafts()
    
    def get_all_reports(self):
        """Get all reports"""
        return self.report_service.get_all_reports()
    
    def get_completed_reports(self):
        """Get all completed reports"""
        all_reports = self.get_all_reports()
        return [r for r in all_reports if r.get('status') == 'completed']

def main():
    """Entry point for the Flet application"""
    app = FieldReportApp()
    
    ft.app(target=lambda page: app.setup_routes(page))

if __name__ == "__main__":
    main()
