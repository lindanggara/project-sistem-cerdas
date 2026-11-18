import writeExcelFile from 'write-excel-file/browser'
import { emotionInfo } from './emotions.js'

const HEADER = { fontWeight: 'bold', backgroundColor: '#ECE6FB' }

export async function exportResults(result) {
  const sheet = [
    [
      { value: 'No', ...HEADER },
      { value: 'Teks', ...HEADER },
      { value: 'Emosi', ...HEADER },
      { value: 'Label', ...HEADER },
      { value: 'Keyakinan (%)', ...HEADER },
    ],
    ...result.results.map((r, i) => [
      { value: i + 1 },
      { value: r.text },
      { value: emotionInfo(r.emotion).nama },
      { value: r.emotion },
      { value: Math.round(r.confidence * 100) },
    ]),
  ]
  const base = (result.meta?.fileName ?? 'data').replace(/\.[^.]+$/, '')
  await writeExcelFile(sheet, {
    columns: [{ width: 6 }, { width: 70 }, { width: 12 }, { width: 10 }, { width: 14 }],
  }).toFile(`hasil_textscope_${base}.xlsx`)
}
