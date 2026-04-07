# Field Report Generator

A mobile-first application for engineers and inspectors to create professional field reports on-site in under 60 seconds.

## Features

- 📱 **Mobile-First UI** - Designed for on-site use with large buttons and minimal typing
- 📸 **Photo Integration** - Capture and attach photos to reports
- 📋 **Dynamic Checklist** - Configurable inspection checklists
- 📄 **Custom Templates** - Create your own report templates with placeholders
- 💾 **Draft System** - Auto-save reports as drafts for later completion
- 📊 **Analytics Dashboard** - Track reports, issues, and trends
- 🔄 **Multi-format Export** - Generate both DOCX and PDF reports
- 🗄️ **SQLite Database** - Persistent local storage with full report history

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or create the project directory**:
```bash
cd field_report_generator
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python main.py
```

The application will open in a new window. For mobile deployment, see the Deployment section below.

## Usage

### Creating a Report

1. Click the **"New Report"** button on the home screen
2. **Step 1 - Basic Info**: Fill in project name, location, and report type
3. **Step 2 - Checklist**: Check off inspection items; any issues trigger issue creation
4. **Step 3 - Issues**: Add detailed issues with severity levels and notes
5. **Step 4 - Photos**: Attach multiple photos from your device
6. **Step 5 - Generate**: Review summary and generate PDF report

### Template Customization

Use the **Settings** screen to customize your report template with placeholders:

**Available Placeholders:**
- `{{project_name}}` - Project name
- `{{date}}` - Report date
- `{{location}}` - Site location
- `{{report_type}}` - Type of report
- `{{#issues}}...{{/issues}}` - Loop through issues (use {{title}}, {{description}}, {{severity}})
- `{{#photos}}...{{/photos}}` - Loop through photos
- `{{generated_date}}` - Report generation timestamp

**Example Template:**
```
FIELD INSPECTION REPORT
=========================

Project: {{project_name}}
Date: {{date}}
Location: {{location}}
Report Type: {{report_type}}

ISSUES FOUND:
{{#issues}}
• {{title}} (Severity: {{severity}})
  Description: {{description}}
{{/issues}}

PHOTOS:
{{#photos}}
- {{photo}}
{{/photos}}

Report Generated: {{generated_date}}
```

### Managing Reports

- **Drafts** - Automatically saved and accessible from home screen; can be edited anytime
- **Completed Reports** - Final PDF reports stored in the `reports/` directory
- **Analytics** - View stats on total reports, issues by severity, and trends over time
- **Export** - Export reports as PDF or DOCX format (from Settings)

### Database Operations

All reports are stored in SQLite database (`field_reports.db`). The database includes:
- **Reports table** - Project info, dates, status
- **Issues table** - Issue details linked to reports
- **Templates table** - Custom report templates
- **Projects table** - Cached project names for quick selection

## Project Structure

```
field_report_generator/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── field_reports.db            # SQLite database (created on first run)
├── assets/                     # Static assets
├── reports/                    # Generated PDF/DOCX reports
└── src/
    ├── __init__.py
    ├── main_app.py             # Application controller
    ├── models/                 # Data models
    │   ├── __init__.py
    │   ├── report.py           # Report data model
    │   ├── issue.py            # Issue data model
    │   └── template.py         # Template data model
    ├── ui/                     # UI screens
    │   ├── __init__.py
    │   ├── home_screen.py      # Dashboard
    │   ├── report_creation.py  # Report wizard
    │   ├── analytics_screen.py # Analytics dashboard
    │   └── settings_screen.py  # Template & config settings
    ├── components/             # Reusable UI components
    │   ├── __init__.py
    │   ├── report_card.py      # Report card widget
    │   ├── issue_card.py       # Issue card widget
    │   └── photo_grid.py       # Photo grid widget
    ├── services/               # Business logic
    │   ├── __init__.py
    │   ├── report_service.py   # Report CRUD & operations
    │   ├── template_service.py # Template management
    │   └── pdf_service.py      # PDF/DOCX generation
    └── storage/                # Data persistence
        ├── __init__.py
        ├── database.py         # SQLite operations
        └── file_storage.py     # File management
```

## Key Components

### Database Layer (`src/storage/database.py`)
- Handles all SQLite operations
- Manages reports, issues, templates, and projects
- Provides analytics data aggregation

