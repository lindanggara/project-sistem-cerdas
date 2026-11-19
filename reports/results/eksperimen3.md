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

| Tanggal     | Model        | PJ    | Data                | Perubahan                                                                                        | Macro F1 (valid) | Macro F1 (test) | Catatan                                                                       |
| ----------- | ------------ | ----- | ------------------- | ------------------------------------------------------------------------------------------------ | ---------------- | --------------- | ----------------------------------------------------------------------------- |
| 17 Nov 2026 | IndoBERT     | Chila | train v1 (70/15/15) | Fine-tuning `indobenchmark/indobert-base-p1`, MAX_LENGTH=128, BATCH_SIZE=4, EPOCHS=1, LR=2e-5    | 0.7728           | 0.7707          | Training CPU selama 87 menit 24 detik                                         |
| 19 Nov 2026 | IndoBERTweet | Chila | train v1 (70/15/15) | Fine-tuning `indolem/indobertweet-base-uncased`, MAX_LENGTH=128, BATCH_SIZE=4, EPOCHS=1, LR=2e-5 | **0.7999**       | **0.7889**      | 🏆 Model transformer terbaik sementara; training CPU selama 62 menit 26 detik |

## **3. Evaluasi Lintas Domain EmoT (Model Klasik & Transformer)**

| Tanggal     | Model        | PJ    | Macro F1 (EmoT) | Catatan                                                                        |
| ----------- | ------------ | ----- | --------------- | ------------------------------------------------------------------------------ |
| 3 Nov 2026  | LogReg Tuned | Linda | 0.4142          | Mengalami penurunan performa dibandingkan pengujian data utama                 |
| 19 Nov 2026 | IndoBERT     | Chila | **0.4166**      | Hanya sedikit lebih tinggi dari LogReg Tuned; prediksi neutral mencapai 58,40% |
| TBD         | IndoBERTweet | Chila | —               | Menunggu evaluasi lintas domain menggunakan EmoT                               |

**Analisis Singkat (EmoT):**

Model klasik terbaik, yaitu LogReg Tuned, memperoleh Macro F1 sebesar 0.4142 pada dataset EmoT, turun dari 0.7286 pada dataset utama.

Sementara itu, IndoBERT memperoleh Macro F1 sebesar 0.4166 pada evaluasi lintas domain. Hasil tersebut hanya berbeda 0.0024 dari LogReg Tuned.

Meskipun IndoBERT memperoleh nilai sedikit lebih tinggi, performanya masih jauh di bawah hasil pengujian pada dataset utama. Hal ini mengindikasikan adanya tantangan generalisasi ketika model diuji pada dataset dengan karakteristik domain berbeda.

Pada evaluasi IndoBERT, sebanyak 58,40% prediksi EmoT diklasifikasikan sebagai `neutral`, padahal dataset EmoT hanya memiliki lima kelas emosi tanpa kelas `neutral`.

Hasil IndoBERTweet pada dataset utama sudah tersedia, tetapi kemampuan generalisasinya pada dataset EmoT masih perlu diuji.

## **4. Analisis Hasil IndoBERT**

IndoBERT berhasil memperoleh Macro F1 sebesar **0.7728 pada validation** dan **0.7707 pada test**. Selisih keduanya hanya 0.0021, sehingga performa model relatif konsisten antara data validation dan test.

Beberapa hasil penting dari eksperimen:

- Training loss: 0.9197.
- Akurasi validation: 0.7649.
- Akurasi test: 0.7659.
- Waktu training: 5.244,39 detik atau sekitar 87 menit 24 detik.
- Epoch terbaik: 1.
- Perangkat training: CPU.

IndoBERT memperoleh Macro F1 test sebesar 0.7707, lebih tinggi dibandingkan model klasik terbaik, yaitu LogReg Tuned dengan Macro F1 test 0.7286. Selisih keduanya sebesar 0.0421.

**Hasil evaluasi lintas domain IndoBERT:**

- Macro F1 EmoT: 0.4166.
- Akurasi: 0.2991.
- Prediksi `neutral`: 2.558 data atau 58,40%.
- Kelas dengan F1 terbaik: `fear` sebesar 0.6771.
- Kelas dengan F1 terendah: `sad` sebesar 0.1638.

Hasil tersebut menunjukkan bahwa IndoBERT memiliki performa cukup baik pada dataset utama, tetapi mengalami penurunan ketika diuji pada dataset EmoT.

**Kesimpulan:** IndoBERT berhasil menjadi salah satu model transformer dengan performa baik pada dataset utama. Namun, evaluasi lintas domain menunjukkan bahwa kemampuan generalisasinya masih perlu ditingkatkan.

