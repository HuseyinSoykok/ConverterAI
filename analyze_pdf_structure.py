"""Quick script to analyze PDF text structure"""
import fitz

doc = fitz.open('2D_Poisson_FEM.pdf')
page = doc[2]  # Page 3 - mathematical content

# Get raw text blocks
blocks = page.get_text('dict')['blocks']
print("=== PDF Text Structure Analysis ===\n")

for block_idx, block in enumerate(blocks[:3]):
    if block.get('type') == 0:
        print(f"Block {block_idx}:")
        for line in block.get('lines', [])[:5]:
            spans_text = []
            for span in line.get('spans', []):
                text = span.get('text', '')
                font = span.get('font', '')
                size = span.get('size', 0)
                spans_text.append(f'"{text}"')
                print(f'  Span: "{text}" | Font: {font} | Size: {size:.1f}')
            print(f'  --> Combined: {" ".join(spans_text)}')
            print('  ---')
        print()

doc.close()
