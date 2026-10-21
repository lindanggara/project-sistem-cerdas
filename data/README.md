# Data directory

Folder ini memisahkan data berdasarkan tahap pengolahan:

- `raw/`: salinan sumber asli yang tidak diubah.
- `interim/`: data setelah pembersihan awal.
- `processed/`: data final untuk analisis/model.

Dataset tidak disertakan di GitHub secara default. Simpan data secara lokal atau pada penyimpanan dengan akses terbatas. Dokumentasikan sumber, tanggal pengambilan, izin penggunaan, skema kolom, dan langkah preprocessing tanpa mempublikasikan informasi sensitif.

Kolom kandidat (sesuaikan dengan data yang benar-benar tersedia):

- `post_id`: identifier yang dianonimkan atau pseudonim.
- `created_at`: waktu unggah menfess.
- `text`: isi teks yang sudah ditangani sesuai kebijakan privasi.
- `reply_count`: jumlah balasan dalam periode observasi yang ditentukan.
- `replied`: label target biner yang diturunkan dari aturan label.

Jangan menganggap kolom tersebut tersedia sebelum memeriksa sumber data. Tentukan pula jendela observasi balasan agar label `replied` konsisten.
