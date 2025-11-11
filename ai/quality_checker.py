"""
AI-powered quality checker for conversions
Supports FREE local AI methods and paid API methods
"""
from typing import Dict, Optional, Any
from pathlib import Path
import os
from utils.logger import logger
from config import OPENAI_API_KEY, ANTHROPIC_API_KEY, QUALITY_THRESHOLDS, AI_QUALITY_METHOD


class QualityChecker:
    """Check conversion quality using AI (FREE and paid options)"""
    
    def __init__(self):
        self.has_openai = bool(OPENAI_API_KEY)
        self.has_anthropic = bool(ANTHROPIC_API_KEY)
        self.method = AI_QUALITY_METHOD
        
        # Initialize local AI checker (FREE!)
        try:
            from ai.local_ai_checker import LocalAIChecker
            self.local_checker = LocalAIChecker(method=self.method)
            logger.info(f"Quality checker initialized with method: {self.method}")
        except Exception as e:
            logger.warning(f"Local AI checker not available: {e}")
            self.local_checker = None
            self.method = 'heuristic'
        
        if not (self.has_openai or self.has_anthropic or self.local_checker):
            logger.warning("No AI methods available. Using basic heuristics only.")
    
    def check_quality(
        self,
        input_file: str,
        output_file: str,
        use_ai: bool = True
    ) -> Dict[str, Any]:
        """
        Check conversion quality (FREE and paid options)
        
        Args:
            input_file: Original file path
            output_file: Converted file path
            use_ai: Whether to use AI for quality check
            
        Returns:
            Dictionary with quality metrics
        """
        logger.info(f"Checking quality: {input_file} -> {output_file}")
        
        # Try FREE local AI methods first (no API keys needed!)
        if use_ai and self.local_checker and self.method in ['heuristic', 'transformers', 'ollama']:
            try:
                result = self.local_checker.check_quality(input_file, output_file)
                result['rating'] = self._get_quality_rating(result['score'])
                logger.info(f"Quality check completed using {result['method']}")
                return result
            except Exception as e:
                logger.warning(f"Local AI check failed: {e}")
        
        # Try paid API methods if available and requested
        if use_ai and (self.has_openai or self.has_anthropic):
            try:
                ai_result = self._ai_check(input_file, output_file)
                if ai_result:
                    ai_result['rating'] = self._get_quality_rating(ai_result['score'])
                    return ai_result
            except Exception as e:
                logger.warning(f"Paid API check failed: {e}")
        
        # Fallback to basic heuristic
        heuristic_score = self._heuristic_check(input_file, output_file)
        
        result = {
            'score': heuristic_score,
            'method': 'heuristic (basic fallback)',
            'metrics': {},
            'issues': [],
            'recommendations': ['Consider using transformers method for better analysis'],
            'rating': self._get_quality_rating(heuristic_score)
        }
        
        return result
    
    def _heuristic_check(self, input_file: str, output_file: str) -> float:
        """
        Perform heuristic-based quality check
        
        Args:
            input_file: Original file
            output_file: Converted file
            
        Returns:
            Quality score (0-1)
        """
        score = 1.0
        
        # Check if output file exists and has content
        if not Path(output_file).exists():
            return 0.0
        
        output_size = Path(output_file).stat().st_size
        if output_size == 0:
            return 0.0
        
        # Compare file sizes (rough heuristic)
        input_size = Path(input_file).stat().st_size
        size_ratio = output_size / input_size if input_size > 0 else 0
        
        # Penalize if output is drastically different in size
        if size_ratio < 0.1:  # Too small
            score -= 0.3
        elif size_ratio > 10:  # Too large
            score -= 0.2
        
        # Check content based on file type
        try:
            output_ext = Path(output_file).suffix.lower()
            
            if output_ext in ['.txt', '.md', '.html']:
                # Check if text file has reasonable content
                with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    if len(content) < 10:
                        score -= 0.5
                    
                    # Check for error indicators
                    error_indicators = ['error', 'failed', 'corrupt', 'invalid']
                    if any(indicator in content.lower() for indicator in error_indicators):
                        score -= 0.2
            
            elif output_ext == '.pdf':
                # Basic PDF validation
                if output_size < 100:  # Too small for valid PDF
                    score -= 0.4
            
            elif output_ext == '.docx':
                # Basic DOCX validation
                if output_size < 500:  # Too small for valid DOCX
                    score -= 0.4
        
        except Exception as e:
            logger.warning(f"Heuristic check error: {e}")
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _ai_check(self, input_file: str, output_file: str) -> Optional[Dict[str, Any]]:
        """
        Perform AI-based quality check
        
        Args:
            input_file: Original file
            output_file: Converted file
            
        Returns:
            Dictionary with AI analysis results or None
        """
        # Read content from both files
        input_content = self._extract_text_content(input_file)
        output_content = self._extract_text_content(output_file)
        
        if not input_content or not output_content:
            return None
        
        # Limit content size for API
        max_chars = 2000
        input_sample = input_content[:max_chars]
        output_sample = output_content[:max_chars]
        
        prompt = f"""Analyze the quality of this document conversion. Compare the original content with the converted output.

Original content (sample):
{input_sample}

Converted content (sample):
{output_sample}

Please evaluate:
1. Content preservation (0-1 score)
2. Format/structure preservation (0-1 score)
3. Overall quality (0-1 score)
4. List any issues found
5. Provide recommendations

Respond in JSON format:
{{
    "content_score": <0-1>,
    "format_score": <0-1>,
    "overall_score": <0-1>,
    "issues": ["issue1", "issue2"],
    "recommendations": ["rec1", "rec2"]
}}"""
        
        try:
            if self.has_openai:
                result = self._check_with_openai(prompt)
            elif self.has_anthropic:
                result = self._check_with_anthropic(prompt)
            else:
                return None
            
            return result
            
        except Exception as e:
            logger.error(f"AI check failed: {e}")
            return None
    
    def _check_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Use OpenAI for quality check"""
        try:
            import openai
            import json
            
            openai.api_key = OPENAI_API_KEY
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a document conversion quality expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return {
                'score': result.get('overall_score', 0.5),
                'metrics': {
                    'content_score': result.get('content_score'),
                    'format_score': result.get('format_score')
                },
                'issues': result.get('issues', []),
                'recommendations': result.get('recommendations', [])
            }
            
        except Exception as e:
            logger.error(f"OpenAI check failed: {e}")
            raise
    
    def _check_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Use Anthropic Claude for quality check"""
        try:
            import anthropic
            import json
            
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            result = json.loads(content)
            
            return {
                'score': result.get('overall_score', 0.5),
                'metrics': {
                    'content_score': result.get('content_score'),
                    'format_score': result.get('format_score')
                },
                'issues': result.get('issues', []),
                'recommendations': result.get('recommendations', [])
            }
            
        except Exception as e:
            logger.error(f"Anthropic check failed: {e}")
            raise
    
    def _extract_text_content(self, file_path: str) -> Optional[str]:
        """Extract text content from file"""
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext in ['.txt', '.md', '.html', '.htm']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            
            elif ext == '.pdf':
                import fitz
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                return text
            
            elif ext in ['.docx', '.doc']:
                from docx import Document
                doc = Document(file_path)
                return '\n'.join([para.text for para in doc.paragraphs])
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not extract text from {file_path}: {e}")
            return None
    
    @staticmethod
    def _get_quality_rating(score: float) -> str:
        """Convert score to quality rating"""
        if score >= QUALITY_THRESHOLDS['excellent']:
            return 'excellent'
        elif score >= QUALITY_THRESHOLDS.get('very_good', 0.80):
            return 'very_good'
        elif score >= QUALITY_THRESHOLDS['good']:
            return 'good'
        elif score >= QUALITY_THRESHOLDS['acceptable']:
            return 'acceptable'
        elif score >= QUALITY_THRESHOLDS['poor']:
            return 'poor'
        else:
            return 'failed'
