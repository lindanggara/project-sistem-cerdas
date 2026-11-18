import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import EmotionDonut from '../components/charts/EmotionDonut.jsx'
import TopicRadarChart from '../components/charts/TopicRadarChart.jsx'
import { ChevronLeft, ChevronRight, Download, Gauge, Loader2, ShieldCheck, Smile, Sparkles, Text } from 'lucide-react'
import Owl from '../components/Owl.jsx'
import { Card, Dot, EmotionChip, EmotionPill, PageHeader } from '../components/ui.jsx'
import { EMOTIONS, emotionInfo, formatNumber, tint } from '../lib/emotions.js'
import { exportResults } from '../lib/exportExcel.js'
import { useAnalysis } from '../context/AnalysisContext.jsx'

const PAGE_SIZE = 10

function Kpi({ bg, iconColor, icon: Icon, label, value, note }) {
  return (
    <div className="flex flex-col gap-2 rounded-[26px] p-5" style={{ background: bg }}>
      <div className="flex items-center justify-between gap-2">
        <span className="text-sm font-extrabold text-muted">{label}</span>
        <span className="flex size-11 shrink-0 items-center justify-center rounded-[15px] bg-white shadow-soft" style={{ color: iconColor }}>
          <Icon size={22} aria-hidden="true" />
        </span>
      </div>
      <span className="text-[32px] leading-tight font-black">{value}</span>
      <span className="text-[13px] text-muted">{note}</span>
    </div>
  )
}

