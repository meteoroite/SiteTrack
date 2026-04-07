"""
Issue card component - displays issue information
"""

import flet as ft

class IssueCard:
    """UI component displaying issue information"""
    
    @staticmethod
    def build(issue, on_click=None, on_delete=None):
        """Build issue card"""
        severity_color = IssueCard.get_severity_color(issue.get('severity'))
        
        action_buttons = [
            ft.IconButton(
                "edit",
                tooltip="Edit",
                on_click=lambda e: print("Edit issue"),
            ),
        ]
        
        if on_delete:
            action_buttons.append(
                ft.IconButton(
                    "delete",
                    tooltip="Delete",
                    on_click=on_delete,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        issue.get('title', 'Untitled'),
                                        weight=ft.FontWeight.BOLD,
                                        size=14,
                                    ),
                                    ft.Text(
                                        issue.get('description', '')[:100],
                                        size=11,
                                        color=ft.colors.GREY_700,
                                    ),
                                ],
                                expand=True,
                                spacing=5,
                            ),
                            ft.Chip(
                                label=ft.Text(
                                    issue.get('severity', 'Medium'),
                                    size=10,
                                    color=ft.colors.WHITE,
                                ),
                                bgcolor=severity_color,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"Status: {issue.get('status', 'open')}",
                                size=10,
                                color=ft.colors.GREY_600,
                            ),
                            ft.Row(action_buttons),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=8,
            ),
            padding=12,
            margin=8,
            bgcolor=ft.colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300),
            on_click=on_click,
        )
    
    @staticmethod
    def get_severity_color(severity):
        """Get color for severity level"""
        severity_lower = severity.lower()
        if severity_lower == 'critical' or severity_lower == 'high':
            return ft.colors.RED_700
        elif severity_lower == 'medium':
            return ft.colors.ORANGE_700
        elif severity_lower == 'low':
            return ft.colors.BLUE_700
        return ft.colors.GREY_700
