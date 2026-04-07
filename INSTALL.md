# Installation & Deployment Guide

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 512MB (1GB recommended)
- **Storage**: 100MB for application + database
- **Disk Space for Photos**: Depends on usage

## Installation Steps

### Windows

#### 1. Install Python
- Download from https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation
- Verify installation:
  ```bash
  python --version
  ```

#### 2. Create Project Directory
```bash
mkdir field_report_generator
cd field_report_generator
```

#### 3. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Run the Application
```bash
python main.py
```

### macOS

#### 1. Install Python
- Using Homebrew (recommended):
  ```bash
  brew install python@3.11
  ```
- Or download from https://www.python.org/downloads/

#### 2. Create Project Directory
```bash
mkdir field_report_generator
cd field_report_generator
```

#### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Run the Application
```bash
python main.py
```

### Linux (Ubuntu/Debian)

#### 1. Install Python and pip
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

#### 2. Create Project Directory
```bash
mkdir field_report_generator
cd field_report_generator
```

#### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Run the Application
```bash
python main.py
```

## Dependency Details

The `requirements.txt` includes:

```
flet==0.21.2              # Cross-platform UI framework
python-docx==1.1.0        # DOCX document generation
Pillow==10.1.0            # Image processing
reportlab==4.0.7          # PDF generation
```

### Installing Individual Packages
If you need to install packages separately:
```bash
pip install flet==0.21.2
pip install python-docx==1.1.0
pip install Pillow==10.1.0
pip install reportlab==4.0.7
```

## Mobile Deployment

### Android (APK)

#### Prerequisites
- Android SDK or Android Studio
- Java Development Kit (JDK)

#### Build Command
```bash
flet build apk
```

#### Installation on Device
1. Enable "Unknown sources" in Android settings
2. Transfer APK to device
3. Tap to install
4. Launch app from app drawer

#### Publishing to Play Store
1. Create Play Store developer account
2. Sign APK with your key
3. Follow Google Play submission guidelines

### iOS (IPA)

#### Prerequisites
- macOS with Xcode
- Apple Developer account
- iOS device or simulator

#### Build Command
```bash
flet build ipa
```

#### Installation
1. Using TestFlight for beta distribution
2. Or direct installation on provisioned devices
3. Publish via App Store

## Desktop Packaging

### Windows EXE

```bash
flet build windows
```

Output: Standalone `.exe` executable in `build/` directory

### macOS APP

```bash
flet build macos
```

Output: `.app` bundle ready for distribution

### Linux

```bash
flet build linux
```

Output: Standalone executable and `.snap` package option

## Environment Configuration

### Virtual Environment Best Practices

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# To deactivate:
deactivate

# Export requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Production Deployment

For team/enterprise deployment:

1. **Create `.env` file** (optional):
   ```
   DATABASE_PATH=./field_reports.db
   REPORTS_DIR=./reports
   TEMPLATE_DIR=./templates
   ```

2. **Configure database path** in `src/storage/database.py`:
   ```python
   self.db_path = os.getenv('DATABASE_PATH', 'field_reports.db')
   ```

3. **Set permissions**:
   ```bash
   chmod 755 field_report_generator/
   chmod 644 field_report_generator/*.py
   ```

## Running as Service

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every morning at 8 AM)
4. Set action:
   - Program: `python.exe`
   - Arguments: `C:\path\to\main.py`
5. Enable "Run with highest privileges"

### macOS/Linux (systemd)

Create `/etc/systemd/system/field-report.service`:
```ini
[Unit]
Description=Field Report Generator
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/field_report_generator
ExecStart=/usr/bin/python3 /path/to/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable field-report
sudo systemctl start field-report
```

## Troubleshooting Installation

### Python Not Found
- Ensure Python is in system PATH
- Restart terminal after installation
- On macOS, use `python3` instead of `python`

### Permission Denied
```bash
# Fix permissions on macOS/Linux
chmod +x main.py
sudo chown -R $USER:$USER .
```

### Pip Install Fails
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear cache
pip cache purge

# Retry installation
pip install -r requirements.txt
```

### Flet Import Error
```bash
# Reinstall Flet with dependencies
pip install --upgrade flet

# Or specific version
pip install flet==0.21.2 --force-reinstall
```

### Database Lock Error
- Ensure only one instance of app is running
- Check for zombie Python processes:
  ```bash
  ps aux | grep python  # macOS/Linux
  tasklist | grep python  # Windows
  ```
- Kill if needed:
  ```bash
  pkill -f main.py  # macOS/Linux
  ```

## Updating the Application

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update to Latest Flet
```bash
pip install --upgrade flet
```

### Rollback to Previous Version
```bash
pip install flet==0.21.2
```

## Uninstallation

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Remove Application Data
```bash
# WARNING: This deletes all reports!
rm field_reports.db
rm -rf reports/
```

### Remove All Dependencies
```bash
pip uninstall -r requirements.txt -y
```

## Performance Optimization

### For Large Datasets

1. **Database Indexing** - Already configured in `database.py`
2. **Lazy Loading** - Photo grids load on-demand
3. **Query Optimization** - Analytics use aggregated queries

### Memory Usage

- Close unused browser tabs
- Limit photos to < 5MB each
- Clear old data periodically via Settings

### Disk Space

Monitor with:
```bash
du -sh reports/  # macOS/Linux
dir /s reports\  # Windows
```

Archive old reports:
```bash
# Create archive
tar -czf reports_backup_2024.tar.gz reports/

# Move to external storage
mv reports_backup_2024.tar.gz /external/drive/
```

## Backup & Recovery

### Backup Database
```bash
# Copy database file
cp field_reports.db field_reports.backup.db

# Or with timestamp
cp field_reports.db field_reports.backup_$(date +%Y%m%d).db
```

### Backup Reports
```bash
# Archive reports folder
tar -czf reports_backup.tar.gz reports/

# Store in cloud or external drive
```

### Recovery from Backup
```bash
# Restore database
cp field_reports.backup.db field_reports.db

# Restore reports
tar -xzf reports_backup.tar.gz
```

## Security Considerations

### File Permissions
```bash
# Secure database
chmod 600 field_reports.db

# Restrict directory access
chmod 700 reports/
chmod 700 .env
```

### Sensitive Data
- Database contains local reports only
- No cloud synchronization by default
- Consider encryption for highly sensitive data
- Use OS-level file encryption for added security

## Deployment Checklist

- [ ] Python 3.8+ installed and verified
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Application runs without errors
- [ ] Database initializes with default template
- [ ] First report can be created and saved
- [ ] PDF generation works correctly
- [ ] Settings/template customization works
- [ ] Analytics display correctly
- [ ] Backups are scheduled (optional)

## Support

For installation issues:
1. Check Python version: `python --version`
2. Verify pip installation: `pip --version`
3. Check virtual environment: `which python` or `where python`
4. Review dependency versions: `pip list`
5. Check system logs for errors

---

**Deployed Successfully?** Check [QUICKSTART.md](QUICKSTART.md) for first-time usage or [README.md](README.md) for full documentation.
