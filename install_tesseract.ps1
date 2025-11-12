# Tesseract OCR Otomatik İndirme ve Kurulum Scripti
# Windows PowerShell için

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  TESSERACT OCR KURULUM YARDIMCISI" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Tesseract versiyonu ve URL
$tesseractVersion = "5.3.3.20231005"
$downloadUrl = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-$tesseractVersion.exe"
$installerPath = "$env:TEMP\tesseract-setup.exe"

Write-Host "📋 Bilgiler:" -ForegroundColor Yellow
Write-Host "   Versiyon: Tesseract OCR 5.3.3"
Write-Host "   Platform: Windows 64-bit"
Write-Host "   Dil Paketleri: Turkish + English (otomatik)"
Write-Host ""

# 1. Mevcut kurulum kontrolü
Write-Host "🔍 Mevcut Tesseract kurulumu kontrol ediliyor..." -ForegroundColor Cyan
$tesseractPath = "C:\Program Files\Tesseract-OCR\tesseract.exe"

if (Test-Path $tesseractPath) {
    Write-Host "✅ Tesseract zaten kurulu!" -ForegroundColor Green
    Write-Host "   Konum: $tesseractPath" -ForegroundColor Gray
    
    # Versiyon kontrolü
    try {
        $version = & $tesseractPath --version 2>&1 | Select-String "tesseract" | Select-Object -First 1
        Write-Host "   Versiyon: $version" -ForegroundColor Gray
        
        # Dil kontrolü
        $langs = & $tesseractPath --list-langs 2>&1 | Select-String -Pattern "tur|eng"
        Write-Host "   Kurulu diller:" -ForegroundColor Gray
        $langs | ForEach-Object { Write-Host "     - $_" -ForegroundColor Gray }
        
        $continue = Read-Host "`n⚠️ Yeniden kurmak ister misiniz? (Y/N)"
        if ($continue -ne 'Y' -and $continue -ne 'y') {
            Write-Host "✅ Kurulum iptal edildi. Mevcut kurulum korundu." -ForegroundColor Green
            Read-Host "`nÇıkmak için Enter'a basın"
            exit
        }
    } catch {
        Write-Host "⚠️ Mevcut kurulum test edilemedi." -ForegroundColor Yellow
    }
}

# 2. İndirme
Write-Host "`n📥 Tesseract indiriliyor..." -ForegroundColor Cyan
Write-Host "   URL: $downloadUrl" -ForegroundColor Gray
Write-Host "   Hedef: $installerPath" -ForegroundColor Gray

try {
    # İndirme progress bar ile
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -ErrorAction Stop
    $ProgressPreference = 'Continue'
    
    # Dosya boyutu kontrol
    $fileSize = (Get-Item $installerPath).Length / 1MB
    $fileSizeRounded = [Math]::Round($fileSize, 2)
    Write-Host "OK Indirme tamamlandi! ($fileSizeRounded MB)" -ForegroundColor Green
    
} catch {
    Write-Host "HATA Indirme basarisiz: $_" -ForegroundColor Red
    Write-Host "`n📝 Manuel indirme için:" -ForegroundColor Yellow
    Write-Host "   1. Şu linki tarayıcıda aç: https://github.com/UB-Mannheim/tesseract/wiki"
    Write-Host "   2. 'tesseract-ocr-w64-setup-5.3.x.exe' dosyasını indir"
    Write-Host "   3. İndirilen dosyayı çalıştır"
    Read-Host "`nÇıkmak için Enter'a basın"
    exit 1
}

# 3. Kurulum Talimatları
Write-Host "`n🛠️ KURULUM TALİMATLARI:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Kurulum penceresi açılacak. Lütfen şu adımları takip edin:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  'Next' butonuna tıklayın" -ForegroundColor White
Write-Host "2️⃣  'I accept the agreement' seçip Next" -ForegroundColor White
Write-Host "3️⃣  Kurulum yolunu DEĞİŞTİRMEYİN:" -ForegroundColor White
Write-Host "    C:\Program Files\Tesseract-OCR" -ForegroundColor Gray
Write-Host "4️⃣  ⚠️ ÖNEMLİ - 'Additional Language Data' ekranında:" -ForegroundColor Red
Write-Host "    ✅ Turkish (MUTLAKA İŞARETLE!)" -ForegroundColor Green
Write-Host "    ✅ English (zaten seçili)" -ForegroundColor Green
Write-Host "5️⃣  ⚠️ 'Add to PATH' seçeneğini İŞARETLE" -ForegroundColor Red
Write-Host "6️⃣  'Install' → Bekle → 'Finish'" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow

$ready = Read-Host "`n✋ Kuruluma başlamak için 'Y' yazıp Enter'a basın (iptal için N)"

if ($ready -ne 'Y' -and $ready -ne 'y') {
    Write-Host "❌ Kurulum iptal edildi." -ForegroundColor Red
    Remove-Item $installerPath -ErrorAction SilentlyContinue
    Read-Host "`nÇıkmak için Enter'a basın"
    exit
}

# 4. Kurulumu başlat
Write-Host "`n🚀 Tesseract kurulum programı başlatılıyor..." -ForegroundColor Cyan
Write-Host "⏳ Kurulum tamamlanana kadar bekleyin..." -ForegroundColor Yellow

