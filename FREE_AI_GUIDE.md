# 🆓 Ücretsiz AI Kalite Kontrolü Rehberi

## 🎯 Genel Bakış

ConverterAI'da **3 ücretsiz kalite kontrol yöntemi** bulunmaktadır:

1. **Heuristic (Sezgisel)** - ✅ Her zaman kullanılabilir, API key gerektirmez
2. **Transformers** - ✅ Ücretsiz, güçlü, local AI
3. **Ollama** - ✅ Ücretsiz, GPT benzeri, en güçlü

## 📊 Yöntem Karşılaştırması

| Özellik | Heuristic | Transformers | Ollama | OpenAI/Anthropic |
|---------|-----------|--------------|--------|------------------|
| **Maliyet** | ✅ Ücretsiz | ✅ Ücretsiz | ✅ Ücretsiz | ❌ Ücretli |
| **API Key Gerekli** | ❌ Hayır | ❌ Hayır | ❌ Hayır | ✅ Evet |
| **İnternet Gerekli** | ❌ Hayır | ❌ Hayır (ilk kullanım hariç) | ❌ Hayır | ✅ Evet |
| **Kalite** | ⭐⭐⭐ İyi | ⭐⭐⭐⭐ Çok İyi | ⭐⭐⭐⭐⭐ Mükemmel | ⭐⭐⭐⭐⭐ Mükemmel |
| **Hız** | ⚡ Çok Hızlı | ⚡ Hızlı | 🐢 Yavaş | 🐢 Yavaş |
| **Disk Alanı** | 0 MB | ~400 MB | ~4 GB | 0 MB |

## 🚀 Kullanım Kılavuzu

### 1️⃣ Heuristic (Varsayılan - Her Zaman Kullanılabilir)

**Hiçbir kurulum gerekmez!** Zaten aktif.

#### Özellikler:
- ✅ Anında çalışır
- ✅ Dosya boyutu analizi
- ✅ İçerik yapısı kontrolü (başlıklar, listeler, tablolar)
- ✅ Karakter ve kelime sayısı analizi
- ✅ Format koruması kontrolü

#### Kullanım:
```python
# .env dosyasında (varsayılan)
AI_QUALITY_METHOD=heuristic
```

**Kullanıcı aksiyonu: YOK!** Zaten çalışır durumda 👍

---

### 2️⃣ Transformers (Önerilen - Ücretsiz ve Güçlü) 🌟

**En iyi ücretsiz seçenek!** Semantic similarity ile kalite ölçümü.

#### Kurulum:
```powershell
# Zaten requirements.txt'de var
pip install sentence-transformers torch
```

#### İlk Kullanım:
```powershell
# Model otomatik indirilecek (~400 MB, sadece bir kez)
# İnternet bağlantısı gerekli (sadece ilk seferde)
```

#### Özellikler:
- ✅ **Semantic similarity**: İçerik benzerliğini AI ile ölçer
- ✅ Çok dilli destek (Türkçe dahil)
- ✅ Başlık, liste, tablo koruması analizi
- ✅ Detaylı metrikler
- ✅ Offline çalışır (model indirildikten sonra)

#### Kullanım:
```powershell
# .env dosyasını düzenle
AI_QUALITY_METHOD=transformers
```

#### Python'da:
```python
from ai.local_ai_checker import LocalAIChecker

checker = LocalAIChecker(method='transformers')
result = checker.check_quality('input.pdf', 'output.docx')

print(f"Kalite: {result['score'] * 100:.1f}%")
print(f"Semantic similarity: {result['metrics']['semantic_similarity']:.2f}")
```

---

### 3️⃣ Ollama (En Güçlü - GPT Benzeri) 🏆

**Local LLM ile GPT kalitesinde analiz!** Hiçbir maliyet yok.

#### Kurulum:

1. **Ollama'yı İndirin:**
   ```
   Windows: https://ollama.ai/download/windows
   ```

2. **Model İndirin:**
   ```powershell
   # Llama 2 (önerilen, ~4 GB)
   ollama pull llama2
   
   # Veya daha hafif modeller:
   ollama pull llama2:7b-chat  # Daha hızlı
   ollama pull mistral          # Alternatif
   ollama pull phi              # En hafif (~2 GB)
   ```

3. **Python kütüphanesini yükleyin:**
   ```powershell
   pip install ollama
   ```

#### Özellikler:
- ✅ **GPT benzeri analiz** - En detaylı raporlar
- ✅ Doğal dil açıklamaları
- ✅ Akıllı öneriler
- ✅ İçerik kalitesi değerlendirmesi
- ✅ Tamamen offline

