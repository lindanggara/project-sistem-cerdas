import { Info } from 'lucide-react'
import Owl from '../components/Owl.jsx'
import { Card } from '../components/ui.jsx'
import { EMOTIONS, emotionInfo, tint } from '../lib/emotions.js'
import { MAX_FILE_MB } from '../lib/readFile.js'

const STEPS = [
  { bg: '#ECE6FB', judul: 'Siapkan file', isi: 'Kumpulkan teks dalam file .csv atau .xlsx, satu teks per baris.' },
  { bg: '#FDE7DC', judul: 'Unggah dan pilih kolom', isi: 'Unggah file, cek pratinjau, lalu pilih kolom yang berisi teks.' },
  { bg: '#FCE4EE', judul: 'Atur Privacy Shield', isi: 'Aktifkan untuk menyensor username, nomor telepon, dan NIM.' },
  { bg: '#DFF3EA', judul: 'Baca dan unduh hasil', isi: 'Lihat distribusi emosi, topik pemicu, dan detail per teks, lalu unduh Excel.' },
]

export default function Panduan() {
  return (
    <div className="flex flex-col gap-7">
      <section className="flex flex-wrap items-center gap-5 rounded-[30px] bg-lilac px-7 py-6">
        <Owl size={140} />
        <div className="min-w-0 flex-[1_1_300px]">
          <h1 className="text-[34px] font-black tracking-tight">Panduan penggunaan</h1>
          <p className="mt-2 max-w-[60ch] leading-relaxed text-muted">Cara menyiapkan file, menjalankan analisis, dan membaca hasilnya. Santai saja, cuma empat langkah.</p>
        </div>
      </section>

      <section className="flex flex-col gap-4">
        <h2 className="text-[22px] font-black">Cara memakai TextScope</h2>
        <ol className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {STEPS.map((s, i) => (
            <li key={s.judul} className="flex flex-col gap-2.5 rounded-[26px] p-5.5" style={{ background: s.bg }}>
              <span className="flex size-11 items-center justify-center rounded-[15px] bg-white text-[19px] font-black text-primary shadow-soft">{i + 1}</span>
              <h3 className="text-lg font-black">{s.judul}</h3>
              <p className="text-[15px] leading-relaxed text-muted">{s.isi}</p>
            </li>
          ))}
        </ol>
      </section>

      <Card className="flex flex-wrap gap-7">
        <div className="flex min-w-0 flex-[1_1_300px] flex-col gap-3">
          <h2 className="text-[22px] font-black">Format file</h2>
          <ul className="list-disc space-y-1.5 pl-5 text-[15px]">
            <li>File berformat <b>.csv</b> atau <b>.xlsx</b>, maksimal {MAX_FILE_MB} MB</li>
            <li>Baris pertama berisi nama kolom</li>
            <li>Satu baris berisi satu teks</li>
            <li>Kolom lain (tanggal, id) boleh ada, tidak ikut dianalisis</li>
          </ul>
        </div>
        <div className="min-w-0 flex-[1_1_360px]">
          <p className="mb-2.5 text-sm font-extrabold text-muted">Contoh isi file</p>
          <div className="overflow-x-auto rounded-[18px] border border-line">
            <table className="w-full min-w-[360px] border-collapse text-sm">
              <thead>
                <tr className="bg-page text-left">
                  <th className="px-3.5 py-2.5 font-extrabold text-muted">id</th>
                  <th className="px-3.5 py-2.5 font-black text-primary">komentar</th>
                </tr>
              </thead>
              <tbody>
                {['Paketnya sampai cepat, makasih!', 'Kesel, CS nggak balas dari kemarin.', 'Pesanan saya dikirim hari Senin.'].map((t, i) => (
                  <tr key={t} className="border-t border-[#F0ECF8]">
                    <td className="px-3.5 py-2.5 text-muted">{i + 1}</td>
                    <td className="px-3.5 py-2.5">{t}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      <section className="flex flex-col gap-4">
        <div>
          <h2 className="text-[22px] font-black">Enam label emosi</h2>
          <p className="mt-1 text-[15px] text-muted">Setiap teks dimasukkan ke salah satu emosi berikut.</p>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {EMOTIONS.map((e) => {
            const info = emotionInfo(e)
            return (
              <Card key={e} className="flex flex-col gap-2.5 p-5.5">
                <div className="flex items-center gap-2.5">
                  <span className="flex size-10 shrink-0 items-center justify-center rounded-[14px]" style={{ background: tint(e) }}>
                    <span className="block size-4 rounded-full" style={{ background: info.color }} />
                  </span>
                  <span className="text-[19px] font-black">{info.nama}</span>
                  <span className="rounded-full bg-page px-2.5 py-1 text-[13px] font-bold text-muted">{e}</span>
                </div>
                <p className="text-[15px] leading-relaxed">{info.arti}</p>
                <p className="text-sm text-muted italic">“{info.contoh}”</p>
              </Card>
            )
          })}
        </div>
      </section>

      <section className="flex items-start gap-4 rounded-[26px] bg-butter px-6 py-5.5">
        <span className="flex size-[42px] shrink-0 items-center justify-center rounded-[14px] bg-white text-[#9A6A00]">
          <Info size={22} aria-hidden="true" />
        </span>
        <div>
          <h2 className="mb-1.5 text-lg font-black">Perlu diingat</h2>
          <p className="max-w-[90ch] text-[15px] leading-relaxed text-[#4E4430]">
            Hasil TextScope adalah prediksi model, bukan penilaian manusia. Model bisa keliru pada teks bernada sarkas, teks yang sangat pendek, atau teks yang mengandung lebih dari satu emosi. Gunakan angka keyakinan sebagai petunjuk: semakin rendah, semakin perlu dicek ulang.
          </p>
        </div>
      </section>
    </div>
  )
}
