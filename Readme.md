# PRTG Webhook Dashboard

## Proje Açıklaması
Bu proje, **PRTG Network Monitor** ile entegre çalışan bir **Flask tabanlı Webhook Dashboard** uygulamasıdır. PRTG sensörleri "Down" olduğunda **Notification Trigger** tetiklenir ve **HTTP Action**, Flask sunucusuna **POST isteği** gönderir. Flask sunucusu gelen veriyi işler, loglar ve bir **dashboard** üzerinden kullanıcıya sunar.

## Özellikler
- **PRTG ile Webhook Entegrasyonu**: PRTG, sensör durumu değiştiğinde Flask sunucusuna HTTP POST isteği gönderir.
- **Kullanıcı Girişi**: Kullanıcı adı ve şifre ile giriş yapılmasını sağlar.
- **Gerçek Zamanlı Dashboard**: PRTG'den gelen verileri işleyerek bir web arayüzünde gösterir.
- **Güvenlik**: Flask `session` yönetimi ve basit kimlik doğrulama içerir.
- **Loglama**: Gelen veriler `http_server.log` dosyasına kaydedilir.

## Kullanılan Teknolojiler
- **Python** (Flask, logging, json, datetime)
- **HTML, CSS (Bootstrap 5.3)**
- **PRTG Network Monitor**

## Kurulum & Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/yusufdalbudak/flask-HTTP-Server.git
cd flask-HTTP-Server
```

### 2. Gerekli Bağımlılıkları Yükleyin
```bash
pip install flask
```

### 3. Flask Sunucusunu Başlatın
```bash
python http_server.py
```
Sunucu **http://0.0.0.0:5000/** adresinde çalışacaktır.

### 4. PRTG'de HTTP Notification Ayarlarını Yapılandırın
1. **PRTG Web Arayüzüne** giriş yapın.
2. **Setup > Notification Templates** bölümüne gidin.
3. Yeni bir **Notification Template** oluşturun.
4. "Execute HTTP Action" seçeneğini etkinleştirin.
5. **URL:** `http://sunucu_ip:5000/prtg-webhook`
6. **Method:** `POST`
7. **Content-Type:** `application/json`
8. Örnek JSON:
```json
{
    "datetime": "2024-02-28 14:30:00",
    "sensor": "CPU Usage",
    "device": "Server-1",
    "status": "Down",
    "message": "CPU %95 üzerinde",
    "priority": "High"
}
```

## Kullanım
1. **Giriş Yapın**: `http://sunucu_ip:5000/` adresine gidin.
2. **Kullanıcı Bilgileri**:
   - **Kullanıcı Adı:** `admin`
   - **Şifre:** `password123`
3. **Dashboard'ı Görüntüleyin**: Tetiklenen alarmlar burada görüntülenir.
4. **Çıkış Yapın**: Sağ üst köşedeki "Logout" butonuna tıklayın.

## Dosya Yapısı
```
prtg-webhook-dashboard/
│── templates/
│   ├── login.html
│   ├── dashboard.html
│── http_server.py
│── http_server.log
│── README.md
```

## Geliştirme
Proje geliştirmeye açıktır. **Pull Request** gönderebilir veya yeni özellik taleplerinde bulunabilirsiniz.

## Lisans
Bu proje **MIT** lisansı ile lisanslanmıştır.

