# RoadSense AI — Azure Ingestion Rehberi

## Hiç Azure bilmeyenler için, her adım tıklama tıklama anlatıldı

---

## Önce Şunu Anlayalım: Azure Ne İşimize Yarıyor?

Şu an bilgisayarında `data/raw/` klasöründe 7.000 satır veri var.
Ama bu veri sadece senin bilgisayarında — kimse dışarıdan ulaşamıyor.

**RoadSense AI'nın amacı şu:** Biri bir poliçe PDF'i yüklediğinde, sistem otomatik olarak:

1. PDF'i açıp metni çıkarır
2. Kişisel bilgileri maskeler (ad, telefon vs.)
3. Metni küçük parçalara böler
4. Parçaları "arama motoruna" yükler
5. Artık bir kullanıcı soru sorduğunda sistem o parçaları bulabilir

Bunun **otomatik ve 7/24 çalışması** için Azure'a ihtiyacımız var.

---

## Temel Kavramlar — Çok Basit Anlatım

### Azure nedir?

Microsoft'un sahip olduğu devasa bilgisayar odaları. Sen oraya para ödersin,
o sana bilgisayar, depolama alanı, program çalıştırma hizmeti verir.
Sanki kendi sunucunu kuruyorsun ama aslında Microsoft'un sunucusunu kiralıyorsun.

### Azure Portal nedir?

`portal.azure.com` — tüm Azure'u web tarayıcından yönetebildiğin sayfa.
Tıkla, ayarla, kontrol et. Kod yazmak zorunda değilsin.

### Blob Storage nedir?

Azure'daki **dosya dolabı**. PDF, Word, resim, JSON — her türlü dosyayı koyarsın.
İçinde "container" açarsın — bunlar da dosya dolabının çekmeceleri gibi.

### Azure Functions nedir?

Sürekli çalışmayan, **sadece iş geldiğinde uyanan program**.
"raw-documents klasörüne yeni dosya düştüğünde uyan ve işlemi başlat" diyorsun.
Dosya gelmezse uyuyor, para ödemiyorsun.

### Durable Functions nedir?

Normal Functions tek iş yapar. Bizim işimiz 4 adım: parse → maskele → parçala → yükle.
Durable Functions bu 4 adımı **sırayla ve güvenli şekilde** yönetir.
3. adımda hata olursa başa dönmez, kaldığı yerden devam eder.

---

## Büyük Resim — RoadSense AI'da Ne Oluyor?

```
1. Sen bir PDF yüklüyorsun  →  Blob Storage'a düşüyor
                                      ↓
2. Azure "Yeni dosya var!" diye alarm çalıyor  (Blob Trigger)
                                      ↓
3. Function uyuyor: "Tamam, orchestrator'ı başlatıyorum"
                                      ↓
4. Orchestrator 4 adımı sırayla çalıştırıyor:
   ├── Adım 1: parse_pdf     →  PDF'den metni çıkar
   ├── Adım 2: pii_mask      →  "Ali Veli, 0412..." → "[KİŞİ], [TELEFON]..."
   ├── Adım 3: chunk_embed   →  Büyük metni küçük parçalara böl + vektöre çevir
   └── Adım 4: index_search  →  Parçaları arama motoruna yükle
                                      ↓
5. RAG sistemi artık bu parçaları bulabilir
```

---

## ADIM 1 — Azure Hesabı Aç (Ücretsiz)

**1.1** Tarayıcında şu adrese git:

```
https://azure.microsoft.com/free
```

**1.2** Sayfada büyük yeşil **"Start free"** butonuna tıkla.

**1.3** Microsoft hesabınla giriş yap.

- Microsoft hesabın yoksa **"Create one!"** linkine tıkla, yeni hesap aç.
- Gmail, Outlook, herhangi bir e-posta ile hesap açabilirsin.

**1.4** Kredi kartı bilgilerini gir.

- **Endişelenme:** İlk 12 ay $200 ücretsiz kredi var. Bu proje bu kredinin çok
  küçük bir kısmını kullanır. Kredi bitmeden ücret kesilmez.
- Kart sadece kimlik doğrulama için isteniyor.

