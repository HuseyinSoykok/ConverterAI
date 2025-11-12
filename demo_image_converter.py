"""
Simple image converter demo without OCR dependency
Creates a markdown file from scratch to demonstrate the pipeline
"""
from converters import UniversalConverter
from PIL import Image, ImageDraw, ImageFont
import os


def create_demo_text_content():
    """Create demo markdown content (simulating OCR output)"""
    return """# TEST DOCUMENT

## Image to Document Conversion Test

This is a test image for the VCR-01 system.
It contains multiple paragraphs with standard text.

The system should be able to:
- Extract all text accurately
- Detect heading structures
- Preserve paragraph formatting
- Handle multi-line content

### Code Example

```python
def hello_world():
    print("Hello from ConverterAI!")
    return True
```

### Table Example

| Feature | Status | Priority |
|---------|--------|----------|
| OCR | Active | High |
| Tables | Active | Medium |
| Math | Beta | High |

## Conclusion

The image conversion system is now operational with basic features.
Advanced features like LaTeX math recognition are in development.
"""


def demo_without_ocr():
    """Demonstrate the conversion pipeline without OCR"""
    print("=" * 70)
    print("  IMAGE CONVERTER DEMO (Without OCR)")
    print("=" * 70)
    print("\n⚠️  Tesseract OCR is not installed.")
    print("📝  Demonstrating the pipeline with sample content...\n")
    
    # Create sample markdown content
    demo_md = "demo_content.md"
    with open(demo_md, 'w', encoding='utf-8') as f:
        f.write(create_demo_text_content())
    
    print("✅ Created sample markdown file")
    
    converter = UniversalConverter()
    
    # Test 1: Markdown → PDF
    print("\n" + "="*70)
    print("TEST 1: Markdown → PDF")
    print("="*70)
    result = converter.convert(
        input_file=demo_md,
        input_format='markdown',
        output_format='pdf'
    )
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        print(f"   Size: {os.path.getsize(result.output_file) / 1024:.1f} KB")
    else:
        print(f"❌ FAILED: {result.error}")
    
    # Test 2: Markdown → DOCX
    print("\n" + "="*70)
    print("TEST 2: Markdown → DOCX")
    print("="*70)
    result = converter.convert(
        input_file=demo_md,
        input_format='markdown',
        output_format='docx'
    )
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        print(f"   Size: {os.path.getsize(result.output_file) / 1024:.1f} KB")
    else:
        print(f"❌ FAILED: {result.error}")
    
    # Test 3: Markdown → HTML
    print("\n" + "="*70)
    print("TEST 3: Markdown → HTML")
    print("="*70)
    result = converter.convert(
        input_file=demo_md,
        input_format='markdown',
        output_format='html'
    )
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        print(f"   Size: {os.path.getsize(result.output_file) / 1024:.1f} KB")
        
        # Preview HTML
        with open(result.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n📄 HTML Preview (first 400 chars):")
        print("-" * 70)
        print(content[:400])
        print("-" * 70)
    else:
        print(f"❌ FAILED: {result.error}")
    
    print("\n" + "="*70)
    print("  DEMO COMPLETED!")
    print("="*70)
    print("\n📚 Next Steps:")
    print("1. Install Tesseract OCR for real image conversion:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. Install Turkish language pack for OCR")
    print("3. Run test_image_converter.py with real images")
    print("\n💡 See IMAGE_CONVERSION_GUIDE.md for detailed instructions")


if __name__ == '__main__':
    try:
        demo_without_ocr()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
