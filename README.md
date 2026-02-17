# 🛸 SkyGuard AI: Otonom Havacılık Sistemi

[![Lisans](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Teknofest](https://img.shields.io/badge/Hedef-Teknofest_2026-red)](https://www.teknofest.org/)
[![Kod Stili: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **"Göklerdeki Gözünüz, Yerdeki Gücünüz"**

**SkyGuard AI**, **Teknofest Ulaşımda Yapay Zeka** yarışması için tasarlanmış kapsamlı bir otonom insansız hava aracı (İHA) yazılım paketidir. Nesneleri tespit etmek, otonom olarak gezinmek ve yer kontrol istasyonuna gerçek zamanlı telemetri sağlamak için son teknoloji bilgisayarlı görü ile sağlam uçuş kontrol algoritmalarını birleştirir.

---

## 🏗️ Mimari

Sistem, ölçeklenebilirlik ve test kolaylığı sağlamak için modüler bir mimari üzerine inşa edilmiştir.

```mermaid
graph TD
    A[Kamera Görüntüsü] -->|Kareler| B(Görüntü İşleme Modülü)
    B -->|Tespitler| C{Karar Mekanizması}
    C -->|Komutlar| D[Kontrol Modülü]
    D -->|PWM Sinyalleri| E[Uçuş Kontrolcüsü (Pixhawk/Sim)]
    D -->|Telemetri Verisi| F[Telemetri Kayıtçısı]
    F -->|WebSocket/Seri| G[Yer Kontrol İstasyonu (Streamlit)]
```

### Temel Bileşenler

- **👁️ Görüntü İşleme Modülü**: Hava görüntüleri için özel olarak ayarlanmış, gerçek zamanlı nesne tespiti ve takibi yapabilen **YOLOv8** ile güçlendirilmiştir.
- **🎮 Kontrol Modülü**: Kararlı uçuş dinamiği ve otonom yol takibi için **PID kontrolcüleri** uygular.
- **📡 Telemetri & Kayıt**: Uçuş sonrası analiz için gerçek zamanlı veri akışı ve "Kara Kutu" kaydı.
- **🖥️ Yer Kontrol İstasyonu (YKİ)**: Uçuş durumunu, pil seviyelerini ve canlı video akışlarını izlemek için **Streamlit** ile oluşturulmuş modern, web tabanlı bir panel.

---

## 🚀 Yetenekler & Özellikler

### 1. Otonom Seyrüsefer
- **Waypoint (Nokta) Seyrüsefer**: Önceden tanımlanmış 3B bir rotayı takip eder.
- **Engel Saffetme**: Statik ve dinamik engelleri algılar ve etrafından dolaşır.

### 2. Gelişmiş Nesne Tespiti
- **Hedef Kilitleme**: Belirli hedefleri (kodlanmış işaretçiler, araçlar, insanlar) tanımlar.
- **İniş Bölgesi Tespiti**: Görsel ipuçlarını kullanarak güvenli iniş noktalarını otomatik olarak bulur.

### 3. Akıllı Güvenlik Önlemleri
- **Eve Dönüş (RTL)**: Sinyal kaybı veya düşük pil durumunda devreye girer.
- **Acil Durum Havada Asılı Kalma (Hover)**: Anormal sensör verileri algılandığında derhal stabilizasyon sağlar.

---

## 🛠️ Kurulum

### Gereksinimler
- Python 3.9+
- CUDA uyumlu GPU (YOLOv8 eğitimi/çıkarımı için önerilir)

### Adımlar

1. **Repoyu klonlayın**
   ```bash
   git clone https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka.git
   cd teknofest_havacilikta_yapay_zeka
   ```

2. **Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

3. **Pre-commit kancalarını yükleyin (İsteğe bağlı)**
   ```bash
   pre-commit install
   ```

---

## 💻 Kullanım

### 1. Yer Kontrol İstasyonunu Başlatın
Sistem durumunu izlemek için paneli başlatın.
```bash
streamlit run dashboard.py
```

### 2. Otonom Görevi Başlatın
Ana uçuş senaryosunu çalıştırın.
```bash
python main.py --mission gorev_1.json
```

---

## 📂 Proje Yapısı

```
teknofest_havacilikta_yapay_zeka/
├── data/                  # Veri Setleri & Loglar
├── models/                # Eğitilmiş YOLOv8 modelleri
├── src/                   # Kaynak Kod
│   ├── control/           # Uçuş dinamiği & PID
│   ├── telemtry/          # Veri kaydı & İletişim
│   ├── vision/            # Bilgisayarlı Görü akışları
│   └── utils/             # Yardımcı fonksiyonlar
├── tests/                 # Birim Testleri
├── dashboard.py           # Streamlit YKİ Uygulaması
├── main.py                # Ana Giriş Noktası
└── requirements.txt       # Proje Bağımlılıkları
```

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen kod kurallarımız ve pull request gönderme süreci hakkında ayrıntılar için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın.

1. Forklayın!
2. Özellik dalınızı (branch) oluşturun: `git checkout -b yeni-ozellik`
3. Değişikliklerinizi commitleyin: `git commit -am 'Yeni bir özellik ekle'`
4. Dalınıza pushlayın: `git push origin yeni-ozellik`
5. Bir Pull Request oluşturun :D

---

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

<p align="center">
  Teknofest için <a href="https://github.com/bahattinyunus">Bahattin Yunus</a> tarafından ❤️ ile yapılmıştır
</p>
