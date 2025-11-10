"""
Comprehensive PDF Test Document Generator
Creates a PDF from the comprehensive HTML using WeasyPrint
"""

import sys
from pathlib import Path

def create_comprehensive_pdf():
    """
    Create a comprehensive PDF file using ReportLab
    """
    try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
            
            print("Using ReportLab to generate PDF...")
            
            # Create PDF
            doc = SimpleDocTemplate(
                "test_comprehensive.pdf",
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for elements
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            # Title
            elements.append(Paragraph("Comprehensive PDF Test Document", title_style))
            elements.append(Spacer(1, 12))
            
            # Purpose
            elements.append(Paragraph("<b>Purpose:</b> Test all PDF elements for conversion quality", styles['Normal']))
            elements.append(Paragraph("<i>Created:</i> November 10, 2025 | <i>Version:</i> 1.0", styles['Normal']))
            elements.append(Spacer(1, 12))
            elements.append(PageBreak())
            
            # Section 1: Headings
            elements.append(Paragraph("1. Heading Hierarchy", styles['Heading1']))
            for i in range(1, 7):
                heading_style = f'Heading{min(i, 6)}'
                elements.append(Paragraph(f"Heading Level {i}", styles[heading_style]))
            elements.append(Spacer(1, 12))
            
            # Section 2: Text Formatting
            elements.append(Paragraph("2. Text Formatting", styles['Heading1']))
            elements.append(Paragraph("This is <b>bold text</b>, <i>italic text</i>, and <b><i>bold italic</i></b>.", styles['Normal']))
            elements.append(Paragraph("This shows <font color='red'>colored text</font> and various styles.", styles['Normal']))
            elements.append(Spacer(1, 12))
            
            # Section 3: Lists
            elements.append(Paragraph("3. Lists", styles['Heading1']))
            elements.append(Paragraph("3.1 Bulleted List", styles['Heading2']))
            for item in ["First bullet", "Second bullet", "Third bullet"]:
                elements.append(Paragraph(f"• {item}", styles['Normal']))
            elements.append(Spacer(1, 12))
            
            # Section 4: Tables
            elements.append(Paragraph("4. Tables", styles['Heading1']))
            table_data = [
                ['Name', 'Age', 'City', 'Occupation'],
                ['Alice Johnson', '28', 'New York', 'Software Engineer'],
                ['Bob Smith', '34', 'London', 'Data Scientist'],
                ['Charlie Brown', '45', 'Tokyo', 'Product Manager']
            ]
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))
            
            # Section 5: Code Blocks
            elements.append(Paragraph("5. Code Blocks", styles['Heading1']))
            code_style = ParagraphStyle(
                'Code',
                parent=styles['Normal'],
                fontName='Courier',
                fontSize=9,
                leftIndent=20,
                rightIndent=20,
                spaceBefore=6,
                spaceAfter=6
            )
            code_text = """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""
            
            elements.append(Paragraph(code_text.replace('\n', '<br/>'), code_style))
            elements.append(Spacer(1, 12))
            
            # Page break
            elements.append(PageBreak())
            
            # Summary
            elements.append(Paragraph("Document Summary", title_style))
            elements.append(Paragraph("This comprehensive PDF document includes:", styles['Normal']))
            
            features = [
                "All heading levels (1-6)",
                "Text formatting (bold, italic, colors)",
                "Lists (bulleted)",
                "Tables with styling",
                "Code blocks with monospace font",
                "Multiple pages with page breaks",
                "Professional typography"
            ]
            
            for feature in features:
                elements.append(Paragraph(f"[OK] {feature}", styles['Normal']))
            
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("<b>Total:</b> 5+ sections covering PDF document features", styles['Normal']))
            
            # Build PDF
            doc.build(elements)
            
            print("test_comprehensive.pdf created successfully!")
            print("  - Multi-page PDF generated with ReportLab")
            print("  - Headings, tables, lists, and code blocks included")
            return True
            
    except ImportError as e:
        print(f"Error: ReportLab not available!")
        print(f"Details: {e}")
        print("Please install: pip install reportlab")
        return False
    
    except Exception as e:
        print(f"Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_comprehensive_pdf()
    sys.exit(0 if success else 1)
