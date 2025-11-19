"""
Unit tests for PostProcessor module
Tests mojibake fixing, whitespace normalization, and content cleanup
"""

import unittest
from utils.post_processor import PostProcessor, apply_post_processing


class TestPostProcessor(unittest.TestCase):
    """Test suite for PostProcessor functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = PostProcessor()
    
    # ==================== MOJIBAKE TESTS ====================
    
    def test_fix_mojibake_turkish_characters(self):
        """Test Turkish character mojibake fixes"""
        test_cases = [
            ("Ã§", "ç"),
            ("ÄŸ", "ğ"),
            ("Ä±", "ı"),
            ("Å", "ş"),
            ("Ã¼", "ü"),
            ("Ã¶", "ö"),
        ]
        
        for mojibake, expected in test_cases:
            with self.subTest(mojibake=mojibake):
                result = self.processor.fix_mojibake(f"Test {mojibake} text")
                self.assertEqual(result, f"Test {expected} text")
    
    def test_fix_mojibake_windows_1252(self):
        """Test Windows-1252 encoding fixes"""
        test_cases = [
            ("â€™", "'"),  # Right single quotation mark
            ("â€œ", '"'),  # Left double quotation mark
            ("â€", '"'),   # Right double quotation mark
        ]
        
        for mojibake, expected in test_cases:
            with self.subTest(mojibake=mojibake):
                result = self.processor.fix_mojibake(f"Test {mojibake} text")
                self.assertEqual(result, f"Test {expected} text")
    
    def test_fix_mojibake_latin1(self):
        """Test Latin-1 encoding fixes"""
        test_cases = [
            ("Ã©", "é"),
            ("Ã¡", "á"),
            ("Ã³", "ó"),
            ("Ã±", "ñ"),
        ]
        
        for mojibake, expected in test_cases:
            with self.subTest(mojibake=mojibake):
                result = self.processor.fix_mojibake(f"Test {mojibake} text")
                self.assertEqual(result, f"Test {expected} text")
    
    def test_fix_mojibake_multiple_occurrences(self):
        """Test fixing multiple mojibake patterns in one text"""
        input_text = "Türkçe karakterler: Ã§, ÄŸ, Ä±, Å, Ã¼, Ã¶"
        expected = "Türkçe karakterler: ç, ğ, ı, ş, ü, ö"
        result = self.processor.fix_mojibake(input_text)
        self.assertEqual(result, expected)
    
    def test_fix_mojibake_mixed_languages(self):
        """Test fixing mixed language mojibake"""
        input_text = "Café, naïve, and Türkçe: â€™ and Ã§"
        result = self.processor.fix_mojibake(input_text)
        self.assertIn("'", result)
        self.assertIn("ç", result)
    
    # ==================== WHITESPACE TESTS ====================
    
    def test_normalize_whitespace_trailing_spaces(self):
        """Test removal of trailing spaces"""
        input_text = "Line 1   \nLine 2  \nLine 3"
        expected = "Line 1\nLine 2\nLine 3"
        result = self.processor.normalize_whitespace(input_text)
        self.assertEqual(result, expected)
    
    def test_normalize_whitespace_excessive_breaks(self):
        """Test normalization of excessive line breaks"""
        input_text = "Line 1\n\n\n\n\nLine 2"
        expected = "Line 1\n\nLine 2"
        result = self.processor.normalize_whitespace(input_text)
        self.assertEqual(result, expected)
    
    def test_normalize_whitespace_zero_width_chars(self):
        """Test removal of zero-width characters"""
        input_text = "Test\u200bwith\u200czero\u200dwidth\ufeffchars"
        expected = "Testwithzerowidthchars"
        result = self.processor.normalize_whitespace(input_text)
        self.assertEqual(result, expected)
    
    def test_normalize_whitespace_mixed_indentation(self):
        """Test handling of mixed tabs/spaces"""
        input_text = "Line 1\n\tLine 2\n    Line 3"
        result = self.processor.normalize_whitespace(input_text)
        # Should not have trailing spaces
        for line in result.split('\n'):
            self.assertEqual(line, line.rstrip())
    
    # ==================== MARKDOWN CLEANUP TESTS ====================
    
    def test_clean_markdown_html_comments(self):
        """Test removal of HTML comments"""
        input_text = "Content <!-- This is a comment --> More content"
        expected = "Content  More content"
        result = self.processor.clean_markdown(input_text)
        self.assertEqual(result, expected)
    
    def test_clean_markdown_link_spacing(self):
        """Test fixing broken links"""
        input_text = "This is a [link] (url) and another [link](url)"
        result = self.processor.clean_markdown(input_text)
        # Both should be proper markdown links
        self.assertIn("[link](url)", result)
        # Should not have space between ] and (
        self.assertNotIn("] (", result)
    
    def test_clean_markdown_heading_spacing(self):
        """Test proper heading spacing"""
        input_text = "##Heading\n###Another"
        expected = "## Heading\n### Another"
        result = self.processor.clean_markdown(input_text)
        self.assertEqual(result, expected)
    
    def test_clean_markdown_code_blocks(self):
        """Test code block formatting"""
        input_text = "```python\ncode\n```\n\n```javascript\nmore code\n```"
        result = self.processor.clean_markdown(input_text)
        # Code blocks should be preserved
        self.assertIn("```python", result)
        self.assertIn("```javascript", result)
    
    # ==================== HTML CLEANUP TESTS ====================
    
    def test_clean_html_empty_tags(self):
        """Test removal of empty HTML tags"""
        input_text = "<p>Content</p><p></p><div></div><p>More</p>"
        result = self.processor.clean_html(input_text)
        # Empty tags should be removed
        self.assertNotIn("<p></p>", result)
        self.assertNotIn("<div></div>", result)
        # Content should be preserved
        self.assertIn("<p>Content</p>", result)
        self.assertIn("<p>More</p>", result)
    
    def test_clean_html_self_closing_tags(self):
        """Test fixing self-closing div tags"""
        input_text = "<div/>Content<div>More</div>"
        result = self.processor.clean_html(input_text)
        # Should fix self-closing divs
        self.assertIn("<div></div>", result)
        self.assertNotIn("<div/>", result)
    
    # ==================== HEADING HIERARCHY TESTS ====================
    
    def test_validate_heading_hierarchy_multiple_h1(self):
        """Test detection of multiple H1 headings"""
        html = "<h1>First</h1><p>Content</p><h1>Second</h1><h1>Third</h1>"
        issues = self.processor.validate_heading_hierarchy(html, 'html')
        
        # Should detect 3 H1s (2 extras)
        h1_issues = [i for i in issues if 'Multiple H1' in i['description']]
        self.assertEqual(len(h1_issues), 1)
        self.assertIn('3 H1', h1_issues[0]['description'])
    
    def test_validate_heading_hierarchy_skipped_level(self):
        """Test detection of skipped heading levels"""
        html = "<h1>Title</h1><h3>Skipped H2</h3>"
        issues = self.processor.validate_heading_hierarchy(html, 'html')
        
        # Should detect skipped level
        skip_issues = [i for i in issues if 'Skipped' in i['description']]
        self.assertEqual(len(skip_issues), 1)
    
    def test_validate_heading_hierarchy_correct_structure(self):
        """Test valid heading hierarchy"""
        html = "<h1>Title</h1><h2>Section</h2><h3>Subsection</h3>"
        issues = self.processor.validate_heading_hierarchy(html, 'html')
        
        # Should only report multiple H1 if any
        self.assertTrue(len(issues) <= 1)
    
    def test_fix_heading_hierarchy_downgrade_h1(self):
        """Test automatic H1 downgrading"""
        html = "<h1>First</h1><p>Content</p><h1>Second</h1>"
        result = self.processor.fix_heading_hierarchy(html, 'html')
        
        # First H1 should remain, second should become H2
        self.assertEqual(result.count('<h1>'), 1)
        self.assertIn('<h2>Second</h2>', result)
    
    def test_fix_heading_hierarchy_markdown(self):
        """Test H1 fixing in markdown"""
        md = "# First\nContent\n# Second\n# Third"
        result = self.processor.fix_heading_hierarchy(md, 'markdown')
        
        # First should remain H1, others become H2
        lines = result.split('\n')
        h1_count = sum(1 for line in lines if line.startswith('# ') and not line.startswith('## '))
        self.assertEqual(h1_count, 1)
    
    # ==================== INTEGRATION TESTS ====================
    
    def test_process_complete_pipeline(self):
        """Test complete processing pipeline"""
        input_text = """