### Report Service (`src/services/report_service.py`)
- Business logic for report CRUD operations
- Draft management
- Issue and photo operations
- Report completion and PDF generation

### PDF Service (`src/services/pdf_service.py`)
- Template parsing with placeholder replacement
- PDF generation using ReportLab
- DOCX generation using python-docx
- Image embedding in reports

### UI Screens
- **HomeScreen** - Dashboard with stats and recent reports
- **ReportCreationScreen** - 5-step wizard for creating reports
- **AnalyticsScreen** - Charts and statistics
- **SettingsScreen** - Template customization and data management

## Technologies Used

- **Flet** (0.21.2) - Cross-platform UI framework
- **SQLite3** - Lightweight database
- **python-docx** (1.1.0) - DOCX document generation
- **reportlab** (4.0.7) - PDF generation
- **Pillow** (10.1.0) - Image processing
- **Python** (3.8+)

## API Reference

### FieldReportApp
```python
navigate_to(route: str)              # Navigate to route
save_draft(report_data: dict)        # Save draft report
get_drafts() -> List[Dict]           # Get all drafts
get_completed_reports() -> List[Dict] # Get completed reports
```

### Database
```python
save_report(report_data: Dict) -> int        # Save new report
update_report(report_id: int, data: Dict)   # Update existing report
get_reports(status: str) -> List[Dict]      # Get reports by status
get_analytics_data() -> Dict                 # Get analytics data
get_template() -> Dict                       # Get active template
save_template(name: str, content: str)      # Save new template
```

### ReportService
```python
create_report(report_data: Dict) -> int          # Create report
save_draft(report_data: Dict)                   # Save as draft
get_drafts() -> List[Dict]                      # Get drafts
get_completed_reports() -> List[Dict]           # Get completed reports
complete_report(report_id: int, data: Dict)     # Complete & generate PDF
add_issue(report_data: Dict, issue: Dict)       # Add issue
add_photo(report_data: Dict, photo_path: str)   # Add photo
```

## Development Notes

### Running in Development Mode
```bash
flet run main.py
```
This enables hot-reload for quick iteration.

### Building for Mobile

**Android APK:**
```bash
flet build apk
```

**iOS IPA:**
```bash
flet build ipa
```

### Adding New Report Types
1. Edit the dropdown in `src/ui/report_creation.py` (`_build_basic_info_step`)
2. Add new checklist items as needed
3. Types automatically populate in issue severity

### Customizing Severity Levels
Edit `src/ui/report_creation.py` and `src/ui/analytics_screen.py` to modify severity color coding and options.

## Troubleshooting

### Database Issues
- **Reset database**: Delete `field_reports.db` and restart the app
- **Corrupted database**: The app will recreate tables automatically

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### File Not Found Errors
- Ensure photos are accessible (not deleted after report creation)
- Check file permissions in the `reports/` directory

### PDF Generation Fails
- Verify ReportLab and Pillow are properly installed
- Check that image files exist and are readable
- Try without images first to isolate the issue

## Performance Optimization

- Reports are indexed by date for faster queries
- Drafts load asynchronously on the home screen
- Analytics use aggregated queries for efficiency
- Photo grid uses lazy loading for large photo counts

## Security Considerations

- All data stored locally in SQLite (no cloud sync)
- No authentication required (assumes trusted device)
- File paths stored as absolute; ensure proper cleanup
- Consider encrypting database for sensitive projects

## License

MIT License - See LICENSE file for details

## Support & Contributing

For issues, feature requests, or contributions:
1. Check existing issues
2. Provide detailed bug descriptions
3. Include Python version and OS information
4. Submit pull requests with clear descriptions

## Changelog

### v1.0 (Initial Release)
- ✅ Complete report creation flow
- ✅ Camera/photo integration
- ✅ Dynamic issue management
- ✅ Custom template system
- ✅ Draft auto-save
- ✅ Analytics dashboard
- ✅ PDF/DOCX generation
- ✅ SQLite persistence

## Roadmap

- [ ] Cloud synchronization
- [ ] Report templates library
- [ ] OCR for receipt/document capture
- [ ] Voice notes attachment
- [ ] Multi-user support
- [ ] Offline mode enhancements
- [ ] Advanced filtering and search

---

**Questions?** Check the README.md in the project root or review the code comments for detailed explanations.
