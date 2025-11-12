# Tesseract OCR Kurulum Kontrolu
# Windows PowerShell

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " TESSERACT OCR KURULUM KONTROL" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Dosya kontrolu
Write-Host "[1/5] Tesseract dosyalari kontrol ediliyor..." -ForegroundColor Yellow
$tesseractPath = "C:\Program Files\Tesseract-OCR\tesseract.exe"

if (Test-Path $tesseractPath) {
    Write-Host "  OK - Tesseract kurulu: $tesseractPath" -ForegroundColor Green
} else {
    Write-Host "  HATA - Tesseract bulunamadi!" -ForegroundColor Red
    Write-Host "  Lutfen once Tesseract'i kurun:" -ForegroundColor Yellow
    Write-Host "  https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Gray
    Read-Host "`nCikmak icin Enter'a basin"
    exit 1
}

# 2. PATH kontrolu
Write-Host "`n[2/5] PATH degiskeni kontrol ediliyor..." -ForegroundColor Yellow
$pathContainsTesseract = $env:Path -split ';' | Where-Object { $_ -like "*Tesseract*" }

if ($pathContainsTesseract) {
    Write-Host "  OK - Tesseract PATH'te: $pathContainsTesseract" -ForegroundColor Green
} else {
    Write-Host "  UYARI - Tesseract PATH'te degil" -ForegroundColor Yellow
    Write-Host "  Gecici olarak ekleniyor..." -ForegroundColor Gray
    $env:Path += ";C:\Program Files\Tesseract-OCR"
}

# 3. Versiyon kontrolu
Write-Host "`n[3/5] Tesseract versiyonu kontrol ediliyor..." -ForegroundColor Yellow

try {
    $version = & tesseract --version 2>&1 | Select-String "tesseract" | Select-Object -First 1
    Write-Host "  OK - $version" -ForegroundColor Green
} catch {
    Write-Host "  HATA - Tesseract calistirilamadi" -ForegroundColor Red
    Write-Host "  PowerShell'i yeniden baslatip tekrar deneyin" -ForegroundColor Yellow
}

# 4. Dil paketleri kontrolu
Write-Host "`n[4/5] Dil paketleri kontrol ediliyor..." -ForegroundColor Yellow

try {
    $langs = & tesseract --list-langs 2>&1 | Out-String
    
    if ($langs -match "tur") {
        Write-Host "  OK - Turkce dil paketi kurulu" -ForegroundColor Green
    } else {
        Write-Host "  HATA - Turkce dil paketi eksik!" -ForegroundColor Red
        Write-Host "  Tesseract'i kaldirip 'Turkish' secenegiyle yeniden kurun" -ForegroundColor Yellow
    }
    
    if ($langs -match "eng") {
        Write-Host "  OK - Ingilizce dil paketi kurulu" -ForegroundColor Green
    } else {
        Write-Host "  UYARI - Ingilizce dil paketi eksik" -ForegroundColor Yellow
    }
    
    Write-Host "`n  Kurulu tum diller:" -ForegroundColor Gray
    $langs -split "`n" | Where-Object { $_ -match "^[a-z]{3}$" } | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
    
} catch {
    Write-Host "  HATA - Dil paketi listesi alinamadi" -ForegroundColor Red
}

# 5. Python entegrasyon kontrolu
Write-Host "`n[5/5] Python entegrasyonu kontrol ediliyor..." -ForegroundColor Yellow

$pythonPath = "D:\Projects\Python\ConverterAI\.venv\Scripts\python.exe"

if (Test-Path $pythonPath) {
    try {
        $testCode = @"
try:
    from ai.ocr_engine import OCREngine
    engine = OCREngine()
    print('OK')
except Exception as e:
    print(f'HATA: {e}')
"@
        
        $result = & $pythonPath -c $testCode 2>&1
        
        if ($result -match "OK") {
            Write-Host "  OK - Python OCR Engine hazir!" -ForegroundColor Green
        } else {
            Write-Host "  UYARI - Python OCR Engine testi basarisiz" -ForegroundColor Yellow
            Write-Host "  Hata: $result" -ForegroundColor Gray
        }
    } catch {
        Write-Host "  UYARI - Python testi yapilamadi" -ForegroundColor Yellow
    }
} else {
    Write-Host "  UYARI - Python sanal ortami bulunamadi" -ForegroundColor Yellow
}

# Sonuc
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host " KURULUM DURUMU" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if ((Test-Path $tesseractPath) -and ($langs -match "tur") -and ($langs -match "eng")) {
    Write-Host ""
    Write-Host "  BASARILI! Tesseract tamamen kurulu." -ForegroundColor Green
    Write-Host ""
    Write-Host "  Simdi deneyebilirsiniz:" -ForegroundColor Yellow
    Write-Host "  1. cd D:\Projects\Python\ConverterAI" -ForegroundColor Gray
    Write-Host "  2. .\.venv\Scripts\activate" -ForegroundColor Gray
    Write-Host "  3. python demo_image_converter.py" -ForegroundColor Gray
    Write-Host "  4. python test_image_converter.py" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "  EKSIK! Lutfen kurulumu tamamlayin." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Adimlar:" -ForegroundColor Yellow
    Write-Host "  1. Tesseract'i indirin ve kurun" -ForegroundColor Gray
    Write-Host "  2. Kurulumda 'Turkish' dil paketini secin" -ForegroundColor Gray
    Write-Host "  3. 'Add to PATH' seçeneğini isaretleyin" -ForegroundColor Gray
    Write-Host "  4. PowerShell'i yeniden baslatın" -ForegroundColor Gray
    Write-Host "  5. Bu scripti tekrar calistirin" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Detayli rehber: TESSERACT_SETUP.md" -ForegroundColor Cyan
Write-Host ""

Read-Host "Cikmak icin Enter'a basin"