# Heading1   
## Heading2  

This has mojibake: â€™ and Ã§

Multiple    spaces    here.


Too many breaks above.

<!-- HTML comment -->

[Link] (broken)
        """
        
        result = self.processor.process(input_text, 'markdown')
        
        # Should fix mojibake
        self.assertIn("'", result)
        self.assertIn("ç", result)
        
        # Should normalize whitespace
        self.assertNotIn("Multiple    spaces", result)
        
        # Should remove HTML comments
        self.assertNotIn("<!--", result)
        
        # Should fix broken links
        self.assertIn("[Link](broken)", result)
    
    def test_apply_post_processing_convenience_function(self):
        """Test convenience function"""
        input_text = "Test â€™ text with   spaces"
        result = apply_post_processing(input_text, 'text')
        
        # Should apply all fixes
        self.assertIn("'", result)
        self.assertNotIn("â€™", result)
    
    def test_process_html_complete(self):
        """Test HTML processing pipeline"""
        html = """
        <html>
        <body>
        <h1>Title</h1>
        <p>Content with â€™ mojibake</p>
        <p></p>
        <div/>
        <h1>Extra H1</h1>
        </body>
        </html>
        """
        
        result = self.processor.process(html, 'html')
        
        # Should fix mojibake
        self.assertIn("'", result)
        
        # Should remove empty tags
        self.assertNotIn("<p></p>", result)
        
        # Should fix self-closing divs
        self.assertNotIn("<div/>", result)
        
        # Should downgrade extra H1
        h1_count = result.count('<h1>')
        self.assertEqual(h1_count, 1)
    
    def test_process_preserves_valid_content(self):
        """Test that processing doesn't break valid content"""
        valid_md = """
# Main Title

This is a paragraph with **bold** and *italic* text.

## Section 1

- List item 1
- List item 2

## Section 2

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |

```python
def hello():
    print("Hello World")
```
        """
        
        result = self.processor.process(valid_md, 'markdown')
        
        # Should preserve all markdown structures
        self.assertIn("# Main Title", result)
        self.assertIn("**bold**", result)
        self.assertIn("*italic*", result)
        self.assertIn("- List item", result)
        self.assertIn("| Column", result)
        self.assertIn("```python", result)
    
    # ==================== EDGE CASES ====================
    
    def test_empty_input(self):
        """Test handling of empty input"""
        result = self.processor.process("", 'text')
        self.assertEqual(result, "")
    
    def test_whitespace_only(self):
        """Test handling of whitespace-only input"""
        result = self.processor.process("   \n\n\n   ", 'text')
        # Should normalize to minimal whitespace
        self.assertTrue(len(result) < 20)
    
    def test_no_issues_input(self):
        """Test handling of already clean input"""
        clean_text = "This is clean text.\nWith proper formatting.\n\nAnd correct spacing."
        result = self.processor.process(clean_text, 'text')
        # Should remain very similar
        self.assertEqual(result.strip(), clean_text.strip())
    
    def test_mixed_file_type_handling(self):
        """Test handling of different file types"""
        text = "Test content with   spaces"
        
        # All types should normalize whitespace
        for file_type in ['markdown', 'html', 'text']:
            with self.subTest(file_type=file_type):
                result = self.processor.process(text, file_type)
                self.assertNotIn("   ", result)


if __name__ == '__main__':
    unittest.main()
