"""
Home dashboard screen with report overview and quick actions
"""

import flet as ft
from datetime import datetime

class HomeScreen:
    """Main dashboard view"""
    
    def __init__(self, app):
        self.app = app
    
    def build(self):
        """Build the home screen UI"""
        return ft.View(
            "/",
            [
                # App Bar
                ft.AppBar(
                    title=ft.Text("SiteTrack", size=20, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                ),
                
                # Main content
                ft.Container(
                    content=ft.Column(
                        [
                            # New Report Button - Prominent
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Row(
                                        [
                                            ft.Text("📝", size=20),
                                            ft.Text("New Report", size=18, weight=ft.FontWeight.BOLD),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    on_click=lambda e: self.app.navigate_to("/new_report"),
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.GREEN_700,
                                        padding=20,
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                    ),
                                    width=float('inf'),
                                ),
                                padding=20,
                            ),
                            
                            # Stats Cards Row
                            ft.Container(
                                content=ft.Row(
                                    [
                                        self._build_stat_card("Drafts", len(self.app.get_drafts()), "📋", ft.colors.ORANGE_700),
                                        self._build_stat_card("Completed", len(self.app.get_completed_reports()), "✅", ft.colors.BLUE_700),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                padding=ft.padding.only(left=10, right=10),
                            ),
                            
                            # Draft Reports Section
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Recent Drafts", size=20, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Column(
                                                self._build_draft_list(),
                                                scroll=ft.ScrollMode.AUTO,
                                                spacing=10,
                                            ),
                                            height=300,
                                        ),
                                    ],
                                ),
                                padding=20,
                            ),
                            
                            # Recent Completed Reports
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Recent Reports", size=20, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Column(
                                                self._build_recent_reports(),
                                                scroll=ft.ScrollMode.AUTO,
                                                spacing=10,
                                            ),
                                            height=300,
                                        ),
                                    ],
                                ),
                                padding=20,
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    expand=True,
                ),
            ],
            navigation_bar=self._build_navigation_bar(),
        )
    
    def _build_stat_card(self, title: str, value: int, icon, color):
        """Build a statistics card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(icon, size=30),
                    ft.Text(str(value), size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(title, size=14, color=ft.colors.GREY_700),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            padding=15,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.GREY_300,
            ),
            width=150,
        )
    
    def _build_draft_list(self):
        """Build list of draft reports"""
        drafts = self.app.get_drafts()
        if not drafts:
            return [ft.Text("No drafts available", color=ft.colors.GREY_600)]
        
        draft_cards = []
        for draft in drafts[:5]:  # Show last 5 drafts
            draft_cards.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Text("📋", size=24),
                        title=ft.Text(draft['project_name'], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Updated: {draft['updated_at'][:10]}"),
                        trailing=ft.IconButton(
                            icon="edit",
                            on_click=lambda e, d=draft: self._edit_draft(d)
                        ),
                    ),
                    bgcolor=ft.colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=3,
                        color=ft.colors.GREY_300,
                    ),
                )
            )
        return draft_cards
    
    def _build_recent_reports(self):
        """Build list of recent completed reports"""
        reports = self.app.get_completed_reports()
        if not reports:
            return [ft.Text("No completed reports", color=ft.colors.GREY_600)]
        
        report_cards = []
        for report in reports[:5]:
            report_cards.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Text("📄", size=24),
                        title=ft.Text(report['project_name'], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Date: {report['date']} | Issues: {len(report.get('issues', []))}"),
                        trailing=ft.Text("👁️", size=20),
                    ),
                    bgcolor=ft.colors.WHITE,
                    border_radius=8,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=3,
                        color=ft.colors.GREY_300,
                    ),
                )
            )
        return report_cards
    
    def _edit_draft(self, draft):
        """Navigate to edit draft report"""
        self.app.current_report = draft
        self.app.navigate_to("/new_report")
    
    def _build_navigation_bar(self):
        """Build bottom navigation bar"""
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon="home", label="Home"),
                ft.NavigationBarDestination(icon="bar_chart", label="Analytics"),
                ft.NavigationBarDestination(icon="settings", label="Settings"),
            ],
            on_change=lambda e: self._handle_navigation(e.control.selected_index),
        )
    
    def _handle_navigation(self, index):
        """Handle navigation bar selection"""
        if index == 0:
            pass  # Already on home
        elif index == 1:
            self.app.navigate_to("/analytics")
        elif index == 2:
            self.app.navigate_to("/settings")
