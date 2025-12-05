"""
Advanced Math OCR Processor
Converts raw OCR text to properly formatted Markdown with LaTeX math
"""
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from utils.logger import logger


class MathOCRProcessor:
    """
    Post-processor for OCR output that:
    1. Detects and converts mathematical expressions to LaTeX
    2. Structures content with proper headings
    3. Removes page headers/footers
    4. Fixes common OCR errors in math symbols
    """
    
    def __init__(self):
        # Common OCR misreadings for math symbols
        # Note: Values should NOT contain raw backslashes that could cause regex issues
        # Use Unicode characters directly instead of LaTeX when possible
        self.symbol_corrections = {
            # Greek letters - direct Unicode replacements
            '82': '∂Ω',  # Boundary
            '8Q': '∂Ω',
            '€': '∈',  # Element of
            '¢': '∈',
            'Vv': '∇v',  # Nabla
            'Vu': '∇u',
            'Wu': '∇u',
            '—A': '-Δ',  # Negative Laplacian
            '->': '→',
            '=>': '⇒',
            '<=': '≤',
            '>=': '≥',
            '!=': '≠',
            '~=': '≈',
            'inf': '∞',
            # Subscripts/superscripts - use Unicode
            'H4': 'H₀¹',
            'H0': 'H₀',
            'L2': 'L²',
            'L?': 'L²',
            'C2': 'C²',
            'C?': 'C²',
            'C+': 'C¹',
            'R2': 'ℝ²',
            'Rn': 'ℝⁿ',
            # Common function spaces
            'AA(Q)': 'H₀¹(Ω)',
        }
        
        # Longer corrections that are safe (no short words to confuse)
        self.safe_replacements = {
            'Vh': 'V_h',
            'Vi': 'V_h', 
            'Vi)': 'V_h',
        }
        
        # Patterns to detect mathematical content
        self.math_patterns = [
            # Equations with operators
            (r'(\w+)\s*=\s*([^,\n]+)', self._format_equation),
            # Integrals
            (r'integral[_\s]*(over[_\s]*)?(\w+)', self._format_integral),
            # Partial derivatives
            (r'partial[_\s]*(\w+)', self._format_partial),
            # Summations
            (r'sum[_\s]*(from|over)?', self._format_sum),
        ]
        
        # Footer/header patterns to remove (more aggressive)
        self.noise_patterns = [
            r'November \d+,?\s*\d{4}.*',  # Date lines
            r'Song the 2d Poisson.*',
            r'Soling the 24 Poison.*',
            r'Sling the 24 Poison.*',
            r'Solving the 2d Poisson.*Method.*\d+',
            r'H\s*LR\s*I?\[?s?\]?',  # Header artifacts
            r'\|?\s*H\s*LR\s*\|?\[?s?\]?',
            r'Ral\s*$',
            r'ry\s*$',
            r'^\s*i\s*$',  # Lone 'i' from page numbers
            r'^\s*sei\s*\d*\s*$',  # Page number artifacts
            r'^\s*site\s*\d*\s*$',
            r'seit\s*\d+\s*$',
            r'\(\s*@\s*\)',  # OCR artifact for equation numbers
            r'€€@',  # OCR artifacts
            r'\s+\d+\s*$',  # Trailing page numbers
            r'^\s*∞\s*——.*$',  # Header line artifacts
            r"^'omputing Cen.*$",  # Corrupted header
            r'^.*SSS\s*S—.*$',  # More header artifacts
            r'^\s*---\s*=.*$',  # Artifact lines
            r'sing=\s*and=a\s*=',  # Corrupted text
            r'VAVAVAVA.*',  # Mesh visualization artifacts
            r'IVAVAVA.*',
            r'AVAVA.*',
            r'77474174.*',
            r'\(r¥-\].*',
            r'OOO,',
            r'KETh',
            r'iad\s+\d+',
            r'PAA\s+\d+',
            r'Od\s+\d+',
            r'^\s*ed\s+i\s*$',
        ]
        
        # Section title patterns - more robust
        self.section_patterns = [
            (r'Strong Formulation of the Poisson Equation.*', '## Strong Formulation of the Poisson Equation\n'),
            (r'Weak Formulation of the Poisson Equation\s*I+.*', '## Weak Formulation of the Poisson Equation\n'),
            (r'Meshing and Function Space\s*I+.*', '## Meshing and Function Space\n'),
            (r'Basis Functions.*Elements?\)?.*', '## Basis Functions (P1 Elements)\n'),
            (r'^Finite Element Method\s*$', '## Finite Element Method\n'),
            (r'Gradients.*Discrete\s*Form.*', '## Gradients & Discrete Form\n'),
            (r'Converting into a Linear.*', '## Converting into a Linear Equation System\n'),
            (r'Assembling and Solving.*', '## Assembling and Solving\n'),
            (r'Algorithm\s*\d*:?\s*Global Assembly.*', '### Algorithm: Global Assembly\n'),
            (r'The Galerkin Problem.*', '### The Galerkin Problem (Discrete Form)\n'),
            (r'Area Coordinates.*', '### Area Coordinates\n'),
            (r'Explicit Formulas.*', '### Explicit Formulas\n'),
            (r'Step\s*1:\s*Meshing', '### Step 1: Meshing\n'),
            (r'Step\s*2:\s*Define.*', '### Step 2: Define $V_h$\n'),
        ]
    
    def process(self, ocr_text: str, title: str = None) -> str:
        """
        Main processing function
        
        Args:
            ocr_text: Raw OCR output text
            title: Optional document title
            
        Returns:
            Formatted Markdown with LaTeX math
        """
        logger.info("Processing OCR text with MathOCRProcessor")
        
        # Step 1: Split into pages
        pages = self._split_pages(ocr_text)
        
        # Step 2: Process each page
        processed_pages = []
        for i, page in enumerate(pages):
            processed = self._process_page(page, i + 1)
            if processed.strip():
                processed_pages.append(processed)
        
        # Step 3: Combine and add header
        content = '\n\n---\n\n'.join(processed_pages)
        
        # Step 4: Add document title
        if title:
            content = f"# {title}\n\n{content}"
        
        # Step 5: Final cleanup
        content = self._final_cleanup(content)
        
        return content
    
    def _split_pages(self, text: str) -> List[str]:
        """Split text into pages"""
        # Try different page markers
        if '## Page' in text:
            parts = re.split(r'---\s*\n\s*## Page \d+\s*\n', text)
            return [p.strip() for p in parts if p.strip()]
        elif '\n\n\n' in text:
            return [p.strip() for p in text.split('\n\n\n') if p.strip()]
        else:
            return [text]
    
    def _process_page(self, page_text: str, page_num: int) -> str:
        """Process a single page"""
        text = page_text
        
        # Remove noise (headers/footers)
        text = self._remove_noise(text)
        
        # Skip empty or nearly empty pages
        if len(text.strip()) < 20:
            return ''
        
        # Apply symbol corrections
        text = self._apply_symbol_corrections(text)
        
        # Detect and format section titles
        text = self._format_sections(text)
        
        # Convert math expressions to LaTeX
        text = self._convert_math_to_latex(text)
        
        # Format lists
        text = self._format_lists(text)
        
        # Clean up whitespace
        text = self._clean_whitespace(text)
        
        return text
    
    def _remove_noise(self, text: str) -> str:
        """Remove page headers, footers, and other noise"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Check against noise patterns
            is_noise = False
            for pattern in self.noise_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    is_noise = True
                    break
            
            if not is_noise:
                # Additional checks for short lines that are likely noise
                stripped = line.strip()
                
                # Skip very short non-meaningful lines
                if len(stripped) <= 3 and not stripped.isalpha():
                    if not stripped in ['*', '-', '#', '##', '###']:
                        continue
                
                # Skip lines that are just numbers (page numbers)
                if stripped.isdigit():
                    continue
                    
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _apply_symbol_corrections(self, text: str) -> str:
        """Apply known symbol corrections using simple string replacement"""
        # First apply longer patterns (to avoid partial matches)
        sorted_corrections = sorted(self.symbol_corrections.items(), key=lambda x: -len(x[0]))
        
        for wrong, correct in sorted_corrections:
            text = text.replace(wrong, correct)
        
        # Apply safe replacements
        for wrong, correct in self.safe_replacements.items():
            text = text.replace(wrong, correct)
        
        return text
    
    def _format_sections(self, text: str) -> str:
        """Format section titles"""
        for pattern, replacement in self.section_patterns:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE | re.IGNORECASE)
        return text
    
    def _convert_math_to_latex(self, text: str) -> str:
        """Convert detected math expressions to LaTeX format"""
        
        # Pattern for standalone equations (on their own line)
        equation_patterns = [
            # Poisson equation variations
            (r'[-—]?\s*[ΔA∆]\s*u\s*=\s*f\s*(?:in|€|∈)?\s*[ΩQ]', r'$$-\\Delta u = f \\quad \\text{in } \\Omega$$'),
            (r'u\s*=\s*0\s*(?:on|€|∈)?\s*[∂∂]?[ΩQ]', r'$$u = 0 \\quad \\text{on } \\partial\\Omega$$'),
            
            # Laplacian definition
            (r'[ΔA∆]\s*u\s*=\s*[∂∂].*?[∂∂]', r'$$\\Delta u = \\frac{\\partial^2 u}{\\partial x^2} + \\frac{\\partial^2 u}{\\partial y^2}$$'),
            
            # Inner product notation
            (r'\(f\s*,\s*g\)\s*:?=\s*∫', r'$$(f,g) := \\int_{\\Omega} f \\cdot g \\, dx$$'),
            
            # Weak formulation
            (r'\(∇u\s*,\s*∇v\)\s*=\s*\(f\s*,\s*v\)', r'$$(\\nabla u, \\nabla v) = (f, v) \\quad \\forall v \\in V$$'),
            
            # Function space V
            (r'V\s*:?=\s*H[₀0]?[¹1]?\s*\([ΩQ]\)', r'$$V := H_0^1(\\Omega)$$'),
            
            # Bilinear form
            (r'a\s*\(\s*u\s*,\s*v\s*\)\s*:?=\s*\(∇u\s*,\s*∇v\)', r'$$a(u,v) := (\\nabla u, \\nabla v)$$'),
            
            # Linear form
            (r'L\s*\(\s*v\s*\)\s*:?=\s*\(f\s*,\s*v\)', r'$$L(v) := (f, v)$$'),
        ]
        
        for pattern, replacement in equation_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Inline math: wrap single variables and simple expressions
        # Variables with subscripts
        text = re.sub(r'\b([uvfgh])_([hijk0-9]+)\b', r'$\1_{\2}$', text)
        
        # Greek letters inline - use simple string replacement instead of regex
        greek_inline = [
            ('Ω', '$\\Omega$'),
            ('∂Ω', '$\\partial\\Omega$'),
            ('∇', '$\\nabla$'),
            ('Δ', '$\\Delta$'),
            ('∈', '$\\in$'),
            ('∀', '$\\forall$'),
            ('→', '$\\rightarrow$'),
            ('ℝ', '$\\mathbb{R}$'),
        ]
        
        for symbol, latex in greek_inline:
            # Only replace if not already in math mode - use simple replace
            if symbol in text:
                # Check if already in math mode by looking for surrounding $
                parts = text.split(symbol)
                new_parts = []
                for i, part in enumerate(parts):
                    new_parts.append(part)
                    if i < len(parts) - 1:
                        # Check if this occurrence is not inside $ $
                        before = ''.join(new_parts)
                        dollar_count = before.count('$')
                        if dollar_count % 2 == 0:  # Not inside math mode
                            new_parts.append(latex)
                        else:
                            new_parts.append(symbol)
                text = ''.join(new_parts)
        
        return text
    
    def _format_lists(self, text: str) -> str:
        """Format bullet points and numbered lists"""
        # Convert various bullet markers to standard markdown
        text = re.sub(r'^[©•◦●○]\s*', '* ', text, flags=re.MULTILINE)
        text = re.sub(r'^\*\s+', '* ', text, flags=re.MULTILINE)
        
        return text
    
    def _clean_whitespace(self, text: str) -> str:
        """Clean up whitespace issues"""
        # Multiple spaces to single
        text = re.sub(r' {2,}', ' ', text)
        
        # Multiple newlines to double
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Trim lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text
    
    def _final_cleanup(self, text: str) -> str:
        """Final cleanup pass"""
        
        # Remove repeated section titles (OCR sometimes duplicates)
        text = re.sub(r'(## [^\n]+)\n+\1', r'\1', text)
        
        # Remove lines that are just artifacts
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            
            # Skip artifact lines
            if any([
                stripped.startswith('∞'),
                'SSS' in stripped,
                'sing=' in stripped,
                '—S-' in stripped,
                'omputing Cen' in stripped,
                'VAVA' in stripped,
                re.match(r'^[\s\-—=~\.]+$', stripped),  # Lines with only punctuation
            ]):
                continue
            
            cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Remove empty sections (sections followed immediately by another section)
        text = re.sub(r'(## [^\n]+)\n+---\n+(?=##)', '', text)
        
        # Ensure proper spacing around headers
        text = re.sub(r'\n+(#{1,3} )', r'\n\n\1', text)
        text = re.sub(r'^(#{1,3} [^\n]+)\n(?!\n)', r'\1\n\n', text, flags=re.MULTILINE)
        
        # Clean up multiple dashes/separators
        text = re.sub(r'\n---\n+---\n', '\n---\n', text)
        text = re.sub(r'---+', '---', text)
        
        # Remove excessive blank lines
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def _format_equation(self, match) -> str:
        """Format a detected equation"""
        lhs = match.group(1)
        rhs = match.group(2)
        return f"${lhs} = {rhs}$"
    
    def _format_integral(self, match) -> str:
        """Format an integral expression"""
        return r"$\int$"
    
    def _format_partial(self, match) -> str:
        """Format a partial derivative"""
        var = match.group(1)
        return rf"$\partial {var}$"
    
    def _format_sum(self, match) -> str:
        """Format a summation"""
        return r"$\sum$"


class AdvancedMathOCR:
    """
    Advanced OCR processor that combines multiple techniques:
    1. High-resolution OCR
    2. Math symbol detection
    3. Structure analysis
    4. LaTeX conversion
    """
    
    def __init__(self):
        self.processor = MathOCRProcessor()
        self._setup_tesseract()
    
    def _setup_tesseract(self):
        """Setup Tesseract with optimal settings for math"""
        try:
            import pytesseract
            import os
            
            tesseract_paths = [
                r'D:\APPS\OCR Tesseract\tesseract.exe',
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            ]
            
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    self.tesseract_available = True
                    return
            
            self.tesseract_available = False
        except ImportError:
            self.tesseract_available = False
    
    def process_pdf(self, pdf_path: str, output_path: str = None, **options) -> Tuple[str, Dict]:
        """
        Process a PDF with advanced math OCR
        
        Args:
            pdf_path: Path to PDF file
            output_path: Optional output path for Markdown
            options:
                dpi: OCR resolution (default: 300)
                lang: OCR language (default: 'eng')
                enhance_math: Enable math enhancement (default: True)
                
        Returns:
            Tuple of (markdown_content, metadata)
        """
        import fitz
        import pytesseract
        from PIL import Image
        
        dpi = options.get('dpi', 300)
        lang = options.get('lang', 'eng')
        enhance_math = options.get('enhance_math', True)
        
        logger.info(f"Processing PDF with AdvancedMathOCR: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        metadata = doc.metadata or {}
        title = metadata.get('title', '') or Path(pdf_path).stem.replace('_', ' ')
        
        all_text = []
        
        # Calculate DPI multiplier (72 DPI is default for PDF)
        dpi_multiplier = dpi / 72
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # High-resolution rendering
            matrix = fitz.Matrix(dpi_multiplier, dpi_multiplier)
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # OCR with optimized settings
            custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
            text = pytesseract.image_to_string(img, lang=lang, config=custom_config)
            
            all_text.append(f"## Page {page_num + 1}\n\n{text}")
        
        doc.close()
        
        # Combine all pages
        raw_text = '\n\n---\n\n'.join(all_text)
        
        # Apply math processing if enabled
        if enhance_math:
            processed_text = self.processor.process(raw_text, title=title)
        else:
            processed_text = f"# {title}\n\n{raw_text}"
        
        # Save if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
            logger.info(f"Saved processed output to: {output_path}")
        
        return processed_text, {
            'title': title,
            'pages': len(doc) if 'doc' in dir() else 0,
            'method': 'advanced_math_ocr',
            'dpi': dpi,
            'lang': lang,
            'enhanced': enhance_math
        }
