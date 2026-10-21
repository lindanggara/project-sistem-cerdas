# Menfess Radar

**Menfess Radar** adalah proyek Sains Data Terapan untuk menganalisis topik pada teks menfess, memantau tren topik dari waktu ke waktu, dan memprediksi kemungkinan sebuah menfess memperoleh balasan. Hasil analisis disajikan melalui dashboard web.

> Status: kerangka awal proyek. Sumber data, definisi target prediksi, dan model final perlu ditetapkan serta divalidasi oleh tim.

## Tujuan

1. Mengumpulkan dan mengeksplorasi data menfess yang diperoleh secara sah.
2. Membersihkan teks dan menyiapkan fitur untuk analisis.
3. Mengidentifikasi kelompok/topik menfess dan memberi interpretasi pada topik.
4. Menganalisis perubahan volume topik berdasarkan waktu.
5. Melatih dan mengevaluasi model untuk memprediksi apakah menfess mendapat balasan.
6. Menyajikan ringkasan, visualisasi, dan hasil prediksi pada dashboard.

## Fitur utama

- Eksplorasi dan preprocessing teks.
- Pemodelan topik (metode dipilih setelah eksplorasi data, misalnya TF-IDF + clustering atau BERTopic).
- Analisis tren topik berdasarkan tanggal/waktu.
- Klasifikasi kemungkinan dibalas menggunakan label target yang didefinisikan secara eksplisit.
- Evaluasi model dan dashboard interaktif.

## Struktur repositori

```text
menfess-radar/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── README.md
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_topic_modeling.ipynb
│   ├── 04_reply_prediction.ipynb
│   ├── 05_model_evaluation.ipynb
│   └── 06_topic_trend_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── topic_modeling.py
│   ├── reply_prediction.py
│   ├── evaluation.py
│   └── trend_analysis.py
├── models/
├── reports/
│   ├── figures/
│   └── results/
├── dashboard/
│   ├── app.py
│   └── README.md
├── tests/
│   ├── test_preprocessing.py
│   └── test_topic_modeling.py
└── docs/
    ├── proposal.md
    ├── methodology.md
    └── references.md
```

## Persiapan lingkungan

Disarankan menggunakan Python 3.10 atau 3.11 dan virtual environment.

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Menjalankan dashboard

Setelah `dashboard/app.py` dibuat dan data/model yang diperlukan tersedia:

```bash
streamlit run dashboard/app.py
```

## Evaluasi yang disarankan

### Analisis topik

Gunakan kombinasi evaluasi kuantitatif yang sesuai dengan metode (misalnya silhouette score jika clustering memungkinkan) dan pemeriksaan kualitatif terhadap kata kunci serta contoh teks per topik. Jangan menganggap skor tunggal cukup untuk membuktikan kualitas topik.

### Prediksi balasan

- Tetapkan label dengan jelas, misalnya `replied = 1` jika ada balasan dalam jendela observasi yang ditentukan, dan `0` jika tidak.
- Hindari fitur yang baru diketahui setelah balasan terjadi karena dapat menyebabkan kebocoran target (*target leakage*).
- Pisahkan data berdasarkan waktu jika penggunaan model ditujukan untuk memprediksi menfess baru.
- Laporkan baseline dan metrik yang sesuai, seperti precision, recall, F1, PR-AUC, serta confusion matrix. Perhatikan ketidakseimbangan kelas.

## Tata kelola data

- Pastikan pengambilan dan penggunaan data mematuhi ketentuan platform serta izin yang berlaku.
- Jangan mengunggah token, cookie, kredensial, atau data pribadi/sensitif ke GitHub.
- Anonimkan identitas bila diperlukan dan batasi akses pada data mentah.
- Data asli tidak disertakan dalam repositori. Lihat [`data/README.md`](data/README.md) untuk panduan penempatan data.

## Kontribusi tim

1. Buat branch untuk pekerjaan masing-masing, misalnya `feat/topic-modeling` atau `feat/reply-prediction`.
2. Buat perubahan kecil dengan pesan commit yang jelas.
3. Jalankan pengujian sebelum membuat pull request.
4. Jangan commit dataset besar, file model besar, atau kredensial.

## Status komponen

Kerangka folder dan dokumentasi awal disiapkan terlebih dahulu. File notebook, modul Python, pengujian, dan dashboard akan diimplementasikan setelah format dataset dan definisi target disepakati.
