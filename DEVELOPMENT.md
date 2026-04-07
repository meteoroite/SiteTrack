# Development Guide & Architecture

## Project Architecture

### Layers

```
┌─────────────────────────────┐
│   Presentation Layer (UI)   │  Flet components
├─────────────────────────────┤
│   Business Logic Layer      │  Services
├─────────────────────────────┤
│   Data Model Layer          │  Models
├─────────────────────────────┤
│   Persistence Layer         │  Database/Storage
└─────────────────────────────┘
```

## Module Overview

### Entry Point: `main.py`
- Application launcher
- Initializes Flet framework
- Entry point for all platforms

### Core Application: `src/main_app.py`
- **FieldReportApp** class - Main controller
- Route management
- Global state handling
- Service initialization

#### Key Methods:
```python
setup_routes(page)        # Configure navigation
navigate_to(route)        # Route navigation
save_draft(report_data)   # Draft saving
get_drafts()              # Retrieve drafts
get_completed_reports()   # Retrieve completed reports
```

## Models Layer: `src/models/`

### Report Model
```python
Report(
    id: Optional[int]
    project_name: str
    location: str
    date: str
    report_type: str
    issues: List[Issue]
    photos: List[str]
    status: str ('draft' or 'completed')
    created_at: str (ISO format)
    updated_at: str (ISO format)
)
```

### Issue Model
```python
Issue(
    id: Optional[int]
    title: str
    description: str
    severity: str ('Low', 'Medium', 'High')
    photo_path: Optional[str]
    report_id: Optional[int]
)
```

### Template Model
```python
Template(
    id: Optional[int]
    name: str
    content: str
    is_active: bool
    created_at: str
)
```

## Services Layer: `src/services/`

### ReportService
Handles all report-related business logic:

```python
create_report(report_data)           # Create new report
save_draft(report_data)              # Save as draft
get_drafts()                         # Retrieve drafts
get_completed_reports()              # Retrieve completed
complete_report(report_id, data)     # Finalize & generate PDF
add_issue(report_data, issue)        # Add issue to report
remove_issue(report_data, index)     # Remove issue
add_photo(report_data, photo_path)   # Add photo
```

### PDFService
Handles PDF and DOCX generation:

```python
parse_template(content, data)        # Replace placeholders
generate_pdf(report_data)            # Generate PDF report
generate_docx(report_data)           # Generate DOCX report
```

**Template Placeholders:**
- `{{project_name}}` - Project name
- `{{date}}` - Report date
- `{{location}}` - Site location
- `{{report_type}}` - Type of report
- `{{#issues}}...{{/issues}}` - Issue loop
- `{{#photos}}...{{/photos}}` - Photo loop
- `{{generated_date}}` - Generation timestamp

### TemplateService
Manages custom templates:

```python
get_active_template()                # Get current template
save_custom_template(name, content)  # Save new template
validate_template(content)           # Validate placeholders
```

## Storage Layer: `src/storage/`

### Database Class
SQLite database operations:

```python
# Report Operations
save_report(report_data) -> int      # Insert report
get_reports(status) -> List[Dict]    # Query reports
update_report(report_id, data)       # Update report

# Template Operations
get_template() -> Dict               # Get active template
save_template(name, content)         # Save & activate

# Project Operations
get_projects() -> List[str]          # Get project list
add_project(project_name)            # Add to project list

# Analytics Operations
get_analytics_data() -> Dict         # Aggregate statistics
```

**Database Schema:**

```sql
-- Reports Table
reports (
    id INTEGER PRIMARY KEY,
    project_name TEXT,
    location TEXT,
    date TEXT,
    report_type TEXT,
    status TEXT,
    photos TEXT (JSON),
    created_at TEXT,
    updated_at TEXT
)

-- Issues Table
issues (
    id INTEGER PRIMARY KEY,
    report_id INTEGER FOREIGN KEY,
    title TEXT,
    description TEXT,
    severity TEXT,
    photo_path TEXT
)

-- Templates Table
templates (
    id INTEGER PRIMARY KEY,
    name TEXT,
    content TEXT,
    is_active INTEGER,
    created_at TEXT
)

-- Projects Table
projects (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    created_at TEXT
)
```

### FileStorage Class
Manages file operations:

```python
save_file(source_path, subfolder) -> str  # Copy & store file
delete_file(file_path)                    # Delete file
get_reports_dir() -> str                  # Get reports directory
```

