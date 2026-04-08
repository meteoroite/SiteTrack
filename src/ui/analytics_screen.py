 url=https://github.com/meteoroite/SiteTrack/blob/main/src/ui/analytics_screen.py
"""
Analytics dashboard showing report statistics and trends with error handling
"""
import flet as ft
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from logger import setup_logger

logger = setup_logger(__name__)


class AnalyticsScreen:
    """Analytics and reporting dashboard"""
    
    def __init__(self, app):
        """Initialize analytics screen"""
        self.app = app
        logger.debug("AnalyticsScreen initialized")
    
    def build(self) -> ft.View:
        """Build analytics dashboard"""
        try:
            logger.info("Building analytics screen...")
            stats = self._get_statistics()
            
            return ft.View(
                "/analytics",
                [
                    ft.AppBar(
                        title=ft.Text("Analytics", size=18),
                        bgcolor=ft.colors.BLUE_700,
                        color=ft.colors.WHITE,
                        leading=ft.IconButton(
                            "arrow_back",
                            on_click=lambda e: self.app.navigate_to("/")
                        ),
                    ),
                    
                    ft.Container(
                        content=ft.ListView(
                            [
                                self._build_summary_cards(stats),
                                ft.Divider(height=15),
                                self._build_report_chart(stats),
                                ft.Divider(height=15),
                                self._build_issue_breakdown(stats),
                                ft.Divider(height=15),
                                self._build_recent_reports(stats),
                            ],
                            spacing=10,
                        ),
                        expand=True,
                        padding=15,
                    ),
                ],
            )
        except Exception as e:
            logger.error(f"Error building analytics screen: {e}")
            return self._build_error_view(e)
    
    def _get_statistics(self) -> dict:
        """Calculate statistics from database"""
        try:
            logger.debug("Calculating statistics...")
            
            reports = self.app.get_all_reports()
            
            total_reports = len(reports)
            completed_reports = len([r for r in reports if r.get('status') == 'completed'])
            draft_reports = len([r for r in reports if r.get('status') == 'draft'])
            archived_reports = len([r for r in reports if r.get('status') == 'archived'])
            
            # Calculate issues
            total_issues = sum(len(r.get('issues', [])) for r in reports)
            critical_issues = sum(
                len([i for i in r.get('issues', []) if i.get('severity') in ['High', 'Critical']])
                for r in reports
            )
            resolved_issues = sum(
                len([i for i in r.get('issues', []) if i.get('status') == 'resolved'])
                for r in reports
            )
            
            stats = {
                'total_reports': total_reports,
                'completed_reports': completed_reports,
                'draft_reports': draft_reports,
                'archived_reports': archived_reports,
                'total_issues': total_issues,
                'critical_issues': critical_issues,
                'resolved_issues': resolved_issues,
                'reports': reports,
            }
            
            logger.debug(f"Statistics calculated: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {
                'total_reports': 0,
                'completed_reports': 0,
                'draft_reports': 0,
                'archived_reports': 0,
                'total_issues': 0,
                'critical_issues': 0,
                'resolved_issues': 0,
                'reports': [],
            }
    
    def _build_summary_cards(self, stats: dict) -> ft.Row:
        """Build summary statistics cards"""
        try:
            return ft.Row(
                [
                    self._build_stat_card("Total Reports", str(stats['total_reports']), ft.colors.BLUE_700),
                    self._build_stat_card("Completed", str(stats['completed_reports']), ft.colors.GREEN_700),
                    self._build_stat_card("Drafts", str(stats['draft_reports']), ft.colors.ORANGE_700),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            )
        except Exception as e:
            logger.error(f"Error building summary cards: {e}")
            return ft.Row()
    
    def _build_stat_card(self, title: str, value: str, color: str) -> ft.Container:
        """Build individual statistic card"""
        try:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=color),
                        ft.Text(title, size=11, color=ft.colors.GREY_700),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
                expand=True,
            )
        except Exception as e:
            logger.error(f"Error building stat card: {e}")
            return ft.Container()
    
    def _build_report_chart(self, stats: dict) -> ft.Container:
        """Build report statistics chart"""
        try:
            completed = stats['completed_reports']
            draft = stats['draft_reports']
            archived = stats['archived_reports']
            
            return ft.Container(
                content=ft.Column([
                    ft.Text("Report Status", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    self._build_progress_bar("Completed", completed, ft.colors.GREEN_700),
                    self._build_progress_bar("Draft", draft, ft.colors.ORANGE_700),
                    self._build_progress_bar("Archived", archived, ft.colors.GREY_700),
                ], spacing=10),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building report chart: {e}")
            return ft.Container()
    
    def _build_progress_bar(self, label: str, value: int, color: str) -> ft.Container:
        """Build progress bar"""
        try:
            total = max(value + 1, 1)  # Avoid division by zero
            percentage = min((value / total) * 100, 100) if total > 0 else 0
            
            return ft.Container(
                content=ft.Row([
                    ft.Text(label, width=70, size=11),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=color,
                            border_radius=5,
                            width=(percentage / 100) * 150,
                            height=15,
                        ),
                        width=150,
                        height=15,
                        bgcolor=ft.colors.GREY_300,
                        border_radius=5,
                    ),
                    ft.Text(f"{int(percentage)}%", width=40, size=10),
                ], alignment=ft.MainAxisAlignment.START),
                padding=10,
            )
        except Exception as e:
            logger.error(f"Error building progress bar: {e}")
            return ft.Container()
    
    def _build_issue_breakdown(self, stats: dict) -> ft.Container:
        """Build issue severity breakdown"""
        try:
            total_issues = stats['total_issues']
            critical = stats['critical_issues']
            resolved = stats['resolved_issues']
            open_issues = total_issues - resolved
            
            return ft.Container(
                content=ft.Column([
                    ft.Text("Issue Status", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(total_issues), size=22, weight=ft.FontWeight.BOLD),
                                ft.Text("Total Issues", size=10),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=5,
                            padding=10,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(critical), size=22, weight=ft.FontWeight.BOLD, color=ft.colors.RED_700),
                                ft.Text("Critical", size=10),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=5,
                            padding=10,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(open_issues), size=22, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_700),
                                ft.Text("Open", size=10),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=5,
                            padding=10,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(resolved), size=22, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                                ft.Text("Resolved", size=10),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=5,
                            padding=10,
                        ),
                    ], spacing=10),
                ], spacing=10),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building issue breakdown: {e}")
            return ft.Container()
    
    def _build_recent_reports(self, stats: dict) -> ft.Container:
        """Build recent reports list"""
        try:
            reports = sorted(stats['reports'], key=lambda x: x.get('date', ''), reverse=True)[:5]
            
            if not reports:
                content = ft.Text("No reports yet", color=ft.colors.GREY_600, size=12)
            else:
                content = ft.Column(
                    [
                        ft.Container(
                            content=ft.Column([
                                ft.Text(report.get('project_name', 'Unknown'), weight=ft.FontWeight.BOLD, size=12),
                                ft.Text(report.get('location', ''), size=11, color=ft.colors.GREY_700),
                                ft.Text(report.get('date', ''), size=10, color=ft.colors.GREY_600),
                            ], spacing=3),
                            padding=10,
                            bgcolor=ft.colors.GREY_50,
                            border_radius=5,
                            border=ft.border.all(1, ft.colors.GREY_300),
                        )
                        for report in reports
                    ],
                    spacing=8,
                )
            
            return ft.Container(
                content=ft.Column([
                    ft.Text("Recent Reports", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    content,
                ], spacing=10),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building recent reports: {e}")
            return ft.Container()
    
    def _build_error_view(self, error: Exception) -> ft.View:
        """Build error view"""
        return ft.View(
            "/analytics",
            [
                ft.AppBar(
                    title=ft.Text("Error", size=18),
                    bgcolor=ft.colors.RED_700,
                    color=ft.colors.WHITE,
                    leading=ft.IconButton(
                        "arrow_back",
                        on_click=lambda e: self.app.navigate_to("/")
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Error Loading Analytics", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(str(error), size=12, color=ft.colors.RED_700),
                            ft.ElevatedButton(
                                "Retry",
                                on_click=lambda e: self.app.navigate_to("/analytics")
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