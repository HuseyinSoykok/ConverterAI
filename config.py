"""
ConverterAI Configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Application settings
APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
APP_PORT = int(os.getenv('APP_PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# API Keys (optional for AI features)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# AI Quality Check Method
AI_QUALITY_METHOD = os.getenv('AI_QUALITY_METHOD', 'heuristic')

# File paths
UPLOAD_FOLDER = BASE_DIR / os.getenv('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = BASE_DIR / os.getenv('OUTPUT_FOLDER', 'outputs')
TEMP_FOLDER = BASE_DIR / os.getenv('TEMP_FOLDER', 'temp')

# Create folders if they don't exist
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    folder.mkdir(exist_ok=True)

# File upload settings
MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {
    'pdf': ['.pdf'],
    'docx': ['.docx', '.doc'],
    'markdown': ['.md', '.markdown'],
    'html': ['.html', '.htm'],
    'image': ['.png', '.jpg', '.jpeg']
}

# Conversion settings
DEFAULT_DPI = int(os.getenv('DEFAULT_DPI', 300))
OCR_LANGUAGE = os.getenv('OCR_LANGUAGE', 'tur+eng')
ENABLE_AI_QUALITY_CHECK = os.getenv('ENABLE_AI_QUALITY_CHECK', 'True').lower() == 'true'

# Tesseract OCR Path
TESSERACT_CMD = os.getenv('TESSERACT_CMD', '')

# Supported conversions
SUPPORTED_CONVERSIONS = {
    'pdf': ['docx', 'markdown', 'html'],
    'docx': ['pdf', 'markdown', 'html'],
    'markdown': ['pdf', 'docx', 'html'],
    'html': ['pdf', 'docx', 'markdown'],
    'image': ['pdf', 'docx', 'markdown', 'html']
}

# Quality check thresholds (adjusted for improved scoring system)
QUALITY_THRESHOLDS = {
    'excellent': 0.90,      # 90%+ - Outstanding quality
    'very_good': 0.80,      # 80-89% - Very good quality
    'good': 0.70,           # 70-79% - Good quality
    'acceptable': 0.60,     # 60-69% - Acceptable quality
    'poor': 0.50            # 50-59% - Poor quality
    # Below 50% = failed
}

# Logging
LOG_FILE = BASE_DIR / 'logs' / 'converter.log'
LOG_FILE.parent.mkdir(exist_ok=True)
