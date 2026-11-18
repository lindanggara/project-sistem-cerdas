// Data dummy untuk dipakai selama backend belum siap.
// Bentuk keluarannya SAMA dengan respons POST /analyze yang disepakati.
import { EMOTIONS, emotionInfo } from './emotions.js'

const KEYWORDS = {
  anger: ['kesel', 'kesal', 'marah', 'emosi', 'lambat', 'parah', 'jelek', 'mahal', 'nyebelin', 'kecewa berat', 'tolol'],
  fear: ['takut', 'khawatir', 'cemas', 'ngeri', 'was-was', 'diretas', 'penipuan', 'tipu'],
  joy: ['senang', 'seneng', 'makasih', 'terima kasih', 'mantap', 'puas', 'bagus', 'cepat', 'keren', 'lulus'],
  love: ['sayang', 'cinta', 'kangen', 'rindu', 'suka banget', 'favorit'],
  sad: ['sedih', 'kecewa', 'nangis', 'rusak', 'hilang', 'gagal', 'batal', 'sendiri'],
}

// Setiap topik punya kata kunci (dari NMF: kata dengan bobot tertinggi di topik itu).
const TOPICS = {
  anger: [['harga', ['mahal', 'naik terus']], ['pelayanan', ['cs lambat', 'nggak dibalas']], ['pengiriman', ['telat', 'kurir']], ['aplikasi', ['error', 'bug']], ['promo', ['syarat ribet']]],
  fear: [['keamanan akun', ['diretas', 'kode otp']], ['pengembalian dana', ['refund', 'uang balik']], ['penipuan', ['tipu', 'curiga']], ['data pribadi', ['bocor']], ['pembayaran', ['terpotong']]],
  joy: [['kecepatan', ['cepat sampai', 'kilat']], ['kualitas', ['puas', 'original']], ['pelayanan', ['ramah banget']], ['harga/promo', ['diskon', 'gratis ongkir']], ['kemudahan', ['gampang', 'praktis']]],
  love: [['produk favorit', ['langganan', 'suka banget']], ['hadiah', ['kado', 'buat ibu']], ['toko', ['setia', 'terbaik']], ['kemasan', ['lucu', 'rapi']], ['pelayanan', ['perhatian']]],
  sad: [['barang rusak', ['rusak', 'pecah']], ['pengembalian dana', ['refund lama']], ['pesanan batal', ['dibatalkan', 'stok habis']], ['pengiriman', ['hilang', 'nyasar']], ['ulasan', ['kecewa']]],
  neutral: [['status pesanan', ['dikirim', 'diproses']], ['pertanyaan produk', ['ukuran', 'warna']], ['jadwal', ['hari senin', 'jam']], ['pembayaran', ['transfer']], ['alamat', ['ubah alamat']]],
}

// Angka acak yang selalu sama untuk teks yang sama.
function hash(str) {
  let h = 2166136261
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return (h >>> 0) / 4294967295
}

export function anonymize(text) {
  let count = 0
  const out = text
    .replace(/@[A-Za-z0-9_.]+/g, () => { count++; return '[USERNAME]' })
    .replace(/(\+62|62|0)8[0-9\-\s]{7,13}[0-9]/g, () => { count++; return '[PHONE]' })
    .replace(/\b\d{8,12}\b/g, () => { count++; return '[NIM]' })
  return { text: out, count }
}

function guessEmotion(text) {
  const t = text.toLowerCase()
  for (const emo of Object.keys(KEYWORDS)) {
    if (KEYWORDS[emo].some((k) => t.includes(k))) return { emotion: emo, confidence: 0.82 + hash(t) * 0.15 }
  }
  // Tanpa kata kunci emosi: kebanyakan dianggap netral.
  const r = hash(t)
  const emotion = r < 0.7 ? 'neutral' : EMOTIONS[Math.floor(hash(t + 'e') * EMOTIONS.length)]
  return { emotion, confidence: 0.55 + hash(t + 'c') * 0.3 }
}

export async function mockAnalyze({ rows, textColumn, privacyShield }) {
  await new Promise((r) => setTimeout(r, 1200))

  let censored = 0
  const results = rows
    .map((row) => String(row[textColumn] ?? '').trim())
    .filter(Boolean)
    .map((raw, i) => {
      let text = raw
      if (privacyShield) {
        const a = anonymize(raw)
        text = a.text
        censored += a.count
      }
      const { emotion, confidence } = guessEmotion(raw)
      return { id: i + 1, text, emotion, confidence: Math.round(confidence * 100) / 100 }
    })

  const total = results.length
  const counts = Object.fromEntries(EMOTIONS.map((e) => [e, 0]))
  results.forEach((r) => { counts[r.emotion]++ })
  const distribution = EMOTIONS
    .map((e) => ({ emotion: e, count: counts[e], percentage: total ? Math.round((counts[e] / total) * 1000) / 10 : 0 }))
    .sort((a, b) => b.count - a.count)

  const topics = Object.fromEntries(EMOTIONS.map((e) => [
    e,
    counts[e] < 3 ? [] : TOPICS[e].map(([topic, keywords], i) => ({
      topic,
      score: Math.round((0.42 - i * 0.06 + hash(topic + e) * 0.08) * 100) / 100,
      keywords,
    })),
  ]))

  const [first, second] = distribution
  const name = (e) => emotionInfo(e).nama.toLowerCase()
  const t1 = topics[first.emotion].slice(0, 2).map((t) => t.topic).join(' dan ')
  const insight = total
    ? `Emosi yang paling banyak muncul adalah ${name(first.emotion)} (${first.percentage}%)` +
      (t1 ? `, terutama terkait ${t1}` : '') +
      (second && second.count ? `. Disusul emosi ${name(second.emotion)} (${second.percentage}%).` : '.')
    : 'Tidak ada teks yang bisa dianalisis.'

  return {
    status: 'success',
    summary: {
      total_texts: total,
      dominant_emotion: first.emotion,
      avg_confidence: total ? Math.round((results.reduce((s, r) => s + r.confidence, 0) / total) * 100) / 100 : 0,
      censored_count: censored,
    },
    distribution,
    topics,
    insight,
    results,
  }
}
