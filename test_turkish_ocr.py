"""
Turkish OCR Test - Türkçe karakter tanıma testi
Tests: İ, ı, Ş, ş, Ğ, ğ, Ö, ö, Ü, ü, Ç, ç
"""
from PIL import Image, ImageDraw, ImageFont
from converters.image_converter import ImageConverter
import time

def create_turkish_test_image():
    """Create test image with Turkish characters"""
    # Create image
    width, height = 1000, 800
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a better font that supports Turkish characters
    try:
        # Try Arial first (Windows default)
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            # Try system fonts
            font_large = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 48)
            font_medium = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 32)
            font_small = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 24)
        except:
            # Fallback to default
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    y = 50
    
    # Title
    draw.text((50, y), "TÜRKÇE KARAKTER TESTİ", fill='black', font=font_large)
    y += 80
    
    # Section 1: All Turkish special characters
    draw.text((50, y), "Özel Karakterler:", fill='black', font=font_medium)
    y += 50
    draw.text((70, y), "İ ı Ş ş Ğ ğ Ö ö Ü ü Ç ç", fill='black', font=font_medium)
    y += 60
    
    # Section 2: Common Turkish words
    draw.text((50, y), "Yaygın Kelimeler:", fill='black', font=font_medium)
    y += 50
    
    turkish_words = [
        "• Türkiye - güzel bir ülkedir",
        "• İstanbul şehrinde çok insan yaşar",
        "• Öğrenci üniversitede öğrenim görüyor",
        "• Çocuğum şimdi üç yaşında",
        "• Değişiklik göstermek önemlidir"
    ]
    
    for word in turkish_words:
        draw.text((70, y), word, fill='black', font=font_small)
        y += 40
    
    y += 20
    
    # Section 3: Pangram with all Turkish letters
    draw.text((50, y), "Tüm Harfler:", fill='black', font=font_medium)
    y += 50
    draw.text((70, y), "Pijamalı hasta yağız şoföre", fill='black', font=font_small)
    y += 35
    draw.text((70, y), "çabucak güvendi.", fill='black', font=font_small)
    y += 50
    
    # Section 4: Mixed case
    draw.text((50, y), "Büyük/Küçük Harf Karışımı:", fill='black', font=font_medium)
    y += 50
    draw.text((70, y), "İÇERİK içerik ŞEHİR şehir ÖĞÜN öğün", fill='black', font=font_small)
    
    # Save
    filename = 'test_turkish_ocr.png'
    image.save(filename)
    print(f"✅ Created {filename}")
    return filename

def test_turkish_ocr():
    """Test Turkish OCR with special characters"""
    print("=" * 70)
    print("  TÜRKÇE OCR TESTİ - Turkish Character Recognition")
    print("=" * 70)
    print()
    
    # Create test image
    print("📝 Creating Turkish test image...")
    image_file = create_turkish_test_image()
    print()
    
    # Test conversions
    converter = ImageConverter()
    
    formats = {
        'markdown': 'test_turkish_ocr.md',
        'html': 'test_turkish_ocr.html',
        'pdf': 'test_turkish_ocr.pdf',
        'docx': 'test_turkish_ocr.docx'
    }
    
    results = {}
    
    for format_name, output_file in formats.items():
        print(f"{'=' * 50}")
        print(f"TEST: Image → {format_name.upper()}")
        print(f"{'=' * 50}")
        
        start = time.time()
        result = converter.convert(image_file, output_file)
        elapsed = time.time() - start
        
        if result.success:
            print(f"✅ SUCCESS: {output_file}")
            print(f"   Conversion time: {elapsed:.2f}s")
            if hasattr(result, 'metadata') and result.metadata:
                if 'ocr_confidence' in result.metadata:
                    print(f"   OCR Confidence: {result.metadata['ocr_confidence']:.1f}%")
                if 'word_count' in result.metadata:
                    print(f"   Words: {result.metadata['word_count']}")
            
            results[format_name] = {
                'success': True,
                'file': output_file,
                'time': elapsed,
                'metadata': result.metadata if hasattr(result, 'metadata') else {}
            }
        else:
            print(f"❌ FAILED: {result.error}")
            results[format_name] = {
                'success': False,
                'error': result.error
            }
        print()
    
    # Show Markdown output for inspection
    if results['markdown']['success']:
        print(f"{'=' * 70}")
        print("📄 MARKDOWN OUTPUT PREVIEW (Turkish Characters)")
        print(f"{'=' * 70}")
        print()
        
        with open('test_turkish_ocr.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:800])
            if len(content) > 800:
                print(f"\n... ({len(content)} total characters)")
        print()
    
    # Analysis of Turkish characters
    print(f"{'=' * 70}")
    print("🔍 TURKISH CHARACTER ANALYSIS")
    print(f"{'=' * 70}")
    print()
    
    if results['markdown']['success']:
        with open('test_turkish_ocr.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        turkish_chars = ['İ', 'ı', 'Ş', 'ş', 'Ğ', 'ğ', 'Ö', 'ö', 'Ü', 'ü', 'Ç', 'ç']
        char_counts = {}
        
        for char in turkish_chars:
            count = content.count(char)
            char_counts[char] = count
            status = "✅" if count > 0 else "⚠️"
            print(f"   {status} '{char}': {count} occurrences")
        
        total_turkish = sum(char_counts.values())
        print()
        print(f"   Total Turkish special characters detected: {total_turkish}")
        
        # Check if all character types present
        present = sum(1 for c in char_counts.values() if c > 0)
        print(f"   Character types present: {present}/{len(turkish_chars)}")
        
        if present == len(turkish_chars):
            print("   🎉 ALL Turkish characters successfully recognized!")
        elif present >= len(turkish_chars) * 0.8:
            print("   ✅ Most Turkish characters recognized (>80%)")
        else:
            print("   ⚠️ Some Turkish characters may be missing")
    
    print()
    print(f"{'=' * 70}")
    print("  TEST COMPLETED!")
    print(f"{'=' * 70}")
    
    return results

if __name__ == "__main__":
    test_turkish_ocr()
