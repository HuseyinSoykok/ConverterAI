# ConverterAI - Hızlı Başlangıç Kılavuzu 🚀

## 📌 Projeniz Hazır!

ConverterAI başarıyla oluşturuldu. Bu profesyonel doküman dönüştürme sistemi şunları içerir:

### ✨ Temel Özellikler
- ✅ 12 farklı dönüşüm yönü (PDF ↔ DOCX ↔ Markdown ↔ HTML)
- ✅ Modern web arayüzü (Flask + HTML/CSS/JS)
- ✅ Komut satırı arayüzü (CLI)
- ✅ Python API
- ✅ **🆓 Ücretsiz AI kalite kontrolü** (API key gerektirmez!)
  - Heuristic (varsayılan)
  - Transformers (önerilen)
  - Ollama (en güçlü)
- ✅ OCR desteği (taranmış PDF'ler)
- ✅ Toplu dönüştürme
- ✅ %100 local çalışma

## 🎯 Hemen Başlayın

### 1. Sanal Ortam ve Bağımlılıklar

```powershell
# Sanal ortam oluştur
python -m venv venv

# Aktive et
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Ortam Değişkenlerini Ayarla

```powershell
# .env dosyası oluştur
copy .env.example .env
```

### 3. Web Uygulamasını Başlat

```powershell
python app.py
```

Tarayıcıda aç: **http://localhost:5000**

## 📚 Kullanım Örnekleri

### Web Arayüzü
1. Dosyayı sürükle-bırak
2. Hedef formatı seç (PDF, DOCX, Markdown, HTML)
3. "Dönüştür" butonuna tıkla
4. İndir!

### Komut Satırı

```powershell
# Basit dönüşüm
python cli.py convert document.pdf --to docx

# Kalite kontrolü ile
python cli.py convert document.pdf --to html --quality-check

# Toplu dönüşüm
python cli.py batch -i ./docs -f markdown -o ./converted
```

### Python API

```python
from converters import UniversalConverter

converter = UniversalConverter()

result = converter.convert(
    input_file="document.pdf",
    output_format="docx",
    quality_check=True
)

if result.success:
    print(f"Başarılı! {result.output_file}")
    print(f"Kalite: {result.quality_score * 100:.1f}%")
```

## 📁 Önemli Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `app.py` | Flask web uygulaması |
| `cli.py` | Komut satırı arayüzü |
| `examples.py` | Kullanım örnekleri |
| `README.md` | Detaylı dokümantasyon |
| `SETUP.md` | Kurulum rehberi |
| `PROJECT_STRUCTURE.md` | Proje yapısı |

## 🎨 Desteklenen Dönüşümler

```
📄 PDF
  → DOCX
  → Markdown
  → HTML

📝 DOCX
  → PDF
  → Markdown
  → HTML

📋 Markdown
  → PDF
  → DOCX
  → HTML

🌐 HTML
  → PDF
  → DOCX
  → Markdown
```

## 🔧 Opsiyonel Araçlar

### Tesseract OCR (Taranmış PDF'ler için)
```
İndir: https://github.com/UB-Mannheim/tesseract/wiki
Kur ve PATH'e ekle
```

### wkhtmltopdf (HTML to PDF için)
```
İndir: https://wkhtmltopdf.org/downloads.html
Kur ve PATH'e ekle
```

## 🧪 Test Edin

```powershell
# Örnek kullanımları çalıştır
python examples.py

# Testleri çalıştır
pytest

# Formatları listele
python cli.py list-formats
```

## 💡 İpuçları

1. **İlk Dönüşüm**: Küçük bir dosya ile test edin
2. **🆓 Ücretsiz AI**: Transformers yöntemi önerilir (API key gerektirmez!)
   ```env
   AI_QUALITY_METHOD=transformers
   ```
3. **AI Detayları**: [FREE_AI_GUIDE.md](FREE_AI_GUIDE.md) dosyasına bakın
4. **OCR**: Taranmış PDF'ler için Tesseract kurun
5. **Performans**: Büyük dosyalar için sabırlı olun
6. **Güvenlik**: Tüm işlemler local, dosyalar buluta gitmiyor

## 📖 Daha Fazla Bilgi

- **README.md**: Tam özellikler ve dokümantasyon
- **SETUP.md**: Detaylı kurulum ve sorun giderme
- **PROJECT_STRUCTURE.md**: Kod yapısı ve mimari
- **examples.py**: 7 farklı kullanım örneği

## 🎉 Tebrikler!

ConverterAI kullanıma hazır! İyi dönüşümler! 🚀

## 🆘 Sorun mu var?

1. `pip install -r requirements.txt` komutuyla bağımlılıkları kontrol edin
2. Python 3.8+ kullandığınızdan emin olun
3. SETUP.md dosyasındaki sorun giderme bölümüne bakın
4. Log dosyalarını kontrol edin: `logs/converter.log`

## 🌟 Özelleştirme

`.env` dosyasını düzenleyerek:
- Port değiştirme
- Dosya boyutu limiti
- DPI ayarları
- OCR dili
- **🆓 AI yöntemi** (heuristic, transformers, ollama)
- AI API anahtarları (opsiyonel, ücretli)

### Ücretsiz AI Kalite Kontrolü 🎉

```env
# .env dosyası
AI_QUALITY_METHOD=transformers  # Önerilen, ücretsiz!

# Diğer seçenekler:
# AI_QUALITY_METHOD=heuristic   # En hızlı
# AI_QUALITY_METHOD=ollama      # En güçlü (Ollama kurulumu gerekli)
```

Detaylı bilgi: **[FREE_AI_GUIDE.md](FREE_AI_GUIDE.md)** 📖

---

**Not**: Bu proje tamamen local çalışır. Verileriniz güvende! 🔒

**Bonus**: API key'siz ücretsiz AI kalite kontrolü! 🆓🤖
