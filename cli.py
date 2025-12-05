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
  
  # Görsel dönüştürme
  python cli.py convert scan.png --to pdf
  python cli.py convert photo.jpg --to markdown
  
  # OCR modu ile PDF dönüştürme (sunum PDF'leri için önerilen)
  python cli.py convert presentation.pdf --to markdown --ocr
  python cli.py convert presentation.pdf --to docx --ocr --ocr-lang tur
  
  # LLM ile gelişmiş dönüştürme (en yüksek kalite!)
  python cli.py convert math_doc.pdf --to markdown --ocr --llm
  python cli.py convert math_doc.pdf --to markdown --ocr --llm --llm-provider ollama
  
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
    convert_parser.add_argument('input', help='Girdi dosyası (pdf, docx, markdown, html, png, jpg, jpeg)')
    convert_parser.add_argument('--to', '-t', required=True, dest='format', help='Hedef format (pdf, docx, markdown, html)')
    convert_parser.add_argument('--output', '-o', help='Çıktı dosyası (opsiyonel)')
    convert_parser.add_argument('--quality-check', '-q', action='store_true', help='AI kalite kontrolü yap')
    
    # OCR options
    convert_parser.add_argument('--ocr', action='store_true', help='OCR modu kullan (sunum PDF\'leri için önerilen)')
    convert_parser.add_argument('--ocr-lang', default='eng', help='OCR dili (örn: eng, tur, deu). Varsayılan: eng')
    convert_parser.add_argument('--ocr-dpi', type=int, default=2, help='OCR çözünürlük çarpanı (1-4). Varsayılan: 2')
    
    # LLM options
    convert_parser.add_argument('--llm', action='store_true', help='LLM post-processing kullan (en yüksek kalite)')
    convert_parser.add_argument('--llm-provider', default='auto', 
                               choices=['auto', 'ollama', 'huggingface', 'gemini'],
                               help='LLM sağlayıcı: auto, ollama (yerel), huggingface, gemini')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Toplu dönüştürme')
    batch_parser.add_argument('--input-folder', '-i', required=True, help='Girdi klasörü')
    batch_parser.add_argument('--format', '-f', required=True, help='Hedef format')
    batch_parser.add_argument('--output-folder', '-o', help='Çıktı klasörü (opsiyonel)')
    batch_parser.add_argument('--quality-check', '-q', action='store_true', help='AI kalite kontrolü yap')
    batch_parser.add_argument('--pattern', '-p', default='*', help='Dosya deseni (örn: *.pdf)')
    
    # List formats command
    list_parser = subparsers.add_parser('list-formats', help='Desteklenen formatları listele')
    
    # Check LLM providers command
    llm_parser = subparsers.add_parser('check-llm', help='LLM sağlayıcılarının durumunu kontrol et')
    
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
    elif args.command == 'check-llm':
        check_llm_providers()


def convert_file(args):
    """Convert single file"""
    logger.info(f"Dönüştürme başlatılıyor: {args.input} -> {args.format}")
    
    # Check if input file exists
    if not Path(args.input).exists():
        logger.error(f"Dosya bulunamadı: {args.input}")
        sys.exit(1)
    
    # Create converter
    converter = UniversalConverter()
    
    # Prepare options
    options = {}
    
    # OCR options
    if hasattr(args, 'ocr') and args.ocr:
        options['use_ocr'] = True
        options['ocr_lang'] = getattr(args, 'ocr_lang', 'eng')
        options['ocr_dpi'] = getattr(args, 'ocr_dpi', 2)
        logger.info(f"OCR modu aktif - Dil: {options['ocr_lang']}, DPI: {options['ocr_dpi']}x")
    
    # LLM options
    if hasattr(args, 'llm') and args.llm:
        options['use_llm'] = True
        options['llm_provider'] = getattr(args, 'llm_provider', 'auto')
        logger.info(f"LLM post-processing aktif - Provider: {options['llm_provider']}")
        
        # Check for API keys in environment
        import os
        if os.environ.get('HUGGINGFACE_API_KEY'):
            options['huggingface_api_key'] = os.environ['HUGGINGFACE_API_KEY']
        if os.environ.get('GOOGLE_API_KEY'):
            options['google_api_key'] = os.environ['GOOGLE_API_KEY']
    
    # Convert
    result = converter.convert(
        input_file=args.input,
        output_format=args.format,
        output_file=args.output,
        quality_check=args.quality_check,
        **options
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


def check_llm_providers():
    """Check available LLM providers"""
    print("\n🤖 LLM Sağlayıcı Durumu\n")
    print("=" * 50)
    
    try:
        from ai.llm_post_processor import LLMPostProcessor
        
        processor = LLMPostProcessor(provider='auto')
        info = processor.get_provider_info()
        
        for name, status in info.items():
            available = status['available']
            active = status['active']
            
            if available:
                icon = "✅" if active else "🟢"
                status_text = "(AKTİF)" if active else "(Kullanılabilir)"
            else:
                icon = "❌"
                status_text = "(Kullanılamıyor)"
            
            print(f"  {icon} {name.upper():15} {status_text}")
        
        print("\n" + "=" * 50)
        print("\n📋 Kurulum Talimatları:\n")
        
        print("  🔹 OLLAMA (Yerel, Ücretsiz - ÖNERİLEN)")
        print("     1. https://ollama.ai adresinden indir")
        print("     2. 'ollama pull llama3.2' komutu ile model indir")
        print("     3. Ollama otomatik olarak algılanacak\n")
        
        print("  🔹 HUGGINGFACE (Bulut, Ücretsiz Tier)")
        print("     1. https://huggingface.co/settings/tokens adresinden token al")
        print("     2. HUGGINGFACE_API_KEY ortam değişkenini ayarla")
        print("     3. Windows: set HUGGINGFACE_API_KEY=hf_xxx\n")
        
        print("  🔹 GOOGLE GEMINI (Bulut, Ücretsiz Tier)")
        print("     1. https://makersuite.google.com/app/apikey adresinden API key al")
        print("     2. GOOGLE_API_KEY ortam değişkenini ayarla")
        print("     3. pip install google-generativeai\n")
        
    except ImportError as e:
        print(f"  ⚠️  LLM modülü yüklenemedi: {e}")
        print("     Gerekli paketleri yükleyin: pip install requests")


if __name__ == '__main__':
    main()
