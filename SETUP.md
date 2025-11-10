# ConverterAI Kurulum ve Kullanım Rehberi

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Yükleyin

```powershell
# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktive edin
.\venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 2. Ortam Değişkenlerini Ayarlayın

```powershell
# .env dosyasını oluşturun
copy .env.example .env

# .env dosyasını düzenleyin (opsiyonel)
notepad .env
```

### 3. Ek Araçları Kurun (Opsiyonel)

#### Tesseract OCR (Taranmış PDF'ler için)
1. İndirin: https://github.com/UB-Mannheim/tesseract/wiki
2. Kurun (varsayılan konum: `C:\Program Files\Tesseract-OCR`)
3. PATH'e ekleyin veya `.env` dosyasında belirtin

#### wkhtmltopdf (HTML to PDF için)
1. İndirin: https://wkhtmltopdf.org/downloads.html
2. Kurun
3. PATH'e ekleyin

## 🌐 Web Arayüzü ile Kullanım

### Uygulamayı Başlatın

```powershell
python app.py
```

Tarayıcınızda açın: http://localhost:5000

### Web Arayüzü Özellikleri

1. **Dosya Yükleme**: Sürükle-bırak veya tıklayarak dosya seçin
2. **Format Seçimi**: Hedef formatı seçin (PDF, DOCX, Markdown, HTML)
3. **AI Kalite Kontrolü**: İsteğe bağlı olarak kalite kontrolü aktifleştirin
4. **Dönüştür**: Tek tıkla dönüştürme
5. **İndir**: Dönüştürülen dosyayı indirin

## 💻 Komut Satırı ile Kullanım

### Tek Dosya Dönüştürme

```powershell
# PDF'den DOCX'e
python cli.py convert document.pdf --to docx

# Kalite kontrolü ile
python cli.py convert document.pdf --to html --quality-check

# Çıktı dosyası belirterek
python cli.py convert input.pdf --to docx --output result.docx
```

### Toplu Dönüştürme

```powershell
# Klasördeki tüm dosyaları dönüştür
python cli.py batch --input-folder ./docs --format markdown --output-folder ./converted

# Belirli dosya türlerini dönüştür
python cli.py batch -i ./docs -f pdf -p "*.md"
```

### Desteklenen Formatları Listele

```powershell
python cli.py list-formats
```

## 🐍 Python API ile Kullanım

### Basit Kullanım

```python
from converters import UniversalConverter

converter = UniversalConverter()

# PDF'den DOCX'e dönüştür
result = converter.convert(
    input_file="document.pdf",
    output_format="docx"
)

if result.success:
    print(f"Başarılı! Çıktı: {result.output_file}")
else:
    print(f"Hata: {result.error}")
```

### Gelişmiş Kullanım

```python
from converters import UniversalConverter

converter = UniversalConverter()

# AI kalite kontrolü ile dönüştürme
result = converter.convert(
    input_file="document.pdf",
    output_format="html",
    output_file="output.html",
    quality_check=True
)

if result.success:
    print(f"İşlem süresi: {result.processing_time:.2f}s")
    print(f"Kalite skoru: {result.quality_score * 100:.1f}%")
    
    if result.warnings:
        print("Uyarılar:")
        for warning in result.warnings:
            print(f"  - {warning}")
```

### Toplu Dönüştürme

```python
from converters import UniversalConverter

converter = UniversalConverter()

files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

results = converter.batch_convert(
    input_files=files,
    output_format="markdown",
    output_dir="./converted",
    quality_check=True
)

# Sonuçları göster
for result in results:
    if result.success:
        print(f"✅ {result.input_file}")
    else:
        print(f"❌ {result.input_file}: {result.error}")
```

## 📋 Desteklenen Dönüşümler

### PDF
- PDF → DOCX
- PDF → Markdown
- PDF → HTML

### DOCX
- DOCX → PDF
- DOCX → Markdown
- DOCX → HTML

### Markdown
- Markdown → PDF
- Markdown → DOCX
- Markdown → HTML

### HTML
- HTML → PDF
- HTML → DOCX
- HTML → Markdown

## ⚙️ Yapılandırma

`.env` dosyasında ayarlayabileceğiniz seçenekler:

```env
# Uygulama ayarları
APP_HOST=127.0.0.1
APP_PORT=5000
DEBUG=True

# Dosya yükleme ayarları
MAX_FILE_SIZE_MB=50
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# Dönüştürme ayarları
DEFAULT_DPI=300
OCR_LANGUAGE=tur+eng
ENABLE_AI_QUALITY_CHECK=True

# AI API anahtarları (opsiyonel)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

## 🔧 Sorun Giderme

### "Module not found" hatası
```powershell
pip install -r requirements.txt
```

### Tesseract bulunamıyor
```powershell
# Tesseract kurulu olduğundan emin olun
tesseract --version

# PATH'e ekleyin veya .env dosyasında belirtin
```

### WeasyPrint kurulum hatası
```powershell
# GTK3 gerekebilir (Windows için)
# https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
```

### Port zaten kulanımda
```powershell
# .env dosyasında farklı port belirtin
APP_PORT=8000
```

## 📚 Örnekler

Daha fazla örnek için `examples.py` dosyasına bakın:

```powershell
python examples.py
```

## 🧪 Testler

```powershell
# Tüm testleri çalıştır
pytest

# Coverage raporu ile
pytest --cov=converters --cov-report=html
```

## 📝 Notlar

- **OCR özelliği** için Tesseract kurulumu gereklidir
- **AI kalite kontrolü** için OpenAI veya Anthropic API anahtarı gereklidir (opsiyonel)
- Tüm dosyalar **local olarak** işlenir, buluta yükleme yapılmaz
- Büyük dosyaların dönüştürülmesi zaman alabilir

## 🆘 Yardım

Daha fazla bilgi için:
- README.md dosyasını okuyun
- GitHub Issues sayfasını ziyaret edin
- Dokümantasyonu kontrol edin

## 🎉 Başarılı Kurulum!

Artık ConverterAI kullanıma hazır! İyi dönüşümler! 🚀
