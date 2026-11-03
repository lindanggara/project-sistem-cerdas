# TextScope

**TextScope** adalah proyek Sains Data Terapan yang berfokus pada **klasifikasi emosi teks Bahasa Indonesia** menggunakan pendekatan machine learning. Proyek ini mencakup preprocessing data, eksplorasi data, pengembangan model klasifikasi, evaluasi performa, serta visualisasi interaktif.

Proyek ini dikembangkan sebagai bagian dari mata kuliah Sistem Cerdas dengan tujuan mengolah data teks yang tidak terstruktur menjadi informasi bermakna melalui penerapan metode machine learning dan natural language processing (NLP).

## Tujuan

1. Mengumpulkan dan mengeksplorasi dataset dari sumber yang dapat dipertanggungjawabkan.
2. Melakukan preprocessing teks untuk mempersiapkan data bagi proses analisis.
3. Mengembangkan model klasifikasi emosi menggunakan pendekatan machine learning klasik dan transformer.
4. Mengevaluasi performa model pada dataset utama serta menguji kemampuan generalisasinya menggunakan dataset lintas domain (EmoT).
5. Menyajikan hasil analisis dan prediksi emosi melalui dashboard interaktif.

## Fitur Utama

- **Preprocessing Teks:** Membersihkan dan menormalisasi teks, termasuk penanganan kata tidak baku dan kata gaul.
- **Klasifikasi Emosi:** Mengklasifikasikan teks ke dalam enam kategori emosi, yaitu anger, fear, joy, love, sad, dan neutral.
- **Evaluasi Model:** Mengukur performa model menggunakan Macro F1-score, precision, recall, dan confusion matrix.
- **Evaluasi Lintas Domain:** Menguji kemampuan generalisasi model menggunakan dataset EmoT dari sumber teks yang berbeda.
- **Dashboard Interaktif:** Menyajikan hasil prediksi dan visualisasi data dalam bentuk aplikasi web.

Ketersediaan setiap fitur mengikuti tahap implementasi dan hasil eksperimen yang telah divalidasi.

## Dataset

Dataset dalam TextScope dipisahkan berdasarkan tujuan penggunaannya.

### 1. Dataset Utama Klasifikasi Emosi

*Emotion Dataset from Indonesian Public Opinion* digunakan sebagai dataset utama untuk pengembangan dan evaluasi model klasifikasi emosi.

Dataset ini mencakup enam kategori emosi:

- Anger
- Fear
- Joy
- Love
- Sad
- Neutral

Script pengunduhan menggabungkan data dari enam berkas emosi menjadi satu dataset. Selanjutnya, dilakukan pembersihan teks duplikat dan teks yang memiliki label berbeda untuk menjaga konsistensi data.

### 2. Dataset Evaluasi Lintas Domain

Dataset EmoT dari IndoNLU digunakan untuk menguji kemampuan generalisasi model pada sumber teks yang berbeda.

Pemetaan label yang digunakan dalam proyek ini mencakup lima kategori:

- Anger
- Fear
- Joy
- Love
- Sad

Kategori netral tidak disertakan dalam pemetaan EmoT. Oleh karena itu, evaluasi lintas dataset dilakukan dengan memperhatikan kesesuaian label dan perbedaan distribusi data.

### 3. Data Demonstrasi

Data menfess atau unggahan media sosial yang diperoleh secara sah dapat digunakan sebagai contoh penerapan model pada data nyata.

Data tersebut **tidak digunakan sebagai dataset pelatihan maupun pengujian resmi** untuk klasifikasi emosi. Tanpa label acuan, hasil prediksi hanya digunakan untuk demonstrasi dan tidak dapat dijadikan dasar penghitungan akurasi maupun metrik evaluasi lainnya.

