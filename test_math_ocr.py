"""
Math Formula OCR Test - Matematik formülü tanıma testi
Tests mathematical notation recognition
"""
from PIL import Image, ImageDraw, ImageFont
from converters.image_converter import ImageConverter
import time

def create_math_test_image():
    """Create test image with mathematical formulas"""
    width, height = 1200, 1100
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 42)
        font_section = ImageFont.truetype("arialbd.ttf", 32)
        font_formula = ImageFont.truetype("arial.ttf", 28)
        font_text = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = font_section = font_formula = font_text = ImageFont.load_default()
    
    y = 40
    
    # Title
    draw.text((50, y), "MATEMATİK FORMÜL TESTİ", fill='black', font=font_title)
    y += 80
    
    # Section 1: Basic arithmetic
    draw.text((50, y), "1. Temel Aritmetik", fill='darkblue', font=font_section)
    y += 50
    
    formulas_basic = [
        "a + b = c",
        "x - y = z",
        "2 × 3 = 6",
        "15 ÷ 3 = 5",
        "3² = 9",
        "√16 = 4"
    ]
    
    for formula in formulas_basic:
        draw.text((70, y), f"• {formula}", fill='black', font=font_formula)
        y += 45
    
    y += 20
    
    # Section 2: Algebraic equations
    draw.text((50, y), "2. Cebirsel Denklemler", fill='darkblue', font=font_section)
    y += 50
    
    formulas_algebra = [
        "ax² + bx + c = 0",
        "x = (-b ± √(b² - 4ac)) / 2a",
        "(a + b)² = a² + 2ab + b²",
        "sin²θ + cos²θ = 1"
    ]
    
    for formula in formulas_algebra:
        draw.text((70, y), formula, fill='#2c3e50', font=font_formula)
        y += 45
    
    y += 20
    
    # Section 3: Calculus
    draw.text((50, y), "3. Kalkülüs", fill='darkblue', font=font_section)
    y += 50
    
    formulas_calculus = [
        "∫ x dx = x²/2 + C",
        "d/dx(sin x) = cos x",
        "lim(x→0) sin(x)/x = 1",
        "∑(n=1 to ∞) 1/n²= π²/6"
    ]
    
    for formula in formulas_calculus:
        draw.text((70, y), formula, fill='#8e44ad', font=font_formula)
        y += 45
    
    y += 20
    
    # Section 4: Greek letters and symbols
    draw.text((50, y), "4. Yunan Harfleri ve Semboller", fill='darkblue', font=font_section)
    y += 50
    
    symbols = [
        "α (alfa), β (beta), γ (gama), δ (delta)",
        "π ≈ 3.14159",
        "∞ (sonsuz), ∅ (boş küme)",
        "≤ (küçük eşit), ≥ (büyük eşit)",
        "≠ (eşit değil), ≈ (yaklaşık)",
        "∈ (elemanı), ∉ (elemanı değil)"
    ]
    
    for symbol in symbols:
        draw.text((70, y), symbol, fill='#e67e22', font=font_text)
        y += 40
    
    y += 20
    
    # Section 5: Complex example
    draw.text((50, y), "5. Karmaşık Örnek", fill='darkblue', font=font_section)
    y += 50
    
    # Draw a box around the complex formula
    box_y = y
    draw.rectangle([60, box_y, width-60, box_y + 120], 
                   outline='#3498db', width=3, fill='#ecf0f1')
    
    complex_formula = [
        "Euler Formülü:",
        "e^(iπ) + 1 = 0",
        "",
        "Burada: e ≈ 2.718, i = √(-1), π ≈ 3.14"
    ]
    
    formula_y = box_y + 20
    for line in complex_formula:
        if "Euler" in line:
            draw.text((80, formula_y), line, fill='#c0392b', font=font_section)
        else:
            draw.text((100, formula_y), line, fill='black', font=font_formula)
        formula_y += 35
    
    # Save
    filename = 'test_math.png'
    image.save(filename)
    print(f"✅ Created {filename}")
    return filename

