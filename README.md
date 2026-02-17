# 🛸 SkyGuard AI: Otonom Havacılık ve Zeka Sistemi

<div align="center">

[![Lisans](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Teknofest](https://img.shields.io/badge/Hedef-Teknofest_2026-red?style=for-the-badge&logo=rocket&logoColor=white)](https://www.teknofest.org/)
[![Kod Stili: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Durum](https://img.shields.io/badge/Status-Active_Development-green?style=for-the-badge)](https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka)
[![CI/CD](https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka/actions/workflows/ci.yml/badge.svg)](https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka/actions)

**"Göklerdeki Gözünüz, Yerdeki Gücünüz"**

Tam otonom uçuş, gerçek zamanlı görüntü işleme ve gelişmiş yer kontrol istasyonu.

[Özellikler](#-temel-özellikler) • [Mimari](#-sistem-mimarisi) • [Simülasyon](#-canlı-simülasyon) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Yol Haritası](#-yol-haritası)

</div>

---

## 🌟 Proje Hakkında

**SkyGuard AI**, **Teknofest Ulaşımda Yapay Zeka** kategorisi için özel olarak geliştirilmiş, yüksek performanslı ve modüler bir otonom uçuş yazılımıdır. Geleneksel İHA sistemlerinin ötesine geçerek, derin öğrenme tabanlı görüntü işleme yeteneklerini gerçek zamanlı uçuş kontrol algoritmalarıyla birleştirir.

Amacımız, karmaşık arama-kurtarma, gözetleme ve lojistik görevlerini insan müdahalesi olmadan, tam otonom bir şekilde gerçekleştirebilen akıllı bir hava platformu oluşturmaktır.

---

## 🚀 Temel Özellikler

### 🧠 1. İleri Seviye Yapay Zeka & Görüntü İşleme
*   **Gerçek Zamanlı Nesne Tespiti**: **YOLOv8** mimarisi ile insan, araç, ateş ve özel işaretçileri tespit eder.
*   **Akıllı Nesne Takibi (Tracking)**: Tespit edilen nesnelere benzersiz kimlikler (ID) atayarak kareler arasında takip eder. Sahradan çıkıp giren nesneleri ayırt eder.
*   **Dinamik Hedef Kilidi**: Hareketli hedeflere kilitlenir ve gimbal/drone yönelimini günceller.

### 🚁 2. Otonom Seyrüsefer & Kontrol
*   **GPS Tabanlı Navigasyon**: Haversine formülü ile hassas waypoint takibi.
*   **Görev Yönetimi**: JSON tabanlı görev dosyaları ile karmaşık uçuş planları oluşturma.
*   **Hassas PID Kontrolü**: Zorlu hava koşullarında bile stabil uçuş sağlayan optimize edilmiş kontrol döngüleri.
*   **Güvenli Modlar**: Eve Dönüş (RTL), Otomatik İniş ve Acil Durum modları.

### 💻 3. Yeni Nesil Yer Kontrol İstasyonu (YKİ)
*   **3B Harita Entegrasyonu**: Drone'un konumunu ve rotasını uydu haritası üzerinde canlı izleyin.
*   **Canlı Simülasyon**: Gerçek uçuş verileriyle senkronize çalışan yapay ufuk ve çevre simülasyonu.
*   **Anlık Telemetri**: İrtifa (AGL), Yer Hızı, Pil Durumu ve GPS verilerinin saniyelik takibi.
*   **Kullanıcı Dostu Arayüz**: **Streamlit** ile geliştirilmiş, modern ve duyarlı kontrol paneli.

---

## 🏗️ Sistem Mimarisi

SkyGuard AI, endüstri standardı modüler bir yapı üzerine inşa edilmiştir. Veri akışı sensörlerden yapay zeka modülüne, oradan da karar mekanizmasına akar.

```mermaid
graph TD
    subgraph "Hava Birimi (Onboard)"
        Cam[Kamera] -->|Video Akışı| Vision[Görüntü İşleme (YOLOv8 + Tracker)]
        GPS[GPS Modülü] -->|Konum| Navigator[Seyrüsefer Yöneticisi]
        Sensors[IMU/Baro] -->|Veri| Stateest[Durum Tahmini]
        
        Navigator -->|Hedef Heading/Mesafe| Decision[Karar Mekanizması]
        Vision -->|Hedef Konumu| Decision
        Stateest -->|Mevcut Durum| Decision
        
        Decision -->|Düzeltme Komutları| Control[PID Kontrolcü]
        Control -->|PWM Sinyali| Motors[Motor Sürücüleri]
    end
    
    subgraph "Yer Birimi (GCS)"
        Telemetry[Telemetri Modülü] <-->|MAVLink/Serial| GCS[SkyGuard Dashboard]
        GCS -->|Görev Yükle| Navigator
        Vision -->|İşlenmiş Görüntü| GCS
    end
```

---

## 🎮 Canlı Simülasyon

Donanım olmadan da sistemi test edebilirsiniz! Dashboard içinde çalışan fizik tabanlı simülatör şunları sunar:
*   **Yapay Ufuk**: Drone'un Roll ve Pitch hareketlerine tepki veren dinamik gökyüzü/yer renderı.
*   **Sanal Hedefler**: Görüntü işleme algoritmalarını test etmek için rastgele oluşturulan yapay hedefler.
*   **HUD (Head-Up Display)**: Pilot için kritik uçuş verilerinin ekran üstü gösterimi.

---

## 🛠️ Teknolojiler

Bu proje, alanındaki en güçlü açık kaynak kütüphaneler kullanılarak geliştirilmiştir:

| Alan | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Dil** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Ana geliştirme dili |
| **Yapay Zeka** | ![YOLOv8](https://img.shields.io/badge/-Ultralytics_YOLOv8-000000?logo=yolo) | Nesne tespiti ve sınıflandırma |
| **Görüntü İşleme** | ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white) | Görüntü sentezi ve işleme |
| **Haritalama** | ![PyDeck](https://img.shields.io/badge/-PyDeck-000000?logo=uber&logoColor=white) | 3B Harita görselleştirme |
| **Arayüz** | ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white) | Modern yer kontrol istasyonu |
| **Navigasyon** | ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white) | Vektörel hesaplamalar |

---

## ⚡ Hızlı Başlangıç

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka.git
cd teknofest_havacilikta_yapay_zeka
```

### 2. Otomatik Kurulum (Windows)
`setup.bat` dosyasını çalıştırarak tüm ortamı tek tıkla kurabilirsiniz.

### 3. Sistemi Başlatın

**Yer Kontrol İstasyonu:**
```bash
streamlit run dashboard.py
```
> Tarayıcınızda açılan panelden "Harita Görünümü" sekmesine geçerek otonom uçuşu izleyin.

**Model Eğitimi (Demo):**
```bash
jupyter notebook notebooks/Egitim_Demo.ipynb
```

**Birim Testleri:**
```bash
pytest tests/
```

---

## 📂 Proje Yapısı

```
teknofest_havacilikta_yapay_zeka/
├── data/
│   ├── missions/          # JSON görev dosyaları
│   └── logs/              # Uçuş kayıtları (Kara Kutu)
├── models/                # Eğitilmiş YOLO modelleri (.pt)
├── notebooks/             # Veri bilimi ve eğitim not defterleri
├── src/
│   ├── control/           # Uçuş kontrol (PID) ve Navigasyon
│   ├── mission/           # Görev yükleyici ve doğrulayıcı
│   ├── simulation/        # Görüntü sentezleyici (Simülatör)
│   ├── telemetry/         # Veri kaydı ve iletişim
│   └── vision/            # Görüntü işleme ve Nesne Takibi
├── tests/                 # Kalite güvence testleri
├── dashboard.py           # Ana Kontrol Paneli Uygulaması
├── main.py                # Otonom Uçuş Betiği
└── requirements.txt       # Bağımlılıklar
```

---

## 🗺️ Yol Haritası

- [x] **Faz 1: Temel Sistem**
    - [x] Proje iskeleti ve PID kontrolcüler
    - [x] Temel Dashboard

- [x] **Faz 2: Simülasyon & Zeka**
    - [x] Sentetik video akışı
    - [x] Model eğitim pipeline'ı
    - [x] Birim test altyapısı

- [x] **Faz 3: Navigasyon & Operasyon**
    - [x] GPS Waypoint takibi
    - [x] Harita tabanlı Dashboard
    - [x] JSON görev yükleyici
    - [x] Nesne Takibi (Object Tracking)

- [ ] **Faz 4: Donanım Entegrasyonu (Gelecek)**
    - [ ] MAVLink ile Pixhawk iletişimi
    - [ ] Jetson Nano üzerinde optimizasyon (TensorRT)
    - [ ] LoRa ile uzun menzilli telemetri

---

## 🤝 Katkıda Bulunma

Açık kaynak dünyasını seviyoruz! Katkıda bulunmak isterseniz:
1.  Forklayın.
2.  Branch oluşturun (`git checkout -b feature/YeniOzellik`).
3.  Commit atın (`git commit -m 'Yeni özellik eklendi'`).
4.  Pushlayın (`git push origin feature/YeniOzellik`).
5.  Pull Request açın.

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

<div align="center">

**Teknofest Havacılık, Uzay ve Teknoloji Festivali için gururla geliştirilmiştir.**
<br>
<sub>Lider Geliştirici: <a href="https://github.com/bahattinyunus">Bahattin Yunus</a></sub>

</div>
