"""
OCR Engine for extracting text from scanned documents
"""
from typing import Optional, Dict, Any
from pathlib import Path
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from utils.logger import logger
from config import OCR_LANGUAGE, DEFAULT_DPI


class OCREngine:
    """OCR engine for text extraction from images and scanned PDFs"""
    
    def __init__(self, language: str = OCR_LANGUAGE):
        """
        Initialize OCR engine
        
        Args:
            language: Tesseract language code (e.g., 'tur+eng')
        """
        self.language = language
        self._check_tesseract()
    
    def _check_tesseract(self):
        """Check if Tesseract is available"""
        try:
            pytesseract.get_tesseract_version()
            logger.info(f"Tesseract OCR available, language: {self.language}")
        except Exception as e:
            logger.warning(f"Tesseract OCR not available: {e}")
            logger.warning("OCR features will not work. Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
    
    def extract_text_from_image(
        self,
        image_path: str,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to image file
            language: Optional language override
            
        Returns:
            Dictionary with text and metadata
        """
        lang = language or self.language
        
        try:
            logger.info(f"Extracting text from image: {image_path}")
            
            # Open image
            image = Image.open(image_path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image, lang=lang)
            
            # Get detailed data
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            # Calculate confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'success': True,
                'text': text,
                'confidence': avg_confidence,
                'word_count': len(text.split()),
                'metadata': {
                    'image_size': image.size,
                    'language': lang
                }
            }
            
        except Exception as e:
            logger.error(f"OCR failed for image {image_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': None
            }
    
    def extract_text_from_pdf(
        self,
        pdf_path: str,
        language: Optional[str] = None,
        dpi: int = DEFAULT_DPI
    ) -> Dict[str, Any]:
        """
        Extract text from scanned PDF using OCR
        
        Args:
            pdf_path: Path to PDF file
            language: Optional language override
            dpi: DPI for PDF to image conversion
            
        Returns:
            Dictionary with text and metadata
        """
        lang = language or self.language
        
        try:
            logger.info(f"Extracting text from PDF with OCR: {pdf_path}")
            
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=dpi)
            
            all_text = []
            page_results = []
            total_confidence = 0
            
            for i, image in enumerate(images, 1):
                logger.info(f"Processing page {i}/{len(images)}")
                
                # Perform OCR on page
                text = pytesseract.image_to_string(image, lang=lang)
                data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
                
                # Calculate confidence for this page
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                page_confidence = sum(confidences) / len(confidences) if confidences else 0
                
                all_text.append(f"--- Page {i} ---\n{text}")
                page_results.append({
                    'page': i,
                    'text': text,
                    'confidence': page_confidence,
                    'word_count': len(text.split())
                })
                
                total_confidence += page_confidence
            
            avg_confidence = total_confidence / len(images) if images else 0
            combined_text = '\n\n'.join(all_text)
            
            return {
                'success': True,
                'text': combined_text,
                'confidence': avg_confidence,
                'page_count': len(images),
                'word_count': len(combined_text.split()),
                'pages': page_results,
                'metadata': {
                    'dpi': dpi,
                    'language': lang
                }
            }
            
        except Exception as e:
            logger.error(f"OCR failed for PDF {pdf_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': None
            }
    
    def is_pdf_scanned(self, pdf_path: str) -> bool:
        """
        Detect if PDF is scanned (image-based) or digital (text-based)
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            True if PDF appears to be scanned
        """
        try:
            import fitz
            
            doc = fitz.open(pdf_path)
            
            # Check first few pages
            pages_to_check = min(3, len(doc))
            text_chars = 0
            
            for page_num in range(pages_to_check):
                page = doc[page_num]
                text = page.get_text()
                text_chars += len(text.strip())
            
            doc.close()
            
            # If very little text, likely scanned
            is_scanned = text_chars < 100
            
            logger.info(f"PDF scan detection: {pdf_path} - {'scanned' if is_scanned else 'digital'}")
            return is_scanned
            
        except Exception as e:
            logger.warning(f"Could not detect PDF type: {e}")
            return False
    
    def process_pdf_with_ocr_fallback(
        self,
        pdf_path: str,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract text from PDF, using OCR if needed
        
        Args:
            pdf_path: Path to PDF file
            language: Optional language override
            
        Returns:
            Dictionary with text and metadata
        """
        try:
            import fitz
            
            # First try digital text extraction
            doc = fitz.open(pdf_path)
            text_parts = []
            
            for page in doc:
                text = page.get_text()
                text_parts.append(text)
            
            doc.close()
            combined_text = '\n\n'.join(text_parts)
            
            # Check if we got meaningful text
            if len(combined_text.strip()) > 100:
                logger.info(f"Extracted text digitally from PDF: {pdf_path}")
                return {
                    'success': True,
                    'text': combined_text,
                    'method': 'digital',
                    'confidence': 1.0
                }
            
            # If not enough text, use OCR
            logger.info(f"PDF appears scanned, using OCR: {pdf_path}")
            result = self.extract_text_from_pdf(pdf_path, language)
            result['method'] = 'ocr'
            return result
            
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': None
            }