def test_math_ocr():
    """Test math formula OCR"""
    print("=" * 70)
    print("  MATEMATİK FORMÜL OCR TESTİ - Math Recognition")
    print("=" * 70)
    print()
    
    print("🔢 Matematik formülü test görseli oluşturuluyor...")
    image_file = create_math_test_image()
    print()
    
    converter = ImageConverter()
    
    print("=" * 50)
    print("TEST: Matematik Görseli → Markdown")
    print("=" * 50)
    
    # Enable math detection
    start = time.time()
    result = converter.convert(image_file, 'test_math.md', detect_math=True)
    elapsed = time.time() - start
    
    if result.success:
        print(f"✅ SUCCESS: test_math.md")
        print(f"   Dönüşüm süresi: {elapsed:.2f}s")
        if hasattr(result, 'metadata') and result.metadata:
            if 'ocr_confidence' in result.metadata:
                print(f"   OCR Güven: {result.metadata['ocr_confidence']:.1f}%")
        
        print()
        print("=" * 70)
        print("📄 MARKDOWN ÇIKTISI")
        print("=" * 70)
        print()
        
        with open('test_math.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        
        print()
        print("=" * 70)
        print("🔍 MATEMATİK SEMBOL ANALİZİ")
        print("=" * 70)
        print()
        
        # Check for mathematical symbols
        math_symbols = {
            '+': 'Toplama',
            '-': 'Çıkarma',
            '×': 'Çarpma',
            '÷': 'Bölme',
            '=': 'Eşittir',
            '²': 'Kare',
            '√': 'Karekök',
            '∫': 'İntegral',
            '∑': 'Toplam',
            'π': 'Pi',
            '∞': 'Sonsuz',
            '≤': 'Küçük eşit',
            '≥': 'Büyük eşit',
            '≠': 'Eşit değil',
            '≈': 'Yaklaşık',
            '∈': 'Elemanı',
            'α': 'Alfa',
            'β': 'Beta',
            'γ': 'Gama',
            'δ': 'Delta',
            'θ': 'Theta'
        }
        
        found_symbols = {}
        for symbol, name in math_symbols.items():
            count = content.count(symbol)
            if count > 0:
                found_symbols[symbol] = (name, count)
        
        print("Bulunan Matematik Sembolleri:")
        if found_symbols:
            for symbol, (name, count) in found_symbols.items():
                print(f"   ✅ '{symbol}' ({name}): {count} kez")
        else:
            print("   ⚠️ Özel matematik sembolleri tanınamadı")
            print("   (ASCII karakterlere dönüştürülmüş olabilir)")
        
        print()
        
        # Check for formulas
        formula_keywords = [
            ('ax²', 'Kuadratik denklem'),
            ('sin', 'Trigonometri'),
            ('cos', 'Trigonometri'),
            ('lim', 'Limit'),
            ('Euler', 'Euler formülü'),
            ('integral', 'İntegral (kelime)'),
            ('dx', 'Diferansiyel')
        ]
        
        print("Formül İçeriği Kontrolü:")
        found_formulas = 0
        for keyword, description in formula_keywords:
            if keyword in content or keyword.upper() in content.upper():
                print(f"   ✅ {description} tespit edildi")
                found_formulas += 1
            else:
                print(f"   ⚠️ {description} bulunamadı")
        
        accuracy = (found_formulas / len(formula_keywords)) * 100
        print()
        print(f"   📊 Formül tanıma oranı: {accuracy:.1f}%")
        
        print()
        print("💡 NOTLAR:")
        print("   • Temel matematik sembolleri (+ - × ÷ =) genellikle iyi tanınır")
        print("   • Özel semboller (∫ ∑ ∞ ≤ ≥) ASCII'ye dönüşebilir")
        print("   • Yunan harfleri (α β γ δ) tanınması zordur")
        print("   • Gelişmiş LaTeX dönüşümü için math_recognizer.py geliştirilecek")
        
        # Test HTML output too
        print()
        print("=" * 50)
        print("Bonus: HTML çıktısı oluşturuluyor...")
        print("=" * 50)
        
        html_result = converter.convert(image_file, 'test_math.html', detect_math=True)
        if html_result.success:
            print("✅ test_math.html oluşturuldu")
    else:
        print(f"❌ FAILED: {result.error}")
    
    print()
    print("=" * 70)
    print("  TEST TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    test_math_ocr()