try {
    Start-Process -FilePath $installerPath -Wait
    Write-Host "✅ Kurulum programı tamamlandı!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Kurulum programı başlatılamadı: $_" -ForegroundColor Yellow
    Write-Host "Manuel olarak şu dosyayı çalıştırın: $installerPath" -ForegroundColor Yellow
}

# 5. Kurulum Doğrulama
Write-Host "`n🔍 Kurulum doğrulanıyor..." -ForegroundColor Cyan

Start-Sleep -Seconds 2

# Tesseract yolu kontrolü
if (Test-Path $tesseractPath) {
    Write-Host "✅ Tesseract dosyaları kuruldu!" -ForegroundColor Green
    Write-Host "   Konum: $tesseractPath" -ForegroundColor Gray
} else {
    Write-Host "⚠️ Tesseract dosyaları bulunamadı!" -ForegroundColor Yellow
    Write-Host "   Beklenen konum: $tesseractPath" -ForegroundColor Gray
}

# PATH kontrolü
Write-Host "`n🔍 PATH kontrolü..." -ForegroundColor Cyan
$pathCheck = $env:Path -split ';' | Where-Object { $_ -like "*Tesseract*" }

if ($pathCheck) {
    Write-Host "✅ Tesseract PATH'e eklendi!" -ForegroundColor Green
    Write-Host "   PATH: $pathCheck" -ForegroundColor Gray
} else {
    Write-Host "⚠️ Tesseract PATH'e eklenmemiş!" -ForegroundColor Yellow
    Write-Host "   PowerShell'i yeniden başlatın veya manuel ekleyin" -ForegroundColor Yellow
}

# Tesseract komut testi
Write-Host "`n🧪 Tesseract komut testi..." -ForegroundColor Cyan

try {
    # PATH'i güncelle (geçici)
    $env:Path += ";C:\Program Files\Tesseract-OCR"
    
    $versionOutput = & tesseract --version 2>&1 | Out-String
    if ($versionOutput -match "tesseract") {
        Write-Host "✅ Tesseract çalışıyor!" -ForegroundColor Green
        $versionLine = $versionOutput -split "`n" | Select-Object -First 1
        Write-Host "   $versionLine" -ForegroundColor Gray
        
        # Dil kontrolü
        $langsOutput = & tesseract --list-langs 2>&1 | Out-String
        if ($langsOutput -match "tur" -and $langsOutput -match "eng") {
            Write-Host "✅ Türkçe ve İngilizce dil paketleri kurulu!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Dil paketleri eksik veya okunamadı!" -ForegroundColor Yellow
            Write-Host "   Tesseract'i kaldırıp Turkish seçeneği ile yeniden kurun" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️ Tesseract henüz komut satırından erişilebilir değil" -ForegroundColor Yellow
    Write-Host "   PowerShell'i yeniden başlatın ve tekrar deneyin" -ForegroundColor Yellow
}

# 6. Python Entegrasyon Talimatları
Write-Host "`n🐍 Python Entegrasyonu:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nSeçenek 1: .env dosyasına ekle (ÖNERİLEN)" -ForegroundColor Yellow
Write-Host "   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe" -ForegroundColor Gray

Write-Host "`nSeçenek 2: OCR engine koduna ekle" -ForegroundColor Yellow
Write-Host "   ai/ocr_engine.py dosyasında manuel yol belirt" -ForegroundColor Gray

# 7. Test önerileri
Write-Host "`n✅ SONRAKİ ADIMLAR:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. PowerShell'i KAPAT ve YENİDEN AÇ (PATH güncellemesi için)" -ForegroundColor White
Write-Host ""
Write-Host "2. Test komutları çalıştır:" -ForegroundColor White
Write-Host "   tesseract --version" -ForegroundColor Gray
Write-Host "   tesseract --list-langs" -ForegroundColor Gray
Write-Host ""
Write-Host "3. ConverterAI'da test et:" -ForegroundColor White
Write-Host "   cd D:\Projects\Python\ConverterAI" -ForegroundColor Gray
Write-Host "   .\.venv\Scripts\activate" -ForegroundColor Gray
Write-Host "   python demo_image_converter.py" -ForegroundColor Gray
Write-Host "   python test_image_converter.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Görsel dönüştürme dene:" -ForegroundColor White
Write-Host "   python cli.py convert scan.png --to pdf" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Green

# 8. Temizlik
Write-Host "`n🧹 İndirilen kurulum dosyası siliniyor..." -ForegroundColor Cyan
Remove-Item $installerPath -ErrorAction SilentlyContinue
Write-Host "✅ Temizlik tamamlandı!" -ForegroundColor Green

# 9. Dokümantasyon
Write-Host "`n📚 Detaylı rehber için:" -ForegroundColor Yellow
Write-Host "   TESSERACT_SETUP.md" -ForegroundColor Gray
Write-Host "   IMAGE_CONVERSION_GUIDE.md" -ForegroundColor Gray

Write-Host "`n🎉 Kurulum işlemi tamamlandı!" -ForegroundColor Green
Write-Host "   PowerShell'i yeniden başlatmayı unutmayın!" -ForegroundColor Yellow
Write-Host ""

Read-Host "Çıkmak için Enter'a basın"
