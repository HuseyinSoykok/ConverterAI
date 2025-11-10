"""
Example usage scripts for ConverterAI
"""
from converters import UniversalConverter
from pathlib import Path


def example_1_simple_conversion():
    """Example 1: Simple PDF to DOCX conversion"""
    print("Example 1: Simple PDF to DOCX conversion")
    print("-" * 50)
    
    converter = UniversalConverter()
    
    result = converter.convert(
        input_file="example.pdf",
        output_format="docx"
    )
    
    if result.success:
        print(f"✅ Success! Output: {result.output_file}")
        print(f"⏱️  Processing time: {result.processing_time:.2f}s")
    else:
        print(f"❌ Failed: {result.error}")


def example_2_with_quality_check():
    """Example 2: Conversion with AI quality check"""
    print("\nExample 2: Conversion with AI quality check")
    print("-" * 50)
    
    converter = UniversalConverter()
    
    result = converter.convert(
        input_file="document.pdf",
        output_format="html",
        quality_check=True
    )
    
    if result.success:
        print(f"✅ Success! Output: {result.output_file}")
        print(f"⭐ Quality score: {result.quality_score * 100:.1f}%")
        
        if result.warnings:
            print("⚠️  Warnings:")
            for warning in result.warnings:
                print(f"  - {warning}")


def example_3_batch_conversion():
    """Example 3: Batch conversion"""
    print("\nExample 3: Batch conversion")
    print("-" * 50)
    
    converter = UniversalConverter()
    
    files = [
        "doc1.pdf",
        "doc2.pdf",
        "doc3.pdf"
    ]
    
    results = converter.batch_convert(
        input_files=files,
        output_format="markdown",
        output_dir="./converted"
    )
    
    success_count = sum(1 for r in results if r.success)
    print(f"📊 Converted {success_count}/{len(files)} files successfully")
    
    for result in results:
        if result.success:
            print(f"  ✅ {Path(result.input_file).name}")
        else:
            print(f"  ❌ {Path(result.input_file).name}: {result.error}")


def example_4_specify_output():
    """Example 4: Specify custom output path"""
    print("\nExample 4: Custom output path")
    print("-" * 50)
    
    converter = UniversalConverter()
    
    result = converter.convert(
        input_file="input.md",
        output_format="pdf",
        output_file="./outputs/custom_name.pdf"
    )
    
    if result.success:
        print(f"✅ Saved to: {result.output_file}")


def example_5_markdown_to_all():
    """Example 5: Convert Markdown to all formats"""
    print("\nExample 5: Markdown to all formats")
    print("-" * 50)
    
    converter = UniversalConverter()
    input_file = "README.md"
    
    formats = ['pdf', 'docx', 'html']
    
    for format_name in formats:
        result = converter.convert(
            input_file=input_file,
            output_format=format_name
        )
        
        if result.success:
            print(f"✅ {format_name.upper()}: {result.output_file}")
        else:
            print(f"❌ {format_name.upper()}: {result.error}")


def example_6_error_handling():
    """Example 6: Proper error handling"""
    print("\nExample 6: Error handling")
    print("-" * 50)
    
    converter = UniversalConverter()
    
    try:
        result = converter.convert(
            input_file="nonexistent.pdf",
            output_format="docx"
        )
        
        if not result.success:
            print(f"❌ Conversion failed: {result.error}")
            
            # Handle specific errors
            if "not found" in result.error.lower():
                print("💡 Tip: Check if the file path is correct")
            elif "unsupported" in result.error.lower():
                print("💡 Tip: Check supported formats with converter.get_supported_conversions()")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def example_7_supported_conversions():
    """Example 7: Check supported conversions"""
    print("\nExample 7: Supported conversions")
    print("-" * 50)
    
    converter = UniversalConverter()
    conversions = converter.get_supported_conversions()
    
    for input_format, output_formats in conversions.items():
        print(f"\n{input_format.upper()} can be converted to:")
        for output_format in output_formats:
            print(f"  → {output_format.upper()}")


if __name__ == '__main__':
    print("=" * 50)
    print("ConverterAI Usage Examples")
    print("=" * 50)
    
    # Uncomment the examples you want to run
    
    # example_1_simple_conversion()
    # example_2_with_quality_check()
    # example_3_batch_conversion()
    # example_4_specify_output()
    # example_5_markdown_to_all()
    # example_6_error_handling()
    example_7_supported_conversions()
