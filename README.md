# Endüstriyel Körük Konumlandırma ve Dolum Tespiti

Bu proje, endüstriyel bir dolum sürecinde kullanılan körüğün dolum noktasına doğru şekilde konumlandırılmasına yardımcı olmak amacıyla geliştirilmiş bir bilgisayarlı görü sistemidir.

Sistem, farklı açılardan görüntü alan iki endüstriyel kamera kullanarak körük ve kapak durumlarını tespit eder. YOLO ile gerçekleştirilen nesne tespitleri, Python ve OpenCV kullanılarak koordinat ve geometrik analizlerle işlenir.

## Projenin Amacı

Körüğün dolum noktasına doğru şekilde hizalanabilmesi için:

- Körüğün konumunu belirlemek
- Körüğün kapağa göre sağ-sol konumunu analiz etmek
- Körüğün yukarı-aşağı konumunu analiz etmek
- Körüğün dolum noktasıyla hizalanıp hizalanmadığını belirlemek
- Dolum durumunu gerçek zamanlı olarak tespit etmek

amaçlanmaktadır.

## Sistem Yapısı

Proje iki farklı kamera görüntüsünü kullanan iki ayrı görüntü işleme modülünden oluşmaktadır.

### Detection – Yan Kamera

`detection` klasörü, yan açıdan görüntü alan kameranın görüntülerini işler.

Bu modülde körük tespit edilerek görüntü üzerindeki koordinatları ve geometrik konumu analiz edilir.

Elde edilen bilgiler kullanılarak körüğün:

- Yukarı hareket etmesi
- Aşağı hareket etmesi

gereken durumların belirlenmesine yönelik konum bilgileri elde edilir.

### Detection2 – Üst Kamera

`detection2` klasörü, yukarıdan görüntü alan ikinci kameranın görüntülerini işler.

Bu modülde:

- `bellows`
- `cover_open`

nesneleri tespit edilir.

Körüğün kapağa göre konumu analiz edilerek **sağ-sol hareketi** için gerekli koordinat bilgileri elde edilir. Ayrıca kapağın açık veya kapalı olduğu belirlenir.

## Genel Çalışma Mantığı

```text
                  İKİ KAMERA
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      YAN KAMERA              ÜST KAMERA
      detection               detection2
          │                       │
          ▼                       ▼
     Y koordinatı             X koordinatı
          │                       │
          ▼                       ▼
     ↑ Yukarı                  ← Sol
     ↓ Aşağı                   → Sağ
          │                       │
          └───────────┬───────────┘
                      ▼
             KÖRÜK KONUMLANDIRMA
                      │
                      ▼
               DOLUM NOKTASI
                   HİZALAMA      
```
## Sistem Görüntüleri

### Yan Kamera – Körük Konumlandırma

<img width="686" height="382" alt="Ekran görüntüsü 2026-08-27 163321" src="https://github.com/user-attachments/assets/4d1397a7-26cf-42ea-b725-4985000e9763" />
<img width="801" height="443" alt="Ekran görüntüsü 2026-08-27 165947" src="https://github.com/user-attachments/assets/a8230b23-f35a-4184-8188-ed99b44de242" />
Yan açıdan alınan görüntü ile körüğün dikey konumu analiz edilerek
**yukarı-aşağı hareketi** için gerekli bilgiler elde edilir.

### Üst Kamera – Körük ve Kapak Tespiti

<img width="805" height="482" alt="Ekran görüntüsü 2026-08-28 161909" src="https://github.com/user-attachments/assets/e3f652ee-5c6e-4a36-a953-4655e1879601" />
<img width="795" height="465" alt="Ekran görüntüsü 2026-08-27 103303" src="https://github.com/user-attachments/assets/eaec4eef-fd10-44e5-a688-6ce7c80edd8b" />
Yukarıdan alınan görüntü ile körüğün kapağa göre yatay konumu ve
kapak durumu analiz edilerek **sağ-sol hareketi** için gerekli bilgiler elde edilir.
