"""
Test script for Image to Document conversion
"""
from converters import UniversalConverter
from PIL import Image, ImageDraw, ImageFont
import os


def create_test_image():
    """Create a test PNG image with text content"""
    # Create image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_medium = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add text content
    y = 50
    
    # Title
    draw.text((50, y), "TEST DOCUMENT", fill='black', font=font_large)
    y += 60
    
    # Subtitle
    draw.text((50, y), "Image to Document Conversion Test", fill='black', font=font_medium)
    y += 50
    
    # Paragraph
    text_lines = [
        "This is a test image for the VCR-01 system.",
        "It contains multiple paragraphs with standard text.",
        "",
        "The system should be able to:",
        "- Extract all text accurately",
        "- Detect heading structures",
        "- Preserve paragraph formatting",
        "- Handle multi-line content"
    ]
    
    for line in text_lines:
        draw.text((50, y), line, fill='black', font=font_small)
        y += 25
    
    # Save image
    img.save('test_image_simple.png')
    print("✅ Created test_image_simple.png")
    return 'test_image_simple.png'


def test_image_to_markdown():
    """Test Image → Markdown conversion"""
    print("\n" + "="*50)
    print("TEST 1: Image → Markdown")
    print("="*50)
    
    # Create test image
    image_file = create_test_image()
    
    converter = UniversalConverter()
    result = converter.convert(
        input_file=image_file,
        input_format='image',
        output_format='markdown'
    )
    
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        print(f"   OCR Confidence: {result.metadata.get('ocr_confidence', 'N/A')}")
        print(f"   Words: {result.metadata.get('word_count', 'N/A')}")
        
        # Read and display output
        with open(result.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n📄 Output Preview (first 500 chars):")
        print("-" * 50)
        print(content[:500])
        print("-" * 50)
    else:
        print(f"❌ FAILED: {result.error}")


def test_image_to_pdf():
    """Test Image → PDF conversion"""
    print("\n" + "="*50)
    print("TEST 2: Image → PDF")
    print("="*50)
    
    # Use existing test image
    image_file = 'test_image_simple.png'
    
    if not os.path.exists(image_file):
        print("⚠️ Test image not found, creating...")
        image_file = create_test_image()
    
    converter = UniversalConverter()
    result = converter.convert(
        input_file=image_file,
        input_format='image',
        output_format='pdf'
    )
    
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        print(f"   Conversion time: {result.conversion_time:.2f}s")
        print(f"   File size: {os.path.getsize(result.output_file) / 1024:.1f} KB")
    else:
        print(f"❌ FAILED: {result.error}")


def test_image_to_docx():
    """Test Image → DOCX conversion"""
    print("\n" + "="*50)
    print("TEST 3: Image → DOCX")
    print("="*50)
    
    # Use existing test image
    image_file = 'test_image_simple.png'
    
    if not os.path.exists(image_file):
        print("⚠️ Test image not found, creating...")
        image_file = create_test_image()
    
    converter = UniversalConverter()
    result = converter.convert(
        input_file=image_file,
        input_format='image',
        output_format='docx'
    )
    
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        print(f"   Conversion time: {result.conversion_time:.2f}s")
    else:
        print(f"❌ FAILED: {result.error}")


def test_image_to_html():
    """Test Image → HTML conversion"""
    print("\n" + "="*50)
    print("TEST 4: Image → HTML")
    print("="*50)
    
    # Use existing test image
    image_file = 'test_image_simple.png'
    
    if not os.path.exists(image_file):
        print("⚠️ Test image not found, creating...")
        image_file = create_test_image()
    
    converter = UniversalConverter()
    result = converter.convert(
        input_file=image_file,
        input_format='image',
        output_format='html'
    )
    
    if result.success:
        print(f"✅ SUCCESS: {result.output_file}")
        
        # Read and display output
        with open(result.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n📄 Output Preview (first 300 chars):")
        print("-" * 50)
        print(content[:300])
        print("-" * 50)
    else:
        print(f"❌ FAILED: {result.error}")


if __name__ == '__main__':
    print("=" * 70)
    print("  IMAGE TO DOCUMENT CONVERSION TESTS (VCR-01)")
    print("=" * 70)
    
    try:
        # Run tests
        test_image_to_markdown()
        test_image_to_pdf()
        test_image_to_docx()
        test_image_to_html()
        
        print("\n" + "=" * 70)
        print("  ALL TESTS COMPLETED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
