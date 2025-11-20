"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Briefcase, Eye, Calendar, Building2, MapPin } from "lucide-react"
import { toast } from "sonner"

function CandidaturesPage() {
  const [selectedApplication, setSelectedApplication] = useState<any>(null)

  const applications = [
    {
      id: 1,
      poste: "Développeur Full Stack",
      entreprise: "TechVision Solutions",
      ville: "Casablanca",
      date: "15 Nov 2024",
      statut: "entretien",
      score: 85,
      timeline: [
        { date: "15 Nov", event: "Candidature envoyée", done: true },
        { date: "18 Nov", event: "Vue par le recruteur", done: true },
        { date: "22 Nov", event: "Entretien planifié", done: true },
        { date: "En attente", event: "Réponse finale", done: false },
      ],
    },
    {
      id: 2,
      poste: "Ingénieur DevOps",
      entreprise: "CloudTech Morocco",
      ville: "Rabat",
      date: "17 Nov 2024",
      statut: "envoyee",
      score: 75,
      timeline: [
        { date: "17 Nov", event: "Candidature envoyée", done: true },
        { date: "En attente", event: "Vue par le recruteur", done: false },
      ],
    },
    {
      id: 3,
      poste: "Tech Lead React",
      entreprise: "Digital Innovations",
      ville: "Casablanca",
      date: "12 Nov 2024",
      statut: "refusee",
      score: 80,
      timeline: [
        { date: "12 Nov", event: "Candidature envoyée", done: true },
        { date: "14 Nov", event: "Vue par le recruteur", done: true },
        { date: "16 Nov", event: "Refusée", done: true },
      ],
    },
  ]

  const getStatusBadge = (statut: string) => {
    const badges = {
      brouillon: <Badge variant="outline" className="bg-gray-100">Brouillon</Badge>,
      envoyee: <Badge className="bg-blue-100 text-blue-700">Envoyée</Badge>,
      vue: <Badge className="bg-purple-100 text-purple-700">Vue</Badge>,
      entretien: <Badge className="bg-green-100 text-green-700">Entretien</Badge>,
      refusee: <Badge className="bg-red-100 text-red-700">Refusée</Badge>,
      acceptee: <Badge className="bg-green-100 text-green-800">Acceptée</Badge>,
    }
    return badges[statut as keyof typeof badges] || badges.brouillon
  }

  const stats = {
    total: applications.length,
    envoyees: applications.filter((a) => a.statut === "envoyee").length,
    entretiens: applications.filter((a) => a.statut === "entretien").length,
    refusees: applications.filter((a) => a.statut === "refusee").length,
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-6xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Suivi des Candidatures</h1>
            <p className="text-gray-600 mt-2">Gérez et suivez toutes vos candidatures en un seul endroit</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card>
              <CardContent className="p-6">
                <p className="text-sm text-gray-600 mb-1">Total</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <p className="text-sm text-gray-600 mb-1">Envoyées</p>
                <p className="text-3xl font-bold text-blue-600">{stats.envoyees}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <p className="text-sm text-gray-600 mb-1">Entretiens</p>
                <p className="text-3xl font-bold text-green-600">{stats.entretiens}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-6">
                <p className="text-sm text-gray-600 mb-1">Refusées</p>
                <p className="text-3xl font-bold text-red-600">{stats.refusees}</p>
              </CardContent>
            </Card>
          </div>

          {/* Tabs */}
          <Tabs defaultValue="tous" className="space-y-6">
            <TabsList>
              <TabsTrigger value="tous">Toutes ({stats.total})</TabsTrigger>
              <TabsTrigger value="envoyees">Envoyées ({stats.envoyees})</TabsTrigger>
              <TabsTrigger value="entretien">Entretiens ({stats.entretiens})</TabsTrigger>
              <TabsTrigger value="refusees">Refusées ({stats.refusees})</TabsTrigger>
            </TabsList>

            <TabsContent value="tous" className="space-y-4">
              {applications.map((app) => (
                <Card key={app.id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-gray-900 text-lg">{app.poste}</h3>
                          {getStatusBadge(app.statut)}
                          <Badge className="bg-green-100 text-green-700">{app.score}% match</Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-600 mb-2">
                          <div className="flex items-center gap-1">
                            <Building2 className="h-4 w-4" />
                            {app.entreprise}
                          </div>
                          <div className="flex items-center gap-1">
                            <MapPin className="h-4 w-4" />
                            {app.ville}
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            {app.date}
                          </div>
                        </div>
                      </div>
                      <Button variant="outline" onClick={() => setSelectedApplication(app)}>
                        <Eye className="mr-2 h-4 w-4" />
                        Voir détails
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>

            <TabsContent value="envoyees">
              <p className="text-gray-500">Filtrage des candidatures envoyées...</p>
            </TabsContent>

            <TabsContent value="entretien">
              <p className="text-gray-500">Filtrage des entretiens...</p>
            </TabsContent>

            <TabsContent value="refusees">
              <p className="text-gray-500">Filtrage des candidatures refusées...</p>
            </TabsContent>
          </Tabs>

          {/* Modal détails */}
          <Dialog open={!!selectedApplication} onOpenChange={() => setSelectedApplication(null)}>
            <DialogContent className="sm:max-w-[600px]">
              {selectedApplication && (
                <>
                  <DialogHeader>
                    <DialogTitle>{selectedApplication.poste}</DialogTitle>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div>
                      <p className="text-sm font-semibold text-gray-700 mb-1">Entreprise</p>
                      <p className="text-gray-900">{selectedApplication.entreprise}</p>
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-gray-700 mb-1">Ville</p>
                      <p className="text-gray-900">{selectedApplication.ville}</p>
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-gray-700 mb-2">Timeline</p>
                      <div className="space-y-3">
                        {selectedApplication.timeline.map((step: any, idx: number) => (
                          <div key={idx} className="flex items-start gap-3">
                            <div
                              className={`w-3 h-3 rounded-full mt-1 ${
                                step.done ? "bg-green-500" : "bg-gray-300"
                              }`}
                            />
                            <div className="flex-1">
                              <p className="text-sm font-medium text-gray-900">{step.event}</p>
                              <p className="text-xs text-gray-500">{step.date}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </>
              )}
            </DialogContent>
          </Dialog>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}

export default CandidaturesPage


