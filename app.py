"""
ConverterAI Flask Web Application
"""
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import time
import uuid
from datetime import datetime

from converters import UniversalConverter
from utils.file_handler import FileHandler
from utils.validator import Validator
from utils.logger import setup_logger
from config import (
    APP_HOST, APP_PORT, DEBUG,
    UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER,
    MAX_FILE_SIZE_BYTES, ALLOWED_EXTENSIONS,
    SUPPORTED_CONVERSIONS
)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_BYTES
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = str(OUTPUT_FOLDER)

# Enable CORS
CORS(app)

# Initialize components
logger = setup_logger()
converter = UniversalConverter()
file_handler = FileHandler()
validator = Validator()

# Store conversion tasks
conversion_tasks = {}


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/supported-conversions', methods=['GET'])
def get_supported_conversions():
    """Get list of supported conversions"""
    return jsonify({
        'success': True,
        'conversions': SUPPORTED_CONVERSIONS
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Secure filename
        filename = secure_filename(file.filename)
        filename = validator.sanitize_filename(filename)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = Path(app.config['UPLOAD_FOLDER']) / unique_filename
        
        # Save file
        file.save(str(file_path))
        
        # Validate file
        is_valid, error = validator.validate_file(str(file_path))
        if not is_valid:
            file_handler.safe_delete(str(file_path))
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        # Detect format
        file_format = validator.get_file_format(str(file_path))
        if not file_format:
            file_handler.safe_delete(str(file_path))
            return jsonify({
                'success': False,
                'error': 'Unsupported file format'
            }), 400
        
        # Get file info
        file_info = file_handler.get_file_info(str(file_path))
        
        logger.info(f"File uploaded: {filename} ({file_format})")
        
        return jsonify({
            'success': True,
            'file_id': unique_filename,
            'original_name': filename,
            'format': file_format,
            'size': file_info['size'],
            'size_mb': round(file_info['size_mb'], 2)
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/convert', methods=['POST'])
def convert_file():
    """Handle file conversion - supports both direct upload or file_id"""
    try:
        # Check if this is multipart/form-data (direct upload) or JSON (file_id reference)
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Direct upload + conversion
            if 'file' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file provided'
                }), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            # Get output format from form data
            output_format = request.form.get('output_format')
            quality_check = request.form.get('quality_check', 'false').lower() == 'true'
            
            if not output_format:
                return jsonify({
                    'success': False,
                    'error': 'Output format not specified'
                }), 400
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = Path(app.config['UPLOAD_FOLDER']) / unique_filename
            file.save(str(file_path))
            
            input_file = file_path
            file_id = unique_filename
            
        else:
            # JSON request with file_id reference
            data = request.get_json()
            
            file_id = data.get('file_id')
            output_format = data.get('output_format')
            quality_check = data.get('quality_check', False)
            
            if not file_id or not output_format:
                return jsonify({
                    'success': False,
                    'error': 'Missing required parameters'
                }), 400
            
            # Get input file
            input_file = Path(app.config['UPLOAD_FOLDER']) / file_id
            if not input_file.exists():
                return jsonify({
                    'success': False,
                    'error': 'File not found'
                }), 404
        
        # Validate conversion
        input_format = validator.get_file_format(str(input_file))
        is_valid, error = validator.validate_conversion(input_format, output_format)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error
            }), 400
        
        # Generate output filename with original name and timestamp
        # Get original filename without extension
        original_name = Path(input_file).stem
        # Clean the UUID prefix if it exists
        if '_' in original_name:
            original_name = '_'.join(original_name.split('_')[1:])
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create meaningful filename: originalname_timestamp.format
        output_filename = f"{original_name}_{timestamp}.{output_format}"
        if output_format == 'markdown':
            output_filename = output_filename.replace('.markdown', '.md')
        
        output_file = Path(app.config['OUTPUT_FOLDER']) / output_filename
        
        # Create task ID
        task_id = str(uuid.uuid4())
        conversion_tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': 'Starting conversion...'
        }
        
        logger.info(f"Starting conversion: {file_id} -> {output_format}")
        
        # Perform conversion
        start_time = time.time()
        result = converter.convert(
            str(input_file),
            input_format=input_format,
            output_format=output_format,
            output_file=str(output_file),
            quality_check=quality_check
        )
        
        processing_time = time.time() - start_time
        
        if result.success:
            conversion_tasks[task_id] = {
                'status': 'completed',
                'progress': 100,
                'message': 'Conversion completed successfully',
                'output_file': output_filename,
                'processing_time': round(processing_time, 2),
                'quality_score': result.quality_score,
                'warnings': result.warnings
            }
            
            logger.info(f"Conversion successful: {output_filename}")
            
            return jsonify({
                'success': True,
                'task_id': task_id,
                'output_file': output_filename,
                'output_format': output_format,
                'processing_time': round(processing_time, 2),
                'quality_score': result.quality_score,
                'warnings': result.warnings
            })
        else:
            conversion_tasks[task_id] = {
                'status': 'failed',
                'progress': 0,
                'message': result.error
            }
            
            logger.error(f"Conversion failed: {result.error}")
            
            return jsonify({
                'success': False,
                'task_id': task_id,
                'error': result.error
            }), 500
        
    except Exception as e:
        logger.error(f"Conversion error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download converted file"""
    try:
        # Secure filename
        filename = secure_filename(filename)
        file_path = Path(app.config['OUTPUT_FOLDER']) / filename
        
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        logger.info(f"Downloading file: {filename}")
        
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Get conversion task status"""
    if task_id not in conversion_tasks:
        return jsonify({
            'success': False,
            'error': 'Task not found'
        }), 404
    
    return jsonify({
        'success': True,
        'task': conversion_tasks[task_id]
    })


@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Clean up old files"""
    try:
        data = request.get_json()
        hours = data.get('hours', 24)
        
        upload_deleted = file_handler.cleanup_directory(
            app.config['UPLOAD_FOLDER'],
            hours
        )
        output_deleted = file_handler.cleanup_directory(
            app.config['OUTPUT_FOLDER'],
            hours
        )
        
        return jsonify({
            'success': True,
            'deleted': {
                'uploads': upload_deleted,
                'outputs': output_deleted,
                'total': upload_deleted + output_deleted
            }
        })
        
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'version': '1.0.0'
    })


@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': f'File too large. Maximum size: {MAX_FILE_SIZE_BYTES / (1024*1024)}MB'
    }), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal error: {e}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting ConverterAI on {APP_HOST}:{APP_PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    # Clean up old files on startup
    file_handler.cleanup_directory(str(UPLOAD_FOLDER), 24)
    file_handler.cleanup_directory(str(OUTPUT_FOLDER), 24)
    
    app.run(
        host=APP_HOST,
        port=APP_PORT,
        debug=DEBUG
    )
