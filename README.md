# Turkish Lawyer Verification & Search

Türkiye Barolar Birliği veritabanında avukat doğrulama ve arama modülü.

## Özellikler

- ✅ **Python Modülü**: Hem CLI hem de Python kodu olarak kullanılabilir
- ✅ **Hızlı**: ~11 saniye içinde sonuç
- ✅ **Ücretsiz**: API key gerektirmez
- ✅ **Cloudflare Bypass**: Otomatik Turnstile geçişi
- ✅ **İki Mod**: Doğrulama (verify) ve Arama (search)
- ✅ **Gizli Çalışma**: Tarayıcı penceresi görünmez
- ✅ **Temiz Çıktı**: DEBUG/WARNING mesajları yok

## Kurulum

```bash
# Gerekli paketleri yükle
uv add browser-use playwright

# Playwright Chromium'u kur
uv run python -m playwright install chromium
```

## Kullanım

### 1. Python Modülü Olarak

Python kodunuzda import ederek kullanabilirsiniz:

```python
import asyncio
from verify_lawyer import search_lawyers, verify_lawyer

# Örnek 1: Tek avukat doğrulama
async def verify_example():
    result = await verify_lawyer(
        name="MEHMET",
        surname="YILMAZ",
        sicil="12345",
        baro_id="34"
    )

    if result['exists']:
        print(f"✅ Bulundu: {result['ad']} {result['soyad']}")
        print(f"Baro: {result['baro']}")
        print(f"Sicil: {result['sicil']}")
    else:
        print("❌ Bulunamadı")

    return result

# Örnek 2: Birden fazla avukat arama
async def search_example():
    results = await search_lawyers(
        name="MEHMET",
        baro_id="34",
        verbose=False  # İlerleme mesajlarını kapat
    )

    print(f"Toplam {results['count']} avukat bulundu")

    for lawyer in results['results']:
        print(f"- {lawyer['ad']} {lawyer['soyad']} (Sicil: {lawyer['sicil']})")

    return results

# Çalıştırma
if __name__ == "__main__":
    # Doğrulama örneği
    result = asyncio.run(verify_example())

    # Arama örneği
    results = asyncio.run(search_example())
```

**Fonksiyon Parametreleri:**

```python
# verify_lawyer() - Tek avukat doğrulama
await verify_lawyer(
    name: str,              # Ad (zorunlu)
    sicil: str = None,      # Sicil numarası (opsiyonel)
    surname: str = None,    # Soyad (opsiyonel)
    baro_id: str = "34",    # Baro ID (default: İstanbul)
    tip: str = "Avukat",    # "Avukat" veya "Stajyer"
    verbose: bool = True    # İlerleme mesajlarını göster
)
# Dönüş: {'exists': True/False, 'ad': str, 'soyad': str, 'baro': str, 'sicil': str}

# search_lawyers() - Çoklu arama
await search_lawyers(
    name: str = None,       # Ad (opsiyonel)
    sicil: str = None,      # Sicil numarası (opsiyonel)
    surname: str = None,    # Soyad (opsiyonel)
    baro_id: str = "0",     # Baro ID (default: tüm barolar)
    tip: str = "Avukat",    # "Avukat" veya "Stajyer"
    verbose: bool = True    # İlerleme mesajlarını göster
)
# Dönüş: {'count': int, 'results': [{'ad': str, 'soyad': str, 'baro': str, 'sicil': str}, ...]}
```

### 2. CLI Olarak

Terminal'den direkt kullanabilirsiniz:

#### Doğrulama Modu (Verify)
Belirli bir avukatın var olup olmadığını kontrol eder.

