#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for new formatting features"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converters.universal import UniversalConverter

def main():
    """Test all formatting enhancements"""
    
    converter = UniversalConverter()
    
    # Test file paths
    test_file = r"d:\Projects\Python\ConverterAI\test_formatting.md"
    pdf_output = r"d:\Projects\Python\ConverterAI\outputs\test_formatting.pdf"
    docx_output = r"d:\Projects\Python\ConverterAI\outputs\test_formatting.docx"
    
    print("=" * 60)
    print("🎨 FORMAT DESTEĞI TEST")
    print("=" * 60)
    print()
    
    # Test 1: MD → PDF
    print("Test 1: Markdown → PDF")
    print("-" * 60)
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='pdf',
            output_file=pdf_output
        )
        
        if result.success:
            print(f"✅ SUCCESS: {pdf_output}")
            print(f"   Input:  {result.input_file}")
            print(f"   Format: {result.input_format} → {result.output_format}")
        else:
            print(f"❌ FAILED: {result.error}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 2: MD → DOCX
    print("Test 2: Markdown → DOCX")
    print("-" * 60)
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='docx',
            output_file=docx_output
        )
        
        if result.success:
            print(f"✅ SUCCESS: {docx_output}")
            print(f"   Input:  {result.input_file}")
            print(f"   Format: {result.input_format} → {result.output_format}")
        else:
            print(f"❌ FAILED: {result.error}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    print("=" * 60)
    print("Test tamamlandı!")
    print("=" * 60)
    print()
    print("📂 Output dosyalarını kontrol edin:")
    print(f"   1. {pdf_output}")
    print(f"   2. {docx_output}")
    print()
    print("Beklenen özellikler:")
    print("   ✅ Strikethrough (~~text~~)")
    print("   ✅ Underline (<u>text</u>)")
    print("   ✅ Superscript (<sup>2</sup>)")
    print("   ✅ Subscript (<sub>2</sub>)")
    print("   ✅ Bold + Italic kombinasyonları")
    print()

if __name__ == "__main__":
    main()
