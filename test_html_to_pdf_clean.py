"""
Test HTML to PDF conversion with style/script tag removal
"""
from converters.universal import UniversalConverter
from pathlib import Path

def test_html_to_pdf_clean():
    """Test that style and script tags are removed from PDF output"""
    
    print("="*60)
    print("🧪 HTML→PDF Style/Script Removal Test")
    print("="*60)
    print()
    
    converter = UniversalConverter()
    
    # Test with test_comprehensive.html which has lots of style tags
    input_file = Path("test_comprehensive.html")
    
    if not input_file.exists():
        print("❌ Test file not found: test_comprehensive.html")
        return
    
    print(f"📄 Input: {input_file}")
    print(f"   Size: {input_file.stat().st_size:,} bytes")
    print()
    
    # Convert to PDF
    print("🔄 Converting HTML → PDF...")
    result = converter.convert(
        input_file=str(input_file),
        input_format='html',
        output_format='pdf'
    )
    
    if result and result.success:
        output_path = Path(result.output_file)
        print(f"✅ Conversion successful!")
        print(f"   Output: {output_path.name}")
        print(f"   Size: {output_path.stat().st_size:,} bytes")
        print()
        
        # Now convert PDF back to text to check content
        print("🔍 Checking PDF content...")
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(str(output_path))
            
            # Get first page text
            first_page_text = doc[0].get_text()
            
            # Check for CSS/style content that shouldn't be there
            bad_patterns = [
                'font-family:',
                'font-size:',
                'background-color:',
                'padding:',
                'margin:',
                '/* Professional Document',
                'ConvertAI uses',
                '.table-bordered',
                'border-collapse:',
                '<style>',
                '</style>'
            ]
            
            issues_found = []
            for pattern in bad_patterns:
                if pattern.lower() in first_page_text.lower():
                    issues_found.append(pattern)
            
            if issues_found:
                print("❌ FAILED: Style/CSS content found in PDF!")
                print(f"   Found {len(issues_found)} problematic patterns:")
                for issue in issues_found[:5]:
                    print(f"      • {issue}")
                print()
                print("First 500 chars of PDF text:")
                print("-" * 60)
                print(first_page_text[:500])
                print("-" * 60)
            else:
                print("✅ SUCCESS: No style/CSS content in PDF!")
                print("   PDF contains clean text only")
                print()
                print("First 300 chars of PDF text:")
                print("-" * 60)
                print(first_page_text[:300])
                print("-" * 60)
            
            doc.close()
            
        except Exception as e:
            print(f"⚠️  Could not check PDF content: {e}")
    
    else:
        print("❌ Conversion failed")
    
    print()
    print("="*60)

if __name__ == '__main__':
    test_html_to_pdf_clean()
