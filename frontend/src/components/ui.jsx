import { emotionInfo, tint } from '../lib/emotions.js'

export function Card({ className = '', children, ...props }) {
  return (
    <section className={`rounded-[28px] bg-white p-6 shadow-soft ${className}`} {...props}>
      {children}
    </section>
  )
}

export function PageHeader({ title, subtitle, actions }) {
  return (
    <header className="flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        <h1 className="text-[34px] font-black tracking-tight">{title}</h1>
        {subtitle && <p className="mt-1 text-muted">{subtitle}</p>}
      </div>
      {actions && <div className="flex flex-wrap gap-2.5">{actions}</div>}
    </header>
  )
}

export function Dot({ color, size = 10 }) {
  return <span className="inline-block shrink-0 rounded-full" style={{ width: size, height: size, background: color }} />
}

export function EmotionChip({ emotion }) {
  const info = emotionInfo(emotion)
  return (
    <span className="inline-flex items-center gap-2 rounded-full px-3 py-1.5 text-sm font-extrabold" style={{ background: tint(emotion, '1F') }}>
      <Dot color={info.color} size={9} />
      {info.nama}
    </span>
  )
}

// Tombol pil untuk memilih emosi (Topic Radar dan filter tabel).
export function EmotionPill({ label, color, active, onClick }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={`flex min-h-[42px] cursor-pointer items-center gap-2 rounded-full px-4 text-sm transition ${active ? 'font-black' : 'font-bold hover:brightness-95'}`}
      style={{
        background: active ? color + '2E' : '#F7F4FC',
        boxShadow: active ? `inset 0 0 0 2px ${color}` : 'none',
      }}
    >
      <Dot color={color} />
      {label}
    </button>
  )
}
