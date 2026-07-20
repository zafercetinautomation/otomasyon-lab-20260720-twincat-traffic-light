# TwinCAT Trafik Lambası

Beckhoff TwinCAT 3 üzerinde Structured Text kullanarak araç ve yaya ışıklarını
bir durum makinesiyle yöneten başlangıç düzeyi PLC eğitim projesi.

Proje iki parçadan oluşur:

- `plc/MAIN.st`: TwinCAT 3 için sembolik giriş/çıkış kullanan PLC örneği
- `src/main.py`: Aynı durum geçişlerini donanım olmadan deneyebileceğiniz Python simülasyonu

## Öğrenme hedefleri

- `CASE` ile durum makinesi kurmak
- `TON` zamanlayıcısını faz geçişlerinde kullanmak
- Çıkışları her çevrim güvenli varsayılanlara çekmek
- Normal çalışma ile acil durum davranışını ayırmak
- PLC mantığını küçük otomatik testlerle doğrulamak

## Durumlar

| Durum | Araç ışığı | Yaya ışığı | Süre |
|---|---|---|---:|
| Araç yeşil | Yeşil | Kırmızı | 10 sn |
| Araç sarı | Sarı | Kırmızı | 3 sn |
| Tümü kırmızı | Kırmızı | Kırmızı | 2 sn |
| Yaya yeşil | Kırmızı | Yeşil | 7 sn |
| Yaya yanıp sönme | Kırmızı | Yeşil/Kapalı | 4 sn |

## Python simülasyonunu çalıştırma

Harici paket gerekmez:

```bash
python3 src/main.py
python3 -m unittest discover -s tests -v
```

Örnek çıktı:

```text
 0 sn | arac_yesil | Araç: yeşil | Yaya: kırmızı
10 sn | arac_sari  | Araç: sarı  | Yaya: kırmızı
13 sn | tumu_kirmizi | Araç: kırmızı | Yaya: kırmızı
```

## TwinCAT 3'e aktarma

1. TwinCAT XAE içinde yeni bir **TwinCAT XAE Project** oluşturun.
2. PLC düğümüne **Standard PLC Project** ekleyin.
3. Projede oluşan `MAIN (PRG)` nesnesini açın.
4. `plc/MAIN.st` içindeki tip bildirimini bir DUT'a, program bölümünü MAIN'e aktarın.
5. `Check all objects` ile sözdizimini kontrol edin.
6. Önce yerel runtime veya simülasyon değişkenleriyle deneyin.

Beckhoff'un resmî başlangıç rehberi:
[İlk TwinCAT 3 PLC projesi](https://infosys.beckhoff.com/content/1033/tc3_system/2525041803.html)

## Deneyler

- Araç yeşil süresini 10 saniyeden 6 saniyeye düşürün.
- Yaya fazından önce ikinci bir tümü-kırmızı durumu ekleyin.
- Yaya yeşil çıkışını son iki saniyede yanıp söndürün.
- Acil durum girişinde bütün yeşil çıkışların kapandığını test edin.
- Faz sürelerini bir yapı veya global değişken listesine taşıyın.

## Değişken özeti

| Değişken | Tür | Açıklama |
|---|---|---|
| `bEnable` | `BOOL` | Çevrimi etkinleştirir |
| `bEmergencyStop` | `BOOL` | Eğitim amaçlı acil durum girişi |
| `bVehicleRed/Yellow/Green` | `BOOL` | Araç ışığı çıkışları |
| `bPedestrianRed/Green` | `BOOL` | Yaya ışığı çıkışları |
| `eState` | `E_TrafficState` | Geçerli faz |

## Güvenlik uyarısı

Bu proje **yalnızca eğitim ve simülasyon amaçlıdır**. Gerçek trafik sistemi,
makine veya proses üzerinde kullanılmamalıdır. Gerçek uygulamada risk analizi,
mevzuat değerlendirmesi, emniyet doğrulaması, arıza analizi ve yetkin uzman
incelemesi gerekir. Buradaki standart PLC kodu, sertifikalı emniyet PLC'si veya
emniyet fonksiyonunun yerine geçmez.

## Lisans

MIT
