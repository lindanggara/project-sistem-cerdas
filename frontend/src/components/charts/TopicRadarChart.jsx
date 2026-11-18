import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer } from 'recharts'

// Label sudut dipecah per kata supaya topik panjang tidak terpotong di layar kecil.
function WrappedTick({ x, y, textAnchor, payload, activeTopic }) {
  const words = String(payload.value).split(' ')
  const half = Math.ceil(words.length / 2)
  const lines = words.length > 1 ? [words.slice(0, half).join(' '), words.slice(half).join(' ')] : words
  const dy = y < 150 ? -(lines.length - 1) * 14 : 0
  const isActive = payload.value === activeTopic
  return (
    <text x={x} y={y + dy} textAnchor={textAnchor} fill={isActive ? '#2F2A3D' : '#5F5875'} fontSize={12} fontWeight={isActive ? 900 : 700}>
      {lines.map((l, i) => <tspan key={i} x={x} dy={i === 0 ? 0 : 14}>{l}</tspan>)}
    </text>
  )
}

// Grafik radar: setiap sudut = satu topik, jarak dari pusat = skor topik.
// Titik bisa diklik untuk memilih topik (kata kuncinya ikut tersorot di daftar).
export default function TopicRadarChart({ topics, color, activeIndex, onSelect }) {
  const max = Math.max(...topics.map((t) => t.score), 0.0001)
  const data = topics.map((t) => ({ topic: t.topic, value: Math.round((t.score / max) * 100) }))
  const activeTopic = topics[activeIndex]?.topic

  const renderDot = ({ cx, cy, index }) => {
    const isActive = index === activeIndex
    return (
      <g key={index} className="cursor-pointer" onClick={() => onSelect?.(index)}>
        <circle cx={cx} cy={cy} r={14} fill="transparent" />
        <circle cx={cx} cy={cy} r={isActive ? 8 : 5} fill={isActive ? color : '#FFFFFF'} stroke={color} strokeWidth={3} />
      </g>
    )
  }

  return (
    <div className="h-[300px] w-full" role="img" aria-label={`Radar topik: ${topics.map((t) => t.topic).join(', ')}`}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="58%" margin={{ top: 16, right: 48, bottom: 16, left: 48 }}>
          <PolarGrid stroke="#E6E0F5" />
          <PolarAngleAxis dataKey="topic" tick={<WrappedTick activeTopic={activeTopic} />} />
          <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
          <Radar dataKey="value" stroke={color} strokeWidth={3} fill={color} fillOpacity={0.2} dot={renderDot} activeDot={false} isAnimationActive={false} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}