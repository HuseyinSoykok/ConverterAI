"""
Mathematical Formula Recognition and LaTeX Conversion
Converts OCR text containing math symbols to proper LaTeX format
"""
import re
from typing import Dict, List, Any, Optional, Tuple
from utils.logger import logger


class MathRecognizer:
    """
    Recognize mathematical formulas and convert to LaTeX
    
    Features:
    - Symbol replacement (OCR errors → LaTeX)
    - Formula pattern recognition
    - Inline vs display math detection
    - LaTeX code generation
    """
    
    def __init__(self):
        """Initialize math recognizer with symbol mappings"""
        
        # OCR error → LaTeX symbol mapping
        self.symbol_map = {
            # Greek letters
            'α': r'\alpha',
            'β': r'\beta',
            'γ': r'\gamma',
            'δ': r'\delta',
            'ε': r'\epsilon',
            'θ': r'\theta',
            'λ': r'\lambda',
            'μ': r'\mu',
            'π': r'\pi',
            'σ': r'\sigma',
            'ω': r'\omega',
            
            # Operators
            '∫': r'\int',
            '∑': r'\sum',
            '∏': r'\prod',
            '√': r'\sqrt',
            '∞': r'\infty',
            '∂': r'\partial',
            
            # Relations
            '≈': r'\approx',
            '≠': r'\neq',
            '≤': r'\leq',
            '≥': r'\geq',
            '±': r'\pm',
            '∈': r'\in',
            '∉': r'\notin',
            '⊂': r'\subset',
            '⊃': r'\supset',
            
            # Arrows
            '→': r'\rightarrow',
            '←': r'\leftarrow',
            '↔': r'\leftrightarrow',
            '⇒': r'\Rightarrow',
            '⇐': r'\Leftarrow',
            
            # Other
            '×': r'\times',
            '÷': r'\div',
            '°': r'^\circ',
            '∅': r'\emptyset'
        }
    
    def recognize_formulas(self, text: str) -> List[Dict[str, Any]]:
        """
        Recognize mathematical formulas in text
        
        Args:
            text: Input text with potential math
        
        Returns:
            List of detected formula dictionaries
        """
        formulas = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Check if line contains math symbols
            if self._contains_math(line):
                formula_type = self._classify_formula(line)
                latex = self._convert_to_latex(line)
                
                formulas.append({
                    'line': i,
                    'text': line,
                    'latex': latex,
                    'type': formula_type,
                    'inline': len(line) < 80 and formula_type != 'equation'
                })
        
        logger.info(f"Recognized {len(formulas)} mathematical formulas")
        return formulas
    
    def _contains_math(self, text: str) -> bool:
        """Check if text contains mathematical notation"""
        # Math symbols
        math_chars = set('∫∑∏√∞∂≈≠≤≥±∈∉×÷αβγδεθλμπσω')
        if any(char in text for char in math_chars):
            return True
        
        # Superscripts/subscripts
        if re.search(r'[a-zA-Z]\^?\d|[a-zA-Z]²|[a-zA-Z]³', text):
            return True
        
        # Common math functions
        math_functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'lim', 'int', 'sum']
        if any(func in text.lower() for func in math_functions):
            return True
        
        # Fractions
        if re.search(r'\d+/\d+|\w+/\w+', text):
            return True
        
        return False
    
    def _classify_formula(self, text: str) -> str:
        """
        Classify type of mathematical formula
        
        Returns:
            'equation', 'integral', 'sum', 'limit', 'trigonometry', 'algebra', 'other'
        """
        text_lower = text.lower()
        
        if '=' in text:
            return 'equation'
        elif '∫' in text or 'int' in text_lower:
            return 'integral'
        elif '∑' in text or 'sum' in text_lower:
            return 'sum'
        elif 'lim' in text_lower:
            return 'limit'
        elif any(f in text_lower for f in ['sin', 'cos', 'tan']):
            return 'trigonometry'
        elif re.search(r'[a-z]\^?\d', text):
            return 'algebra'
        else:
            return 'other'
    
    def _convert_to_latex(self, text: str) -> str:
        """
        Convert mathematical text to LaTeX
        
        Args:
            text: Input math text
        
        Returns:
            LaTeX formatted string
        """
        latex = text
        
        # 1. Replace Unicode symbols with LaTeX commands
        for symbol, latex_cmd in self.symbol_map.items():
            latex = latex.replace(symbol, latex_cmd)
        
        # 2. Handle superscripts (x², x³, x^2, etc.)
        latex = re.sub(r'([a-zA-Z])²', r'\1^{2}', latex)
        latex = re.sub(r'([a-zA-Z])³', r'\1^{3}', latex)
        latex = re.sub(r'([a-zA-Z])\^(\d+)', r'\1^{\2}', latex)
        
        # 3. Handle subscripts (x_1, x_n, etc.)
        latex = re.sub(r'([a-zA-Z])_(\w+)', r'\1_{\2}', latex)
        
        # 4. Handle square roots
        # √16 → \sqrt{16}
        latex = re.sub(r'\\sqrt\s*(\d+)', r'\\sqrt{\1}', latex)
        # √(expression) → \sqrt{expression}
        latex = re.sub(r'\\sqrt\s*\(([^)]+)\)', r'\\sqrt{\1}', latex)
        
        # 5. Handle fractions
        # a/b → \frac{a}{b} (only for simple fractions)
        latex = re.sub(r'(\w+)/(\w+)', r'\\frac{\1}{\2}', latex)
        
        # 6. Handle integrals
        # ∫x dx → \int x \, dx
        if r'\int' in latex:
            latex = latex.replace('dx', r'\, dx')
            latex = latex.replace('dy', r'\, dy')
            latex = latex.replace('dt', r'\, dt')
        
        # 7. Handle limits
        # lim(x→0) → \lim_{x \to 0}
        latex = re.sub(r'lim\s*\(([a-z])\s*→\s*(\d+)\)', r'\\lim_{\1 \\to \2}', latex)
        
        # 8. Handle summations
        # ∑(n=1 to ∞) → \sum_{n=1}^{\infty}
        if r'\sum' in latex:
            latex = re.sub(
                r'\\sum\s*\(([a-z])=(\d+)\s+to\s+\\infty\)',
                r'\\sum_{\1=\2}^{\\infty}',
                latex
            )
        
        # 9. Add spacing around operators
        latex = re.sub(r'([a-zA-Z\d])([\+\-])', r'\1 \2 ', latex)
        latex = re.sub(r'([\+\-])([a-zA-Z\d])', r'\1 \2', latex)
        
        # 10. Clean up multiple spaces
        latex = re.sub(r'\s+', ' ', latex).strip()
        
        return latex
    
    def format_for_markdown(self, formulas: List[Dict[str, Any]], original_text: str) -> str:
        """
        Format formulas for Markdown with LaTeX
        
        Args:
            formulas: List of detected formulas
            original_text: Original text
        
        Returns:
            Markdown text with LaTeX math notation
        """
        lines = original_text.split('\n')
        output_lines = []
        
        formula_lines = {f['line']: f for f in formulas}
        
        for i, line in enumerate(lines):
            if i in formula_lines:
                formula = formula_lines[i]
                if formula['inline']:
                    # Inline math: $...$
                    output_lines.append(f"${formula['latex']}$")
                else:
                    # Display math: $$...$$
                    output_lines.append(f"$${formula['latex']}$$")
            else:
                output_lines.append(line)
        
        return '\n'.join(output_lines)
    
    def generate_latex_document(self, formulas: List[Dict[str, Any]], title: str = "Mathematical Formulas") -> str:
        """
        Generate complete LaTeX document
        
        Args:
            formulas: List of formulas
            title: Document title
        
        Returns:
            Complete LaTeX document string
        """
        latex_doc = [
            r'\documentclass{article}',
            r'\usepackage{amsmath}',
            r'\usepackage{amssymb}',
            r'\begin{document}',
            f'\\title{{{title}}}',
            r'\maketitle',
            ''
        ]
        
        # Group formulas by type
        by_type = {}
        for formula in formulas:
            ftype = formula['type']
            if ftype not in by_type:
                by_type[ftype] = []
            by_type[ftype].append(formula)
        
        # Add formulas by section
        for ftype, formulas_list in sorted(by_type.items()):
            latex_doc.append(f'\\section{{{ftype.title()}}}')
            latex_doc.append('')
            
            for formula in formulas_list:
                if formula['inline']:
                    latex_doc.append(f"${formula['latex']}$")
                else:
                    latex_doc.append(r'\begin{equation}')
                    latex_doc.append(formula['latex'])
                    latex_doc.append(r'\end{equation}')
                latex_doc.append('')
        
        latex_doc.extend([
            r'\end{document}'
        ])
        
        return '\n'.join(latex_doc)
    
    def enhance_ocr_math(self, text: str) -> str:
        """
        Apply additional corrections specific to mathematical OCR errors
        
        Args:
            text: OCR text with potential errors
        
        Returns:
            Corrected text
        """
        corrections = {
            # Common OCR misreads in math context
            'x7': 'x²',
            'x?': 'x²',
            'b?': 'b²',
            'a?': 'a²',
            'n?': 'n²',
            '/2a': '/ 2a',
            'V(': '√(',
            'N16': '√16',
            'T=': 'π =',
            'T ': 'π ',
            '~ ': '∞ ',
            'J ': '∫ ',
            '> ': '∑ ',
            'lim(x—': 'lim(x→',
            'lim(x-': 'lim(x→',
            'sin?': 'sin²',
            'cos?': 'cos²',
            'tan?': 'tan²',
            # Spacing issues
            'x*t*': 'x² +',
            'X*t*': 'x² +',
        }
        
        enhanced = text
        for wrong, correct in corrections.items():
            enhanced = enhanced.replace(wrong, correct)
        
        return enhanced
