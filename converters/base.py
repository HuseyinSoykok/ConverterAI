"""
Base converter class and result model
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime
from utils.logger import logger


@dataclass
class ConversionResult:
    """Result of a conversion operation"""
    success: bool
    input_file: str
    output_file: Optional[str] = None
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    error: Optional[str] = None
    warnings: list = None
    quality_score: Optional[float] = None
    processing_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> dict:
        """Convert result to dictionary"""
        return {
            'success': self.success,
            'input_file': self.input_file,
            'output_file': self.output_file,
            'input_format': self.input_format,
            'output_format': self.output_format,
            'error': self.error,
            'warnings': self.warnings,
            'quality_score': self.quality_score,
            'processing_time': self.processing_time,
            'metadata': self.metadata
        }


class BaseConverter(ABC):
    """Base class for all converters"""
    
    def __init__(self):
        self.logger = logger
    
    @abstractmethod
    def convert(self, input_file: str, output_file: str, **options) -> ConversionResult:
        """
        Convert file from one format to another
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            **options: Additional conversion options
            
        Returns:
            ConversionResult object
        """
        pass
    
    def _create_success_result(
        self,
        input_file: str,
        output_file: str,
        input_format: str,
        output_format: str,
        processing_time: float = 0,
        **kwargs
    ) -> ConversionResult:
        """Helper to create success result"""
        return ConversionResult(
            success=True,
            input_file=input_file,
            output_file=output_file,
            input_format=input_format,
            output_format=output_format,
            processing_time=processing_time,
            **kwargs
        )
    
    def _create_error_result(
        self,
        input_file: str,
        error: str,
        input_format: str = None,
        output_format: str = None
    ) -> ConversionResult:
        """Helper to create error result"""
        self.logger.error(f"Conversion failed: {error}")
        return ConversionResult(
            success=False,
            input_file=input_file,
            input_format=input_format,
            output_format=output_format,
            error=error
        )
    
    def _validate_files(self, input_file: str, output_file: str) -> Optional[str]:
        """
        Validate input and output files
        
        Args:
            input_file: Input file path
            output_file: Output file path
            
        Returns:
            Error message if validation fails, None otherwise
        """
        if not Path(input_file).exists():
            return f"Input file not found: {input_file}"
        
        if not Path(input_file).is_file():
            return f"Input path is not a file: {input_file}"
        
        # Create output directory if needed
        try:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return f"Cannot create output directory: {e}"
        
        return None