**1.5** "Sign up" butonuna tıkla ve bekle (1-2 dakika sürer).

**1.6** Onaylandıktan sonra şu adrese otomatik gideceksin:

```
https://portal.azure.com
```

Bu sayfa senin **Azure ana sayfan**. Her şeyi buradan yöneteceksin.

---

## ADIM 2 — Azure CLI Kur (Terminaldeki Araç)

Azure Portal'da her şeyi tıklayarak yapabilirsin. Ama bazı adımları terminalde
yapmak çok daha hızlı. Bu yüzden bir araç kuracağız.

**2.1** Mac'inde terminali aç (Spotlight'ta "Terminal" yaz).

**2.2** Şu komutu yapıştır ve Enter'a bas:

```bash
brew install azure-cli
```

(Homebrew yoksa önce `https://brew.sh` adresinden kur — bir komutla kuruluyor)

**2.3** Kurulum bitince giriş yap:

```bash
az login
```

**2.4** Tarayıcı açılır, Azure hesabınla giriş yap.

**2.5** Başarılı olursa terminal şunu gösterir:

```json
[
  {
    "name": "Azure subscription 1",
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
]
```

Bu `id` değerini bir kenara yaz — Subscription ID, sonra lazım olabilir.

---

## ADIM 3 — Resource Group Oluştur

### Resource Group nedir?

Düşün ki Azure bir IKEA mağazası gibi. Satın aldığın her şeyi (masa, sandalye,
raf) bir "oda" ile etiketliyorsun. Projeyi bitirince o odayı toptan siliyorsun —
tek tek uğraşmıyorsun. Resource Group tam olarak bu.

---

**3.1** `portal.azure.com`'da sol üstteki **☰ (hamburger menü)** ikonuna tıkla.

**3.2** Listeden **"Resource groups"** seç.

**3.3** Sayfanın üstünde **"+ Create"** butonuna tıkla.

**3.4** Açılan formda şunları doldur:

| Alan | Değer |
|------|-------|
| Subscription | Azure subscription 1 (otomatik gelir) |
| Resource group name | `roadsense-dev` |
| Region | **Australia East** |

> **Neden Australia East?** RACV Melbourne'da. Verileri kullanıcıya yakın tutmak
> hem sistemi hızlandırır, hem de mülakaatta bunu söyleyebilirsin.

**3.5** Alttaki **"Review + create"** butonuna tıkla.

**3.6** Bir sonraki sayfada **"Create"** butonuna tıkla.

**3.7** 10-15 saniye sonra "roadsense-dev" resource group hazır.

---

## ADIM 4 — Storage Account ve Container Oluştur

### Storage Account nedir?

Azure'daki ana dosya dolabın. İçinde "container" açarsın — bunlar çekmeceler.
Biz `raw-documents` adında bir çekmece kullanacağız. Oraya PDF yüklenince
sistem otomatik uyanacak.

---

### Storage Account Oluştur

**4.1** `portal.azure.com`'da üst arama çubuğuna yaz: `Storage accounts`

**4.2** Çıkan seçeneğe tıkla.

**4.3** **"+ Create"** butonuna tıkla.

**4.4** Formu şöyle doldur:

| Alan | Değer |
|------|-------|
| Subscription | Azure subscription 1 |
| Resource group | `roadsense-dev` |
| Storage account name | `roadsensedevst` (küçük harf, özel karakter yok) |
| Region | Australia East |
| Performance | Standard |
| Redundancy | LRS (Locally-redundant storage) |

**4.5** **"Review + create"** → **"Create"** butonlarına sırayla tıkla.

**4.6** "Deployment is complete" mesajı gelince **"Go to resource"** tıkla.

---

### Container Oluştur

**4.7** Sol menüde **"Data storage"** başlığının altında **"Containers"** tıkla.

**4.8** **"+ Container"** butonuna tıkla.

**4.9** Sağdan açılan panelde şunları gir:

- Name: `raw-documents`
- Public access level: **Private (no anonymous access)**

**4.10** **"Create"** butonuna tıkla.

Artık `raw-documents` klasörün var. Buraya dosya atınca sistem uyanacak.

