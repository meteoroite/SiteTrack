 url=https://github.com/meteoroite/SiteTrack/blob/main/src/ui/report_creation.py
"""
Multi-step report creation flow with comprehensive validation and error handling
"""
import flet as ft
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from logger import setup_logger
from src.utils.validators import (
    validate_report_data, validate_issue_data, validate_photo_file
)
from src.utils.exceptions import ValidationError, DatabaseError

logger = setup_logger(__name__)


class ReportCreationScreen:
    """Report creation wizard with validation and error handling"""
    
    def __init__(self, app):
        """Initialize report creation screen"""
        self.app = app
        self.report_data = app.current_report or {
            'project_name': '',
            'location': '',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'report_type': 'Site Inspection',
            'issues': [],
            'photos': [],
            'status': 'draft',
            'notes': '',
        }
        self.current_step = 0
        self.steps = ["Basic Info", "Checklist", "Issues", "Photos", "Review"]
        self.photo_picker = None
        self.checklist_results = {}  # Track checklist selections
        logger.debug("ReportCreationScreen initialized")
    
    def build(self) -> ft.View:
        """Build the report creation UI"""
        try:
            logger.info(f"Building report creation screen - Step {self.current_step}")
            
            return ft.View(
                "/new_report",
                [
                    ft.AppBar(
                        title=ft.Text(f"New Report - {self.steps[self.current_step]}", size=16),
                        bgcolor=ft.colors.BLUE_700,
                        color=ft.colors.WHITE,
                        leading=ft.IconButton(
                            "arrow_back",
                            on_click=lambda e: self._go_back()
                        ),
                    ),
                    
                    ft.Container(
                        content=ft.Column(
                            [
                                self._build_progress_indicator(),
                                ft.Container(
                                    content=self._get_step_content(),
                                    expand=True,
                                    padding=20,
                                ),
                                self._build_navigation_buttons(),
                            ],
                            spacing=15,
                        ),
                        expand=True,
                    ),
                ],
            )
        except Exception as e:
            logger.error(f"Error building report creation screen: {e}")
            return self._build_error_view(e)
    
    def _build_progress_indicator(self) -> ft.Container:
        """Build step progress indicator"""
        try:
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(
                                    content=ft.Text(
                                        f"{i+1}",
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.WHITE if i <= self.current_step else ft.colors.BLACK,
                                    ),
                                    bgcolor=ft.colors.BLUE_700 if i <= self.current_step else ft.colors.GREY_300,
                                    border_radius=15,
                                    width=30,
                                    height=30,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Text(self.steps[i], size=10),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        )
                        for i in range(len(self.steps))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                padding=15,
            )
        except Exception as e:
            logger.error(f"Error building progress indicator: {e}")
            return ft.Container()
    
    def _get_step_content(self) -> ft.Control:
        """Get content for current step"""
        try:
            if self.current_step == 0:
                return self._build_basic_info_step()
            elif self.current_step == 1:
                return self._build_checklist_step()
            elif self.current_step == 2:
                return self._build_issues_step()
            elif self.current_step == 3:
                return self._build_photos_step()
            elif self.current_step == 4:
                return self._build_review_step()
            return ft.Text("Unknown step")
        except Exception as e:
            logger.error(f"Error getting step content: {e}")
            return ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)
    
    def _build_basic_info_step(self) -> ft.Column:
        """Step 1: Basic information form"""
        try:
            return ft.Column(
                [
                    ft.TextField(
                        label="Project Name *",
                        value=self.report_data.get('project_name', ''),
                        on_change=lambda e: self._update_field('project_name', e.control.value),
                        hint_text="Enter project name (required)",
                        min_lines=1,
                    ),
                    ft.TextField(
                        label="Location *",
                        value=self.report_data.get('location', ''),
                        on_change=lambda e: self._update_field('location', e.control.value),
                        hint_text="Site location (required)",
                        min_lines=1,
                    ),
                    ft.TextField(
                        label="Date",
                        value=self.report_data.get('date', ''),
                        read_only=True,
                    ),
                    ft.Dropdown(
                        label="Report Type",
                        value=self.report_data.get('report_type', 'Site Inspection'),
                        options=[
                            ft.dropdown.Option("Site Inspection"),
                            ft.dropdown.Option("Safety Audit"),
                            ft.dropdown.Option("Quality Control"),
                            ft.dropdown.Option("Maintenance Report"),
                            ft.dropdown.Option("Final Inspection"),
                            ft.dropdown.Option("Progress Report"),
                            ft.dropdown.Option("Incident Report"),
                        ],
                        on_change=lambda e: self._update_field('report_type', e.control.value),
                    ),
                    ft.TextField(
                        label="Notes",
                        value=self.report_data.get('notes', ''),
                        on_change=lambda e: self._update_field('notes', e.control.value),
                        hint_text="Additional notes (optional)",
                        multiline=True,
                        min_lines=3,
                    ),
                ],
                spacing=15,
            )
        except Exception as e:
            logger.error(f"Error building basic info step: {e}")
            return ft.Column([ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)])
    
    def _build_checklist_step(self) -> ft.Column:
        """Step 2: Dynamic checklist"""
        try:
            checklist_items = [
                "Safety Equipment Available",
                "Site Access Clear",
                "Proper Signage Posted",
                "Emergency Exits Accessible",
                "Equipment Properly Maintained",
                "Documentation Complete",
                "Environmental Hazards Assessed",
                "Quality Standards Met",
            ]
            
            checklist_controls = []
            for item in checklist_items:
                checklist_controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(item, expand=True, size=12),
                                ft.ToggleButtons(
                                    selected=[0] if self.checklist_results.get(item, 'ok') == 'ok' else [1],
                                    options=[
                                        ft.ToggleButtonsOption(text="✓", value="ok"),
                                        ft.ToggleButtonsOption(text="✕", value="issue"),
                                    ],
                                    on_change=lambda e, i=item: self._update_checklist(i, e.control.selected),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=10,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        margin=ft.margin.only(bottom=5),
                    )
                )
            
            return ft.Column(
                [
                    ft.Text("Site Inspection Checklist", size=14, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                ] + checklist_controls,
                spacing=5,
            )
        except Exception as e:
            logger.error(f"Error building checklist step: {e}")
            return ft.Column([ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)])
    
    def _build_issues_step(self) -> ft.Column:
        """Step 3: Issues management"""
        try:
            issues = self.report_data.get('issues', [])
            
            add_button = ft.IconButton(
                "add_circle",
                icon_size=24,
                on_click=lambda e: self._add_issue_dialog(),
                tooltip="Add new issue",
            )
            
            if not issues:
                issue_content = ft.Text("No issues added yet", color=ft.colors.GREY_600, size=12)
            else:
                issue_content = ft.Column(
                    [
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(issue.get('title', ''), weight=ft.FontWeight.BOLD, size=12),
                                    ft.IconButton(
                                        "delete",
                                        icon_size=16,
                                        on_click=lambda e, idx=issues.index(issue): self._remove_issue(idx),
                                    ),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Text(issue.get('description', ''), size=11, color=ft.colors.GREY_700),
                                ft.Row([
                                    ft.Chip(label=ft.Text(f"Severity: {issue.get('severity', '')}", size=9)),
                                    ft.Chip(label=ft.Text(f"Status: {issue.get('status', '')}", size=9)),
                                ], spacing=10),
                            ], spacing=5),
                            padding=10,
                            bgcolor=ft.colors.WHITE,
                            border_radius=5,
                            border=ft.border.all(1, ft.colors.GREY_300),
                        )
                        for issue in issues
                    ],
                    spacing=10,
                )
            
            return ft.Column([
                ft.Row([
                    ft.Text("Issues Found", weight=ft.FontWeight.BOLD, size=14),
                    add_button,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Container(content=issue_content, expand=True),
            ])
        except Exception as e:
            logger.error(f"Error building issues step: {e}")
            return ft.Column([ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)])
    
    def _build_photos_step(self) -> ft.Column:
        """Step 4: Photos management"""
        try:
            return ft.Column([
                ft.Row([
                    ft.Text("Site Photos", weight=ft.FontWeight.BOLD, size=14),
                    ft.ElevatedButton(
                        "Add Photos",
                        icon="image",
                        on_click=lambda e: self._add_photo(),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text(f"📷 {len(self.report_data.get('photos', []))} photo(s) attached", size=12),
            ], spacing=10)
        except Exception as e:
            logger.error(f"Error building photos step: {e}")
            return ft.Column([ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)])
    
    def _build_review_step(self) -> ft.Column:
        """Step 5: Review report"""
        try:
            issues_count = len(self.report_data.get('issues', []))
            photos_count = len(self.report_data.get('photos', []))
            
            return ft.Column([
                ft.Text("📄", size=60, text_align=ft.TextAlign.CENTER),
                ft.Text("Review Report", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                ft.Text(f"Project: {self.report_data.get('project_name', 'Not specified')}", size=12),
                ft.Text(f"Location: {self.report_data.get('location', 'Not specified')}", size=12),
                ft.Text(f"Date: {self.report_data.get('date', 'N/A')}", size=12),
                ft.Text(f"Type: {self.report_data.get('report_type', 'N/A')}", size=12),
                ft.Divider(),
                ft.Text(f"Issues: {issues_count}", size=12, color=ft.colors.RED_700 if issues_count > 0 else ft.colors.GREY_700),
                ft.Text(f"Photos: {photos_count}", size=12),
                ft.Divider(),
                ft.ElevatedButton(
                    "Generate PDF Report",
                    icon="picture_as_pdf",
                    on_click=lambda e: self._generate_report(),
                    width=200,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        except Exception as e:
            logger.error(f"Error building review step: {e}")
            return ft.Column([ft.Text(f"Error: {str(e)}", color=ft.colors.RED_700)])
    
    def _build_navigation_buttons(self) -> ft.Container:
        """Build next/previous navigation buttons"""
        try:
            buttons = []
            
            if self.current_step > 0:
                buttons.append(
                    ft.ElevatedButton(
                        "Previous",
                        on_click=lambda e: self._previous_step(),
                        icon="arrow_back",
                    )
                )
            
            if self.current_step < len(self.steps) - 1:
                buttons.append(
                    ft.ElevatedButton(
                        "Next",
                        on_click=lambda e: self._next_step(),
                        icon="arrow_forward",
                    )
                )
            
            buttons.append(
                ft.TextButton(
                    "Save Draft",
                    on_click=lambda e: self._save_draft(),
                    icon="save",
                )
            )
            
            return ft.Container(
                content=ft.Row(buttons, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True),
                padding=10,
            )
        except Exception as e:
            logger.error(f"Error building navigation buttons: {e}")
            return ft.Container()
    
    def _update_field(self, field: str, value):
        """Update report data field"""
        try:
            self.report_data[field] = value
            logger.debug(f"Updated field {field}")
        except Exception as e:
            logger.error(f"Error updating field {field}: {e}")
    
    def _update_checklist(self, item: str, selected):
        """Update checklist result"""
        try:
            if selected and len(selected) > 0:
                self.checklist_results[item] = 'issue' if selected[0] == 1 else 'ok'
                logger.debug(f"Checklist item '{item}' updated to: {self.checklist_results[item]}")
        except Exception as e:
            logger.error(f"Error updating checklist: {e}")
    
    def _add_issue_dialog(self):
        """Dialog to add new issue"""
        try:
            title_field = ft.TextField(label="Issue Title *", min_lines=1)
            desc_field = ft.TextField(label="Description *", multiline=True, min_lines=3)
            severity_field = ft.Dropdown(
                label="Severity",
                options=[ft.dropdown.Option(x) for x in ["Low", "Medium", "High", "Critical"]],
                value="Medium"
            )
            
            def add_issue(e):
                try:
                    # Validate issue data
                    issue_data = {
                        'title': title_field.value,
                        'description': desc_field.value,
                        'severity': severity_field.value or "Medium",
                        'status': 'open',
                        'report_id': 1,  # Temporary, will be set on save
                    }
                    
                    is_valid, errors = validate_issue_data(issue_data)
                    if not is_valid:
                        error_msg = "\n".join(errors)
                        self._show_error(f"Invalid Issue\n{error_msg}")
                        return
                    
                    self.report_data['issues'].append(issue_data)
                    dialog.open = False
                    logger.info(f"Issue added: {issue_data['title']}")
                    self.app.page.update()
                except Exception as ex:
                    logger.error(f"Error adding issue: {ex}")
                    self._show_error(f"Error: {str(ex)}")
            
            def close_dialog(e):
                dialog.open = False
                self.app.page.update()
            
            dialog = ft.AlertDialog(
                title=ft.Text("Add Issue"),
                content=ft.Column([title_field, desc_field, severity_field], spacing=10),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dialog),
                    ft.ElevatedButton("Add", on_click=add_issue),
                ],
            )
            
            self.app.page.dialog = dialog
            dialog.open = True
            self.app.page.update()
            logger.debug("Issue dialog opened")
        except Exception as e:
            logger.error(f"Error opening issue dialog: {e}")
            self._show_error(f"Error: {str(e)}")
    
    def _remove_issue(self, index: int):
        """Remove issue from list"""
        try:
            if 0 <= index < len(self.report_data['issues']):
                removed = self.report_data['issues'].pop(index)
                logger.info(f"Issue removed: {removed.get('title')}")
                self.app.page.update()
        except Exception as e:
            logger.error(f"Error removing issue: {e}")
    
    def _add_photo(self):
        """Add photo using file picker"""
        try:
            def on_result(e: ft.FilePickerResultEvent):
                try:
                    if e.files:
                        for file in e.files:
                            # Validate photo
                            is_valid, error_msg = validate_photo_file(file.path)
                            if not is_valid:
                                logger.warning(f"Invalid photo: {error_msg}")
                                self._show_error(f"Invalid Photo\n{error_msg}")
                                continue
                            
                            self.report_data['photos'].append(file.path)
                            logger.info(f"Photo added: {file.path}")
                        
                        self.app.page.update()
                except Exception as ex:
                    logger.error(f"Error processing photos: {ex}")
                    self._show_error(f"Error: {str(ex)}")
            
            # Create picker only once
            if self.photo_picker is None:
                self.photo_picker = ft.FilePicker(on_result=on_result)
                self.app.page.overlay.append(self.photo_picker)
            
            self.photo_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["jpg", "jpeg", "png", "gif"]
            )
            logger.debug("Photo picker opened")
        except Exception as e:
            logger.error(f"Error opening photo picker: {e}")
            self._show_error(f"Error: {str(e)}")
    
    def _save_draft(self):
        """Save current report as draft"""
        try:
            # Validate report data
            is_valid, errors = validate_report_data(self.report_data)
            if not is_valid:
                error_msg = "\n".join(errors)
                self._show_error(f"Validation Error\n{error_msg}")
                return
            
            if self.app.save_draft(self.report_data):
                self._show_success("Draft Saved Successfully")
                logger.info("Draft saved successfully")
            else:
                self._show_error("Failed to save draft")
        except Exception as e:
            logger.error(f"Error saving draft: {e}")
            self._show_error(f"Save Error\n{str(e)}")
    
    def _generate_report(self):
        """Generate final PDF report"""
        try:
            # Validate report data
            is_valid, errors = validate_report_data(self.report_data)
            if not is_valid:
                error_msg = "\n".join(errors)
                self._show_error(f"Validation Error\n{error_msg}")
                return
            
            logger.info(f"Generating report: {self.report_data.get('project_name')}")
            
            # Create report if new
            if not self.report_data.get('id'):
                self.report_data['id'] = self.app.report_service.create_report(self.report_data)
            
            # Complete report and generate PDF
            pdf_path = self.app.report_service.complete_report(
                self.report_data['id'],
                self.report_data
            )
            
            self._show_success(f"Report Generated\n{pdf_path}")
            logger.info(f"Report generated successfully: {pdf_path}")
            
            # Navigate back to home
            self.app.navigate_to("/")
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            self._show_error(f"Generation Error\n{str(e)}")
    
    def _next_step(self):
        """Go to next step with validation"""
        try:
            # Validate current step before proceeding
            if self.current_step == 0:
                is_valid, errors = validate_report_data(self.report_data)
                if not is_valid:
                    error_msg = "\n".join(errors)
                    self._show_error(f"Validation Error\n{error_msg}")
                    return
            
            self.current_step = min(self.current_step + 1, len(self.steps) - 1)
            logger.debug(f"Advanced to step {self.current_step}")
            self.app.page.views[-1] = self.build()
            self.app.page.update()
        except Exception as e:
            logger.error(f"Error advancing step: {e}")
            self._show_error(f"Error: {str(e)}")
    
    def _previous_step(self):
        """Go to previous step"""
        try:
            self.current_step = max(self.current_step - 1, 0)
            logger.debug(f"Returned to step {self.current_step}")
            self.app.page.views[-1] = self.build()
            self.app.page.update()
        except Exception as e:
            logger.error(f"Error going back: {e}")
            self._show_error(f"Error: {str(e)}")
    
    def _go_back(self):
        """Go back to home"""
        try:
            logger.debug("Returning to home screen")
            self.app.navigate_to("/")
        except Exception as e:
            logger.error(f"Error navigating back: {e}")
    
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
            snack = ft.SnackBar(ft.Text(f"✓ {message}"), bgcolor=ft.colors.GREEN_50)
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
            "/new_report",
            [
                ft.AppBar(
                    title=ft.Text("Error", size=16),
                    bgcolor=ft.colors.RED_700,
                    color=ft.colors.WHITE,
                    leading=ft.IconButton(
                        "arrow_back",
                        on_click=lambda e: self._go_back()
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Error Creating Report", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(str(error), size=12, color=ft.colors.RED_700),
                            ft.ElevatedButton(
                                "Go Back",
                                on_click=lambda e: self._go_back()
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