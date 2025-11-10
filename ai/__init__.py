"""
AI modules for ConverterAI
Supports FREE local AI and paid API methods
"""
from .quality_checker import QualityChecker

# Try to import OCR engine (optional, requires pytesseract and Tesseract)
try:
    from .ocr_engine import OCREngine
    has_ocr = True
except ImportError as e:
    OCREngine = None
    has_ocr = False

# Try to import local AI checker (optional)
try:
    from .local_ai_checker import LocalAIChecker
    has_local_ai = True
except ImportError:
    LocalAIChecker = None
    has_local_ai = False

__all__ = ['QualityChecker']
if has_ocr:
    __all__.append('OCREngine')
if has_local_ai:
    __all__.append('LocalAIChecker')
