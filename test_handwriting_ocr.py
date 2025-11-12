"""
Handwriting OCR Test - El yazısı tanıma testi
Tests handwritten Turkish text recognition with special characters
"""
from PIL import Image, ImageDraw, ImageFont
from converters.image_converter import ImageConverter
import time
import random

def create_handwriting_test_image():
    """
    Create test image that simulates handwritten text
    Uses a handwriting-style font or creates simulated handwriting
    """
    # Create image
    width, height = 1200, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to find a handwriting-style font
    handwriting_fonts = [
        "C:\\Windows\\Fonts\\segoepr.ttf",  # Segoe Print (handwriting-like)
        "C:\\Windows\\Fonts\\segoeprb.ttf", # Segoe Print Bold
        "C:\\Windows\\Fonts\\comic.ttf",     # Comic Sans (readable handwriting-like)
        "C:\\Windows\\Fonts\\gabriola.ttf",  # Gabriola (decorative)
        "arial.ttf"  # Fallback
    ]
    
    font_large = None
    font_medium = None
    font_small = None
    used_font = "default"
    
    for font_path in handwriting_fonts:
        try:
            font_large = ImageFont.truetype(font_path, 56)
            font_medium = ImageFont.truetype(font_path, 38)
            font_small = ImageFont.truetype(font_path, 30)
            used_font = font_path.split("\\")[-1]
            print(f"✅ Using font: {used_font}")
            break
        except:
            continue
    
    if font_large is None:
        print("⚠️ Using default font (handwriting fonts not found)")
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    y = 50
    
    # Title with slight variations (simulate handwriting imperfection)
    title = "El Yazısı Testi"
    draw.text((50, y), title, fill='black', font=font_large)
    y += 90
    
    # Add a note about handwriting
    draw.text((50, y), "Bu metin el yazısı stilinde yazılmıştır.", 
              fill='darkblue', font=font_small)
    y += 60
    
    # Section 1: Turkish characters in context
    draw.text((50, y), "Türkçe Karakterler:", fill='black', font=font_medium)
    y += 55
    
    turkish_sentences = [
        "İstanbul çok güzel bir şehirdir.",
        "Öğretmen öğrencilere ders anlatıyor.",
        "Çocuğum şimdi okula gidiyor.",
        "Ağaç gölgesinde dinleniyoruz.",
        "Üzüm bağında çalışıyorlar."
    ]
    
    for sentence in turkish_sentences:
        # Add slight random offset to simulate handwriting variation
        x_offset = random.randint(-3, 3) if used_font != "default" else 0
        draw.text((70 + x_offset, y), sentence, fill='black', font=font_small)
        y += 45
    
    y += 20
    
    # Section 2: Mixed text with special characters
    draw.text((50, y), "Karışık Cümle:", fill='black', font=font_medium)
    y += 55
    
    mixed_text = [
        "İşçi, mühendis ve öğretmen",
        "şehir merkezinde buluştular.",
        "Çünkü önemli bir görüşmeleri vardı."
    ]
    
    for line in mixed_text:
        x_offset = random.randint(-3, 3) if used_font != "default" else 0
        draw.text((70 + x_offset, y), line, fill='black', font=font_small)
        y += 45
    
    y += 20
    
    # Section 3: Common challenges for OCR
    draw.text((50, y), "Zorlu Kelimeler:", fill='black', font=font_medium)
    y += 55
    
    challenging_words = [
        "İİİ ııı ŞŞŞ şşş ÖÖÖ ööö",
        "Çağrışım, düğümleme, öğrenim",
        "Ünlü, ışık, şövalye, çığlık"
    ]
    
    for line in challenging_words:
        x_offset = random.randint(-2, 2) if used_font != "default" else 0
        draw.text((70 + x_offset, y), line, fill='black', font=font_small)
        y += 45
    
    y += 30
    
    # Section 4: Numbers and dates (common in handwriting)
    draw.text((50, y), "Tarih ve Sayılar:", fill='black', font=font_medium)
    y += 55
    
    draw.text((70, y), "12 Kasım 2025 - Salı günü", fill='black', font=font_small)
    y += 45
    draw.text((70, y), "Saat: 14:30, Yer: Ankara", fill='black', font=font_small)
    
    # Add some noise/texture to make it more realistic
    # (Optional: add slight gray texture to simulate paper)
    
    # Save
    filename = 'test_handwriting.png'
    image.save(filename)
    print(f"✅ Created {filename}")
    return filename