## UI Layer: `src/ui/`

### HomeScreen (`home_screen.py`)
**Features:**
- Dashboard with stats cards (drafts, completed reports)
- Recent drafts list with edit capability
- Recent completed reports
- Bottom navigation bar
- New Report button

**Key Methods:**
```python
_build_stat_card()           # Statistics card widget
_build_draft_list()          # Draft reports list
_build_recent_reports()      # Completed reports list
_build_navigation_bar()      # Bottom navigation
_handle_navigation()         # Navigation handler
```

### ReportCreationScreen (`report_creation.py`)
**5-Step Wizard:**

1. **Basic Info** - Project details form
2. **Checklist** - Dynamic site inspection checklist
3. **Issues** - Issue management with CRUD
4. **Photos** - Photo grid management
5. **Generate** - Summary and PDF generation

**Key Methods:**
```python
_build_progress_indicator()      # Step progress display
_get_step_content()              # Get current step UI
_next_step() / _previous_step()  # Step navigation
_add_issue_dialog()              # Issue creation dialog
_add_photo()                     # File picker for photos
_generate_report()               # PDF generation trigger
```

### AnalyticsScreen (`analytics_screen.py`)
**Analytics Features:**
- Total reports and issues count
- Reports by project (bar chart)
- Issues by severity (bar chart)
- Reports timeline (last 7 days)

**Key Methods:**
```python
_build_metric_card()             # Metric card widget
_build_reports_by_project_chart() # Project chart
_build_severity_chart()          # Severity distribution
_build_timeline_chart()          # Timeline chart
```

### SettingsScreen (`settings_screen.py`)
**Settings Features:**
- Custom template editor
- Template validation
- Data management (clear all, export)
- About section

**Key Methods:**
```python
_save_template()                 # Save custom template
_confirm_clear_data()            # Clear data confirmation
_export_reports()                # Export functionality
```

## Components Layer: `src/components/`

### ReportCard
Reusable card component for report display:
```python
ReportCard(report, on_click=None)  # Report list item
```

### IssueCard
Reusable card component for issue display:
```python
IssueCard(issue, on_delete=None)   # Issue list item
```

### PhotoGrid
Reusable grid component for photo display:
```python
PhotoGrid(photos, on_delete=None)  # Photo gallery
```

## Data Flow

### Creating a Report

```
HomeScreen
    ↓
ReportCreationScreen (Step 1-5)
    ↓
ReportService.create_report()
    ↓
Database.save_report()
    ↓
SQLite Insert (reports + issues tables)
    ↓
PDF Generation (PDFService)
    ↓
Report saved in reports/ directory
    ↓
Return to HomeScreen
```

### Saving Draft

```
ReportCreationScreen
    ↓
ReportService.save_draft()
    ↓
Database.update_report() (or save_report if new)
    ↓
SQLite Insert/Update
    ↓
SnackBar notification
```

### Analytics Display

```
HomeScreen → Analytics Click
    ↓
AnalyticsScreen initialized
    ↓
Database.get_analytics_data()
    ↓
Aggregate SQL queries
    ↓
Charts rendered with data
```

## Development Conventions

