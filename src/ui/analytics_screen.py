"""
Analytics dashboard showing report statistics and trends
"""

import flet as ft
from datetime import datetime, timedelta

class AnalyticsScreen:
    """Analytics and reporting dashboard"""
    
    def __init__(self, app):
        self.app = app
    
    def build(self):
        """Build analytics dashboard"""
        stats = self._get_statistics()
        
        return ft.View(
            "/analytics",
            [
                ft.AppBar(
                    title=ft.Text("Analytics", size=18),
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                    leading=ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: self.app.navigate_to("/")
                    ),
                ),
                
                ft.Container(
                    content=ft.ListView(
                        [
                            self._build_summary_cards(stats),
                            ft.Divider(height=20),
                            self._build_report_chart(),
                            ft.Divider(height=20),
                            self._build_issue_breakdown(stats),
                            ft.Divider(height=20),
                            self._build_recent_reports(),
                        ],
                        spacing=20,
                    ),
                    expand=True,
                    padding=20,
                ),
            ],
        )
    
    def _get_statistics(self):
        """Calculate statistics from database"""
        try:
            reports = self.app.db.get_all_reports()
            issues = self.app.db.get_all_issues()
            
            total_reports = len(reports)
            completed_reports = len([r for r in reports if r.get('status') == 'completed'])
            draft_reports = len([r for r in reports if r.get('status') == 'draft'])
            
            total_issues = len(issues)
            critical_issues = len([i for i in issues if i.get('severity') == 'High'])
            resolved_issues = len([i for i in issues if i.get('status') == 'resolved'])
            
            return {
                'total_reports': total_reports,
                'completed_reports': completed_reports,
                'draft_reports': draft_reports,
                'total_issues': total_issues,
                'critical_issues': critical_issues,
                'resolved_issues': resolved_issues,
                'reports': reports,
                'issues': issues,
            }
        except:
            return {
                'total_reports': 0,
                'completed_reports': 0,
                'draft_reports': 0,
                'total_issues': 0,
                'critical_issues': 0,
                'resolved_issues': 0,
                'reports': [],
                'issues': [],
            }
    
    def _build_summary_cards(self, stats):
        """Build summary statistics cards"""
        return ft.Row(
            [
                self._build_stat_card("Total Reports", str(stats['total_reports']), ft.colors.BLUE_700),
                self._build_stat_card("Completed", str(stats['completed_reports']), ft.colors.GREEN_700),
                self._build_stat_card("Drafts", str(stats['draft_reports']), ft.colors.ORANGE_700),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def _build_stat_card(self, title, value, color):
        """Build individual statistic card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(title, size=12, color=ft.colors.GREY_700),
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
    
    def _build_report_chart(self):
        """Build report statistics chart"""
        stats = self._get_statistics()
        completed = stats['completed_reports']
        draft = stats['draft_reports']
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Report Status", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                self._build_progress_bar("Completed", completed, ft.colors.GREEN_700),
                self._build_progress_bar("Draft", draft, ft.colors.ORANGE_700),
            ]),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _build_progress_bar(self, label, value, color):
        """Build progress bar"""
        total = value + 1  # Avoid division by zero
        percentage = min((value / total) * 100, 100) if total > 0 else 0
        
        return ft.Container(
            content=ft.Row([
                ft.Text(label, width=60),
                ft.Container(
                    content=ft.Container(
                        bgcolor=color,
                        border_radius=5,
                        width=(percentage / 100) * 200,
                        height=20,
                    ),
                    width=200,
                    height=20,
                    bgcolor=ft.colors.GREY_300,
                    border_radius=5,
                ),
                ft.Text(f"{int(percentage)}%", width=40),
            ]),
            padding=10,
        )
    
    def _build_issue_breakdown(self, stats):
        """Build issue severity breakdown"""
        total_issues = stats['total_issues']
        critical = stats['critical_issues']
        resolved = stats['resolved_issues']
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Issue Status", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(str(total_issues), size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Total Issues"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        padding=10,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(str(critical), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_700),
                            ft.Text("Critical"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        padding=10,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(str(resolved), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                            ft.Text("Resolved"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        expand=True,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        padding=10,
                    ),
                ], spacing=10),
            ]),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _build_recent_reports(self):
        """Build recent reports list"""
        stats = self._get_statistics()
        reports = sorted(stats['reports'], key=lambda x: x.get('date'), reverse=True)[:5]
        
        if not reports:
            content = ft.Text("No reports yet", color=ft.colors.GREY_600)
        else:
            content = ft.Column(
                [
                    ft.Container(
                        content=ft.Column([
                            ft.Text(report.get('project_name', 'Unknown'), weight=ft.FontWeight.BOLD),
                            ft.Text(report.get('location', ''), size=12, color=ft.colors.GREY_700),
                            ft.Text(report.get('date', ''), size=11, color=ft.colors.GREY_600),
                        ]),
                        padding=10,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        on_click=lambda e, rid=report.get('id'): self._view_report(rid),
                    )
                    for report in reports
                ]
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Recent Reports", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                content,
            ]),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _view_report(self, report_id):
        """Navigate to report details"""
        self.app.current_report_id = report_id
        self.app.navigate_to(f"/report/{report_id}")
