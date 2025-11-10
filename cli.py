"""
ConverterAI Command Line Interface
"""
import argparse
import sys
from pathlib import Path
from typing import List

from converters import UniversalConverter
from utils.logger import setup_logger
from utils.file_handler import FileHandler
from config import SUPPORTED_CONVERSIONS

logger = setup_logger('CLI')


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='ConverterAI - AI Destekli Doküman Dönüştürücü',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # Tek dosya dönüştürme
  python cli.py convert document.pdf --to docx
  
  # Kalite kontrolü ile
  python cli.py convert document.pdf --to html --quality-check
  
  # Çıktı dosyası belirterek
  python cli.py convert input.pdf --to docx --output result.docx
  
  # Toplu dönüştürme
  python cli.py batch --input-folder ./docs --format markdown --output-folder ./converted
  
  # Desteklenen dönüşümleri listele
  python cli.py list-formats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Komutlar')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Dosya dönüştür')
    convert_parser.add_argument('input', help='Girdi dosyası')
    convert_parser.add_argument('--to', '-t', required=True, dest='format', help='Hedef format (pdf, docx, markdown, html)')
    convert_parser.add_argument('--output', '-o', help='Çıktı dosyası (opsiyonel)')
    convert_parser.add_argument('--quality-check', '-q', action='store_true', help='AI kalite kontrolü yap')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Toplu dönüştürme')
    batch_parser.add_argument('--input-folder', '-i', required=True, help='Girdi klasörü')
    batch_parser.add_argument('--format', '-f', required=True, help='Hedef format')
    batch_parser.add_argument('--output-folder', '-o', help='Çıktı klasörü (opsiyonel)')
    batch_parser.add_argument('--quality-check', '-q', action='store_true', help='AI kalite kontrolü yap')
    batch_parser.add_argument('--pattern', '-p', default='*', help='Dosya deseni (örn: *.pdf)')
    
    # List formats command
    list_parser = subparsers.add_parser('list-formats', help='Desteklenen formatları listele')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Execute command
    if args.command == 'convert':
        convert_file(args)
    elif args.command == 'batch':
        batch_convert(args)
    elif args.command == 'list-formats':
        list_formats()


def convert_file(args):
    """Convert single file"""
    logger.info(f"Dönüştürme başlatılıyor: {args.input} -> {args.format}")
    
    # Check if input file exists
    if not Path(args.input).exists():
        logger.error(f"Dosya bulunamadı: {args.input}")
        sys.exit(1)
    
    # Create converter
    converter = UniversalConverter()
    
    # Convert
    result = converter.convert(
        args.input,
        args.format,
        args.output,
        quality_check=args.quality_check
    )
    
    # Display result
    if result.success:
        print(f"\n✅ Dönüştürme başarılı!")
        print(f"📄 Çıktı dosyası: {result.output_file}")
        print(f"⏱️  İşlem süresi: {result.processing_time:.2f} saniye")
        
        if result.quality_score is not None:
            score_percent = result.quality_score * 100
            print(f"⭐ Kalite skoru: {score_percent:.1f}%")
        
        if result.warnings:
            print(f"\n⚠️  Uyarılar:")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        sys.exit(0)
    else:
        print(f"\n❌ Dönüştürme başarısız!")
        print(f"Hata: {result.error}")
        sys.exit(1)


def batch_convert(args):
    """Convert multiple files"""
    logger.info(f"Toplu dönüştürme başlatılıyor: {args.input_folder}")
    
    # Check if input folder exists
    input_path = Path(args.input_folder)
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Klasör bulunamadı: {args.input_folder}")
        sys.exit(1)
    
    # Get files
    file_handler = FileHandler()
    files = file_handler.list_files(str(input_path), args.pattern)
    
    if not files:
        logger.error(f"Klasörde dosya bulunamadı: {args.input_folder}")
        sys.exit(1)
    
    print(f"\n📦 {len(files)} dosya bulundu")
    
    # Create converter
    converter = UniversalConverter()
    
    # Convert files
    results = converter.batch_convert(
        files,
        args.format,
        args.output_folder,
        quality_check=args.quality_check
    )
    
    # Display results
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count
    
    print(f"\n📊 Sonuçlar:")
    print(f"  ✅ Başarılı: {success_count}")
    print(f"  ❌ Başarısız: {fail_count}")
    
    if fail_count > 0:
        print(f"\n⚠️  Başarısız dönüşümler:")
        for result in results:
            if not result.success:
                print(f"  - {Path(result.input_file).name}: {result.error}")
    
    sys.exit(0 if fail_count == 0 else 1)


def list_formats():
    """List supported formats and conversions"""
    print("\n🔄 Desteklenen Dönüşümler:\n")
    
    for input_format, output_formats in SUPPORTED_CONVERSIONS.items():
        print(f"📄 {input_format.upper()}")
        for output_format in output_formats:
            print(f"  → {output_format.upper()}")
        print()


if __name__ == '__main__':
    main()
