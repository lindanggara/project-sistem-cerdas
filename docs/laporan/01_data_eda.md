# Bagian Data — Laporan TextScope

Oct 28, 2026 · @han han

## Sumber data dan lisensi

Proyek memakai dua dataset teks Bahasa Indonesia: satu untuk melatih, memvalidasi, dan menguji model, dan satu lagi khusus untuk menguji model pada sumber teks yang berbeda.

| Dataset | Jumlah kelas | Peran | Lisensi |
| --- | --- | --- | --- |
| Emotion Dataset from Indonesian Public Opinion (dataset utama) | 6: anger, fear, joy, love, sad, neutral | Latih, validasi, dan uji | CC-BY-NC-ND 4.0 |
| EmoT dari IndoNLU | 5: anger, fear, joy, love, sad | Uji lintas domain saja, tidak dipakai melatih | \[ISI: lisensi EmoT, salin dari repositori IndoNLU\] |

Tautan sumber: \[ISI: tautan dataset utama\] dan \[ISI: tautan EmoT\]. Data diunduh pada \[ISI: tanggal unduh\].

Lisensi NC (NonCommercial) dan ND (NoDerivatives) membatasi data pada penggunaan akademik tanpa distribusi ulang. Karena itu data mentah dan hasil olahan hanya disimpan di penyimpanan tim dan tidak diunggah ke GitHub.

## Jumlah dan struktur data

Dataset utama berisi 7.105 teks mentah yang menjadi 7.031 teks setelah dibersihkan, sedangkan EmoT berisi 4.401 teks mentah yang menjadi 4.379 teks.

Dataset utama terdiri atas enam file, satu per kelas, dengan dua kolom (teks dan label) yang dipisahkan tab. EmoT terdiri atas tiga file bawaan (train 3.521, valid 440, dan test 440 baris) yang digabung seluruhnya karena hanya dipakai sebagai data uji.

| Berkas olahan | Isi | Jumlah baris |
| --- | --- | --: |
| emosi\_gabungan.csv | Seluruh dataset utama, tanpa penyaringan | 7.105 |
| emosi\_bersih.csv | Dataset utama setelah pembersihan | 7.031 |
| train.csv | Data latih (70%) | 4.921 |
| valid.csv | Data validasi (15%) | 1.055 |
| test.csv | Data uji (15%) | 1.055 |
| emot\_lintas.csv | EmoT untuk uji lintas domain | 4.379 |

Train, valid, dan test dibagi dari emosi\_bersih.csv secara stratified sehingga proporsi kelas terjaga, dan tidak ada teks yang sama di dua split.

## Sebaran label

Kelas neutral paling dominan (28,2%) dan love paling sedikit (10,7%), dengan rasio 2,63 : 1, sehingga Macro F1 dipakai sebagai metrik utama.

| Kelas | Bersih | Persen | Train | Valid | Test | EmoT |
| --- | --: | --: | --: | --: | --: | --: |
| anger | 1.123 | 16,0% | 786 | 168 | 169 | 1.099 |
| fear | 905 | 12,9% | 633 | 136 | 136 | 641 |
| joy | 1.255 | 17,8% | 878 | 189 | 188 | 1.009 |
| love | 754 | 10,7% | 528 | 113 | 113 | 636 |
| sad | 1.008 | 14,3% | 706 | 151 | 151 | 994 |
| neutral | 1.986 | 28,2% | 1.390 | 298 | 298 | 0 |
| **Total** | **7.031** | **100%** | **4.921** | **1.055** | **1.055** | **4.379** |

Proporsi kelas di train, valid, dan test berbeda tidak lebih dari sekitar 0,1 poin persentase, jadi pembagian stratified berhasil. Sebagai pembanding, model yang selalu menebak neutral mencapai akurasi 0,282 tetapi Macro F1 hanya sekitar 0,073. EmoT tidak memiliki kelas neutral, dan kelas terbesarnya adalah anger (25,1%).

## Preprocessing

Preprocessing sengaja ringan: membuang noise dan data pribadi tanpa mengubah isi bahasa. Langkahnya berurutan:

