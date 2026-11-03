# Bagian Laporan: Model Klasik & Evaluasi

*Dokumen ini adalah bagian Model Klasik pada laporan akhir TextScope. Ditulis oleh Linda (PJ Model Klasik & Evaluasi).*

## 1. Pendahuluan

Bagian ini menjelaskan pendekatan klasik yang digunakan sebagai *baseline* sebelum beralih ke model transformer. Tujuan utamanya adalah untuk membangun fondasi yang kuat, memahami karakteristik data, dan menyediakan pembanding yang adil (fair comparison) untuk model yang lebih kompleks.

## 2. Metodologi

### 2.1 Preprocessing
- Normalisasi teks (Unicode NFKC).
- Penghapusan placeholder `[USERNAME]`, `[URL]`, dan mention.
- **Normalisasi Kata Gaul (Tambahan dari Linda):** Mengubah singkatan umum (misal: *gak* → *tidak*, *bgt* → *banget*) menggunakan kamus yang didefinisikan pada `src/baseline.py`.

### 2.2 Ekstraksi Fitur (Feature Engineering)
Dua pendekatan TF-IDF yang digunakan:
1.  **TF-IDF Kata (Word-level):** Menggunakan n-gram (1,2) dengan `max_features=10000`.
2.  **TF-IDF Karakter (Char-level):** Menggunakan `analyzer='char_wb'` dengan n-gram (3,5) dan `max_features=5000`. Ini sangat berguna untuk menangkap typo dan singkatan yang tidak ada di kamus.

### 2.3 Model yang Diuji
1.  **Logistic Regression (LogReg):** Model linear yang kuat dan cepat.
2.  **Support Vector Machine (SVM):** Model linear yang mencari hyperplane terbaik.
3.  **Naive Bayes (NB):** Model probabilistik sederhana.

**Penanganan Imbalance:**
Karena distribusi kelas tidak seimbang (`neutral` 28.2% vs `love` 10.7%), diterapkan `class_weight='balanced'` pada LogReg dan SVM. Ini memberikan bobot lebih pada kelas minoritas.

### 2.4 Hyperparameter Tuning
Dilakukan *GridSearchCV* dengan 3-fold cross-validation untuk mencari nilai parameter regularisasi (`C`) terbaik pada LogReg dan SVM.

## 3. Hasil Eksperimen

### 3.1 Evaluasi Utama (Dataset Test)

| Model | Macro F1 (Test) | Catatan |
| :--- | :---: | :--- |
| Baseline LogReg | 0.7108 | Baseline awal |
| LogReg + Normalisasi + Class Weighting | 0.7155 | Peningkatan dari normalisasi |
| **LogReg Tuned (Char TF-IDF + C=1.0)** | **0.7286** | **🏆 Model Klasik Terbaik** |
| SVM Tuned | 0.7251 | — |
| Naive Bayes | 0.5628 | Performa rendah, tidak dilanjutkan |

**Analisis Singkat:**
Peningkatan skor dari 0.7108 menjadi 0.7286 dicapai melalui kombinasi normalisasi kata gaul, ekstraksi fitur karakter, dan tuning hyperparameter. Model LogReg terbukti paling stabil dan memberikan hasil terbaik.

### 3.2 Evaluasi Lintas Domain (EmoT)

| Model | Macro F1 (EmoT) | Catatan |
| :--- | :---: | :--- |
| LogReg Tuned | **0.4142** | Turun drastis dari 0.7286. |

**Analisis Kritis:**
Penurunan performa yang sangat drastis (dari 0.7286 menjadi 0.4142) saat diuji pada dataset EmoT (Twitter) menunjukkan bahwa model klasik **sangat bergantung pada kosakata dan gaya bahasa dataset pelatihan**. Model gagal mengenali singkatan dan *slang* baru yang umum di Twitter. Recall yang sangat rendah (0.3147) mengindikasikan model sering melewatkan emosi yang sebenarnya.

Temuan ini menjadi justifikasi kuat untuk beralih ke model **Transformer (IndoBERT)**, yang diharapkan lebih tahan terhadap perbedaan domain karena kemampuannya memahami konteks kalimat secara lebih mendalam.

### 3.3 Analisis Error (Salah Tebak)

Dari 1.055 data uji, model LogReg Tuned salah menebak **295 baris (28%)**. Analisis terhadap 10 pasangan kesalahan terbanyak mengungkap beberapa pola utama:

**Tabel Pasangan Kesalahan Terbanyak:**
| Asli | Ditebak | Jumlah | Analisis |
| :--- | :--- | :---: | :--- |
| neutral | joy | 29 | Model menganggap kata positif (*lucu, cerah*) sebagai `joy`. |
| neutral | anger | 26 | Model menangkap kata *"aneh, tolol"* sebagai `anger`. |
| sad | neutral | 23 | Model gagal menangkap emosi implisit (kekhawatiran, kepedulian). |
| joy | neutral | 23 | Teks `joy` yang singkat (*"bismillah semoga beruntung"*) dianggap netral. |
| anger | neutral | 23 | Sarkasme dan kritik tajam tidak terdeteksi sebagai `anger`. |

**Pola Utama:**
1. **Keterbatasan Konteks:** Model klasik tidak dapat memahami konteks kalimat secara utuh. Kata-kata positif/netral sering disalahartikan sebagai emosi lain.
2. **Emosi Implisit:** Emosi yang tidak diekspresikan secara eksplisit (misal: sedih tanpa kata "sedih") sering gagal terdeteksi.
3. **Sarkasme dan Nada Bicara:** Model kesulitan menangkap sarkasme atau kritik yang dibalut dengan kata-kata netral.
4. **Ambiguitas `joy` vs `love`:** Nuansa antara kebahagiaan dan cinta sulit dibedakan oleh model klasik.

**Implikasi:**
Temuan ini menegaskan bahwa model klasik (TF-IDF) memiliki keterbatasan fundamental dalam memahami **semantik dan konteks** bahasa. Hal ini menjadi justifikasi kuat untuk beralih ke model **Transformer (IndoBERT)** yang mampu memahami konteks kalimat secara lebih mendalam melalui mekanisme *self-attention*.

## 4. Kesimpulan Bagian Model Klasik
Model klasik berhasil memberikan *baseline* yang kuat dengan skor Macro F1 0.7286. Namun, keterbatasan model klasik dalam menghadapi perbedaan domain (ditunjukkan oleh skor EmoT yang rendah) dan kesulitan memahami konteks (ditunjukkan oleh analisis error) membuka jalan bagi eksperimen model transformer untuk memberikan hasil yang lebih general dan akurat.

---

*Catatan: Bagian ini akan disempurnakan dengan grafik confusion matrix dan tabel perbandingan detail dari output `baseline.py`.*