def analyze_handwriting_results(markdown_file, original_text_samples):
    """
    Analyze handwriting OCR results for accuracy
    
    Args:
        markdown_file: Path to OCR output markdown file
        original_text_samples: List of original text samples to compare
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()
    
    print(f"{'=' * 70}")
    print("🔍 EL YAZISI TANIMA ANALİZİ")
    print(f"{'=' * 70}")
    print()
    
    # Check for Turkish characters
    turkish_chars = ['İ', 'ı', 'Ş', 'ş', 'Ğ', 'ğ', 'Ö', 'ö', 'Ü', 'ü', 'Ç', 'ç']
    char_found = {}
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        original_content = f.read()  # Case-sensitive
    
    for char in turkish_chars:
        count = original_content.count(char)
        char_found[char] = count
    
    print("Türkçe Karakter Tanıma:")
    for char in turkish_chars:
        count = char_found[char]
        status = "✅" if count > 0 else "⚠️"
        print(f"   {status} '{char}': {count} kez")
    
    total_chars = sum(char_found.values())
    present_types = sum(1 for c in char_found.values() if c > 0)
    
    print()
    print(f"   Toplam Türkçe karakter: {total_chars}")
    print(f"   Karakter çeşidi: {present_types}/{len(turkish_chars)}")
    
    # Calculate accuracy score
    accuracy_score = (present_types / len(turkish_chars)) * 100
    
    print()
    print(f"📊 PERFORMANS SKORU:")
    if accuracy_score >= 90:
        print(f"   ⭐⭐⭐ Mükemmel: {accuracy_score:.1f}%")
    elif accuracy_score >= 70:
        print(f"   ⭐⭐ İyi: {accuracy_score:.1f}%")
    elif accuracy_score >= 50:
        print(f"   ⭐ Orta: {accuracy_score:.1f}%")
    else:
        print(f"   ⚠️ Zayıf: {accuracy_score:.1f}%")
    
    print()
    
    # Check for key words
    print("Anahtar Kelime Kontrolü:")
    key_words = [
        ('istanbul', 'İstanbul'),
        ('öğretmen', 'Öğretmen'),
        ('çocuk', 'Çocuk'),
        ('ağaç', 'Ağaç'),
        ('üzüm', 'Üzüm'),
        ('şehir', 'Şehir'),
        ('öğrenci', 'Öğrenci')
    ]
    
    found_count = 0
    for search_word, display_word in key_words:
        if search_word in content:
            print(f"   ✅ '{display_word}' bulundu")
            found_count += 1
        else:
            print(f"   ❌ '{display_word}' bulunamadı")
    
    word_accuracy = (found_count / len(key_words)) * 100
    print()
    print(f"   Kelime tanıma oranı: {word_accuracy:.1f}% ({found_count}/{len(key_words)})")
    
    return {
        'char_accuracy': accuracy_score,
        'word_accuracy': word_accuracy,
        'total_turkish_chars': total_chars
    }

def test_handwriting_ocr():
    """Test handwriting OCR with Turkish characters"""
    print("=" * 70)
    print("  EL YAZISI OCR TESTİ - Handwriting Recognition")
    print("=" * 70)
    print()
    
    # Create test image
    print("📝 El yazısı stili test görseli oluşturuluyor...")
    image_file = create_handwriting_test_image()
    print()
    
    # Test conversions
    converter = ImageConverter()
    
    formats = {
        'markdown': 'test_handwriting.md',
        'html': 'test_handwriting.html',
        'pdf': 'test_handwriting.pdf',
        'docx': 'test_handwriting.docx'
    }
    
    results = {}
    
    for format_name, output_file in formats.items():
        print(f"{'=' * 50}")
        print(f"TEST: El Yazısı → {format_name.upper()}")
        print(f"{'=' * 50}")
        
        start = time.time()
        result = converter.convert(image_file, output_file)
        elapsed = time.time() - start
        
        if result.success:
            print(f"✅ SUCCESS: {output_file}")
            print(f"   Dönüşüm süresi: {elapsed:.2f}s")
            if hasattr(result, 'metadata') and result.metadata:
                if 'ocr_confidence' in result.metadata:
                    confidence = result.metadata['ocr_confidence']
                    print(f"   OCR Güven Skoru: {confidence:.1f}%")
                    if confidence >= 85:
                        print(f"   💚 Yüksek güven")
                    elif confidence >= 70:
                        print(f"   💛 Orta güven")
                    else:
                        print(f"   🧡 Düşük güven (el yazısı için normal)")
                if 'word_count' in result.metadata:
                    print(f"   Kelime sayısı: {result.metadata['word_count']}")
            
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
    
    # Show Markdown output
    if results['markdown']['success']:
        print(f"{'=' * 70}")
        print("📄 MARKDOWN ÇIKTISI (El Yazısı OCR)")
        print(f"{'=' * 70}")
        print()
        
        with open('test_handwriting.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:1000])
            if len(content) > 1000:
                print(f"\n... (toplam {len(content)} karakter)")
        print()
        
        # Analyze results
        original_samples = [
            "İstanbul çok güzel",
            "Öğretmen öğrencilere",
            "Çocuğum şimdi",
            "Ağaç gölgesinde",
            "Üzüm bağında"
        ]
        
        analysis = analyze_handwriting_results('test_handwriting.md', original_samples)
        
        print()
        print(f"{'=' * 70}")
        print("💡 EL YAZISI OCR HAKKINDA NOTLAR")
        print(f"{'=' * 70}")
        print()
        print("El yazısı tanıma, basılı metne göre daha zordur çünkü:")
        print("  • Her kişinin yazısı farklıdır")
        print("  • Harfler birbirine bitişiktir")
        print("  • Tutarlılık yoktur (boyut, açı, boşluk)")
        print("  • Karmaşık karakterler (İ, Ğ, Ş) zorludur")
        print()
        print("Bu testte kullanılan font el yazısı simülasyonudur.")
        print("Gerçek el yazısı için daha düşük doğruluk beklenir.")
        print()
        
        # Recommendations
        if analysis['char_accuracy'] < 70:
            print("💡 ÖNERİLER:")
            print("  1. Daha yüksek çözünürlüklü görsel kullanın")
            print("  2. Kontrastı artırın (siyah mürekkep, beyaz kağıt)")
            print("  3. Net, okunaklı yazı yazın")
            print("  4. Harflerin üst üste binmesini önleyin")
    
    print()
    print(f"{'=' * 70}")
    print("  TEST TAMAMLANDI!")
    print(f"{'=' * 70}")
    
    return results

if __name__ == "__main__":
    test_handwriting_ocr()