### Naming Conventions
- **Classes**: PascalCase (e.g., `ReportService`, `HomeScreen`)
- **Functions/Methods**: snake_case (e.g., `save_draft`, `get_analytics_data`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DATABASE_PATH`)
- **Private methods**: Leading underscore (e.g., `_build_stat_card`)

### Code Structure
- One class per file (except components)
- Docstrings for all public methods
- Type hints for function parameters
- Comments for complex logic

### UI Patterns
- Container for styling/layout
- Column/Row for structure
- Theme colors: `ft.Colors.BLUE_700`, `ft.Colors.RED_700`, etc.
- Consistent padding: 10-20px
- Shadow for depth: `ft.BoxShadow(...)`

## Adding New Features

### Add a New Report Type

1. **Edit `report_creation.py`**:
   ```python
   # In _build_basic_info_step():
   ft.Dropdown(
       options=[
           ...,
           ft.dropdown.Option("Your New Type"),
       ]
   )
   ```

2. **Update database enum** (if hardcoding):
   - Add to dropdown options above

3. **Update templates** if needed:
   - Add logic in `pdf_service.py` if special formatting

### Add a New Checklist Item

1. **Edit `report_creation.py`**:
   ```python
   # In _build_checklist_step():
   checklist_items = [
       ...,
       "Your New Checklist Item",
   ]
   ```

### Add a New Analytics Chart

1. **Add data collection in `database.py`**:
   ```python
   # In get_analytics_data():
   new_metric = """SELECT ... FROM ..."""
   ```

2. **Build chart in `analytics_screen.py`**:
   ```python
   def _build_new_chart(self):
       data = self.analytics_data.get('new_metric', {})
       # Build chart visualization
   ```

3. **Add to layout**:
   ```python
   # In build():
   ft.Container(
       content=ft.Column([
           ft.Text("New Chart", size=18, weight=ft.FontWeight.BOLD),
           self._build_new_chart(),
       ]),
   )
   ```

### Add Database Field

1. **Update schema in `database.py`**:
   ```python
   # In init_database():
   cursor.execute("""
       ALTER TABLE reports ADD COLUMN new_field TEXT
   """)
   ```

2. **Update Report model** in `models/report.py`:
   ```python
   @dataclass
   class Report:
       ...
       new_field: Optional[str]
   ```

3. **Update CRUD operations** in `database.py`

## Testing

### Manual Testing Checklist
- [ ] App starts without errors
- [ ] Can create new report through all 5 steps
- [ ] Draft saves and resumes correctly
- [ ] PDF generates with all content
- [ ] Analytics load without errors
- [ ] Template can be customized
- [ ] Photos load correctly in grid
- [ ] Dropdowns populate from database
- [ ] Navigation works between all screens
- [ ] Home screen updates after new report

### Unit Testing (Future)
```python
# Example test structure
def test_report_creation():
    report_data = {
        'project_name': 'Test Project',
        'location': 'Test Location',
        ...
    }
    service = ReportService(db)
    report_id = service.create_report(report_data)
    assert report_id > 0
```

## Performance Tips

1. **Lazy Load Data**
   - Don't load all reports at startup
   - Load on-demand in screens

2. **Use Aggregated Queries**
   - Use SQL GROUP BY for analytics
   - Avoid loading all data into memory

3. **Cache Results**
   - Cache analytics data on screen load
   - Refresh on demand

4. **Image Optimization**
   - Compress images before saving
   - Limit photo size to 5MB

## Debugging

### Print Debug Info
```python
print(f"DEBUG: {variable_name} = {value}")
```

### Check Database State
```python
import sqlite3
conn = sqlite3.connect('field_reports.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM reports LIMIT 5")
print(cursor.fetchall())
```

### Monitor File Operations
```python
import os
print(f"Files in reports/: {os.listdir('reports/')}")
```

### Debug Flet Issues
```python
# Add to main_app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Common Issues & Solutions

### Issue: Database locks up
**Solution**: Close other instances, restart app

### Issue: PDF doesn't include images
**Solution**: Check image paths exist, verify Pillow installation

### Issue: Template not updating
**Solution**: Ensure template is marked active in database

### Issue: Reports not saving
**Solution**: Check database permissions, verify disk space

## Best Practices

1. **Always use transactions**
   ```python
   with sqlite3.connect(self.db_path) as conn:
       # Operations here
   ```

2. **Validate user input**
   ```python
   if not self.report_data.get('project_name'):
       self._show_error("Project name required")
       return
   ```

3. **Handle exceptions gracefully**
   ```python
   try:
       pdf_path = self.generate_pdf(report_data)
   except Exception as e:
       self._show_error(f"Error: {str(e)}")
   ```

4. **Use meaningful variable names**
   ```python
   # Good
   completed_reports_count = len(reports)
   
   # Avoid
   x = len(reports)
   ```

5. **Comment complex logic**
   ```python
   # This regex extracts placeholders from template content
   # Supports {{placeholder}} and {{#loop}}...{{/loop}} syntax
   pattern = r'{{.*?}}'
   ```

## Version History

### v1.0.0
- Initial release
- Core features implemented
- PDF/DOCX generation
- Analytics dashboard
- Template customization

### Planned v1.1.0
- Cloud sync (optional)
- Voice notes
- Advanced filtering
- Report templates library

## Contributing

To contribute:
1. Create feature branch
2. Make changes following conventions
3. Test thoroughly
4. Submit pull request with description

---

**Happy Coding!** Refer to inline comments in source code for implementation details.
