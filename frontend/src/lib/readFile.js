import Papa from 'papaparse'
import { readSheet } from 'read-excel-file/browser'

export const MAX_FILE_MB = 10
export const ACCEPTED_EXT = ['.csv', '.xlsx']

function extOf(name) {
  const i = name.lastIndexOf('.')
  return i >= 0 ? name.slice(i).toLowerCase() : ''
}

// Cek format dan ukuran sebelum file dibaca.
export function validateFile(file) {
  if (!file) return 'Belum ada file yang dipilih.'
  if (!ACCEPTED_EXT.includes(extOf(file.name))) {
    return 'Format file tidak didukung. Gunakan file .csv atau .xlsx.'
  }
  if (file.size > MAX_FILE_MB * 1024 * 1024) {
    return `Ukuran file melebihi ${MAX_FILE_MB} MB.`
  }
  return null
}

function cleanHeader(h, i) {
  const s = String(h ?? '').trim()
  return s || `kolom_${i + 1}`
}

async function readCsv(file) {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: 'greedy',
      transformHeader: cleanHeader,
      complete: (res) => resolve({ columns: res.meta.fields ?? [], rows: res.data }),
      error: reject,
    })
  })
}

async function readXlsx(file) {
  const data = await readSheet(file)
  if (!data.length) return { columns: [], rows: [] }
  const columns = data[0].map(cleanHeader)
  const rows = data.slice(1)
    .filter((r) => r.some((v) => v !== null && String(v).trim() !== ''))
    .map((r) => Object.fromEntries(columns.map((c, i) => [c, r[i] ?? ''])))
  return { columns, rows }
}

// Tebak kolom teks: kolom dengan rata-rata panjang isi paling besar.
function guessTextColumn(columns, rows) {
  const sample = rows.slice(0, 50)
  let best = columns[0]
  let bestLen = -1
  for (const c of columns) {
    const avg = sample.reduce((sum, r) => sum + String(r[c] ?? '').length, 0) / (sample.length || 1)
    if (avg > bestLen) { best = c; bestLen = avg }
  }
  return best
}

// Membaca file .csv / .xlsx di browser untuk pratinjau dan pilihan kolom.
export async function readDataFile(file) {
  const parsed = extOf(file.name) === '.csv' ? await readCsv(file) : await readXlsx(file)
  if (!parsed.columns.length || !parsed.rows.length) {
    throw new Error('File kosong atau tidak memiliki baris data.')
  }
  return { ...parsed, suggestedColumn: guessTextColumn(parsed.columns, parsed.rows) }
}
