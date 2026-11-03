# Tabel Eksperimen TextScope

Catatan semua percobaan model. **Jangan hapus baris lama**, tambahkan baris baru setiap kali ada percobaan.

## Format
| Tanggal | Model | PJ | Data | Perubahan | Macro F1 (valid) | Macro F1 (test) | Catatan |
|---|---|---|---|---|---|---|---|

## 1. Eksperimen Model Klasik

| Tanggal | Model | PJ | Data | Perubahan | Macro F1 (valid) | Macro F1 (test) | Catatan |
|---|---|---|---|---|---|---|---|
| 28 Okt 2026 | LogReg | Linda | train v1 | Baseline (TF-IDF) | 0.7176 | 0.7108 | Baseline awal |
| 28 Okt 2026 | SVM | Linda | train v1 | Baseline (TF-IDF) | 0.7231 | 0.6997 | — |
| 28 Okt 2026 | Naive Bayes | Linda | train v1 | Baseline (TF-IDF) | 0.5456 | 0.5628 | — |
| 3 Nov 2026 | LogReg | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.7247 | 0.7155 | 🥇 Eksperimen 1 |
| 3 Nov 2026 | SVM | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.7251 | 0.7075 | — |
| 3 Nov 2026 | Naive Bayes | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.5580 | 0.5586 | — |
| 3 Nov 2026 | LogReg Tuned | Linda | train v1 | + Fitur Char TF-IDF + GridSearch (C=1.0) | 0.7312 | **0.7286** | 🏆 **Model klasik terbaik keseluruhan** |
| 3 Nov 2026 | SVM Tuned | Linda | train v1 | + Fitur Char TF-IDF + GridSearch (C=0.1) | 0.7265 | 0.7251 | — |

## 2. Eksperimen Model Transformer (Chila)

| Tanggal | Model | PJ | Data | Perubahan | Macro F1 (valid) | Macro F1 (test) | Catatan |
|---|---|---|---|---|---|---|---|
| _TBD_ | IndoBERT | Chila | — | — | — | — | Menunggu |
| _TBD_ | IndoBERTweet | Chila | — | — | — | — | Menunggu |

## 3. Evaluasi Lintas Domain EmoT (Model Klasik & Transformer)

| Tanggal | Model | PJ | Macro F1 (EmoT) | Catatan |
|---|---|---|---|---|
| 3 Nov 2026 | LogReg Tuned | Linda | **0.4142** | Turun drastis dari 0.7286. Bukti model klasik *overfit* domain. |
| _TBD_ | IndoBERT | Chila | — | Menunggu |

**Analisis Singkat (EmoT):**
Model klasik terbaik (LogReg Tuned) mengalami penurunan performa yang sangat drastis (dari 0.7286 menjadi 0.4142) saat diuji pada dataset EmoT. Recall yang sangat rendah (0.3147) menunjukkan model gagal mengenali gaya bahasa Twitter. Kelas `sad` dan `joy` paling terdampak. Ini menjadi bukti kuat bahwa model klasik sangat bergantung pada kosakata domain pelatihan, dan menjadi *baseline* penting untuk membandingkan performa IndoBERT (Chila) nanti.