"""
Local AI-based quality checker (FREE - No API keys needed)
Uses HuggingFace Transformers for completely free AI analysis
"""
from typing import Dict, Any, Optional
from pathlib import Path
import re
from utils.logger import logger

# Try to import AI libraries (optional)
try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Sentence Transformers not installed. Install with: pip install sentence-transformers")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class LocalAIChecker:
    """Free local AI quality checker using Transformers"""
    
    def __init__(self, method: str = 'heuristic'):
        """
        Initialize local AI checker
        
        Args:
            method: Quality check method
                - 'heuristic': Rule-based (always available, fast)
                - 'transformers': HuggingFace models (free, good quality)
                - 'ollama': Local LLM (free, best quality if installed)
        """
        self.method = method
        self.model = None
        
        if method == 'transformers' and TRANSFORMERS_AVAILABLE:
            self._init_transformers()
        elif method == 'ollama' and OLLAMA_AVAILABLE:
            self._check_ollama()
    
    def _init_transformers(self):
        """Initialize sentence transformer model (downloads once, ~400MB)"""
        try:
            logger.info("Loading sentence transformer model (first time may take a few minutes)...")
            # Use a lightweight multilingual model
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            logger.info("Sentence transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load transformer model: {e}")
            self.method = 'heuristic'
    
    def _check_ollama(self):
        """Check if Ollama is available"""
        try:
            # Try to list models
            models = ollama.list()
            if models:
                logger.info(f"Ollama available with {len(models)} models")
            else:
                logger.warning("Ollama installed but no models found. Install with: ollama pull llama2")
                self.method = 'heuristic'
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            self.method = 'heuristic'
    
    def check_quality(
        self,
        input_file: str,
        output_file: str,
        input_content: Optional[str] = None,
        output_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check conversion quality using free local AI
        
        Args:
            input_file: Original file path
            output_file: Converted file path
            input_content: Pre-extracted content (optional)
            output_content: Pre-extracted content (optional)
            
        Returns:
            Dictionary with quality metrics
        """
        # Extract content if not provided
        if not input_content:
            input_content = self._extract_sample_content(input_file)
        if not output_content:
            output_content = self._extract_sample_content(output_file)
        
        if not input_content or not output_content:
            return self._heuristic_check(input_file, output_file)
        
        # Route to appropriate method
        if self.method == 'transformers' and self.model:
            result = self._transformers_check(input_content, output_content)
        elif self.method == 'ollama' and OLLAMA_AVAILABLE:
            result = self._ollama_check(input_content, output_content)
        else:
            result = self._heuristic_check_with_content(input_content, output_content)
        
        # Apply format-specific adjustments
        result = self._apply_format_specific_scoring(result, input_file, output_file, input_content, output_content)
        
        return result
    
    def _transformers_check(self, input_content: str, output_content: str) -> Dict[str, Any]:
        """
        Quality check using sentence transformers (FREE!)
        Measures semantic similarity between input and output
        """
        logger.info("Performing transformer-based quality check...")
        
        try:
            # Limit content size
            input_sample = input_content[:2000]
            output_sample = output_content[:2000]
            
            # Get embeddings
            input_embedding = self.model.encode(input_sample, convert_to_tensor=True)
            output_embedding = self.model.encode(output_sample, convert_to_tensor=True)
            
            # Calculate cosine similarity
            similarity = util.pytorch_cos_sim(input_embedding, output_embedding).item()
            
            # Additional metrics
            length_ratio = len(output_content) / len(input_content) if len(input_content) > 0 else 0
            word_count_ratio = len(output_content.split()) / len(input_content.split()) if len(input_content.split()) > 0 else 0
            
            # Check structure preservation
            input_headings = len(re.findall(r'^#{1,6}\s', input_content, re.MULTILINE))
            output_headings = len(re.findall(r'^#{1,6}\s', output_content, re.MULTILINE))
            heading_preservation = min(output_headings / input_headings if input_headings > 0 else 1, 1.0)
            
            # Calculate overall score
            overall_score = (
                similarity * 0.5 +  # Semantic similarity (50%)
                min(length_ratio, 1.0) * 0.2 +  # Length preservation (20%)
                min(word_count_ratio, 1.0) * 0.2 +  # Word count preservation (20%)
                heading_preservation * 0.1  # Structure preservation (10%)
            )
            
            # Generate issues and recommendations
            issues = []
            recommendations = []
            
            if similarity < 0.7:
                issues.append("Semantic content differs significantly from original")
                recommendations.append("Review the conversion for content accuracy")
            
            if length_ratio < 0.5:
                issues.append("Output significantly shorter than input")
                recommendations.append("Check if content was lost during conversion")
            elif length_ratio > 2.0:
                issues.append("Output significantly longer than input")
                recommendations.append("Check for added formatting artifacts")
            
            if heading_preservation < 0.8:
                issues.append("Some headings may not be preserved correctly")
                recommendations.append("Review heading structure in output")
            
            return {
                'score': overall_score,
                'method': 'transformers (free)',
                'metrics': {
                    'semantic_similarity': similarity,
                    'length_ratio': length_ratio,
                    'word_count_ratio': word_count_ratio,
                    'heading_preservation': heading_preservation
                },
                'issues': issues,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Transformer check failed: {e}")
            return self._heuristic_check_with_content(input_content, output_content)
    
    def _ollama_check(self, input_content: str, output_content: str) -> Dict[str, Any]:
        """
        Quality check using Ollama local LLM (FREE!)
        Provides GPT-like analysis without API costs
        """
        logger.info("Performing Ollama-based quality check...")
        
        try:
            # Limit content
            input_sample = input_content[:1500]
            output_sample = output_content[:1500]
            
            prompt = f"""Analyze this document conversion quality. Rate it 0-1.

Original (first 1500 chars):
{input_sample}

Converted (first 1500 chars):
{output_sample}

Provide:
1. Overall quality score (0-1)
2. Issues found
3. Recommendations

Format as JSON:
{{"score": 0.85, "issues": ["list"], "recommendations": ["list"]}}"""
            
            response = ollama.generate(
                model='llama2',  # or any installed model
                prompt=prompt
            )
            
            # Parse response
            import json
            result_text = response.get('response', '{}')
            
            # Try to extract JSON
            try:
                result_data = json.loads(result_text)
                score = float(result_data.get('score', 0.7))
                issues = result_data.get('issues', [])
                recommendations = result_data.get('recommendations', [])
            except:
                # Fallback if JSON parsing fails
                score = 0.75
                issues = ["Ollama analysis completed but format parsing failed"]
                recommendations = ["Review output manually"]
            
            return {
                'score': score,
                'method': 'ollama (free local LLM)',
                'metrics': {
                    'model': 'llama2',
                    'analysis': 'full'
                },
                'issues': issues,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Ollama check failed: {e}")
            return self._heuristic_check_with_content(input_content, output_content)
    
    def _heuristic_check_with_content(self, input_content: str, output_content: str) -> Dict[str, Any]:
        """
        Enhanced heuristic check with content analysis (ALWAYS FREE!)
        No AI needed, just smart algorithms with comprehensive quality metrics
        """
        logger.info("Performing enhanced heuristic quality check...")
        
        score = 1.0
        issues = []
        recommendations = []
        metrics = {}
        
        # 1. Length Analysis (improved tolerance)
        input_len = len(input_content)
        output_len = len(output_content)
        length_ratio = output_len / input_len if input_len > 0 else 0
        metrics['length_ratio'] = length_ratio
        
        # More lenient length checks - HTML/formatting can legitimately increase size
        if length_ratio < 0.2:
            score -= 0.25
            issues.append("Output is significantly shorter than input (>80% content loss)")
            recommendations.append("Check if conversion preserved all content")
        elif length_ratio < 0.5:
            score -= 0.08
            issues.append("Output is noticeably shorter than input")
        elif length_ratio > 5.0:
            score -= 0.15
            issues.append("Output is much longer than input (possible formatting artifacts)")
            recommendations.append("Check for duplicated or added content")
        else:
            # Good length preservation bonus
            score += 0.05
        
        # 2. Word Count Analysis (with better scoring)
        input_words = len(input_content.split())
        output_words = len(output_content.split())
        word_ratio = output_words / input_words if input_words > 0 else 0
        metrics['word_count_ratio'] = word_ratio
        
        # Bonus for good word preservation
        if 0.7 <= word_ratio <= 1.5:
            score += 0.05
        elif word_ratio < 0.5:
            score -= 0.1
            issues.append("Significant word count reduction")
        
        # 3. Paragraph Structure Analysis (NEW!)
        input_paragraphs = len(re.findall(r'\n\s*\n', input_content)) + 1
        output_paragraphs = len(re.findall(r'\n\s*\n|<p>|</p>', output_content))
        
        if input_paragraphs > 2:
            para_ratio = output_paragraphs / input_paragraphs
            metrics['paragraph_preservation'] = para_ratio
            
            if para_ratio >= 0.8:
                score += 0.05  # Bonus for good paragraph structure
            elif para_ratio < 0.5:
                score -= 0.08
                issues.append("Paragraph structure not well preserved")
        
        # 4. Sentence Analysis (NEW!)
        input_sentences = len(re.findall(r'[.!?]+\s', input_content))
        output_sentences = len(re.findall(r'[.!?]+\s', output_content))
        
        if input_sentences > 5:
            sentence_ratio = output_sentences / input_sentences
            metrics['sentence_preservation'] = sentence_ratio
            
            if 0.8 <= sentence_ratio <= 1.2:
                score += 0.05  # Bonus for good sentence preservation
            elif sentence_ratio < 0.6:
                score -= 0.08
                issues.append("Some sentences may be lost or merged")
        
        # 5. Structure Analysis - Headings (improved)
        input_headings = len(re.findall(r'(^#{1,6}\s|<h[1-6][^>]*>|^[A-Z][A-Z\s]{10,60}$)', input_content, re.MULTILINE))
        output_headings = len(re.findall(r'(^#{1,6}\s|<h[1-6][^>]*>)', output_content, re.MULTILINE))
        
        if input_headings > 0:
            heading_ratio = min(output_headings / input_headings, 1.0)
            metrics['heading_preservation'] = heading_ratio
            
            if heading_ratio >= 0.9:
                score += 0.08  # Significant bonus for excellent heading preservation
            elif heading_ratio >= 0.7:
                score += 0.03
            elif heading_ratio < 0.6:
                score -= 0.12
                issues.append(f"Only {heading_ratio*100:.0f}% of headings preserved")
                recommendations.append("Review heading structure")
        
        # 6. Lists (improved detection and scoring)
        input_lists = len(re.findall(r'(^\s*[-*+•]\s|^\s*\d+\.\s|<li[^>]*>|<ul[^>]*>|<ol[^>]*>)', input_content, re.MULTILINE))
        output_lists = len(re.findall(r'(^\s*[-*+•]\s|^\s*\d+\.\s|<li[^>]*>|<ul[^>]*>|<ol[^>]*>)', output_content, re.MULTILINE))
        
        if input_lists > 3:
            list_ratio = min(output_lists / input_lists, 1.0)
            metrics['list_preservation'] = list_ratio
            
            if list_ratio >= 0.9:
                score += 0.05  # Bonus for excellent list preservation
            elif list_ratio >= 0.7:
                score += 0.02
            elif list_ratio < 0.5:
                score -= 0.08
                issues.append("Some list items may be lost")
        
        # 7. Code Blocks (improved)
        input_code = len(re.findall(r'```|<code[^>]*>|<pre[^>]*>|`[^`]+`', input_content))
        output_code = len(re.findall(r'```|<code[^>]*>|<pre[^>]*>|`[^`]+`', output_content))
        
        if input_code > 0:
            code_ratio = min(output_code / input_code, 1.0)
            metrics['code_preservation'] = code_ratio
            
            if code_ratio >= 0.9:
                score += 0.04  # Bonus for code preservation
            elif code_ratio < 0.7:
                score -= 0.08
                issues.append("Code blocks may not be fully preserved")
        
        # 8. Tables (improved)
        input_tables = len(re.findall(r'(\|.*\||\<table[^>]*\>)', input_content))
        output_tables = len(re.findall(r'(\|.*\||\<table[^>]*\>)', output_content))
        
        if input_tables > 0:
            table_ratio = min(output_tables / input_tables, 1.0)
            metrics['table_preservation'] = table_ratio
            
            if table_ratio >= 0.9:
                score += 0.06  # Significant bonus for table preservation
            elif table_ratio >= 0.7:
                score += 0.03
            elif table_ratio < 0.6:
                score -= 0.12
                issues.append("Tables may not be fully converted")
                recommendations.append("Manually check table formatting")
        
        # 9. Formatting Tags Preservation (NEW!)
        input_bold = len(re.findall(r'\*\*[^*]+\*\*|<b[^>]*>|<strong[^>]*>|__[^_]+__', input_content))
        output_bold = len(re.findall(r'\*\*[^*]+\*\*|<b[^>]*>|<strong[^>]*>|__[^_]+__', output_content))
        
        input_italic = len(re.findall(r'\*[^*]+\*|<i[^>]*>|<em[^>]*>|_[^_]+_', input_content))
        output_italic = len(re.findall(r'\*[^*]+\*|<i[^>]*>|<em[^>]*>|_[^_]+_', output_content))
        
        formatting_score = 0
        if input_bold > 0:
            bold_ratio = min(output_bold / input_bold, 1.0)
            formatting_score += bold_ratio * 0.5
            if bold_ratio < 0.6:
                issues.append("Some bold formatting may be lost")
        
        if input_italic > 0:
            italic_ratio = min(output_italic / input_italic, 1.0)
            formatting_score += italic_ratio * 0.5
            if italic_ratio < 0.6:
                issues.append("Some italic formatting may be lost")
        
        if input_bold > 0 or input_italic > 0:
            metrics['formatting_preservation'] = formatting_score
            if formatting_score >= 0.8:
                score += 0.04  # Bonus for formatting preservation
            elif formatting_score < 0.5:
                score -= 0.06
        
        # 10. Unicode and Special Characters (NEW!)
        input_unicode = len(re.findall(r'[^\x00-\x7F]', input_content))
        output_unicode = len(re.findall(r'[^\x00-\x7F]', output_content))
        
        if input_unicode > 10:
            unicode_ratio = output_unicode / input_unicode
            metrics['unicode_preservation'] = unicode_ratio
            
            if unicode_ratio >= 0.9:
                score += 0.03  # Bonus for Unicode preservation
            elif unicode_ratio < 0.5:
                score -= 0.08
                issues.append("Unicode/special characters may be lost")
                recommendations.append("Check character encoding")
        
        # 11. Links/URLs Preservation (NEW!)
        input_links = len(re.findall(r'https?://[^\s<>"\')]+|<a\s+href=', input_content))
        output_links = len(re.findall(r'https?://[^\s<>"\')]+|<a\s+href=', output_content))
        
        if input_links > 0:
            link_ratio = min(output_links / input_links, 1.0)
            metrics['link_preservation'] = link_ratio
            
            if link_ratio >= 0.9:
                score += 0.03
            elif link_ratio < 0.6:
                score -= 0.05
                issues.append("Some links may be lost")
        
        # 12. Images Preservation (NEW!)
        input_images = len(re.findall(r'!\[.*?\]\(.*?\)|<img[^>]*>', input_content))
        output_images = len(re.findall(r'!\[.*?\]\(.*?\)|<img[^>]*>', output_content))
        
        if input_images > 0:
            image_ratio = min(output_images / input_images, 1.0)
            metrics['image_preservation'] = image_ratio
            
            if image_ratio >= 0.9:
                score += 0.03
            elif image_ratio < 0.7:
                score -= 0.05
                issues.append("Some images may be missing")
        
        # 13. Whitespace and Line Breaks (NEW!)
        input_breaks = len(re.findall(r'\n', input_content))
        output_breaks = len(re.findall(r'\n|<br>', output_content))
        
        if input_breaks > 10:
            break_ratio = output_breaks / input_breaks
            metrics['line_break_preservation'] = break_ratio
            
            # Don't penalize too much for line break differences (formatting can change this)
            if break_ratio < 0.3:
                score -= 0.03
                issues.append("Line break structure significantly changed")
        
        # 14. Empty Output Check
        if output_len < 100:
            score = 0.1
            issues.append("Output file is too small")
            recommendations.append("Conversion may have failed")
        elif output_len < 500 and input_len > 5000:
            score -= 0.15
            issues.append("Output is suspiciously small")
        
        # 15. Character Encoding Issues (improved)
        encoding_issues = output_content.count('�') + output_content.count('\ufffd')
        if encoding_issues > 0:
            penalty = min(0.15, encoding_issues * 0.01)
            score -= penalty
            issues.append(f"Character encoding issues detected ({encoding_issues} problematic characters)")
            recommendations.append("Check output file encoding")
        
        # 16. Content Similarity Score (NEW! - Simple n-gram comparison)
        try:
            # Extract 3-grams from both contents (sample for performance)
            def get_ngrams(text, n=3, sample_size=1000):
                text_sample = text[:sample_size]
                words = text_sample.lower().split()
                return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))
            
            input_ngrams = get_ngrams(input_content)
            output_ngrams = get_ngrams(output_content)
            
            if input_ngrams:
                ngram_similarity = len(input_ngrams & output_ngrams) / len(input_ngrams)
                metrics['content_similarity'] = ngram_similarity
                
                if ngram_similarity >= 0.7:
                    score += 0.06  # Significant bonus for content similarity
                elif ngram_similarity >= 0.5:
                    score += 0.03
                elif ngram_similarity < 0.3:
                    score -= 0.08
                    issues.append("Content significantly differs from original")
        except Exception as e:
            logger.debug(f"N-gram comparison failed: {e}")
        
        # 17. HTML Tag Balance Check (NEW! - for HTML outputs)
        if '<html>' in output_content.lower() or '<!doctype' in output_content.lower():
            # Check if basic HTML structure is valid
            open_tags = len(re.findall(r'<(?!/)([a-z][a-z0-9]*)', output_content, re.IGNORECASE))
            close_tags = len(re.findall(r'</([a-z][a-z0-9]*)', output_content, re.IGNORECASE))
            
            tag_balance = min(close_tags / open_tags if open_tags > 0 else 1, 1.0)
            metrics['html_tag_balance'] = tag_balance
            
            if tag_balance >= 0.9:
                score += 0.04  # Bonus for balanced HTML
            elif tag_balance < 0.7:
                score -= 0.06
                issues.append("HTML tag structure may be malformed")
        
        # 18. Quality Bonuses for High Completeness (NEW!)
        completeness_metrics = [
            metrics.get('heading_preservation', 0),
            metrics.get('list_preservation', 0),
            metrics.get('table_preservation', 0),
            metrics.get('code_preservation', 0),
            metrics.get('formatting_preservation', 0)
        ]
        
        # Filter out zero metrics (features not present in input)
        active_metrics = [m for m in completeness_metrics if m > 0]
        
        if active_metrics:
            avg_completeness = sum(active_metrics) / len(active_metrics)
            metrics['avg_feature_preservation'] = avg_completeness
            
            # Significant bonus for high average preservation
            if avg_completeness >= 0.95:
                score += 0.08
            elif avg_completeness >= 0.85:
                score += 0.05
            elif avg_completeness >= 0.75:
                score += 0.02
        
        # Ensure score is in valid range
        score = max(0.0, min(1.0, score))
        
        # Add context-aware recommendations
        if score >= 0.92 and not recommendations:
            recommendations.append("Conversion quality is excellent! All features preserved well.")
        elif score >= 0.85:
            recommendations.append("Conversion quality is very good")
        elif score >= 0.75:
            recommendations.append("Conversion quality is good, minor improvements possible")
        elif score >= 0.65:
            recommendations.append("Conversion quality is acceptable, some features may need review")
        else:
            recommendations.append("Conversion quality needs improvement, please review output carefully")
        
        # Add metric summary to help debugging
        metrics['total_checks'] = len(metrics)
        metrics['issues_found'] = len(issues)
        
        return {
            'score': score,
            'method': 'enhanced heuristic v2 (free, comprehensive)',
            'metrics': metrics,
            'issues': issues,
            'recommendations': recommendations
        }
    
    def _heuristic_check(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Basic heuristic check without content"""
        from pathlib import Path
        
        score = 1.0
        issues = []
        
        # Check if output exists
        if not Path(output_file).exists():
            return {
                'score': 0.0,
                'method': 'heuristic',
                'metrics': {},
                'issues': ['Output file not found'],
                'recommendations': ['Check conversion process']
            }
        
        # File size comparison
        input_size = Path(input_file).stat().st_size
        output_size = Path(output_file).stat().st_size
        
        if output_size == 0:
            score = 0.0
            issues.append('Output file is empty')
        elif output_size < input_size * 0.1:
            score -= 0.3
            issues.append('Output file is very small compared to input')
        
        return {
            'score': max(0.0, score),
            'method': 'heuristic (basic)',
            'metrics': {'size_ratio': output_size / input_size if input_size > 0 else 0},
            'issues': issues,
            'recommendations': ['Consider using transformers method for better analysis']
        }
    
    def _extract_sample_content(self, file_path: str, max_chars: int = 3000) -> Optional[str]:
        """Extract text content from file for analysis"""
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext in ['.txt', '.md', '.markdown', '.html', '.htm']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(max_chars)
            
            elif ext == '.pdf':
                try:
                    import fitz
                    doc = fitz.open(file_path)
                    text = ""
                    for page in doc[:3]:  # First 3 pages
                        text += page.get_text()
                        if len(text) > max_chars:
                            break
                    doc.close()
                    return text[:max_chars]
                except:
                    return None
            
            elif ext in ['.docx', '.doc']:
                try:
                    from docx import Document
                    doc = Document(file_path)
                    text = '\n'.join([p.text for p in doc.paragraphs[:50]])
                    return text[:max_chars]
                except:
                    return None
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not extract content from {file_path}: {e}")
            return None
    
    def _apply_format_specific_scoring(
        self,
        result: Dict[str, Any],
        input_file: str,
        output_file: str,
        input_content: str,
        output_content: str
    ) -> Dict[str, Any]:
        """
        Apply format-specific scoring adjustments based on conversion type
        
        Args:
            result: Base quality check result
            input_file: Input file path
            output_file: Output file path
            input_content: Input content
            output_content: Output content
            
        Returns:
            Adjusted quality result
        """
        input_ext = Path(input_file).suffix.lower()
        output_ext = Path(output_file).suffix.lower()
        
        score_adjustment = 0.0
        format_issues = []
        format_recommendations = []
        
        # PDF → HTML conversion
        if input_ext == '.pdf' and output_ext in ['.html', '.htm']:
            logger.info("Applying PDF→HTML specific scoring...")
            
            # Check for proper HTML structure
            has_doctype = '<!doctype' in output_content.lower()
            has_html_tag = '<html' in output_content.lower()
            has_body_tag = '<body' in output_content.lower()
            
            if has_doctype and has_html_tag and has_body_tag:
                score_adjustment += 0.03
            else:
                score_adjustment -= 0.05
                format_issues.append("HTML structure incomplete")
            
            # Check for heading tags (PDF headings should become <h1>, <h2>, etc.)
            heading_count = len(re.findall(r'<h[1-6]>', output_content))
            if heading_count > 0:
                score_adjustment += 0.04
            else:
                format_recommendations.append("Consider improving heading detection in PDF")
            
            # Check for list tags
            list_count = len(re.findall(r'<ul>|<ol>|<li>', output_content))
            if list_count > 0:
                score_adjustment += 0.03
            
            # Check for table tags
            table_count = len(re.findall(r'<table>', output_content))
            if table_count > 0:
                score_adjustment += 0.03
            
            # Check for CSS styling
            has_style = '<style>' in output_content or 'style=' in output_content
            if has_style:
                score_adjustment += 0.02
            
        # HTML → PDF conversion
        elif input_ext in ['.html', '.htm'] and output_ext == '.pdf':
            logger.info("Applying HTML→PDF specific scoring...")
            
            # For HTML→PDF, check if PDF file is valid size
            pdf_size = Path(output_file).stat().st_size
            if pdf_size > 1000:  # Valid PDF should be at least 1KB
                score_adjustment += 0.05
            else:
                score_adjustment -= 0.15
                format_issues.append("PDF file size is too small")
            
            # Check if content length is reasonable (PDF text extraction)
            if len(output_content) > 100:
                score_adjustment += 0.03
            
        # Markdown → HTML conversion
        elif input_ext in ['.md', '.markdown'] and output_ext in ['.html', '.htm']:
            logger.info("Applying Markdown→HTML specific scoring...")
            
            # Check if markdown features are converted
            input_headings = len(re.findall(r'^#{1,6}\s', input_content, re.MULTILINE))
            output_headings = len(re.findall(r'<h[1-6][^>]*>', output_content))
            
            if input_headings > 0:
                heading_ratio = min(output_headings / input_headings, 1.0)
                if heading_ratio >= 0.9:
                    score_adjustment += 0.05
                elif heading_ratio < 0.7:
                    format_issues.append(f"Only {heading_ratio*100:.0f}% of headings converted")
            
            # Check code blocks
            input_code_blocks = len(re.findall(r'```', input_content))
            output_code_blocks = len(re.findall(r'<pre[^>]*>|<code[^>]*>', output_content))
            
            if input_code_blocks > 0:
                code_ratio = min(output_code_blocks / input_code_blocks, 1.0)
                if code_ratio >= 0.8:
                    score_adjustment += 0.04
                elif code_ratio < 0.6:
                    format_issues.append("Some code blocks may not be converted")
            
            # Check lists
            input_lists = len(re.findall(r'^\s*[-*+]\s|^\s*\d+\.\s', input_content, re.MULTILINE))
            output_lists = len(re.findall(r'<ul[^>]*>|<ol[^>]*>|<li[^>]*>', output_content))
            
            if input_lists > 0:
                list_ratio = min(output_lists / input_lists, 1.0)
                if list_ratio >= 0.7:
                    score_adjustment += 0.03
                elif list_ratio < 0.5:
                    format_issues.append("Some lists may not be converted properly")
            
            # Check for proper HTML structure
            has_doctype = '<!doctype' in output_content.lower()
            has_html_tag = '<html' in output_content.lower()
            
            if has_doctype and has_html_tag:
                score_adjustment += 0.02
        
        # HTML → Markdown conversion
        elif input_ext in ['.html', '.htm'] and output_ext in ['.md', '.markdown']:
            logger.info("Applying HTML→Markdown specific scoring...")
            
            # Check if HTML tags are converted to markdown syntax
            input_headings = len(re.findall(r'<h[1-6]>', input_content))
            output_headings = len(re.findall(r'^#{1,6}\s', output_content, re.MULTILINE))
            
            if input_headings > 0 and output_headings >= input_headings * 0.8:
                score_adjustment += 0.05
            
            # Check if HTML lists are converted
            input_lists = len(re.findall(r'<ul>|<ol>', input_content))
            output_lists = len(re.findall(r'^\s*[-*+]\s|^\s*\d+\.\s', output_content, re.MULTILINE))
            
            if input_lists > 0 and output_lists >= input_lists * 0.7:
                score_adjustment += 0.04
        
        # DOCX → Any format
        elif input_ext in ['.docx', '.doc']:
            logger.info("Applying DOCX source specific scoring...")
            
            # DOCX conversions should preserve formatting well
            if result['metrics'].get('formatting_preservation', 0) >= 0.8:
                score_adjustment += 0.03
            
        # Any → DOCX conversion
        elif output_ext in ['.docx', '.doc']:
            logger.info("Applying DOCX output specific scoring...")
            
            # Check if DOCX file is valid size
            docx_size = Path(output_file).stat().st_size
            if docx_size > 2000:  # Valid DOCX should be at least 2KB
                score_adjustment += 0.04
            else:
                score_adjustment -= 0.10
                format_issues.append("DOCX file size is suspiciously small")
        
        # Apply adjustments
        result['score'] = max(0.0, min(1.0, result['score'] + score_adjustment))
        
        if format_issues:
            result['issues'].extend(format_issues)
        
        if format_recommendations:
            result['recommendations'].extend(format_recommendations)
        
        # Add format-specific info
        result['conversion_type'] = f"{input_ext} → {output_ext}"
        result['format_adjustment'] = score_adjustment
        
        # Update rating based on new score
        result['rating'] = self._get_quality_rating(result['score'])
        
        return result
    
    def _get_quality_rating(self, score: float) -> str:
        """Convert score to quality rating"""
        if score >= 0.90:
            return 'excellent'
        elif score >= 0.80:
            return 'very_good'
        elif score >= 0.70:
            return 'good'
        elif score >= 0.60:
            return 'acceptable'
        elif score >= 0.50:
            return 'poor'
        else:
            return 'failed'

