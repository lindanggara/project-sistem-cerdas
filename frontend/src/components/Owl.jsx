import { useId } from 'react'

// Maskot TextScope: burung hantu berkacamata dengan kaca pembesar.
export default function Owl({ size = 120, label = 'Maskot TextScope', className = '' }) {
  const id = useId().replace(/:/g, '')
  const g = `owl-body-${id}`
  const l = `owl-lens-${id}`
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" role="img" aria-label={label} className={`block shrink-0 ${className}`}>
<defs><radialGradient id={g} cx="35%" cy="28%" r="85%"><stop offset="0" stopColor="#D6C9FF"/><stop offset="0.6" stopColor="#A08BEE"/><stop offset="1" stopColor="#7259CF"/></radialGradient>
      <radialGradient id={l} cx="35%" cy="30%" r="80%"><stop offset="0" stopColor="#FFFFFF"/><stop offset="1" stopColor="#DDE7FF"/></radialGradient></defs>
      <ellipse cx="96" cy="191" rx="58" ry="8" fill="#2F2A3D" opacity="0.10"/>
      <path d="M50 62 L40 24 L80 46Z" fill="#7A64D2"/><path d="M142 62 L152 24 L112 46Z" fill="#7A64D2"/>
      <path d="M96 38 C148 38 166 80 166 124 C166 164 136 184 96 184 C56 184 26 164 26 124 C26 80 44 38 96 38Z" fill={`url(#${g})`}/>
      <ellipse cx="96" cy="150" rx="38" ry="30" fill="#EFE9FF"/>
      <path d="M80 144 q6 6 12 0 M100 144 q6 6 12 0 M90 158 q6 6 12 0" stroke="#C9BDF2" strokeWidth="3" fill="none" strokeLinecap="round"/>
      <ellipse cx="34" cy="134" rx="11" ry="23" fill="#8C76E0" transform="rotate(12 34 134)"/>
      <ellipse cx="54" cy="124" rx="8" ry="5" fill="#FF9DB8" opacity="0.8"/>
      <circle cx="66" cy="96" r="21" fill="#FFFFFF" stroke="#5B4BB0" strokeWidth="6"/>
      <circle cx="68" cy="98" r="9" fill="#2F2A3D"/><circle cx="71.5" cy="94" r="3.4" fill="#FFFFFF"/>
      <path d="M87 94 Q93 88 99 92" stroke="#5B4BB0" strokeWidth="5" fill="none" strokeLinecap="round"/>
      <path d="M150 128 L186 168" stroke="#5B4BB0" strokeWidth="17" strokeLinecap="round"/>
      <path d="M156 135 L181 163" stroke="#8D7BE0" strokeWidth="5" strokeLinecap="round"/>
      <circle cx="128" cy="100" r="33" fill={`url(#${l})`} stroke="#5B4BB0" strokeWidth="10"/>
      <path d="M106 88 A24 24 0 0 1 122 72" stroke="#FFFFFF" strokeWidth="5" fill="none" strokeLinecap="round"/>
      <circle cx="130" cy="103" r="15" fill="#2F2A3D"/><circle cx="135.5" cy="96.5" r="5.5" fill="#FFFFFF"/><circle cx="126" cy="109" r="2.2" fill="#FFFFFF"/>
      <ellipse cx="163" cy="148" rx="13" ry="9" fill="#8C76E0" transform="rotate(-35 163 148)"/>
      <path d="M89 120 L96 130 L103 120 Z" fill="#F4A261"/>
      <ellipse cx="80" cy="185" rx="12" ry="6" fill="#F4A261"/><ellipse cx="112" cy="185" rx="12" ry="6" fill="#F4A261"/>
      <path d="M178 64 l3 7 7 3 -7 3 -3 7 -3 -7 -7 -3 7 -3z" fill="#FFD166"/>
      
    </svg>
  )
}
