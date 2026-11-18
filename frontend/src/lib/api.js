import { mockAnalyze } from './mockApi.js'
import { EMOTIONS } from './emotions.js'

const API_URL = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000').replace(/\/$/, '')
export const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'

// Pastikan keenam emosi selalu ada, walau jumlahnya 0, supaya grafik konsisten.
function normalize(data) {
  const byEmotion = Object.fromEntries((data.distribution ?? []).map((d) => [d.emotion, d]))
  const distribution = EMOTIONS
    .map((e) => byEmotion[e] ?? { emotion: e, count: 0, percentage: 0 })
    .sort((a, b) => b.count - a.count)
  const topics = Object.fromEntries(EMOTIONS.map((e) => [e, data.topics?.[e] ?? []]))
  return { ...data, distribution, topics, results: data.results ?? [] }
}

/**
 * Kirim file ke backend: POST /analyze (multipart/form-data)
 *   file           : File .csv / .xlsx
 *   text_column    : nama kolom teks
 *   privacy_shield : "true" / "false"
 */
export async function analyzeFile({ file, rows, textColumn, privacyShield }) {
  if (USE_MOCK) {
    return normalize(await mockAnalyze({ rows, textColumn, privacyShield }))
  }

  const form = new FormData()
  form.append('file', file)
  form.append('text_column', textColumn)
  form.append('privacy_shield', String(privacyShield))

  let res
  try {
    res = await fetch(`${API_URL}/analyze`, { method: 'POST', body: form })
  } catch {
    throw new Error('Tidak bisa terhubung ke server. Coba lagi beberapa saat lagi.')
  }

  let data = null
  try {
    data = await res.json()
  } catch {
    // respons bukan JSON
  }
  if (!res.ok || data?.status !== 'success') {
    throw new Error(data?.message ?? `Analisis gagal (kode ${res.status}).`)
  }
  return normalize(data)
}
