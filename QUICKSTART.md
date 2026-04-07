# Field Report Generator - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Python Requirements
```bash
cd field_report_generator
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

The app will launch in a new window. You're ready to go!

## 📱 First-Time Usage

### Creating Your First Report

1. **Home Screen** - Review your dashboard
   - "New Report" button at the top
   - Stats showing drafts and completed reports
   - Recent reports and drafts listed

2. **Step 1: Basic Information**
   - Enter Project Name (required)
   - Enter Site Location
   - Date is auto-filled with today's date
   - Select Report Type from dropdown
   - Click "Next" to proceed

3. **Step 2: Site Inspection Checklist**
   - Review each checklist item
   - Toggle "OK" or "Issue" for each item
   - If you mark "Issue", a dialog appears to log it
   - Click "Next" to proceed

4. **Step 3: Issues**
   - View all issues added from checklist
   - Click "+" icon to add custom issues
   - Fill in Title, Description, and Severity
   - Delete issues by clicking the trash icon
   - Click "Next" to proceed

5. **Step 4: photos**
   - Click "Add Photo" button
   - Select images from your device (JPG, PNG, HEIC)
   - Photos display in a grid
   - Remove photos by clicking the X button
   - Click "Next" to proceed

6. **Step 5: Generate Report**
   - Review report summary
   - Click "Generate PDF Report" to create the report
   - Report saves to `reports/` directory
   - You're done! Click "Home" to start another report

### Saving as Draft

At any point during report creation:
- Click "Save Draft" button at the bottom
- Your progress is saved automatically
- Resume editing from the home screen

## 📊 Viewing Analytics

1. Click "Analytics" in the bottom navigation
2. View key metrics:
   - Total Reports count
   - Total Issues count
3. Charts show:
   - Reports by project
   - Issues by severity
   - Reports over the past 7 days

## ⚙️ Customizing Templates

1. Click "Settings" in bottom navigation
2. Scroll to "Report Template" section
3. Edit the template using placeholders:
   - `{{project_name}}` - Project name
   - `{{date}}` - Report date
   - `{{location}}` - Site location
   - `{{#issues}}...{{/issues}}` - Issue loop
   - `{{#photos}}...{{/photos}}` - Photo loop

4. Click "Save Template" to apply changes
5. All future reports use your custom template

## 💾 Managing Your Data

### View All Reports
- **Home** - See recent reports and drafts
- **Analytics** - See statistics and trends

### Find Specific Reports
- Reports are stored in SQLite database: `field_reports.db`
- Generated PDFs are in `reports/` folder
- Open any PDF in your document viewer

### Clear or Export Data
- Go to **Settings** → "Data Management"
- "Clear All Data" removes all reports (⚠️ use with caution)
- "Export All Reports" feature coming soon

## 🎯 Pro Tips

1. **Quick Issue from Checklist**
   - Toggle "Issue" on checklist items to auto-create
   - Fastest way to log problems on-site

2. **Save Drafts Often**
   - Click "Save Draft" frequently
   - You can edit drafts anytime from home screen

3. **Multiple Photos**
   - Add photos from the gallery or camera
   - Take multiple photos per location
   - They all embed in the final PDF

4. **Custom Templates**
   - Create templates matching your company format
   - Use consistent templates across teams
   - Available on all future reports

5. **Severity Levels**
   - Low: Minor findings, cosmetic issues
   - Medium: Should address soon, operational impact
   - High: Critical, address immediately, safety concerns

## 📖 Common Workflows

### Field Project Inspection
1. Start new report when arriving at site
2. Go through checklist
3. Log any issues with photos
4. Add additional photos of key areas
5. Generate PDF for client handoff

### Maintenance Audit
1. Create report for facility/equipment
2. Complete checklist against maintenance items
3. Add before/after photos
4. Note any repairs needed
5. Generate report for records

### Safety Audit
1. New report for site/facility
2. Complete safety checklist
3. Log any violations in Issues
4. Attach proof photos
5. Generate report for compliance

## 🔧 Troubleshooting

### App Won't Start
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Then try again
python main.py
```

### Can't Find My Photos
- Photos must be selected from your device
- They're not downloaded, just linked
- If original file is deleted, photo won't show in PDF

### Report PDF Looks Wrong
- Check your template for proper placeholders
- Ensure you're using `{{}}` syntax correctly
- View default template for reference

### Database Corrupted
1. Close the app
2. Delete `field_reports.db` file
3. Restart the app
4. Database recreates automatically with default template

## 📞 Need Help?

- Check the full **README.md** for detailed documentation
- Review inline code comments for implementation details
- Ensure Python 3.8+ is installed
- Verify all dependencies: `pip list | grep -E "flet|docx|pillow|reportlab"`

## 🎓 Next Steps

1. ✅ Run the app and create your first report
2. ✅ Customize the template for your use case
3. ✅ Try all three screens (Home, Analytics, Settings)
4. ✅ Generate a PDF and review the output
5. ✅ Start using for real reports!

---

**Questions?** Review the comments in `src/` files or check the full README.md for complete API documentation.
