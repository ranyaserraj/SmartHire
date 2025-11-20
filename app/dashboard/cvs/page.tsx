"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Upload, Trash2, Eye } from "lucide-react"
import { toast } from "sonner"

function CVsPage() {
  const [cvs, setCvs] = useState([
    {
      id: 1,
      filename: "CV_Ranya_SERRAJ.pdf",
      uploadDate: "15 Nov 2024",
      size: "245 KB",
      structureScore: 85,
      atsScore: 78,
      completenessScore: 90,
    },
  ])

  const handleUpload = () => {
    toast.info("Upload de CV", {
      description: "Fonctionnalité d'upload en développement",
    })
  }

  const handleAnalyze = (id: number) => {
    toast.success("Analyse démarrée pour le CV #" + id)
  }

  const handleDelete = (id: number) => {
    setCvs(cvs.filter((cv) => cv.id !== id))
    toast.success("CV supprimé avec succès")
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Mes CV</h1>
              <p className="text-gray-600 mt-2">Gérez tous vos CV en un seul endroit</p>
            </div>
            <Button onClick={handleUpload}>
              <Upload className="mr-2 h-4 w-4" />
              Upload nouveau CV
            </Button>
          </div>

          {cvs.length === 0 ? (
            <Card className="p-12">
              <div className="flex flex-col items-center justify-center text-center">
                <FileText className="h-16 w-16 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Aucun CV uploadé</h3>
                <p className="text-gray-500 mb-4 max-w-md">
                  Commencez par uploader votre CV pour recevoir des recommandations d'offres personnalisées
                </p>
                <Button onClick={handleUpload}>
                  <Upload className="mr-2 h-4 w-4" />
                  Uploader mon premier CV
                </Button>
              </div>
            </Card>
          ) : (
            <div className="grid grid-cols-1 gap-6">
              {cvs.map((cv) => (
                <Card key={cv.id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="p-3 bg-blue-100 rounded-lg">
                          <FileText className="h-6 w-6 text-blue-600" />
                        </div>
                        <div>
                          <h3 className="font-semibold text-gray-900">{cv.filename}</h3>
                          <p className="text-sm text-gray-500">
                            Uploadé le {cv.uploadDate} • {cv.size}
                          </p>
                          <div className="flex gap-4 mt-2">
                            <span className="text-xs text-gray-600">
                              Structure: <span className="font-semibold text-blue-600">{cv.structureScore}/100</span>
                            </span>
                            <span className="text-xs text-gray-600">
                              ATS: <span className="font-semibold text-green-600">{cv.atsScore}/100</span>
                            </span>
                            <span className="text-xs text-gray-600">
                              Complétude: <span className="font-semibold text-purple-600">{cv.completenessScore}/100</span>
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" onClick={() => handleAnalyze(cv.id)}>
                          <Eye className="mr-2 h-4 w-4" />
                          Analyser
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => toast.info("Téléchargement...")}>
                          Télécharger
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => handleDelete(cv.id)}>
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

export default CVsPage


