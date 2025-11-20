"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Download, ArrowLeft, CheckCircle, XCircle, FileText } from "lucide-react"
import ScoreGauge from "@/components/results/score-gauge"
import SkillsRadar from "@/components/results/skills-radar"
import CVAdvancedAnalysis from "@/components/results/cv-advanced-analysis"
import AIPrediction from "@/components/results/ai-prediction"
import EnhancedSuggestions from "@/components/results/enhanced-suggestions"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { toast } from "sonner"

export default function ResultsPage() {
  const matchingScore = 85

  const matchingSkills = ["JavaScript", "React", "TypeScript", "Next.js", "Node.js", "CSS"]

  const missingSkills = ["AWS", "Docker", "DevOps", "Kubernetes"]

  const improvements = [
    "Ajouter de l'expérience en architecture cloud (AWS/GCP)",
    "Approfondir vos compétences en DevOps et containerization",
    "Développer vos connaissances en base de données avancées",
    "Renforcer vos projets open source pour démontrer votre expertise",
  ]

  const handleDownloadPDF = () => {
    toast.info("Téléchargement du PDF en cours...")
  }

  const handleGenerateLetter = () => {
    window.location.href = "/motivation-letter"
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <Link href="/dashboard" className="flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-2">
                <ArrowLeft className="h-4 w-4" />
                Retour au tableau de bord
              </Link>
              <h1 className="text-3xl font-bold text-gray-900">Résultats de l'analyse</h1>
            </div>
            <Button onClick={handleDownloadPDF} className="gap-2">
              <Download className="h-4 w-4" />
              Télécharger PDF
            </Button>
          </div>

          {/* Analyse Avancée du CV */}
          <CVAdvancedAnalysis />

          {/* Score Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <Card className="p-8 border border-gray-200 flex flex-col items-center justify-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Score de matching</h2>
              <ScoreGauge score={matchingScore} />
              <p className="mt-6 text-center text-gray-600">
                Votre profil correspond à <strong>{matchingScore}%</strong> à cette offre d'emploi
              </p>
            </Card>

            <Card className="p-8 border border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Vue d'ensemble</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Compétences correspondantes</p>
                  <p className="text-2xl font-bold text-green-600">{matchingSkills.length}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Compétences manquantes</p>
                  <p className="text-2xl font-bold text-red-600">{missingSkills.length}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Niveau d'adéquation</p>
                  <p className="text-2xl font-bold text-blue-600">Très bon</p>
                </div>
              </div>
            </Card>
          </div>

          {/* Prédiction IA */}
          <AIPrediction />

          {/* Skills Comparison */}
          <Card className="p-8 border border-gray-200 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Comparaison des compétences</h2>
            <SkillsRadar skills={matchingSkills} />
          </Card>

          {/* Matching and Missing Skills */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <Card className="p-8 border border-gray-200">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <CheckCircle className="w-6 h-6 text-green-600" />
                Compétences correspondantes
              </h3>
              <div className="flex flex-wrap gap-2">
                {matchingSkills.map((skill) => (
                  <div
                    key={skill}
                    className="px-4 py-2 bg-green-100 border border-green-200 rounded-full text-sm font-medium text-green-700"
                  >
                    {skill}
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-8 border border-gray-200">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <XCircle className="w-6 h-6 text-red-600" />
                Compétences manquantes
              </h3>
              <div className="flex flex-wrap gap-2">
                {missingSkills.map((skill) => (
                  <div
                    key={skill}
                    className="px-4 py-2 bg-red-100 border border-red-200 rounded-full text-sm font-medium text-red-700"
                  >
                    {skill}
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Enhanced Suggestions */}
          <EnhancedSuggestions />

          {/* Action Buttons */}
          <div className="flex justify-center gap-4 mt-12">
            <Button onClick={handleGenerateLetter} size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600">
              <FileText className="mr-2 h-5 w-5" />
              Générer lettre de motivation
            </Button>
            <Link href="/dashboard">
              <Button variant="outline" size="lg">
                Nouvelle analyse
              </Button>
            </Link>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}