export default function Hasil() {
  const { result } = useAnalysis()
  const { summary, distribution, topics, insight, results, meta } = result

  // Emosi aktif dipakai bersama oleh donat, daftar emosi, dan Topic Radar.
  const [activeEmotion, setActiveEmotion] = useState(summary.dominant_emotion ?? distribution[0].emotion)
  const activeInfo = emotionInfo(activeEmotion)
  // Topik yang sedang disorot di Topic Radar (indeks 0 = topik terkuat).
  const [activeTopic, setActiveTopic] = useState(0)

  function selectEmotion(e) {
    setActiveEmotion(e)
    setActiveTopic(0)
  }
  const [filter, setFilter] = useState('all')
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(1)
  const [exporting, setExporting] = useState(false)

  const maxPct = Math.max(...distribution.map((d) => d.percentage), 1)
  const countOf = Object.fromEntries(distribution.map((d) => [d.emotion, d.count]))
  const dominant = emotionInfo(summary.dominant_emotion)
  const dominantPct = distribution.find((d) => d.emotion === summary.dominant_emotion)?.percentage ?? 0

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return results.filter((r) => (filter === 'all' || r.emotion === filter) && (!q || r.text.toLowerCase().includes(q)))
  }, [results, filter, query])
  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const current = Math.min(page, pageCount)
  const rows = filtered.slice((current - 1) * PAGE_SIZE, current * PAGE_SIZE)

  const topicList = topics[activeEmotion] ?? []
  const maxScore = Math.max(...topicList.map((t) => t.score), 0.0001)

  async function handleExport() {
    setExporting(true)
    try { await exportResults(result) } finally { setExporting(false) }
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Hasil Analisis"
        subtitle={`${meta?.fileName ?? 'File'} · kolom “${meta?.textColumn ?? '-'}” · Privacy Shield ${meta?.privacyShield ? 'aktif' : 'nonaktif'}`}
        actions={<>
          <Link to="/upload" className="flex min-h-12 items-center rounded-full bg-white px-5 font-extrabold text-primary no-underline shadow-soft">Analisis file baru</Link>
          <button type="button" onClick={handleExport} disabled={exporting} className="flex min-h-12 cursor-pointer items-center gap-2 rounded-full bg-primary px-5.5 font-black text-white shadow-button hover:bg-primary-dark disabled:opacity-70">
            {exporting ? <Loader2 size={18} className="animate-spin" aria-hidden="true" /> : <Download size={18} aria-hidden="true" />}
            Unduh Excel
          </button>
        </>}
      />

      <div className="flex flex-wrap items-stretch gap-5">
        <section aria-label="Ringkasan otomatis" className="flex min-w-0 flex-[3_1_440px] flex-wrap items-center gap-5 rounded-[30px] bg-peach px-7 py-6">
          <Owl size={140} />
          <div className="flex min-w-0 flex-[1_1_240px] flex-col gap-2.5">
            <span className="flex items-center gap-1.5 self-start rounded-full bg-white px-3 py-1.5 text-[13px] font-black text-[#B4532A]">
              <Sparkles size={16} aria-hidden="true" /> Ringkasan otomatis
            </span>
            <p className="text-[17px] leading-relaxed font-semibold text-[#4A3A45]">{insight}</p>
          </div>
        </section>
        <div className="grid min-w-0 flex-[4_1_480px] grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-4">
          <Kpi bg="#ECE6FB" iconColor="#6B5DC2" icon={Text} label="Total teks" value={formatNumber(summary.total_texts)} note="teks yang dianalisis" />
          <Kpi bg="#FDE3E3" iconColor="#C93B3A" icon={Smile} label="Emosi dominan" value={dominant.nama} note={`${dominantPct}% dari seluruh teks`} />
          <Kpi bg="#DFF3EA" iconColor="#2E8A62" icon={Gauge} label="Rata-rata keyakinan" value={`${Math.round(summary.avg_confidence * 100)}%`} note="semakin tinggi, semakin yakin" />
          <Kpi bg="#FCE4EE" iconColor="#C2416F" icon={ShieldCheck} label="Data disensor" value={formatNumber(summary.censored_count)} note="username, telepon, NIM" />
        </div>
      </div>

      <div className="flex flex-wrap items-stretch gap-5">
        <Card className="flex min-w-0 flex-[1_1_440px] flex-col gap-5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-black">Distribusi 6 emosi</h2>
              <p className="mt-1 text-sm text-muted">Klik irisan atau baris emosi untuk memperbarui Topic Radar</p>
            </div>
            <span className="shrink-0 rounded-full bg-lilac px-3 py-1 text-[13px] font-extrabold text-primary">Interaktif</span>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-7">
            <EmotionDonut data={distribution} active={activeEmotion} onSelect={selectEmotion} />
            <ul className="flex min-w-0 flex-[1_1_230px] flex-col gap-1.5" aria-label="Pilih emosi">
              {distribution.map((d) => {
                const info = emotionInfo(d.emotion)
                const isActive = d.emotion === activeEmotion
                return (
                  <li key={d.emotion}>
                    <button
                      type="button"
                      aria-pressed={isActive}
                      onClick={() => selectEmotion(d.emotion)}
                      className={`flex min-h-12 w-full cursor-pointer flex-col justify-center gap-1.5 rounded-2xl px-3.5 py-2 text-left transition ${isActive ? 'bg-page' : 'hover:bg-page/70'}`}
                      style={{ boxShadow: isActive ? `inset 0 0 0 2px ${info.color}` : 'none' }}
                    >
                      <span className="flex w-full items-center gap-2 text-[15px]">
                        <Dot color={info.color} />
                        <span className={`flex-1 ${isActive ? 'font-black' : 'font-bold'}`}>{info.nama}</span>
                        <span className="text-sm font-bold">{formatNumber(d.count)}</span>
                        <span className="w-14 text-right text-sm text-muted">({d.percentage}%)</span>
                      </span>
                      <span className="block h-[6px] w-full overflow-hidden rounded-full bg-[#F0ECF8]">
                        <span className="block h-full rounded-full" style={{ width: `${(d.percentage / maxPct) * 100}%`, background: info.color }} />
                      </span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </div>
          <div className="mt-auto flex justify-between gap-3 border-t border-line pt-4 text-[13px] text-muted">
            <span>{formatNumber(summary.total_texts)} teks dianalisis</span>
            <span>6 kategori emosi</span>
          </div>
        </Card>

        <Card className="flex min-w-0 flex-[1_1_440px] flex-col gap-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div className="min-w-0">
              <h2 className="flex flex-wrap items-center gap-2 text-xl font-black">
                Topic Radar:
                <span className="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-[15px] font-black" style={{ background: tint(activeEmotion, '2E') }}>
                  <Dot color={activeInfo.color} />{activeInfo.nama}
                </span>
              </h2>
              <p className="mt-1 text-sm text-muted">Topik dan kata kunci pemicu utama emosi <b className="text-ink">{activeInfo.nama}</b> · {formatNumber(countOf[activeEmotion] ?? 0)} teks</p>
            </div>
            <div role="group" aria-label="Pilih emosi" className="flex gap-1">
              {EMOTIONS.map((e) => {
                const isActive = e === activeEmotion
                return (
                  <button
                    key={e}
                    type="button"
                    aria-pressed={isActive}
                    aria-label={emotionInfo(e).nama}
                    title={emotionInfo(e).nama}
                    onClick={() => selectEmotion(e)}
                    className="flex size-8 cursor-pointer items-center justify-center rounded-full"
                  >
                    <span
                      className="block rounded-full transition-all"
                      style={{
                        width: isActive ? 24 : 18,
                        height: isActive ? 24 : 18,
                        background: emotionInfo(e).color,
                        opacity: isActive ? 1 : 0.55,
                        boxShadow: isActive ? `0 0 0 3px #FFFFFF, 0 0 0 5px ${emotionInfo(e).color}` : 'none',
                      }}
                    />
                  </button>
                )
              })}
            </div>
          </div>

          {topicList.length === 0 ? (
            <p className="flex flex-1 items-center justify-center rounded-[22px] bg-page px-6 py-16 text-center font-semibold text-muted">
              Data untuk emosi ini belum cukup untuk dianalisis topiknya.
            </p>
          ) : topicList.length >= 3 ? (
            <TopicRadarChart topics={topicList} color={activeInfo.color} activeIndex={activeTopic} onSelect={setActiveTopic} />
          ) : (
            <ul className="flex flex-col gap-3 rounded-[22px] bg-page px-5 py-4">
              {topicList.map((t) => (
                <li key={t.topic} className="flex justify-between font-extrabold capitalize">{t.topic}<span className="text-sm text-muted">skor {t.score.toFixed(2)}</span></li>
              ))}
            </ul>
          )}

          {topicList.length > 0 && (
            <div className="flex flex-col gap-2.5">
              <span className="text-[13px] font-extrabold tracking-wide text-muted uppercase">Topik &amp; kata kuncinya</span>
              <ul className="flex flex-col gap-2">
                {topicList.map((t, i) => {
                  const isActive = i === activeTopic
                  const width = Math.round((t.score / maxScore) * 100)
                  return (
                    <li key={t.topic}>
                      <button
                        type="button"
                        aria-pressed={isActive}
                        onClick={() => setActiveTopic(i)}
                        className="flex w-full cursor-pointer flex-col gap-2 rounded-2xl px-3.5 py-3 text-left transition"
                        style={{
                          background: isActive ? tint(activeEmotion, '1F') : '#F7F4FC',
                          boxShadow: isActive ? `inset 0 0 0 2px ${activeInfo.color}` : 'none',
                        }}
                      >
                        <span className="flex items-center gap-3">
                          <span className="flex size-7 shrink-0 items-center justify-center rounded-[9px] bg-white text-[13px] font-black text-primary">{i + 1}</span>
                          <span className={`flex-1 capitalize ${isActive ? 'font-black' : 'font-extrabold'}`}>{t.topic}</span>
                          <span className="hidden h-2 w-20 overflow-hidden rounded-full bg-white sm:block">
                            <span className="block h-full rounded-full" style={{ width: `${width}%`, background: activeInfo.color }} />
                          </span>
                          <span className="w-12 text-right text-[13px] font-bold text-muted">{t.score.toFixed(2)}</span>
                        </span>
                        {t.keywords?.length > 0 && (
                          <span className="flex flex-wrap gap-1.5 pl-10">
                            {t.keywords.map((k) => (
                              <span key={k} className="rounded-lg bg-white px-2.5 py-1 text-sm font-semibold">
                                <span className="text-muted">#</span> {k}
                              </span>
                            ))}
                          </span>
                        )}
                      </button>
                    </li>
                  )
                })}
              </ul>
            </div>
          )}
        </Card>
      </div>

      <Card className="flex flex-col gap-4">
        <div className="flex flex-wrap items-end justify-between gap-3.5">
          <div>
            <h2 className="text-xl font-black">Detail per teks</h2>
            <p className="mt-1 text-sm text-muted">Hasil prediksi untuk setiap baris data</p>
          </div>
          <div className="flex min-w-[220px] flex-[0_1_300px] flex-col gap-1">
            <label htmlFor="cari" className="text-[13px] font-extrabold text-muted">Cari teks</label>
            <input
              id="cari"
              type="search"
              value={query}
              onChange={(e) => { setQuery(e.target.value); setPage(1) }}
              placeholder="mis. ongkir, refund…"
              className="min-h-[46px] rounded-full border-[1.5px] border-[#D6CCF4] bg-page px-4"
            />
          </div>
        </div>
        <div role="group" aria-label="Filter emosi" className="flex flex-wrap gap-2">
          <EmotionPill label="Semua" color="#6B5DC2" active={filter === 'all'} onClick={() => { setFilter('all'); setPage(1) }} />
          {EMOTIONS.map((e) => (
            <EmotionPill key={e} label={emotionInfo(e).nama} color={emotionInfo(e).color} active={filter === e} onClick={() => { setFilter(e); setPage(1) }} />
          ))}
        </div>
        <div className="overflow-x-auto rounded-[18px] border border-line">
          <table className="w-full min-w-[680px] border-collapse text-[15px]">
            <thead>
              <tr className="bg-page text-left text-muted">
                <th className="w-14 px-4 py-3 font-extrabold">No</th>
                <th className="px-4 py-3 font-extrabold">Teks</th>
                <th className="w-36 px-4 py-3 font-extrabold">Emosi</th>
                <th className="w-48 px-4 py-3 font-extrabold">Keyakinan</th>
              </tr>
            </thead>
            <tbody>
              {rows.length === 0 && (
                <tr><td colSpan={4} className="px-4 py-8 text-center font-semibold text-muted">Tidak ada teks yang cocok.</td></tr>
              )}
              {rows.map((r) => (
                <tr key={r.id} className="border-t border-[#F0ECF8]">
                  <td className="px-4 py-3.5 text-muted">{r.id}</td>
                  <td className="px-4 py-3.5 leading-snug">{r.text}</td>
                  <td className="px-4 py-3.5"><EmotionChip emotion={r.emotion} /></td>
                  <td className="px-4 py-3.5">
                    <div className="flex items-center gap-2.5">
                      <div className="h-[9px] flex-1 overflow-hidden rounded-full bg-[#F0ECF8]">
                        <div className="h-full rounded-full bg-primary" style={{ width: `${r.confidence * 100}%` }} />
                      </div>
                      <span className="w-10 text-right font-extrabold">{Math.round(r.confidence * 100)}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="text-sm text-muted">
            {filtered.length ? `Menampilkan ${(current - 1) * PAGE_SIZE + 1}–${(current - 1) * PAGE_SIZE + rows.length} dari ${formatNumber(filtered.length)} teks` : '0 teks'}
          </span>
          <div className="flex items-center gap-2">
            <button type="button" aria-label="Halaman sebelumnya" disabled={current <= 1} onClick={() => setPage(current - 1)} className="flex size-11 cursor-pointer items-center justify-center rounded-full bg-lilac text-primary disabled:cursor-not-allowed disabled:opacity-40">
              <ChevronLeft size={18} aria-hidden="true" />
            </button>
            <span className="min-w-16 text-center text-sm font-extrabold">{current} / {pageCount}</span>
            <button type="button" aria-label="Halaman berikutnya" disabled={current >= pageCount} onClick={() => setPage(current + 1)} className="flex size-11 cursor-pointer items-center justify-center rounded-full bg-lilac text-primary disabled:cursor-not-allowed disabled:opacity-40">
              <ChevronRight size={18} aria-hidden="true" />
            </button>
          </div>
        </div>
      </Card>
    </div>
  )
}
