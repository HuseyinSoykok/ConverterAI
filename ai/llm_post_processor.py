"""
LLM Post-Processor for OCR Output Enhancement
Supports multiple free LLM providers:
- HuggingFace Inference API (free tier)
- Ollama (local, free)
- Google Gemini (free API)
"""
import os
import re
import json
from typing import Optional, Dict, Tuple
from abc import ABC, abstractmethod

from utils.logger import logger


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    def process(self, text: str, prompt: str) -> str:
        """Process text with the LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available"""
        pass


class HuggingFaceProvider(BaseLLMProvider):
    """
    HuggingFace Inference API provider (free tier)
    Models: mistralai/Mistral-7B-Instruct-v0.2, microsoft/Phi-3-mini-4k-instruct
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get('HUGGINGFACE_API_KEY', '')
        # Free tier compatible models
        self.model = model or "mistralai/Mistral-7B-Instruct-v0.2"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
    
    def is_available(self) -> bool:
        if not self.api_key:
            return False
        try:
            import requests
            response = requests.get(
                f"https://huggingface.co/api/models/{self.model}",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def process(self, text: str, prompt: str) -> str:
        import requests
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Format for instruction-tuned models
        full_prompt = f"<s>[INST] {prompt}\n\nText to process:\n{text}\n[/INST]"
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 4096,
                "temperature": 0.3,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', text)
                return text
            else:
                logger.warning(f"HuggingFace API error: {response.status_code}")
                return text
                
        except Exception as e:
            logger.error(f"HuggingFace processing failed: {e}")
            return text


class OllamaProvider(BaseLLMProvider):
    """
    Ollama local LLM provider (completely free)
    Requires Ollama installed locally with a model like llama2, mistral, or phi
    """
    
    def __init__(self, model: str = None, host: str = None):
        self.model = model or "llama3.2"  # Default to llama3.2 (small, fast)
        self.host = host or os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
    
    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '').split(':')[0] for m in models]
                return self.model.split(':')[0] in model_names
            return False
        except:
            return False
    
    def process(self, text: str, prompt: str) -> str:
        import requests
        
        full_prompt = f"{prompt}\n\nText to process:\n{text}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 4096
            }
        }
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=300  # Longer timeout for local processing
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', text)
            else:
                logger.warning(f"Ollama API error: {response.status_code}")
                return text
                
        except Exception as e:
            logger.error(f"Ollama processing failed: {e}")
            return text


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini API provider (free tier: 60 requests/minute)
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY', '')
        self.model = "gemini-2.0-flash"  # Updated free tier model
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def process(self, text: str, prompt: str) -> str:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            full_prompt = f"{prompt}\n\nText to process:\n{text}"
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 8192,
                }
            )
            
            return response.text
            
        except ImportError:
            logger.error("google-generativeai not installed. Install with: pip install google-generativeai")
            return text
        except Exception as e:
            logger.error(f"Gemini processing failed: {e}")
            return text


class LLMPostProcessor:
    """
    Main LLM post-processor that manages multiple providers
    and provides specialized prompts for math/academic content
    """
    
    # Specialized prompts for different tasks
    PROMPTS = {
        'math_latex': """You are an expert at converting OCR text from academic/mathematical PDFs to clean, properly formatted Markdown with LaTeX.

CRITICAL RULES:
1. REMOVE all page markers like "=== Page X ===" completely
2. REMOVE all headers/footers like "November 24, 2025", "Seite X", "H LR |s", "SSS", random symbols
3. REMOVE slide deck artifacts like "24" at end of sections

MATH FORMATTING:
4. Convert ALL mathematical expressions to proper LaTeX
5. Inline math: $expression$ (e.g., $u$, $f$, $\\Omega$)
6. Block/display math: $$expression$$ for important equations
7. Fix Greek letters: Ω→$\\Omega$, Δ→$\\Delta$, ∇→$\\nabla$, ∂→$\\partial$, α→$\\alpha$, β→$\\beta$
8. Fix operators: ∈→$\\in$, ∀→$\\forall$, ∃→$\\exists$, →→$\\to$, ≤→$\\leq$
9. Fix subscripts/superscripts: u_i→$u_i$, x^2→$x^2$, H^1_0→$H^1_0$

