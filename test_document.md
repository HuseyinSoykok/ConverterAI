# ConverterAI Test Belgesi

Bu belge, **ConverterAI** sisteminin dönüşüm kalitesini test etmek için oluşturulmuştur.

## Özellikler

ConverterAI aşağıdaki özelliklere sahiptir:

1. **PDF Dönüşümü**: PDF dosyalarını diğer formatlara dönüştürme
2. **DOCX Desteği**: Word belgelerini işleme
3. **Markdown İşleme**: Markdown formatını destekleme
4. **HTML Dönüştürücü**: HTML belgelerini işleme

### AI Kalite Kontrolü

Sistem üç farklı AI yöntemi sunar:

- **Heuristic**: Kural tabanlı kalite kontrolü
- **Transformers**: Ücretsiz, semantik benzerlik analizi (API key gerektirmez)
- **Ollama**: Yerel LLM entegrasyonu

## Kod Örneği

```python
from converters import UniversalConverter

converter = UniversalConverter()
result = converter.convert(
    input_file="document.pdf",
    output_file="document.docx",
    quality_check=True
)
```

## Tablo Örneği

| Format | Giriş | Çıkış |
|--------|-------|-------|
| PDF    | ✓     | ✓     |
| DOCX   | ✓     | ✓     |
| MD     | ✓     | ✓     |
| HTML   | ✓     | ✓     |

## Sonuç

ConverterAI, **ücretsiz AI destekli** belge dönüşümü için mükemmel bir çözümdür!
