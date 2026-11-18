import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, FileCheck2, FileText, Loader2, Lock, ShieldCheck, Smile, UploadCloud } from 'lucide-react'
import Owl from '../components/Owl.jsx'
import { Card, PageHeader } from '../components/ui.jsx'
import { ACCEPTED_EXT, MAX_FILE_MB, readDataFile, validateFile } from '../lib/readFile.js'
import { analyzeFile, USE_MOCK } from '../lib/api.js'
import { anonymize } from '../lib/mockApi.js'
import { formatNumber } from '../lib/emotions.js'
import { useAnalysis } from '../context/AnalysisContext.jsx'

function InfoTile({ bg, iconColor, icon: Icon, label, value, note }) {
  return (
    <div className="flex flex-col gap-2.5 rounded-[26px] p-5" style={{ background: bg }}>
      <span className="flex size-[46px] items-center justify-center rounded-2xl bg-white shadow-soft" style={{ color: iconColor }}>
        <Icon size={22} strokeWidth={2.2} aria-hidden="true" />
      </span>
      <span className="text-sm font-bold text-muted">{label}</span>
      <span className="text-[26px] leading-tight font-black">{value}</span>
      <span className="text-[13px] text-muted">{note}</span>
    </div>
  )
}

export default function Upload() {
  const navigate = useNavigate()
  const { setResult } = useAnalysis()
  const inputRef = useRef(null)

  const [file, setFile] = useState(null)
  const [data, setData] = useState(null) // { columns, rows }
  const [textColumn, setTextColumn] = useState('')
  const [privacy, setPrivacy] = useState(true)
  const [dragOver, setDragOver] = useState(false)
  const [reading, setReading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState('')

  async function handleFile(f) {
    setError('')
    const problem = validateFile(f)
    if (problem) { setError(problem); return }
    setReading(true)
    try {
      const parsed = await readDataFile(f)
      setFile(f)
      setData(parsed)
      setTextColumn(parsed.suggestedColumn)
    } catch (e) {
      setError(e.message || 'File tidak bisa dibaca.')
    } finally {
      setReading(false)
    }
  }

  function reset() {
    setFile(null)
    setData(null)
    setTextColumn('')
    setError('')
    if (inputRef.current) inputRef.current.value = ''
  }

  async function handleAnalyze() {
    setError('')
    setAnalyzing(true)
    try {
      const res = await analyzeFile({ file, rows: data.rows, textColumn, privacyShield: privacy })
      setResult({ ...res, meta: { fileName: file.name, textColumn, privacyShield: privacy } })
      navigate('/hasil')
    } catch (e) {
      setError(e.message || 'Analisis gagal. Coba lagi.')
    } finally {
      setAnalyzing(false)
    }
  }

  const ready = Boolean(data && textColumn) && !analyzing
  const preview = data?.rows.slice(0, 5) ?? []
  const sample = 'makasih @rina_putri, cek 081234567890'

  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Upload Data" subtitle="Langkah 1 dari 2 · unggah file berisi kumpulan teks" />

      <div className="flex flex-wrap items-stretch gap-5">
        <section className="flex min-w-0 flex-[3_1_440px] flex-wrap items-center gap-5 rounded-[30px] bg-peach px-7 py-6">
          <Owl size={150} />
          <div className="flex min-w-0 flex-[1_1_240px] flex-col gap-2.5">
            <h2 className="text-[28px] leading-tight font-black">Halo, selamat datang!</h2>
            <p className="leading-relaxed text-[#5A4A55]">Unggah file teksmu, nanti TextScope bantu temukan emosi dan topik pemicunya.</p>
            <div className="mt-1 flex flex-wrap gap-2">
              {['1 · Unggah file', '2 · Pilih kolom', '3 · Analisis'].map((s) => (
                <span key={s} className="rounded-full bg-white px-3.5 py-1.5 text-sm font-extrabold text-[#B4532A]">{s}</span>
              ))}
            </div>
          </div>
        </section>
        <div className="grid min-w-0 flex-[4_1_480px] grid-cols-[repeat(auto-fit,minmax(160px,1fr))] gap-4">
          <InfoTile bg="#ECE6FB" iconColor="#6B5DC2" icon={FileText} label="Format file" value=".csv / .xlsx" note={`maks. ${MAX_FILE_MB} MB`} />
          <InfoTile bg="#DFF3EA" iconColor="#2E8A62" icon={Smile} label="Emosi dideteksi" value="6 emosi" note="marah sampai netral" />
          <InfoTile bg="#FCE4EE" iconColor="#C2416F" icon={ShieldCheck} label="Privacy Shield" value={privacy ? 'Aktif' : 'Nonaktif'} note="sensor data pribadi" />
        </div>
      </div>

      {error && (
        <div role="alert" className="rounded-2xl bg-[#FDE3E3] px-5 py-3.5 font-bold text-[#A42F2E]">{error}</div>
      )}

      <div className="flex flex-wrap items-start gap-5">
        <Card className="flex min-w-0 flex-[2_1_520px] flex-col gap-4">
          <h2 className="text-xl font-black">File kamu</h2>

          {!data ? (
            <label
              onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => { e.preventDefault(); setDragOver(false); handleFile(e.dataTransfer.files?.[0]) }}
              className={`flex cursor-pointer flex-col items-center gap-3 rounded-3xl border-[2.5px] border-dashed px-6 py-10 text-center transition ${dragOver ? 'border-primary bg-lilac' : 'border-[#C9BDF2] bg-page'}`}
            >
              <span className="flex size-[68px] items-center justify-center rounded-[22px] bg-white text-primary shadow-soft">
                {reading ? <Loader2 size={30} className="animate-spin" aria-hidden="true" /> : <UploadCloud size={30} aria-hidden="true" />}
              </span>
              <span className="text-[19px] font-black">{reading ? 'Membaca file…' : 'Tarik dan lepas file di sini'}</span>
              <span className="text-muted">atau pilih dari komputermu ({ACCEPTED_EXT.join(' / ')})</span>
              <span className="mt-1 flex min-h-[46px] items-center rounded-full bg-primary px-6 font-extrabold text-white">Pilih file</span>
              <input
                ref={inputRef}
                type="file"
                accept={ACCEPTED_EXT.join(',')}
                className="sr-only"
                onChange={(e) => handleFile(e.target.files?.[0])}
              />
            </label>
          ) : (
            <div className="flex flex-col gap-4">
              <div className="flex flex-wrap items-center gap-3.5 rounded-[20px] bg-mint px-4 py-3.5">
                <span className="flex size-[46px] shrink-0 items-center justify-center rounded-2xl bg-white text-[#2E8A62]">
                  <FileCheck2 size={22} aria-hidden="true" />
                </span>
                <div className="min-w-0 flex-[1_1_200px]">
                  <p className="truncate text-[17px] font-black">{file.name}</p>
                  <p className="text-sm text-[#3F5E50]">{formatNumber(data.rows.length)} baris · {data.columns.length} kolom · berhasil dibaca</p>
                </div>
                <button type="button" onClick={reset} disabled={analyzing} className="min-h-10 cursor-pointer rounded-full bg-white px-4 text-sm font-extrabold text-[#2E6B50] disabled:cursor-not-allowed disabled:opacity-60">
                  Ganti file
                </button>
              </div>

              <div>
                <p className="mb-2.5 font-black">Pratinjau data <span className="text-sm font-semibold text-muted">· 5 baris pertama</span></p>
                <div className="overflow-x-auto rounded-[18px] border border-line">
                  <table className="w-full min-w-[560px] border-collapse text-[15px]">
                    <thead>
                      <tr className="bg-page text-left">
                        {data.columns.map((c) => (
                          <th key={c} className={`px-4 py-3 ${c === textColumn ? 'bg-lilac font-black text-primary' : 'font-extrabold text-muted'}`}>
                            {c}{c === textColumn && ' · kolom teks'}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {preview.map((row, i) => (
                        <tr key={i} className="border-t border-[#F0ECF8]">
                          {data.columns.map((c) => (
                            <td key={c} className={`px-4 py-3 ${c === textColumn ? 'bg-page' : 'text-muted'}`}>{String(row[c] ?? '')}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </Card>

        <Card className="flex min-w-0 flex-[1_1_300px] flex-col gap-5">
          <h2 className="text-xl font-black">Pengaturan analisis</h2>

          <div className="flex flex-col gap-2">
            <label htmlFor="kolom" className="font-extrabold">Kolom yang berisi teks</label>
            <select
              id="kolom"
              value={textColumn}
              disabled={!data || analyzing}
              onChange={(e) => setTextColumn(e.target.value)}
              className="min-h-12 rounded-2xl border-[1.5px] border-[#D6CCF4] bg-white px-3.5 font-bold disabled:opacity-55"
            >
              {!data && <option value="">Belum ada file</option>}
              {data?.columns.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
            <span className="text-[13px] text-muted">
              {data ? 'Hanya kolom ini yang dianalisis.' : 'Pilihan kolom muncul setelah file diunggah.'}
            </span>
          </div>

          <div className="flex flex-col gap-3 rounded-[22px] bg-page p-4">
            <div className="flex items-center gap-3">
              <span className="flex size-[38px] shrink-0 items-center justify-center rounded-xl bg-pink text-[#C2416F]">
                <ShieldCheck size={20} aria-hidden="true" />
              </span>
              <span id="shield-label" className="flex-1 font-black">Privacy Shield</span>
              <button
                type="button"
                role="switch"
                aria-checked={privacy}
                aria-labelledby="shield-label"
                disabled={analyzing}
                onClick={() => setPrivacy((v) => !v)}
                className={`flex h-[34px] w-[58px] shrink-0 cursor-pointer rounded-full p-1 transition ${privacy ? 'justify-end bg-primary' : 'justify-start bg-[#D3CCE6]'}`}
              >
                <span className="block size-[26px] rounded-full bg-white shadow" />
              </button>
            </div>
            <p className="text-sm leading-relaxed text-muted">Sensor username, nomor telepon, dan NIM sebelum dianalisis.</p>
            <div className="rounded-xl bg-white px-3 py-2.5 text-sm leading-7">
              <div><span className="font-bold text-muted">Sebelum:</span> {sample}</div>
              <div><span className="font-bold text-muted">Sesudah:</span> {privacy ? anonymize(sample).text : sample}</div>
            </div>
          </div>

          <button
            type="button"
            onClick={handleAnalyze}
            disabled={!ready}
            aria-describedby="analisis-hint"
            className="flex min-h-14 cursor-pointer items-center justify-center gap-2.5 rounded-full bg-primary text-[17px] font-black text-white shadow-button transition hover:bg-primary-dark disabled:cursor-not-allowed disabled:bg-[#E6E1F2] disabled:text-[#6E6886] disabled:shadow-none"
          >
            {analyzing ? <><Loader2 size={20} className="animate-spin" aria-hidden="true" /> Menganalisis…</> : (
              <>Analisis sekarang {data ? <ArrowRight size={20} aria-hidden="true" /> : <Lock size={20} aria-hidden="true" />}</>
            )}
          </button>
          <p id="analisis-hint" className="-mt-2 text-center text-[13px] text-muted">
            {!data ? 'Unggah file terlebih dahulu untuk memulai analisis.' : analyzing ? 'Mohon tunggu, file sedang diproses.' : 'File besar bisa butuh beberapa detik.'}
          </p>
          {USE_MOCK && (
            <p className="rounded-xl bg-butter px-3 py-2 text-center text-xs font-bold text-[#6B5200]">Mode data dummy aktif (VITE_USE_MOCK=true)</p>
          )}
        </Card>
      </div>
    </div>
  )
}
