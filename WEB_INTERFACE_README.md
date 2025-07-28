# 🌐 İş Bankası AI Chatbot Web Interface

Bu proje, İş Bankası AI Chatbot'unun modern bir web arayüzünü sağlar. Flask tabanlı bu arayüz, kullanıcıların bankacılık sorularını doğal dilde sorabilmelerine ve AI asistanından yanıt alabilmelerine olanak tanır.

## ✨ Özellikler

### 🎨 Modern Kullanıcı Arayüzü
- **Responsive Design**: Mobil ve masaüstü cihazlarda mükemmel görünüm
- **Glassmorphism Tasarım**: Modern, şeffaf ve estetik arayüz
- **Smooth Animations**: Yumuşak geçişler ve animasyonlar
- **Real-time Chat**: Gerçek zamanlı mesajlaşma deneyimi

### 🚀 Gelişmiş Fonksiyonlar
- **Auto-resize Textarea**: Mesaj kutusu otomatik boyutlanır
- **Character Counter**: Karakter sayısı takibi (1000 karakter limit)
- **Quick Actions**: Hızlı soru butonları
- **Chat History**: Sohbet geçmişi yönetimi
- **Connection Status**: Bağlantı durumu göstergesi
- **Loading States**: Yükleme animasyonları

### 🔧 Teknik Özellikler
- **Flask Backend**: Python tabanlı web sunucusu
- **RESTful API**: Modern API tasarımı
- **CORS Support**: Cross-origin istek desteği
- **Error Handling**: Kapsamlı hata yönetimi
- **Health Check**: Sistem durumu kontrolü

## 🛠️ Kurulum

### 1. Gereksinimler
- Python 3.8+
- Groq API Key
- Veri pipeline'ının çalıştırılmış olması

### 2. Hızlı Başlangıç

```bash
# 1. Projeyi klonlayın (zaten mevcut)
cd İşRAG

# 2. Web interface'i başlatın
bash start_web_interface.sh
```

### 3. Manuel Kurulum

```bash
# Virtual environment oluşturun
python3 -m venv venv
source venv/bin/activate

# Gereksinimleri yükleyin
pip install -r requirements.txt

# .env dosyası oluşturun
echo "API_KEY=your_groq_api_key_here" > .env

# Web interface'i başlatın
python app.py
```

### 4. Tarayıcıda Açın
```
http://localhost:5000
```

## 📁 Dosya Yapısı

```
İşRAG/
├── app.py                          # Flask web uygulaması
├── start_web_interface.sh          # Başlatma scripti
├── templates/
│   └── index.html                  # Ana HTML template
├── static/
│   ├── css/
│   │   └── style.css              # CSS stilleri
│   └── js/
│       └── chat.js                # JavaScript fonksiyonları
└── WEB_INTERFACE_README.md        # Bu dosya
```

## 🎯 Kullanım

### Ana Özellikler

1. **Mesaj Gönderme**
   - Metin kutusuna yazın
   - Enter tuşuna basın veya gönder butonuna tıklayın
   - Shift+Enter ile yeni satır

2. **Hızlı Sorular**
   - Alt kısımdaki butonlara tıklayın
   - Önceden tanımlanmış sorular otomatik gönderilir

3. **Sohbet Yönetimi**
   - "Sohbeti Temizle" butonu ile geçmişi silin
   - Karakter sayacı ile mesaj uzunluğunu takip edin

4. **Bağlantı Durumu**
   - Sağ üst köşede bağlantı durumu göstergesi
   - Yeşil: Bağlı, Kırmızı: Hata

### API Endpoints

- `GET /` - Ana sayfa
- `POST /api/chat` - Mesaj gönderme
- `GET /api/health` - Sistem durumu

## 🎨 Özelleştirme

### CSS Değişiklikleri
`static/css/style.css` dosyasını düzenleyerek:
- Renk şemasını değiştirin
- Font stillerini güncelleyin
- Animasyonları özelleştirin

### JavaScript Fonksiyonları
`static/js/chat.js` dosyasını düzenleyerek:
- Yeni özellikler ekleyin
- API çağrılarını değiştirin
- UI davranışlarını özelleştirin

### HTML Template
`templates/index.html` dosyasını düzenleyerek:
- Sayfa yapısını değiştirin
- Yeni bileşenler ekleyin
- Meta bilgilerini güncelleyin

## 🔧 Geliştirme

### Yerel Geliştirme
```bash
# Debug modunda çalıştırın
export FLASK_ENV=development
python app.py
```

### Production Deployment
```bash
# Gunicorn ile production sunucusu
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🐛 Sorun Giderme

### Yaygın Sorunlar

1. **"ChromaDB veritabanı bulunamadı"**
   ```bash
   # Veri pipeline'ını çalıştırın
   bash scripts/run_pipeline.sh
   ```

2. **"API_KEY bulunamadı"**
   ```bash
   # .env dosyası oluşturun
   echo "API_KEY=your_groq_api_key_here" > .env
   ```

3. **Port 5000 kullanımda**
   ```bash
   # Farklı port kullanın
   python app.py --port 5001
   ```

4. **CORS Hatası**
   - `flask-cors` paketinin yüklü olduğundan emin olun
   - Tarayıcı cache'ini temizleyin

### Log Kontrolü
```bash
# Flask loglarını görüntüleyin
tail -f app.log
```

## 📊 Performans

### Optimizasyonlar
- **Lazy Loading**: Sadece gerekli bileşenler yüklenir
- **Debounced Input**: API çağrıları optimize edilir
- **Connection Pooling**: Veritabanı bağlantıları yönetilir
- **Caching**: Statik dosyalar cache'lenir

### Monitoring
- Health check endpoint'i
- Response time tracking
- Error rate monitoring
- User session tracking

## 🔒 Güvenlik

### Önlemler
- **Input Validation**: Kullanıcı girdileri doğrulanır
- **XSS Protection**: Cross-site scripting koruması
- **CSRF Protection**: Cross-site request forgery koruması
- **Rate Limiting**: API çağrı limitleri

### Environment Variables
```bash
# Güvenlik için environment değişkenleri
export FLASK_SECRET_KEY="your-secret-key"
export GROQ_API_KEY="your-groq-api-key"
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 Destek

Sorularınız için:
- GitHub Issues kullanın
- Proje maintainer'ına ulaşın
- Dokümantasyonu kontrol edin

---

**Not**: Bu web interface, mevcut RAG pipeline'ınızla tam entegre çalışır ve aynı veri kaynaklarını kullanır. 