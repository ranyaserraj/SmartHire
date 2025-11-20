"use client"

interface DashboardHeaderProps {
  stats: Array<{ label: string; value: string }>
}

export default function DashboardHeader({ stats }: DashboardHeaderProps) {
  return (
    <div className="bg-card border-b border-border sticky top-0 z-40">
      <div className="p-6 max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row gap-4 justify-between">
          {stats.map((stat) => (
            <div key={stat.label} className="flex flex-col">
              <span className="text-sm text-muted-foreground font-medium">{stat.label}</span>
              <span className="text-3xl font-bold text-foreground">{stat.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