---

### Connection String'i Al ve Kaydet

**4.11** Sol menüde **"Security + networking"** başlığı altında **"Access keys"** tıkla.

**4.12** Sayfada **"key1"** satırındaki **"Connection string"** bölümünün
yanında **"Show"** butonuna tıkla.

**4.13** Çıkan uzun metni **kopyala** — şöyle görünür:

```
DefaultEndpointsProtocol=https;AccountName=roadsensedevst;AccountKey=ABC123...
```

**Bu değeri bir kenara yaz, sonra lazım.**

---

## ADIM 5 — Function App Oluştur

### Function App nedir?

Kodunu çalıştıracak yer. Bilgisayarını açıp Python çalıştırmak yerine,
Azure'un bilgisayarında çalıştırıyorsun.

---

**5.1** `portal.azure.com`'da üst arama çubuğuna yaz: `Function App`

**5.2** Çıkan seçeneğe tıkla.

**5.3** **"+ Create"** butonuna tıkla.

**5.4** **"Consumption"** seçeneğini seç (en ucuzu, kullandığın kadar öde).

**5.5** **"Select"** butonuna tıkla.

**5.6** Formu şöyle doldur:

| Alan | Değer |
|------|-------|
| Subscription | Azure subscription 1 |
| Resource group | `roadsense-dev` |
| Function App name | `roadsense-dev-functions` |
| Runtime stack | **Python** |
| Version | **3.11** |
| Region | Australia East |
| Operating System | Linux |

**5.7** **"Review + create"** → **"Create"** tıkla.

**5.8** Deployment bitince **"Go to resource"** tıkla.

---

## ADIM 6 — Environment Variables Ekle (Gizli Ayarlar)

### Environment Variable nedir?

Kodun içine şifre/anahtar yazmak tehlikeli — GitHub'a yükleyince herkes görür.
Onun yerine "bu değişkenin değeri şu" diye ayrıca tanımlarsın.
Kod o değişken adını kullanır, değeri Azure güvenli şekilde saklar.

---

**6.1** Function App sayfasında sol menüde **"Settings"** başlığı altında
**"Environment variables"** tıkla.

**6.2** **"+ Add"** butonuna tıkla.

**6.3** İlk değişkeni ekle:

- Name: `AZURE_STORAGE_CONNECTION_STRING`
- Value: 4. adımda kopyaladığın uzun connection string

**6.4** **"Apply"** tıkla.

**6.5** Aynı işlemi diğer değişkenler için tekrarla:

| Name | Value |
| ---- | ----- |
| `AZURE_STORAGE_CONNECTION_STRING` | Adım 4'te kopyaladığın değer |
| `FUNCTIONS_WORKER_RUNTIME` | `python` |
| `AzureWebJobsStorage` | Adım 4'te kopyaladığın aynı connection string |

**6.6** Tüm değişkenleri ekledikten sonra sayfanın üstündeki **"Save"** butonuna tıkla.

---

## ADIM 7 — Kodu Azure'a Gönder (Deploy)

Bu adım için terminali kullanacağız — portalde kod yükleme çok karmaşık.

**7.1** Mac'inde terminali aç.

**7.2** Azure Functions Core Tools'u kur:

```bash
brew install azure-functions-core-tools@4
```

**7.3** Proje klasörüne git:

```bash
cd /Users/osmanorka/RoadSense-AI
```

**7.4** Ingestion klasörüne `requirements.txt` ekle:

```bash
cat > ingestion/requirements.txt << 'EOF'
azure-functions==1.21.3
azure-durable-functions==1.2.9
azure-storage-blob==12.20.0
httpx==0.28.1
structlog==24.1.0
EOF
```

**7.5** Kodu Azure'a gönder:

```bash
cd ingestion

func azure functionapp publish roadsense-dev-functions \
  --python \
  --build remote
```

**7.6** Terminal şunu gösterirse başarılı:

```text
Deployment completed successfully.
```

---

## ADIM 8 — Test Et

### Blob Storage'a Test Dosyası Yükle

**8.1** `portal.azure.com`'da `roadsensedevst` storage hesabına git.

