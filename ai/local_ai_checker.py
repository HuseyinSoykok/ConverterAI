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
            return self._transformers_check(input_content, output_content)
        elif self.method == 'ollama' and OLLAMA_AVAILABLE:
            return self._ollama_check(input_content, output_content)
        else:
            return self._heuristic_check_with_content(input_content, output_content)
    
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
        No AI needed, just smart algorithms
        """
        logger.info("Performing enhanced heuristic quality check...")
        
        score = 1.0
        issues = []
        recommendations = []
        metrics = {}
        
        # 1. Length Analysis
        input_len = len(input_content)
        output_len = len(output_content)
        length_ratio = output_len / input_len if input_len > 0 else 0
        metrics['length_ratio'] = length_ratio
        
        if length_ratio < 0.3:
            score -= 0.3
            issues.append("Output is significantly shorter than input (>70% content loss)")
            recommendations.append("Check if conversion preserved all content")
        elif length_ratio < 0.6:
            score -= 0.1
            issues.append("Output is noticeably shorter than input")
        elif length_ratio > 3.0:
            score -= 0.2
            issues.append("Output is much longer than input (possible formatting artifacts)")
            recommendations.append("Check for duplicated or added content")
        
        # 2. Word Count Analysis
        input_words = len(input_content.split())
        output_words = len(output_content.split())
        word_ratio = output_words / input_words if input_words > 0 else 0
        metrics['word_count_ratio'] = word_ratio
        
        # 3. Structure Analysis
        # Headings
        input_headings = len(re.findall(r'(^#{1,6}\s|<h[1-6]>)', input_content, re.MULTILINE))
        output_headings = len(re.findall(r'(^#{1,6}\s|<h[1-6]>)', output_content, re.MULTILINE))
        
        if input_headings > 0:
            heading_ratio = output_headings / input_headings
            metrics['heading_preservation'] = heading_ratio
            
            if heading_ratio < 0.7:
                score -= 0.15
                issues.append(f"Only {heading_ratio*100:.0f}% of headings preserved")
                recommendations.append("Review heading structure")
        
        # 4. Lists
        input_lists = len(re.findall(r'(^\s*[-*+]\s|^\s*\d+\.\s|<li>)', input_content, re.MULTILINE))
        output_lists = len(re.findall(r'(^\s*[-*+]\s|^\s*\d+\.\s|<li>)', output_content, re.MULTILINE))
        
        if input_lists > 3:
            list_ratio = output_lists / input_lists
            metrics['list_preservation'] = list_ratio
            
            if list_ratio < 0.6:
                score -= 0.1
                issues.append("Some list items may be lost")
        
        # 5. Code Blocks
        input_code = len(re.findall(r'```|<code>|<pre>', input_content))
        output_code = len(re.findall(r'```|<code>|<pre>', output_content))
        
        if input_code > 0:
            code_ratio = output_code / input_code
            metrics['code_preservation'] = code_ratio
            
            if code_ratio < 0.8:
                score -= 0.1
                issues.append("Code blocks may not be fully preserved")
        
        # 6. Tables
        input_tables = len(re.findall(r'(\|.*\||\<table\>)', input_content))
        output_tables = len(re.findall(r'(\|.*\||\<table\>)', output_content))
        
        if input_tables > 0:
            table_ratio = output_tables / input_tables
            metrics['table_preservation'] = table_ratio
            
            if table_ratio < 0.7:
                score -= 0.15
                issues.append("Tables may not be fully converted")
                recommendations.append("Manually check table formatting")
        
        # 7. Special Characters
        input_special = len(re.findall(r'[^\w\s]', input_content))
        output_special = len(re.findall(r'[^\w\s]', output_content))
        
        if input_special > 100:
            special_ratio = output_special / input_special
            if special_ratio < 0.5:
                score -= 0.05
                issues.append("Some special characters may be lost")
        
        # 8. Empty Output Check
        if output_len < 100:
            score = 0.1
            issues.append("Output file is too small")
            recommendations.append("Conversion may have failed")
        
        # 9. Character Encoding Issues
        if '�' in output_content or '\ufffd' in output_content:
            score -= 0.1
            issues.append("Character encoding issues detected")
            recommendations.append("Check output file encoding")
        
        # Ensure score is in valid range
        score = max(0.0, min(1.0, score))
        
        # Add default recommendation if score is good
        if score >= 0.9 and not recommendations:
            recommendations.append("Conversion quality is excellent!")
        elif score >= 0.7 and not recommendations:
            recommendations.append("Conversion quality is good")
        
        return {
            'score': score,
            'method': 'enhanced heuristic (free, always available)',
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
