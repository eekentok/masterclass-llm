# 🏦 Bankacılık Chatbotu için RAG Pipeline Projesi

Bu proje, **halka açık bankacılık/finans içeriklerini** toplayıp temizleyerek, parçalara (chunk) ayırıp embedding vektörlerine dönüştürerek ve bir LLM (Groq API) kullanarak **Retriever-Augmented Generation (RAG)** mimarisiyle sorulara yanıt verecek bir prototip chatbot geliştirmek için tasarlanmıştır.

**Hedef:** Banka müşterisinin veya çalışanının finans/bankacılık terimlerini ve bilgilerini doğal dilde sormasına olanak tanıyan bir “Finans Asistanı” prototipi üretmek.

---

## 📌 Projenin Özeti

- **Web Scraping**: Halka açık bankacılık/finans içeriklerini topla.
- **Temizlik**: HTML ve gereksiz karakterleri temizle.
- **Chunking**: Uzun metinleri anlamlı parçalara böl.
- **Embedding**: Groq API ile vektör temsillerini oluştur.
- **Retrieval**: Kullanıcının sorusuna en yakın chunk’ı bul.
- **Generation**: Groq LLM ile yanıt üret.

---

## 🎯 Gerçek Hayat Senaryosu

Bir banka chatbotu veya self-servis yardım sistemi düşünün:

> Kullanıcı: “Vadeli Mevduat Nedir?”  
> Chatbot: Bankanın veya regülasyon kurumlarının sitelerinden çekilmiş metinleri kullanarak, kendi üslubuyla anlamlı ve doğru bir açıklama üretir.

### 📌 ✅ Örnek Soru Seti

> **Amaç:** Chatbot'un retrieval ve generation kalitesini test etmek için farklı perspektiflerden kullanıcı soruları.  
> Her soruyu dene, sonucu gözlemle ve yanıt kalitesini analiz et.

#### 🟢 Basit Sorular (Müşteri Dili)
- Vadeli mevduat nedir?
- Banka nedir ve ne iş yapar?
- Vadeli hesap nasıl açılır?
- Vadeli ve vadesiz hesap arasındaki fark nedir?
- Paramı biriktirmek istiyorum, vadeli mi açayım?
- Bana en karlı hesap hangisi olur?
- Nasıl faiz kazanırım anlatır mısın?

#### 🟡 İşlem / Senaryo Bazlı Sorular
- Vadeli hesap açmak için hangi belgelere ihtiyacım var?
- Şubeye gitmeden vadeli hesap açabilir miyim?
- Telefon bankacılığıyla hesabı kapatabilir miyim?
- Vadeli hesabı internetten nasıl yönetirim?
- EFT yapabilir miyim vadeli hesaptan?
- Vadeli hesabımı erken kapatırsam ne olur?

#### 🟠 Kavram Açıklatıcı Sorular
- Stopaj ne demek?
- Mevduat sigortası nedir?
- Faiz oranı nasıl belirlenir?
- Brüt faiz / net faiz farkı ne?
- Ana para koruması nedir?

#### 🟣 Karşılaştırmalı Sorular
- Vadeli mi vadesiz mi avantajlı?
- Vadeli mevduat mı yatırım fonu mu daha iyi?
- Katılma hesabı ile vadeli hesap farkı nedir?
- Altın hesabı mı vadeli TL hesabı mı?
- Vadeli mevduat mı döviz hesabı mı?

#### 🔴 Risk ve Mevzuat Soruları
- Vadeli hesabın riskleri var mı?
- Devlet garantisi limiti nedir?
- BDDK mevduat sigortası ne kadar?
- Faiz oranları serbest mi?
- Vadeli hesabı erken bozdurursam zarar eder miyim?

#### 🧭 Stratejik / Analitik Sorular
- Vadeli mevduat enflasyona karşı nasıl koruma sağlar?
- Vadeli mevduatın likidite riski nedir?
- Bankaların bilançolarında vadeli mevduat nasıl gösterilir?
- Faizler yükselirse ne olur?
- Uzun vadeli mi kısa vadeli mi daha karlı?
- Bankalar neden vadeli hesap açtırmak ister?

#### 🧩 Basitleştirilmiş / Çocuk Diliyle Açıklama İsteyen Sorular
- Vadeli hesabı bana çocuk gibi anlatır mısın?
- Faiz nedir basitçe açıkla.
- Bankacılık ne iş yapar anlat.
- En kolay dille vadeli hesap nedir?

