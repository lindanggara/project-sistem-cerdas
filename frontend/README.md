# TextScope · Frontend

Dashboard analisis emosi teks Bahasa Indonesia. Dibangun dengan **React + Vite + Tailwind CSS**, grafik memakai **Recharts**, dan di-deploy ke **Vercel**.

## Halaman

| URL | Halaman | Keterangan |
|---|---|---|
| `/` | Landing page | Perkenalan TextScope, tombol "Mulai analisis" |
| `/upload` | Upload Data | Unggah `.csv`/`.xlsx`, pratinjau, pilih kolom teks, Privacy Shield |
| `/hasil` | Hasil Analisis | Ringkasan, KPI, distribusi emosi + Topic Radar (saling terhubung), tabel, unduh Excel. Terkunci sebelum ada hasil |
| `/panduan` | Panduan | Cara pakai, format file, arti 6 label emosi |

## Menjalankan di komputer

Butuh **Node.js 20 atau lebih baru**.

```bash
npm install
cp .env.example .env     # Windows PowerShell: copy .env.example .env
npm run dev
```

Buka alamat yang muncul di terminal (biasanya http://localhost:5173).

## Mode data dummy vs backend asli

Atur di file `.env`:

```env
VITE_API_URL=http://localhost:8000   # alamat backend FastAPI
VITE_USE_MOCK=true                   # true = data dummy, false = backend asli
```

Selama backend belum siap, biarkan `VITE_USE_MOCK=true`. Dashboard tetap bisa dicoba dengan file sungguhan: teks dari file kamu dipakai, tapi label emosinya hanya tebakan sederhana (lihat `src/lib/mockApi.js`).

Setelah backend siap, ubah ke `VITE_USE_MOCK=false`, lalu jalankan ulang `npm run dev`.

## Kontrak API untuk tim backend

### `POST /analyze`

Request `multipart/form-data`:

| Field | Tipe | Keterangan |
|---|---|---|
| `file` | File | `.csv` / `.xlsx` |
| `text_column` | string | nama kolom teks |
| `privacy_shield` | `"true"` / `"false"` | sensor username, nomor telepon, NIM |

Response sukses (`200`):

```json
{
  "status": "success",
  "summary": {
    "total_texts": 1000,
    "dominant_emotion": "anger",
    "avg_confidence": 0.87,
    "censored_count": 124
  },
  "distribution": [
    { "emotion": "anger", "count": 280, "percentage": 28.0 }
  ],
  "topics": {
    "anger": [
      { "topic": "harga", "score": 0.42, "keywords": ["mahal", "naik terus"] }
    ],
    "fear": [], "joy": [], "love": [], "sad": [], "neutral": []
  },
  "insight": "Emosi yang paling banyak muncul adalah marah (28%), terutama terkait harga dan pelayanan.",
  "results": [
    { "id": 1, "text": "Harganya naik terus…", "emotion": "anger", "confidence": 0.92 }
  ]
}
```

Catatan:
- Label emosi **huruf kecil**: `anger`, `fear`, `joy`, `love`, `sad`, `neutral`.
- `topics` sebaiknya berisi **5 topik** per emosi supaya grafik radar terbentuk (minimal 3). Array kosong = data belum cukup, dashboard akan menampilkan pesan.
- `keywords` per topik **opsional** (kata dengan bobot tertinggi dari NMF). Kalau ada, tampil sebagai "Kata kunci dominan".
- Teks di `results` dikirim versi yang sudah disensor jika `privacy_shield` aktif.
- Emosi yang tidak muncul boleh tidak dikirim di `distribution`; frontend melengkapinya dengan 0.

Response gagal (`4xx`/`5xx`):

```json
{ "status": "error", "message": "Kolom 'komentar' tidak ditemukan di file." }
```

Backend perlu mengaktifkan **CORS** untuk alamat frontend (misalnya domain Vercel).

## Deploy ke Vercel

1. Push folder ini ke GitHub.
2. Di Vercel: **Add New → Project**, pilih repo-nya. Framework otomatis terdeteksi sebagai Vite.
3. Isi **Environment Variables**: `VITE_API_URL` (alamat backend) dan `VITE_USE_MOCK` (`true`/`false`).
4. Deploy. File `vercel.json` sudah mengatur agar refresh di `/hasil` atau `/upload` tidak error 404.

## Struktur folder

```text
src/
├── App.jsx                     # daftar halaman (routing)
├── index.css                   # warna tema (lavender, peach, mint, …) dan font Nunito
├── context/AnalysisContext.jsx # menyimpan hasil analisis (bertahan saat refresh)
├── components/
│   ├── DashboardLayout.jsx     # sidebar + area konten
│   ├── Logo.jsx                # logo TextScope (lensa di huruf "o")
│   ├── Owl.jsx                 # maskot burung hantu
│   ├── ui.jsx                  # Card, EmotionChip, EmotionPill, dll.
│   └── charts/
│       ├── EmotionDonut.jsx    # donat interaktif (irisan aktif menonjol)
│       └── TopicRadarChart.jsx # grafik radar topik
├── lib/
│   ├── api.js                  # panggilan POST /analyze (atau mock)
│   ├── mockApi.js              # data dummy + sensor sederhana
│   ├── readFile.js             # baca .csv/.xlsx di browser
│   ├── exportExcel.js          # unduh hasil ke .xlsx
│   └── emotions.js             # nama, warna, arti 6 emosi
└── pages/
    ├── Landing.jsx
    ├── Upload.jsx
    ├── Hasil.jsx
    └── Panduan.jsx
```
