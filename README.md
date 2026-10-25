# TextScope

**TextScope** adalah proyek Sains Data Terapan yang berfokus pada analisis teks menggunakan pendekatan machine learning. Proyek ini mencakup pemodelan topik, klasifikasi emosi, analisis tren topik, serta prediksi kemungkinan sebuah unggahan memperoleh balasan.

Proyek ini dikembangkan sebagai bagian dari mata kuliah Sistem Cerdas dengan tujuan mengolah data teks yang tidak terstruktur menjadi informasi yang bermakna melalui preprocessing, pemodelan, evaluasi, dan visualisasi interaktif.

## Tujuan

1. Mengumpulkan dan mengeksplorasi dataset dari sumber yang dapat dipertanggungjawabkan.
2. Melakukan preprocessing teks untuk mempersiapkan data bagi proses analisis.
3. Mengidentifikasi topik dan pola dalam teks menggunakan metode pemodelan topik yang sesuai.
4. Menganalisis perubahan frekuensi topik berdasarkan waktu.
5. Mengembangkan dan mengevaluasi model untuk memprediksi kemungkinan sebuah unggahan memperoleh balasan.
6. Mengembangkan model klasifikasi emosi dan mengevaluasi kemampuannya pada dataset yang berbeda.
7. Menyajikan hasil analisis dan prediksi melalui dashboard interaktif.

## Fitur Utama

- **Preprocessing Teks:** Membersihkan dan menormalisasi teks sebelum analisis.
- **Pemodelan Topik:** Mengidentifikasi kelompok teks yang memiliki keterkaitan menggunakan metode seperti TF-IDF dengan clustering atau BERTopic.
- **Analisis Tren Topik:** Mengamati perubahan frekuensi topik dari waktu ke waktu.
- **Prediksi Balasan:** Memprediksi kemungkinan sebuah unggahan memperoleh balasan berdasarkan target yang telah didefinisikan.
- **Klasifikasi Emosi:** Mengklasifikasikan teks ke dalam kategori emosi.
- **Evaluasi Model:** Mengukur performa model menggunakan metrik evaluasi yang sesuai.
- **Dashboard Interaktif:** Menyajikan hasil analisis dan prediksi dalam bentuk visualisasi.

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

Script pengunduhan menggabungkan data dari enam berkas emosi menjadi satu dataset. Selanjutnya, dilakukan pembersihan teks duplikat dan teks yang memiliki label berbeda.

### 2. Dataset Evaluasi Lintas Domain

Dataset EmoT dari IndoNLU digunakan untuk menguji kemampuan generalisasi model pada sumber teks yang berbeda.

Pemetaan label yang digunakan dalam proyek ini mencakup lima kategori:

- Anger
- Fear
- Joy
- Love
- Sad

Kategori netral tidak disertakan dalam pemetaan EmoT. Oleh karena itu, evaluasi lintas dataset perlu memperhatikan kesesuaian label dan perbedaan distribusi data.

### 3. Data Demonstrasi

Data menfess atau unggahan media sosial yang diperoleh secara sah dapat digunakan sebagai contoh penerapan model pada data nyata.

