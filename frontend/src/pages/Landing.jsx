import { Link } from 'react-router-dom'
import { ArrowRight, Download, PieChart, Radar, ShieldCheck, Sparkles } from 'lucide-react'
import Logo from '../components/Logo.jsx'
import Owl from '../components/Owl.jsx'
import { EMOTIONS, emotionInfo, tint } from '../lib/emotions.js'

const LANGKAH = [
  { bg: '#ECE6FB', judul: 'Unggah file', isi: 'Masukkan file .csv atau .xlsx berisi kumpulan teks, lalu pilih kolom teksnya.' },
  { bg: '#FDE7DC', judul: 'Analisis otomatis', isi: 'Model mendeteksi emosi setiap teks dan mencari topik yang memicunya.' },
  { bg: '#DFF3EA', judul: 'Lihat dan unduh hasil', isi: 'Baca grafik, kesimpulan, dan detail per teks, lalu unduh hasilnya.' },
]

const FITUR = [
  { bg: '#ECE6FB', color: '#6B5DC2', icon: PieChart, judul: 'Distribusi emosi', isi: 'Lihat persentase enam emosi dari seluruh teks dalam satu grafik.' },
  { bg: '#FDE7DC', color: '#B4532A', icon: Radar, judul: 'Topic Radar', isi: 'Temukan topik dan kata kunci yang paling sering memicu setiap emosi.' },
  { bg: '#FCE4EE', color: '#C2416F', icon: ShieldCheck, judul: 'Privacy Shield', isi: 'Sensor username, nomor telepon, dan NIM secara otomatis sebelum dianalisis.' },
  { bg: '#DFF3EA', color: '#2E8A62', icon: Download, judul: 'Unduh hasil', isi: 'Simpan hasil prediksi setiap teks sebagai file Excel.' },
]

const PRIMARY_BTN = 'flex min-h-14 items-center gap-2.5 rounded-full bg-primary px-7 text-lg font-black text-white no-underline shadow-button transition hover:bg-primary-dark'

function SectionTitle({ eyebrow, title }) {
  return (
    <div className="flex max-w-[60ch] flex-col gap-2">
      <span className="text-sm font-black tracking-wider text-primary uppercase">{eyebrow}</span>
      <h2 className="text-3xl leading-tight font-black tracking-tight sm:text-[38px]">{title}</h2>
    </div>
  )
}

