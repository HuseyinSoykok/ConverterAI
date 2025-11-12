# 📸 Görsel Dönüştürme Rehberi (VCR-01)

## 🎯 Özellikler

ConverterAI artık **PNG, JPG, JPEG** görsel dosyalarını desteklemektedir:

### Desteklenen Dönüşümler
- 🖼️ **Image** → Markdown
- 🖼️ **Image** → PDF  
- 🖼️ **Image** → DOCX
- 🖼️ **Image** → HTML

### Gelişmiş İçerik Tanıma
- ✅ **Standart Metin**: Yüksek doğruluklu OCR ile tüm metin çıkarılır
- ✅ **Başlık Tespit**: Büyük/kalın metinler otomatik başlık olarak işaretlenir
- ✅ **Liste Tanıma**: Madde işaretli ve numaralı listeler korunur
- ✅ **Tablo Algılama**: Grid yapıları Markdown/HTML tablo formatına dönüştürülür
- ✅ **Kod Bloğu Tespit**: Girintili ve anahtar kelime içeren bloklar kod olarak işaretlenir
- 🔄 **Matematik Formül**: LaTeX dönüşümü (geliştirme aşamasında)

## 📋 Gereksinimler

### 1. Python Kütüphaneleri
```bash
# Zaten yüklü (requirements.txt'te mevcut)
pip install pytesseract pdf2image pillow
```

### 2. Tesseract OCR Motoru

#### Windows
1. İndirin: https://github.com/UB-Mannheim/tesseract/wiki
2. Kurulum dosyasını çalıştırın (önerilen: `tesseract-ocr-w64-setup-5.3.x.exe`)
3. Kurulum yolu: `C:\Program Files\Tesseract-OCR`
4. Sistem PATH'e ekleyin veya Python'da tanımlayın:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

#### macOS
```bash
brew install tesseract
```

### 3. Türkçe Dil Desteği
```bash
# Windows - Kurulum sırasında Turkish seçin veya
# Linux/macOS
sudo apt install tesseract-ocr-tur  # Linux
brew install tesseract-lang          # macOS
```

## 🚀 Kullanım

### Python API

```python
from converters import UniversalConverter

converter = UniversalConverter()

# Image → Markdown
result = converter.convert(
    input_file="document_scan.png",
    input_format="image",
    output_format="markdown"
)

# Image → PDF
result = converter.convert(
    input_file="notes.jpg",
    input_format="image",
    output_format="pdf",
    ocr_language="tur+eng"  # Türkçe + İngilizce
)

# Image → DOCX
result = converter.convert(
    input_file="screenshot.jpeg",
    input_format="image",
    output_format="docx",
    detect_tables=True,      # Tablo algılama
    detect_code=True,        # Kod bloğu algılama
    detect_math=False        # Matematik formül (henüz beta)
)

if result.success:
    print(f"✅ Başarılı: {result.output_file}")
    print(f"📊 OCR Güveni: {result.metadata.get('ocr_confidence', 0):.1f}%")
    print(f"📝 Kelime Sayısı: {result.metadata.get('word_count', 0)}")
else:
    print(f"❌ Hata: {result.error}")
```

### Komut Satırı

```bash
# Temel dönüşüm
python cli.py convert image document_scan.png markdown

# Özel çıktı dosyası
python cli.py convert image notes.jpg pdf --output my_notes.pdf

# Tablo ve kod algılama ile
python cli.py convert image screenshot.png docx --detect-tables --detect-code
```

### Web Arayüzü

```bash
python app.py
# http://127.0.0.1:5000 adresine gidin
# Image formatını seçin ve dosya yükleyin
```

## ⚙️ İleri Seviye Ayarlar

### OCR Dil Konfigürasyonu

`.env` dosyasında:
```bash
# Varsayılan: Türkçe + İngilizce
OCR_LANGUAGE=tur+eng

# Sadece İngilizce
OCR_LANGUAGE=eng

# Çoklu dil (Türkçe + İngilizce + Almanca)
OCR_LANGUAGE=tur+eng+deu
```

### DPI Ayarı (PDF → Image dönüşümünde)

```bash
DEFAULT_DPI=300  # Yüksek kalite (varsayılan)
DEFAULT_DPI=150  # Normal kalite (hızlı)
DEFAULT_DPI=600  # Çok yüksek kalite (yavaş)
```

