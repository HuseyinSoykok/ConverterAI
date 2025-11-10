"""
Universal converter - routes to specific converters
"""
from pathlib import Path
from typing import Optional, List
from converters.base import BaseConverter, ConversionResult
from converters.pdf_converter import PDFConverter
from converters.docx_converter import DOCXConverter
from converters.markdown_converter import MarkdownConverter
from converters.html_converter import HTMLConverter
from utils.validator import Validator
from utils.logger import logger
from config import SUPPORTED_CONVERSIONS


class UniversalConverter(BaseConverter):
    """Universal converter that routes to specific format converters"""
    
    def __init__(self):
        super().__init__()
        self.pdf_converter = PDFConverter()
        self.docx_converter = DOCXConverter()
        self.markdown_converter = MarkdownConverter()
        self.html_converter = HTMLConverter()
        self.validator = Validator()
    
    def convert(
        self,
        input_file: str,
        input_format: Optional[str] = None,
        output_format: Optional[str] = None,
        output_file: Optional[str] = None,
        quality_check: bool = False,
        **options
    ) -> ConversionResult:
        """
        Convert file to specified format
        
        Args:
            input_file: Path to input file
            input_format: Source format (optional, auto-detected if not provided)
            output_format: Target format (pdf, docx, markdown, html)
            output_file: Optional output file path
            quality_check: Whether to perform AI quality check
            **options: Additional conversion options
            
        Returns:
            ConversionResult object
        """
        # Validate input file
        is_valid, error = self.validator.validate_file(input_file)
        if not is_valid:
            return self._create_error_result(input_file, error)
        
        # Detect input format if not provided
        if not input_format:
            input_format = self.validator.get_file_format(input_file)
        if not input_format:
            return self._create_error_result(
                input_file,
                "Could not determine file format"
            )
        
        # If output_format not provided, try to infer from output_file
        if not output_format and output_file:
            output_format = Path(output_file).suffix.lower().lstrip('.')
        
        if not output_format:
            return self._create_error_result(
                input_file,
                "Output format must be specified"
            )
        
        # Normalize output format
        output_format = output_format.lower().lstrip('.')
        if output_format == 'md':
            output_format = 'markdown'
        elif output_format in ['htm', 'doc']:
            output_format = {'htm': 'html', 'doc': 'docx'}[output_format]
        
        # Validate conversion
        is_valid, error = self.validator.validate_conversion(input_format, output_format)
        if not is_valid:
            return self._create_error_result(input_file, error, input_format, output_format)
        
        # Generate output file path if not provided
        if not output_file:
            input_path = Path(input_file)
            ext = self._get_extension_for_format(output_format)
            output_file = str(input_path.with_suffix(ext))
        
        # Validate output path
        is_valid, error = self.validator.validate_output_path(output_file, output_format)
        if not is_valid:
            return self._create_error_result(
                input_file,
                error,
                input_format,
                output_format
            )
        
        logger.info(f"Converting {input_format} to {output_format}: {input_file}")
        
        # Route to appropriate converter
        try:
            if input_format == 'pdf':
                result = self.pdf_converter.convert(input_file, output_file, **options)
            elif input_format == 'docx':
                result = self.docx_converter.convert(input_file, output_file, **options)
            elif input_format == 'markdown':
                result = self.markdown_converter.convert(input_file, output_file, **options)
            elif input_format == 'html':
                result = self.html_converter.convert(input_file, output_file, **options)
            else:
                return self._create_error_result(
                    input_file,
                    f"No converter available for format: {input_format}",
                    input_format,
                    output_format
                )
            
            # Perform quality check if requested and conversion was successful
            if quality_check and result.success:
                try:
                    from ai.quality_checker import QualityChecker
                    checker = QualityChecker()
                    quality_result = checker.check_quality(input_file, output_file)
                    result.quality_score = quality_result.get('score')
                    result.metadata['quality_report'] = quality_result
                except Exception as e:
                    logger.warning(f"Quality check failed: {e}")
                    result.warnings.append(f"Quality check unavailable: {e}")
            
            return result
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}", exc_info=True)
            return self._create_error_result(
                input_file,
                f"Conversion error: {e}",
                input_format,
                output_format
            )
    
    def batch_convert(
        self,
        input_files: List[str],
        output_format: str,
        output_dir: Optional[str] = None,
        quality_check: bool = False,
        **options
    ) -> List[ConversionResult]:
        """
        Convert multiple files
        
        Args:
            input_files: List of input file paths
            output_format: Target format
            output_dir: Output directory (optional)
            quality_check: Whether to perform quality checks
            **options: Additional conversion options
            
        Returns:
            List of ConversionResult objects
        """
        results = []
        
        for input_file in input_files:
            # Generate output file path
            if output_dir:
                input_path = Path(input_file)
                ext = self._get_extension_for_format(output_format)
                output_file = str(Path(output_dir) / input_path.with_suffix(ext).name)
            else:
                output_file = None
            
            # Convert
            result = self.convert(
                input_file,
                output_format,
                output_file,
                quality_check,
                **options
            )
            results.append(result)
            
            # Log progress
            success_count = sum(1 for r in results if r.success)
            logger.info(
                f"Batch progress: {len(results)}/{len(input_files)} "
                f"({success_count} successful)"
            )
        
        return results
    
    def get_supported_conversions(self) -> dict:
        """Get dictionary of supported conversions"""
        return SUPPORTED_CONVERSIONS
    
    @staticmethod
    def _get_extension_for_format(format_name: str) -> str:
        """Get file extension for format"""
        extensions = {
            'pdf': '.pdf',
            'docx': '.docx',
            'markdown': '.md',
            'html': '.html'
        }
        return extensions.get(format_name, f'.{format_name}')
