"use client"

import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Clock, FileText, BarChart3, Mail } from "lucide-react"
import { useRouter } from "next/navigation"

function HistoriquePage() {
  const router = useRouter()

  const activities = [
    {
      id: 1,
      type: "analysis",
      title: "Analyse de CV pour Développeur Full Stack",
      description: "TechVision Solutions",
      date: "18 Nov 2024, 14:30",
      score: 85,
    },
    {
      id: 2,
      type: "cv_upload",
      title: "Upload de CV",
      description: "CV_Ranya_SERRAJ.pdf",
      date: "18 Nov 2024, 14:25",
    },
    {
      id: 3,
      type: "cover_letter",
      title: "Génération de lettre de motivation",
      description: "Ingénieur DevOps - CloudTech Morocco",
      date: "17 Nov 2024, 16:20",
    },
    {
      id: 4,
      type: "analysis",
      title: "Analyse de CV pour Ingénieur DevOps",
      description: "CloudTech Morocco",
      date: "17 Nov 2024, 16:15",
      score: 75,
    },
  ]

  const getIcon = (type: string) => {
    switch (type) {
      case "analysis":
        return <BarChart3 className="h-5 w-5 text-blue-600" />
      case "cv_upload":
        return <FileText className="h-5 w-5 text-green-600" />
      case "cover_letter":
        return <Mail className="h-5 w-5 text-purple-600" />
      default:
        return <Clock className="h-5 w-5 text-gray-600" />
    }
  }

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "analysis":
        return "Analyse"
      case "cv_upload":
        return "Upload CV"
      case "cover_letter":
        return "Lettre"
      default:
        return "Activité"
    }
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Historique</h1>
            <p className="text-gray-600 mt-2">Suivez toutes vos activités sur SmartHire</p>
          </div>

          {activities.length === 0 ? (
            <Card className="p-12">
              <div className="flex flex-col items-center justify-center text-center">
                <Clock className="h-16 w-16 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Aucune activité</h3>
                <p className="text-gray-500 mb-4">Votre historique d'activités apparaîtra ici</p>
                <Button onClick={() => router.push("/dashboard")}>Commencer</Button>
              </div>
            </Card>
          ) : (
            <div className="space-y-4">
              {activities.map((activity, index) => (
                <Card key={activity.id}>
                  <CardContent className="p-6">
                    <div className="flex items-start gap-4">
                      <div className="p-3 bg-gray-100 rounded-lg">{getIcon(activity.type)}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-1">
                          <h3 className="font-semibold text-gray-900">{activity.title}</h3>
                          <Badge variant="outline">{getTypeLabel(activity.type)}</Badge>
                          {activity.score && (
                            <Badge
                              className={
                                activity.score >= 80
                                  ? "bg-green-100 text-green-700"
                                  : activity.score >= 60
                                  ? "bg-orange-100 text-orange-700"
                                  : "bg-red-100 text-red-700"
                              }
                            >
                              {activity.score}%
                            </Badge>
                          )}
                        </div>
                        <p className="text-gray-600 mb-2">{activity.description}</p>
                        <p className="text-sm text-gray-500">{activity.date}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}

export default HistoriquePage


