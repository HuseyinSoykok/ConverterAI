"""
Compare text extraction vs OCR results
"""
import os

def compare_results():
    print("=" * 60)
    print("COMPARISON: Text Extraction vs OCR")
    print("=" * 60)
    
    # File sizes
    files = [
        ('test_outputs/2D_Poisson_FEM_test.md', 'Text Extraction - Markdown'),
        ('test_outputs/2D_Poisson_FEM_ocr.md', 'OCR - Markdown'),
        ('test_outputs/2D_Poisson_FEM_test.html', 'Text Extraction - HTML'),
        ('test_outputs/2D_Poisson_FEM_ocr.html', 'OCR - HTML'),
    ]
    
    print("\n📁 File Sizes:")
    for filepath, label in files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"  {label}: {size:,} bytes, {len(content):,} chars")
    
    # Read and compare Page 3 content
    print("\n" + "=" * 60)
    print("📝 Page 3 Comparison (Strong Formulation of Poisson Equation)")
    print("=" * 60)
    
    # Text extraction version
    try:
        with open('test_outputs/2D_Poisson_FEM_test.md', 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        print("\n🔴 TEXT EXTRACTION (first 500 chars of page content):")
        # Try to find relevant section
        start = text_content.find("Strong")
        if start > 0:
            sample = text_content[start:start+500]
            print(sample)
        else:
            print(text_content[:500])
    except Exception as e:
        print(f"Error reading text extraction: {e}")
    
    # OCR version
    try:
        with open('test_outputs/2D_Poisson_FEM_ocr.md', 'r', encoding='utf-8') as f:
            ocr_content = f.read()
        
        print("\n🟢 OCR (first 500 chars of page content):")
        start = ocr_content.find("Strong Formulation")
        if start > 0:
            sample = ocr_content[start:start+500]
            print(sample)
        else:
            print(ocr_content[:500])
    except Exception as e:
        print(f"Error reading OCR: {e}")
    
    # Word count comparison
    print("\n" + "=" * 60)
    print("📊 Quality Metrics")
    print("=" * 60)
    
    try:
        with open('test_outputs/2D_Poisson_FEM_test.md', 'r', encoding='utf-8') as f:
            text_content = f.read()
        with open('test_outputs/2D_Poisson_FEM_ocr.md', 'r', encoding='utf-8') as f:
            ocr_content = f.read()
        
        # Count words
        text_words = len(text_content.split())
        ocr_words = len(ocr_content.split())
        
        # Count sentences (rough)
        text_sentences = text_content.count('. ')
        ocr_sentences = ocr_content.count('. ')
        
        # Check for long concatenated words (extraction error indicator)
        text_long_words = len([w for w in text_content.split() if len(w) > 25])
        ocr_long_words = len([w for w in ocr_content.split() if len(w) > 25])
        
        print(f"\n  Metric                  | Text Extraction | OCR")
        print(f"  ------------------------|-----------------|--------")
        print(f"  Total Characters        | {len(text_content):>15,} | {len(ocr_content):>6,}")
        print(f"  Word Count              | {text_words:>15,} | {ocr_words:>6,}")
        print(f"  Sentence Count (approx) | {text_sentences:>15,} | {ocr_sentences:>6,}")
        print(f"  Long Words (>25 chars)  | {text_long_words:>15,} | {ocr_long_words:>6,}")
        
        print("\n  ⚠️  High 'Long Words' count indicates concatenation errors")
        
        if text_long_words > ocr_long_words + 5:
            print("\n  ✅ OCR produces cleaner text with fewer concatenation issues!")
        
    except Exception as e:
        print(f"Error in comparison: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATION")
    print("=" * 60)
    print("""
    For LaTeX/Beamer presentation PDFs like this one:
    
    ✅ USE OCR MODE: converter.convert('file.pdf', 'output.md', use_ocr=True)
    
    OCR produces readable, properly-spaced text while direct text
    extraction often results in concatenated words due to the way
    LaTeX embeds individual character glyphs.
    
    OCR mode works for all formats: .md, .html, .docx
    """)

if __name__ == '__main__':
    compare_results()
