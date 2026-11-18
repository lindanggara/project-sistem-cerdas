// Satu emosi = satu warna di semua bagian dashboard.
// Warna diambil dari dashboard/app.py di repo agar konsisten.
export const EMOTIONS = ['anger', 'fear', 'joy', 'love', 'sad', 'neutral']

export const EMOTION_INFO = {
  anger:   { nama: 'Marah',  color: '#E34948', arti: 'Kesal, jengkel, atau tidak terima terhadap sesuatu.', contoh: 'Kesel banget, CS nggak balas dari kemarin.' },
  fear:    { nama: 'Takut',  color: '#6250D6', arti: 'Cemas, khawatir, atau merasa terancam.', contoh: 'Aku khawatir akunku diretas.' },
  joy:     { nama: 'Senang', color: '#EDA100', arti: 'Gembira, puas, atau bersyukur.', contoh: 'Paketnya sampai cepat, makasih!' },
  love:    { nama: 'Cinta',  color: '#E87BA4', arti: 'Sayang, kagum, atau rasa dekat dengan seseorang atau sesuatu.', contoh: 'Sayang banget sama toko ini.' },
  sad:     { nama: 'Sedih',  color: '#2A78D6', arti: 'Kecewa, kehilangan, atau patah semangat.', contoh: 'Sedih, barangnya ternyata rusak.' },
  neutral: { nama: 'Netral', color: '#1BAF7A', arti: 'Informasi atau pernyataan tanpa muatan emosi yang jelas.', contoh: 'Pesanan saya dikirim hari Senin.' },
}

export function emotionInfo(key) {
  return EMOTION_INFO[key] ?? { nama: key, color: '#8A84A0', arti: '', contoh: '' }
}

// Warna transparan untuk latar label (hex + alpha).
export function tint(key, alpha = '26') {
  return emotionInfo(key).color + alpha
}

export function formatNumber(n) {
  return Number(n ?? 0).toLocaleString('id-ID')
}