Sebelum digunakan, data demonstrasi perlu diperiksa dari sisi privasi dan dianonimkan apabila mengandung informasi yang dapat mengidentifikasi seseorang.

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
│   ├── 01_preprocessing_data.ipynb
│   └── 02_eda.ipynb
├── src/
│   └── download_data.py
├── models/
│   └── README.md
├── reports/
│   ├── figures/
│   └── results/
│       └── eksperimen.md
├── dashboard/
├── tests/
└── docs/
    ├── panduan/
    │   └── PANDUAN_TIM.md
    └── laporan/
        ├── 01_data_eda.md
        └── 02_model_klasik.md
```

Struktur tersebut menggambarkan direktori utama proyek. Beberapa direktori dan berkas dapat dikembangkan sesuai kebutuhan implementasi.

## Persiapan Lingkungan

Proyek disarankan menggunakan Python 3.10 atau 3.11 dengan memperhatikan kompatibilitas dependensi yang tercantum dalam `requirements.txt`.

### Windows (PowerShell)

Jalankan perintah berikut dari direktori utama proyek:

```powershell
cd "D:\Project Sistem Cerdas"

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Jika virtual environment sudah tersedia, cukup aktifkan lingkungan tersebut tanpa membuatnya kembali.

## Mengunduh dan Menyiapkan Dataset

Setelah dependensi terpasang, jalankan script berikut dari direktori utama proyek:

```powershell
python .\src\download_data.py
```

Script akan mengunduh dataset utama klasifikasi emosi dan dataset EmoT, kemudian menyimpan berkas hasil pengolahan ke direktori `data/`.

### Berkas yang Dihasilkan

| Berkas | Keterangan |
|---|---|
| `emosi_gabungan.csv` | Gabungan data dari enam kategori emosi pada dataset utama. |
| `emosi_bersih.csv` | Data yang telah dibersihkan dari teks duplikat dan konflik label. |
| `emot_lintas.csv` | Dataset EmoT yang telah disiapkan untuk evaluasi lintas domain, termasuk informasi pembagian data aslinya. |
| `train.csv` | Data pelatihan model. |
| `valid.csv` | Data validasi model. |
| `test.csv` | Data pengujian model. |

Berkas mentah disimpan pada direktori:

```text
data/raw/emosi_opini_publik/
data/raw/emot/
```

Dataset disimpan secara lokal dan tidak disertakan dalam repositori GitHub.

Untuk memeriksa hasil pengunduhan, jalankan:

```powershell
Get-ChildItem .\data\raw -Recurse
Get-ChildItem .\data\processed
```

Informasi mengenai sumber, lisensi, dan pengelolaan dataset dapat dilihat pada [`data/README.md`](data/README.md).

## Metodologi dan Evaluasi

### Klasifikasi Emosi

Pengembangan dan evaluasi klasifikasi emosi dilakukan melalui dua tahap utama.

**1. Evaluasi Utama**

Evaluasi utama menggunakan data uji yang berasal dari dataset utama. Tahap ini bertujuan mengukur kemampuan model dalam mengklasifikasikan emosi pada data yang belum pernah digunakan selama pelatihan.

Metrik evaluasi yang digunakan meliputi:

- **Macro F1-score:** Metrik utama untuk mengukur keseimbangan performa klasifikasi pada seluruh kelas.
- **Precision:** Mengukur ketepatan prediksi pada setiap kategori emosi.
- **Recall:** Mengukur kemampuan model dalam menemukan seluruh data pada setiap kategori.
- **Confusion Matrix:** Menganalisis pola kesalahan klasifikasi antar kategori emosi.

**2. Evaluasi Lintas Dataset**

Model diuji menggunakan dataset EmoT untuk mengamati kemampuan generalisasi ketika diterapkan pada sumber teks yang berbeda.

Hasil evaluasi lintas dataset dilaporkan secara terpisah dari evaluasi utama dengan mempertimbangkan perbedaan domain, gaya bahasa, serta distribusi label.

**3. Demonstrasi pada Data Nyata**

Data menfess dapat digunakan untuk menunjukkan contoh penerapan model pada teks media sosial. Namun, data tanpa label acuan tidak digunakan untuk menghasilkan skor evaluasi resmi.

