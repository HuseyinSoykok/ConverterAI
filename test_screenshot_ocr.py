"""
Real Screenshot OCR Test - Gerçek ekran görüntüsü testi
Tests OCR on realistic screenshot-like content
"""
from PIL import Image, ImageDraw, ImageFont
from converters.image_converter import ImageConverter
import time

def create_screenshot_test_image():
    """Create realistic screenshot-like image"""
    width, height = 1400, 1000
    
    # Create image with gray background (like a window)
    image = Image.new('RGB', (width, height), '#f0f0f0')
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_normal = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 18)
        font_mono = ImageFont.truetype("consola.ttf", 20)  # Monospace
    except:
        font_title = font_normal = font_small = font_mono = ImageFont.load_default()
    
    # Draw window header (like a browser or app)
    draw.rectangle([0, 0, width, 60], fill='#2c3e50')
    draw.text((20, 15), "📄 Belge Görüntüleyici - Document.txt", 
              fill='white', font=font_title)
    
    # Content area (white background)
    draw.rectangle([10, 70, width-10, height-10], fill='white', outline='#cccccc', width=2)
    
    y = 100
    x = 40
    
    # Document content
    draw.text((x, y), "TÜRKİYE CUMHURİYETİ", fill='black', font=font_title)
    y += 60
    
    draw.text((x, y), "Resmi Belge No: 2025/TR/12345", fill='#555555', font=font_small)
    y += 40
    
    draw.text((x, y), "Tarih: 12 Kasım 2025", fill='#555555', font=font_small)
    y += 50
    
    # Main content
    content_lines = [
        "Konu: Proje Onay Belgesi",
        "",
        "Sayın Yetkili,",
        "",
        "ConverterAI projesinin geliştirilmesi ve test edilmesi sürecinde",
        "aşağıdaki özellikler başarıyla tamamlanmıştır:",
        "",
        "1. OCR (Optik Karakter Tanıma) sistemi entegre edildi",
        "2. Türkçe karakter desteği %100 çalışır durumda",
        "3. Görsel formatları (PNG, JPG, JPEG) destekleniyor",
        "4. Çıktı formatları: PDF, DOCX, HTML, Markdown",
        "",
        "Test Sonuçları:",
        "• Basılı metin: %91.7 doğruluk",
        "• El yazısı: %93.7 doğruluk",
        "• Tablo tanıma: Aktif (temel seviye)",
        "",
        "Sistem şu anda üretim için hazır durumda.",
        "",
        "İletişim: info@converterai.com",
        "Telefon: +90 (312) 555-1234"
    ]
    
    for line in content_lines:
        if line.startswith("1.") or line.startswith("2.") or \
           line.startswith("3.") or line.startswith("4."):
            draw.text((x + 20, y), line, fill='#2c3e50', font=font_normal)
        elif line.startswith("•"):
            draw.text((x + 20, y), line, fill='#e74c3c', font=font_normal)
        elif "%" in line or "Sonuç" in line:
            draw.text((x, y), line, fill='#27ae60', font=font_normal)
        else:
            draw.text((x, y), line, fill='black', font=font_normal)
        y += 35
    
    # Footer (like a status bar)
    draw.rectangle([0, height-40, width, height], fill='#ecf0f1')
    draw.text((20, height-30), "Sayfa 1/1 | Karakter: 856 | Kelime: 142", 
              fill='#555555', font=font_small)
    
    # Save
    filename = 'test_screenshot.png'
    image.save(filename)
    print(f"✅ Created {filename}")
    return filename

def test_screenshot_ocr():
    """Test screenshot OCR"""
    print("=" * 70)
    print("  EKRAN GÖRÜNTÜSÜ OCR TESTİ - Screenshot Recognition")
    print("=" * 70)
    print()
    
    print("📸 Gerçekçi ekran görüntüsü oluşturuluyor...")
    image_file = create_screenshot_test_image()
    print()
    
    converter = ImageConverter()
    
    formats = ['md', 'html', 'docx']
    
    for fmt in formats:
        output_file = f'test_screenshot.{fmt}'
        print("=" * 50)
        print(f"TEST: Ekran Görüntüsü → {fmt.upper()}")
        print("=" * 50)
        
        start = time.time()
        result = converter.convert(image_file, output_file)
        elapsed = time.time() - start
        
        if result.success:
            print(f"✅ SUCCESS: {output_file}")
            print(f"   Dönüşüm süresi: {elapsed:.2f}s")
            if hasattr(result, 'metadata') and result.metadata:
                if 'ocr_confidence' in result.metadata:
                    print(f"   OCR Güven: {result.metadata['ocr_confidence']:.1f}%")
        else:
            print(f"❌ FAILED: {result.error}")
        print()
    
    # Analyze markdown output
    print("=" * 70)
    print("📄 MARKDOWN ÇIKTISI (İlk 800 karakter)")
    print("=" * 70)
    print()
    
    with open('test_screenshot.md', 'r', encoding='utf-8') as f:
        content = f.read()
        print(content[:800])
        if len(content) > 800:
            print(f"\n... (toplam {len(content)} karakter)")
    
    print()
    print("=" * 70)
    print("🔍 İÇERİK ANALİZİ")
    print("=" * 70)
    print()
    
    # Check key elements
    checks = {
        "Başlık": "TÜRKİYE CUMHURİYETİ" in content.upper(),
        "Belge No": "2025" in content and "12345" in content,
        "Tarih": "12 Kasım 2025" in content or "Kasım" in content,
        "Numaralı liste": any(f"{i}." in content for i in range(1, 5)),
        "İletişim bilgisi": "info@converterai.com" in content or "@" in content,
        "Yüzde değerleri": "%" in content,
        "Telefon": "+90" in content or "312" in content
    }
    
    for item, found in checks.items():
        status = "✅" if found else "⚠️"
        print(f"   {status} {item}: {'Bulundu' if found else 'Bulunamadı'}")
    
    success_rate = sum(checks.values()) / len(checks) * 100
    print()
    print(f"   📊 İçerik doğruluğu: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print(f"   🎉 Mükemmel! Ekran görüntüsü başarıyla tanındı!")
    elif success_rate >= 60:
        print(f"   ✅ İyi! Çoğu içerik doğru tanındı.")
    else:
        print(f"   ⚠️ Bazı detaylar eksik olabilir.")
    
    print()
    print("=" * 70)
    print("  TEST TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    test_screenshot_ocr()
