"""
Report card component - displays report summary
"""

import flet as ft

class ReportCard:
    """UI component displaying report information"""
    
    @staticmethod
    def build(report, on_click=None):
        """Build report card"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                report.get('project_name', 'Untitled'),
                                weight=ft.FontWeight.BOLD,
                                size=14,
                                expand=True,
                            ),
                            ft.Chip(
                                label=ft.Text(report.get('status', 'draft').upper(), size=10),
                                bgcolor=ReportCard.get_status_color(report.get('status')),
                            ),
                        ]
                    ),
                    ft.Text(
                        report.get('location', ''),
                        size=12,
                        color=ft.colors.GREY_700,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"Date: {report.get('date', 'N/A')}",
                                size=10,
                                color=ft.colors.GREY_600,
                            ),
                            ft.Text(
                                f"Issues: {len(report.get('issues', []))}",
                                size=10,
                                color=ft.colors.GREY_600,
                            ),
                        ],
                        spacing=30,
                    ),
                ],
                spacing=5,
            ),
            padding=15,
            margin=10,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.GREY_300),
            on_click=on_click,
        )
    
    @staticmethod
    def get_status_color(status):
        """Get color for status"""
        if status == 'completed':
            return ft.colors.GREEN_500
        elif status == 'draft':
            return ft.colors.ORANGE_500
        elif status == 'archived':
            return ft.colors.GREY_500
        return ft.colors.BLUE_500
