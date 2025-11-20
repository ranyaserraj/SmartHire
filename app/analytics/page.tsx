"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { LineChart, Line, BarChart, Bar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { TrendingUp, TrendingDown, Users, FileText, Award, Download, RefreshCw } from "lucide-react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { useAuth } from "@/contexts/AuthContext"
import { toast } from "sonner"

// Données de simulation
const scoreEvolutionData = [
  { date: "15 Nov", score: 72 },
  { date: "16 Nov", score: 75 },
  { date: "17 Nov", score: 78 },
  { date: "18 Nov", score: 82 },
  { date: "19 Nov", score: 85 },
]

const skillsComparisonData = [
  { skill: "JavaScript", vous: 90, marche: 85 },
  { skill: "Python", vous: 75, marche: 80 },
  { skill: "React", vous: 85, marche: 75 },
  { skill: "Node.js", vous: 80, marche: 70 },
  { skill: "SQL", vous: 70, marche: 82 },
]

const radarData = [
  { subject: "Compétences techniques", vous: 85, marche: 75 },
  { subject: "Expérience", vous: 70, marche: 80 },
  { subject: "Formation", vous: 90, marche: 85 },
  { subject: "Soft skills", vous: 80, marche: 75 },
  { subject: "Langues", vous: 75, marche: 70 },
]

const trendingSkillsData = [
  { skill: "React", demand: 245, trend: 15, hasSkill: true },
  { skill: "Python", demand: 223, trend: 12, hasSkill: true },
  { skill: "Docker", demand: 198, trend: 8, hasSkill: false },
  { skill: "Kubernetes", demand: 187, trend: 18, hasSkill: false },
  { skill: "TypeScript", demand: 165, trend: 10, hasSkill: true },
]

function AnalyticsPage() {
  const [period, setPeriod] = useState("30")
  const { user } = useAuth()

  const handleExport = () => {
    toast.success("Export démarré", {
      description: "Vos données sont en cours d'export..."
    })
  }

  const handleDownload = () => {
    toast.success("Téléchargement démarré", {
      description: "Le rapport est en cours de génération..."
    })
  }

  const handleRefresh = () => {
    toast.success("Actualisation en cours", {
      description: "Les données sont en cours de mise à jour..."
    })
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Analytics Avancé</h1>
                <p className="text-gray-600 mt-2">Analysez votre progression et comparez-vous au marché</p>
              </div>
              <div className="flex items-center gap-4">
                <Select value={period} onValueChange={setPeriod}>
                  <SelectTrigger className="w-40">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="7">7 derniers jours</SelectItem>
                    <SelectItem value="30">30 derniers jours</SelectItem>
                    <SelectItem value="90">3 mois</SelectItem>
                    <SelectItem value="365">1 an</SelectItem>
                    <SelectItem value="all">Tout</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline" onClick={handleExport}>
                  <Download className="mr-2 h-4 w-4" />
                  Exporter
                </Button>
              </div>
            </div>

            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-gray-600">Score Moyen</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-blue-600">82%</div>
                  <div className="flex items-center text-sm text-green-600 mt-2">
                    <TrendingUp className="h-4 w-4 mr-1" />
                    +5% ce mois
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-gray-600">Matchings Réussis</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-600">24</div>
                  <div className="flex items-center text-sm text-green-600 mt-2">
                    <TrendingUp className="h-4 w-4 mr-1" />
                    +12 cette semaine
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-gray-600">Offres Analysées</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-purple-600">47</div>
                  <div className="flex items-center text-sm text-gray-500 mt-2">
                    <FileText className="h-4 w-4 mr-1" />
                    Total
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-gray-600">Classement Marché</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-orange-600">Top 15%</div>
                  <div className="flex items-center text-sm text-green-600 mt-2">
                    <Award className="h-4 w-4 mr-1" />
                    Excellent
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Évolution du Score */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Évolution de votre Score Moyen</CardTitle>
                <CardDescription>Progression de vos scores d'analyse au fil du temps</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={scoreEvolutionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="score" stroke="#3B82F6" strokeWidth={2} name="Score" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              {/* Radar Chart */}
              <Card>
                <CardHeader>
                  <CardTitle>Votre Profil vs Marché</CardTitle>
                  <CardDescription>Comparaison de votre profil avec la moyenne du marché</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="subject" />
                      <PolarRadiusAxis domain={[0, 100]} />
                      <Radar name="Vous" dataKey="vous" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.6} />
                      <Radar name="Marché" dataKey="marche" stroke="#9CA3AF" fill="#9CA3AF" fillOpacity={0.3} />
                      <Legend />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Bar Chart */}
              <Card>
                <CardHeader>
                  <CardTitle>Compétences vs Marché</CardTitle>
                  <CardDescription>Comparaison de vos compétences principales</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={skillsComparisonData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="skill" />
                      <YAxis domain={[0, 100]} />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="vous" fill="#3B82F6" name="Vous" />
                      <Bar dataKey="marche" fill="#9CA3AF" name="Marché" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Tendances du Marché */}
            <Card className="mb-8">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Tendances du Marché</CardTitle>
                    <CardDescription>Compétences les plus demandées et leur évolution</CardDescription>
                  </div>
                  <Button variant="outline" onClick={handleDownload}>
                    <Download className="mr-2 h-4 w-4" />
                    Télécharger Rapport
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {trendingSkillsData.map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-4 flex-1">
                        <div className="text-lg font-semibold text-gray-400">#{index + 1}</div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <h4 className="font-semibold text-gray-900">{item.skill}</h4>
                            {item.hasSkill && (
                              <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                                Vous avez
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-4 mt-2">
                            <span className="text-sm text-gray-600">{item.demand} offres</span>
                            <div className="flex items-center text-sm text-green-600">
                              <TrendingUp className="h-4 w-4 mr-1" />
                              +{item.trend}%
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="w-48">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${item.hasSkill ? "bg-green-500" : "bg-red-500"}`}
                            style={{ width: `${(item.demand / 250) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recommandations */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Recommandations Personnalisées</CardTitle>
                    <CardDescription>Actions pour améliorer votre profil</CardDescription>
                  </div>
                  <Button variant="outline" onClick={handleRefresh}>
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Actualiser les données
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-semibold text-blue-900 mb-2">🎯 Priorité Haute</h4>
                    <p className="text-blue-800">Ajoutez Docker et Kubernetes à vos compétences - ces technologies sont en forte demande (+18% cette année)</p>
                  </div>
                  <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2">✅ Bon Positionnement</h4>
                    <p className="text-green-800">Vos compétences en React et TypeScript sont très demandées. Continuez à les développer !</p>
                  </div>
                  <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                    <h4 className="font-semibold text-orange-900 mb-2">📈 Opportunité</h4>
                    <p className="text-orange-800">Envisagez d'ajouter des certifications AWS ou Azure pour augmenter votre employabilité de 25%</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Boutons d'action supplémentaires */}
            <div className="mt-8 flex gap-4">
              <Button size="lg" onClick={handleDownload}>
                <Download className="mr-2 h-5 w-5" />
                Télécharger Rapport Complet
              </Button>
              <Button size="lg" variant="outline" onClick={handleRefresh}>
                <RefreshCw className="mr-2 h-5 w-5" />
                Réinitialiser
              </Button>
            </div>
          </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}

export default AnalyticsPage

