 url=https://github.com/meteoroite/SiteTrack/blob/main/src/ui/settings_screen.py
"""
Settings and preferences screen with enhanced functionality
"""
import flet as ft
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from logger import setup_logger

logger = setup_logger(__name__)


class SettingsScreen:
    """Application settings and preferences"""
    
    def __init__(self, app):
        """Initialize settings screen"""
        self.app = app
        logger.debug("SettingsScreen initialized")
    
    def build(self) -> ft.View:
        """Build settings interface"""
        try:
            logger.info("Building settings screen...")
            
            return ft.View(
                "/settings",
                [
                    ft.AppBar(
                        title=ft.Text("Settings", size=18),
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
                                self._build_app_settings(),
                                ft.Divider(height=15),
                                self._build_storage_settings(),
                                ft.Divider(height=15),
                                self._build_data_management(),
                                ft.Divider(height=15),
                                self._build_about_section(),
                            ],
                            spacing=10,
                        ),
                        expand=True,
                        padding=15,
                    ),
                ],
            )
        except Exception as e:
            logger.error(f"Error building settings screen: {e}")
            return self._build_error_view(e)
    
    def _build_app_settings(self) -> ft.Container:
        """Build general app settings"""
        try:
            return ft.Container(
                content=ft.Column([
                    ft.Text("Application Settings", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    self._build_setting_row(
                        "Auto-save Drafts",
                        ft.Switch(value=True, label="Enabled"),
                    ),
                    self._build_setting_row(
                        "Show Notifications",
                        ft.Switch(value=True, label="Enabled"),
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
                            width=150,
                        ),
                    ),
                ], spacing=10),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building app settings: {e}")
            return ft.Container()
    
    def _build_storage_settings(self) -> ft.Container:
        """Build storage and database settings"""
        try:
            storage_stats = self.app.file_storage.get_storage_stats()
            
            return ft.Container(
                content=ft.Column([
                    ft.Text("Storage & Database", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    ft.Text(
                        f"Total Storage: {storage_stats.get('total_kb', 0):.2f} KB",
                        size=11,
                        color=ft.colors.GREY_700
                    ),
                    ft.Text(
                        f"Photos: {storage_stats.get('photos_kb', 0):.2f} KB",
                        size=11,
                        color=ft.colors.GREY_700
                    ),
                    ft.Text(
                        f"Backups: {storage_stats.get('backups_kb', 0):.2f} KB",
                        size=11,
                        color=ft.colors.GREY_700
                    ),
                    ft.Divider(height=10),
                    ft.Row([
                        ft.ElevatedButton(
                            "Backup Database",
                            icon="backup",
                            on_click=lambda e: self._backup_database(),
                        ),
                        ft.ElevatedButton(
                            "Cleanup Old Backups",
                            icon="delete",
                            on_click=lambda e: self._cleanup_backups(),
                        ),
                    ], spacing=10, wrap=True),
                ], spacing=10),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building storage settings: {e}")
            return ft.Container()
    
    def _build_data_management(self) -> ft.Container:
        """Build data management settings"""
        try:
            return ft.Container(
                content=ft.Column([
                    ft.Text("Data Management", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    ft.Row([
                        ft.ElevatedButton(
                            "Export Reports",
                            icon="download",
                            on_click=lambda e: self._export_reports(),
                        ),
                        ft.ElevatedButton(
                            "Export Templates",
                            icon="download",
                            on_click=lambda e: self._export_templates(),
                        ),
                    ], spacing=10, wrap=True),
                ], spacing=10),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building data management: {e}")
            return ft.Container()
    
    def _build_about_section(self) -> ft.Container:
        """Build about section"""
        try:
            return ft.Container(
                content=ft.Column([
                    ft.Text("About", weight=ft.FontWeight.BOLD, size=14),
                    ft.Divider(height=10),
                    ft.Text("SiteTrack", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Field Report Generation System", size=12, color=ft.colors.GREY_700),
                    ft.Text("Version 2.0.0", size=11, color=ft.colors.GREY_600),
                    ft.Text("© 2026 SiteTrack. All rights reserved.", size=10, color=ft.colors.GREY_600),
                ], spacing=5),
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=3, color=ft.colors.GREY_300),
            )
        except Exception as e:
            logger.error(f"Error building about section: {e}")
            return ft.Container()
    
    def _build_setting_row(self, label: str, control: ft.Control) -> ft.Row:
        """Build a settings row"""
        try:
            return ft.Row(
                [
                    ft.Text(label, expand=True, size=12),
                    control,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        except Exception as e:
            logger.error(f"Error building setting row: {e}")
            return ft.Row()
    
    def _backup_database(self):
        """Backup database"""
        try:
            logger.info("Starting database backup...")
            backup_path = self.app.file_storage.backup_database()
            self._show_success(f"✓ Database Backed Up\n{backup_path}")
            logger.info(f"Database backed up: {backup_path}")
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            self._show_error(f"Backup Error\n{str(e)}")
    
    def _cleanup_backups(self):
        """Cleanup old backups"""
        try:
            logger.info("Cleaning up old backups...")
            count = self.app.file_storage.cleanup_old_backups(days=30)
            self._show_success(f"✓ Cleanup Complete\n{count} old backups removed")
            logger.info(f"Cleanup complete: {count} backups removed")
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            self._show_error(f"Cleanup Error\n{str(e)}")
    
    def _export_reports(self):
        """Export all reports"""
        try:
            logger.info("Exporting reports...")
            reports = self.app.get_all_reports()
            export_path = self.app.file_storage.export_reports(reports)
            self._show_success(f"✓ Reports Exported\n{export_path}")
            logger.info(f"Reports exported: {export_path}")
        except Exception as e:
            logger.error(f"Error exporting reports: {e}")
            self._show_error(f"Export Error\n{str(e)}")
    
    def _export_templates(self):
        """Export templates"""
        try:
            logger.info("Exporting templates...")
            templates = self.app.template_service.get_all_templates()
            export_path = self.app.file_storage.export_reports(templates)
            self._show_success(f"✓ Templates Exported\n{export_path}")
            logger.info(f"Templates exported: {export_path}")
        except Exception as e:
            logger.error(f"Error exporting templates: {e}")
            self._show_error(f"Export Error\n{str(e)}")
    
    def _show_error(self, message: str):
        """Show error message"""
        try:
            dialog = ft.AlertDialog(
                title=ft.Text("Error", color=ft.colors.RED_700),
                content=ft.Text(message, size=12),
                actions=[ft.TextButton("OK", on_click=lambda e: self._close_dialog(dialog))],
            )
            self.app.page.dialog = dialog
            dialog.open = True
            self.app.page.update()
        except Exception as e:
            logger.error(f"Error showing error dialog: {e}")
    
    def _show_success(self, message: str):
        """Show success message"""
        try:
            snack = ft.SnackBar(ft.Text(message), bgcolor=ft.colors.GREEN_50)
            self.app.page.snack_bar = snack
            snack.open = True
            self.app.page.update()
        except Exception as e:
            logger.error(f"Error showing success message: {e}")
    
    def _close_dialog(self, dialog: ft.AlertDialog):
        """Close dialog"""
        dialog.open = False
        self.app.page.update()
    
    def _build_error_view(self, error: Exception) -> ft.View:
        """Build error view"""
        return ft.View(
            "/settings",
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
                            ft.Text("Error Loading Settings", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(str(error), size=12, color=ft.colors.RED_700),
                            ft.ElevatedButton(
                                "Go Back",
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