import { emotionInfo, formatNumber } from '../../lib/emotions.js'

// Donat buatan sendiri (SVG) supaya irisan yang dipilih bisa "menonjol" keluar.
function arcPath(cx, cy, rOuter, rInner, start, end) {
  const toXY = (r, a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)]
  const large = end - start > Math.PI ? 1 : 0
  const [x1, y1] = toXY(rOuter, start)
  const [x2, y2] = toXY(rOuter, end)
  const [x3, y3] = toXY(rInner, end)
  const [x4, y4] = toXY(rInner, start)
  return `M${x1} ${y1} A${rOuter} ${rOuter} 0 ${large} 1 ${x2} ${y2} L${x3} ${y3} A${rInner} ${rInner} 0 ${large} 0 ${x4} ${y4}Z`
}

export default function EmotionDonut({ data, active, onSelect, size = 240 }) {
  const total = data.reduce((s, d) => s + d.count, 0) || 1
  const c = size / 2
  const rOuter = c - 14
  const rInner = rOuter - 30
  const gap = 0.025
  let angle = -Math.PI / 2
  const slices = data.filter((d) => d.count > 0).map((d) => {
    const sweep = (d.count / total) * Math.PI * 2
    const start = angle + (sweep > gap * 2 ? gap / 2 : 0)
    const end = angle + sweep - (sweep > gap * 2 ? gap / 2 : 0)
    angle += sweep
    return { ...d, start, end, full: sweep >= Math.PI * 2 - 0.0001 }
  })
  const activeData = data.find((d) => d.emotion === active)
  const info = emotionInfo(active)

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
        {slices.map((s) => {
          const isActive = s.emotion === active
          const ro = isActive ? rOuter + 12 : rOuter
          const ri = isActive ? rInner - 2 : rInner
          const color = emotionInfo(s.emotion).color
          return s.full ? (
            <circle key={s.emotion} cx={c} cy={c} r={(ro + ri) / 2} fill="none" stroke={color} strokeWidth={ro - ri}
              className="cursor-pointer" onClick={() => onSelect(s.emotion)} />
          ) : (
            <path
              key={s.emotion}
              d={arcPath(c, c, ro, ri, s.start, s.end)}
              fill={color}
              opacity={isActive ? 1 : 0.88}
              className="cursor-pointer transition-all duration-300 hover:opacity-100"
              style={isActive ? { filter: `drop-shadow(0 6px 10px ${color}66)` } : undefined}
              onClick={() => onSelect(s.emotion)}
            />
          )
        })}
      </svg>
      <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-[11px] font-extrabold tracking-[0.12em] text-muted uppercase">Radar aktif</span>
        <span className="text-[26px] leading-tight font-black" style={{ color: info.color === '#EDA100' ? '#B87D00' : info.color }}>{info.nama}</span>
        <span className="text-[13px] font-semibold text-muted">
          {formatNumber(activeData?.count ?? 0)} teks ({activeData?.percentage ?? 0}%)
        </span>
      </div>
    </div>
  )
}
