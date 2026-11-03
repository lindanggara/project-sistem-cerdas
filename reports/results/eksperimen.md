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
| 3 Nov 2026 | LogReg | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.7247 | **0.7155** | 🥇 Model klasik terbaik |
| 3 Nov 2026 | SVM | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.7251 | 0.7075 | — |
| 3 Nov 2026 | Naive Bayes | Linda | train v1 | + Normalisasi kata gaul + Class Weighting | 0.5580 | 0.5586 | — |

## 2. Eksperimen Model Transformer (Chila)

| Tanggal | Model | PJ | Data | Perubahan | Macro F1 (valid) | Macro F1 (test) | Catatan |
|---|---|---|---|---|---|---|---|
| _TBD_ | IndoBERT | Chila | — | — | — | — | Menunggu |
| _TBD_ | IndoBERTweet | Chila | — | — | — | — | Menunggu |

## 3. Evaluasi Lintas Domain EmoT (Chila)

| Tanggal | Model | PJ | Macro F1 (EmoT) | Catatan |
|---|---|---|---|---|
| _TBD_ | — | Chila | — | Menunggu |