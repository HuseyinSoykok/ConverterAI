"""
Test OCR-based PDF conversion
"""
from converters.pdf_converter import PDFConverter

def test_ocr_conversion():
    converter = PDFConverter()
    
    # First, detect if OCR is recommended
    detection = converter.detect_if_ocr_needed('2D_Poisson_FEM.pdf')
    print('=== OCR Detection ===')
    print(f"Recommended: {detection['recommended']}")
    print(f"Reason: {detection['reason']}")
    print(f"Confidence: {detection['confidence']}")
    print()
    
    # Convert with OCR to Markdown
    print('=== Converting to Markdown (OCR mode) ===')
    result = converter.convert('2D_Poisson_FEM.pdf', 'test_outputs/2D_Poisson_FEM_ocr.md', use_ocr=True)
    print(f'Success: {result.success}')
    print(f'Warnings: {len(result.warnings)} warnings')
    if result.warnings:
        for w in result.warnings[:5]:
            print(f'  - {w}')
    if result.metadata:
        print(f'Pages: {result.metadata.get("pages", "N/A")}')
        print(f'Method: {result.metadata.get("method", "N/A")}')
    
    # Show sample output
    print('\n=== Sample OCR Output (first 2000 chars) ===')
    try:
        with open('test_outputs/2D_Poisson_FEM_ocr.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:2000])
            print(f'\n... Total length: {len(content)} characters')
    except Exception as e:
        print(f'Could not read output: {e}')
    
    print('\n' + '='*60)
    
    # Also convert to HTML with OCR
    print('\n=== Converting to HTML (OCR mode) ===')
    result_html = converter.convert('2D_Poisson_FEM.pdf', 'test_outputs/2D_Poisson_FEM_ocr.html', use_ocr=True)
    print(f'Success: {result_html.success}')
    if result_html.metadata:
        print(f'Pages: {result_html.metadata.get("pages", "N/A")}')
        print(f'Method: {result_html.metadata.get("method", "N/A")}')
    
    # Convert to DOCX with OCR
    print('\n=== Converting to DOCX (OCR mode) ===')
    result_docx = converter.convert('2D_Poisson_FEM.pdf', 'test_outputs/2D_Poisson_FEM_ocr.docx', use_ocr=True)
    print(f'Success: {result_docx.success}')
    if result_docx.metadata:
        print(f'Pages: {result_docx.metadata.get("pages", "N/A")}')
        print(f'Method: {result_docx.metadata.get("method", "N/A")}')

if __name__ == '__main__':
    test_ocr_conversion()
