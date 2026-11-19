
# **Tabel Eksperimen TextScope**

Catatan semua percobaan model. **Jangan hapus baris lama**, tambahkan baris baru setiap kali ada percobaan.

## **1. Eksperimen Model Klasik**

| Tanggal     | Model        | PJ    | Data     | Perubahan                                 | Macro F1 (valid) | Macro F1 (test) | Catatan                             |
| ----------- | ------------ | ----- | -------- | ----------------------------------------- | ---------------- | --------------- | ----------------------------------- |
| 28 Okt 2026 | LogReg       | Linda | train v1 | Baseline (TF-IDF)                         | 0.7176           | 0.7108          | Baseline awal                       |
| 28 Okt 2026 | SVM          | Linda | train v1 | Baseline (TF-IDF)                         | 0.7231           | 0.6997          | —                                   |
| 28 Okt 2026 | Naive Bayes  | Linda | train v1 | Baseline (TF-IDF)                         | 0.5456           | 0.5628          | —                                   |
| 3 Nov 2026  | LogReg       | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.7247           | 0.7155          | 🥇 Eksperimen 1                     |
| 3 Nov 2026  | SVM          | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.7251           | 0.7075          | —                                   |
| 3 Nov 2026  | Naive Bayes  | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.5580           | 0.5586          | —                                   |
| 3 Nov 2026  | LogReg Tuned | Linda | train v1 | + Fitur Char TF-IDF + GridSearch (C=1.0)  | 0.7312           | **0.7286**      | 🏆 Model klasik terbaik keseluruhan |
| 3 Nov 2026  | SVM Tuned    | Linda | train v1 | + Fitur Char TF-IDF + GridSearch (C=0.1)  | 0.7265           | 0.7251          | —                                   |

## **2. Eksperimen Model Transformer (Chila)**

| Tanggal     | Model        | PJ    | Data                | Perubahan                                                                                     | Macro F1 (valid) | Macro F1 (test) | Catatan                                                                   |
| ----------- | ------------ | ----- | ------------------- | --------------------------------------------------------------------------------------------- | ---------------- | --------------- | ------------------------------------------------------------------------- |
| 17 Nov 2026 | IndoBERT     | Chila | train v1 (70/15/15) | Fine-tuning `indobenchmark/indobert-base-p1`, MAX_LENGTH=128, BATCH_SIZE=4, EPOCHS=1, LR=2e-5 | **0.7728**       | **0.7707**      | 🏆 Hasil training IndoBERT pertama; training CPU selama 87 menit 24 detik |
| *TBD*       | IndoBERTweet | Chila | —                   | —                                                                                             | —                | —               | Menunggu eksperimen                                                       |

## **3. Evaluasi Lintas Domain EmoT (Model Klasik & Transformer)**

| Tanggal    | Model        | PJ    | Macro F1 (EmoT) | Catatan                                                                            |
| ---------- | ------------ | ----- | --------------- | ---------------------------------------------------------------------------------- |
| 3 Nov 2026 | LogReg Tuned | Linda | **0.4142**      | Turun drastis dari 0.7286. Indikasi perbedaan domain data pelatihan dan pengujian. |
| *TBD*      | IndoBERT     | Chila | —               | Menunggu evaluasi lintas domain                                                    |

**Analisis Singkat (EmoT):**

Model klasik terbaik (LogReg Tuned) mengalami penurunan performa dari 0.7286 menjadi 0.4142 saat diuji pada dataset EmoT. Recall yang sangat rendah (0.3147) menunjukkan bahwa model mengalami kesulitan mengenali pola bahasa pada dataset lintas domain. Kelas `sad` dan `joy` menjadi kelas yang paling terdampak.

Hasil tersebut menjadi baseline untuk membandingkan kemampuan generalisasi model Transformer, khususnya IndoBERT.

## **4. Analisis Hasil IndoBERT**

IndoBERT berhasil memperoleh **Macro F1 sebesar 0.7728 pada validation** dan **0.7707 pada test**. Hasil ini menunjukkan performa yang cukup konsisten antara data validation dan test, dengan selisih hanya 0.0021.

Beberapa hasil penting dari eksperimen:

- Training loss: 0.9197.
- Akurasi validation: 0.7649.
- Akurasi test: 0.7659.
- Waktu training: 5.244,39 detik atau sekitar 87 menit 24 detik.
- Epoch terbaik: 1.
- Perangkat training: CPU.

IndoBERT memperoleh Macro F1 test 0.7707, lebih tinggi daripada model klasik terbaik, yaitu LogReg Tuned dengan Macro F1 test 0.7286. Selisihnya sebesar 0.0421.

**Kesimpulan sementara:** IndoBERT menjadi model dengan performa terbaik pada pengujian data test utama sejauh eksperimen yang tercatat. Namun, kemampuan generalisasinya pada domain berbeda masih perlu dibuktikan melalui evaluasi menggunakan dataset EmoT.

Eksperimen IndoBERT berhasil

**Catatan penting:** hasil IndoBERT di atas adalah evaluasi pada dataset utama, bukan hasil evaluasi lintas domain. Jadi, jangan masukkan angka 0.7707 ke kolom Macro F1 EmoT.

Langkah berikutnya adalah menjalankan evaluasi IndoBERT pada `emot_lintas.csv`, supaya bagian lintas domain juga bisa kita isi dengan hasil eksperimenmu yang sebenarnya.
