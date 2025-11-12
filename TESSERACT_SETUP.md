# 🔧 Tesseract OCR Kurulum Rehberi (Windows)

## 📥 Adım 1: İndirme

### Otomatik İndirme (PowerShell)
```powershell
# Tesseract 5.3.3 (En son kararlı sürüm)
$url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
$output = "$env:TEMP\tesseract-setup.exe"

Write-Host "📥 Tesseract OCR indiriliyor..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $url -OutFile $output
Write-Host "✅ İndirildi: $output" -ForegroundColor Green
Start-Process $output
```

### Manuel İndirme
1. Şu linke git: https://github.com/UB-Mannheim/tesseract/wiki
2. **tesseract-ocr-w64-setup-5.3.3.xxxxxxxx.exe** dosyasını indir
3. Çalıştır

---

## 🛠️ Adım 2: Kurulum

### Kurulum Adımları:
1. **İndirilen .exe dosyasını çalıştır**
2. **"Next"** tıkla
3. **"I accept the agreement"** seç → Next
4. **Kurulum Yolu**: `C:\Program Files\Tesseract-OCR` (varsayılan, değiştirme)
5. **ÖNEMLİ - Additional Language Data**:
   - ✅ **Turkish** (tur) - MUTLAKA SEÇ!
   - ✅ **English** (eng) - Zaten seçili
   - İsterseniz diğer diller (deu=Almanca, fra=Fransızca, etc.)
6. **"Add Tesseract to PATH"** seçeneğini İŞARETLE ✅
7. **Install** → Bekle → **Finish**

---

## ⚙️ Adım 3: PATH Kontrolü

### PowerShell ile Kontrol:
```powershell
# PATH'e eklenmiş mi kontrol et
$env:Path -split ';' | Select-String "Tesseract"

# Tesseract çalışıyor mu test et
tesseract --version

# Kurulu diller
tesseract --list-langs
```

### Manuel PATH Ekleme (Gerekirse):
Eğer `tesseract --version` çalışmazsa:

1. **Windows Ayarlar** → **Sistem** → **Hakkında**
2. **Gelişmiş sistem ayarları**
3. **Ortam Değişkenleri**
4. **Sistem değişkenleri** altında **Path** seç → **Düzenle**
5. **Yeni** → `C:\Program Files\Tesseract-OCR` ekle
6. **Tamam** → **PowerShell'i yeniden başlat**

---

## 🧪 Adım 4: Python Entegrasyonu

### Python'da Tesseract Yolu Ayarla:

Eğer PATH sorunu devam ederse, Python kodunda manuel yol belirt:

**Yöntem 1: Ortam Değişkeni** (`.env` dosyasına ekle):
```bash
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Yöntem 2: Python Kodu** (`ai/ocr_engine.py`):
```python
import pytesseract

# Windows için manuel yol
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## ✅ Adım 5: Test

### PowerShell'de Test:
```powershell
# 1. Tesseract çalışıyor mu?
tesseract --version
# Çıktı: tesseract 5.3.3

# 2. Türkçe dil paketi kurulu mu?
tesseract --list-langs
# Çıktıda 'tur' ve 'eng' görünmeli

# 3. Basit OCR testi
cd D:\Projects\Python\ConverterAI
D:\.venv\Scripts\python.exe -c "from ai.ocr_engine import OCREngine; e = OCREngine(); print('✅ OCR Engine hazır!')"
```

### Python Test Script:
```powershell
# Görsel dönüştürme testi (gerçek OCR ile)
cd D:\Projects\Python\ConverterAI
D:\.venv\Scripts\python.exe test_image_converter.py
```

---

## 🔧 Sorun Giderme

### Problem 1: "tesseract is not recognized"
**Çözüm**: PATH'e ekle (Adım 3'e bak)

### Problem 2: "Error opening data file"
**Çözüm**: Türkçe dil paketi eksik
```powershell
# Tesseract'i kaldır ve yeniden kur
# Kurulumda "Turkish" seçmeyi unutma!
```

### Problem 3: Python'da "Tesseract not found"
**Çözüm**: Manuel yol belirt (Adım 4)

### Problem 4: Düşük OCR Doğruluğu
**Çözümler**:
- Görsel çözünürlüğünü artır (300+ DPI)
- Kontrast artır (siyah-beyaz)
- Gürültüyü azalt
- Doğru dil paketi seçilmiş mi kontrol et

---

## 📊 Kurulum Sonrası Beklenen Sonuçlar

### Komut Satırı:
```powershell
PS> tesseract --version
tesseract 5.3.3
 leptonica-1.83.1
  libgif 5.2.1 : libjpeg 8d (libjpeg-turbo 2.1.3) : libpng 1.6.39 : libtiff 4.5.0 : zlib 1.2.13 : libwebp 1.2.4 : libopenjp2 2.5.0

PS> tesseract --list-langs
List of available languages (3):
eng
osd
tur
```

### Python Test:
```python
from ai.ocr_engine import OCREngine

engine = OCREngine(language='tur+eng')
result = engine.extract_text_from_image('test_image.png')

print(f"OCR Başarılı: {result['success']}")
print(f"Güven Skoru: {result['confidence']:.1f}%")
print(f"Metin: {result['text'][:100]}...")
```

---

## 🎯 ConverterAI için Önerilen Ayarlar

### `.env` Dosyası:
```bash
# OCR Ayarları
OCR_LANGUAGE=tur+eng          # Türkçe + İngilizce
DEFAULT_DPI=300               # Yüksek kalite
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe  # Opsiyonel
```

### İlk Kullanım:
```powershell
# Demo çalıştır (OCR'sız - pipeline testi)
python demo_image_converter.py

# Gerçek OCR testi
python test_image_converter.py

# CLI ile görsel dönüştür
python cli.py convert scan.png --to pdf
```

---

## 📚 Ek Kaynaklar

- **Tesseract Dokümantasyonu**: https://tesseract-ocr.github.io/
- **Dil Paketleri**: https://github.com/tesseract-ocr/tessdata
- **ConverterAI Rehberi**: `IMAGE_CONVERSION_GUIDE.md`
- **Pytesseract Dokümantasyonu**: https://pypi.org/project/pytesseract/

---

## 🎉 Kurulum Tamamlandı!

Artık ConverterAI ile gerçek görsel tanıma yapabilirsiniz:

```python
from converters import UniversalConverter

converter = UniversalConverter()
result = converter.convert(
    input_file="taranmis_belge.jpg",
    input_format="image",
    output_format="pdf",
    ocr_language="tur+eng"
)

print(f"✅ Dönüştürüldü: {result.output_file}")
print(f"📊 OCR Güveni: {result.metadata['ocr_confidence']:.1f}%")
```

**Başarılar!** 🚀