**8.2** Sol menüde **"Containers"** tıkla.

**8.3** **"raw-documents"** container'ına tıkla.

**8.4** Sayfanın üstünde **"Upload"** butonuna tıkla.

**8.5** Sağdan açılan panelde:

- **"Browse for files"** tıkla
- Bilgisayarından herhangi küçük bir `.txt` veya `.json` dosyası seç

**8.6** **"Upload"** tıkla.

---

### Function'ın Çalışıp Çalışmadığını Kontrol Et

**8.7** `portal.azure.com`'da `roadsense-dev-functions` Function App'ine git.

**8.8** Sol menüde **"Functions"** tıkla.

**8.9** `blob_ingest_starter` fonksiyonuna tıkla.

**8.10** **"Monitor"** sekmesine tıkla.

**8.11** Son çalışmaları göreceksin. Yeşil tik = başarılı, kırmızı = hata.

---

## Sık Sorulan Sorular

---

### "Blob trigger nedir?"

Blob trigger, "raw-documents klasörüne yeni dosya geldiğinde bu fonksiyonu çalıştır"
demek. Kodda şöyle görünüyor:

```python
@app.blob_trigger(
    path="raw-documents/{name}",      # ← "raw-documents'a dosya düşünce..."
    connection="AZURE_STORAGE_CONNECTION_STRING",
)
async def blob_ingest_starter(blob, client):
    # ...uyan ve işlemi başlat
```

---

### "Orchestrator ne demek?"

Şantiye ustası gibi düşün. 4 işçi var (parse, mask, chunk, index). Usta sırayla
her birine iş verir. Bir işçi hastalanırsa (hata verirse) en başa dönmez —
kaldığı yerden devam eder.

Kodda:

```python
def orchestrator_function(context):
    parsed = yield context.call_activity("parse_pdf",    ...)  # ← İşçi 1
    masked = yield context.call_activity("pii_mask",     ...)  # ← İşçi 2
    chunks = yield context.call_activity("chunk_embed",  ...)  # ← İşçi 3
    result = yield context.call_activity("index_search", ...)  # ← İşçi 4
```

---

### "host.json ne işe yarıyor?"

```json
{
  "extensions": {
    "durableTask": {
      "hubName": "RoadSenseIngestion"
    }
  }
}
```

`hubName` orchestrator'ların birbirleriyle iletişim kurduğu "posta kutusu" adı.
Dev ortam ve prod ortam aynı storage'ı paylaşıyorsa farklı hub adları sayesinde
birbirini karıştırmazlar.

---

### "Tüm bu kaynakları tek tek mi oluşturmalıyım?"

Hayır! Projemizde `infra/` klasöründe Bicep dosyaları var. Bunlar Azure'a
"şu kaynakları şu ayarlarla oluştur" diyen tarifler. Terminalde tek komutla
hepsini oluşturabilirsin:

```bash
bash infra/deploy.sh roadsense-dev australiaeast dev
```

Ama önce portaldaki adımları elle yapmak, ne kurulduğunu anlamak için iyi.

---

## İlerleme Durumu

```
✅ data/raw/         → 7.000 satır veri indirildi
⬜ data/transform.py → Ham veriyi temizle + normalize et
⬜ ingestion/        → Azure'a deploy et  ← ŞU AN BURADADAYIZ
⬜ agents/           → LangGraph agentic pipeline
⬜ api/              → FastAPI endpoint'leri
⬜ frontend/         → Operator konsolu (TypeScript/Next.js)
⬜ eval/             → RAGAS + promptfoo test suiti
⬜ observability/    → Langfuse tracing + dashboards
```

---

## Sonraki Ders

Azure ingestion kurulumundan sonra sıradaki adım:

**`data/transform.py` — Ham Veriyi Pipeline'a Hazırla**

`data/raw/*.jsonl` dosyalarını alıp temizleyeceğiz, standart formata sokacağız
ve `data/processed/normalized.jsonl` olarak kaydedeceğiz. Ardından bu dosyaları
Blob Storage'a yükleyip ingestion pipeline'ını ilk kez gerçekten test edeceğiz.