#### Kullanım:
```powershell
# .env dosyasını düzenle
AI_QUALITY_METHOD=ollama
```

#### Test Edin:
```powershell
# Ollama çalışıyor mu?
ollama list

# Model test
ollama run llama2 "Hello"
```

---

## ⚙️ Yapılandırma

### .env Dosyası:
```env
# Ücretsiz AI yöntemlerinden birini seçin
AI_QUALITY_METHOD=heuristic      # Varsayılan, her zaman çalışır
# AI_QUALITY_METHOD=transformers  # Ücretsiz, güçlü (önerilen)
# AI_QUALITY_METHOD=ollama        # Ücretsiz, en güçlü (GPT benzeri)

# Ücretli API'lar (opsiyonel, yorum satırında bırakın)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

## 💡 Öneriler

### Genel Kullanım İçin:
👉 **Transformers** kullanın
- İyi performans
- Makul hız
- Güvenilir sonuçlar

### En İyi Kalite İstiyorsanız:
👉 **Ollama** kullanın
- GPT kalitesinde
- Detaylı analiz
- Biraz yavaş ama değer

### Hız Öncelikliyse:
👉 **Heuristic** kullanın
- Anında sonuç
- Kabul edilebilir kalite
- Sıfır kurulum

## 🔄 Yöntemler Arası Geçiş

```powershell
# .env dosyasını düzenle
notepad .env

# Satırı değiştir:
AI_QUALITY_METHOD=transformers  # veya heuristic, ollama

# Uygulamayı yeniden başlat
python app.py
```

## 📈 Örnek Çıktılar

### Heuristic:
```json
{
  "score": 0.85,
  "method": "enhanced heuristic (free)",
  "metrics": {
    "length_ratio": 0.92,
    "word_count_ratio": 0.88,
    "heading_preservation": 1.0
  },
  "issues": [],
  "recommendations": ["Conversion quality is excellent!"]
}
```

### Transformers:
```json
{
  "score": 0.89,
  "method": "transformers (free)",
  "metrics": {
    "semantic_similarity": 0.92,
    "length_ratio": 0.95,
    "heading_preservation": 1.0
  },
  "issues": [],
  "recommendations": []
}
```

### Ollama:
```json
{
  "score": 0.91,
  "method": "ollama (free local LLM)",
  "issues": ["Minor formatting differences in tables"],
  "recommendations": [
    "Overall excellent conversion",
    "Check table borders in output"
  ]
}
```

## 🐛 Sorun Giderme

### Transformers Yüklenmiyor:
```powershell
# PyTorch yükleyin
pip install torch torchvision torchaudio

# Sentence transformers
pip install sentence-transformers
```

### Ollama Çalışmıyor:
```powershell
# Ollama servisini başlatın
ollama serve

# Model var mı kontrol edin
ollama list

# Yoksa indirin
ollama pull llama2
```

### "Module not found" Hatası:
```powershell
# Tüm bağımlılıkları yükleyin
pip install -r requirements.txt
```

## 🎓 Hangi Yöntemi Seçmeliyim?

### İlk Kez Kullanıyorsanız:
1. **Heuristic** ile başlayın (hiçbir kurulum yok)
2. Transformers'ı deneyin (tek komut: `pip install sentence-transformers`)
3. Beğendiyseniz Ollama'yı kurun

### Profesyonel Kullanım:
- Günlük kullanım: **Transformers**
- Kritik dönüşümler: **Ollama**
- Hızlı testler: **Heuristic**

## 💰 Maliyet Karşılaştırması

| Yöntem | Aylık Maliyet | 1000 Dönüşüm Maliyeti |
|--------|---------------|----------------------|
| Heuristic | **₺0** | **₺0** |
| Transformers | **₺0** | **₺0** |
| Ollama | **₺0** | **₺0** |
| OpenAI GPT-3.5 | ~₺200 | ~₺50 |
| OpenAI GPT-4 | ~₺1000 | ~₺250 |
| Anthropic Claude | ~₺300 | ~₺75 |

## ✅ Sonuç

**Hiçbir API key'e ihtiyacınız yok!** 

Ücretsiz yöntemler profesyonel kalitede sonuçlar verir:
- ✅ Heuristic: Her zaman hazır
- ✅ Transformers: En iyi ücretsiz seçenek
- ✅ Ollama: GPT kalitesinde, tamamen ücretsiz

---

**İyi dönüşümler!** 🚀
