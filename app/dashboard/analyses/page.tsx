"use client"

import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BarChart3, Eye, Trash2 } from "lucide-react"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

function AnalysesPage() {
  const router = useRouter()

  const analyses = [
    {
      id: 1,
      jobTitle: "Développeur Full Stack",
      company: "TechVision Solutions",
      date: "18 Nov 2024",
      overallScore: 85,
      matchingSkills: ["React", "Node.js", "PostgreSQL"],
      status: "completed",
    },
    {
      id: 2,
      jobTitle: "Ingénieur DevOps",
      company: "CloudTech Morocco",
      date: "17 Nov 2024",
      overallScore: 75,
      matchingSkills: ["AWS", "Docker"],
      status: "completed",
    },
  ]

  const handleViewResults = (id: number) => {
    router.push("/results")
  }

  const handleDelete = (id: number) => {
    toast.success("Analyse supprimée")
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Mes Analyses</h1>
            <p className="text-gray-600 mt-2">Consultez l'historique de toutes vos analyses CV/Offre</p>
          </div>

          {analyses.length === 0 ? (
            <Card className="p-12">
              <div className="flex flex-col items-center justify-center text-center">
                <BarChart3 className="h-16 w-16 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Aucune analyse effectuée</h3>
                <p className="text-gray-500 mb-4 max-w-md">
                  Lancez votre première analyse pour obtenir un matching détaillé entre votre CV et une offre d'emploi
                </p>
                <Button onClick={() => router.push("/dashboard")}>Commencer une analyse</Button>
              </div>
            </Card>
          ) : (
            <div className="grid grid-cols-1 gap-6">
              {analyses.map((analysis) => (
                <Card key={analysis.id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-gray-900 text-lg">{analysis.jobTitle}</h3>
                          <Badge
                            className={
                              analysis.overallScore >= 80
                                ? "bg-green-100 text-green-700"
                                : analysis.overallScore >= 60
                                ? "bg-orange-100 text-orange-700"
                                : "bg-red-100 text-red-700"
                            }
                          >
                            {analysis.overallScore}% de matching
                          </Badge>
                        </div>
                        <p className="text-gray-600 mb-3">{analysis.company}</p>
                        <div className="flex flex-wrap gap-2 mb-2">
                          {analysis.matchingSkills.map((skill, idx) => (
                            <Badge key={idx} variant="outline" className="bg-blue-50 text-blue-700">
                              {skill}
                            </Badge>
                          ))}
                        </div>
                        <p className="text-sm text-gray-500">Analysé le {analysis.date}</p>
                      </div>

                      <div className="flex gap-2">
                        <Button variant="outline" onClick={() => handleViewResults(analysis.id)}>
                          <Eye className="mr-2 h-4 w-4" />
                          Voir les résultats
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => handleDelete(analysis.id)}>
                          <Trash2 className="h-4 w-4 text-red-500" />
                        </Button>
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

export default AnalysesPage


