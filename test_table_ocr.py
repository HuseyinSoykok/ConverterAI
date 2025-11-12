"""
Table OCR Test - Tablo tanıma testi
Tests table structure detection and conversion
"""
from PIL import Image, ImageDraw, ImageFont
from converters.image_converter import ImageConverter
import time

def create_table_test_image():
    """Create test image with tables"""
    width, height = 1200, 900
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 42)
        font_header = ImageFont.truetype("arialbd.ttf", 28)  # Bold
        font_cell = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_cell = ImageFont.load_default()
    
    y = 40
    
    # Title
    draw.text((50, y), "TABLO TANIMA TESTİ", fill='black', font=font_title)
    y += 80
    
    # Table 1: Simple student grades table
    draw.text((50, y), "Tablo 1: Öğrenci Notları", fill='darkblue', font=font_header)
    y += 50
    
    # Draw table borders
    table_x = 50
    table_y = y
    col_widths = [200, 120, 120, 120]
    row_height = 45
    
    # Headers
    headers = ["Öğrenci Adı", "Matematik", "Türkçe", "Ortalama"]
    
    # Data
    data = [
        ["Ahmet Yılmaz", "85", "90", "87.5"],
        ["Ayşe Demir", "92", "88", "90.0"],
        ["Mehmet Öz", "78", "82", "80.0"],
        ["Zeynep Kaya", "95", "94", "94.5"]
    ]
    
    # Draw table grid
    total_width = sum(col_widths)
    total_height = (len(data) + 1) * row_height
    
    # Outer border
    draw.rectangle([table_x, table_y, table_x + total_width, table_y + total_height], 
                   outline='black', width=3)
    
    # Horizontal lines
    for i in range(len(data) + 2):
        y_line = table_y + i * row_height
        draw.line([table_x, y_line, table_x + total_width, y_line], 
                  fill='black', width=2)
    
    # Vertical lines
    x_pos = table_x
    for width in col_widths:
        draw.line([x_pos, table_y, x_pos, table_y + total_height], 
                  fill='black', width=2)
        x_pos += width
    draw.line([x_pos, table_y, x_pos, table_y + total_height], 
              fill='black', width=2)
    
    # Fill headers
    x_pos = table_x
    for i, header in enumerate(headers):
        text_x = x_pos + 10
        text_y = table_y + 10
        draw.text((text_x, text_y), header, fill='black', font=font_header)
        x_pos += col_widths[i]
    
    # Fill data
    for row_idx, row in enumerate(data):
        x_pos = table_x
        for col_idx, cell in enumerate(row):
            text_x = x_pos + 10
            text_y = table_y + (row_idx + 1) * row_height + 10
            draw.text((text_x, text_y), cell, fill='black', font=font_cell)
            x_pos += col_widths[col_idx]
    
    y = table_y + total_height + 60
    
    # Table 2: Product price table
    draw.text((50, y), "Tablo 2: Ürün Fiyatları", fill='darkblue', font=font_header)
    y += 50
    
    # Simple table with lines
    table2_data = [
        ["Ürün", "Fiyat", "Stok"],
        ["Kalem", "5 TL", "150"],
        ["Defter", "12 TL", "80"],
        ["Silgi", "3 TL", "200"]
    ]
    
    table2_x = 50
    table2_y = y
    col2_widths = [250, 150, 150]
    
    # Draw simple table
    total2_width = sum(col2_widths)
    total2_height = len(table2_data) * row_height
    
    draw.rectangle([table2_x, table2_y, table2_x + total2_width, table2_y + total2_height],
                   outline='black', width=3)
    
    # Horizontal lines
    for i in range(len(table2_data) + 1):
        y_line = table2_y + i * row_height
        draw.line([table2_x, y_line, table2_x + total2_width, y_line],
                  fill='black', width=2)
    
    # Vertical lines
    x_pos = table2_x
    for width in col2_widths:
        draw.line([x_pos, table2_y, x_pos, table2_y + total2_height],
                  fill='black', width=2)
        x_pos += width
    draw.line([x_pos, table2_y, x_pos, table2_y + total2_height],
              fill='black', width=2)
    
    # Fill table 2
    for row_idx, row in enumerate(table2_data):
        x_pos = table2_x
        font_used = font_header if row_idx == 0 else font_cell
        for col_idx, cell in enumerate(row):
            text_x = x_pos + 10
            text_y = table2_y + row_idx * row_height + 10
            draw.text((text_x, text_y), cell, fill='black', font=font_used)
            x_pos += col2_widths[col_idx]
    
    # Save
    filename = 'test_table.png'
    image.save(filename)
    print(f"✅ Created {filename}")
    return filename

def test_table_ocr():
    """Test table OCR"""
    print("=" * 70)
    print("  TABLO OCR TESTİ - Table Recognition")
    print("=" * 70)
    print()
    
    print("📊 Tablo içeren test görseli oluşturuluyor...")
    image_file = create_table_test_image()
    print()
    
    converter = ImageConverter()
    
    print("=" * 50)
    print("TEST: Tablo Görseli → Markdown")
    print("=" * 50)
    
    start = time.time()
    result = converter.convert(image_file, 'test_table.md')
    elapsed = time.time() - start
    
    if result.success:
        print(f"✅ SUCCESS: test_table.md")
        print(f"   Dönüşüm süresi: {elapsed:.2f}s")
        if hasattr(result, 'metadata') and result.metadata:
            if 'ocr_confidence' in result.metadata:
                print(f"   OCR Güven: {result.metadata['ocr_confidence']:.1f}%")
        
        print()
        print("=" * 70)
        print("📄 MARKDOWN ÇIKTISI")
        print("=" * 70)
        print()
        
        with open('test_table.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        
        print()
        print("=" * 70)
        print("🔍 TABLO TANIMA ANALİZİ")
        print("=" * 70)
        print()
        
        # Check if tables were detected
        if '|' in content or 'Öğrenci' in content:
            print("✅ Tablo içeriği tespit edildi")
            
            # Count potential table markers
            pipe_count = content.count('|')
            if pipe_count > 0:
                print(f"   Markdown tablo formatı: {pipe_count} pipe (|) karakteri")
            
            # Check for student names
            students = ['Ahmet', 'Ayşe', 'Mehmet', 'Zeynep']
            found_students = [s for s in students if s in content]
            print(f"   Öğrenci adları: {len(found_students)}/{len(students)} bulundu")
            
            # Check for numbers
            if any(str(i) in content for i in range(70, 100)):
                print(f"   ✅ Notlar tanındı (70-100 arası sayılar)")
            
            # Check for products
            products = ['Kalem', 'Defter', 'Silgi']
            found_products = [p for p in products if p in content]
            print(f"   Ürünler: {len(found_products)}/{len(products)} bulundu")
        else:
            print("⚠️ Tablo yapısı tam olarak korunamadı")
            print("   (Ancak metin içeriği çıkarıldı)")
        
        print()
        print("💡 NOT: Temel tablo algılama mevcut.")
        print("   Gelişmiş tablo yapısı için OpenCV entegrasyonu planlanıyor.")
    else:
        print(f"❌ FAILED: {result.error}")
    
    print()
    print("=" * 70)
    print("  TEST TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    test_table_ocr()
