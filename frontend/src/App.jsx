import { Navigate, Route, Routes } from 'react-router-dom'
import DashboardLayout from './components/DashboardLayout.jsx'
import Landing from './pages/Landing.jsx'
import Upload from './pages/Upload.jsx'
import Hasil from './pages/Hasil.jsx'
import Panduan from './pages/Panduan.jsx'
import { useAnalysis } from './context/AnalysisContext.jsx'

// Halaman Hasil hanya bisa dibuka kalau sudah ada hasil analisis.
function RequireResult({ children }) {
  const { result } = useAnalysis()
  return result ? children : <Navigate to="/upload" replace />
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route element={<DashboardLayout />}>
        <Route path="/upload" element={<Upload />} />
        <Route path="/hasil" element={<RequireResult><Hasil /></RequireResult>} />
        <Route path="/panduan" element={<Panduan />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