export default function Landing() {
  return (
    <div className="bg-page">
      <header className="mx-auto flex max-w-[1200px] flex-wrap items-center justify-between gap-4 px-6 py-5 sm:px-8">
        <Link to="/" className="no-underline" aria-label="TextScope"><Logo size={36} /></Link>
        <nav aria-label="Navigasi halaman" className="flex flex-wrap items-center gap-1 rounded-full bg-white p-1.5 shadow-soft">
          <a href="#cara-kerja" className="flex min-h-11 items-center rounded-full px-4 font-extrabold text-[#4A4360] no-underline">Cara kerja</a>
          <a href="#fitur" className="flex min-h-11 items-center rounded-full px-4 font-extrabold text-[#4A4360] no-underline">Fitur</a>
          <Link to="/upload" className="flex min-h-11 items-center rounded-full bg-primary px-5 font-black text-white no-underline">Mulai analisis</Link>
        </nav>
      </header>

      <section className="mx-auto max-w-[1200px] px-6 pt-4 pb-10 sm:px-8">
        <div className="flex flex-wrap items-center gap-10 rounded-[40px] bg-sidebar px-7 py-12 sm:px-12 sm:py-14">
          <div className="flex min-w-0 flex-[1_1_440px] flex-col gap-5">
            <span className="flex items-center gap-2 self-start rounded-full bg-white px-4 py-2 text-sm font-black text-primary shadow-soft">
              <Sparkles size={16} aria-hidden="true" /> Analisis emosi teks Bahasa Indonesia
            </span>
            <h1 className="text-[44px] leading-[1.05] font-black tracking-[-0.03em] sm:text-6xl">Pahami emosi di balik ribuan teks.</h1>
            <p className="max-w-[46ch] text-[19px] leading-relaxed text-muted">
              Unggah file berisi komentar, ulasan, atau keluhan. TextScope mendeteksi emosi di setiap teks dan menunjukkan topik apa yang memicunya.
            </p>
            <div className="mt-1"><Link to="/upload" className={`${PRIMARY_BTN} inline-flex`}>Mulai analisis <ArrowRight size={20} aria-hidden="true" /></Link></div>
          </div>
          <div className="flex min-w-0 flex-[1_1_400px] flex-col items-center">
            <Owl size={220} />
            <div className="-mt-2 flex w-full max-w-[420px] flex-col gap-3.5 rounded-[28px] bg-white p-5 shadow-[0_20px_50px_rgba(107,93,194,.18)]">
              <div className="flex items-center justify-between gap-2">
                <span className="font-black">Contoh tampilan hasil</span>
                <span className="rounded-full bg-peach px-2.5 py-1 text-xs font-extrabold text-[#B4532A]">data contoh</span>
              </div>
              <div className="flex flex-wrap items-center gap-4.5">
                <div
                  role="img"
                  aria-label="Contoh diagram distribusi emosi"
                  className="flex size-[110px] shrink-0 items-center justify-center rounded-full"
                  style={{ background: 'conic-gradient(#E34948 0% 28%, #2A78D6 28% 50%, #EDA100 50% 68%, #1BAF7A 68% 83%, #6250D6 83% 93%, #E87BA4 93% 100%)' }}
                >
                  <div className="size-[66px] rounded-full bg-white" />
                </div>
                <div className="grid flex-[1_1_150px] grid-cols-2 gap-x-3 gap-y-2 text-sm font-bold">
                  {EMOTIONS.map((e) => (
                    <span key={e} className="flex items-center gap-1.5">
                      <span className="size-[9px] rounded-full" style={{ background: emotionInfo(e).color }} />{emotionInfo(e).nama}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="cara-kerja" className="mx-auto flex max-w-[1200px] flex-col gap-7 px-6 pt-14 pb-6 sm:px-8">
        <SectionTitle eyebrow="Cara kerja" title="Tiga langkah, tanpa membaca satu per satu." />
        <ol className="grid grid-cols-[repeat(auto-fit,minmax(260px,1fr))] gap-5">
          {LANGKAH.map((l, i) => (
            <li key={l.judul} className="flex flex-col gap-3 rounded-[28px] bg-white p-6.5 shadow-soft">
              <span className="flex size-[54px] items-center justify-center rounded-[18px] text-[22px] font-black" style={{ background: l.bg }}>{i + 1}</span>
              <h3 className="text-[21px] font-black">{l.judul}</h3>
              <p className="leading-relaxed text-muted">{l.isi}</p>
            </li>
          ))}
        </ol>
      </section>

      <section id="fitur" className="mx-auto flex max-w-[1200px] flex-col gap-7 px-6 pt-14 pb-6 sm:px-8">
        <SectionTitle eyebrow="Fitur" title="Tahu emosinya, tahu juga penyebabnya." />
        <div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-5">
          {FITUR.map((f) => (
            <div key={f.judul} className="flex flex-col gap-3 rounded-[28px] p-6.5" style={{ background: f.bg }}>
              <span className="flex size-[52px] items-center justify-center rounded-[18px] bg-white shadow-soft" style={{ color: f.color }}>
                <f.icon size={24} aria-hidden="true" />
              </span>
              <h3 className="text-xl font-black">{f.judul}</h3>
              <p className="leading-relaxed text-muted">{f.isi}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto flex max-w-[1200px] flex-col gap-5.5 px-6 pt-14 pb-6 sm:px-8">
        <SectionTitle eyebrow="Enam emosi" title="Setiap teks masuk ke salah satu emosi ini." />
        <div className="flex flex-wrap gap-3">
          {EMOTIONS.map((e) => (
            <span key={e} className="flex items-center gap-2.5 rounded-full px-5.5 py-3.5 text-lg font-black" style={{ background: tint(e) }}>
              <span className="size-3 rounded-full" style={{ background: emotionInfo(e).color }} />
              {emotionInfo(e).nama}
              <span className="text-sm font-bold text-muted">{e}</span>
            </span>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-[1200px] px-6 pt-14 pb-18 sm:px-8">
        <div className="flex flex-wrap items-center gap-7 rounded-[36px] bg-peach px-8 py-9 sm:px-11">
          <Owl size={130} />
          <div className="min-w-0 flex-[1_1_360px]">
            <h2 className="text-[30px] leading-tight font-black tracking-tight sm:text-[34px]">Siap melihat emosi di data kamu?</h2>
            <p className="mt-2 text-[17px] text-[#5A4A55]">Siapkan file .csv atau .xlsx, lalu mulai analisis.</p>
          </div>
          <Link to="/upload" className={PRIMARY_BTN}>Mulai analisis <ArrowRight size={20} aria-hidden="true" /></Link>
        </div>
      </section>

      <footer className="border-t border-[#E6E0F5]">
        <div className="mx-auto flex max-w-[1200px] flex-wrap items-center justify-between gap-4 px-6 py-7 text-[15px] text-muted sm:px-8">
          <Logo size={26} />
          <span>Proyek mata kuliah Sistem Cerdas</span>
        </div>
      </footer>
    </div>
  )
}
