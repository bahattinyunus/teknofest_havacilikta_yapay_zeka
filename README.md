# 🛸 SkyGuard AI: Yeni Nesil Otonom Havacılık Sistemi

<div align="center">

[![Lisans](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Teknofest](https://img.shields.io/badge/Hedef-Teknofest_2026-red?style=for-the-badge&logo=rocket&logoColor=white)](https://www.teknofest.org/)
[![Kod Stili: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Durum](https://img.shields.io/badge/Status-Active_Development-green?style=for-the-badge)](https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka)

**"Göklerdeki Gözünüz, Yerdeki Gücünüz"**

[Özellikler](#-temel-özellikler) • [Mimari](#-sistem-mimarisi) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Yol Haritası](#-yol-haritası)

</div>

---

## 🌟 Proje Hakkında

**SkyGuard AI**, **Teknofest Ulaşımda Yapay Zeka** kategorisi için özel olarak geliştirilmiş, yüksek performanslı ve modüler bir otonom uçuş yazılımıdır. Geleneksel İHA sistemlerinin ötesine geçerek, derin öğrenme tabanlı görüntü işleme yeteneklerini gerçek zamanlı uçuş kontrol algoritmalarıyla birleştirir.

Amacımız, karmaşık arama-kurtarma, gözetleme ve lojistik görevlerini insan müdahalesi olmadan, tam otonom bir şekilde gerçekleştirebilen akıllı bir hava platformu oluşturmaktır.

---

## 🚀 Temel Özellikler

### 🧠 1. İleri Seviye Yapay Zeka
*   **Gerçek Zamanlı Nesne Tespiti**: YOLOv8 mimarisi ile insan, araç, ateş ve özel işaretçileri milisaniyeler içinde tespit eder.
*   **Dinamik Hedef Takibi**: Hareketli hedeflere kilitlenir ve onları görüş alanında tutar.
*   **Akıllı İniş**: Görsel verileri kullanarak en güvenli iniş alanını belirler.

### 🚁 2. Otonom Uçuş Kontrolü
*   **Hassas PID Kontrolü**: Zorlu hava koşullarında bile stabil uçuş sağlayan optimize edilmiş kontrol döngüleri.
*   **Görev Planlama**: 3B uzayda karmaşık waypoint görevlerini icra edebilir.
*   **Engel Sakınma**: Çevresel farkındalık ile statik ve dinamik engellerden kaçınır.

### � 3. Yeni Nesil Yer Kontrol İstasyonu (YKİ)
*   **Canlı Video Akışı**: Düşük gecikmeli HD görüntü aktarımı.
*   **Anlık Telemetri**: İrtifa, hız, pil durumu ve GPS verilerinin saniyelik takibi.
*   **Kullanıcı Dostu Arayüz**: Streamlit tabanlı, modern ve duyarlı kontrol paneli.

---

## 🏗️ Sistem Mimarisi

SkyGuard AI, endüstri standardı modüler bir yapı üzerine inşa edilmiştir. Bu sayede her bir bileşen bağımsız olarak geliştirilebilir ve test edilebilir.

```mermaid
graph TD
    subgraph "Hava Birimi"
        Cam[Kamera] -->|Video Akışı| Vision[Görüntü İşleme (YOLOv8)]
        Sensors[Sensörler] -->|IMU/GPS/Baro| Stateest[Durum Tahmini]
        Vision -->|Hedef Konumu| Decision[Karar Mekanizması]
        Stateest -->|Mevcut Durum| Decision
        Decision -->|Setpoints| Control[PID Kontrolcü]
        Control -->|PWM| Motors[Motor Sürücüleri]
    end
    
    subgraph "Yer Birimi"
        Telemetry[Telemetri Modülü] <-->|Kablosuz Bağlantı| GCS[Yer Kontrol İstasyonu]
        GCS -->|Komutlar| Decision
        Vision -->|İşlenmiş Görüntü| GCS
    end
    
    style Vision fill:#f9f,stroke:#333
    style Control fill:#bbf,stroke:#333
    style GCS fill:#bfb,stroke:#333
```

---

## 🛠️ Teknolojiler

Bu proje, alanındaki en güçlü açık kaynak kütüphaneler kullanılarak geliştirilmiştir:

| Alan | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Dil** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Ana geliştirme dili |
| **Yapay Zeka** | ![YOLOv8](https://img.shields.io/badge/-Ultralytics_YOLOv8-000000?logo=yolo) | Nesne tespiti ve sınıflandırma |
| **Görüntü İşleme** | ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?logo=opencv&logoColor=white) | Görüntü ön işleme ve görselleştirme |
| **Arayüz** | ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=streamlit&logoColor=white) | Modern yer kontrol istasyonu |
| **Veri Analizi** | ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white) | Uçuş verilerinin analizi |

---

## ⚡ Hızlı Başlangıç

Projenin kurulumu ve çalıştırılması son derece basittir.

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/bahattinyunus/teknofest_havacilikta_yapay_zeka.git
cd teknofest_havacilikta_yapay_zeka
```

### 2. Otomatik Kurulum (Windows)
`setup.bat` dosyasını çalıştırarak tüm ortamı tek tıkla kurabilirsiniz.

Veya manuel kurulum için:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Sistemi Başlatın

**Yer Kontrol İstasyonu:**
```bash
streamlit run dashboard.py
```

**Otonom Uçuş Modu:**
```bash
python main.py
```

---

## �️ Yol Haritası

- [x] **Faz 1: Temel Sistem** (Tamamlandı)
    - [x] Proje iskeletinin oluşturulması
    - [x] Temel PID kontrolcüleri
    - [x] Dashboard arayüzü

- [ ] **Faz 2: Yapay Zeka Entegrasyonu**
    - [ ] Özel veri seti ile YOLO modelinin eğitimi
    - [ ] Hareketli nesne takibi
    - [ ] İniş pisti tespiti

- [ ] **Faz 3: Donanım Entegrasyonu**
    - [ ] Pixhawk/Ardupilot ile MAVLink haberleşmesi
    - [ ] Gerçek zamanlı video aktarımı (RTSP)
    - [ ] Saha testleri ve optimizasyon

---

## 🤝 Katkıda Bulunma

Açık kaynak dünyasını seviyoruz! Katkıda bulunmak isterseniz:

1.  Bu repoyu **Fork**layın.
2.  Yeni bir **Branch** oluşturun (`git checkout -b feature/HarikaOzellik`).
3.  Değişikliklerinizi **Commit**leyin (`git commit -m 'Harika özellik eklendi'`).
4.  Branch'inizi **Push**layın (`git push origin feature/HarikaOzellik`).
5.  Bir **Pull Request** oluşturun.

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

<div align="center">

**Teknofest Havacılık, Uzay ve Teknoloji Festivali için gururla geliştirilmiştir.**
<br>
<sub>Geliştirici: <a href="https://github.com/bahattinyunus">Bahattin Yunus</a></sub>

</div>
