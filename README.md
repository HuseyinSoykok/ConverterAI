# ConverterAI 🚀

**AI Destekli Profesyonel Doküman Dönüşüm Sistemi**

ConverterAI, PDF, DOCX, Markdown ve HTML formatları arasında yapay zeka destekli, yüksek kaliteli dönüşümler sağlayan, tamamen local çalışan bir doküman dönüşüm platformudur.

## ✨ Özellikler

### Desteklenen Dönüşümler
- 📄 **PDF** ↔️ DOCX / Markdown / HTML
- 📝 **DOCX** ↔️ PDF / Markdown / HTML
- 📋 **Markdown** ↔️ PDF / DOCX / HTML
- 🌐 **HTML** ↔️ PDF / DOCX / Markdown

### Temel Özellikler
- ✅ **AI Destekli Kalite Kontrol** - Dönüşüm kalitesini otomatik değerlendirme
  - 🆓 **Heuristic**: Sezgisel analiz (her zaman kullanılabilir)
  - 🆓 **Transformers**: Semantic AI analizi (ücretsiz, önerilen)
  - 🆓 **Ollama**: Local LLM ile GPT kalitesinde analiz (ücretsiz)
  - 💰 OpenAI/Anthropic: Ücretli API'lar (opsiyonel)
- 🔒 **100% Local** - Dosyalarınız bilgisayarınızdan çıkmaz
- 🎨 **Format Koruma** - Başlıklar, tablolar, görseller korunur
- 📊 **OCR Desteği** - Taranmış PDF'lerden metin çıkarımı
- 📦 **Toplu İşleme** - Birden fazla dosyayı aynı anda dönüştürme
- 📈 **İlerleme Takibi** - Real-time dönüşüm durumu
- 💾 **Export As** - Dönüştürülen dosyaları indirme
- 🎯 **Kullanıcı Dostu Arayüz** - Modern ve responsive tasarım

## 🛠️ Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- 2 GB RAM (önerilen)
- 100 MB boş disk alanı

### Adım 1: Repository'yi İndirin
```bash
git clone https://github.com/HuseyınSoykok/ConverterAI.git
cd ConverterAI
```

### Adım 2: Sanal Ortam Oluşturun
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: Yapılandırma
```bash
# .env dosyasını oluşturun
copy .env.example .env
# .env dosyasını düzenleyin (isteğe bağlı)
```