STRUCTURE:
10. Use ## for main section titles
11. Use ### for subsections  
12. Keep document flow logical and readable
13. Format algorithm/pseudocode in code blocks with ```

OUTPUT:
- Return ONLY the clean Markdown document
- NO explanations, NO comments about what you did
- Start directly with the content""",

        'clean_text': """You are a text cleaning expert. Clean the following OCR output:

1. Fix spelling and grammar errors
2. Remove duplicate content
3. Fix paragraph breaks
4. Remove noise (random characters, page numbers)
5. Keep the original meaning and structure

Output ONLY the cleaned text, no explanations.""",

        'structure': """You are a document structure expert. Restructure this OCR text:

1. Add proper Markdown headings (##, ###, ####)
2. Format lists with * or -
3. Create proper paragraphs
4. Add code blocks where appropriate
5. Keep all content intact

Output ONLY the restructured Markdown, no explanations.""",
    }
    
    def __init__(self, provider: str = 'auto', **kwargs):
        """
        Initialize the post-processor
        
        Args:
            provider: 'huggingface', 'ollama', 'gemini', or 'auto'
            **kwargs: Provider-specific arguments (api_key, model, host)
        """
        self.providers = {
            'huggingface': HuggingFaceProvider(
                api_key=kwargs.get('huggingface_api_key'),
                model=kwargs.get('huggingface_model')
            ),
            'ollama': OllamaProvider(
                model=kwargs.get('ollama_model'),
                host=kwargs.get('ollama_host')
            ),
            'gemini': GeminiProvider(
                api_key=kwargs.get('google_api_key')
            ),
        }
        
        self.provider_name = provider
        self.active_provider = None
        
        if provider == 'auto':
            self._auto_select_provider()
        elif provider in self.providers:
            if self.providers[provider].is_available():
                self.active_provider = self.providers[provider]
                self.provider_name = provider
            else:
                logger.warning(f"Provider '{provider}' not available, trying auto-select")
                self._auto_select_provider()
    
    def _auto_select_provider(self):
        """Auto-select the best available provider"""
        # Priority: Ollama (local, free) > Gemini (fast, free) > HuggingFace (free tier)
        priority = ['ollama', 'gemini', 'huggingface']
        
        for name in priority:
            provider = self.providers[name]
            if provider.is_available():
                self.active_provider = provider
                self.provider_name = name
                logger.info(f"Auto-selected LLM provider: {name}")
                return
        
        logger.warning("No LLM provider available")
        self.active_provider = None
    
    def is_available(self) -> bool:
        """Check if any provider is available"""
        return self.active_provider is not None
    
    def get_provider_info(self) -> Dict:
        """Get information about available providers"""
        info = {}
        for name, provider in self.providers.items():
            info[name] = {
                'available': provider.is_available(),
                'active': name == self.provider_name
            }
        return info
    
    def _pre_clean_ocr_text(self, text: str) -> str:
        """Pre-clean OCR text before sending to LLM to reduce token count"""
        # Remove page markers
        text = re.sub(r'===\s*Page\s*\d+\s*===', '', text)
        
        # Remove common header/footer patterns
        noise_patterns = [
            r'November\s+\d+,\s+\d+.*?(?=\n|$)',  # Date headers
            r'Seite\s+\d+',  # German page numbers
            r'H\s*L\s*R\s*\|?\s*[sS]',  # HLR markers
            r'SSS+',  # SSS markers
            r'^\s*24\s*$',  # Standalone "24"
            r'\d{1,2}/\d{1,2}/\d{4}',  # Date patterns
            r'Solving the 2d Poisson Equation using the FEM and a CG Method',  # Repeated title
        ]
        
        for pattern in noise_patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)
        
        # Remove excessive whitespace
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remove lines that are mostly noise (short lines with random chars)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            # Keep lines that have meaningful content
            if len(stripped) > 3 or stripped == '':
                # Skip lines that look like pure noise
                if not re.match(r'^[\|\-=~\s]+$', stripped):
                    cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def process_math_document(self, text: str) -> Tuple[str, Dict]:
        """
        Process a mathematical/academic document
        
        Args:
            text: Raw OCR text
            
        Returns:
            Tuple of (processed_text, metadata)
        """
        if not self.active_provider:
            logger.warning("No LLM provider available, returning original text")
            return text, {'provider': None, 'processed': False}
        
        logger.info(f"Processing document with {self.provider_name}")
        
        # Pre-clean the text to reduce noise and token count
        cleaned_text = self._pre_clean_ocr_text(text)
        logger.info(f"Pre-cleaned text: {len(text)} -> {len(cleaned_text)} chars")
        
        # Split into chunks if too long (most free APIs have limits)
        chunks = self._split_into_chunks(cleaned_text, max_chars=6000)
        processed_chunks = []
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            processed = self.active_provider.process(chunk, self.PROMPTS['math_latex'])
            # Post-clean to remove any remaining artifacts
            processed = self._post_clean(processed)
            processed_chunks.append(processed)
        
        result = '\n\n'.join(processed_chunks)
        
        return result, {
            'provider': self.provider_name,
            'processed': True,
            'chunks': len(chunks)
        }
    
    def _post_clean(self, text: str) -> str:
        """Post-clean LLM output"""
        # Remove any remaining page markers the LLM might have kept
        text = re.sub(r'===\s*Page\s*\d+\s*===', '', text)
        # Remove empty headers
        text = re.sub(r'^#+\s*$', '', text, flags=re.MULTILINE)
        # Fix multiple blank lines
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        return text.strip()
    
    def clean_ocr_text(self, text: str) -> str:
        """Clean OCR text without math formatting"""
        if not self.active_provider:
            return text
        
        return self.active_provider.process(text, self.PROMPTS['clean_text'])
    
    def restructure_document(self, text: str) -> str:
        """Add structure (headings, lists) to text"""
        if not self.active_provider:
            return text
        
        return self.active_provider.process(text, self.PROMPTS['structure'])
    
    def _split_into_chunks(self, text: str, max_chars: int = 6000) -> list:
        """Split text into chunks while preserving structure"""
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        # Split by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            para_length = len(para)
            
            if current_length + para_length > max_chars and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks


def setup_llm_provider(config: Dict = None) -> LLMPostProcessor:
    """
    Factory function to create LLM post-processor from config
    
    Config can include:
        provider: 'auto', 'huggingface', 'ollama', 'gemini'
        huggingface_api_key: str
        huggingface_model: str
        ollama_model: str
        ollama_host: str
        google_api_key: str
    """
    config = config or {}
    return LLMPostProcessor(**config)


# Convenience function for quick processing
def enhance_ocr_with_llm(text: str, provider: str = 'auto', **kwargs) -> str:
    """
    Quick function to enhance OCR text with LLM
    
    Args:
        text: Raw OCR text
        provider: 'auto', 'huggingface', 'ollama', 'gemini'
        **kwargs: Provider-specific arguments
        
    Returns:
        Enhanced text
    """
    processor = LLMPostProcessor(provider=provider, **kwargs)
    if processor.is_available():
        result, _ = processor.process_math_document(text)
        return result
    return text
