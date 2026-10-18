# Projek Statistika dan Probabilitas - Kelompok 7 (3TIE)

**Analisis Hubungan Kadar Alkohol dan Keasaman Volatil terhadap Kualitas Anggur Merah Vinho Verde sebagai Dasar Penyusunan Aturan Fuzzy**

Politeknik Caltex Riau - Program Studi Teknik Informatika - T.A 2025/2026

## Anggota Kelompok
| Nama | NIM |
|---|---|
| Salsabilla Dheawan Shenza | 2455301173 |
| Farhan Gusri Fadhilah | 2455301066 |
| Gebi Rovando Rahmanda | 2455301072 |
| Zikra Mahiza Wafiq | 2455301210 |

## Deskripsi
Repository ini berisi data dan program Python untuk Tahap 3 projek, yaitu deskripsi data,
statistika deskriptif, probabilitas empiris, dan visualisasi data pada dataset Red Wine Quality
(1.599 sampel, 12 variabel). Variabel utama: `alcohol`, `volatile acidity`, dan `quality`.

## Sumber Data
Data sekunder: [Red Wine Quality - Kaggle](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009)
(Cortez et al., 2009). Data disimpan pada `3TIE_07_WineQuality-Red.xlsx` (sheet `Dataset`) tanpa mengubah nilai asli.

## Struktur Repository
```
.
├── analisis_wine.py              # program analisis (statistik deskriptif, probabilitas, grafik)
├── 3TIE_07_WineQuality-Red.xlsx  # dataset
├── requirements.txt              # pustaka Python yang dibutuhkan
└── gambar/                       # keluaran program (grafik, tabel CSV, hasil JSON, log keluaran)
```

## Cara Menjalankan
```bash
pip install -r requirements.txt
python analisis_wine.py
```
Jalankan dari folder utama repository agar file Excel terbaca. Hasil grafik dan tabel akan
tersimpan di folder `gambar/`.

## Keluaran Program
- Pemeriksaan data (dimensi, nilai kosong, duplikat)
- Statistika deskriptif: mean, median, modus, rentang, simpangan baku, varians, kuartil, IQR, skewness
- Distribusi frekuensi dan probabilitas empiris skor `quality`
- Identifikasi pencilan (aturan 1,5 x IQR) dan distribusi frekuensi berkelompok
- Grafik: histogram alkohol, histogram keasaman volatil, diagram batang quality, boxplot per skor quality

## Referensi
Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems, 47*(4), 547-553.
