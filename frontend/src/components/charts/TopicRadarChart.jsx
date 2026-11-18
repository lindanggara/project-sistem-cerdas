import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer } from 'recharts'

// Label sudut dipecah per kata supaya topik panjang tidak terpotong di layar kecil.
function WrappedTick({ x, y, textAnchor, payload }) {
  const words = String(payload.value).split(' ')
  const lines = words.length > 1 ? [words.slice(0, Math.ceil(words.length / 2)).join(' '), words.slice(Math.ceil(words.length / 2)).join(' ')] : words
  const dy = y < 150 ? -(lines.length - 1) * 14 : 0
  return (
    <text x={x} y={y + dy} textAnchor={textAnchor} fill="#2F2A3D" fontSize={12} fontWeight={700}>
      {lines.map((l, i) => <tspan key={i} x={x} dy={i === 0 ? 0 : 14}>{l}</tspan>)}
    </text>
  )
}

// Grafik radar: setiap sudut = satu topik, jarak dari pusat = skor topik.
export default function TopicRadarChart({ topics, color }) {
  const max = Math.max(...topics.map((t) => t.score), 0.0001)
  const data = topics.map((t) => ({ topic: t.topic, value: Math.round((t.score / max) * 100) }))
  return (
    <div className="h-[300px] w-full" role="img" aria-label={`Radar topik: ${topics.map((t) => t.topic).join(', ')}`}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="58%" margin={{ top: 16, right: 48, bottom: 16, left: 48 }}>
          <PolarGrid stroke="#E6E0F5" />
          <PolarAngleAxis dataKey="topic" tick={<WrappedTick />} />
          <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
          <Radar
            dataKey="value"
            stroke={color}
            strokeWidth={3}
            fill={color}
            fillOpacity={0.2}
            dot={{ r: 5, fill: '#FFFFFF', stroke: color, strokeWidth: 3 }}
            isAnimationActive
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