### Adım 5: Ek Araçlar (Windows için)
- **Tesseract OCR** (taranmış PDF'ler için):
  - İndirin: https://github.com/UB-Mannheim/tesseract/wiki
  - PATH'e ekleyin
  
- **wkhtmltopdf** (HTML to PDF için):
  - İndirin: https://wkhtmltopdf.org/downloads.html
  - PATH'e ekleyin

## 🚀 Kullanım

### Web Arayüzü ile Kullanım
```bash
python app.py
```
Tarayıcınızda `http://localhost:5000` adresini açın.

### Komut Satırı ile Kullanım
```bash
# Tek dosya dönüşümü
python cli.py convert input.pdf --to docx --output output.docx

# Toplu dönüşüm
python cli.py batch --input-folder ./docs --format markdown --output-folder ./converted

# Kalite kontrolü
python cli.py convert input.pdf --to html --quality-check
```

## 📚 API Kullanımı

```python
from converters import UniversalConverter

# Converter oluştur
converter = UniversalConverter()

# PDF'i DOCX'e dönüştür
result = converter.convert(
    input_file="document.pdf",
    output_format="docx",
    output_file="output.docx",
    quality_check=True
)

if result.success:
    print(f"Dönüşüm başarılı! Kalite skoru: {result.quality_score}")
else:
    print(f"Hata: {result.error}")
```

## 🏗️ Proje Yapısı

```
ConverterAI/
├── app.py                      # Flask web uygulaması
├── cli.py                      # Komut satırı arayüzü
├── config.py                   # Yapılandırma ayarları
├── requirements.txt            # Python bağımlılıkları
├── README.md                   # Dokümantasyon
│
├── converters/                 # Dönüşüm motorları
│   ├── __init__.py
│   ├── base.py                # Temel converter sınıfı
│   ├── pdf_converter.py       # PDF dönüşümleri
│   ├── docx_converter.py      # DOCX dönüşümleri
│   ├── markdown_converter.py  # Markdown dönüşümleri
│   ├── html_converter.py      # HTML dönüşümleri
│   └── universal.py           # Merkezi converter
│
├── ai/                         # AI modülleri
│   ├── __init__.py
│   ├── quality_checker.py     # Kalite değerlendirme
│   └── ocr_engine.py          # OCR motoru
│
├── utils/                      # Yardımcı fonksiyonlar
│   ├── __init__.py
│   ├── file_handler.py        # Dosya işlemleri
│   ├── validator.py           # Doğrulama
│   └── logger.py              # Loglama
│
├── static/                     # Frontend dosyaları
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│
├── templates/                  # HTML şablonları
│   └── index.html
│
└── tests/                      # Test dosyaları
    ├── test_converters.py
    └── test_quality.py
```

## 🎯 Kullanım Örnekleri

### Web Arayüzü
1. Dosyayı sürükle-bırak veya seç
2. Hedef formatı seç
3. "Dönüştür" butonuna tıkla
4. Önizleme yap
5. "İndir" ile dosyayı kaydet

### Python API
```python
# Örnek 1: Markdown'dan PDF
converter.convert("README.md", "pdf", "README.pdf")

# Örnek 2: HTML'den DOCX (AI kalite kontrolü ile)
result = converter.convert(
    "webpage.html", 
    "docx", 
    "document.docx",
    quality_check=True,
    preserve_images=True
)

# Örnek 3: Toplu dönüşüm
converter.batch_convert(
    input_files=["doc1.pdf", "doc2.pdf"],
    output_format="markdown",
    output_dir="./converted"
)
```

## 🔧 Yapılandırma

`.env` dosyasında şu ayarları yapabilirsiniz:

- `MAX_FILE_SIZE_MB`: Maksimum dosya boyutu (varsayılan: 50 MB)
- `DEFAULT_DPI`: PDF çözünürlüğü (varsayılan: 300)
- `OCR_LANGUAGE`: OCR dili (varsayılan: tur+eng)
- `ENABLE_AI_QUALITY_CHECK`: AI kalite kontrolü (varsayılan: True)
- `AI_QUALITY_METHOD`: Kalite kontrol yöntemi
  - `heuristic` - Sezgisel (varsayılan, her zaman kullanılabilir)
  - `transformers` - HuggingFace AI (ücretsiz, önerilen) 🌟
  - `ollama` - Local LLM (ücretsiz, GPT benzeri)
  - `openai` - OpenAI API (ücretli, opsiyonel)
  - `anthropic` - Anthropic API (ücretli, opsiyonel)

### 🆓 Ücretsiz AI Kalite Kontrolü

**Hiçbir API key'e ihtiyacınız yok!** Detaylı bilgi için: [FREE_AI_GUIDE.md](FREE_AI_GUIDE.md)

```env
# .env dosyası
AI_QUALITY_METHOD=transformers  # Ücretsiz, güçlü, önerilen!
```

## 🧪 Test

```bash
# Tüm testleri çalıştır
pytest

# Coverage raporu
pytest --cov=converters --cov-report=html
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📧 İletişim

Sorularınız için issue açabilir veya [https://huseyinsoykok.github.io/huseyin_soykok/] adresinden ulaşabilirsiniz.

## 🙏 Teşekkürler

Bu proje şu açık kaynak kütüphaneleri kullanmaktadır:
- PyMuPDF, python-docx, BeautifulSoup4, WeasyPrint ve daha fazlası
- HuggingFace Transformers (ücretsiz AI)
- Ollama (ücretsiz local LLM)

---

**Not**: 
- 🆓 **AI kalite kontrolü tamamen ücretsiz!** API key gerekmez.
- 💡 Transformers yöntemi önerilir (ücretsiz ve güçlü).
- 📖 Detaylar için: [FREE_AI_GUIDE.md](FREE_AI_GUIDE.md)
