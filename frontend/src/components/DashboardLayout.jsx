import { Link, NavLink, Outlet } from 'react-router-dom'
import { BarChart3, BookOpen, Lock, Upload } from 'lucide-react'
import Logo from './Logo.jsx'
import Owl from './Owl.jsx'
import { useAnalysis } from '../context/AnalysisContext.jsx'

function NavItem({ to, icon: Icon, label, locked }) {
  if (locked) {
    return (
      <div
        aria-disabled="true"
        title="Jalankan analisis terlebih dahulu"
        className="flex min-h-[52px] cursor-not-allowed items-center gap-3 rounded-[18px] px-2.5 font-bold text-[#7A7392]"
      >
        <span className="flex size-9 shrink-0 items-center justify-center rounded-xl bg-[#E2DBF3]">
          <Icon size={20} strokeWidth={2.2} aria-hidden="true" />
        </span>
        <span className="flex-1">{label}</span>
        <Lock size={16} strokeWidth={2.2} aria-label="Terkunci" />
      </div>
    )
  }
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex min-h-[52px] items-center gap-3 rounded-[18px] px-2.5 no-underline transition ${
          isActive
            ? 'bg-white font-extrabold text-primary shadow-soft'
            : 'font-bold text-[#4A4360] hover:bg-white/60'
        }`
      }
    >
      {({ isActive }) => (
        <>
          <span className={`flex size-9 shrink-0 items-center justify-center rounded-xl ${isActive ? 'bg-lilac' : 'bg-[#E2DBF3]'}`}>
            <Icon size={20} strokeWidth={2.2} aria-hidden="true" />
          </span>
          {label}
        </>
      )}
    </NavLink>
  )
}

export default function DashboardLayout() {
  const { result } = useAnalysis()
  return (
    <div className="flex min-h-screen flex-col bg-page lg:flex-row">
      <aside className="flex shrink-0 flex-col gap-5 bg-sidebar px-4 py-5 lg:sticky lg:top-0 lg:h-screen lg:w-[264px] lg:gap-7 lg:rounded-r-[32px] lg:py-7">
        <Link to="/" aria-label="TextScope, ke halaman utama" className="flex min-h-[52px] items-center px-2 no-underline">
          <Logo size={32} tagline />
        </Link>
        <nav aria-label="Navigasi utama" className="flex flex-row flex-wrap gap-2 lg:flex-col">
          <NavItem to="/upload" icon={Upload} label="Upload Data" />
          <NavItem to="/hasil" icon={BarChart3} label="Hasil Analisis" locked={!result} />
          <NavItem to="/panduan" icon={BookOpen} label="Panduan" />
        </nav>
        <div className="mt-auto hidden flex-col items-center gap-2 rounded-3xl bg-white p-4 text-center shadow-soft lg:flex">
          <Owl size={84} />
          <p className="font-extrabold">Butuh bantuan?</p>
          <p className="text-[13px] leading-snug text-muted">Lihat cara menyiapkan file dan membaca hasil.</p>
          <Link to="/panduan" className="flex min-h-10 items-center rounded-full bg-lilac px-4 text-sm font-extrabold text-primary no-underline">
            Buka panduan
          </Link>
        </div>
      </aside>
      <main className="min-w-0 flex-1 px-5 py-7 sm:px-8 lg:px-10 lg:py-9">
        <Outlet />
      </main>
    </div>
  )
}
