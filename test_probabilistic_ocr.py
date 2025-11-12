"""
Test script for probabilistic model image OCR with math formulas
"""
from converters.image_converter import ImageConverter
import os

def test_probabilistic_model():
    print("=" * 80)
    print("📊 PROBABILISTIC MODEL OCR TEST")
    print("=" * 80)
    
    # Image path
    image_path = r"uploads\57701e1b89f7499f8dc489ef1b0281ad_Screenshot_2025-11-12_131115.png"
    output_path = "test_probabilistic_model.md"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"\n📁 Input: {image_path}")
    print(f"📁 Output: {output_path}")
    
    # Initialize converter
    converter = ImageConverter()
    
    # Convert with math detection
    print("\n🔄 Converting with math detection enabled...")
    result = converter.convert(
        image_path,
        output_path,
        detect_tables=True,
        detect_math=True
    )
    
    # Print results
    print("\n" + "=" * 80)
    print("📊 CONVERSION RESULTS")
    print("=" * 80)
    
    metadata = result.metadata if hasattr(result, 'metadata') else {}
    layout_info = metadata.get('layout_info', {})
    content_analysis = metadata.get('content_analysis', {})
    
    print(f"\n📏 Image Size: {layout_info.get('image_width', 0)}x{layout_info.get('image_height', 0)}px")
    print(f"📊 Tables Detected: {len(layout_info.get('detected_structures', {}).get('tables', []))}")
    print(f"🔢 Math Formulas: {len(content_analysis.get('math_blocks', []))}")
    print(f"📈 OCR Confidence: {metadata.get('ocr_confidence', 0):.1f}%")
    print(f"⏱️ Processing Time: {metadata.get('processing_time', 0):.2f}s")
    
    # Show detected math formulas
    math_blocks = content_analysis.get('math_blocks', [])
    if math_blocks:
        print("\n" + "=" * 80)
        print("🔢 DETECTED MATHEMATICAL FORMULAS")
        print("=" * 80)
        
        for i, block in enumerate(math_blocks, 1):
            print(f"\n{i}. Line {block.get('line', 0)}:")
            print(f"   Original: {block.get('text', '')}")
            print(f"   LaTeX: {block.get('latex', '')}")
            print(f"   Type: {block.get('type', 'unknown')}")
            print(f"   Inline: {block.get('inline', False)}")
    
    # Read and display output
    print("\n" + "=" * 80)
    print("📄 OUTPUT PREVIEW (First 50 lines)")
    print("=" * 80)
    
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:50], 1):
                print(f"{i:3d}: {line.rstrip()}")
    
    print("\n" + "=" * 80)
    print("✅ Test completed!")
    print("=" * 80)
    
    return result

if __name__ == '__main__':
    test_probabilistic_model()
