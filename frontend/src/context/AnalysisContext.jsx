import { createContext, useContext, useState } from 'react'

const AnalysisContext = createContext(null)
const STORAGE_KEY = 'textscope:result'

// Hasil disimpan di sessionStorage supaya tidak hilang saat halaman di-refresh
// atau saat pengguna pindah ke Panduan lalu kembali.
function loadSaved() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function AnalysisProvider({ children }) {
  const [result, setResultState] = useState(loadSaved)

  function setResult(next) {
    setResultState(next)
    try {
      if (next) sessionStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      else sessionStorage.removeItem(STORAGE_KEY)
    } catch {
      // Penyimpanan penuh atau diblokir browser: hasil tetap ada selama tab terbuka.
    }
  }

  return (
    <AnalysisContext.Provider value={{ result, setResult, clearResult: () => setResult(null) }}>
      {children}
    </AnalysisContext.Provider>
  )
}

export function useAnalysis() {
  return useContext(AnalysisContext)
}