Data tersebut **tidak digunakan sebagai dataset pelatihan maupun pengujian resmi** untuk klasifikasi emosi. Tanpa label acuan, hasil prediksi hanya digunakan untuk demonstrasi dan tidak dapat dijadikan dasar penghitungan akurasi atau metrik evaluasi lainnya.

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
├── src/
│   └── download_data.py
├── models/
│   └── README.md
├── reports/
│   ├── figures/
│   └── results/
├── dashboard/
├── tests/
└── docs/
```

Struktur tersebut menggambarkan direktori utama proyek. Isi setiap direktori dapat berkembang sesuai kebutuhan implementasi.

## Persiapan Lingkungan

Proyek disarankan menggunakan Python 3.10 atau 3.11, dengan tetap memperhatikan kompatibilitas dependensi pada `requirements.txt`.

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
| `emosi_bersih.csv` | Data yang telah dibersihkan dari teks duplikat dan teks dengan konflik label. |
| `emot_lintas.csv` | Dataset EmoT yang telah disiapkan untuk evaluasi lintas domain, termasuk informasi pembagian data aslinya. |

Berkas mentah disimpan pada direktori:

```text
data/raw/emosi_opini_publik/
data/raw/emot/
```

Script melewati pengunduhan jika berkas terkait sudah tersedia. Apabila pengunduhan sebelumnya terputus, periksa kelengkapan berkas sebelum menjalankan ulang proses.

Untuk memeriksa hasil pengunduhan, jalankan:

```powershell
Get-ChildItem .\data\raw -Recurse
Get-ChildItem .\data\processed
```

Dataset disimpan secara lokal dan tidak disertakan dalam repositori GitHub. Informasi mengenai sumber, lisensi, dan pengelolaan dataset dapat dilihat pada [`data/README.md`](data/README.md).

## Metodologi dan Evaluasi

### Klasifikasi Emosi

Evaluasi klasifikasi emosi dilakukan melalui dua tahap.

**Evaluasi utama**

Evaluasi utama menggunakan data uji yang berasal dari dataset utama. Metrik yang dapat digunakan meliputi:

- Macro F1-score sebagai salah satu metrik utama.
- Precision, recall, dan F1-score untuk setiap kelas.
- Confusion matrix untuk menganalisis kesalahan klasifikasi.

**Evaluasi lintas dataset**

Model diuji menggunakan EmoT untuk mengamati perubahan performa ketika diterapkan pada sumber teks yang berbeda. Hasilnya dilaporkan secara terpisah dari evaluasi utama dengan mempertimbangkan perbedaan domain, gaya bahasa, dan distribusi label.

**Demonstrasi pada data nyata**

Data menfess dapat digunakan untuk menunjukkan contoh prediksi model. Namun, data tanpa label acuan tidak digunakan untuk menghasilkan skor evaluasi resmi.

### Pemodelan Topik

Pemodelan topik digunakan untuk mengidentifikasi tema dan kelompok teks yang saling berkaitan.

Metode evaluasi disesuaikan dengan pendekatan yang digunakan. Jika menerapkan clustering, metrik seperti silhouette score dapat dipertimbangkan apabila sesuai. Interpretasi juga dilakukan secara kualitatif melalui kata kunci dan contoh teks yang mewakili setiap kelompok.

### Prediksi Balasan

Pengembangan model prediksi balasan memperhatikan beberapa aspek berikut:

1. Mendefinisikan target secara eksplisit, misalnya apakah sebuah unggahan memperoleh setidaknya satu balasan dalam jangka waktu pengamatan tertentu.
2. Menghindari penggunaan fitur yang baru tersedia setelah balasan terjadi untuk mencegah kebocoran target (*target leakage*).
3. Memisahkan data berdasarkan waktu apabila model ditujukan untuk memprediksi unggahan baru.
4. Membandingkan performa model dengan metode dasar (*baseline*).
5. Melaporkan metrik yang relevan, seperti precision, recall, F1-score, PR-AUC, dan confusion matrix.

## Tata Kelola Data

- Memastikan pengumpulan dan penggunaan data sesuai dengan ketentuan sumber, lisensi, dan izin yang berlaku.
- Tidak mengunggah API key, cookie, kredensial, atau informasi sensitif ke GitHub.
- Melakukan anonimisasi terhadap informasi identitas pada data demonstrasi apabila diperlukan.
- Menghindari publikasi teks asli yang dapat mengidentifikasi pemilik akun tanpa dasar penggunaan yang sesuai.
- Memisahkan data demonstrasi dari dataset pelatihan dan evaluasi resmi.
- Memeriksa ketentuan lisensi sebelum menggunakan atau mendistribusikan ulang dataset.

## Kontribusi Tim

1. Membuat branch terpisah untuk setiap pekerjaan, misalnya `feat/topic-modeling` atau `feat/reply-prediction`.
2. Melakukan perubahan secara bertahap dengan pesan commit yang jelas.
3. Menjalankan pengujian yang relevan sebelum menggabungkan perubahan.
4. Tidak melakukan commit terhadap dataset lokal, artefak model berukuran besar, atau kredensial.
5. Memperbarui dokumentasi apabila terdapat perubahan pada struktur proyek, metodologi, atau cara menjalankan aplikasi.

## Status Pengembangan

Proyek saat ini telah memiliki struktur repositori serta script untuk mengunduh dan menyiapkan dataset klasifikasi emosi.

Tahap pengembangan selanjutnya mencakup eksplorasi data, eksperimen pemodelan, evaluasi, implementasi dashboard, dan dokumentasi hasil berdasarkan eksperimen yang telah divalidasi.

TextScope merupakan proyek akademik yang dikembangkan secara bertahap. Klaim performa model dan status penyelesaian fitur akan disesuaikan dengan hasil implementasi dan pengujian yang dapat direproduksi.