1. Membaca file mentah dataset utama per baris, memisahkan teks dan label pada tab terakhir, lalu mencocokkan label dengan nama file. Tidak ada baris yang dilewati.
2. Normalisasi Unicode (NFKC).
3. Membuang placeholder seperti \[USERNAME\] dan \[URL\], alamat URL, dan mention.
4. Anonimisasi: membuang nomor telepon dan NIM.
5. Memendekkan huruf berulang lebih dari dua kali (misalnya "senaaang" menjadi "senaang") dan merapikan spasi.
6. Membuang teks yang muncul dengan label berbeda (konflik), seluruh barisnya, lalu membuang duplikat dan menyisakan satu. Pembandingnya huruf kecil dengan spasi dirapikan.
7. Khusus EmoT: memetakan label happy menjadi joy dan sadness menjadi sad, lalu membuang teks yang juga ada di dataset utama.

| Tahap | Dataset utama | EmoT |
| --- | --: | --: |
| Data mentah | 7.105 | 4.401 |
| Setelah teks kosong dibuang | 7.105 | 4.401 |
| Setelah label konflik dibuang | 7.082 | 4.399 |
| Setelah duplikat dibuang | 7.031 | 4.379 |
| Setelah tumpang tindih dengan dataset utama dibuang | tidak berlaku | 4.379 |

Label konflik berasal dari 11 teks unik pada dataset utama dan 1 teks unik pada EmoT. Tidak ada teks EmoT yang sama dengan dataset utama, jadi tahap terakhir tidak membuang baris.

Yang belum dilakukan: mengubah seluruh teks ke huruf kecil, normalisasi kata gaul, stemming, dan penghapusan stopword. Keempatnya diuji sebagai eksperimen terpisah dan dicatat di tabel percobaan, supaya pengaruhnya terhadap Macro F1 bisa diukur.

## Karakteristik dan kualitas data

Teks pada dataset utama pendek (median 13 kata, persentil ke-95 sebesar 44 kata, maksimum 59 kata pada data latih), dan panjangnya berbeda antar kelas.

| Kelas | Median (kata) | Teks 3 kata atau kurang |
| --- | --: | --: |
| anger | 12,5 | 7,4% |
| fear | 9 | 11,8% |
| joy | 9 | 15,8% |
| love | 19 | 1,3% |
| sad | 12 | 9,8% |
| neutral | 15 | 4,9% |

Teks EmoT lebih panjang, dengan median 28 kata dibanding 13 kata pada dataset utama. Sebanyak 14,3% token EmoT tidak ada di kosakata data latih, dibanding 11,5% untuk data validasi, sehingga selisih kosakata antar domain kecil dan perbedaan gaya lebih tampak pada panjang teks.

Pengamatan lain dari analisis eksplorasi pada data latih:

- Tidak ditemukan emoji maupun teks yang seluruhnya berhuruf kapital.
- Kata paling khas per kelas umumnya bermakna emosi (misalnya kata makian pada anger dan kata takut pada fear). Pada joy dan love juga muncul nama tokoh, dan pada neutral banyak kosakata formal bergaya berita. Ini indikasi awal bias topik dan gaya bahasa yang belum diuji.
- Pasangan kelas dengan kosakata paling mirip adalah sad dan neutral (kemiripan 0,45), sesuai dugaan bahwa keduanya paling mudah tertukar.
- Noise label terlihat dari teks pendek identik yang berlabel berbeda, misalnya joy dan neutral. Yang identik sudah dibuang, tetapi yang hampir sama tidak terdeteksi.

## Keterbatasan data

Hasil evaluasi perlu dibaca dengan lima keterbatasan berikut.

- Label berasal dari sumber dataset, bukan anotasi ulang oleh tim, sehingga noise label tetap mungkin ada dan membatasi skor tertinggi yang bisa dicapai.
- Kelas tidak seimbang (rasio 2,63 : 1), sehingga akurasi saja menyesatkan dan kelas kecil seperti love perlu perhatian khusus.
- Panjang teks yang berbeda antar kelas dapat menjadi jalan pintas yang dipelajari model, bukan emosi itu sendiri.
- Dugaan bias topik dan gaya bahasa (nama tokoh dan kosakata formal) dapat membuat skor pada data uji lebih tinggi daripada kemampuan sebenarnya di sumber teks lain.
- EmoT tidak memiliki kelas neutral, sehingga evaluasi lintas domain hanya mencakup lima kelas dan dilaporkan terpisah dari evaluasi utama.