## **5. Analisis Hasil IndoBERTweet**

IndoBERTweet berhasil memperoleh Macro F1 sebesar **0.7999 pada validation** dan **0.7889 pada test**. Hasil ini menunjukkan bahwa model mampu mempelajari pola emosi pada dataset utama dengan performa yang lebih tinggi dibandingkan IndoBERT.

Beberapa hasil penting dari eksperimen:

- Training loss: 0.8472.
- Akurasi validation: 0.7915.
- Akurasi test: 0.7829.
- Waktu training: 3.746,42 detik atau sekitar 62 menit 26 detik.
- Epoch terbaik: 1.
- Perangkat training: CPU.
- Model pretrained: `indolem/indobertweet-base-uncased`.
- MAX_LENGTH: 128.
- BATCH_SIZE: 4.
- LEARNING_RATE: 2e-5.

**Hasil F1-score setiap kelas pada data test:**

| Kelas   | Precision | Recall | F1-score |
| ------- | --------- | ------ | -------- |
| anger   | 0.8034    | 0.8462 | 0.8242   |
| fear    | 0.8120    | 0.7941 | 0.8030   |
| joy     | 0.8079    | 0.7606 | 0.7836   |
| love    | 0.7647    | 0.8053 | 0.7845   |
| sad     | 0.8852    | 0.7152 | 0.7912   |
| neutral | 0.7147    | 0.7819 | 0.7468   |

IndoBERTweet memperoleh Macro F1 test sebesar 0.7889, lebih tinggi dibandingkan IndoBERT yang memperoleh 0.7707. Selisih keduanya sebesar 0.0182.

Jika dibandingkan dengan model klasik terbaik, yaitu LogReg Tuned dengan Macro F1 test 0.7286, IndoBERTweet memiliki selisih sebesar 0.0603.

IndoBERTweet juga memperoleh nilai F1 lebih tinggi pada lima dari enam kelas emosi dibandingkan IndoBERT. Kelas `anger` memperoleh F1 tertinggi sebesar 0.8242, sedangkan kelas `neutral` memiliki F1 terendah sebesar 0.7468.

**Kesimpulan sementara:** IndoBERTweet menjadi model dengan performa terbaik pada dataset utama berdasarkan eksperimen yang telah dilakukan. Namun, hasil tersebut belum cukup untuk menetapkan IndoBERTweet sebagai model final karena evaluasi lintas domain menggunakan dataset EmoT belum dilakukan.

## **6. Perbandingan Keseluruhan Model**

Berdasarkan Macro F1 pada dataset utama (test).

| Peringkat | Model        | Macro F1 Test |
| --------- | ------------ | ------------- |
| 1         | IndoBERTweet | **0.7889**    |
| 2         | IndoBERT     | 0.7707        |
| 3         | LogReg Tuned | 0.7286        |
| 4         | SVM Tuned    | 0.7251        |
| 5         | LogReg       | 0.7108        |
| 6         | SVM          | 0.6997        |
| 7         | Naive Bayes  | 0.5628        |

Perbandingan Macro F1 Test

Performa model pada dataset utama.

00.250.50.751IndoBERTweetIndoBERTLogReg TunedSVM TunedLogRegSVMNaive Bayes

**Kesimpulan sementara keseluruhan:**

Berdasarkan eksperimen yang sudah dilakukan, IndoBERTweet memperoleh Macro F1 tertinggi pada dataset utama dengan nilai 0.7889. IndoBERT berada di posisi kedua dengan nilai 0.7707, sedangkan model klasik terbaik adalah LogReg Tuned dengan nilai 0.7286.

Meskipun demikian, penentuan model final masih mempertimbangkan hasil evaluasi lintas domain EmoT. Model dengan performa terbaik pada dataset utama belum tentu memiliki kemampuan generalisasi terbaik pada dataset berbeda.

## **7. Status eksperimen Chila**

**Fine-tuning IndoBERT** : Selesai

**Evaluasi cross-domain IndoBERT** : Selesai

**Fine-tuning IndoBERTweet** : Selesai

**Evaluasi cross-domain IndoBERTweet** : Belum

**Perbandingan akhir transformer** : Menunggu EmoT

- Model mana yang paling baik dalam generalisasi lintas domain?

**Catatan:** Semua hasil di atas menggunakan angka eksperimen yang sudah kamu kirim. Hasil IndoBERTweet cross-domain sengaja belum diisi karena memang belum dijalankan.
