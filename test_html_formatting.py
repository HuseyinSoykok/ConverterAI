#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for HTML formatting features"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from converters.universal import UniversalConverter

def main():
    """Test HTML formatting enhancements"""
    
    converter = UniversalConverter()
    
    # Test file paths
    test_file = r"d:\Projects\Python\ConverterAI\test_formatting.html"
    pdf_output = r"d:\Projects\Python\ConverterAI\outputs\test_formatting_html.pdf"
    docx_output = r"d:\Projects\Python\ConverterAI\outputs\test_formatting_html.docx"
    md_output = r"d:\Projects\Python\ConverterAI\outputs\test_formatting_html.md"
    
    print("=" * 60)
    print("🎨 HTML FORMAT DESTEĞI TEST")
    print("=" * 60)
    print()
    
    # Test 1: HTML → PDF
    print("Test 1: HTML → PDF")
    print("-" * 60)
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='pdf',
            output_file=pdf_output
        )
        
        if result.success:
            print(f"✅ SUCCESS: {pdf_output}")
        else:
            print(f"❌ FAILED: {result.error}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 2: HTML → DOCX
    print("Test 2: HTML → DOCX")
    print("-" * 60)
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='docx',
            output_file=docx_output
        )
        
        if result.success:
            print(f"✅ SUCCESS: {docx_output}")
        else:
            print(f"❌ FAILED: {result.error}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 3: HTML → MD
    print("Test 3: HTML → Markdown")
    print("-" * 60)
    try:
        result = converter.convert(
            input_file=test_file,
            output_format='markdown',
            output_file=md_output
        )
        
        if result.success:
            print(f"✅ SUCCESS: {md_output}")
        else:
            print(f"❌ FAILED: {result.error}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    print("=" * 60)
    print("HTML Test tamamlandı!")
    print("=" * 60)
    print()
    print("📂 Output dosyalarını kontrol edin:")
    print(f"   1. {pdf_output}")
    print(f"   2. {docx_output}")
    print(f"   3. {md_output}")
    print()

if __name__ == "__main__":
    main()
