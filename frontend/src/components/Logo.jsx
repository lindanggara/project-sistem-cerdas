// Logo A: huruf "o" pada Scope diganti kaca pembesar yang membaca teks.
export function LensMark({ ring = '#6B5DC2', inner = '#FFFFFF', className = '' }) {
  return (
    <svg viewBox="0 0 44 52" aria-hidden="true" className={className}>
      <circle cx="19" cy="24" r="14.5" fill={inner} stroke={ring} strokeWidth="6.5" />
      <path d="M12 19.5h11" stroke="#E34948" strokeWidth="3.4" strokeLinecap="round" />
      <path d="M12 24.5h14" stroke="#EDA100" strokeWidth="3.4" strokeLinecap="round" />
      <path d="M12 29.5h8" stroke="#2A78D6" strokeWidth="3.4" strokeLinecap="round" />
      <path d="M30 35.5 40 46" stroke={ring} strokeWidth="7" strokeLinecap="round" />
    </svg>
  )
}

export default function Logo({ size = 32, tagline = false, light = false }) {
  const textColor = light ? '#FFFFFF' : '#2F2A3D'
  const accent = light ? '#FFE3A6' : '#6B5DC2'
  return (
    <span className="inline-flex flex-col gap-0.5">
      <span
        role="img"
        aria-label="TextScope"
        className="inline-flex items-baseline font-black leading-none tracking-[-0.035em]"
        style={{ fontSize: size }}
      >
        <span style={{ color: textColor }}>Text</span>
        <span style={{ color: accent }}>Sc</span>
        <span className="inline-block" style={{ width: '0.62em', height: '0.72em', verticalAlign: '-0.16em', margin: '0 0.01em' }}>
          <LensMark ring={accent} inner={light ? '#6B5DC2' : '#FFFFFF'} className="h-full w-full" />
        </span>
        <span style={{ color: accent }}>pe</span>
      </span>
      {tagline && (
        <span className="text-xs font-extrabold tracking-wide text-muted">Analisis emosi teks</span>
      )}
    </span>
  )
}
