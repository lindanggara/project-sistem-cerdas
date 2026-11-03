# Bagian Laporan: Model Klasik & Evaluasi

*Dokumen ini adalah kerangka untuk bagian Model Klasik pada laporan akhir TextScope. Ditulis oleh Linda (PJ Model Klasik).*

## 1. Pendahuluan

Bagian ini menjelaskan pendekatan klasik yang digunakan sebagai *baseline* sebelum beralih ke model transformer. Tujuan utamanya adalah untuk membangun fondasi yang kuat, memahami karakteristik data, dan menyediakan pembanding yang adil (fair comparison) untuk model yang lebih kompleks.

## 2. Metodologi

### 2.1 Preprocessing
*(Ringkas hasil kerja Yuhanidz dan tambahan darimu)*
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
*(Tabel ini diambil dari `reports/results/eksperimen.md`)*

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
*(Tabel ini diambil dari `reports/results/eksperimen.md`)*

| Model | Macro F1 (EmoT) | Catatan |
| :--- | :---: | :--- |
| LogReg Tuned | **0.4142** | Turun drastis dari 0.7286. |

**Analisis Kritis:**
Penurunan performa yang sangat drastis (dari 0.7286 menjadi 0.4142) saat diuji pada dataset EmoT (Twitter) menunjukkan bahwa model klasik **sangat bergantung pada kosakata dan gaya bahasa dataset pelatihan**. Model gagal mengenali singkatan dan *slang* baru yang umum di Twitter. Recall yang sangat rendah (0.3147) mengindikasikan model sering melewatkan emosi yang sebenarnya.

Temuan ini menjadi justifikasi kuat untuk beralih ke model **Transformer (IndoBERT)**, yang diharapkan lebih tahan terhadap perbedaan domain karena kemampuannya memahami konteks kalimat secara lebih mendalam.

## 4. Kesimpulan Bagian Model Klasik
Model klasik berhasil memberikan *baseline* yang kuat dengan skor Macro F1 0.7286. Namun, keterbatasan model klasik dalam menghadapi perbedaan domain (ditunjukkan oleh skor EmoT yang rendah) membuka jalan bagi eksperimen model transformer untuk memberikan hasil yang lebih general.

---

*Catatan: Bagian ini akan disempurnakan dengan grafik confusion matrix dan tabel perbandingan detail dari `notebooks/` atau output `baseline.py`.*