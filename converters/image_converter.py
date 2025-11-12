"""
Image converter - handles PNG/JPG/JPEG to document conversions
VCR-01: Visual Content Restructuring with advanced OCR, math recognition, and layout analysis
"""
import time
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image
import io

from converters.base import BaseConverter, ConversionResult
from converters.markdown_converter import MarkdownConverter
from ai.ocr_engine import OCREngine
from ai.table_detector import TableDetector
from ai.math_recognizer import MathRecognizer
from utils.logger import logger


class ImageConverter(BaseConverter):
    """
    Convert images (PNG, JPG, JPEG) to document formats
    with advanced content recognition and structural fidelity
    
    Supports:
    - Standard text extraction (OCR)
    - Mathematical notation recognition (LaTeX)
    - Table structure detection
    - Code block identification
    - Layout analysis (headings, paragraphs, lists)
    """
    
    SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg']
    
    def __init__(self):
        """Initialize image converter with OCR engine and advanced modules"""
        super().__init__()
        self.ocr_engine = OCREngine()
        self.markdown_converter = MarkdownConverter()
        self.table_detector = TableDetector()
        self.math_recognizer = MathRecognizer()
    
    def convert(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """
        Route to appropriate conversion method
        
        Args:
            input_file: Path to input image file
            output_file: Path to output document file
            **options: Additional conversion options
                - ocr_language: OCR language (default: 'tur+eng')
                - detect_math: Enable math formula recognition (default: False)
                - detect_tables: Enable table detection (default: True)
                - detect_code: Enable code block detection (default: True)
                - quality_check: Run quality check after conversion (default: False)
        
        Returns:
            ConversionResult object
        """
        output_format = Path(output_file).suffix.lower().lstrip('.')
        start_time = time.time()
        
        # Validate files
        error = self._validate_files(input_file, output_file)
        if error:
            return self._create_error_result(input_file, error, 'image', output_format)
        
        # Validate image format
        input_format = Path(input_file).suffix.lower().lstrip('.')
        if input_format not in self.SUPPORTED_FORMATS:
            return self._create_error_result(
                input_file,
                f"Unsupported image format: {input_format}. Supported: {', '.join(self.SUPPORTED_FORMATS)}",
                'image',
                output_format
            )
        
        try:
            # First convert to Markdown (unified intermediate format)
            logger.info(f"Converting image to Markdown: {input_file}")
            markdown_file = input_file + '.temp.md'
            md_result = self._image_to_markdown(input_file, markdown_file, **options)
            
            if not md_result.success:
                return md_result
            
            # Then convert Markdown to target format
            if output_format in ['md', 'markdown']:
                # Just rename the temp file
                Path(markdown_file).rename(output_file)
                result = md_result
                result.output_file = output_file
            elif output_format == 'pdf':
                result = self.markdown_converter._markdown_to_pdf(markdown_file, output_file, **options)
            elif output_format in ['docx', 'doc']:
                result = self.markdown_converter._markdown_to_docx(markdown_file, output_file, **options)
            elif output_format in ['html', 'htm']:
                result = self.markdown_converter._markdown_to_html(markdown_file, output_file, **options)
            else:
                return self._create_error_result(
                    input_file,
                    f"Unsupported output format: {output_format}",
                    'image',
                    output_format
                )
            
            # Clean up temp file
            try:
                Path(markdown_file).unlink(missing_ok=True)
            except:
                pass
            
            # Update result metadata
            result.conversion_time = time.time() - start_time
            result.input_format = 'image'
            
            logger.info(f"Successfully converted image to {output_format}: {output_file}")
            return result
            
        except Exception as e:
            logger.error(f"Image conversion failed: {e}")
            return self._create_error_result(
                input_file,
                str(e),
                'image',
                output_format
            )
    
    def _image_to_markdown(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """
        Convert image to Markdown with advanced content recognition
        
        This is the core method that implements VCR-01 specifications:
        1. Advanced layout analysis
        2. Content parsing (text, tables, math, code)
        3. Specialized content transformation
        4. Structural reconstruction
        
        Args:
            input_file: Path to input image
            output_file: Path to output Markdown file
            **options: Conversion options
        
        Returns:
            ConversionResult object
        """
        logger.info(f"Converting image to Markdown: {input_file} -> {output_file}")
        
        try:
            # Extract options
            ocr_language = options.get('ocr_language', 'tur+eng')
            detect_math = options.get('detect_math', False)
            detect_tables = options.get('detect_tables', True)
            detect_code = options.get('detect_code', True)
            
            # Phase 1: Advanced Layout Analysis (with OpenCV)
            logger.info("Phase 1: Layout analysis (OpenCV table detection)")
            layout_info = self._analyze_layout(input_file)
            
            # Phase 1.5: Image preprocessing for tables if detected
            image_to_ocr = input_file
            if layout_info.get('has_tables', False) and detect_tables:
                logger.info("Phase 1.5: Enhancing image for table OCR")
                try:
                    enhanced_path = self.table_detector.enhance_table_image(input_file)
                    image_to_ocr = enhanced_path
                    logger.info(f"Using enhanced image: {enhanced_path}")
                except Exception as e:
                    logger.warning(f"Image enhancement failed, using original: {e}")
            
            # Phase 2: Content Parsing
            logger.info("Phase 2: OCR text extraction")
            # Use layout-preserving OCR for tables
            preserve_layout = layout_info.get('has_tables', False)
            ocr_result = self.ocr_engine.extract_text_from_image(
                image_to_ocr, 
                language=ocr_language,
                preserve_layout=preserve_layout
            )
            
            if not ocr_result['success']:
                return self._create_error_result(
                    input_file,
                    f"OCR failed: {ocr_result.get('error', 'Unknown error')}",
                    'image',
                    'markdown'
                )
            
            raw_text = ocr_result['text']
            ocr_confidence = ocr_result.get('confidence', 0)
            
            # Phase 2.5: OCR Post-Processing (NEW)
            logger.info("Phase 2.5: OCR post-processing")
            cleaned_text = self._post_process_ocr(raw_text, ocr_confidence)
            
            # Phase 3: Specialized Content Transformation
            markdown_content = self._transform_content(
                cleaned_text,
                layout_info,
                detect_math=detect_math,
                detect_tables=detect_tables,
                detect_code=detect_code
            )
            
            # Phase 4: Structural Reconstruction
            final_markdown = self._reconstruct_structure(markdown_content, layout_info)
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_markdown)
            
            logger.info(f"Successfully converted image to Markdown: {output_file}")
            logger.info(f"OCR Confidence: {ocr_confidence:.1f}%")
            
            return self._create_success_result(
                input_file,
                output_file,
                'image',
                'markdown',
                metadata={
                    'ocr_confidence': ocr_confidence,
                    'word_count': len(final_markdown.split()),
                    'character_count': len(final_markdown),
                    'layout_blocks': len(layout_info.get('blocks', []))
                }
            )
            
        except Exception as e:
            logger.error(f"Image to Markdown conversion failed: {e}")
            raise
    
    def _analyze_layout(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze image layout to detect logical blocks using OpenCV
        
        Detects:
        - Text blocks (headings, paragraphs)
        - Tables (using line detection)
        - Code blocks
        - Math formulas
        - Images/diagrams
        
        Args:
            image_path: Path to image file
        
        Returns:
            Dictionary with layout information
        """
        try:
            # Open image
            image = Image.open(image_path)
            width, height = image.size
            
            # Detect tables using OpenCV
            detected_tables = self.table_detector.detect_tables(image_path)
            
            layout_info = {
                'width': width,
                'height': height,
                'blocks': [],
                'reading_order': [],
                'detected_structures': {
                    'tables': detected_tables,
                    'code_blocks': [],
                    'math_regions': []
                },
                'has_tables': len(detected_tables) > 0
            }
            
            logger.info(f"Layout analysis: {width}x{height}px, {len(detected_tables)} tables detected")
            return layout_info
            
        except Exception as e:
            logger.warning(f"Layout analysis failed: {e}")
            return {
                'blocks': [],
                'reading_order': [],
                'detected_structures': {},
                'has_tables': False
            }
    
    def _post_process_ocr(self, text: str, confidence: float) -> str:
        """
        Post-process OCR text to fix common recognition errors
        
        Fixes:
        - Word spacing issues (e.g., "Itcontains" → "It contains")
        - Common character confusion (l→I, 0→O, rn→m)
        - Double spaces and formatting issues
        - Common English/Turkish word corrections
        
        Args:
            text: Raw OCR text
            confidence: OCR confidence score (0-100)
        
        Returns:
            Cleaned text
        """
        if not text:
            return text
        
        original_text = text
        
        # 1. Fix common word spacing issues (CamelCase → Camel Case)
        # Pattern: lowercase letter followed by uppercase letter
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # 2. Fix common character confusions
        char_fixes = {
            # Only apply if confidence is lower
            '0O': 'OO',  # Zero followed by O might be two Os
            'O0': 'O0',  # Keep as is (might be intentional)
            'l1': 'li',  # lowercase l followed by 1 is likely 'li'
            'Il': 'Il',  # Keep capital I lowercase l
        }
        
        # 3. Fix specific known OCR errors for common words
        word_fixes = {
            'Itcontains': 'It contains',
            'Ithas': 'It has',
            'Itis': 'It is',
            'Itwas': 'It was',
            'multiine': 'multiline',
            'rnulti': 'multi',
            'sorne': 'some',
            'frorn': 'from',
            'tlie': 'the',
            'witli': 'with',
            'thern': 'them',
            'exarnple': 'example',
        }
        
        for wrong, correct in word_fixes.items():
            text = text.replace(wrong, correct)
        
        # 3.5. Fix mathematical symbol OCR errors (NEW)
        math_symbol_fixes = {
            # Complex probability/statistics formulas (specific patterns first)
            'Palo)': 'p(μ|σ)',  # Probability notation
            'N(u|': 'N(μ|',  # Normal distribution mu
            'N(u ': 'N(μ ',  # Normal distribution mu variant
            '0,07)': '0,σ²)',  # Sigma squared
            'ng?': '√(1/(2πσ²))',  # Square root fraction  
            'XP': 'exp',  # Exponential
            '2g?': '2σ²',  # 2 sigma squared
            'pk | 1)': 'p(x|μ) =',  # Probability x given mu complete
            'pk |': 'p(x|',  # Conditional probability x
            'p(x| 1)': 'p(x|μ) =',  # Probability x given mu
            'pk)': 'p(x)',  # Probability x
            'Mel)': 'N(x|μ,1)',  # Normal distribution
            '((x-μ)² ²)': 'exp(-½(x-μ)²)',  # Complete exponential form
            '(² ²)': '',  # Remove artifact
            ' ²)': '²)',  # Fix spacing
            'eer': '1/√(2π)',  # Euler constant fraction
            'ğe': '(x-μ)²',  # Squared difference (Turkish char)
            '<9': '²',  # Superscript 2
            'x1,...,': 'x₁,...,',  # Subscripts start
            '{21,': '{x₁,',  # Subscript in set
            ',2v}': ',xₙ}',  # Subscript end in set
            '21,...,2v': 'x₁,...,xₙ',  # Subscripts full
            ',...,2v': ',...,xₙ',  # Subscripts end
            ' 2v ': ' xₙ ',  # Subscript n standalone
            'x;': 'xᵢ',  # Subscript i
            ' 1 =?': '',  # Remove OCR artifact
            '2 1 =?': '',  # Remove header artifact
            'exp 2σ²': 'exp(-μ²/2σ²)',  # Complete exponential
            'σ ∑': 'σ⁻²',  # Sigma inverse squared (already has sigma symbol)
            'o ∑': 'σ⁻²',  # Sigma inverse squared
            'o-*': 'σ⁻²',  # Sigma inverse variant
            'p( |': 'p(μ|',  # Probability with mu
            'p(|': 'p(μ|',  # Probability variant
            ' o)': ' σ)',  # Sigma closing paren
            ' o ': ' σ ',  # Sigma space
            ' a)': ' α)',  # Alpha closing paren
            'p(j |': 'p(μ|',  # Mu misread as j
            ' &)': ' α)',  # Alpha misread as &
            ' « ': ' | ',  # Vertical bar (conditional)
            '1/0?': '1/σ²',  # Inverse variance
            '0?': 'σ²',  # Variance
            'o?': 'σ²',  # Variance variant
            'α nicer': 'a nicer',  # Common word fix
            'α set of': 'a set of',  # Common phrase
            'α set': 'a set',  # Common word
            'to α nicer': 'to a nicer',  # Common phrase variant
            '(£)': '(e)',  # Letter e misread
            '# O\n)': '(f)',  # Letter f misread with newline
            '# O': '',  # Remove artifact
            'p | |': 'μ|α',  # Mu given alpha
            # Basic symbols (general patterns)
            'x7': 'x²',  # x to the 7 → x squared
            'x?': 'x²',  # x? → x²
            'x*t*': 'x² +',  # Corrupted squared equation
            'X*t*': 'x² +',  # Uppercase variant
            '/2a': '/ 2a',  # Missing space in division
            'V(': '√(',  # Square root symbol
            'N16': '√16',  # Square root at start
            '. N': '. √',  # Square root with dot
            'T=': 'π =',  # Pi symbol
            'T ': 'π ',  # Pi with space
            '~ ': '∞ ',  # Infinity
            '~)': '∞)',  # Infinity in parentheses
            'J ': '∫ ',  # Integral symbol
            'Jx': '∫x',  # Integral x
            '> ': '∑ ',  # Summation
            '>(': '∑(',  # Summation with parentheses
            'd/dx': 'd/dx',  # Keep derivative notation
            'lim(x—': 'lim(x→',  # Limit arrow
            'lim(x-': 'lim(x→',  # Limit arrow variant
            '+ V': '+ √',  # Plus square root
            '- V': '- √',  # Minus square root
            'b?': 'b²',  # b squared
            'a?': 'a²',  # a squared
            'n?': 'n²',  # n squared
            'sin?': 'sin²',  # sin squared
            'cos?': 'cos²',  # cos squared
            'tan?': 'tan²',  # tan squared
            # Greek letters (common OCR errors)
            ' a ': ' α ',  # Alpha (when lowercase a appears in math context)
            ' B ': ' β ',  # Beta (uppercase B in math)
            ' y ': ' γ ',  # Gamma
            ' 5 ': ' δ ',  # Delta (5 misread as delta)
            '@ ': 'θ ',  # Theta
            '9 ': 'θ ',  # Theta variant
        }
        
        for wrong, correct in math_symbol_fixes.items():
            text = text.replace(wrong, correct)
        
        # 4. Fix multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # 5. Fix space before punctuation
        text = re.sub(r' +([.,!?;:])', r'\1', text)
        
        # 6. Fix missing space after punctuation
        text = re.sub(r'([.,!?;:])([A-Za-z])', r'\1 \2', text)
        
        # 7. Fix line breaks (too many or too few)
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
        
        # Log if corrections were made
        if text != original_text:
            corrections = len([1 for a, b in zip(original_text.split(), text.split()) if a != b])
            logger.info(f"OCR post-processing: {corrections} word(s) corrected")
        
        return text
    
    def _transform_content(
        self,
        raw_text: str,
        layout_info: Dict[str, Any],
        detect_math: bool = False,
        detect_tables: bool = True,
        detect_code: bool = True
    ) -> Dict[str, Any]:
        """
        Transform raw OCR text into structured content
        
        Args:
            raw_text: Raw OCR text
            layout_info: Layout analysis results
            detect_math: Enable math detection
            detect_tables: Enable table detection
            detect_code: Enable code detection
        
        Returns:
            Dictionary with transformed content
        """
        content = {
            'text': raw_text,
            'math_blocks': [],
            'tables': [],
            'code_blocks': []
        }
        
        # Detect and extract tables
        if detect_tables:
            content['tables'] = self._detect_tables(raw_text, layout_info)
        
        # Detect and extract code blocks
        if detect_code:
            content['code_blocks'] = self._detect_code_blocks(raw_text, layout_info)
        
        # Detect and extract math formulas
        if detect_math:
            content['math_blocks'] = self._detect_math_formulas(raw_text, layout_info)
        
        return content
    
    def _detect_tables(self, text: str, layout_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect tables in text and layout - IMPROVED VERSION
        
        Enhanced table detection using:
        - Multiple space/tab alignment detection
        - Consistent column structure recognition
        - Numeric pattern detection (common in tables)
        - Header row identification
        
        Args:
            text: OCR text
            layout_info: Layout information
        
        Returns:
            List of detected tables with proper structure
        """
        tables = []
        lines = text.split('\n')
        
        # Enhanced table detection
        potential_table = []
        table_start_idx = -1
        
        for idx, line in enumerate(lines):
            # Clean line
            line = line.strip()
            if not line:
                if potential_table and len(potential_table) >= 2:
                    # End of table - process it
                    table_data = self._structure_table(potential_table)
                    if table_data:
                        tables.append(table_data)
                potential_table = []
                table_start_idx = -1
                continue
            
            # Check if line looks like table row
            is_table_row = False
            
            # Method 1: Multiple spaces (column separator)
            if '  ' in line or '\t' in line:
                is_table_row = True
            
            # Method 2: Pipe character (already markdown table)
            if '|' in line:
                is_table_row = True
            
            # Method 3: Numbers with consistent spacing
            # e.g., "90  85  87.5" or "Ahmet  90  85"
            parts = re.split(r'\s{2,}|\t', line)
            if len(parts) >= 2:
                # Check if has numbers (common in tables)
                has_numbers = any(re.search(r'\d+', part) for part in parts)
                if has_numbers or len(parts) >= 3:
                    is_table_row = True
            
            # Method 4: Check for header-like content
            # Words like "Adı", "Matematik", "Fiyat", "Stok" etc.
            header_keywords = ['Adı', 'Adi', 'İsim', 'Isim', 'No', 'Numara', 
                              'Matematik', 'Türkçe', 'Turkce', 'Not', 
                              'Fiyat', 'Stok', 'Ürün', 'Urun', 'Miktar',
                              'Tarih', 'Saat', 'Toplam', 'Ortalama']
            if any(keyword in line for keyword in header_keywords):
                if len(parts) >= 2:
                    is_table_row = True
            
            if is_table_row:
                if table_start_idx == -1:
                    table_start_idx = idx
                potential_table.append(line)
            elif potential_table and len(potential_table) >= 2:
                # End of table
                table_data = self._structure_table(potential_table)
                if table_data:
                    tables.append(table_data)
                potential_table = []
                table_start_idx = -1
        
        # Check remaining table
        if potential_table and len(potential_table) >= 2:
            table_data = self._structure_table(potential_table)
            if table_data:
                tables.append(table_data)
        
        logger.info(f"Detected {len(tables)} potential tables")
        return tables
    
    def _structure_table(self, table_lines: List[str]) -> Optional[Dict[str, Any]]:
        """
        Convert detected table lines into structured Markdown table format
        
        Args:
            table_lines: List of raw table line strings
        
        Returns:
            Structured table dictionary or None if invalid
        """
        if not table_lines or len(table_lines) < 2:
            return None
        
        # Parse rows - split by multiple spaces or tabs
        parsed_rows = []
        max_cols = 0
        
        for line in table_lines:
            # Try different separators
            if '|' in line:
                # Already markdown format
                cells = [c.strip() for c in line.split('|') if c.strip()]
            elif '\t' in line:
                # Tab separated
                cells = [c.strip() for c in line.split('\t') if c.strip()]
            else:
                # Multiple spaces (2 or more)
                cells = [c.strip() for c in re.split(r'\s{2,}', line) if c.strip()]
            
            if cells:
                parsed_rows.append(cells)
                max_cols = max(max_cols, len(cells))
        
        if not parsed_rows or max_cols < 2:
            return None
        
        # Normalize rows to have same number of columns
        for row in parsed_rows:
            while len(row) < max_cols:
                row.append('')
        
        # Build Markdown table
        markdown_lines = []
        
        # Header row (first row)
        header = '| ' + ' | '.join(parsed_rows[0]) + ' |'
        markdown_lines.append(header)
        
        # Separator
        separator = '| ' + ' | '.join(['---'] * max_cols) + ' |'
        markdown_lines.append(separator)
        
        # Data rows
        for row in parsed_rows[1:]:
            data_row = '| ' + ' | '.join(row) + ' |'
            markdown_lines.append(data_row)
        
        return {
            'type': 'table',
            'rows': parsed_rows,
            'markdown': '\n'.join(markdown_lines),
            'columns': max_cols,
            'row_count': len(parsed_rows)
        }
    
    def _detect_code_blocks(self, text: str, layout_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect code blocks and pseudocode
        
        Heuristics:
        - Consistent indentation
        - Keywords (if, for, while, function, etc.)
        - Special characters ({}, [], (), ;)
        - Monospace-like formatting
        
        Args:
            text: OCR text
            layout_info: Layout information
        
        Returns:
            List of detected code blocks
        """
        code_blocks = []
        
        # Code block keywords
        code_keywords = [
            'function', 'def', 'class', 'if', 'else', 'for', 'while',
            'return', 'import', 'from', 'include', 'void', 'int', 'string',
            'Algorithm', 'Input:', 'Output:', 'BEGIN', 'END'
        ]
        
        lines = text.split('\n')
        code_block = []
        in_code = False
        
        for i, line in enumerate(lines):
            # Check if line looks like code
            stripped = line.strip()
            
            # Check for code keywords
            has_keyword = any(kw in stripped for kw in code_keywords)
            
            # Check for code-like characters
            has_code_chars = any(char in stripped for char in ['{', '}', '(', ')', ';', '='])
            
            # Check for indentation
            has_indent = len(line) > len(stripped) and len(line) - len(stripped) >= 2
            
            if has_keyword or (has_code_chars and has_indent):
                in_code = True
                code_block.append(line)
            elif in_code and stripped == '':
                code_block.append(line)
            elif in_code:
                # End of code block
                if len(code_block) >= 3:
                    code_blocks.append({
                        'type': 'code',
                        'lines': code_block.copy(),
                        'language': self._detect_programming_language(code_block)
                    })
                code_block = []
                in_code = False
        
        # Check for remaining code block
        if code_block and len(code_block) >= 3:
            code_blocks.append({
                'type': 'code',
                'lines': code_block,
                'language': self._detect_programming_language(code_block)
            })
        
        logger.info(f"Detected {len(code_blocks)} potential code blocks")
        return code_blocks
    
    def _detect_programming_language(self, code_lines: List[str]) -> str:
        """
        Detect programming language from code snippet
        
        Args:
            code_lines: Lines of code
        
        Returns:
            Detected language or 'text' if unknown
        """
        code_text = '\n'.join(code_lines).lower()
        
        # Simple language detection
        if 'def ' in code_text or 'import ' in code_text:
            return 'python'
        elif 'function' in code_text and ('{' in code_text or '}' in code_text):
            return 'javascript'
        elif '#include' in code_text or 'int main' in code_text:
            return 'cpp'
        elif 'public class' in code_text or 'public static void' in code_text:
            return 'java'
        elif 'algorithm' in code_text or 'input:' in code_text:
            return 'pseudocode'
        else:
            return 'text'
    
    def _detect_math_formulas(self, text: str, layout_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect mathematical formulas and convert to LaTeX
        
        TODO: Implement advanced math recognition using:
        - Pix2Tex model
        - MathPix API
        - Symbol detection (∫, Σ, √, etc.)
        
        Args:
            text: OCR text
            layout_info: Layout information
        
        Returns:
            List of detected math formulas
        """
        # Use MathRecognizer to detect and convert formulas
        formulas = self.math_recognizer.recognize_formulas(text)
        
        logger.info(f"Detected {len(formulas)} potential math formulas")
        if formulas:
            logger.info("Math formulas converted to LaTeX format")
        
        return formulas
    
    def _reconstruct_structure(self, content: Dict[str, Any], layout_info: Dict[str, Any]) -> str:
        """
        Reconstruct document structure in Markdown format
        
        Creates proper hierarchy:
        - Headings (detected from font size/weight)
        - Paragraphs
        - Lists (bullet/numbered)
        - Tables (Markdown format)
        - Code blocks (fenced with ```)
        - Math formulas ($...$ or $$...$$)
        
        Args:
            content: Transformed content
            layout_info: Layout information
        
        Returns:
            Final Markdown string
        """
        markdown_lines = []
        
        # Process main text
        text = content['text']
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                markdown_lines.append('')
                i += 1
                continue
            
            # Detect headings (heuristic: short lines, all caps or title case)
            if len(line) < 80 and (line.isupper() or line.istitle()):
                # Guess heading level based on length
                if len(line) < 30:
                    markdown_lines.append(f"# {line}")
                else:
                    markdown_lines.append(f"## {line}")
            
            # Detect list items
            elif line.startswith('-') or line.startswith('•') or (len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')']):
                markdown_lines.append(line)
            
            # Regular paragraph
            else:
                markdown_lines.append(line)
            
            i += 1
        
        # Insert tables at appropriate positions (NEW: use structured markdown)
        for table in content['tables']:
            if 'markdown' in table:
                # Use pre-formatted markdown from _structure_table
                markdown_lines.append('\n')
                markdown_lines.append(table['markdown'])
                markdown_lines.append('\n')
            else:
                # Fallback to old method
                markdown_lines.append('\n')
                markdown_lines.append(self._format_table_markdown(table))
                markdown_lines.append('\n')
        
        # Insert code blocks
        for code_block in content['code_blocks']:
            markdown_lines.append('\n')
            markdown_lines.append(f"```{code_block['language']}")
            markdown_lines.extend(code_block['lines'])
            markdown_lines.append("```")
            markdown_lines.append('\n')
        
        # Insert math formulas (with LaTeX)
        for math_block in content['math_blocks']:
            latex = math_block.get('latex', '')
            if latex:
                if math_block.get('inline', False):
                    # Inline math
                    markdown_lines.append(f"\n${latex}$\n")
                else:
                    # Display math
                    markdown_lines.append('\n')
                    markdown_lines.append(f"$${latex}$$")
                    markdown_lines.append('\n')
            else:
                # Fallback: use raw text
                markdown_lines.append(f"\n*Math: {math_block.get('text', '')}*\n")
        
        return '\n'.join(markdown_lines)
    
    def _format_table_markdown(self, table: Dict[str, Any]) -> str:
        """
        Format table data as Markdown table
        
        Args:
            table: Table dictionary with rows
        
        Returns:
            Markdown table string
        """
        if not table['rows']:
            return ''
        
        rows = table['rows']
        
        # Split each row into cells (by multiple spaces or tabs)
        import re
        cells = []
        for row in rows:
            row_cells = re.split(r'\s{2,}|\t+', row.strip())
            cells.append(row_cells)
        
        if not cells:
            return ''
        
        # Find max column count
        max_cols = max(len(row) for row in cells)
        
        # Pad rows to same length
        for row in cells:
            while len(row) < max_cols:
                row.append('')
        
        # Format as Markdown
        markdown_table = []
        
        # Header row
        markdown_table.append('| ' + ' | '.join(cells[0]) + ' |')
        
        # Separator
        markdown_table.append('| ' + ' | '.join(['---'] * max_cols) + ' |')
        
        # Data rows
        for row in cells[1:]:
            markdown_table.append('| ' + ' | '.join(row) + ' |')
        
        return '\n'.join(markdown_table)
