#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test HTML to PDF conversion with problematic elements"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converters.universal import UniversalConverter

def main():
    """Test HTML→PDF with links and anchors"""
    
    converter = UniversalConverter()
    
    test_file = r"d:\Projects\Python\ConverterAI\test_comprehensive.html"
    pdf_output = r"d:\Projects\Python\ConverterAI\outputs\test_html_pdf_fix.pdf"
    
    print("=" * 60)
    print("🔧 HTML→PDF Hata Düzeltme Testi")
    print("=" * 60)
    print()
    
    print("Test: HTML → PDF (Link ve Anchor Temizleme)")
    print("-" * 60)
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='pdf',
            output_file=pdf_output
        )
        
        if result.success:
            print(f"✅ BAŞARILI: {pdf_output}")
            print(f"   Input:  {result.input_file}")
            print(f"   Format: {result.input_format} → {result.output_format}")
            if result.warnings:
                print(f"   Uyarılar: {len(result.warnings)}")
                for warning in result.warnings[:3]:
                    print(f"     - {warning}")
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
