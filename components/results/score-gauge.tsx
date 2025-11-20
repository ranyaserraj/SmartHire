"use client"

import { useEffect, useState } from "react"

interface ScoreGaugeProps {
  score: number
}

export default function ScoreGauge({ score }: ScoreGaugeProps) {
  const [displayScore, setDisplayScore] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setDisplayScore((prev) => {
        if (prev < score) {
          return Math.min(prev + 2, score)
        }
        return prev
      })
    }, 20)
    return () => clearInterval(interval)
  }, [score])

  const circumference = 2 * Math.PI * 45
  const offset = circumference - (displayScore / 100) * circumference

  const getColor = () => {
    if (displayScore >= 80) return "#10b981"
    if (displayScore >= 60) return "#f59e0b"
    return "#ef4444"
  }

  return (
    <div className="relative w-48 h-48">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
        {/* Background circle */}
        <circle cx="60" cy="60" r="45" fill="none" stroke="currentColor" strokeWidth="8" className="text-muted" />
        {/* Progress circle */}
        <circle
          cx="60"
          cy="60"
          r="45"
          fill="none"
          stroke={getColor()}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-500"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <div className="text-4xl font-bold text-foreground">{displayScore}%</div>
        <div className="text-xs text-muted-foreground">Match</div>
      </div>
    </div>
  )
}
