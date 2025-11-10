# Format Desteği Test Dosyası

## 🎯 Test 1: Temel Inline Formatlar

**Kalın metin** ile başlıyoruz.

*İtalik metin* de önemli.

~~Yanlış bilgi~~ düzeltildi.

<u>Altı çizili önemli nokta</u>

## 🧪 Test 2: Bilimsel Notasyon

### Kimya Formülleri:
- Su molekülü: H<sub>2</sub>O
- Karbondioksit: CO<sub>2</sub>
- Sülfürik asit: H<sub>2</sub>SO<sub>4</sub>

### Matematik İfadeleri:
- Einstein: E=mc<sup>2</sup>
- Üs alma: x<sup>2</sup> + y<sup>2</sup> = z<sup>2</sup>
- İndis: a<sub>1</sub>, a<sub>2</sub>, a<sub>n</sub>

## 🎨 Test 3: Kombine Formatlar

1. **_Kalın ve italik birlikte_**
2. **~~Kalın ve çizili~~**
3. <u>**Altı çizili ve kalın**</u>
4. <u>*Altı çizili ve italik*</u>

## 💻 Test 4: Kod ve Teknik İçerik

Inline kod örneği: `print("Merhaba Dünya")`

Kod bloğu:
```python
def test_function():
    # Bu bir test fonksiyonu
    return "Test başarılı"
```

## 📋 Test 5: Listeler ve Formatlar

### Sıralı Liste:
1. **İlk madde** (kalın)
2. *İkinci madde* (italik)
3. ~~Üçüncü madde~~ (çizili)
4. <u>Dördüncü madde</u> (altı çizili)

### Sırasız Liste:
- Normal metin
- **Kalın metin**
- *İtalik metin*
- `Kod metni`

## 🔬 Test 6: Karmaşık Bilimsel İçerik

### Fizik:
- Planck sabiti: h = 6.626 × 10<sup>-34</sup> J·s
- Elektron konfigürasyonu: 1s<sup>2</sup> 2s<sup>2</sup> 2p<sup>6</sup>

### Matematik:
- İntegral: ∫<sub>a</sub><sup>b</sup> f(x)dx
- Limit: lim<sub>x→∞</sub> (1 + 1/x)<sup>x</sup> = e

## 📝 Test 7: Gerçek Dünya Örneği

### Akademik Yazı:
Bu çalışmada **önemli bulgular** elde ettik. Önceki çalışmalar<sup>1,2,3</sup> göstermiştir ki H<sub>2</sub>O molekülünün yapısı çok önemlidir.

~~İlk hipotezimiz yanlıştı~~ ancak düzeltilmiş modelimiz E=mc<sup>2</sup> denklemine dayanmaktadır.

<u>Not:</u> Tüm ölçümler ±0.01 hassasiyetle yapılmıştır.

### Programlama Notu:
Array indexing genellikle a<sub>i</sub> şeklinde gösterilir, burada `i` index değeridir. Örneğin:
- a<sub>0</sub> = ilk eleman
- a<sub>1</sub> = ikinci eleman
- a<sub>n-1</sub> = son eleman

## 📊 Test 8: Tablo ile Formatlar

| Özellik | Durum | Açıklama |
|---------|-------|----------|
| **Kalın** | ✅ | Çalışıyor |
| *İtalik* | ✅ | Çalışıyor |
| ~~Çizili~~ | ✅ | Çalışıyor |
| <u>Altı çizili</u> | ✅ | Çalışıyor |
| x<sup>2</sup> | ✅ | Çalışıyor |
| H<sub>2</sub>O | ✅ | Çalışıyor |

## 🎓 Test 9: Alıntı ve Referanslar

> **Önemli Not:** Bu sistem ~~eski formatları~~ desteklemez.
> 
> Yeni formatlar şunlardır:
> - Üst simge: x<sup>n</sup>
> - Alt simge: x<sub>n</sub>
> - <u>Altı çizili metin</u>

## ⚡ Test 10: Çok Katmanlı Format

***Üç yıldız*** = kalın + italik

Karmaşık örnek: <u>**_E=mc<sup>2</sup> formülü_**</u> çok önemlidir.

Kimya + Format: **H<sub>2</sub>SO<sub>4</sub>** sülfürik asittir.

---

## ✨ Test Sonucu Beklentisi

Bu dosya şunları test eder:
1. ✅ Bold (`**text**`)
2. ✅ Italic (`*text*`)
3. ✅ Strikethrough (`~~text~~`)
4. ✅ Underline (`<u>text</u>`)
5. ✅ Superscript (`<sup>text</sup>`)
6. ✅ Subscript (`<sub>text</sub>`)
7. ✅ Code (`\`code\``)
8. ✅ Kombine formatlar
9. ✅ Tablolar içinde formatlar
10. ✅ Listeler içinde formatlar

**Beklenen Çıktı:** Tüm formatlar hem PDF'de hem DOCX'te doğru görünmeli!
