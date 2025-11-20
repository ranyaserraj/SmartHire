"use client"

export default function SkillsRadar({ skills }: { skills: string[] }) {
  const chartSkills = [
    { name: "Frontend", value: 90 },
    { name: "Backend", value: 85 },
    { name: "DevOps", value: 40 },
    { name: "Database", value: 75 },
    { name: "Architecture", value: 70 },
    { name: "Cloud", value: 50 },
  ]

  const maxValue = 100
  const numSkills = chartSkills.length
  const angle = (Math.PI * 2) / numSkills
  const radius = 80

  const getCoordinates = (index: number, value: number) => {
    const a = angle * index - Math.PI / 2
    const x = 120 + ((radius * value) / maxValue) * Math.cos(a)
    const y = 120 + ((radius * value) / maxValue) * Math.sin(a)
    return { x, y }
  }

  const points = chartSkills
    .map((skill, i) => getCoordinates(i, skill.value))
    .map((p) => `${p.x},${p.y}`)
    .join(" ")

  return (
    <div className="flex justify-center">
      <svg width="240" height="240" viewBox="0 0 240 240" className="mx-auto">
        {/* Grid circles */}
        {[20, 40, 60, 80, 100].map((r) => (
          <circle
            key={r}
            cx="120"
            cy="120"
            r={(r / maxValue) * radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="1"
            className="text-border"
          />
        ))}

        {/* Axes */}
        {chartSkills.map((_, i) => {
          const end = getCoordinates(i, maxValue)
          return (
            <line
              key={`axis-${i}`}
              x1="120"
              y1="120"
              x2={end.x}
              y2={end.y}
              stroke="currentColor"
              strokeWidth="1"
              className="text-border"
            />
          )
        })}

        {/* Data polygon */}
        <polygon
          points={points}
          fill="rgb(59, 130, 246)"
          fillOpacity="0.2"
          stroke="rgb(59, 130, 246)"
          strokeWidth="2"
        />

        {/* Labels */}
        {chartSkills.map((skill, i) => {
          const labelPos = getCoordinates(i, maxValue + 20)
          return (
            <text
              key={`label-${i}`}
              x={labelPos.x}
              y={labelPos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="text-xs font-medium fill-foreground"
            >
              {skill.name}
            </text>
          )
        })}
      </svg>
    </div>
  )
}
