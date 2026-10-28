# Data directory

Data proyek **TextScope**: klasifikasi emosi teks Bahasa Indonesia + evaluasi lintas domain.

## Struktur folder

| Folder | Isi | Di-commit? |
|---|---|---|
| `raw/` | Salinan sumber asli, tidak diubah | Tidak |
| `interim/` | Data setelah pembersihan awal | Tidak |
| `processed/` | Data final untuk modeling | Tidak (simpan di Google Drive bersama) |

```
data/
├── raw/
│   ├── emosi_opini_publik/   AngerData.csv, FearData.csv, JoyData.csv,
│   │                         LoveData.csv, NeutralData.csv, SadData.csv
│   └── emot/                 train_preprocess.csv, valid_preprocess.csv, test_preprocess.csv
├── interim/
└── processed/                emosi_gabungan.csv, emosi_bersih.csv, emot_lintas.csv,
                              train.csv, valid.csv, test.csv
```

Data mentah dan hasil olahan tidak boleh masuk GitHub. Jangan unggah API key, cookie, atau kredensial apa pun.

## Sumber dan lisensi

| Dataset | Kelas | Fungsi | Lisensi |
|---|---|---|---|
| Emotion Dataset from Indonesian Public Opinion | 6: anger, fear, joy, love, sad, neutral | **Dataset utama** (latih, validasi, uji) | CC-BY-NC-ND 4.0 |
| EmoT (IndoNLU) | 5: anger, fear, joy, love, sad (tanpa neutral) | **Uji lintas domain** saja, tidak dipakai melatih | `ISI: salin dari repo IndoNLU` |

- Tautan sumber dataset utama: `ISI`
- Tautan sumber EmoT: `ISI`
- Tanggal unduh: `ISI`

Lisensi NC (NonCommercial) dan ND (NoDerivatives) berarti data hanya dipakai untuk keperluan akademik dan tidak disebarluaskan ulang.

## Format file mentah

- **Dataset utama:** satu file per kelas, dua kolom dipisah **TAB** (`Tweet<TAB>Label`), tanpa tanda kutip. Teks boleh mengandung koma dan tanda kutip, sehingga file ini **tidak boleh dibaca dengan `pd.read_csv` biasa**. Label diambil dari nama file dan dicocokkan dengan kolom Label.
- **EmoT:** CSV biasa dengan kolom `tweet` dan `label` (label asli: `anger`, `fear`, `happy`, `love`, `sadness`).

## File di `processed/`

| File | Isi | Baris |
|---|---|---|
| `emosi_gabungan.csv` | Semua baris dataset utama (6 file digabung), tanpa filter | 7.105 |
| `emosi_bersih.csv` | Teks dibersihkan, tanpa duplikat, tanpa teks berlabel konflik | 7.031 |
| `emot_lintas.csv` | EmoT, label dipetakan ke skema utama, khusus uji lintas domain | 4.379 |
| `train.csv` | Split stratified dari `emosi_bersih.csv` | 4.921 |
| `valid.csv` | Split stratified dari `emosi_bersih.csv` | 1.055 |
| `test.csv` | Split stratified dari `emosi_bersih.csv` | 1.055 |

### Skema kolom

| Kolom | Keterangan |
|---|---|
| `text` | Teks yang sudah dibersihkan (huruf besar/kecil tidak diubah) |
| `label` | `anger`, `fear`, `joy`, `love`, `sad`, `neutral` (EmoT tanpa `neutral`) |
| `source` | Hanya di `emosi_gabungan.csv`: nama file asal |

Pemetaan label EmoT ke skema utama: `happy → joy`, `sadness → sad`.

## Sebaran label

| Kelas | Gabungan | Bersih | Train | Valid | Test | EmoT |
|---|---:|---:|---:|---:|---:|---:|
| anger | 1.135 | 1.123 | 786 | 168 | 169 | 1.099 |
| fear | 911 | 905 | 633 | 136 | 136 | 641 |
| joy | 1.275 | 1.255 | 878 | 189 | 188 | 1.009 |
| love | 760 | 754 | 528 | 113 | 113 | 636 |
| sad | 1.022 | 1.008 | 706 | 151 | 151 | 994 |
| neutral | 2.002 | 1.986 | 1.390 | 298 | 298 | 0 |
| **Total** | **7.105** | **7.031** | **4.921** | **1.055** | **1.055** | **4.379** |

Kelas terbesar (`neutral`) dan terkecil (`love`) pada data bersih berbanding sekitar 2,63 : 1. Karena tidak seimbang, metrik utama proyek adalah **Macro F1**.

## Cara membuat data

1. `notebooks/01_preprocessing_data.ipynb` menghasilkan tiga file: `emosi_gabungan.csv`, `emosi_bersih.csv`, `emot_lintas.csv`.
2. `python src/split_data.py` menghasilkan `train.csv`, `valid.csv`, `test.csv` (stratified, seed tetap, dicek tanpa teks yang sama di dua split).
3. `notebooks/02_eda.ipynb` membuat analisis eksplorasi; grafik di `reports/figures/`, tabel di `reports/results/`.

Jalankan urutan ini dari awal bila data mentah berubah. Jangan menjalankan ulang split tanpa sepengetahuan tim, karena skor antar model hanya comparable pada split yang sama.

## Preprocessing

Dilakukan di notebook 01, berurutan:

1. Normalisasi Unicode (NFKC).
2. Buang placeholder `[USERNAME]`, `[URL]`, `[RT]`, `[HASHTAG]`, serta URL dan mention `@`.
3. Anonimisasi: buang nomor telepon dan NIM.
4. Pendekkan huruf berulang lebih dari dua kali (`senaaang` → `senaang`), rapikan spasi.
5. Buang teks kosong.
6. Buang **semua** baris dari teks yang punya label berbeda (konflik), lalu buang duplikat (sisakan satu). Pembanding memakai huruf kecil dan spasi yang dirapikan.
7. Untuk EmoT: petakan label, lalu buang teks yang sama dengan dataset utama (agar evaluasi lintas domain tidak terlalu optimis). Hasilnya 0 teks yang tumpang tindih.

| Tahap | Dataset utama | EmoT |
|---|---:|---:|
| Awal | 7.105 | 4.401 |
| Setelah buang label konflik | 7.082 (11 teks unik) | 4.399 (1 teks unik) |
| Setelah buang duplikat | 7.031 | 4.379 |

**Sengaja belum dilakukan:** huruf kecil seluruhnya, normalisasi kata gaul, stemming, dan penghapusan stopword. Ini bagian eksperimen Minggu 12 dan dicatat di tabel percobaan.

## Catatan kualitas data

- Masih ada noise label: teks pendek yang sama bisa muncul dengan label berbeda (misalnya joy vs neutral). Yang ketahuan sudah dibuang, tetapi noise yang tidak identik tetap ada.
- Panjang teks berbeda antar kelas (median `love` sekitar 19 kata, `fear` dan `joy` sekitar 9), sehingga panjang bisa menjadi jalan pintas bagi model.
- EmoT lebih panjang daripada dataset utama (median sekitar 28 vs 13 kata).
- Teks 3 kata atau kurang sekitar 8,5% dari train.

## Privasi

- Username, nomor telepon, dan NIM dihapus oleh preprocessing. **Nama orang tidak dihapus.**
- Sebelum mengutip contoh teks di laporan atau slide, anonimkan lagi nama orang dan samarkan kata kasar.
- Jangan membagikan data mentah di luar tim.
