"""
Settings and preferences screen
"""

import flet as ft
import os

class SettingsScreen:
    """Application settings and preferences"""
    
    def __init__(self, app):
        self.app = app
    
    def build(self):
        """Build settings interface"""
        return ft.View(
            "/settings",
            [
                ft.AppBar(
                    title=ft.Text("Settings", size=18),
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
                            self._build_app_settings(),
                            ft.Divider(height=20),
                            self._build_storage_settings(),
                            ft.Divider(height=20),
                            self._build_export_settings(),
                            ft.Divider(height=20),
                            self._build_about_section(),
                        ],
                        spacing=20,
                    ),
                    expand=True,
                    padding=20,
                ),
            ],
        )
    
    def _build_app_settings(self):
        """Build general app settings"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Application Settings", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                self._build_setting_row(
                    "Auto-save Drafts",
                    ft.Switch(value=True, on_change=lambda e: None),
                ),
                self._build_setting_row(
                    "Enable Notifications",
                    ft.Switch(value=True, on_change=lambda e: None),
                ),
                self._build_setting_row(
                    "Report Format",
                    ft.Dropdown(
                        value="PDF",
                        options=[
                            ft.dropdown.Option("PDF"),
                            ft.dropdown.Option("DOCX"),
                            ft.dropdown.Option("Both"),
                        ],
                    ),
                ),
                self._build_setting_row(
                    "Photo Quality",
                    ft.Dropdown(
                        value="High",
                        options=[
                            ft.dropdown.Option("Low"),
                            ft.dropdown.Option("Medium"),
                            ft.dropdown.Option("High"),
                        ],
                    ),
                ),
            ]),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _build_storage_settings(self):
        """Build storage and database settings"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Storage", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                self._build_storage_info(),
                ft.ElevatedButton(
                    "Clear Cache",
                    icon="delete",
                    on_click=lambda e: self._clear_cache(),
                ),
                ft.ElevatedButton(
                    "Backup Database",
                    icon="backup",
                    on_click=lambda e: self._backup_database(),
                ),
                ft.ElevatedButton(
                    "Restore from Backup",
                    icon="restore",
                    on_click=lambda e: self._restore_backup(),
                ),
            ], spacing=10),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _build_storage_info(self):
        """Show storage info"""
        try:
            if os.path.exists('field_reports.db'):
                db_size = os.path.getsize('field_reports.db') / 1024  # KB
                return ft.Column([
                    ft.Text(f"Database Size: {db_size:.2f} KB"),
                    ft.Text(f"Location: {os.path.abspath('field_reports.db')}", size=11, color=ft.colors.GREY_700),
                ])
            else:
                return ft.Text("Database not found", color=ft.colors.GREY_600)
        except Exception as e:
            return ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)
    
    def _build_export_settings(self):
        """Build export/import settings"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Data Management", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                ft.ElevatedButton(
                    "Export All Reports",
                    icon="download",
                    on_click=lambda e: self._export_reports(),
                ),
                ft.ElevatedButton(
                    "Export Templates",
                    icon="download",
                    on_click=lambda e: self._export_templates(),
                ),
                ft.ElevatedButton(
                    "Import Reports",
                    icon="upload",
                    on_click=lambda e: self._import_reports(),
                ),
            ], spacing=10),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _build_about_section(self):
        """Build about section"""
        return ft.Container(
            content=ft.Column([
                ft.Text("About", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                ft.Text("SiteTrack", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Field Report Generation System", size=12, color=ft.colors.GREY_700),
                ft.Text("Version 1.0.0", size=11, color=ft.colors.GREY_600),
                ft.Divider(),
                ft.Row([
                    ft.IconButton("bug_report", tooltip="Report Issue"),
                    ft.IconButton("info", tooltip="More Info"),
                    ft.IconButton("settings", tooltip="Advanced"),
                ]),
            ]),
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
        )
    
    def _build_setting_row(self, label, control):
        """Build a settings row"""
        return ft.Row(
            [
                ft.Text(label, expand=True),
                control,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    def _clear_cache(self):
        """Clear application cache"""
        try:
            # Implementation would clear temp files
            self.app.page.snack_bar = ft.SnackBar(ft.Text("Cache cleared"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
        except Exception as e:
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
    
    def _backup_database(self):
        """Backup database"""
        try:
            backup_path = self.app.file_storage.backup_database()
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Backup: {backup_path}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
        except Exception as e:
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Backup error: {str(e)}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
    
    def _restore_backup(self):
        """Restore from backup"""
        self.app.page.snack_bar = ft.SnackBar(ft.Text("Restore functionality coming soon"))
        self.app.page.snack_bar.open = True
        self.app.page.update()
    
    def _export_reports(self):
        """Export all reports"""
        try:
            export_path = self.app.file_storage.export_reports()
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Exported to: {export_path}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
        except Exception as e:
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Export error: {str(e)}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
    
    def _export_templates(self):
        """Export templates"""
        try:
            export_path = self.app.file_storage.export_templates()
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Templates exported to: {export_path}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
        except Exception as e:
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Export error: {str(e)}"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
    
    def _import_reports(self):
        """Import reports"""
        self.app.page.snack_bar = ft.SnackBar(ft.Text("Import functionality coming soon"))
        self.app.page.snack_bar.open = True
        self.app.page.update()
