"""
PDF service - generate PDF reports
"""

import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from PIL import Image as PILImage

class PDFService:
    """Service for PDF generation"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_report_pdf(self, report_data: dict) -> str:
        """Generate PDF report from report data"""
        filename = f"report_{report_data.get('id', 'draft')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0052CC'),
            spaceAfter=30,
            alignment=1,
        )
        story.append(Paragraph("Site Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Report Info
        info_data = [
            ['Project:', report_data.get('project_name', 'N/A')],
            ['Location:', report_data.get('location', 'N/A')],
            ['Date:', report_data.get('date', 'N/A')],
            ['Type:', report_data.get('report_type', 'N/A')],
            ['Status:', report_data.get('status', 'draft').upper()],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8EEF9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Issues Section
        issues = report_data.get('issues', [])
        if issues:
            story.append(Paragraph("Issues Found", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            issues_data = [['#', 'Issue', 'Severity', 'Status']]
            for i, issue in enumerate(issues, 1):
                issues_data.append([
                    str(i),
                    issue.get('title', 'N/A'),
                    issue.get('severity', 'N/A'),
                    issue.get('status', 'open'),
                ])
            
            issues_table = Table(issues_data, colWidths=[0.5*inch, 3*inch, 1*inch, 1*inch])
            issues_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0052CC')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            story.append(issues_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Notes Section
        if report_data.get('notes'):
            story.append(Paragraph("Notes", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(report_data.get('notes', ''), styles['BodyText']))
            story.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1,
        )))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_project_summary_pdf(self, reports: list) -> str:
        """Generate summary PDF for multiple reports"""
        filename = f"project_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        story.append(Paragraph("Project Summary Report", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Summary Table
        summary_data = [['Project', 'Location', 'Reports', 'Issues']]
        projects = {}
        
        for report in reports:
            project_name = report.get('project_name', 'Unknown')
            if project_name not in projects:
                projects[project_name] = {'location': report.get('location'), 'count': 0, 'issues': 0}
            projects[project_name]['count'] += 1
            projects[project_name]['issues'] += len(report.get('issues', []))
        
        for project, data in projects.items():
            summary_data.append([
                project,
                data['location'],
                str(data['count']),
                str(data['issues']),
            ])
        
        if len(summary_data) > 1:
            summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0052CC')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            story.append(summary_table)
        
        doc.build(story)
        return filepath
    
    def optimize_image(self, image_path: str, max_width: int = 800) -> str:
        """Optimize image for PDF"""
        try:
            img = PILImage.open(image_path)
            
            # Resize if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), PILImage.Resampling.LANCZOS)
            
            # Save optimized version
            base, ext = os.path.splitext(image_path)
            optimized_path = f"{base}_optimized{ext}"
            img.save(optimized_path, quality=85)
            
            return optimized_path
        except Exception as e:
            print(f"Error optimizing image: {e}")
            return image_path
    
    def apply_template(self, template: str, data: dict) -> str:
        """Apply data to template string"""
        output = template
        for key, value in data.items():
            if isinstance(value, list):
                continue
            output = output.replace(f"{{{{{key}}}}}", str(value))
        return output
    
    def generate_pdf(self, report_data: dict) -> str:
        """Quick PDF generation (MVP version)"""
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            
            elements.append(Paragraph("Field Report", styles["Title"]))
            elements.append(Spacer(1, 12))
            
            elements.append(Paragraph(f"Project: {report_data.get('project_name', 'N/A')}", styles["Normal"]))
            elements.append(Paragraph(f"Date: {report_data.get('date', 'N/A')}", styles["Normal"]))
            elements.append(Paragraph(f"Location: {report_data.get('location', 'N/A')}", styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            elements.append(Paragraph("Issues:", styles["Heading2"]))
            for issue in report_data.get("issues", []):
                elements.append(Paragraph(f"- {issue.get('title', 'N/A')} ({issue.get('severity', 'N/A')})", styles["Normal"]))
                elements.append(Paragraph(issue.get('description', ''), styles["Normal"]))
                elements.append(Spacer(1, 8))
            
            if report_data.get('notes'):
                elements.append(Spacer(1, 12))
                elements.append(Paragraph("Notes:", styles["Heading2"]))
                elements.append(Paragraph(report_data.get('notes', ''), styles["Normal"]))
            
            doc.build(elements)
            return filepath
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
