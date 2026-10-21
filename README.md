# Menfess Radar

**Menfess Radar** adalah proyek Sains Data Terapan untuk menganalisis topik pada teks menfess, memantau tren topik dari waktu ke waktu, dan memprediksi kemungkinan sebuah menfess memperoleh balasan. Hasil analisis disajikan melalui dashboard web interaktif.

> **Status:** Kerangka awal proyek. Sumber data, definisi target prediksi, dan model final perlu ditetapkan serta divalidasi oleh tim.

## Tujuan

1. Mengumpulkan dan mengeksplorasi data menfess yang diperoleh secara sah.
2. Membersihkan teks dan menyiapkan fitur untuk analisis.
3. Mengidentifikasi kelompok atau topik menfess serta menginterpretasikan hasilnya.
4. Menganalisis perubahan volume topik berdasarkan waktu.
5. Melatih dan mengevaluasi model untuk memprediksi apakah menfess mendapat balasan.
6. Menyajikan ringkasan, visualisasi, dan hasil prediksi melalui dashboard.

## Fitur Utama

- Eksplorasi dan preprocessing teks.
- Pemodelan topik menggunakan metode yang sesuai dengan karakteristik data, seperti TF-IDF dengan clustering atau BERTopic.
- Analisis tren topik berdasarkan tanggal atau waktu.
- Prediksi kemungkinan menfess memperoleh balasan menggunakan label target yang didefinisikan secara eksplisit.
- Evaluasi model dan visualisasi interaktif melalui dashboard web.

## Struktur Repositori

```text
project-sistem-cerdas/
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
│   └── README.md
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

*Catatan: Struktur di atas merupakan struktur yang direncanakan. Sesuaikan dengan file yang benar-benar tersedia di repositori.*

## Persiapan Lingkungan

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

## Menjalankan Dashboard

Setelah `dashboard/app.py` dan komponen yang diperlukan tersedia, jalankan:

```bash
streamlit run dashboard/app.py
```

## Metodologi dan Evaluasi

### Analisis Topik

Evaluasi dilakukan melalui kombinasi metrik kuantitatif dan pemeriksaan kualitatif. Jika menggunakan clustering, silhouette score dapat dipertimbangkan apabila sesuai dengan metode dan representasi datanya. Interpretasikan topik berdasarkan kata kunci dan contoh teks yang mewakilinya.

### Prediksi Balasan

- Tetapkan label secara eksplisit, misalnya `replied = 1` jika sebuah menfess memperoleh setidaknya satu balasan dalam jendela observasi yang ditentukan, dan `replied = 0` jika tidak.
- Hindari fitur yang baru diketahui setelah balasan terjadi karena dapat menyebabkan kebocoran target (*target leakage*).
- Pisahkan data berdasarkan waktu jika model ditujukan untuk memprediksi menfess baru.
- Bandingkan hasil model dengan baseline sederhana.
- Laporkan metrik yang sesuai, seperti precision, recall, F1-score, PR-AUC, dan confusion matrix.
- Perhatikan ketidakseimbangan kelas saat mengevaluasi hasil prediksi.

## Tata Kelola Data

- Pastikan pengambilan dan penggunaan data mematuhi ketentuan platform serta izin yang berlaku.
- Jangan mengunggah token, cookie, kredensial, atau data pribadi dan sensitif ke GitHub.
- Anonimkan identitas bila diperlukan dan batasi akses terhadap data mentah.
- Dataset asli tidak disertakan secara otomatis dalam repositori. Lihat [`data/README.md`](data/README.md) untuk panduan penempatan data.

## Kontribusi Tim

1. Buat branch untuk pekerjaan masing-masing, misalnya `feat/topic-modeling` atau `feat/reply-prediction`.
2. Buat perubahan secara bertahap dengan pesan commit yang jelas.
3. Jalankan pengujian sebelum menggabungkan perubahan.
4. Jangan commit dataset besar, file model berukuran besar, atau kredensial.

## Status Pengembangan

Kerangka folder dan dokumentasi awal disiapkan terlebih dahulu. Notebook eksperimen, modul Python, pengujian, serta dashboard akan diimplementasikan setelah format dataset, sumber data, dan definisi target prediksi disepakati oleh tim.