# 📘 Panduan Kerja Tim TextScope — Dari Minggu 10 Sampai Presentasi

> **Proyek:** TextScope — Klasifikasi Emosi Bahasa Indonesia + Evaluasi Lintas Domain  
> **Basis Data:** `src/download_data.py` → Emotion Dataset from Indonesian Public Opinion (6 kelas) + EmoT IndoNLU (5 kelas)  
> **Periode:** Minggu 10 (26–30 Okt 2026) → Presentasi Akhir Minggu 15 (30 Nov–4 Des 2026)  
> **Tim:** 4 orang — Yuhanidz, Linda, Chila, Zura

---

## 📑 Daftar Isi

1. [Gambaran Besar Proyek](#1-gambaran-besar-proyek)
2. [Struktur Tim & Peran](#2-struktur-tim--peran)
3. [Cara Kerja: Beruntun vs Paralel](#3-cara-kerja-beruntun-vs-paralel)
4. [Peta Jalan Minggu 10 → 15 (Detail)](#4-peta-jalan-minggu-10--15-detail)
5. [Titik Keputusan (Gate)](#5-titik-keputusan-gate)
6. [Aturan Kerja Harian](#6-aturan-kerja-harian)
7. [Tabel Catatan Percobaan](#7-tabel-catatan-percobaan)
8. [Struktur Repositori & Branch](#8-struktur-repositori--branch)
9. [Checklist per Minggu](#9-checklist-per-minggu)
10. [Daftar Istilah](#10-daftar-istilah)
11. [FAQ & Troubleshooting](#11-faq--troubleshooting)

---

## 1. Gambaran Besar Proyek

### 1.1 Apa yang Dibuat?

Sistem yang bisa **menebak emosi** dari teks Bahasa Indonesia. Input: teks (mis. komentar media sosial). Output: salah satu dari 6 emosi — `anger`, `fear`, `joy`, `love`, `sad`, `neutral`.

Sistem diuji dua tahap:
1. **Evaluasi utama** — pakai data uji dari dataset utama (6 kelas).
2. **Evaluasi lintas domain** — pakai EmoT IndoNLU (5 kelas, tanpa netral) untuk melihat seberapa bagus model kalau dipakai di sumber teks berbeda.

Hasilnya ditampilkan di **dashboard**: user tempel teks → muncul prediksi emosi + grafik distribusi & confusion matrix.

### 1.2 Dari Mana Datanya?

| Dataset | Kelas | Fungsi |
|---|---|---|
| **Emotion Dataset from Indonesian Public Opinion** | 6: anger, fear, joy, love, sad, neutral | Dataset **utama** (latih + validasi + uji) |
| **EmoT (IndoNLU)** | 5: anger, fear, joy, love, sad | **Uji lintas domain** (bukan untuk latih) |

Output `python src/download_data.py`:
- `data/processed/emosi_gabungan.csv` — semua baris dataset utama
- `data/processed/emosi_bersih.csv` — tanpa duplikat & tanpa label konflik
- `data/processed/emot_lintas.csv` — EmoT siap uji lintas domain

### 1.3 Deliverable Akhir

1. Dataset bersih (3 file) + split train/valid/test
2. Baseline model klasik (TF-IDF + LogReg/SVM/NB)
3. Model transformer (IndoBERT / IndoBERTweet)
4. Tabel perbandingan skor (Macro F1)
5. Hasil evaluasi lintas domain EmoT
6. Confusion matrix + analisis error
7. Dashboard demo
8. Laporan + slide
9. Demo live saat presentasi

### 1.4 Timeline

- **Presentasi akhir:** Minggu 15 (30 Nov–4 Des 2026)
- **Perbaikan nilai:** Minggu 16 (14–18 Des 2026)

---

## 2. Struktur Tim & Peran

### 2.1 Tabel Peran & Penanggung Jawab

| No | Peran | Nama | Tugas Utama | Deliverable |
|---|---|---|---|---|
| 1 | **Koordinator Data & Kualitas Dataset** | **Yuhanidz** | Jalankan `download_data.py`, verifikasi 3 file output, cek duplikat & konflik label, EDA, analisis error, tulis bagian Data laporan | Dataset bersih + laporan kualitas data + bagian Data |
| 2 | **PJ Model Klasik & Evaluasi** *(Ketua Tim)* | **Linda** | Split train/valid/test, baseline TF-IDF + LogReg/SVM/NB, tabel skor Macro F1, pilih model terbaik, analisis error | Split + baseline + tabel skor + model terpilih |
| 3 | **PJ Model Transformer** | **Chila** | Fine-tuning IndoBERT & IndoBERTweet di Colab, evaluasi lintas domain EmoT, catatan eksperimen, tulis bagian Eksperimen | Model transformer + hasil cross-domain + bagian Eksperimen |
| 4 | **PJ Dashboard & Laporan** | **Zura** | Dashboard demo prediksi emosi, grafik distribusi & confusion matrix, penyatuan laporan & slide | Dashboard + laporan final + slide |

> 📌 **Ketua Tim: Linda** (merangkap PJ Model Klasik & Evaluasi — beban paling ringan di awal proyek).

### 2.2 Tugas Tambahan Ketua (Linda)

- Memimpin pertemuan mingguan (20–30 menit)
- Menjaga **kode skor sama** untuk semua model (biar perbandingan adil)
- Pemeriksaan akhir slide & laporan sebelum dikumpulkan
- Menyampaikan hambatan tim secara jujur saat presentasi progres

### 2.3 Cadangan (Backup) per Peran

| Peran | Utama | Cadangan |
|---|---|---|
| Koordinator Data | Yuhanidz | Zura |
| PJ Model Klasik | Linda | Chila |
| PJ Model Transformer | Chila | Linda |
| PJ Dashboard | Zura | Yuhanidz |

> Cadangan bertugas menggantikan kalau yang utama berhalangan, dan **ikut memahami** pekerjaan utama (biar bisa bantu review pull request).

---

## 3. Cara Kerja: Beruntun vs Paralel

### 3.1 Jalur Beruntun (Harus Urut)

```
Data bersih (Yuhanidz)
      ↓
Split train/valid/test (Linda)
      ↓
┌─────────────────┬──────────────────┐
│ Baseline (Linda)│  IndoBERT (Chila)│  ← PARALEL
└─────────────────┴──────────────────┘
      ↓
Pilih model terbaik (Linda)
      ↓
┌─────────────────────────┬──────────────────────────┐
│ Model terbaik → Dashboard│ Evaluasi EmoT (Chila)   │ ← PARALEL
│        (Zura)            │                          │
└─────────────────────────┴──────────────────────────┘
      ↓
Laporan & slide (semua)
```

**Yang tidak bisa dilompati:**

| Pekerjaan | Harus Menunggu | Alasan |
|---|---|---|
| Split data (Linda) | Data bersih (Yuhanidz) | Nggak bisa split data kotor |
| Modeling (Linda & Chila) | Split terkunci (Linda) | Kalau split berubah, skor nggak comparable |
| Pilih model terbaik (Linda) | Baseline + transformer selesai | Butuh tabel perbandingan lengkap |
| Dashboard final (Zura) | Model terbaik terpilih | Dashboard nampilin model terbaik |
| Laporan final (semua) | Semua eksperimen selesai | Angka harus final |

### 3.2 Jalur Paralel (Bisa Jalan Bareng)

| Minggu | Yuhanidz (Data) | Linda (Klasik) | Chila (Transformer) | Zura (Dashboard) |
|---|---|---|---|---|
| **10** | Bersihin data | Siapin kode split & evaluasi | Smoke test IndoBERT | Kerangka dashboard |
| **11** | EDA + tulis bagian Data | Baseline 3 model | IndoBERT v1 | Pasang baseline |
| **12** | Analisis teks sulit | Perbaikan preprocessing | IndoBERTweet | Confusion matrix |
| **13** | Analisis error | Tabel final + pilih model | Cross-domain EmoT | Pasang model terbaik |
| **14** | Laporan bagian Data | Laporan bagian Klasik | Laporan bagian Transformer | Satukan laporan & slide |

### 3.3 Anti-Macet

| Masalah | Solusi |
|---|---|
| Yuhanidz lambat → semua nunggu | Kerjakan data bersih **hari pertama** Minggu 10 |
| Linda nunggu data | Siapkan **kode split + kode evaluasi** duluan |
| Chila nunggu split | **Smoke test IndoBERT** dulu (nggak butuh data final) |
| Zura nunggu model | Bangun **kerangka + mock input→output** dulu |
| Laporan numpuk di akhir | **Tulis bagian masing-masing tiap minggu** |

---

## 4. Peta Jalan Minggu 10 → 15 (Detail)

### 🗓️ MINGGU 10 (26–30 Okt) — Fondasi: Kunci Data, Kunci Split, Kunci Skor

> **Tema:** "Jangan modeling dulu. Kunci fondasi."

#### Tugas per Orang

**① Yuhanidz — Koordinator Data**
- [ ] Jalankan `python src/download_data.py` dari direktori proyek
- [ ] Verifikasi 3 file output ada: `emosi_gabungan.csv`, `emosi_bersih.csv`, `emot_lintas.csv`
- [ ] Cek jumlah baris & sebaran label masing-masing file
- [ ] Verifikasi duplikat & konflik label (script sudah handle, tapi cek manual)
- [ ] Update `data/README.md`: sumber, lisensi (CC-BY-NC-ND 4.0 untuk dataset utama; cek lisensi IndoNLU), cara unduh
- [ ] Laporkan hasil verifikasi ke tim

**② Linda — PJ Model Klasik & Evaluasi (Ketua)**
- [ ] Siapkan kode split stratified dari `emosi_bersih.csv` → train/valid/test (mis. 70/15/15)
- [ ] Pastikan **no leakage**: tidak ada teks sama di dua split
- [ ] Simpan split ke `data/processed/train.csv`, `valid.csv`, `test.csv`
- [ ] Tulis fungsi `evaluate_macro_f1()` yang dipakai **semua model**
- [ ] Siapkan kode evaluasi: precision, recall, F1 per kelas, confusion matrix
- [ ] Pimpin pertemuan mingguan pertama: tetapkan hari/jam, isi cadangan, bagi tugas

**③ Chila — PJ Model Transformer**
- [ ] Buka Google Colab, cek akses GPU (Runtime → Change runtime type → GPU)
- [ ] Smoke test IndoBERT: load model, 1 epoch kecil di subset data (boleh data dummy)
- [ ] Catat waktu training & VRAM di tabel eksperimen
- [ ] Siapkan notebook training yang rapi (sel terpisah: load data, tokenize, train, eval)

**④ Zura — PJ Dashboard & Laporan**
- [ ] Buat kerangka dashboard (Streamlit atau Gradio): input teks → output label (mock dulu)
- [ ] Buat **tabel catatan percobaan** di Google Sheets/Drive bersama
- [ ] Siapkan struktur folder `reports/figures/` dan `reports/results/`
- [ ] Tulis draft bagian Metode laporan

#### ✅ Gate Minggu 10

| Yang Dicek | PJ | Status |
|---|---|---|
| `emosi_bersih.csv` tervalidasi | Yuhanidz | ☐ |
| `emot_lintas.csv` tervalidasi (5 label, tanpa netral) | Yuhanidz | ☐ |
| Split train/valid/test **terkunci** & stratified | Linda | ☐ |
| Kode evaluasi Macro F1 siap | Linda | ☐ |
| Smoke test IndoBERT berhasil | Chila | ☐ |
| Kerangka dashboard ada | Zura | ☐ |
| Tabel catatan percobaan dibuat | Zura | ☐ |
| `data/README.md` diperbarui | Yuhanidz | ☐ |

> ⚠️ Kalau gate belum aman → **jangan lanjut Minggu 11**.

---

### 🗓️ MINGGU 11 (2–6 Nov) — Baseline Jalan

> **Tema:** "Baseline dulu, transformer nyusul."

#### Tugas per Orang

**① Yuhanidz — Koordinator Data**
- [ ] EDA: sebaran label per split, panjang teks per kelas, kata umum per kelas
- [ ] Visualisasi: bar chart distribusi label, histogram panjang teks
- [ ] Tulis **bagian Data** laporan (sumber, jumlah, sebaran, preprocessing, lisensi)
- [ ] Simpan grafik ke `reports/figures/`

**② Linda — PJ Model Klasik**
- [ ] Baseline **TF-IDF + Logistic Regression**
- [ ] Baseline **TF-IDF + SVM**
- [ ] Baseline **TF-IDF + Naive Bayes**
- [ ] Isi tabel skor Macro F1 (valid & test) ketiga model
- [ ] Simpan confusion matrix tiap model
- [ ] Catat 3 baris di tabel eksperimen

**③ Chila — PJ Transformer**
- [ ] Latih **IndoBERT pertama** pada dataset utama (train, validasi pakai valid)
- [ ] Evaluasi di test → Macro F1
- [ ] Catat 1 baris di tabel eksperimen
- [ ] Simpan model ke `models/` (di Drive, bukan GitHub)

**④ Zura — PJ Dashboard**
- [ ] Pasang baseline terbaik di dashboard
- [ ] Tambah grafik distribusi label
- [ ] Uji input teks → prediksi masuk akal

#### Output Minggu 11
- ✅ Bagian Data laporan (Yuhanidz)
- ✅ Tabel skor 3 baseline (Linda)
- ✅ IndoBERT v1 + skor (Chila)
- ✅ Dashboard v1 (Zura)

---

### 🗓️ MINGGU 12 (9–13 Nov) — Penyempurnaan & Bandingkan

> **Tema:** "Perbaiki baseline, bandingkan transformer."

#### Tugas per Orang

**① Yuhanidz — Koordinator Data**
- [ ] Identifikasi teks sulit/ambigu (mis. `neutral` vs `sad`, `love` vs `joy`)
- [ ] Usul perbaikan preprocessing (normalisasi kata gaul; script sudah buang `[USERNAME]`/`[URL]` di EmoT)
- [ ] Dokumentasikan temuan

**② Linda — PJ Model Klasik**
- [ ] Coba perbaikan: normalisasi kata gaul, class weighting untuk kelas minoritas
- [ ] Bandingkan baseline v1 vs v2
- [ ] Catat tiap percobaan di tabel eksperimen

**③ Chila — PJ Transformer**
- [ ] Latih **IndoBERTweet**
- [ ] Bandingkan dengan IndoBERT (Macro F1 valid & test)
- [ ] Catat 1 baris di tabel eksperimen
- [ ] Siapkan kode evaluasi lintas domain (belum jalan, siap-siap)

**④ Zura — PJ Dashboard**
- [ ] Tambah **confusion matrix** interaktif
- [ ] Tambah grafik per-kelas (precision/recall/F1)
- [ ] Update dashboard v2

#### ⚠️ Gate Minggu 12
- Harus sudah ada hasil **baseline + minimal 1 transformer**
- Kalau IndoBERTweet macet → **hentikan (Chila), fokus 1 transformer**

---

### 🗓️ MINGGU 13 (16–20 Nov) — Evaluasi Lintas Domain & Pilih Model Terbaik

> **Tema:** "Pilih juara, uji di domain lain."

#### Tugas per Orang

**① Yuhanidz — Koordinator Data**
- [ ] Analisis error per kelas: mana yang sering tertukar (mis. `love↔joy`, `neutral↔sad`)
- [ ] Ambil contoh teks yang salah ditebak
- [ ] Tulis analisis kualitatif

**② Linda — PJ Model Klasik (Ketua)**
- [ ] Susun **tabel perbandingan akhir** semua model (baseline v1, v2, IndoBERT, IndoBERTweet)
- [ ] **Pilih model terbaik** berdasarkan Macro F1 di test
- [ ] Dokumentasikan alasan pemilihan
- [ ] Serahkan model terbaik ke Zura

**③ Chila — PJ Transformer**
- [ ] **Evaluasi lintas domain** pada `emot_lintas.csv` (5 kelas, tanpa netral)
- [ ] Laporkan hasil **terpisah** dari evaluasi utama
- [ ] Catat perbedaan domain (gaya bahasa, distribusi label)
- [ ] Tulis **bagian Eksperimen** laporan

**④ Zura — PJ Dashboard**
- [ ] Pasang **model terbaik** di dashboard
- [ ] Uji end-to-end: input → prediksi → tampil grafik
- [ ] Update dashboard final

#### ⚠️ Gate Minggu 13
- Model terbaik **harus** sudah di dashboard
- Kalau transformer macet → **pakai baseline terbaik** untuk dashboard
- Hasil cross-domain EmoT sudah dilaporkan

---

### 🗓️ MINGGU 14 (23–27 Nov) — Rapikan & Latihan

> **Tema:** "Semua ketemu di laporan & slide."

#### Tugas Semua Orang

- [ ] Selesaikan **bagian laporan masing-masing**:
  - **Yuhanidz** → Data & kualitas dataset
  - **Linda** → Baseline & perbandingan model + kesimpulan
  - **Chila** → Transformer & cross-domain
  - **Zura** → Dashboard & visualisasi
- [ ] Uji dashboard bersama (input nyata → prediksi masuk akal)
- [ ] **Zura**: satukan laporan & slide, susun alur demo
- [ ] **Linda (Ketua)**: pemeriksaan akhir — konsistensi angka Macro F1 di laporan vs dashboard vs tabel eksperimen
- [ ] Latihan demo 1–2 kali

#### Yang Wajib Ada Sebelum Minggu 15

| No | Item | PJ | Status |
|---|---|---|---|
| 1 | Tabel perbandingan model dengan Macro F1 | Linda | ☐ |
| 2 | Hasil evaluasi lintas domain EmoT | Chila | ☐ |
| 3 | Confusion matrix + analisis error | Yuhanidz + Linda | ☐ |
| 4 | Dashboard demo (input → label) | Zura | ☐ |
| 5 | Laporan lengkap | Semua | ☐ |
| 6 | Slide presentasi | Zura | ☐ |

> **4 hal yang TIDAK boleh dipangkas:**
> 1. ✅ Evaluasi pada data uji dataset utama (Macro F1)
> 2. ✅ Evaluasi lintas domain EmoT (dilaporkan terpisah)
> 3. ✅ Confusion matrix + analisis error
> 4. ✅ Dashboard minimal

---

### 🗓️ MINGGU 15 (30 Nov–4 Des) — Presentasi Akhir & Demo

#### Tugas Semua Orang

- [ ] Demo dashboard live
- [ ] Presentasi bagian masing-masing (5–7 menit/orang)
- [ ] **Linda (Ketua)**: sampaikan hambatan tim secara jujur + pencapaian
- [ ] Siapkan jawaban untuk pertanyaan dosen

#### Struktur Presentasi (Saran)

| Urutan | Durasi | Pembicara | Isi |
|---|---|---|---|
| 1 | 2 menit | **Linda** (Ketua) | Latar belakang, tujuan |
| 2 | 5 menit | **Yuhanidz** | Data: sumber, jumlah, sebaran, lisensi |
| 3 | 5 menit | **Linda** | Metode: baseline + split |
| 4 | 5 menit | **Chila** | Transformer: IndoBERT/IndoBERTweet, cross-domain |
| 5 | 5 menit | **Linda** | Hasil: tabel perbandingan, model terbaik |
| 6 | 5 menit | **Zura** | Dashboard: demo live |
| 7 | 5 menit | **Yuhanidz + Linda** | Analisis error & kesimpulan |
| 8 | 10 menit | **Semua** | Tanya jawab |

---

## 5. Titik Keputusan (Gate)

| Kapan | Yang Dicek | PJ Penanggung Jawab | Jika Belum Aman |
|---|---|---|---|
| **Akhir Minggu 10** | Data bersih + split terkunci + kode skor siap | Yuhanidz + Linda | Perbaiki dulu, **jangan** modeling |
| **Akhir Minggu 12** | Baseline + 1 transformer sudah ada hasil | Linda + Chila | Hentikan IndoBERTweet, fokus 1 transformer |
| **Akhir Minggu 13** | Model terbaik sudah di dashboard | Linda + Zura | Pakai baseline terbaik untuk dashboard |
| **Akhir Minggu 14** | Laporan & slide jadi, demo jalan | Semua | Potong fitur non-esensial, jangan potong 4 hal wajib |

**Yang tidak boleh dipangkas apa pun:**
1. ✅ Data uji berlabel (dari dataset utama)
2. ✅ Perbandingan skor dengan **Macro F1**
3. ✅ Analisis salah tebak
4. ✅ Dashboard minimal

---

## 6. Aturan Kerja Harian

1. **Pertemuan mingguan** — 20–30 menit, dipimpin **Linda**. Tiap orang jawab: *apa yang selesai, apa yang macet, apa yang dikerjakan berikutnya.*
2. **Catatan percobaan** — setiap percobaan baru = satu baris tabel (tanggal, perubahan, data, skor, komentar). **Jangan hapus/timpa baris lama.**
3. **Cara hitung skor harus sama** — semua model dinilai dengan kode `evaluate_macro_f1()` dari **Linda**. Metrik utama **Macro F1**.
4. **Penyimpanan berkas** — kode di GitHub; data & model di Google Drive bersama. **Data mentah tidak boleh masuk GitHub.**
5. **Berkas rahasia** — API key, cookie, kredensial **tidak boleh** diunggah ke GitHub/Drive bersama.
6. **Anonimisasi** — hapus username, nomor telepon, NIM sebelum data dibagikan/dikutip di laporan.
7. **Satu cabang satu pekerjaan** — branch `feat/...` + pull request.
8. **Kalau macet, bilang lebih awal** — hambatan di pertemuan mingguan masih bisa dibantu.

---

## 7. Tabel Catatan Percobaan

Simpan di Google Sheets/Drive bersama (dibuat **Zura**). Format:

| Tanggal | Model | PJ | Data | Perubahan | Macro F1 (valid) | Macro F1 (test) | Catatan |
|---|---|---|---|---|---|---|---|
| 2 Nov | TF-IDF + LogReg | Linda | train v1 | baseline | 0.xx | 0.xx | — |
| 4 Nov | IndoBERT | Chila | train v1 | 3 epoch, lr 2e-5 | 0.xx | 0.xx | GPU 12 GB |
| 6 Nov | IndoBERTweet | Chila | train v1 | 3 epoch, lr 2e-5 | 0.xx | 0.xx | — |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Aturan:**
- Satu baris per percobaan
- **Jangan hapus/timpa** baris lama
- Catat **semua** percobaan, termasuk yang gagal
- Sertakan komentar singkat kenapa hasilnya begitu

---

## 8. Struktur Repositori & Branch

### 8.1 Struktur Folder

```
project-sistem-cerdas/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── README.md
│   ├── raw/            # emosi_opini_publik/, emot/  ← TIDAK di-commit
│   ├── interim/
│   └── processed/      # emosi_gabungan.csv, emosi_bersih.csv, emot_lintas.csv, train/valid/test
├── notebooks/
├── src/
│   └── download_data.py
├── models/             # artefak model ← TIDAK di-commit
├── reports/
│   ├── figures/
│   └── results/
├── dashboard/
├── tests/
└── docs/
```

### 8.2 Branch per Orang

| Orang | Branch | Untuk |
|---|---|---|
| **Yuhanidz** | `feat/data-quality` | Verifikasi data, EDA, analisis error |
| **Linda** | `feat/baseline` | Split, baseline, tabel skor, pemilihan model |
| **Chila** | `feat/indobert`, `feat/cross-domain-eval` | Training transformer, evaluasi EmoT |
| **Zura** | `feat/dashboard`, `docs/laporan` | Dashboard, penyatuan laporan & slide |

### 8.3 Alur Git

1. Buat branch dari `main`: `git checkout -b feat/baseline`
2. Kerjakan, commit bertahap dengan pesan jelas
3. Push, buat **pull request**
4. Minta review **cadangan** masing-masing (lihat §2.3)
5. Merge ke `main` setelah disetujui **Linda (Ketua)**

---

## 9. Checklist per Minggu

### Minggu 10
- [ ] **Yuhanidz**: `download_data.py` berhasil, 3 file output ada
- [ ] **Yuhanidz**: `emosi_bersih.csv` & `emot_lintas.csv` tervalidasi
- [ ] **Yuhanidz**: `data/README.md` diperbarui
- [ ] **Linda**: Split train/valid/test terkunci
- [ ] **Linda**: Kode `evaluate_macro_f1()` siap
- [ ] **Linda**: Pertemuan mingguan pertama diadakan
- [ ] **Chila**: Smoke test IndoBERT berhasil
- [ ] **Zura**: Kerangka dashboard ada
- [ ] **Zura**: Tabel catatan percobaan dibuat

### Minggu 11
- [ ] **Yuhanidz**: EDA selesai + grafik disimpan + bagian Data ditulis
- [ ] **Linda**: 3 baseline selesai (LogReg, SVM, NB) + tabel skor
- [ ] **Chila**: IndoBERT v1 selesai + skor
- [ ] **Zura**: Dashboard v1 (baseline terpasang)

### Minggu 12
- [ ] **Yuhanidz**: Analisis teks sulit/ambigu
- [ ] **Linda**: Perbaikan preprocessing + baseline v2
- [ ] **Chila**: IndoBERTweet selesai + skor
- [ ] **Zura**: Confusion matrix + grafik per-kelas di dashboard

### Minggu 13
- [ ] **Yuhanidz**: Analisis error per kelas
- [ ] **Linda**: Tabel perbandingan akhir + model terbaik terpilih
- [ ] **Chila**: Cross-domain EmoT selesai + bagian Eksperimen ditulis
- [ ] **Zura**: Model terbaik di dashboard

### Minggu 14
- [ ] **Yuhanidz**: Bagian Data laporan final
- [ ] **Linda**: Bagian Klasik + kesimpulan + pemeriksaan akhir
- [ ] **Chila**: Bagian Transformer final
- [ ] **Zura**: Laporan & slide disatukan
- [ ] **Semua**: Dashboard diuji bersama + latihan demo

### Minggu 15
- [ ] **Semua**: Presentasi
- [ ] **Semua**: Demo live
- [ ] **Semua**: Tanya jawab

---

## 10. Daftar Istilah

| Istilah | Arti |
|---|---|
| **Dataset utama** | Emotion Dataset from Indonesian Public Opinion (6 kelas) |
| **EmoT** | Dataset IndoNLU (5 kelas, tanpa netral) untuk uji lintas domain |
| **Pemetaan label** | `happy→joy`, `sadness→sad` (EmoT → skema utama) |
| **Dedup** | Buang teks kembar; teks dengan label ganda dibuang seluruhnya |
| **Split** | Train/valid/test dari dataset utama, stratified |
| **Stratified** | Proporsi kelas dijaga sama di tiap split |
| **Leakage** | Data uji "bocor" ke data latih — harus dihindari |
| **TF-IDF** | Cara ubah teks jadi angka berdasarkan kekhasan kata |
| **LogReg / SVM / NB** | Model klasik: Logistic Regression, SVM, Naive Bayes |
| **Transformer** | Model bahasa besar (IndoBERT, IndoBERTweet) |
| **Fine-tuning** | Latih ulang model bahasa pra-latih dengan data kita |
| **Macro F1** | Rata-rata F1 per kelas, bobot sama (kelas jarang tetap dihitung) |
| **Confusion matrix** | Tabel yang menunjukkan prediksi benar/salah per kelas |
| **Cross-domain eval** | Uji model pada EmoT, dilaporkan terpisah |
| **EDA** | Exploratory Data Analysis — eksplorasi data awal |
| **Smoke test** | Uji kecil untuk pastikan pipeline jalan sebelum training penuh |

---

## 11. FAQ & Troubleshooting

**Q: `download_data.py` gagal, file tidak ada?**  
A: Cek koneksi internet. Script melewati unduhan kalau file sudah ada — hapus file rusak di `data/raw/` lalu jalankan ulang. Cek URL di script masih valid.

**Q: Split data berubah setelah dijalankan ulang?**  
A: Gunakan `random_state` tetap (mis. 42) di `train_test_split`. Simpan split ke file agar tidak berubah.

**Q: IndoBERT lambat / Colab kehabisan GPU?**  
A: Kurangi batch size, pakai `fp16`, atau latih di subset dulu. Kalau tetap macet → gate Minggu 12: hentikan IndoBERTweet, fokus 1 transformer.

**Q: Skor Macro F1 berbeda antar model padahal kode sama?**  
A: Cek: (1) split sama? (2) preprocessing sama? (3) label mapping sama? (4) random seed sama? Kalau semua sama, perbedaan wajar.

**Q: EmoT hasilnya jelek sekali?**  
A: Wajar — beda domain. Laporkan **terpisah**, jelaskan perbedaan distribusi & gaya bahasa. Ini temuan, bukan kegagalan.

**Q: Dashboard belum bisa tampil model terbaik?**  
A: Gate Minggu 13: kalau transformer macet, pakai **baseline terbaik** untuk dashboard.

**Q: Laporan numpuk di Minggu 14?**  
A: Tulis bagian masing-masing **tiap minggu** (Yuhanidz: Minggu 11; Linda & Chila: Minggu 13; Zura: Minggu 14).

**Q: Angka di laporan beda dengan dashboard?**  
A: **Linda (Ketua)** wajib periksa di Minggu 14. Sumber kebenaran: **tabel catatan percobaan**. Semua angka harus dari situ.

---

## 📌 Ringkasan Siapa Kerja Apa

| Minggu | Yuhanidz | Linda (Ketua) | Chila | Zura |
|---|---|---|---|---|
| **10** | Data bersih | Split + kode skor + pimpin rapat | Smoke test IndoBERT | Kerangka dashboard + tabel eksperimen |
| **11** | EDA + bagian Data | 3 baseline | IndoBERT v1 | Dashboard v1 |
| **12** | Analisis teks sulit | Perbaikan preprocessing | IndoBERTweet | Confusion matrix |
| **13** | Analisis error | Tabel final + pilih model | Cross-domain EmoT + bagian Eksperimen | Model terbaik di dashboard |
| **14** | Laporan Data | Laporan Klasik + pemeriksaan akhir | Laporan Transformer | Satukan laporan & slide |
| **15** | Presentasi Data & error | Presentasi pembuka + hasil | Presentasi Transformer | Presentasi + demo dashboard |

> **Kunci sukses:**
> 1. **Minggu 10 = kunci fondasi.** Jangan modeling dulu.
> 2. **Minggu 11–13 = kerja paralel.**
> 3. **Minggu 14 = sinkronisasi.**
> 4. **Minggu 15 = presentasi.**
>
> Yang tidak boleh dipangkas: **evaluasi Macro F1 di data uji**, **cross-domain EmoT**, **confusion matrix + analisis error**, **dashboard minimal**.

*Terakhir diperbarui: Minggu 10 (26–30 Oktober 2026)*  
*Simpan dokumen ini di `docs/PANDUAN_TIM.md` di repositori.*