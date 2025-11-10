"""
Comprehensive Conversion Testing Suite
Tests all conversion paths and identifies issues
"""

from converters import UniversalConverter
from pathlib import Path
import time

def test_conversion(converter, source, source_format, target_format, output_path):
    """Test a single conversion and return results"""
    result = {
        'source': source,
        'source_format': source_format,
        'target_format': target_format,
        'output': output_path,
        'success': False,
        'error': None,
        'duration': 0,
        'file_size': 0,
        'checks': {}
    }
    
    start = time.time()
    
    try:
        conv_result = converter.convert(source, source_format, target_format, output_path)
        result['duration'] = time.time() - start
        
        # Check if conversion was successful
        if conv_result.success and Path(conv_result.output_file).exists():
            result['success'] = True
            result['file_size'] = Path(conv_result.output_file).stat().st_size
            result['output'] = conv_result.output_file
            
            # Content checks based on target format
            if target_format == 'html':
                with open(result['output'], 'r', encoding='utf-8') as f:
                    content = f.read()
                result['checks'] = {
                    'has_headings': '<h1>' in content or '<h2>' in content,
                    'has_tables': '<table>' in content,
                    'has_code': '<pre>' in content or '<code>' in content,
                    'has_lists': '<ul>' in content or '<ol>' in content,
                    'has_formatting': '<strong>' in content or '<em>' in content,
                }
            elif target_format == 'markdown':
                with open(result['output'], 'r', encoding='utf-8') as f:
                    content = f.read()
                result['checks'] = {
                    'has_headings': content.count('#') > 0,
                    'has_tables': '|' in content and '---' in content,
                    'has_code': '```' in content or '`' in content,
                    'has_lists': content.count('- ') > 0 or content.count('* ') > 0,
                    'has_bold': '**' in content or '__' in content,
                }
            
    except Exception as e:
        result['error'] = str(e)
        result['duration'] = time.time() - start
    
    return result

def print_result(result, test_num):
    """Print formatted test result"""
    status = "PASS" if result['success'] else "FAIL"
    symbol = "[OK]" if result['success'] else "[X]"
    
    print(f"\nTest {test_num}: {result['source_format'].upper()} -> {result['target_format'].upper()}")
    print(f"  Status: {symbol} {status}")
    print(f"  Source: {Path(result['source']).name}")
    
    if result['success']:
        print(f"  Output: {Path(result['output']).name}")
        print(f"  Size: {result['file_size']:,} bytes")
        print(f"  Duration: {result['duration']:.2f}s")
        
        if result['checks']:
            print("  Content checks:")
            for check, passed in result['checks'].items():
                check_symbol = "[OK]" if passed else "[X]"
                print(f"    {check_symbol} {check.replace('_', ' ').title()}")
    else:
        print(f"  Error: {result['error']}")
    
    return result['success']

def main():
    print("=" * 70)
    print("COMPREHENSIVE CONVERSION TEST SUITE")
    print("=" * 70)
    
    converter = UniversalConverter()
    results = []
    test_num = 0
    
    # Ensure outputs directory exists
    Path('outputs').mkdir(exist_ok=True)
    
    # Test Suite 1: Markdown Conversions
    print("\n" + "=" * 70)
    print("SUITE 1: MARKDOWN CONVERSIONS")
    print("=" * 70)
    
    md_tests = [
        ('test_comprehensive.md', 'markdown', 'html', 'outputs/test_md_to_html.html'),
        ('test_comprehensive.md', 'markdown', 'pdf', 'outputs/test_md_to_pdf.pdf'),
        ('test_comprehensive.md', 'markdown', 'docx', 'outputs/test_md_to_docx.docx'),
    ]
    
    for source, src_fmt, tgt_fmt, output in md_tests:
        test_num += 1
        result = test_conversion(converter, source, src_fmt, tgt_fmt, output)
        results.append(result)
        print_result(result, test_num)
    
    # Test Suite 2: HTML Conversions
    print("\n" + "=" * 70)
    print("SUITE 2: HTML CONVERSIONS")
    print("=" * 70)
    
    html_tests = [
        ('test_comprehensive.html', 'html', 'markdown', 'outputs/test_html_to_md.md'),
        ('test_comprehensive.html', 'html', 'pdf', 'outputs/test_html_to_pdf.pdf'),
        ('test_comprehensive.html', 'html', 'docx', 'outputs/test_html_to_docx.docx'),
    ]
    
    for source, src_fmt, tgt_fmt, output in html_tests:
        test_num += 1
        result = test_conversion(converter, source, src_fmt, tgt_fmt, output)
        results.append(result)
        print_result(result, test_num)
    
    # Test Suite 3: DOCX Conversions
    print("\n" + "=" * 70)
    print("SUITE 3: DOCX CONVERSIONS")
    print("=" * 70)
    
    docx_tests = [
        ('test_comprehensive.docx', 'docx', 'markdown', 'outputs/test_docx_to_md.md'),
        ('test_comprehensive.docx', 'docx', 'html', 'outputs/test_docx_to_html.html'),
        ('test_comprehensive.docx', 'docx', 'pdf', 'outputs/test_docx_to_pdf.pdf'),
    ]
    
    for source, src_fmt, tgt_fmt, output in docx_tests:
        test_num += 1
        result = test_conversion(converter, source, src_fmt, tgt_fmt, output)
        results.append(result)
        print_result(result, test_num)
    
    # Test Suite 4: PDF Conversions
    print("\n" + "=" * 70)
    print("SUITE 4: PDF CONVERSIONS")
    print("=" * 70)
    
    pdf_tests = [
        ('test_comprehensive.pdf', 'pdf', 'markdown', 'outputs/test_pdf_to_md.md'),
        ('test_comprehensive.pdf', 'pdf', 'html', 'outputs/test_pdf_to_html.html'),
    ]
    
    for source, src_fmt, tgt_fmt, output in pdf_tests:
        test_num += 1
        result = test_conversion(converter, source, src_fmt, tgt_fmt, output)
        results.append(result)
        print_result(result, test_num)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results if r['success'])
    failed = len(results) - passed
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed} ([OK])")
    print(f"Failed: {failed} ([X])")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    # Failed tests detail
    if failed > 0:
        print("\n" + "=" * 70)
        print("FAILED TESTS - ISSUES TO FIX")
        print("=" * 70)
        for i, r in enumerate(results, 1):
            if not r['success']:
                print(f"\n{i}. {r['source_format'].upper()} -> {r['target_format'].upper()}")
                print(f"   Source: {Path(r['source']).name}")
                print(f"   Error: {r['error']}")
    
    # Content quality issues
    print("\n" + "=" * 70)
    print("CONTENT QUALITY ISSUES")
    print("=" * 70)
    
    for i, r in enumerate(results, 1):
        if r['success'] and r['checks']:
            failed_checks = [k for k, v in r['checks'].items() if not v]
            if failed_checks:
                print(f"\n{i}. {r['source_format'].upper()} -> {r['target_format'].upper()}")
                print(f"   Output: {Path(r['output']).name}")
                print(f"   Missing elements:")
                for check in failed_checks:
                    print(f"     - {check.replace('_', ' ').title()}")
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    main()
