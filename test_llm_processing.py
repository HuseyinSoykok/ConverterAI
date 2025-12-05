"""
Test LLM Post-Processing

Bu script LLM post-processing özelliğini test eder.

Önce bir LLM sağlayıcısı kurulmalı:

1. OLLAMA (Önerilen - Yerel, Ücretsiz):
   - https://ollama.ai adresinden indir
   - Terminal'de: ollama pull llama3.2
   - Otomatik olarak algılanacak

2. HUGGINGFACE:
   - HUGGINGFACE_API_KEY ortam değişkenini ayarla
   
3. GOOGLE GEMINI:
   - pip install google-generativeai
   - GOOGLE_API_KEY ortam değişkenini ayarla
"""

import os
import sys

def test_llm_availability():
    """Test which LLM providers are available"""
    print("=" * 60)
    print("LLM Sağlayıcı Testi")
    print("=" * 60)
    
    from ai.llm_post_processor import LLMPostProcessor
    
    processor = LLMPostProcessor(provider='auto')
    info = processor.get_provider_info()
    
    print("\n📊 Sağlayıcı Durumu:")
    for name, status in info.items():
        icon = "✅" if status['available'] else "❌"
        active = " (AKTİF)" if status['active'] else ""
        print(f"  {icon} {name}{active}")
    
    return processor.is_available()


def test_llm_processing():
    """Test LLM processing with sample text"""
    print("\n" + "=" * 60)
    print("LLM İşleme Testi")
    print("=" * 60)
    
    from ai.llm_post_processor import LLMPostProcessor
    
    processor = LLMPostProcessor(provider='auto')
    
    if not processor.is_available():
        print("\n⚠️  Hiçbir LLM sağlayıcısı kullanılamıyor!")
        print("   Lütfen yukarıdaki kurulum talimatlarını takip edin.")
        return False
    
    # Sample OCR text (simulating poor OCR output)
    sample_text = """
    Strong Formulation of the Poisson Equation
    
    Goal: Find the unknown function u (e.g., temperature) on a domain Q, given a source f.
    
    Find u: Q -> R such that:
    -Au = f in Q (Poisson's Equation)
    u = 0 on dQ (Boundary Condition)
    
    The Laplace operator A is defined as:
    Au = d2u/dx2 + d2u/dy2
    
    Problem: Requires u to be twice-differentiable (C2).
    """
    
    print(f"\n📥 Girdi Metni ({len(sample_text)} karakter):")
    print("-" * 40)
    print(sample_text[:300] + "...")
    
    print(f"\n🔄 İşleniyor ({processor.provider_name} kullanılıyor)...")
    
    try:
        result, metadata = processor.process_math_document(sample_text)
        
        print(f"\n📤 Çıktı Metni ({len(result)} karakter):")
        print("-" * 40)
        print(result[:500] + "..." if len(result) > 500 else result)
        
        print(f"\n📊 Meta Veri:")
        print(f"  Provider: {metadata.get('provider')}")
        print(f"  Chunks: {metadata.get('chunks')}")
        print(f"  Processed: {metadata.get('processed')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        return False


def test_pdf_conversion_with_llm():
    """Test full PDF to Markdown conversion with LLM"""
    print("\n" + "=" * 60)
    print("PDF Dönüştürme Testi (LLM ile)")
    print("=" * 60)
    
    from converters.pdf_converter import PDFConverter
    
    pdf_file = '2D_Poisson_FEM.pdf'
    output_file = 'test_outputs/2D_Poisson_FEM_llm.md'
    
    if not os.path.exists(pdf_file):
        print(f"\n⚠️  Test dosyası bulunamadı: {pdf_file}")
        return False
    
    converter = PDFConverter()
    
    print(f"\n📄 Girdi: {pdf_file}")
    print(f"📝 Çıktı: {output_file}")
    print("\n🔄 Dönüştürülüyor (bu birkaç dakika sürebilir)...")
    
    try:
        result = converter.convert(
            pdf_file, 
            output_file,
            use_ocr=True,
            use_llm=True,
            llm_provider='auto',
            ocr_dpi=3
        )
        
        if result.success:
            print(f"\n✅ Dönüştürme başarılı!")
            print(f"⏱️  Süre: {result.processing_time:.2f} saniye")
            print(f"📊 Sayfa: {result.metadata.get('pages')}")
            print(f"🤖 LLM: {result.metadata.get('llm_provider')}")
            
            # Show sample output
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n📝 Çıktı Örneği (ilk 1000 karakter):")
            print("-" * 40)
            print(content[:1000])
            
            return True
        else:
            print(f"\n❌ Dönüştürme başarısız: {result.error}")
            return False
            
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("ConverterAI - LLM Post-Processing Test")
    print("=" * 60)
    
    # Test 1: Check availability
    available = test_llm_availability()
    
    if not available:
        print("\n" + "=" * 60)
        print("⚠️  LLM sağlayıcısı bulunamadı!")
        print("=" * 60)
        print("""
Lütfen aşağıdaki seçeneklerden birini kurun:

1. OLLAMA (Önerilen):
   - Windows: https://ollama.ai/download/windows
   - Sonra terminal'de: ollama pull llama3.2
   
2. HUGGINGFACE:
   - https://huggingface.co/settings/tokens
   - set HUGGINGFACE_API_KEY=hf_xxxxx
   
3. GOOGLE GEMINI:
   - pip install google-generativeai
   - https://makersuite.google.com/app/apikey
   - set GOOGLE_API_KEY=AIzaxxxx
        """)
        sys.exit(1)
    
    # Test 2: Test processing
    success = test_llm_processing()
    
    if success:
        # Test 3: Full PDF conversion
        print("\n" + "-" * 60)
        response = input("\nPDF dönüştürme testini çalıştırmak ister misiniz? (e/h): ")
        if response.lower() in ['e', 'y', 'yes', 'evet']:
            test_pdf_conversion_with_llm()
    
    print("\n✅ Test tamamlandı!")
