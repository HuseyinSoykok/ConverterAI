"""
File validation utilities
"""
import os
from pathlib import Path
from typing import Tuple, Optional

# Try to import magic, but make it optional
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False

from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES, SUPPORTED_CONVERSIONS
from utils.logger import logger


class Validator:
    """File and conversion validation"""
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if file exists and is readable
        
        Args:
            file_path: Path to file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File not found: {file_path}"
        
        if not path.is_file():
            return False, f"Not a file: {file_path}"
        
        if not os.access(file_path, os.R_OK):
            return False, f"File not readable: {file_path}"
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
            return False, f"File too large: {size_mb:.2f}MB (max: {max_mb}MB)"
        
        if file_size == 0:
            return False, "File is empty"
        
        return True, None
    
    @staticmethod
    def get_file_format(file_path: str) -> Optional[str]:
        """
        Detect file format from extension and content
        
        Args:
            file_path: Path to file
            
        Returns:
            Format name (pdf, docx, markdown, html) or None
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        # Check by extension first
        for format_name, extensions in ALLOWED_EXTENSIONS.items():
            if extension in extensions:
                return format_name
        
        # Try to detect by content using python-magic (if available)
        if HAS_MAGIC:
            try:
                file_type = magic.from_file(file_path, mime=True)
                
                mime_map = {
                    'application/pdf': 'pdf',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
                    'application/msword': 'docx',
                    'text/markdown': 'markdown',
                    'text/html': 'html',
                    'text/plain': 'markdown',  # Assume .md for plain text
                    'image/png': 'image',
                    'image/jpeg': 'image',
                    'image/jpg': 'image'
                }
                
                return mime_map.get(file_type)
            except Exception as e:
                logger.warning(f"Could not detect file type: {e}")
                return None
        
        return None
    
    @staticmethod
    def validate_conversion(input_format: str, output_format: str) -> Tuple[bool, Optional[str]]:
        """
        Check if conversion is supported
        
        Args:
            input_format: Source format
            output_format: Target format
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if input_format not in SUPPORTED_CONVERSIONS:
            return False, f"Unsupported input format: {input_format}"
        
        if output_format not in SUPPORTED_CONVERSIONS[input_format]:
            return False, f"Cannot convert {input_format} to {output_format}"
        
        if input_format == output_format:
            return False, "Input and output formats are the same"
        
        return True, None
    
    @staticmethod
    def validate_output_path(output_path: str, output_format: str) -> Tuple[bool, Optional[str]]:
        """
        Validate output path and format
        
        Args:
            output_path: Output file path
            output_format: Expected format
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        path = Path(output_path)
        
        # Check if parent directory exists or can be created
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"Cannot create output directory: {e}"
        
        # Check extension matches format
        expected_extensions = ALLOWED_EXTENSIONS.get(output_format, [])
        if expected_extensions and path.suffix.lower() not in expected_extensions:
            return False, f"Output file extension should be one of {expected_extensions}"
        
        return True, None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent security issues
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path separators
        filename = os.path.basename(filename)
        
        # Remove or replace dangerous characters
        dangerous_chars = '<>:"|?*\x00'
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:255-len(ext)] + ext
        
        return filename
