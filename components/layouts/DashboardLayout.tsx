"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { useAuth } from "@/contexts/AuthContext"
import {
  LayoutDashboard,
  FileText,
  BarChart3,
  Clock,
  TrendingUp,
  Bell,
  Briefcase,
  Menu,
  X,
  User,
  Settings,
  LogOut,
  ChevronDown
} from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout } = useAuth()

  const menuItems = [
    {
      section: "PRINCIPAL",
      items: [
        { id: "dashboard", label: "Tableau de bord", icon: LayoutDashboard, path: "/dashboard" },
        { id: "cvs", label: "Mes CV", icon: FileText, path: "/dashboard/cvs" },
        { id: "analyses", label: "Mes analyses", icon: BarChart3, path: "/dashboard/analyses" },
        { id: "historique", label: "Historique", icon: Clock, path: "/dashboard/historique" },
      ],
    },
    {
      section: "PAGES",
      items: [
        { id: "analytics", label: "Analytics", icon: TrendingUp, path: "/analytics" },
        { id: "alertes", label: "Mes Alertes", icon: Bell, path: "/dashboard/alertes", badge: "3" },
        { id: "candidatures", label: "Candidatures", icon: Briefcase, path: "/dashboard/candidatures" },
      ],
    },
  ]

  const handleLogout = () => {
    logout()
    router.push("/auth")
  }

  const getInitials = (prenom?: string, nom?: string) => {
    if (!prenom && !nom) return "U"
    const p = prenom?.charAt(0) || ""
    const n = nom?.charAt(0) || ""
    return (p + n).toUpperCase()
  }

  const getFullName = () => {
    if (!user) return "Utilisateur"
    return `${user.prenom || ""} ${user.nom || ""}`.trim() || "Utilisateur"
  }

  const getPhotoUrl = () => {
    if (!user?.photo_profil) return undefined
    // Si c'est une URL complète, la retourner telle quelle
    if (user.photo_profil.startsWith("http")) return user.photo_profil
    // Sinon, construire l'URL vers le backend
    return `http://localhost:8080${user.photo_profil}`
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-gray-200 z-50">
        <div className="flex items-center justify-between h-full px-4">
          {/* Left: Logo + Menu burger */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
            >
              {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
            <Link href="/dashboard" className="text-xl font-bold text-blue-600">
              SmartHire
            </Link>
          </div>

          {/* Right: Notifications + User */}
          <div className="flex items-center gap-4">
            {/* Notifications */}
            <button className="relative p-2 hover:bg-gray-100 rounded-lg">
              <Bell className="h-5 w-5 text-gray-600" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            {/* User Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={getPhotoUrl()} />
                    <AvatarFallback className="bg-blue-600 text-white">
                      {getInitials(user?.prenom, user?.nom)}
                    </AvatarFallback>
                  </Avatar>
                  <div className="hidden md:block text-left">
                    <p className="text-sm font-medium text-gray-900">
                      {getFullName()}
                    </p>
                    <p className="text-xs text-gray-500">{user?.email || ""}</p>
                  </div>
                  <ChevronDown className="h-4 w-4 text-gray-500" />
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>Mon compte</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => router.push("/dashboard/profil")}>
                  <User className="mr-2 h-4 w-4" />
                  Mon Profil
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => router.push("/dashboard/parametres")}>
                  <Settings className="mr-2 h-4 w-4" />
                  Paramètres
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="text-red-600">
                  <LogOut className="mr-2 h-4 w-4" />
                  Déconnexion
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </nav>

      {/* Sidebar */}
      <aside
        className={`fixed top-16 left-0 bottom-0 w-64 bg-white border-r border-gray-200 z-40 transition-transform duration-300 lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4 space-y-6">
            {menuItems.map((section) => (
              <div key={section.section}>
                <p className="text-xs font-semibold text-gray-400 mb-2">{section.section}</p>
                <div className="space-y-1">
                  {section.items.map((item) => {
                    const Icon = item.icon
                    const isActive = pathname === item.path
                    return (
                      <Link
                        key={item.id}
                        href={item.path}
                        onClick={() => setSidebarOpen(false)}
                        className={`flex items-center justify-between gap-3 px-3 py-2 rounded-lg transition-colors ${
                          isActive
                            ? "bg-blue-50 text-blue-600 border-l-4 border-blue-600"
                            : "text-gray-700 hover:bg-gray-100"
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <Icon className="h-5 w-5" />
                          <span className="font-medium">{item.label}</span>
                        </div>
                        {item.badge && (
                          <Badge variant="destructive" className="h-5 px-1.5">
                            {item.badge}
                          </Badge>
                        )}
                      </Link>
                    )
                  })}
                </div>
              </div>
            ))}
          </nav>

          {/* Sidebar Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center gap-3">
              <Avatar className="h-10 w-10">
                <AvatarImage src={getPhotoUrl()} />
                <AvatarFallback className="bg-blue-600 text-white">
                  {getInitials(user?.prenom, user?.nom)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {getFullName()}
                </p>
                <p className="text-xs text-gray-500 truncate">{user?.email || ""}</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Backdrop for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="pt-16 lg:pl-64">
        <div className="p-8">{children}</div>
      </main>
    </div>
  )
}


