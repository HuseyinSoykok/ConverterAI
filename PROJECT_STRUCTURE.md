# ConverterAI Proje Yapısı

```
ConverterAI/
│
├── 📄 app.py                      # Flask web uygulaması (ana dosya)
├── 📄 cli.py                      # Komut satırı arayüzü
├── 📄 config.py                   # Yapılandırma ayarları
├── 📄 examples.py                 # Kullanım örnekleri
│
├── 📋 requirements.txt            # Python bağımlılıkları
├── 📋 README.md                   # Ana dokümantasyon
├── 📋 SETUP.md                    # Kurulum ve kullanım rehberi
├── 📋 .env.example                # Örnek ortam değişkenleri
├── 📋 .gitignore                  # Git ignore dosyası
│
├── 📁 converters/                 # Dönüşüm motorları
│   ├── __init__.py
│   ├── base.py                   # Temel converter sınıfı
│   ├── pdf_converter.py          # PDF dönüşümleri
│   ├── docx_converter.py         # DOCX dönüşümleri
│   ├── markdown_converter.py     # Markdown dönüşümleri
│   ├── html_converter.py         # HTML dönüşümleri
│   └── universal.py              # Merkezi converter
│
├── 📁 ai/                         # AI modülleri
│   ├── __init__.py
│   ├── quality_checker.py        # Kalite değerlendirme
│   └── ocr_engine.py             # OCR motoru
│
├── 📁 utils/                      # Yardımcı fonksiyonlar
│   ├── __init__.py
│   ├── file_handler.py           # Dosya işlemleri
│   ├── validator.py              # Doğrulama
│   └── logger.py                 # Loglama
│
├── 📁 static/                     # Frontend dosyaları
│   ├── css/
│   │   └── style.css             # Ana stil dosyası
│   ├── js/
│   │   └── app.js                # Frontend JavaScript
│   └── images/
│
├── 📁 templates/                  # HTML şablonları
│   └── index.html                # Ana sayfa
│
├── 📁 tests/                      # Test dosyaları
│   └── test_converters.py        # Converter testleri
│
├── 📁 uploads/                    # Yüklenen dosyalar (otomatik oluşur)
├── 📁 outputs/                    # Dönüştürülen dosyalar (otomatik oluşur)
├── 📁 temp/                       # Geçici dosyalar (otomatik oluşur)
└── 📁 logs/                       # Log dosyaları (otomatik oluşur)
```

## 📦 Ana Modüller

### 1. Converters (Dönüştürücüler)
- **base.py**: Tüm dönüştürücüler için temel sınıf
- **pdf_converter.py**: PDF → DOCX/Markdown/HTML
- **docx_converter.py**: DOCX → PDF/Markdown/HTML
- **markdown_converter.py**: Markdown → PDF/DOCX/HTML
- **html_converter.py**: HTML → PDF/DOCX/Markdown
- **universal.py**: Tüm dönüştürücüleri yöneten merkezi sınıf

### 2. AI Modülleri
- **quality_checker.py**: AI ile kalite değerlendirme (OpenAI/Anthropic)
- **ocr_engine.py**: Tesseract ile OCR (taranmış PDF'ler için)

### 3. Utilities (Yardımcılar)
- **file_handler.py**: Dosya kopyalama, taşıma, silme, temizleme
- **validator.py**: Dosya ve dönüşüm doğrulama
- **logger.py**: Loglama sistemi

### 4. Web Arayüzü
- **app.py**: Flask backend API
- **templates/index.html**: Modern ve responsive web arayüzü
- **static/css/style.css**: Özel CSS stilleri
- **static/js/app.js**: Frontend JavaScript mantığı

### 5. CLI ve Örnekler
- **cli.py**: Komut satırı arayüzü
- **examples.py**: Python API kullanım örnekleri

## 🔄 Veri Akışı

### Web Arayüzü Akışı
```
Kullanıcı → Frontend (HTML/JS) → Flask API → UniversalConverter → 
Format-Specific Converter → Output File → Download
```

### CLI Akışı
```
Komut → CLI Parser → UniversalConverter → Format-Specific Converter → 
Output File → Console Output
```

### Python API Akışı
```
Python Code → UniversalConverter.convert() → Validation → 
Format Detection → Converter Selection → Conversion → Result Object
```

## 🛠️ Teknolojiler

### Backend
- **Python 3.8+**: Ana programlama dili
- **Flask**: Web framework
- **PyMuPDF**: PDF işleme
- **python-docx**: DOCX işleme
- **BeautifulSoup4**: HTML parsing
- **WeasyPrint**: HTML to PDF
- **Markdown**: Markdown işleme
- **Tesseract**: OCR motoru

### Frontend
- **HTML5**: Yapı
- **CSS3**: Stil (Flexbox, Grid, Animations)
- **Vanilla JavaScript**: İnteraktivite
- **Font Awesome**: İkonlar

### AI
- **OpenAI GPT**: Kalite değerlendirme (opsiyonel)
- **Anthropic Claude**: Alternatif AI (opsiyonel)

## 📊 Özellikler

### ✅ Temel Özellikler
- 12 farklı dönüşüm yönü (PDF/DOCX/Markdown/HTML)
- Web tabanlı arayüz
- Komut satırı arayüzü
- Python API
- Toplu dönüştürme
- İlerleme takibi

### 🎨 Gelişmiş Özellikler
- AI destekli kalite kontrolü
- OCR desteği (taranmış PDF'ler)
- Format koruma (başlıklar, tablolar, görseller)
- Otomatik dosya temizleme
- Hata yönetimi ve loglama
- Responsive tasarım

### 🔒 Güvenlik
- Local işleme (bulut yok)
- Dosya boyutu sınırlaması
- Güvenli dosya adı sanitization
- Otomatik geçici dosya temizleme

## 🚀 Başlangıç Komutları

```powershell
# Kurulum
pip install -r requirements.txt

# Web arayüzü
python app.py

# CLI kullanımı
python cli.py convert document.pdf --to docx

# Örnekleri çalıştır
python examples.py

# Testleri çalıştır
pytest
```

## 📝 Notlar

- Tüm dönüştürücüler **BaseConverter** sınıfından türetilir
- Her dönüştürücü **ConversionResult** objesi döndürür
- Hata durumunda detaylı mesajlar döner
- Log dosyaları `logs/` klasöründe saklanır
- Geçici dosyalar otomatik temizlenir (24 saat)
