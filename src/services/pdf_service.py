import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image as RLImage
)
from reportlab.lib import colors
from PIL import Image as PILImage
from config import REPORTS_DIR
from logger import setup_logger
from src.utils.exceptions import PDFGenerationError
from src.utils.validators import validate_report_data

logger = setup_logger(__name__)

class PDFService:
    """Service for PDF generation with error handling"""
    
    def __init__(self, output_dir: str = str(REPORTS_DIR)):
        """Initialize PDF service"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("PDFService initialized")
    
    def generate_report_pdf(self, report_data: dict) -> str:
        """
        Generate PDF report from report data
        
        Args:
            report_data: Report dictionary
        
        Returns:
            Path to generated PDF
        
        Raises:
            PDFGenerationError: If generation fails
        """
        try:
            # Validate report data
            is_valid, errors = validate_report_data(report_data)
            if not is_valid:
                raise PDFGenerationError(f"Invalid report data: {'; '.join(errors)}")
            
            filename = f"report_{report_data.get('id', 'draft')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = self.output_dir / filename
            
            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#0052CC'),
                spaceAfter=30,
                alignment=1,
            )
            story.append(Paragraph("Site Inspection Report", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Add report info
            story.append(self._build_report_info_table(report_data, styles))
            story.append(Spacer(1, 0.3*inch))
            
            # Add issues section
            if report_data.get('issues'):
                story.append(self._build_issues_section(report_data, styles))
                story.append(Spacer(1, 0.3*inch))
            
            # Add notes section
            if report_data.get('notes'):
                story.append(Paragraph("Notes", styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(report_data.get('notes', ''), styles['BodyText']))
                story.append(Spacer(1, 0.3*inch))
            
            # Add footer
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
            logger.info(f"PDF generated: {filepath}")
            return str(filepath)
        except PDFGenerationError:
            raise
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise PDFGenerationError(f"Failed to generate PDF: {e}")
    
    def _build_report_info_table(self, report_data: dict, styles) -> Table:
        """Build report information table"""
        info_data = [
            ['Project:', report_data.get('project_name', 'N/A')],
            ['Location:', report_data.get('location', 'N/A')],
            ['Date:', report_data.get('date', 'N/A')],
            ['Type:', report_data.get('report_type', 'N/A')],
            ['Status:', report_data.get('status', 'draft').upper()],
        ]
        
        table = Table(info_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8EEF9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        return table
    
    def _build_issues_section(self, report_data: dict, styles) -> Table:
        """Build issues section"""
        issues = report_data.get('issues', [])
        
        if not issues:
            return Paragraph("No issues found", styles['Normal'])
        
        issues_data = [['#', 'Issue', 'Severity', 'Status']]
        for i, issue in enumerate(issues, 1):
            issues_data.append([
                str(i),
                issue.get('title', 'N/A')[:50],
                issue.get('severity', 'N/A'),
                issue.get('status', 'open'),
            ])
        
        table = Table(issues_data, colWidths=[0.5*inch, 3*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
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
        
        section = [Paragraph("Issues Found", styles['Heading2']), Spacer(1, 0.1*inch), table]
        return section[2]  # Return just the table
    
    def optimize_image(self, image_path: str, max_width: int = 800) -> str:
        """Optimize image for PDF"""
        try:
            img = PILImage.open(image_path)
            
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), PILImage.Resampling.LANCZOS)
            
            base, ext = os.path.splitext(image_path)
            optimized_path = f"{base}_optimized{ext}"
            img.save(optimized_path, quality=85)
            
            return optimized_path
        except Exception as e:
            logger.error(f"Error optimizing image: {e}")
            raise PDFGenerationError(f"Failed to optimize image: {e}")