 url=https://github.com/meteoroite/SiteTrack/blob/main/src/ui/home_screen.py
"""
Home dashboard screen with report overview and quick actions
"""
import flet as ft
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from logger import setup_logger

logger = setup_logger(__name__)


class HomeScreen:
    """Main dashboard view with error handling"""
    
    def __init__(self, app):
        """Initialize home screen"""
        self.app = app
        logger.debug("HomeScreen initialized")
    
    def build(self) -> ft.View:
        """Build the home screen UI with error handling"""
        try:
            logger.info("Building home screen...")
            
            return ft.View(
                "/",
                [
                    # App Bar
                    ft.AppBar(
                        title=ft.Text("SiteTrack", size=20, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.BLUE_700,
                        color=ft.colors.WHITE,
                        center_title=False,
                    ),
                    
                    # Main content
                    ft.Container(
                        content=ft.Column(
                            [
                                # New Report Button - Prominent
                                self._build_new_report_button(),
                                
                                # Stats Cards Row
                                self._build_stats_row(),
                                
                                # Draft Reports Section
                                self._build_drafts_section(),
                                
                                # Recent Completed Reports
                                self._build_recent_reports_section(),
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            spacing=15,
                        ),
                        expand=True,
                        padding=15,
                    ),
                ],
                navigation_bar=self._build_navigation_bar(),
            )
        except Exception as e:
            logger.error(f"Error building home screen: {e}")
            return self._build_error_view(e)
    
    def _build_new_report_button(self) -> ft.Container:
        """Build new report button"""
        try:
            return ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Text("📝", size=20),
                            ft.Text("New Report", size=16, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=lambda e: self._navigate_new_report(),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREEN_700,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    width=float('inf'),
                ),
                padding=10,
            )
        except Exception as e:
            logger.error(f"Error building new report button: {e}")
            return ft.Container()
    
    def _build_stats_row(self) -> ft.Container:
        """Build statistics row"""
        try:
            drafts_count = len(self.app.get_drafts())
            completed_count = len(self.app.get_completed_reports())
            
            return ft.Container(
                content=ft.Row(
                    [
                        self._build_stat_card("Drafts", str(drafts_count), "📋", ft.colors.ORANGE_700),
                        self._build_stat_card("Completed", str(completed_count), "✅", ft.colors.BLUE_700),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                padding=10,
            )
        except Exception as e:
            logger.error(f"Error building stats row: {e}")
            return ft.Container()
    
    def _build_stat_card(self, title: str, value: str, icon: str, color: str) -> ft.Container:
        """Build a statistics card"""
        try:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(icon, size=30),
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(title, size=12, color=ft.colors.GREY_700),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                padding=15,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.colors.GREY_300),
                expand=True,
            )
        except Exception as e:
            logger.error(f"Error building stat card: {e}")
            return ft.Container()
    
    def _build_drafts_section(self) -> ft.Container:
        """Build drafts section"""
        try:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text("📋 Recent Drafts", size=16, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Container(
                            content=ft.Column(
                                self._build_draft_list(),
                                scroll=ft.ScrollMode.AUTO,
                                spacing=8,
                            ),
                            height=250,
                            border_radius=8,
                            bgcolor=ft.colors.GREY_50,
                            padding=10,
                        ),
                    ],
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building drafts section: {e}")
            return ft.Container()
    
    def _build_draft_list(self) -> list:
        """Build list of draft reports"""
        try:
            drafts = self.app.get_drafts()
            
            if not drafts:
                return [ft.Text("No drafts available", color=ft.colors.GREY_600, size=13)]
            
            draft_cards = []
            for draft in drafts[:5]:  # Show last 5 drafts
                try:
                    draft_cards.append(
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row([
                                        ft.Text(draft.get('project_name', 'Untitled'), 
                                               weight=ft.FontWeight.BOLD, size=13),
                                        ft.IconButton(
                                            "edit",
                                            icon_size=18,
                                            on_click=lambda e, d=draft: self._edit_draft(d)
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    ft.Text(
                                        f"Location: {draft.get('location', 'N/A')}",
                                        size=11,
                                        color=ft.colors.GREY_700
                                    ),
                                    ft.Text(
                                        f"Updated: {self._format_date(draft.get('updated_at', draft.get('date', 'N/A')))}",
                                        size=10,
                                        color=ft.colors.GREY_600
                                    ),
                                ],
                                spacing=5,
                            ),
                            padding=10,
                            bgcolor=ft.colors.WHITE,
                            border_radius=5,
                            border=ft.border.all(1, ft.colors.GREY_300),
                        )
                    )
                except Exception as e:
                    logger.warning(f"Error building draft card: {e}")
                    continue
            
            return draft_cards if draft_cards else [ft.Text("No valid drafts", color=ft.colors.GREY_600)]
        except Exception as e:
            logger.error(f"Error building draft list: {e}")
            return [ft.Text("Error loading drafts", color=ft.colors.RED_700)]
    
    def _build_recent_reports_section(self) -> ft.Container:
        """Build recent reports section"""
        try:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text("📄 Recent Reports", size=16, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.Container(
                            content=ft.Column(
                                self._build_recent_reports_list(),
                                scroll=ft.ScrollMode.AUTO,
                                spacing=8,
                            ),
                            height=250,
                            border_radius=8,
                            bgcolor=ft.colors.GREY_50,
                            padding=10,
                        ),
                    ],
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building recent reports section: {e}")
            return ft.Container()
    
    def _build_recent_reports_list(self) -> list:
        """Build list of recent completed reports"""
        try:
            reports = self.app.get_completed_reports()
            
            if not reports:
                return [ft.Text("No completed reports", color=ft.colors.GREY_600, size=13)]
            
            report_cards = []
            for report in reports[:5]:
                try:
                    issues_count = len(report.get('issues', []))
                    report_cards.append(
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(report.get('project_name', 'Untitled'),
                                           weight=ft.FontWeight.BOLD, size=13),
                                    ft.Text(
                                        f"Location: {report.get('location', 'N/A')}",
                                        size=11,
                                        color=ft.colors.GREY_700
                                    ),
                                    ft.Row([
                                        ft.Text(
                                            f"Date: {report.get('date', 'N/A')}",
                                            size=10,
                                            color=ft.colors.GREY_600
                                        ),
                                        ft.Text(
                                            f"Issues: {issues_count}",
                                            size=10,
                                            color=ft.colors.RED_700 if issues_count > 0 else ft.colors.GREEN_700
                                        ),
                                    ], spacing=15),
                                ],
                                spacing=5,
                            ),
                            padding=10,
                            bgcolor=ft.colors.WHITE,
                            border_radius=5,
                            border=ft.border.all(1, ft.colors.GREY_300),
                        )
                    )
                except Exception as e:
                    logger.warning(f"Error building report card: {e}")
                    continue
            
            return report_cards if report_cards else [ft.Text("No valid reports", color=ft.colors.GREY_600)]
        except Exception as e:
            logger.error(f"Error building recent reports list: {e}")
            return [ft.Text("Error loading reports", color=ft.colors.RED_700)]
    
    def _build_navigation_bar(self) -> ft.NavigationBar:
        """Build bottom navigation bar"""
        try:
            return ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon="home", label="Home"),
                    ft.NavigationBarDestination(icon="bar_chart", label="Analytics"),
                    ft.NavigationBarDestination(icon="settings", label="Settings"),
                ],
                on_change=lambda e: self._handle_navigation(e.control.selected_index),
            )
        except Exception as e:
            logger.error(f"Error building navigation bar: {e}")
            return ft.NavigationBar()
    
    def _handle_navigation(self, index: int):
        """Handle navigation bar selection"""
        try:
            routes = ["/", "/analytics", "/settings"]
            if 0 <= index < len(routes):
                self.app.navigate_to(routes[index])
                logger.debug(f"Navigation to index {index}: {routes[index]}")
        except Exception as e:
            logger.error(f"Error handling navigation: {e}")
    
    def _edit_draft(self, draft):
        """Navigate to edit draft report"""
        try:
            logger.info(f"Editing draft: {draft.get('project_name')}")
            self.app.current_report = draft
            self.app.navigate_to("/new_report")
        except Exception as e:
            logger.error(f"Error editing draft: {e}")
    
    def _navigate_new_report(self):
        """Navigate to create new report"""
        try:
            logger.debug("Navigating to new report creation")
            self.app.current_report = None
            self.app.navigate_to("/new_report")
        except Exception as e:
            logger.error(f"Error navigating to new report: {e}")
    
    def _format_date(self, date_str: str) -> str:
        """Format date string"""
        try:
            if not date_str or date_str == 'N/A':
                return 'N/A'
            # Try to parse ISO format or standard format
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except:
                # If it's already formatted, return as is
                if len(date_str) >= 10:
                    return date_str[:10]
                return date_str
        except Exception as e:
            logger.warning(f"Error formatting date {date_str}: {e}")
            return date_str[:10] if len(date_str) >= 10 else date_str
    
    def _build_error_view(self, error: Exception) -> ft.View:
        """Build error view"""
        return ft.View(
            "/",
            [
                ft.AppBar(
                    title=ft.Text("Error", size=20),
                    bgcolor=ft.colors.RED_700,
                    color=ft.colors.WHITE,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Error Loading Dashboard", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(str(error), size=14, color=ft.colors.RED_700),
                            ft.ElevatedButton(
                                "Retry",
                                on_click=lambda e: self.app.navigate_to("/")
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
            ],
        )