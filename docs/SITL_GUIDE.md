# SkyGuard AI: ArduPilot SITL Entegrasyon Rehberi

SkyGuard AI, gerçek donanım (Pixhawk/Cube Orange) veya "Software In The Loop" (SITL) simülasyonu ile çalışacak şekilde tasarlanmıştır. Bu rehber, SITL kullanarak sistemin nasıl test edileceğini açıklar.

## 1. Gereksinimler
-   **Mission Planner** (Windows) veya **MAVProxy** (Linux).
-   **ArduPilot SITL** ikili dosyaları.

## 2. SITL Kurulumu (Windows)
1.  Mission Planner'ı indirin ve kurun.
2.  Mission Planner'ı açın ve **Simulation** sekmesine gidin.
3.  **Multirotor** simgesini seçin.
4.  **Model** olarak "Quadcopter" seçin.
5.  **Simulate** butonuna tıklayın.

ArduPilot simülasyonu arka planda çalışmaya başlayacaktır. Genellikle TCP 5760 üzerinden veri yayınlar, ancak MAVLink köprümüz varsayılan olarak `udp:127.0.0.1:14550` dinler.

## 3. Bağlantının Yapılandırılması
SkyGuard AI Dashboard üzerinden SITL'a bağlanmak için:

1.  Mission Planner'da çalışan simülasyondan veri akışını yönlendirmek gerekebilir.
2.  Ancak en kolayı, `setup.bat` ile SkyGuard AI'ı başlattıktan sonra Dashboard'a gitmektir.
3.  **Bağlantı Ayarları** bölümünde:
    *   **Veri Kaynağı**: "MAVLink (Donanım/SITL)" seçin.
    *   **Bağlantı Adresi**: `tcp:127.0.0.1:5760` (Mission Planner için) veya `udp:127.0.0.1:14550` (MAVProxy varsayılanı).
4.  **Bağlan** butonuna tıklayın.

## 4. Test Senaryosu
1.  Dashboard'da bağlantı başarılı olduğunda "Durum: BAĞLI 🟢" yazısını göreceksiniz.
2.  **Uçuş Kontrolü** panelinden **SİSTEMİ BAŞLAT (ARM)** butonuna basın.
3.  Simülasyon konsolunda motorların çalıştığını teyit edin.
4.  Mission Planner haritasında drone'un hareketlerini izleyin; SkyGuard AI haritası ile senkronize olmalıdır.

## 5. Gerçek Donanım
Gerçek bir Pixhawk'a bağlanmak için:
1.  Telemetri radyosunu USB portuna takın.
2.  Bağlantı adresi olarak COM portunu girin: `com3` (Baud: 57600).
3.  Bağlanın!
