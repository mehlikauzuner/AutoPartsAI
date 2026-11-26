# AutoPartsAI

AutoPartsAI, araç ruhsatı görsellerinden araç bilgilerini okuyup parça talebi sürecine temel oluşturmayı amaçlayan bir Python/FastAPI prototipidir.

## Mevcut özellikler

- Ruhsat görselinden OCR ile VIN, marka, model, model yılı, motor hacmi ve yakıt türünü çıkarmayı dener.
- Sohbet arayüzü: `/chat`
- API belgeleri ve deneme sayfası: `/docs`
- Sağlık kontrolü: `/health`
- Araç ve parça talebi verilerini doğrulayan API uç noktaları

Araç ve parça talepleri şu an veritabanına kaydedilmiyor. Parça kataloğu, fiyat ve depo entegrasyonları henüz uygulanmadı. OCR sonuçlarını kullanmadan önce kontrol edin; örnek ruhsat görselindeki VIN test amaçlıdır.

## Gereksinimler

- Python 3
- Tesseract OCR
- Tesseract Türkçe dil verisi (`tur`)

### macOS

Homebrew ile Tesseract ve ek dil verilerini kurun:

```bash
brew install tesseract tesseract-lang
```

Tesseract’ın çalıştığını ve Türkçe verisinin kurulduğunu kontrol edin:

```bash
tesseract --version
tesseract --list-langs
```

Listede `tur` görünmelidir. Homebrew’un temel Tesseract paketi İngilizce ve yön verisi içerir; Türkçe gibi ek diller `tesseract-lang` paketiyle gelir. [Tesseract paketi](https://formulae.brew.sh/formula/tesseract) · [Ek dil verileri](https://formulae.brew.sh/formula/tesseract-lang)

### Windows

1. [Tesseract kurulum belgelerindeki Windows yönergelerini](https://tesseract-ocr.github.io/tessdoc/Installation.html) izleyerek Tesseract’ı yükleyin. Kurulumdan sonra `tesseract.exe` yolu genellikle `C:\Program Files\Tesseract-OCR\tesseract.exe` olur.
2. Türkçe eğitim verisi kurulumda yoksa [Tesseract dil dosyalarından](https://tesseract-ocr.github.io/tessdoc/Data-Files.html) `tur.traineddata` dosyasını indirin ve Tesseract’ın `tessdata` klasörüne koyun. Kurulum yolu genellikle `C:\Program Files\Tesseract-OCR\tessdata` olur.
3. PowerShell’i yeniden açın ve doğrulayın:

```powershell
tesseract --version
tesseract --list-langs
```

Listede `tur` görünmelidir. Kurulum klasörü PATH içinde değilse aşağıdaki Tesseract yol ayarını yapın.

## Python ortamını kurma

Terminali/PowerShell’i `requirements.txt` dosyasının bulunduğu `AutoPartsAI` proje klasöründe açın.

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

PowerShell sanal ortamı etkinleştirmeyi engellerse Komut İstemi’ni açıp şunu kullanabilirsiniz:

```bat
.venv\Scripts\activate.bat
```

## Tesseract yolunu ayarlama (gerekirse)

Terminalde `tesseract --version` çalışıyorsa ve Tesseract PATH içindeyse `.env` dosyası gerekmez.

Tesseract PATH içinde değilse `.env.example` dosyasını `.env` adıyla kopyalayın ve işletim sisteminize uygun `TESSERACT_CMD` satırının başındaki `#` işaretini kaldırın. Gerekirse yolu kendi kurulumunuza göre değiştirin.

macOS’ta Tesseract yolunu görmek için:

```bash
which tesseract
```

`.env` dosyası proje kökünde, yani `requirements.txt` ile aynı klasörde olmalıdır.

## Uygulamayı başlatma

Sanal ortam etkinken proje klasöründe çalıştırın:

```bash
uvicorn src.api.main:app --reload
```

Tarayıcıda şu adresleri açın:

- Sohbet arayüzü: <http://127.0.0.1:8000/chat>
- API belgeleri: <http://127.0.0.1:8000/docs>
- Sağlık kontrolü: <http://127.0.0.1:8000/health>

Sohbet ekranında **Görsel seç** düğmesine basın, ruhsat görselini seçin ve **Gönder**’e tıklayın. Okunan araç bilgileri sohbet içinde görünür. Alanlardan biri okunamazsa daha net ve düz bir fotoğraf deneyin; dönen bilgileri kontrol edin.

Sunucuyu durdurmak için terminalde `Ctrl+C` tuşlarına basın.

## API uç noktaları

| Yöntem | Adres | Açıklama |
| --- | --- | --- |
| `GET` | `/` | API durum mesajı |
| `GET` | `/health` | Sağlık kontrolü |
| `GET` | `/chat` | Sohbet arayüzü |
| `POST` | `/vehicles` | Araç bilgisini doğrular ve geri döndürür |
| `POST` | `/part-requests` | Parça talebini doğrular ve geri döndürür |
| `POST` | `/vehicles/upload-registration` | Ruhsat görselini OCR ile işler |

Ayrıntılı istek ve yanıt örnekleri `/docs` sayfasındadır.

## Testleri çalıştırma

Sanal ortam etkinken:

**macOS:**

```bash
python3 -m pytest
```

**Windows PowerShell:**

```powershell
python -m pytest
```

## Proje yapısı

```text
config/                  Uygulama yapılandırması
src/api/                 FastAPI uç noktaları ve sohbet arayüzü
src/models/              Araç ve parça talebi veri modelleri
src/vehicle_detection/   OCR ve ruhsat alanı ayrıştırma
src/parts_lookup/        Parça arama modülü (henüz uygulanmadı)
src/pricing/             Fiyat modülü (henüz uygulanmadı)
src/cross_reference/     Muadil parça modülü (henüz uygulanmadı)
src/warehouse/           Depo modülü (henüz uygulanmadı)
data/                    Örnek görseller
tests/                   API ve model testleri
```