## 📊 Performans ve Doğruluk

### OCR Güven Skorları
- **90%+**: Mükemmel - Temiz, yüksek çözünürlüklü metin
- **75-90%**: Çok İyi - Okunabilir, az hata
- **60-75%**: İyi - Kullanılabilir, bazı hatalar
- **50-60%**: Kabul Edilebilir - Manuel kontrol önerilir
- **<50%**: Zayıf - Görsel kalitesi düşük

### Optimizasyon İpuçları
1. **Yüksek Çözünürlük**: En az 300 DPI tavsiye edilir
2. **Kontrast**: Siyah metin, beyaz arka plan en iyisidir
3. **Düz Açı**: Görsel eğik olmamalı (otomatik düzeltme yapılır)
4. **Temiz Arka Plan**: Gürültü ve lekeler OCR'ı zorlaştırır
5. **Yazı Tipi**: Standart yazı tipleri daha iyi tanınır

## 🔍 Sorun Giderme

### "Tesseract not found" Hatası
```bash
# Windows - PATH kontrolü
where tesseract

# Linux/macOS
which tesseract

# Python'da manuel tanımlama
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Düşük OCR Doğruluğu
- Görsel kalitesini artırın
- Kontrast ve parlaklığı ayarlayın
- Doğru dil paketini seçin
- DPI ayarını yükseltin

### Türkçe Karakterler Bozuk
- Türkçe dil paketi kurulu olduğundan emin olun
- `OCR_LANGUAGE=tur+eng` ayarını kontrol edin
- Font desteği için Arial/DejaVu fontları kurulu olmalı

## 🎓 Örnekler

### Örnek 1: Taranmış Belge
```python
# Kitap sayfası → PDF
converter = UniversalConverter()
result = converter.convert(
    input_file="book_page.jpg",
    output_format="pdf",
    ocr_language="tur"
)
```

### Örnek 2: Ekran Görüntüsü
```python
# Kod içeren screenshot → Markdown
result = converter.convert(
    input_file="code_screenshot.png",
    output_format="markdown",
    detect_code=True
)
```

### Örnek 3: El Yazısı Notlar
```python
# Not kağıdı → DOCX
result = converter.convert(
    input_file="handwritten_notes.jpg",
    output_format="docx",
    ocr_language="tur+eng"
)
# Not: El yazısı tanıma sınırlıdır, temiz yazı önerilir
```

## 🛠️ Gelişmiş Özellikler (Yol Haritası)

### Yakında Gelecek
- 🔬 **Matematik Formül Tanıma**: LaTeX dönüşümü (Pix2Tex)
- 📊 **Gelişmiş Tablo Algılama**: Birleştirilmiş hücreler, karmaşık yapılar
- 🎨 **Layout Analizi**: Çok sütunlu belgeler, karmaşık düzenler
- 🖊️ **El Yazısı Tanıma**: Daha iyi el yazısı desteği
- 🌍 **Çoklu Dil**: 100+ dil desteği

### Katkıda Bulunun
Görsel tanıma kalitesini artırmak için:
1. Test görselleri gönderin
2. Hataları raporlayın
3. Özellik önerisi yapın
4. Kod katkısı sağlayın

## 📚 API Referansı

### ImageConverter Sınıfı

```python
from converters.image_converter import ImageConverter

converter = ImageConverter()

# Markdown'a dönüştür
result = converter._image_to_markdown(
    input_file="image.png",
    output_file="output.md",
    ocr_language="tur+eng",     # OCR dili
    detect_math=False,           # Matematik algılama
    detect_tables=True,          # Tablo algılama
    detect_code=True             # Kod algılama
)

# Metadata
print(result.metadata['ocr_confidence'])  # OCR güven skoru
print(result.metadata['word_count'])      # Kelime sayısı
print(result.metadata['layout_blocks'])   # Algılanan blok sayısı
```

## 📄 Lisans ve Krediler

- **Tesseract OCR**: Apache 2.0 License
- **ConverterAI**: MIT License
- **VCR-01 Specification**: Özel geliştirme

---

**Not**: Bu özellik aktif geliştirme aşamasındadır. Geri bildirimleriniz ve katkılarınız çok değerlidir!
