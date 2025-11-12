# 🚀 Tesseract OCR Hızlı Kurulum Rehberi

## ⚡ Özet (TL;DR)

1. **İndir**: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
2. **Kur**: Turkish + English dil paketlerini seç, "Add to PATH" işaretle
3. **Test**: `PowerShell -ExecutionPolicy Bypass -File check_tesseract.ps1`
4. **Kullan**: `python test_image_converter.py`

---

## 📋 Adım Adım Kurulum

### 1️⃣ İndirme

**Link** açıldı mı? Eğer açılmadıysa:
```powershell
Start-Process "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
```

İndirme başladı ✅  
Dosya boyutu: ~50-60 MB  
Süre: 1-2 dakika (internet hızına bağlı)

### 2️⃣ Kurulum

İndirme tamamlanınca `.exe` dosyasını çalıştır:

1. **Welcome** → `Next`
2. **License Agreement** → `I accept` → `Next`
3. **Installation Path** → `C:\Program Files\Tesseract-OCR` (DEĞİŞTİRME!) → `Next`
4. **⚠️ ÖNEMLİ - Choose Components**:
   ```
   ✅ Tesseract (zaten seçili)
   ✅ Add to PATH (MUTLAKA SEÇ!)
   ✅ Additional Language Data:
      ✅ Turkish [tur] (MUTLAKA SEÇ!)
      ✅ English [eng] (zaten seçili)
   ```
5. `Next` → `Install` → **BEKLEemek:** 30-60 saniye
6. `Finish` ✅

### 3️⃣ Doğrulama

**YENİ PowerShell penceresi** aç (PATH güncellemesi için) ve çalıştır:

```powershell
# Kurulum kontrolü
PowerShell -ExecutionPolicy Bypass -File check_tesseract.ps1
```

**Beklenen sonuç:**
```
[1/5] Tesseract dosyalari kontrol ediliyor...
  OK - Tesseract kurulu: C:\Program Files\Tesseract-OCR\tesseract.exe

[2/5] PATH degiskeni kontrol ediliyor...
  OK - Tesseract PATH'te

[3/5] Tesseract versiyonu kontrol ediliyor...
  OK - tesseract 5.3.3

[4/5] Dil paketleri kontrol ediliyor...
  OK - Turkce dil paketi kurulu
  OK - Ingilizce dil paketi kurulu

[5/5] Python entegrasyonu kontrol ediliyor...
  OK - Python OCR Engine hazir!

BASARILI! Tesseract tamamen kurulu.
```

### 4️⃣ Kullanım

**ConverterAI ile test et:**

```powershell
# Sanal ortamı aktifleştir
.\.venv\Scripts\activate

# Demo çalıştır (OCR'sız - pipeline testi)
python demo_image_converter.py

# Gerçek OCR testi (Tesseract gerekli)
python test_image_converter.py

# Görsel dönüştürme dene
python cli.py convert scan.png --to pdf
```

---

## ❌ Sorun Giderme

### Problem: "Tesseract bulunamadı"

**Çözüm 1: PATH Kontrolü**
```powershell
# PATH'te Tesseract var mı?
$env:Path -split ';' | Select-String "Tesseract"

# Yoksa manuel ekle (geçici)
$env:Path += ";C:\Program Files\Tesseract-OCR"
```

**Çözüm 2: Manuel Yol Belirtme**

`.env` dosyasına ekle:
```bash
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Problem: "Türkçe dil paketi eksik"

**Çözüm:**
- Tesseract'i kaldır (Programs & Features)
- Yeniden kur
- Kurulumda **"Turkish"** seçeneğini MUTLAKA işaretle

### Problem: Python'da "tesseract is not installed"

**Çözüm:**
```powershell
# PowerShell'i YENİDEN BAŞLAT
# Kurulum sonrası PATH güncellemesi için gerekli
```

---

## ✅ Test Çıktıları

### Başarılı Kurulum:
```powershell
PS> tesseract --version
tesseract 5.3.3

PS> tesseract --list-langs
List of available languages:
eng
osd
tur

PS> python -c "from ai.ocr_engine import OCREngine; print('OK')"
OK
```

### Python ile OCR Testi:
```python
from ai.ocr_engine import OCREngine

engine = OCREngine(language='tur+eng')
result = engine.extract_text_from_image('test_image.png')

print(f"Başarılı: {result['success']}")
print(f"Güven: {result['confidence']:.1f}%")
print(f"Metin:\n{result['text']}")
```

---

## 📊 Performans Beklentileri

| Görsel Tipi | OCR Doğruluğu | Süre |
|-------------|---------------|------|
| Temiz metin (300 DPI) | 90-95% | 1-3s |
| Taranmış belge | 80-90% | 2-5s |
| Ekran görüntüsü | 85-95% | 1-2s |
| El yazısı (temiz) | 60-75% | 2-4s |

---

## 🎯 Sonraki Adımlar

### Test Dönüşümleri:
```powershell
# Image → Markdown
python cli.py convert scan.png --to markdown

# Image → PDF (Türkçe karakter desteği ile)
python cli.py convert document.jpg --to pdf

# Image → DOCX
python cli.py convert notes.jpeg --to docx

# Image → HTML
python cli.py convert screenshot.png --to html
```

### Web Arayüzü:
```powershell
python app.py
# Tarayıcıda aç: http://127.0.0.1:5000
# Image dosyası yükle ve dönüştür
```

---

## 📚 Kaynaklar

- **Tesseract Dokümantasyonu**: https://tesseract-ocr.github.io/
- **ConverterAI Rehberi**: `IMAGE_CONVERSION_GUIDE.md`
- **Detaylı Kurulum**: `TESSERACT_SETUP.md`
- **GitHub**: https://github.com/tesseract-ocr/tesseract

---

## 💡 İpuçları

1. **Yüksek Kalite**: 300 DPI veya üzeri görsel kullan
2. **Kontrast**: Siyah metin + beyaz arka plan en iyisi
3. **Dil Seçimi**: `tur+eng` hem Türkçe hem İngilizce için
4. **Güven Skoru**: %75+ iyi sayılır, %90+ mükemmel
5. **Hızlı Test**: `check_tesseract.ps1` ile her zaman kontrol et

---

**🎉 Kurulum başarılı olursa, gerçek zamanlı OCR dönüşümleri yapmaya hazırsınız!**
