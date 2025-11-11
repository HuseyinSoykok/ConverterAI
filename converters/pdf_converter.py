"""
PDF converter - handles all PDF conversions
"""
import time
import re
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF
import pdfplumber
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import markdown
from bs4 import BeautifulSoup
from PIL import Image
import io

from converters.base import BaseConverter, ConversionResult
from utils.logger import logger


class PDFConverter(BaseConverter):
    """Convert PDF to other formats"""
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        if not text:
            return ''
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
    
    def convert(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """Route to appropriate conversion method"""
        output_format = Path(output_file).suffix.lower().lstrip('.')
        
        start_time = time.time()
        
        # Validate files
        error = self._validate_files(input_file, output_file)
        if error:
            return self._create_error_result(input_file, error, 'pdf', output_format)
        
        try:
            if output_format in ['docx', 'doc']:
                result = self._pdf_to_docx(input_file, output_file, **options)
            elif output_format in ['md', 'markdown']:
                result = self._pdf_to_markdown(input_file, output_file, **options)
            elif output_format in ['html', 'htm']:
                result = self._pdf_to_html(input_file, output_file, **options)
            else:
                return self._create_error_result(
                    input_file, 
                    f"Unsupported output format: {output_format}",
                    'pdf',
                    output_format
                )
            
            processing_time = time.time() - start_time
            result.processing_time = processing_time
            return result
            
        except Exception as e:
            logger.error(f"PDF conversion failed: {e}", exc_info=True)
            return self._create_error_result(input_file, str(e), 'pdf', output_format)
    
    def _pdf_to_docx(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """Convert PDF to DOCX with improved text extraction and formatting"""
        logger.info(f"Converting PDF to DOCX: {input_file} -> {output_file}")
        
        doc = Document()
        warnings = []
        
        try:
            # Open PDF with PyMuPDF for better text extraction
            pdf_document = fitz.open(input_file)
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                
                # Try table extraction first with pdfplumber
                try:
                    import pdfplumber
                    with pdfplumber.open(input_file) as pdf_plumber:
                        plumber_page = pdf_plumber.pages[page_num]
                        tables = plumber_page.extract_tables()
                        
                        if tables:
                            for table_data in tables:
                                if table_data and len(table_data) > 0:
                                    # Add table to document
                                    num_rows = len(table_data)
                                    num_cols = max(len(row) for row in table_data)
                                    
                                    table = doc.add_table(rows=num_rows, cols=num_cols)
                                    table.style = 'Table Grid'
                                    
                                    for i, row in enumerate(table_data):
                                        for j, cell in enumerate(row):
                                            if j < num_cols and cell:
                                                table.rows[i].cells[j].text = str(cell).strip()
                                    
                                    # Add spacing after table
                                    doc.add_paragraph()
                except Exception as e:
                    warnings.append(f"Table extraction failed: {e}")
                
                # Extract text with formatting
                text_dict = page.get_text("dict")
                blocks = text_dict.get("blocks", [])
                
                for block in blocks:
                    if block.get("type") == 0:  # Text block
                        block_text = []
                        max_font_size = 0
                        is_bold = False
                        
                        for line in block.get("lines", []):
                            line_text = ""
                            line_spans = line.get("spans", [])
                            
                            for span_idx, span in enumerate(line_spans):
                                span_text = span.get("text", "")
                                
                                # Preserve spaces between spans
                                if span_idx > 0 and span_text and not span_text[0].isspace():
                                    line_text += " "
                                
                                line_text += span_text
                                
                                # Track font properties
                                font_size = span.get("size", 12)
                                if font_size > max_font_size:
                                    max_font_size = font_size
                                
                                # Check if bold
                                font_flags = span.get("flags", 0)
                                if font_flags & 2**4:  # Bold flag
                                    is_bold = True
                            
                            if line_text.strip():
                                block_text.append(line_text.strip())
                        
                        if block_text:
                            full_text = " ".join(block_text)
                            
                            if full_text.strip():
                                # Detect if it's a heading based on font size and properties
                                para = doc.add_paragraph()
                                
                                # Smart heading detection
                                if max_font_size > 18 or (max_font_size > 16 and is_bold):
                                    para.style = 'Heading 1'
                                elif max_font_size > 14 or (max_font_size > 12 and is_bold and len(full_text) < 100):
                                    para.style = 'Heading 2'
                                elif max_font_size > 12 and is_bold and len(full_text) < 80:
                                    para.style = 'Heading 3'
                                else:
                                    para.style = 'Normal'
                                
                                # Add text to paragraph
                                run = para.add_run(full_text)
                                if is_bold and para.style == 'Normal':
                                    run.bold = True
                                
                                # Add spacing after paragraph for better readability
                                para.paragraph_format.space_after = Pt(6)
                    
                    elif block.get("type") == 1:  # Image block
                        try:
                            # Extract and add image
                            img = block.get("image")
                            if img:
                                xref = block.get("xref")
                                if xref:
                                    base_image = pdf_document.extract_image(xref)
                                    image_bytes = base_image["image"]
                                    
                                    # Save temporarily and add to document
                                    image_stream = io.BytesIO(image_bytes)
                                    doc.add_picture(image_stream, width=Inches(5.0))
                        except Exception as e:
                            warnings.append(f"Could not extract image: {e}")
                
                # Page break after each page (except last)
                if page_num < len(pdf_document) - 1:
                    doc.add_page_break()
            
            pdf_document.close()
            
            # Save document
            doc.save(output_file)
            
            logger.info(f"Successfully converted PDF to DOCX: {output_file}")
            return self._create_success_result(
                input_file, 
                output_file, 
                'pdf', 
                'docx',
                warnings=warnings,
                metadata={'pages': len(pdf_document)}
            )
            
        except Exception as e:
            logger.error(f"PDF to DOCX conversion failed: {e}")
            raise
    
    def _pdf_to_markdown(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """Convert PDF to Markdown with enhanced table, list, and formatting support"""
        logger.info(f"Converting PDF to Markdown: {input_file} -> {output_file}")
        
        markdown_content = []
        warnings = []
        
        try:
            # Use both PyMuPDF (for formatting) and pdfplumber (for tables)
            doc = fitz.open(input_file)
            num_pages = len(doc)
            
            for page_num in range(num_pages):
                page = doc[page_num]
                
                # Add page header with proper spacing
                if page_num > 0:
                    markdown_content.append("\n\n---\n\n")
                
                markdown_content.append(f"## Page {page_num + 1}\n\n")
                
                # STEP 1: Extract tables first with pdfplumber
                tables_extracted = []
                table_bboxes = []
                
                try:
                    with pdfplumber.open(input_file) as pdf_plumber:
                        plumber_page = pdf_plumber.pages[page_num]
                        tables = plumber_page.extract_tables()
                        
                        if tables:
                            for table_data in tables:
                                if table_data and len(table_data) > 0:
                                    # Convert table to markdown
                                    md_table = self._table_to_markdown(table_data)
                                    tables_extracted.append(md_table)
                                    
                                    # Try to get table bbox (approximate)
                                    try:
                                        table_obj = plumber_page.find_tables()
                                        if table_obj:
                                            for t in table_obj:
                                                table_bboxes.append(t.bbox)
                                    except:
                                        pass
                except Exception as e:
                    warnings.append(f"Table extraction failed on page {page_num + 1}: {e}")
                
                # STEP 2: Extract text blocks with formatting
                blocks = page.get_text("dict")["blocks"]
                
                # Calculate average font size for the page
                all_font_sizes = []
                for block in blocks:
                    if block.get("type") == 0:
                        for line in block.get("lines", []):
                            for span in line.get("spans", []):
                                all_font_sizes.append(span.get("size", 12))
                
                avg_font_size = sum(all_font_sizes) / len(all_font_sizes) if all_font_sizes else 12
                
                for block in blocks:
                    if block.get("type") == 0:  # Text block
                        # Check if block overlaps with a table (skip if yes)
                        block_bbox = block.get("bbox", [0, 0, 0, 0])
                        is_in_table = False
                        
                        for table_bbox in table_bboxes:
                            if self._bbox_overlap(block_bbox, table_bbox):
                                is_in_table = True
                                break
                        
                        if is_in_table:
                            continue
                        
                        # Process lines in block
                        for line in block.get("lines", []):
                            line_text_parts = []
                            line_font_size = 0
                            is_bold = False
                            is_italic = False
                            is_monospace = False
                            
                            for span in line.get("spans", []):
                                span_text = span.get("text", "").strip()
                                if not span_text:
                                    continue
                                
                                # Font properties
                                font_size = span.get("size", 12)
                                font_flags = span.get("flags", 0)
                                font_name = span.get("font", "").lower()
                                
                                if font_size > line_font_size:
                                    line_font_size = font_size
                                
                                # Check bold (bit 4 = 16)
                                span_bold = bool(font_flags & (1 << 4))
                                # Check italic (bit 1 = 2)
                                span_italic = bool(font_flags & (1 << 1))
                                # Check monospace fonts
                                span_monospace = any(mono in font_name for mono in ['courier', 'mono', 'consolas', 'menlo'])
                                
                                # Apply formatting
                                formatted_text = span_text
                                
                                if span_monospace:
                                    formatted_text = f"`{formatted_text}`"
                                    is_monospace = True
                                elif span_bold and span_italic:
                                    formatted_text = f"***{formatted_text}***"
                                elif span_bold:
                                    formatted_text = f"**{formatted_text}**"
                                    is_bold = True
                                elif span_italic:
                                    formatted_text = f"*{formatted_text}*"
                                    is_italic = True
                                
                                line_text_parts.append(formatted_text)
                            
                            if not line_text_parts:
                                continue
                            
                            full_line = " ".join(line_text_parts)
                            
                            # Smart content type detection
                            
                            # 1. Heading detection (based on font size)
                            if line_font_size > avg_font_size * 1.5:
                                heading_level = 1
                            elif line_font_size > avg_font_size * 1.3:
                                heading_level = 2
                            elif line_font_size > avg_font_size * 1.15:
                                heading_level = 3
                            else:
                                heading_level = 0
                            
                            # Additional heading indicators
                            if heading_level == 0:
                                # All caps + short = heading
                                if len(full_line) < 100 and full_line.upper() == full_line and len(full_line) > 3:
                                    heading_level = 3
                                    full_line = full_line.title()
                                # Ends with colon + short = subheading
                                elif len(full_line) < 80 and full_line.endswith(':'):
                                    heading_level = 4
                            
                            if heading_level > 0:
                                # Remove markdown formatting from headings
                                clean_line = full_line.replace('**', '').replace('*', '').replace('`', '')
                                markdown_content.append(f"\n{'#' * heading_level} {clean_line}\n\n")
                                continue
                            
                            # 2. List detection (bullet or numbered)
                            stripped_line = full_line.lstrip()
                            
                            # Bullet list detection
                            if stripped_line and stripped_line[0] in ['•', '·', '◦', '▪', '▫', '-', '–', '—']:
                                list_text = stripped_line[1:].strip()
                                markdown_content.append(f"- {list_text}\n")
                                continue
                            
                            # Numbered list detection (1., a., i., etc.)
                            import re
                            numbered_match = re.match(r'^(\d+|[a-z]|[ivxlcdm]+)[\.\)]\s+(.+)', stripped_line, re.IGNORECASE)
                            if numbered_match:
                                list_text = numbered_match.group(2)
                                markdown_content.append(f"1. {list_text}\n")
                                continue
                            
                            # 3. Code block detection (multiple monospace spans)
                            if is_monospace or full_line.count('`') > 2:
                                # Remove inline code markers for code block
                                code_line = full_line.replace('`', '')
                                # Check if previous line was also code
                                if markdown_content and markdown_content[-1].startswith('    '):
                                    markdown_content.append(f"    {code_line}\n")
                                else:
                                    markdown_content.append(f"\n    {code_line}\n")
                                continue
                            
                            # 4. Regular paragraph
                            # Handle hyphenation
                            if full_line.endswith('-'):
                                markdown_content.append(full_line[:-1])  # Remove hyphen
                            else:
                                markdown_content.append(full_line)
                                
                                # Add proper line break
                                if not full_line.endswith(('.', '!', '?', ':', ';')):
                                    markdown_content.append(" ")
                                else:
                                    markdown_content.append("\n\n")
                
                # STEP 3: Add extracted tables at the end of page content
                if tables_extracted:
                    markdown_content.append("\n\n")
                    for table_md in tables_extracted:
                        markdown_content.append(table_md)
                        markdown_content.append("\n\n")
            
            doc.close()
            
            # Clean up the final content
            final_content = ''.join(markdown_content)
            
            # Remove excessive blank lines (more than 2)
            final_content = re.sub(r'\n{4,}', '\n\n\n', final_content)
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write(final_content)
            
            logger.info(f"Successfully converted PDF to Markdown: {output_file}")
            return self._create_success_result(
                input_file,
                output_file,
                'pdf',
                'markdown',
                warnings=warnings,
                metadata={'pages': num_pages, 'tables': len(tables_extracted)}
            )
            
        except Exception as e:
            logger.error(f"PDF to Markdown conversion failed: {e}")
            raise
    
    def _table_to_markdown(self, table_data):
        """Convert table data to Markdown table format"""
        if not table_data or len(table_data) == 0:
            return ""
        
        md_lines = []
        
        # Get max columns
        max_cols = max(len(row) for row in table_data)
        
        # Process header row
        if len(table_data) > 0:
            header = table_data[0]
            header_cells = []
            for i in range(max_cols):
                cell = header[i] if i < len(header) else ""
                # Clean cell content
                cell_text = str(cell).strip().replace('\n', ' ').replace('|', '\\|')
                header_cells.append(cell_text)
            
            md_lines.append("| " + " | ".join(header_cells) + " |")
            
            # Separator row
            md_lines.append("| " + " | ".join(["---"] * max_cols) + " |")
        
        # Process data rows
        for row in table_data[1:]:
            row_cells = []
            for i in range(max_cols):
                cell = row[i] if i < len(row) else ""
                # Clean cell content
                cell_text = str(cell).strip().replace('\n', ' ').replace('|', '\\|')
                row_cells.append(cell_text)
            
            md_lines.append("| " + " | ".join(row_cells) + " |")
        
        return "\n".join(md_lines)
    
    def _bbox_overlap(self, bbox1, bbox2, threshold=0.5):
        """Check if two bounding boxes overlap significantly"""
        if not bbox1 or not bbox2:
            return False
        
        # bbox format: (x0, y0, x1, y1)
        x_overlap = max(0, min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0]))
        y_overlap = max(0, min(bbox1[3], bbox2[3]) - max(bbox1[1], bbox2[1]))
        
        overlap_area = x_overlap * y_overlap
        bbox1_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
        
        if bbox1_area == 0:
            return False
        
        overlap_ratio = overlap_area / bbox1_area
        return overlap_ratio > threshold
    
    def _pdf_to_html(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """Convert PDF to HTML with enhanced styling and readability"""
        logger.info(f"Converting PDF to HTML: {input_file} -> {output_file}")
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '<title>Converted PDF</title>',
            '<style>',
            '* { box-sizing: border-box; }',
            'body {',
            '    font-family: "Segoe UI", Arial, sans-serif;',
            '    margin: 0;',
            '    padding: 40px;',
            '    line-height: 1.8;',
            '    color: #333;',
            '    background-color: #f5f5f5;',
            '}',
            '.container {',
            '    max-width: 900px;',
            '    margin: 0 auto;',
            '    background: white;',
            '    padding: 40px;',
            '    box-shadow: 0 2px 8px rgba(0,0,0,0.1);',
            '}',
            '.page {',
            '    margin-bottom: 60px;',
            '    padding-bottom: 40px;',
            '    border-bottom: 2px solid #e0e0e0;',
            '}',
            '.page:last-child { border-bottom: none; }',
            'h1, h2, h3, h4, h5, h6 {',
            '    margin-top: 24px;',
            '    margin-bottom: 16px;',
            '    font-weight: 600;',
            '    line-height: 1.25;',
            '}',
            'h1 {',
            '    font-size: 2em;',
            '    color: #1a1a1a;',
            '    border-bottom: 3px solid #0066cc;',
            '    padding-bottom: 12px;',
            '}',
            'h2 {',
            '    font-size: 1.5em;',
            '    color: #2a2a2a;',
            '    border-bottom: 2px solid #e0e0e0;',
            '    padding-bottom: 8px;',
            '}',
            'h3 { font-size: 1.25em; color: #333; }',
            'h4 { font-size: 1.1em; color: #444; }',
            'p {',
            '    margin: 16px 0;',
            '    text-align: justify;',
            '}',
            'ul, ol {',
            '    margin: 16px 0;',
            '    padding-left: 32px;',
            '}',
            'li {',
            '    margin: 8px 0;',
            '    line-height: 1.6;',
            '}',
            'ul li {',
            '    list-style-type: disc;',
            '}',
            'table {',
            '    border-collapse: collapse;',
            '    width: 100%;',
            '    margin: 24px 0;',
            '    background-color: white;',
            '    box-shadow: 0 1px 3px rgba(0,0,0,0.1);',
            '}',
            'table, th, td {',
            '    border: 1px solid #ddd;',
            '}',
            'th, td {',
            '    padding: 14px 16px;',
            '    text-align: left;',
            '}',
            'th {',
            '    background-color: #0066cc;',
            '    color: white;',
            '    font-weight: 600;',
            '    text-transform: uppercase;',
            '    font-size: 0.9em;',
            '    letter-spacing: 0.5px;',
            '}',
            'tr:nth-child(even) { background-color: #f9f9f9; }',
            'tr:hover { background-color: #f0f0f0; }',
            'img {',
            '    max-width: 100%;',
            '    height: auto;',
            '    margin: 20px 0;',
            '    border-radius: 4px;',
            '    box-shadow: 0 2px 4px rgba(0,0,0,0.1);',
            '}',
            'code {',
            '    background-color: #f4f4f4;',
            '    padding: 2px 6px;',
            '    border-radius: 3px;',
            '    font-family: "Courier New", monospace;',
            '    font-size: 0.9em;',
            '}',
            'pre {',
            '    background-color: #f4f4f4;',
            '    padding: 16px;',
            '    border-radius: 4px;',
            '    overflow-x: auto;',
            '    margin: 20px 0;',
            '}',
            '.page-number {',
            '    color: #666;',
            '    font-size: 0.9em;',
            '    margin-bottom: 20px;',
            '}',
            '@media print {',
            '    body { background: white; }',
            '    .container { box-shadow: none; }',
            '    .page { page-break-after: always; }',
            '}',
            '</style>',
            '</head>',
            '<body>',
            '<div class="container">',
        ]
        
        warnings = []
        
        try:
            # Use pdfplumber for better structured extraction
            with pdfplumber.open(input_file) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    html_parts.append(f'<div class="page">')
                    html_parts.append(f'<div class="page-number">Page {page_num} of {len(pdf.pages)}</div>')
                    
                    # Extract text with layout preservation
                    text = page.extract_text()
                    if text:
                        # Split into lines for better processing
                        lines = text.split('\n')
                        current_paragraph = []
                        in_list = False
                        
                        for line in lines:
                            line = line.strip()
                            if not line:
                                # Empty line - end current paragraph
                                if current_paragraph:
                                    para_text = ' '.join(current_paragraph)
                                    html_parts.append(f'<p>{self._escape_html(para_text)}</p>')
                                    current_paragraph = []
                                if in_list:
                                    html_parts.append('</ul>')
                                    in_list = False
                                continue
                            
                            # Detect headings by font size and formatting
                            # Check if line is all uppercase and short (likely heading)
                            if len(line) < 100 and line.isupper() and not any(char.isdigit() for char in line[:3]):
                                if current_paragraph:
                                    para_text = ' '.join(current_paragraph)
                                    html_parts.append(f'<p>{self._escape_html(para_text)}</p>')
                                    current_paragraph = []
                                html_parts.append(f'<h2>{self._escape_html(line.title())}</h2>')
                            
                            # Detect subheadings (lines ending with colon)
                            elif len(line) < 80 and line.endswith(':') and not line.startswith(' '):
                                if current_paragraph:
                                    para_text = ' '.join(current_paragraph)
                                    html_parts.append(f'<p>{self._escape_html(para_text)}</p>')
                                    current_paragraph = []
                                html_parts.append(f'<h3>{self._escape_html(line)}</h3>')
                            
                            # Detect bullet points or numbered lists
                            elif line.startswith(('•', '-', '*', '▪', '◦', '▫', '■', '□')) or \
                                 (len(line) > 2 and line[0].isdigit() and line[1] in '.):'):
                                if current_paragraph:
                                    para_text = ' '.join(current_paragraph)
                                    html_parts.append(f'<p>{self._escape_html(para_text)}</p>')
                                    current_paragraph = []
                                if not in_list:
                                    html_parts.append('<ul>')
                                    in_list = True
                                # Remove bullet/number prefix
                                list_text = line.lstrip('•-*▪◦▫■□ ')
                                if line[0].isdigit():
                                    list_text = line.split('.', 1)[1].strip() if '.' in line else line
                                html_parts.append(f'<li>{self._escape_html(list_text)}</li>')
                            
                            # Regular text line
                            else:
                                if in_list:
                                    html_parts.append('</ul>')
                                    in_list = False
                                current_paragraph.append(line)
                        
                        # Close any remaining paragraph or list
                        if current_paragraph:
                            para_text = ' '.join(current_paragraph)
                            html_parts.append(f'<p>{self._escape_html(para_text)}</p>')
                        if in_list:
                            html_parts.append('</ul>')
                    
                    # Extract tables with better formatting
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            if table and len(table) > 0:
                                html_parts.append('<table>')
                                
                                for row_idx, row in enumerate(table):
                                    html_parts.append('<tr>')
                                    tag = 'th' if row_idx == 0 else 'td'
                                    
                                    for cell in row:
                                        if cell:
                                            # Clean and escape cell content
                                            cell_content = ' '.join(str(cell).split())
                                            cell_content = self._escape_html(cell_content)
                                        else:
                                            cell_content = ''
                                        html_parts.append(f'<{tag}>{cell_content}</{tag}>')
                                    
                                    html_parts.append('</tr>')
                                
                                html_parts.append('</table>')
                    
                    html_parts.append('</div>')
            
            html_parts.extend(['</div>', '</body>', '</html>'])
            
            # Write to file with UTF-8 encoding
            final_html = '\n'.join(html_parts)
            with open(output_file, 'w', encoding='utf-8-sig') as f:
                f.write(final_html)
            
            logger.info(f"Successfully converted PDF to HTML: {output_file}")
            return self._create_success_result(
                input_file,
                output_file,
                'pdf',
                'html',
                warnings=warnings,
                metadata={'pages': len(pdf.pages)}
            )
            
        except Exception as e:
            logger.error(f"PDF to HTML conversion failed: {e}")
            raise