#### 🌐 İngilizce Soru Örnekleri
- What is a time deposit?
- Difference between demand and time deposit?
- How do banks calculate interest for time deposits?
- Advantages of a time deposit account.
- What happens if I break a time deposit early?
- Is a time deposit safe?
- How does the banking system work?

---

## 💡 Neden Bunu Yapıyoruz?

✅ Banka müşterilerine self-service yanıt sağlamak.  
✅ Çağrı merkezi yükünü azaltmak.  
✅ Çalışanların iç doküman aramasını hızlandırmak.  
✅ LLM yanıtlarının kuruma özel, izinli kaynaklardan türemesi.  
✅ Gerçek bir veri mühendisliği ve LLM uygulama deneyimi kazanmak.

---

## ⚙️ Mimari

1. **Web Scraping**
   - Halka açık içerikleri çek.
2. **Cleaning**
   - HTML ve gereksiz karakterleri temizle.
3. **Chunking**
   - Uzun metinleri parçalara ayır.
4. **Embedding (Groq API)**
   - Vektör temsillerini oluştur.
5. **Retriever (Similarity Search)**
   - Kullanıcı sorusuna en yakın chunk’ı bul.
6. **Generator (Groq ChatCompletion)**
   - Son yanıtı üret.

---

## 🚀 Kullanım Akışı Adımları

### 1️⃣ Web Scraping
- Halka açık sitelerden bankacılık/finans içerikleri çek.
- Robots.txt kontrolü (etik scraping).
- Sayfa başlığı, içerik, URL çıkart.
- CSV/JSONL dosyasına yaz.
  
