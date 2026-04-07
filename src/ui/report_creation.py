"""
Multi-step report creation flow with camera and issue management
"""

import flet as ft
from datetime import datetime
import os

class ReportCreationScreen:
    """Report creation wizard with steps"""
    
    def __init__(self, app):
        self.app = app
        self.report_data = app.current_report or {
            'project_name': '',
            'location': '',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'report_type': 'Site Inspection',
            'issues': [],
            'photos': [],
            'status': 'draft'
        }
        self.current_step = 0
        self.steps = ["Basic Info", "Checklist", "Issues", "Photos", "Generate"]
        self.photo_picker = None  # Initialize once to avoid duplication
    
    def build(self):
        """Build the report creation UI"""
        return ft.View(
            "/new_report",
            [
                ft.AppBar(
                    title=ft.Text(f"New Report - {self.steps[self.current_step]}", size=18),
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                    leading=ft.IconButton(
                        icon="arrow_back",
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
                        spacing=20,
                    ),
                    expand=True,
                ),
            ],
        )
    
    def _build_progress_indicator(self):
        """Build step progress indicator"""
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
            padding=20,
        )
    
    def _get_step_content(self):
        """Get content for current step"""
        if self.current_step == 0:
            return self._build_basic_info_step()
        elif self.current_step == 1:
            return self._build_checklist_step()
        elif self.current_step == 2:
            return self._build_issues_step()
        elif self.current_step == 3:
            return self._build_photos_step()
        elif self.current_step == 4:
            return self._build_generate_step()
        return ft.Text("Unknown step")
    
    def _build_basic_info_step(self):
        """Step 1: Basic information form"""
        return ft.Column(
            [
                ft.TextField(
                    label="Project Name",
                    value=self.report_data.get('project_name', ''),
                    on_change=lambda e: self._update_field('project_name', e.control.value),
                    hint_text="Enter project name",
                ),
                ft.TextField(
                    label="Location",
                    value=self.report_data.get('location', ''),
                    on_change=lambda e: self._update_field('location', e.control.value),
                    hint_text="Site location",
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
                    ],
                    on_change=lambda e: self._update_field('report_type', e.control.value),
                ),
                ft.ElevatedButton(
                    "Save Project",
                    icon="save",
                    on_click=lambda e: self._save_project(),
                ),
            ],
            spacing=15,
        )
    
    def _build_checklist_step(self):
        """Step 2: Dynamic checklist"""
        checklist_items = [
            "Safety Equipment Available",
            "Site Access Clear",
            "Proper Signage Posted",
            "Emergency Exits Accessible",
            "Equipment Properly Maintained",
            "Documentation Complete",
        ]
        
        return ft.Column(
            [
                ft.Text("Site Inspection Checklist", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
            ] + [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(item, expand=True),
                            ft.ToggleButtons(
                                selected=[0],
                                options=[
                                    ft.ToggleButtonsOption(text="✓", value="ok"),
                                    ft.ToggleButtonsOption(text="✕", value="issue"),
                                ],
                            ),
                        ]
                    ),
                    padding=10,
                    bgcolor=ft.colors.GREY_100,
                    border_radius=5,
                    margin=ft.margin.only(bottom=5),
                )
                for item in checklist_items
            ],
            spacing=5,
        )
    
    def _build_issues_step(self):
        """Step 3: Issues management"""
        issues = self.report_data.get('issues', [])
        
        if not issues:
            issue_content = ft.Text("No issues added yet", color=ft.colors.GREY_600)
        else:
            issue_content = ft.Column(
                [
                    ft.Container(
                        content=ft.Column([
                            ft.Text(issue.get('title', ''), weight=ft.FontWeight.BOLD),
                            ft.Text(issue.get('description', ''), size=12, color=ft.colors.GREY_700),
                            ft.Text(f"Severity: {issue.get('severity', '')}"),
                        ]),
                        padding=10,
                        bgcolor=ft.colors.WHITE,
                        border_radius=5,
                    )
                    for issue in issues
                ]
            )
        
        return ft.Column([
            ft.Row([
                ft.Text("Issues Found", weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    "note",
                    on_click=lambda e: self._add_issue_dialog(),
                ),
            ]),
            ft.Divider(),
            ft.Container(content=issue_content, expand=True),
        ])
    
    def _build_photos_step(self):
        """Step 4: Photos management"""
        return ft.Column([
            ft.Row([
                ft.Text("Site Photos", weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Add Photo", on_click=lambda e: self._add_photo()),
            ]),
            ft.Divider(),
            ft.Text(f"Photos: {len(self.report_data.get('photos', []))}"),
        ])
    
    def _build_generate_step(self):
        """Step 5: Generate report"""
        return ft.Column([
            ft.Text("📄", size=80),
            ft.Text("Ready to Generate Report", size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"Project: {self.report_data.get('project_name', 'Not specified')}"),
            ft.Text(f"Location: {self.report_data.get('location', 'Not specified')}"),
            ft.Text(f"Issues: {len(self.report_data.get('issues', []))}"),
            ft.Text(f"Photos: {len(self.report_data.get('photos', []))}"),
            ft.Divider(),
            ft.ElevatedButton(
                "Generate PDF Report",
                icon="picture_as_pdf",
                on_click=lambda e: self._generate_report(),
                width=200,
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    
    def _build_navigation_buttons(self):
        """Build next/previous navigation buttons"""
        buttons = []
        
        if self.current_step > 0:
            buttons.append(ft.ElevatedButton("Previous", on_click=lambda e: self._previous_step()))
        
        if self.current_step < len(self.steps) - 1:
            buttons.append(ft.ElevatedButton("Next", on_click=lambda e: self._next_step()))
        
        buttons.append(ft.TextButton("Save Draft", on_click=lambda e: self._save_draft()))
        
        return ft.Container(
            content=ft.Row(buttons, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10,
        )
    
    def _update_field(self, field, value):
        """Update report data field"""
        self.report_data[field] = value
    
    def _add_issue_dialog(self):
        """Dialog to add new issue"""
        def add_issue(e):
            issue = {
                'title': title_field.value,
                'description': desc_field.value,
                'severity': severity_field.value or "Medium",
                'photo_path': None
            }
            self.report_data['issues'].append(issue)
            dialog.open = False
            self.app.page.update()
        
        title_field = ft.TextField(label="Issue Title")
        desc_field = ft.TextField(label="Description", multiline=True, min_lines=3)
        severity_field = ft.Dropdown(
            label="Severity",
            options=[ft.dropdown.Option(x) for x in ["Low", "Medium", "High"]],
            value="Medium"
        )
        
        def close_dialog(e):
            dialog.open = False
            self.app.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Add Issue"),
            content=ft.Column([title_field, desc_field, severity_field]),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.ElevatedButton("Add", on_click=add_issue),
            ],
        )
        
        self.app.page.dialog = dialog
        dialog.open = True
        self.app.page.update()
    
    def _add_photo(self):
        """Add photo using file picker"""
        try:
            def on_result(e: ft.FilePickerResultEvent):
                if e.files:
                    self.report_data['photos'].extend([f.path for f in e.files])
                    self.app.page.update()
            
            # Initialize picker only once
            if self.photo_picker is None:
                self.photo_picker = ft.FilePicker(on_result=on_result)
                self.app.page.overlay.append(self.photo_picker)
            
            self.photo_picker.pick_files(allow_multiple=True, allowed_extensions=["jpg", "jpeg", "png"])
        except Exception as ex:
            self._show_error(f"Error: {str(ex)}")
    
    def _save_draft(self):
        """Save current report as draft"""
        try:
            self.app.save_draft(self.report_data)
            self.app.page.snack_bar = ft.SnackBar(ft.Text("Draft saved!"))
            self.app.page.snack_bar.open = True
            self.app.page.update()
        except Exception as ex:
            self._show_error(f"Save error: {str(ex)}")
    
    def _generate_report(self):
        """Generate final PDF report"""
        try:
            if not self.report_data.get('project_name'):
                self._show_error("Please enter project name")
                return
            
            if not self.report_data.get('id'):
                self.report_data['id'] = self.app.report_service.create_report(self.report_data)
            
            pdf_path = self.app.report_service.complete_report(self.report_data['id'], self.report_data)
            
            self.app.page.snack_bar = ft.SnackBar(ft.Text(f"Report saved to: {pdf_path}"))
            self.app.page.snack_bar.open = True
            self.app.navigate_to("/")
        except Exception as ex:
            self._show_error(f"Error: {str(ex)}")
        
        self.app.page.update()
    
    def _next_step(self):
        """Go to next step"""
        if self.current_step == 0 and not self.report_data.get('project_name'):
            self._show_error("Please enter project name")
            return
        self.current_step = min(self.current_step + 1, len(self.steps) - 1)
        # Rebuild the view to refresh all content
        self.app.page.views[-1] = self.build()
        self.app.page.update()
    
    def _previous_step(self):
        """Go to previous step"""
        self.current_step = max(self.current_step - 1, 0)
        # Rebuild the view to refresh all content
        self.app.page.views[-1] = self.build()
        self.app.page.update()
    
    def _save_project(self):
        """Save project to database"""
        if self.report_data.get('project_name'):
            self.app.db.add_project(self.report_data['project_name'])
            self._show_error("Project saved!")
    
    def _go_back(self):
        """Go back to home"""
        self.app.navigate_to("/")
    
    def _show_error(self, message):
        """Show error message"""
        self.app.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.app.page.snack_bar.open = True
        self.app.page.update()
