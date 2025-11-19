"""
Comprehensive QA Test Suite for ConverterAI
============================================
Test Strategy: Deep Analysis of Data Integrity, Structural Fidelity, and AI Logic

Date: November 19, 2025
QA Lead: Senior Test Engineer
"""

import os
import re
from typing import Dict, List, Tuple
from converters.universal import UniversalConverter
from converters.markdown_converter import MarkdownConverter
from converters.html_converter import HTMLConverter
from converters.pdf_converter import PDFConverter
from converters.docx_converter import DOCXConverter

# Import python-docx for proper DOCX reading
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("WARNING: python-docx not installed. DOCX testing will be limited.")

class ComprehensiveQATest:
    """
    Comprehensive Quality Assurance Test Suite
    Tests all conversion paths with deep inspection
    """
    
    def __init__(self):
        self.test_files = {
            'html': 'test_comprehensive.html',
            'md': 'test_comprehensive.md',
            'pdf': 'test_comprehensive.pdf',
            'docx': 'test_comprehensive.docx'
        }
        
        self.results = {
            'encoding_issues': [],
            'ghost_characters': [],
            'data_loss': [],
            'table_structure': [],
            'heading_hierarchy': [],
            'layout_whitespace': [],
            'list_structure': [],
            'ai_scoring': [],
            'over_processing': []
        }
        
        self.conversion_matrix = []
        
    def test_1_encoding_integrity(self, content: str, file_type: str) -> Dict:
        """
        Test 1: Character Encoding & Mojibake Detection
        """
        print(f"\n{'='*80}")
        print(f"TEST 1: ENCODING INTEGRITY - {file_type.upper()}")
        print(f"{'='*80}")
        
        issues = []
        
        # Check for BOM (Byte Order Mark)
        if content.startswith('\ufeff') or content.startswith('\\ufeff'):
            issues.append({
                'type': 'BOM_DETECTED',
                'severity': 'MEDIUM',
                'location': 'Start of file',
                'description': 'UTF-8 BOM marker detected - may cause display issues'
            })
        
        # Check for mojibake patterns
        mojibake_patterns = [
            r'â€™',  # Right single quotation mark
            r'â€œ',  # Left double quotation mark
            r'â€',   # Right double quotation mark
            r'Â',    # Non-breaking space
            r'Ã',    # Various accented characters
            r'â',    # Various special characters
            r'•',    # Bullet (if not intended)
            r'\ufffd'  # Replacement character
        ]
        
        for pattern in mojibake_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                context_start = max(0, match.start() - 30)
                context_end = min(len(content), match.end() + 30)
                context = content[context_start:context_end]
                
                issues.append({
                    'type': 'MOJIBAKE',
                    'severity': 'HIGH',
                    'pattern': pattern,
                    'location': f'Position {match.start()}',
                    'context': context.replace('\n', ' ')
                })
        
        # Check for encoding declaration mismatches (HTML)
        if file_type == 'html':
            if 'charset=' in content:
                charset_match = re.search(r'charset=["\']?([^"\'>\s]+)', content)
                if charset_match and charset_match.group(1).lower() != 'utf-8':
                    issues.append({
                        'type': 'CHARSET_MISMATCH',
                        'severity': 'HIGH',
                        'declared': charset_match.group(1),
                        'expected': 'utf-8'
                    })
        
        # Check for ASCII control characters (except newline, tab, carriage return)
        control_chars = re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', content)
        if control_chars:
            issues.append({
                'type': 'CONTROL_CHARACTERS',
                'severity': 'MEDIUM',
                'count': len(control_chars),
                'characters': list(set(control_chars))
            })
        
        print(f"\nEncoding Issues Found: {len(issues)}")
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['type']} - Severity: {issue['severity']}")
            for key, value in issue.items():
                if key not in ['type', 'severity']:
                    print(f"   {key}: {value}")
        
        return {'issues': issues, 'score': max(0, 100 - len(issues) * 10)}
    
    def test_2_ghost_characters(self, content: str, file_type: str) -> Dict:
        """
        Test 2: Ghost Characters & Whitespace Anomalies
        """
        print(f"\n{'='*80}")
        print(f"TEST 2: GHOST CHARACTERS - {file_type.upper()}")
        print(f"{'='*80}")
        
        issues = []
        
        # Check for multiple consecutive spaces
        multi_spaces = re.findall(r' {3,}', content)
        if multi_spaces:
            issues.append({
                'type': 'EXCESSIVE_SPACES',
                'severity': 'LOW',
                'count': len(multi_spaces),
                'max_consecutive': max(len(s) for s in multi_spaces)
            })
        
        # Check for trailing whitespace
        trailing_spaces = re.findall(r' +\n', content)
        if trailing_spaces:
            issues.append({
                'type': 'TRAILING_SPACES',
                'severity': 'LOW',
                'count': len(trailing_spaces)
            })
        
        # Check for mixed tabs and spaces
        if '\t' in content and '  ' in content:
            tab_count = content.count('\t')
            space_count = content.count('  ')
            issues.append({
                'type': 'MIXED_INDENTATION',
                'severity': 'MEDIUM',
                'tabs': tab_count,
                'double_spaces': space_count
            })
        
        # Check for excessive line breaks
        excessive_breaks = re.findall(r'\n{4,}', content)
        if excessive_breaks:
            issues.append({
                'type': 'EXCESSIVE_LINE_BREAKS',
                'severity': 'MEDIUM',
                'count': len(excessive_breaks),
                'max_consecutive': max(b.count('\n') for b in excessive_breaks)
            })
        
        # Check for zero-width characters
        zero_width_chars = [
            '\u200b',  # Zero-width space
            '\u200c',  # Zero-width non-joiner
            '\u200d',  # Zero-width joiner
            '\ufeff'   # Zero-width no-break space (BOM)
        ]
        
        for char in zero_width_chars:
            count = content.count(char)
            if count > 0:
                issues.append({
                    'type': 'ZERO_WIDTH_CHARACTER',
                    'severity': 'HIGH',
                    'character': repr(char),
                    'count': count
                })
        
        print(f"\nGhost Character Issues Found: {len(issues)}")
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['type']} - Severity: {issue['severity']}")
            for key, value in issue.items():
                if key not in ['type', 'severity']:
                    print(f"   {key}: {value}")
        
        return {'issues': issues, 'score': max(0, 100 - len(issues) * 5)}
    
    def test_3_data_loss(self, original_content: str, converted_content: str, 
                        conversion_type: str) -> Dict:
        """
        Test 3: Data Loss Detection
        """
        print(f"\n{'='*80}")
        print(f"TEST 3: DATA LOSS - {conversion_type}")
        print(f"{'='*80}")
        
        issues = []
        
        # Count words (simple approach)
        original_words = len(re.findall(r'\w+', original_content))
        converted_words = len(re.findall(r'\w+', converted_content))
        
        word_loss_pct = ((original_words - converted_words) / original_words * 100) if original_words > 0 else 0
        
        if word_loss_pct > 5:
            issues.append({
                'type': 'WORD_COUNT_LOSS',
                'severity': 'HIGH',
                'original': original_words,
                'converted': converted_words,
                'loss_percentage': f"{word_loss_pct:.2f}%"
            })
        elif word_loss_pct > 2:
            issues.append({
                'type': 'WORD_COUNT_LOSS',
                'severity': 'MEDIUM',
                'original': original_words,
                'converted': converted_words,
                'loss_percentage': f"{word_loss_pct:.2f}%"
            })
        
        # Count paragraphs
        original_paragraphs = len(re.findall(r'\n\s*\n', original_content))
        converted_paragraphs = len(re.findall(r'\n\s*\n', converted_content))
        
        if abs(original_paragraphs - converted_paragraphs) > original_paragraphs * 0.1:
            issues.append({
                'type': 'PARAGRAPH_COUNT_MISMATCH',
                'severity': 'MEDIUM',
                'original': original_paragraphs,
                'converted': converted_paragraphs
            })
        
        # Check for truncated sentences (sentences ending without punctuation)
        truncated = re.findall(r'[a-z]\n', converted_content)
        if len(truncated) > 5:
            issues.append({
                'type': 'TRUNCATED_SENTENCES',
                'severity': 'HIGH',
                'count': len(truncated),
                'examples': truncated[:3]
            })
        
        print(f"\nData Loss Issues Found: {len(issues)}")
        print(f"Word Count: {original_words} -> {converted_words} ({word_loss_pct:.2f}% loss)")
        print(f"Paragraphs: {original_paragraphs} -> {converted_paragraphs}")
        
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['type']} - Severity: {issue['severity']}")
            for key, value in issue.items():
                if key not in ['type', 'severity']:
                    print(f"   {key}: {value}")
        
        return {
            'issues': issues, 
            'score': max(0, 100 - len(issues) * 15),
            'word_loss_pct': word_loss_pct
        }
    
    def test_4_table_structure(self, content: str, file_type: str) -> Dict:
        """
        Test 4: Table Structure Integrity
        """
        print(f"\n{'='*80}")
        print(f"TEST 4: TABLE STRUCTURE - {file_type.upper()}")
        print(f"{'='*80}")
        
        issues = []
        tables_found = 0
        
        if file_type == 'md':
            # Markdown tables
            table_pattern = r'\|(.+)\|'
            tables = re.findall(table_pattern, content, re.MULTILINE)
            tables_found = len(set(tables)) // 2  # Rough estimate
            
            # Check for misaligned columns
            table_blocks = re.split(r'\n\s*\n', content)
            for block in table_blocks:
                if '|' in block:
                    lines = [l for l in block.split('\n') if '|' in l]
                    if len(lines) < 2:
                        continue
                    
                    col_counts = [line.count('|') for line in lines]
                    if len(set(col_counts)) > 1:
                        issues.append({
                            'type': 'MISALIGNED_COLUMNS',
                            'severity': 'HIGH',
                            'column_counts': col_counts,
                            'table_preview': lines[0][:50]
                        })
        
        elif file_type == 'html':
            # HTML tables
            table_tags = re.findall(r'<table.*?>', content, re.IGNORECASE | re.DOTALL)
            tables_found = len(table_tags)
            
            # Check for tables without headers
            tables_with_thead = len(re.findall(r'<thead>', content, re.IGNORECASE))
            if tables_found > tables_with_thead:
                issues.append({
                    'type': 'MISSING_TABLE_HEADERS',
                    'severity': 'MEDIUM',
                    'tables_total': tables_found,
                    'tables_with_thead': tables_with_thead
                })
            
            # Check for empty cells
            empty_cells = re.findall(r'<t[dh]>\s*</t[dh]>', content, re.IGNORECASE)
            if len(empty_cells) > 5:
                issues.append({
                    'type': 'EXCESSIVE_EMPTY_CELLS',
                    'severity': 'MEDIUM',
                    'count': len(empty_cells)
                })
        
        print(f"\nTables Found: {tables_found}")
        print(f"Table Structure Issues Found: {len(issues)}")
        
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['type']} - Severity: {issue['severity']}")
            for key, value in issue.items():
                if key not in ['type', 'severity']:
                    print(f"   {key}: {value}")
        
        return {
            'issues': issues,
            'tables_found': tables_found,
            'score': max(0, 100 - len(issues) * 20)
        }
    
    def test_5_heading_hierarchy(self, content: str, file_type: str) -> Dict:
        """
        Test 5: Heading Hierarchy Preservation
        """
        print(f"\n{'='*80}")
        print(f"TEST 5: HEADING HIERARCHY - {file_type.upper()}")
        print(f"{'='*80}")
        
        issues = []
        headings = []
        
        if file_type == 'md':
            # Markdown headings
            heading_matches = re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
            for match in heading_matches:
                level = len(match.group(1))
                text = match.group(2)
                headings.append((level, text))
        
        elif file_type == 'html':
            # HTML headings
            heading_matches = re.finditer(r'<h([1-6])[^>]*>(.*?)</h\1>', content, re.IGNORECASE | re.DOTALL)
            for match in heading_matches:
                level = int(match.group(1))
                text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
                headings.append((level, text))
        
        # Check for skipped levels
        if headings:
            for i in range(len(headings) - 1):
                current_level = headings[i][0]
                next_level = headings[i+1][0]
                
                if next_level - current_level > 1:
                    issues.append({
                        'type': 'SKIPPED_HEADING_LEVEL',
                        'severity': 'MEDIUM',
                        'from_level': current_level,
                        'to_level': next_level,
                        'from_text': headings[i][1][:30],
                        'to_text': headings[i+1][1][:30]
                    })
        
        # Check for multiple H1s
        h1_count = sum(1 for h in headings if h[0] == 1)
        if h1_count > 1:
            issues.append({
                'type': 'MULTIPLE_H1_HEADINGS',
                'severity': 'LOW',
                'count': h1_count,
                'h1_texts': [h[1][:30] for h in headings if h[0] == 1]
            })
        
        print(f"\nHeadings Found: {len(headings)}")
        print(f"Hierarchy Issues Found: {len(issues)}")
        
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['type']} - Severity: {issue['severity']}")
            for key, value in issue.items():
                if key not in ['type', 'severity']:
                    print(f"   {key}: {value}")
        
        return {
            'issues': issues,
            'headings_found': len(headings),
            'heading_distribution': dict((i, sum(1 for h in headings if h[0] == i)) for i in range(1, 7)),
            'score': max(0, 100 - len(issues) * 10)
        }
    
    def run_all_tests(self):
        """
        Execute complete test suite
        """
        print("\n" + "="*80)
        print("CONVERTERAI - COMPREHENSIVE QA TEST SUITE")
        print("="*80)
        
        # Test each file type
        for file_type, filename in self.test_files.items():
            if not os.path.exists(filename):
                print(f"\n⚠️ Warning: {filename} not found, skipping...")
                continue
            
            # Read file with appropriate method
            if file_type == 'docx' and DOCX_AVAILABLE:
                # Use python-docx for proper DOCX reading
                doc = Document(filename)
                content = '\n'.join([para.text for para in doc.paragraphs])
                print(f"✅ Reading {filename} with python-docx (proper DOCX parsing)")
            else:
                # Regular text file reading for HTML, MD, etc.
                with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            
            # Run tests
            encoding_result = self.test_1_encoding_integrity(content, file_type)
            ghost_result = self.test_2_ghost_characters(content, file_type)
            table_result = self.test_4_table_structure(content, file_type)
            heading_result = self.test_5_heading_hierarchy(content, file_type)
            
            # Store results
            self.results['encoding_issues'].extend(encoding_result['issues'])
            self.results['ghost_characters'].extend(ghost_result['issues'])
            self.results['table_structure'].extend(table_result['issues'])
            self.results['heading_hierarchy'].extend(heading_result['issues'])
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """
        Generate comprehensive QA report
        """
        print("\n" + "="*80)
        print("FINAL QA REPORT")
        print("="*80)
        
        total_issues = sum(len(issues) for issues in self.results.values())
        
        print(f"\nTotal Issues Found: {total_issues}")
        print(f"\nBreakdown by Category:")
        for category, issues in self.results.items():
            if issues:
                print(f"  {category.replace('_', ' ').title()}: {len(issues)}")
        
        # Calculate severity distribution
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for issues in self.results.values():
            for issue in issues:
                severity_counts[issue.get('severity', 'UNKNOWN')] += 1
        
        print(f"\nSeverity Distribution:")
        print(f"  🔴 HIGH: {severity_counts['HIGH']}")
        print(f"  🟡 MEDIUM: {severity_counts['MEDIUM']}")
        print(f"  🟢 LOW: {severity_counts['LOW']}")
        
        # Priority recommendations
        print(f"\n{'='*80}")
        print("PRIORITY RECOMMENDATIONS")
        print("="*80)
        
        if severity_counts['HIGH'] > 0:
            print(f"\n🔴 CRITICAL: {severity_counts['HIGH']} high-priority issues require immediate attention")
        
        if severity_counts['MEDIUM'] > 0:
            print(f"\n🟡 IMPORTANT: {severity_counts['MEDIUM']} medium-priority issues should be addressed")
        
        if severity_counts['LOW'] > 0:
            print(f"\n🟢 MINOR: {severity_counts['LOW']} low-priority issues can be addressed in next iteration")

if __name__ == '__main__':
    qa_test = ComprehensiveQATest()
    qa_test.run_all_tests()
