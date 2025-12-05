"""
Final comparison and quality assessment
"""

def compare_outputs():
    print("=" * 70)
    print("KARŞILAŞTIRMA: Beklenen Çıktı vs OCR Çıktısı")
    print("=" * 70)
    
    # Read expected output
    with open('2D_Poisson_FEM.md', 'r', encoding='utf-8') as f:
        expected = f.read()
    
    # Read OCR output
    with open('test_outputs/2D_Poisson_FEM_math_ocr.md', 'r', encoding='utf-8') as f:
        ocr_output = f.read()
    
    print(f"\n📊 Boyut Karşılaştırması:")
    print(f"  Beklenen: {len(expected):,} karakter")
    print(f"  OCR:      {len(ocr_output):,} karakter")
    
    # Check for key elements
    print(f"\n🔍 Anahtar Element Kontrolü:")
    
    elements = [
        ('LaTeX inline ($...$)', expected.count('$') - expected.count('$$'), ocr_output.count('$') - ocr_output.count('$$')),
        ('LaTeX block ($$...$$)', expected.count('$$'), ocr_output.count('$$')),
        ('Başlık (##)', expected.count('##'), ocr_output.count('##')),
        ('Madde işareti (*)', expected.count('* '), ocr_output.count('* ')),
        ('Omega (Ω/$\\Omega$)', expected.count('Omega') + expected.count('Ω'), ocr_output.count('Omega') + ocr_output.count('Ω')),
        ('Nabla (∇/$\\nabla$)', expected.count('nabla') + expected.count('∇'), ocr_output.count('nabla') + ocr_output.count('∇')),
        ('Delta (Δ/$\\Delta$)', expected.count('Delta') + expected.count('Δ'), ocr_output.count('Delta') + ocr_output.count('Δ')),
    ]
    
    print(f"  {'Element':<30} | {'Beklenen':>10} | {'OCR':>10}")
    print(f"  {'-'*30}-+-{'-'*10}-+-{'-'*10}")
    for name, exp_count, ocr_count in elements:
        status = "✅" if ocr_count >= exp_count * 0.5 else "⚠️"
        print(f"  {name:<30} | {exp_count:>10} | {ocr_count:>10} {status}")
    
    # Sample content comparison
    print(f"\n📝 İçerik Örnekleri:")
    
    print(f"\n--- BEKLENEN (Strong Formulation bölümü) ---")
    start = expected.find("## 2. Strong")
    if start > 0:
        end = expected.find("## 3.", start)
        print(expected[start:end][:600])
    
    print(f"\n--- OCR ÇIKTISI (Strong Formulation bölümü) ---")
    start = ocr_output.find("Goal: Find")
    if start > 0:
        print(ocr_output[start:start+600])
    
    print("\n" + "=" * 70)
    print("📋 SONUÇ VE ÖNERİLER")
    print("=" * 70)
    print("""
    ✅ Başarılı Noktalar:
       - OCR text çıkarma çalışıyor
       - Temel yapı korunuyor
       - Bazı matematik sembolleri dönüştürülüyor
    
    ⚠️  İyileştirme Gereken Alanlar:
       - LaTeX denklemleri tam olarak oluşturulmuyor
       - Bazı OCR hataları düzeltilemiyor
       - Görsel içerikler (grafikler) kaybolıyor
    
    💡 Öneriler:
       1. Daha yüksek DPI (300+) kullanın
       2. Türkçe içerik için --ocr-lang tur+eng kullanın
       3. Manuel düzeltme için çıktıyı kontrol edin
       4. AI destekli düzeltme için LLM entegrasyonu düşünülebilir
    """)

if __name__ == '__main__':
    compare_outputs()