```bash
# Temel kullanım (wrapper script - temiz çıktı)
uv run python verify-lawyer "MEHMET ALİ" -s 12345

# Ad ve soyad ayrı
uv run python verify-lawyer "MEHMET" -l "YILMAZ" -s 12345

# Farklı baro (İstanbul=34, Ankara=6, İzmir=35)
uv run python verify-lawyer "AHMET" -b 6

# Stajyer avukat
uv run python verify-lawyer "ZEYNEP" -t stajyer

# Alternatif: Direkt modül çağrısı
uv run python -m verify_lawyer.cli "MEHMET" -l "YILMAZ"
```

#### Arama Modu (Search)
Kriterlere uyan tüm avukatları listeler.

```bash
# İsimle arama (tüm barolar)
uv run python verify-lawyer "MEHMET" --search -b 0

# Belirli baroda arama
uv run python verify-lawyer "MEHMET" --search -b 34

# Soyisimle arama
uv run python verify-lawyer "YILMAZ" --search -b 34

# Sicil numarası ile arama
uv run python verify-lawyer --search -s 12345 -b 34
```

## Parametreler

| Parametre | Kısaltma | Açıklama | Default |
|-----------|----------|----------|---------|
| `name` | - | Avukat adı (opsiyonel search modunda) | - |
| `--sicil` | `-s` | Sicil numarası | - |
| `--lastname` | `-l` | Soyisim | - |
| `--baro` | `-b` | Baro ID (0=tümü, 34=İstanbul, 6=Ankara, 35=İzmir) | 34 |
| `--type` | `-t` | Tip: `avukat` veya `stajyer` | avukat |
| `--search` | - | Arama modu (tüm sonuçları göster) | False |
| `verbose` | - | İlerleme mesajlarını göster (sadece Python API) | True |

## Örnek Çıktılar

### Doğrulama Modu (CLI)
```bash
$ uv run python verify-lawyer "MEHMET" -s 12345 -l "YILMAZ"
✅ VAR
   MEHMET YILMAZ
   İstanbul Barosu - 12345
```

```bash
$ uv run python verify-lawyer "ALİ" -s 99999
❌ YOK
```

### Arama Modu (CLI)
```bash
$ uv run python verify-lawyer "MEHMET" --search -b 34
✅ 42 sonuç bulundu:

1. MEHMET YILMAZ
   İstanbul Barosu - Sicil: 12345

2. MEHMET KAYA
   İstanbul Barosu - Sicil: 23456

3. MEHMET ALİ DEMİR
   İstanbul Barosu - Sicil: 34567

...
```

### Python Modülü (Kod)
```python
# Doğrulama örneği
result = await verify_lawyer("MEHMET", surname="YILMAZ", sicil="12345")
if result['exists']:
    print(f"{result['ad']} {result['soyad']} - {result['sicil']}")

# Arama örneği
results = await search_lawyers(name="MEHMET", baro_id="34")
for lawyer in results['results'][:3]:
    print(f"{lawyer['ad']} {lawyer['soyad']}")
```


## Çıkış Kodları (CLI)

- `0` - Başarılı (avukat bulundu veya arama sonuçları var)
- `1` - Başarısız (avukat bulunamadı veya sonuç yok)

## Teknik Detaylar

### Cloudflare Turnstile Bypass
- `headless=False` - Gerçek tarayıcı gibi görünür
- Pencere ekran dışına konumlandırılır (görünmez)
- 5 saniye bekleme ile otomatik geçiş
- Manuel müdahale gerekmez

### Performans
- **Başlatma**: ~5 saniye (Cloudflare Turnstile)
- **Form işleme**: ~3 saniye
- **Veri çekme**: ~3 saniye
- **Toplam**: ~11 saniye

### Mimari
```
verify_lawyer/
├── __init__.py      # Module exports
├── core.py          # Core functions (search_lawyers, verify_lawyer)
└── cli.py           # Command-line interface
```

## Baro ID Listesi

| ID | Baro Adı |
|----|----------|
| 0 | Tüm Barolar |
| 6 | Ankara |
| 34 | İstanbul |
| 35 | İzmir |
| 7 | Antalya |
| 16 | Bursa |
| ... | Diğer barolar |

## Lisans

MIT
