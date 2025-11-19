"""
Post-processing module for content cleanup and quality improvements
"""

import re
from typing import Dict, List, Any
from utils.logger import logger


class PostProcessor:
    """Post-process converted content for quality improvements"""
    
    def __init__(self):
        # Mojibake correction map (encoding corruption patterns)
        self.mojibake_map = {
            # Windows-1252 → UTF-8
            'â€™': "'",
            'â€œ': '"',
            'â€': '"',
            'â€"': '—',
            'â€"': '–',
            'â€¢': '•',
            'â€¦': '…',
            
            # Latin-1 issues
            'Ã©': 'é',
            'Ã¡': 'á',
            'Ã³': 'ó',
            'Ã±': 'ñ',
            'Ã¨': 'è',
            'Ã ': 'à',
            'Ã²': 'ò',
            'Ã¬': 'ì',
            'Ãº': 'ú',
            'Ã£': 'ã',
            'Ãµ': 'õ',
            'Ã§': 'ç',
            
            # Turkish characters
            'Ã§': 'ç',
            'Ã‡': 'Ç',
            'ÄŸ': 'ğ',
            'Ä': 'Ğ',
            'Ä±': 'ı',
            'Ä°': 'İ',
            'Å': 'ş',
            'ÅŸ': 'Ş',
            'Ã¼': 'ü',
            'Ãœ': 'Ü',
            'Ã¶': 'ö',
            'Ã–': 'Ö',
            
            # Common replacements
            'Â': ' ',  # Non-breaking space corruption
        }
    
    def fix_mojibake(self, text: str) -> str:
        """Fix common mojibake (encoding corruption) patterns"""
        fixed_text = text
        fixes_applied = 0
        
        for wrong, correct in self.mojibake_map.items():
            count = fixed_text.count(wrong)
            if count > 0:
                fixed_text = fixed_text.replace(wrong, correct)
                fixes_applied += count
        
        if fixes_applied > 0:
            logger.info(f"Fixed {fixes_applied} mojibake pattern(s)")
        
        return fixed_text
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace characters for consistent formatting"""
        # Remove trailing spaces at end of lines
        text = re.sub(r' +\n', '\n', text)
        
        # Normalize multiple consecutive spaces to single space
        text = re.sub(r' {3,}', ' ', text)
        
        # Normalize excessive line breaks (max 2 consecutive)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove zero-width characters
        zero_width_chars = [
            '\u200b',  # Zero-width space
            '\u200c',  # Zero-width non-joiner
            '\u200d',  # Zero-width joiner
            '\ufeff'   # Zero-width no-break space (BOM)
        ]
        
        for char in zero_width_chars:
            text = text.replace(char, '')
        
        # Remove BOM at start of file
        if text.startswith('\ufeff'):
            text = text[1:]
        
        return text
    
    def clean_markdown(self, md_content: str) -> str:
        """Markdown-specific cleanup and formatting"""
        # Remove stray HTML comments
        md_content = re.sub(r'<!--.*?-->', '', md_content, flags=re.DOTALL)
        
        # Fix malformed links [text] (url) to [text](url)
        md_content = re.sub(
            r'\[([^\]]+)\]\s+\(([^)]+)\)',
            r'[\1](\2)',
            md_content
        )
        
        # Normalize heading spacing: ##Text to ## Text
        md_content = re.sub(
            r'^(#{1,6})([^ #])',
            r'\1 \2',
            md_content,
            flags=re.MULTILINE
        )
        
        return md_content
    
    def clean_html(self, html_content: str) -> str:
        """HTML-specific cleanup and normalization"""
        # Remove empty tags
        html_content = re.sub(
            r'<([a-z][a-z0-9]*)\s*>\s*</\1>',
            '',
            html_content,
            flags=re.IGNORECASE
        )
        
        # Fix self-closing tags that shouldn't be self-closing
        html_content = re.sub(
            r'<(div|span|p|h[1-6])\s*/>',
            r'<\1></\1>',
            html_content,
            flags=re.IGNORECASE
        )
        
        return html_content
    
    def validate_heading_hierarchy(self, content: str, file_type: str) -> List[Dict[str, Any]]:
        """Validate heading hierarchy and detect issues"""
        issues = []
        headings = []
        
        if file_type == 'markdown':
            heading_matches = re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
            for match in heading_matches:
                level = len(match.group(1))
                text = match.group(2)
                headings.append((level, text, match.start()))
        
        elif file_type == 'html':
            heading_matches = re.finditer(
                r'<h([1-6])[^>]*>(.*?)</h\1>',
                content,
                re.IGNORECASE | re.DOTALL
            )
            for match in heading_matches:
                level = int(match.group(1))
                text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
                headings.append((level, text, match.start()))
        
        if not headings:
            return issues
        
        # Check for skipped levels
        for i in range(len(headings) - 1):
            current_level = headings[i][0]
            next_level = headings[i + 1][0]
            
            if next_level - current_level > 1:
                issues.append({
                    'type': 'SKIPPED_HEADING_LEVEL',
                    'severity': 'MEDIUM',
                    'description': f'Skipped from H{current_level} to H{next_level}'
                })
        
        # Check for multiple H1s
        h1_count = sum(1 for h in headings if h[0] == 1)
        if h1_count > 1:
            issues.append({
                'type': 'MULTIPLE_H1_HEADINGS',
                'severity': 'LOW',
                'description': f'Multiple H1 headings found: {h1_count} H1s'
            })
        
        return issues
    
    def fix_heading_hierarchy(self, content: str, file_type: str) -> str:
        """Automatically fix heading hierarchy issues"""
        if file_type == 'html':
            # Downgrade extra H1s to H2
            h1_count = 0
            
            def replace_h1(match):
                nonlocal h1_count
                h1_count += 1
                if h1_count == 1:
                    return match.group(0)
                else:
                    return match.group(0).replace('<h1', '<h2', 1).replace('</h1>', '</h2>', 1)
            
            content = re.sub(
                r'<h1[^>]*>.*?</h1>',
                replace_h1,
                content,
                flags=re.IGNORECASE | re.DOTALL
            )
        
        elif file_type == 'markdown':
            h1_count = 0
            
            def replace_md_h1(match):
                nonlocal h1_count
                h1_count += 1
                if h1_count == 1:
                    return match.group(0)
                else:
                    return '##' + match.group(0)[1:]
            
            content = re.sub(
                r'^#\s+.+$',
                replace_md_h1,
                content,
                flags=re.MULTILINE
            )
        
        return content
    
    def process(self, content: str, file_type: str) -> str:
        """Apply complete post-processing pipeline"""
        # Fix encoding issues
        content = self.fix_mojibake(content)
        
        # Normalize whitespace
        content = self.normalize_whitespace(content)
        
        # Format-specific cleanup
        if file_type == 'markdown':
            content = self.clean_markdown(content)
            content = self.fix_heading_hierarchy(content, 'markdown')
        elif file_type == 'html':
            content = self.clean_html(content)
            content = self.fix_heading_hierarchy(content, 'html')
        
        return content


# Global instance
post_processor = PostProcessor()


def apply_post_processing(content: str, file_type: str) -> str:
    """Convenience function to apply post-processing"""
    return post_processor.process(content, file_type)