## Tata Kelola Data

Pengelolaan data dalam proyek TextScope memperhatikan beberapa prinsip berikut:

- Memastikan pengumpulan dan penggunaan data sesuai dengan ketentuan sumber, lisensi, dan izin yang berlaku.
- Tidak mengunggah API key, cookie, kredensial, atau informasi sensitif ke GitHub.
- Melakukan anonimisasi terhadap informasi identitas pada data demonstrasi apabila diperlukan.
- Memisahkan data demonstrasi dari dataset pelatihan dan evaluasi resmi.
- Menghindari publikasi teks asli yang dapat mengidentifikasi pemilik akun tanpa dasar penggunaan yang sesuai.
- Memeriksa ketentuan lisensi sebelum menggunakan atau mendistribusikan ulang dataset.

## Kontribusi Tim

Untuk menjaga konsistensi pengembangan proyek, setiap anggota tim mengikuti ketentuan berikut:

1. Membuat branch terpisah untuk setiap pekerjaan, misalnya `feat/baseline` atau `feat/indobert`.
2. Melakukan perubahan secara bertahap dengan pesan commit yang jelas.
3. Menjalankan pengujian yang relevan sebelum menggabungkan perubahan.
4. Tidak melakukan commit terhadap dataset lokal, artefak model berukuran besar, atau kredensial.
5. Memperbarui dokumentasi apabila terdapat perubahan pada struktur proyek, metodologi, atau cara menjalankan aplikasi.

## Dokumentasi & Hasil

Dokumentasi pengembangan dan hasil eksperimen TextScope dapat diakses melalui beberapa dokumen berikut.

| Dokumen | Deskripsi |
|---|---|
| [📊 Tabel Eksperimen](reports/results/eksperimen.md) | Catatan lengkap dan perbandingan seluruh percobaan model. |
| [📘 Panduan Tim](docs/panduan/PANDUAN_TIM.md) | Jadwal, pembagian tugas, dan aturan kerja tim. |
| [📁 Data README](data/README.md) | Sumber, lisensi, dan deskripsi dataset. |
| [🔬 Laporan EDA](docs/laporan/01_data_eda.md) | Hasil eksplorasi dan analisis dataset. |
| [🤖 Laporan Model Klasik](docs/laporan/02_model_klasik.md) | Metodologi, eksperimen, dan hasil evaluasi model machine learning klasik. |

### Hasil Eksperimen

**Hasil sementara per 3 November 2026**

| Model | Macro F1 (Test) | Status |
|---|---:|---|
| **Logistic Regression + Normalisasi + Class Weighting** | **0.7155** | Model klasik terbaik |
| SVM + Normalisasi + Class Weighting | 0.7075 | Selesai |
| IndoBERT | Menunggu hasil | Dalam pengembangan (PIC: Chila) |
| IndoBERTweet | Menunggu hasil | Dalam pengembangan (PIC: Chila) |

Hasil eksperimen tersebut merupakan hasil pengujian pada dataset utama. Perbandingan performa dilakukan menggunakan data uji dan konfigurasi eksperimen yang telah ditetapkan.

## Status Pengembangan

Proyek saat ini telah menyelesaikan beberapa tahapan utama, yaitu **pengumpulan dan pembersihan data**, **eksplorasi data (EDA)**, serta **eksperimen model machine learning klasik** dengan hasil terbaik sementara berupa Macro F1-score sebesar **0.7155**.

Tahap pengembangan selanjutnya mencakup **pelatihan dan evaluasi model transformer (IndoBERT dan IndoBERTweet)**, **evaluasi lintas domain menggunakan EmoT**, serta **implementasi dashboard interaktif**.

TextScope merupakan proyek akademik yang dikembangkan secara bertahap. Klaim performa model dan status penyelesaian fitur akan disesuaikan dengan hasil implementasi dan pengujian yang dapat direproduksi.