✅ Örnek Kaynaklar:
- [Wikipedia](https://tr.wikipedia.org):
  - "Banka", "Mevduat", "Kredi", "Enflasyon", "Faiz", "Mortgage", "Katılım Bankacılığı" gibi maddeler.
  - Avantaj: Tamamen açık ve izinli.

- [Merkez Bankası (TCMB) Resmi Sitesi](https://www.tcmb.gov.tr):
  - Faiz karar metinleri, enflasyon raporları, tanıtım sayfaları.
  - Politikalar ve terimler üzerine gerçek içerik.

- [BDDK](https://www.bddk.org.tr/) ve [SPK](https://spk.gov.tr/) Siteleri:
  - Düzenleme metinleri, sektör raporları.
  - Bankacılık sistemi tanıtımı, tanımlar.

- Bankaların Resmi Blog veya Eğitim Sayfaları:
  - Örneğin [İş Bankası](https://www.isbank.com.tr/mevduat-ve-yatirim) gibi bankaların "Bilgi Merkezi", "Finansal Sözlük" bölümleri.
  - Resmi, güvenilir ve kamuya açık içerikler.

- Finans Haber Siteleri:
  - Dünya Gazetesi, Bloomberg HT, Ekonomist Dergi.
  - "Kavramlar" veya "Özel Dosyalar" başlıkları.
    
- Finans Eğitim Blogları:
  - bankacilikdunyasi.com, finansokulu.com
  - Basit ve anlaşılır kavram anlatımları.

- Resmi AB veya IMF Sayfaları:
  - Finansal terimler sözlükleri ve raporlar.
  - Uluslararası kavramlar.

✅ İpucu:
- Her kaynakta önce `robots.txt` kontrolü yapılmalı.

✅ Çıktı: `input/scraped_data.csv`

---

### 2️⃣ Temizlik (Cleaning)
- HTML tagleri kaldır.
- Lower-case dönüşüm.
- Noktalama işaretleri ve gereksiz boşlukları temizle.

✅ Çıktı: `output/cleaned_data.csv`

---

### 3️⃣ Chunking
- ~500–1000 token’lık parçalara böl.
- Overlap opsiyonu ile bağlam koru.

✅ Çıktı: `output/chunked_data.csv`

---

### 4️⃣ Embedding
- Groq Embedding API kullanarak vektör temsillerini oluştur.
- JSONL formatında kaydet.

✅ Çıktı: `output/embeddings.jsonl`

---

### 5️⃣ Retrieval (Arama)
- Kullanıcının sorusunu embed edin.
- Veri içindeki embeddinglerle karşılaştırıp en yakın chunk’ı bulun.
- Yanıt üretme için bu chunk’ı LLM’e vereceksiniz.

✅ **Temel Yöntem:**

- Cosine similarity kullanarak Python döngüsü ile en yakın chunk’ı seçin.
- Küçük veri setleri için yeterli ve anlaşılır.

✅ **İsteğe Bağlı (Opsiyonel):**

- Daha gelişmiş bir çözüm için FAISS kütüphanesini entegre edebilirsiniz.
- FAISS → Büyük veri setlerinde embedding aramasını çok hızlı hale getirir.

---

### 6️⃣ Generation (Yanıt Üretme)
- En iyi chunk’ı prompt’a ekle.
- Groq ChatCompletion API → doğal dilde yanıt.

---

### 7️⃣ Otomasyon
- Bash script ile tüm pipeline’ı çalıştır.
- Cronjob ile belirli aralıklarla veri güncelle.

---

## 🗂️ Proje Klasör Yapısı

```bash
.
├── input/
│ └── scraped_data.csv
│
├── output/
│ ├── cleaned_data.csv
│ ├── chunked_data.csv
│ ├── embeddings.jsonl
│ └── logs/
│ └── pipeline.log
│
├── data/
│ └── index.faiss
│
├── scripts/
│ ├── scraper.py
│ ├── clean.py
│ ├── chunk.py
│ ├── embed.py
│ ├── search.py
│ ├── rag.py
│ ├── run_pipeline.sh
│ └── schedule_cron.sh
│
├── notebooks/
│ ├── scraping_demo.ipynb
│ ├── profiling.ipynb
│ └── rag_demo.ipynb
│
├── tests/
│ └── test_pipeline.py
└── README.md
```

---

## 📜 Scripts Açıklamaları

- **scraper.py**:
  - Requests, BeautifulSoup ile scraping.
  - Bonus: Robots.txt kontrolü.
  - Başlık, içerik, URL → CSV/JSONL.

- **clean.py**:
  - HTML temizliği.
  - Lower-case.
  - Noktalama ve boşluk temizliği.

- **chunk.py**:
  - ~500-1000 token parçalama.
  - Overlap desteği.

- **embed.py**:
  - Groq Embedding API ile vektör üretimi.
  - JSONL çıktısı.

- **search.py**:
  - Kullanıcı sorusunu embed et.
  - FAISS veya dot-product similarity.

- **rag.py**:
  - Prompt hazırlama.
  - Groq ChatCompletion API çağrısı.

- **run_pipeline.sh**:
  - Tüm adımları ardışık çalıştırır.
    python scraper.py
    python clean.py
    python chunk.py
    python embed.py
    python build_index.py

---

- **schedule_cron.sh**:
  - Örnek cronjob:
  ```
  0 3 * * * /bin/bash /home/ubuntu/run_pipeline.sh >> /home/ubuntu/logs/pipeline.log 2>&1
  ```

---

## 📓 Notebooks
- **scraping_demo.ipynb**: Scraping ve robots.txt kontrolü.
- **profiling.ipynb**: ydata-profiling analizi.
- **rag_demo.ipynb**: Kullanıcı sorusu → embedding → en yakın chunk → LLM yanıtı.

---

## 🧪 Tests
- **test_pipeline.py**:
  - Scraped veri dolu mu?
  - Clean sonrası HTML kalmış mı?
  - Chunk uzunluğu uygun mu?
  - Embedding boyutu doğru mu?
  - Similarity sıralaması mantıklı mı?

---

## ✅ Kurulum Adımları

1️⃣ Ortam kurulumu:

```
pip install pandas beautifulsoup4 requests groq numpy faiss-cpu ydata-profiling
```

2️⃣ Groq API Key almak için:
- [Groq.com](https://groq.com)

3️⃣ Google Colab:
- Tarayıcıda çalıştır → ücretsiz.

---

## ⚡ Kullanım Örneği

```
bash scripts/run_pipeline.sh
```

✅ Tüm pipeline baştan sona otomatik çalışır.

---

## ✅ Version Control Önerisi

- `main` → üretime hazır kod.
- `dev` → geliştirme dalları.
- `feature/cleaning` → cleaning geliştirmeleri.
- `feature/chunking` → chunking geliştirmeleri.

✅ PR → Review → Merge.  
✅ Issues → Görev yönetimi.

---
