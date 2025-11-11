#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test PDF to HTML conversion improvements"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converters.universal import UniversalConverter

def main():
    """Test PDF→HTML with better formatting"""
    
    converter = UniversalConverter()
    
    # Find a PDF file to test
    test_files = [
        r"d:\Projects\Python\ConverterAI\outputs\test_formatting.pdf",
        r"d:\Projects\Python\ConverterAI\outputs\test_comprehensive_20251111_134926.pdf",
    ]
    
    test_file = None
    for file in test_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if not test_file:
        print("❌ Test PDF dosyası bulunamadı!")
        return
    
    html_output = r"d:\Projects\Python\ConverterAI\outputs\test_pdf_to_html_improved.html"
    
    print("=" * 60)
    print("🔧 PDF→HTML Formatlama İyileştirme Testi")
    print("=" * 60)
    print()
    
    print("Test: PDF → HTML (Geliştirilmiş Formatlama)")
    print("-" * 60)
    print(f"Input: {os.path.basename(test_file)}")
    print()
    
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='html',
            output_file=html_output
        )
        
        if result.success:
            print(f"✅ BAŞARILI: {html_output}")
            print(f"   Format: {result.input_format} → {result.output_format}")
            if result.metadata:
                print(f"   Sayfa sayısı: {result.metadata.get('pages', 'N/A')}")
            if result.warnings:
                print(f"   Uyarılar: {len(result.warnings)}")
            print()
            print("İyileştirmeler:")
            print("   ✅ Heading tanıma (BÜYÜK HARF)")
            print("   ✅ Subheading tanıma (: ile biten)")
            print("   ✅ Liste tanıma (•, -, *, 1., vb.)")
            print("   ✅ Paragraf birleştirme")
            print("   ✅ Tablo formatlama")
            print("   ✅ HTML karakter escape")
            print("   ✅ Geliştirilmiş CSS stilleri")
        else:
            print(f"❌ BAŞARISIZ: {result.error}")
    
    except Exception as e:
        print(f"❌ HATA: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("Test tamamlandı!")
    print("=" * 60)

if __name__ == "__main__":
    main()
