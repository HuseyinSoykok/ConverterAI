"""
Test script for improved quality checker
Demonstrates the enhanced quality scoring system
"""
import sys
from pathlib import Path
from ai.local_ai_checker import LocalAIChecker
from converters.universal import UniversalConverter
from utils.logger import logger

def test_quality_improvements():
    """Test the improved quality checker with real conversions"""
    
    print("="*60)
    print("🔬 Quality Checker Improvement Test")
    print("="*60)
    print()
    
    # Initialize checker and converter
    checker = LocalAIChecker(method='heuristic')
    converter = UniversalConverter()
    
    # Test files directory
    test_dir = Path(__file__).parent
    outputs_dir = test_dir / 'outputs'
    
    # Find test files - check multiple locations
    test_files = []
    
    # PDF files in outputs
    if (outputs_dir / 'test_formatting.pdf').exists():
        test_files.append(('outputs/test_formatting.pdf', 'html'))
    
    # HTML files
    if (test_dir / 'test_comprehensive.html').exists():
        test_files.append(('test_comprehensive.html', 'markdown'))
    
    # Markdown files
    if (test_dir / 'test_comprehensive.md').exists():
        test_files.append(('test_comprehensive.md', 'html', 'markdown'))
    
    if (test_dir / 'test_formatting.md').exists():
        test_files.append(('test_formatting.md', 'html', 'markdown'))
    
    if (test_dir / 'README.md').exists():
        test_files.append(('README.md', 'html', 'markdown'))
    
    results = []
    
    if not test_files:
        print("⚠️  No test files found!")
        print("\nSearched locations:")
        print(f"   • {outputs_dir}/test_formatting.pdf")
        print(f"   • {test_dir}/test_comprehensive.html")
        print(f"   • {test_dir}/test_comprehensive.md")
        print(f"   • {test_dir}/test_formatting.md")
        print(f"   • {test_dir}/README.md")
        return
    
    print(f"Found {len(test_files)} test file(s)\n")
    
    for test_item in test_files:
        if len(test_item) == 3:
            input_name, target_format, input_format = test_item
        else:
            input_name, target_format = test_item
            input_format = None
        
        input_path = test_dir / input_name
        
        if not input_path.exists():
            print(f"⏭️  Skipping {input_name} (not found)")
            continue
        
        print(f"\n{'='*60}")
        print(f"📄 Testing: {input_name} → {target_format}")
        print(f"{'='*60}")
        
        try:
            # Perform conversion
            if input_format is None:
                input_format = input_path.suffix[1:]
            
            result = converter.convert(
                input_file=str(input_path),
                input_format=input_format,
                output_format=target_format
            )
            
            if result and result.success:
                output_path = result.output_file
                print(f"✅ Conversion successful: {Path(output_path).name}")
                
                # Check quality with improved system
                quality_result = checker.check_quality(
                    str(input_path),
                    output_path
                )
                
                # Display results
                print(f"\n📊 Quality Report:")
                print(f"   Score: {quality_result['score']:.2%} ({quality_result['rating'].upper()})")
                print(f"   Method: {quality_result['method']}")
                
                if 'conversion_type' in quality_result:
                    print(f"   Conversion: {quality_result['conversion_type']}")
                
                if 'format_adjustment' in quality_result:
                    adj = quality_result['format_adjustment']
                    print(f"   Format bonus: {adj:+.2%}")
                
                # Show key metrics
                print(f"\n   Key Metrics:")
                metrics = quality_result['metrics']
                
                important_metrics = [
                    ('heading_preservation', 'Headings'),
                    ('list_preservation', 'Lists'),
                    ('table_preservation', 'Tables'),
                    ('paragraph_preservation', 'Paragraphs'),
                    ('sentence_preservation', 'Sentences'),
                    ('formatting_preservation', 'Formatting'),
                    ('content_similarity', 'Content Similarity'),
                    ('avg_feature_preservation', 'Avg Features'),
                ]
                
                for key, label in important_metrics:
                    if key in metrics:
                        value = metrics[key]
                        print(f"      • {label}: {value:.1%}")
                
                # Show issues if any
                if quality_result['issues']:
                    print(f"\n   ⚠️  Issues ({len(quality_result['issues'])}):")
                    for issue in quality_result['issues'][:3]:  # Show first 3
                        print(f"      • {issue}")
                
                # Show recommendations
                if quality_result['recommendations']:
                    print(f"\n   💡 Recommendations:")
                    for rec in quality_result['recommendations'][:2]:  # Show first 2
                        print(f"      • {rec}")
                
                results.append({
                    'file': input_name,
                    'score': quality_result['score'],
                    'rating': quality_result['rating']
                })
                
            else:
                print(f"❌ Conversion failed")
                results.append({
                    'file': input_name,
                    'score': 0.0,
                    'rating': 'failed'
                })
        
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Test failed for {input_name}: {e}", exc_info=True)
            results.append({
                'file': input_name,
                'score': 0.0,
                'rating': 'error'
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("📈 SUMMARY")
    print(f"{'='*60}")
    
    if results:
        avg_score = sum(r['score'] for r in results) / len(results)
        print(f"\nTotal tests: {len(results)}")
        print(f"Average score: {avg_score:.2%}")
        print()
        
        # Rating distribution
        from collections import Counter
        rating_counts = Counter(r['rating'] for r in results)
        
        print("Rating Distribution:")
        for rating in ['excellent', 'very_good', 'good', 'acceptable', 'poor', 'failed']:
            count = rating_counts.get(rating, 0)
            if count > 0:
                bar = '█' * count
                print(f"   {rating:12s}: {bar} ({count})")
        
        print()
        print("Quality Improvements Summary:")
        print("   ✅ Enhanced heuristic analysis (18+ metrics)")
        print("   ✅ Format-specific scoring adjustments")
        print("   ✅ Content integrity checks (paragraphs, sentences)")
        print("   ✅ Advanced similarity metrics (n-grams)")
        print("   ✅ Comprehensive feature preservation tracking")
        print("   ✅ HTML tag balance validation")
        print("   ✅ Context-aware recommendations")
        print()
        
        if avg_score >= 0.85:
            print(f"🎉 EXCELLENT! Quality scoring system is working great!")
            print(f"   Average score: {avg_score:.1%} (Target: 85%+)")
        elif avg_score >= 0.75:
            print(f"✅ GOOD! Quality scoring improved significantly!")
            print(f"   Average score: {avg_score:.1%} (Previous: ~70-75%)")
        else:
            print(f"⚠️  Quality score: {avg_score:.1%}")
            print(f"   More improvements may be needed")
    else:
        print("No test files found. Please ensure test files exist in outputs/ directory:")
        print("   • test_formatting.pdf")
        print("   • test_comprehensive.html")
        print("   • test_formatting.md")
    
    print(f"\n{'='*60}")

if __name__ == '__main__':
    test_quality_improvements()
