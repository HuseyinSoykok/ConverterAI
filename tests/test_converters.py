"""
Test suite for ConverterAI
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from converters import UniversalConverter
from utils.validator import Validator
from utils.file_handler import FileHandler


class TestValidator:
    """Test Validator class"""
    
    def test_validate_file_exists(self, tmp_path):
        """Test file existence validation"""
        validator = Validator()
        
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        is_valid, error = validator.validate_file(str(test_file))
        assert is_valid is True
        assert error is None
    
    def test_validate_file_not_exists(self):
        """Test validation for non-existent file"""
        validator = Validator()
        
        is_valid, error = validator.validate_file("nonexistent.txt")
        assert is_valid is False
        assert "not found" in error.lower()
    
    def test_get_file_format_pdf(self, tmp_path):
        """Test PDF format detection"""
        validator = Validator()
        
        test_file = tmp_path / "test.pdf"
        test_file.write_text("fake pdf")
        
        format_name = validator.get_file_format(str(test_file))
        assert format_name == "pdf"
    
    def test_validate_conversion_valid(self):
        """Test valid conversion validation"""
        validator = Validator()
        
        is_valid, error = validator.validate_conversion("pdf", "docx")
        assert is_valid is True
        assert error is None
    
    def test_validate_conversion_invalid(self):
        """Test invalid conversion validation"""
        validator = Validator()
        
        is_valid, error = validator.validate_conversion("pdf", "mp3")
        assert is_valid is False
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        validator = Validator()
        
        dangerous = "test<>file.pdf"
        safe = validator.sanitize_filename(dangerous)
        
        assert "<" not in safe
        assert ">" not in safe


class TestFileHandler:
    """Test FileHandler class"""
    
    def test_safe_copy(self, tmp_path):
        """Test safe file copy"""
        handler = FileHandler()
        
        src = tmp_path / "source.txt"
        dst = tmp_path / "dest.txt"
        
        src.write_text("test content")
        
        success = handler.safe_copy(str(src), str(dst))
        assert success is True
        assert dst.exists()
        assert dst.read_text() == "test content"
    
    def test_safe_delete(self, tmp_path):
        """Test safe file deletion"""
        handler = FileHandler()
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        success = handler.safe_delete(str(test_file))
        assert success is True
        assert not test_file.exists()
    
    def test_get_file_info(self, tmp_path):
        """Test file info retrieval"""
        handler = FileHandler()
        
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        info = handler.get_file_info(str(test_file))
        assert info is not None
        assert info['name'] == "test.txt"
        assert info['size'] > 0
    
    def test_get_unique_filename(self, tmp_path):
        """Test unique filename generation"""
        handler = FileHandler()
        
        # Create existing file
        existing = tmp_path / "test.txt"
        existing.write_text("test")
        
        unique = handler.get_unique_filename(str(tmp_path), "test.txt")
        assert unique != "test.txt"
        assert "test_" in unique


class TestUniversalConverter:
    """Test UniversalConverter class"""
    
    def test_converter_initialization(self):
        """Test converter initialization"""
        converter = UniversalConverter()
        assert converter is not None
        assert converter.pdf_converter is not None
        assert converter.docx_converter is not None
    
    def test_get_supported_conversions(self):
        """Test getting supported conversions"""
        converter = UniversalConverter()
        conversions = converter.get_supported_conversions()
        
        assert isinstance(conversions, dict)
        assert 'pdf' in conversions
        assert 'docx' in conversions['pdf']
    
    def test_get_extension_for_format(self):
        """Test extension generation"""
        converter = UniversalConverter()
        
        assert converter._get_extension_for_format('pdf') == '.pdf'
        assert converter._get_extension_for_format('docx') == '.docx'
        assert converter._get_extension_for_format('markdown') == '.md'


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
