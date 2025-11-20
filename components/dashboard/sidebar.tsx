"use client"

import Link from "next/link"
import { LayoutGrid, FileText, BarChart3, Clock, LogOut } from "lucide-react"

interface SidebarProps {
  activeTab: string
  setActiveTab: (tab: string) => void
}

export default function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  const menuItems = [
    { id: "analysis", label: "Tableau de bord", icon: LayoutGrid },
    { id: "cvs", label: "Mes CV", icon: FileText },
    { id: "analyses", label: "Mes analyses", icon: BarChart3 },
    { id: "history", label: "Historique", icon: Clock },
  ]

  return (
    <aside className="w-64 bg-card border-r border-border flex flex-col hidden md:flex">
      <div className="p-6 border-b border-border">
        <Link href="/" className="text-2xl font-bold text-primary">
          SmartHire
        </Link>
      </div>

      <nav className="flex-1 overflow-y-auto p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                activeTab === item.id ? "bg-primary/10 text-primary" : "text-foreground hover:bg-muted"
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </button>
          )
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-foreground hover:bg-muted transition-colors">
          <LogOut size={20} />
          <span className="font-medium">Déconnexion</span>
        </button>
      </div>
    </aside>
  )
}
