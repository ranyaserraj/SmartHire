"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Layout, Bot, Users, FileText } from "lucide-react"

const softSkills = [
  "Leadership",
  "Communication",
  "Travail d'équipe",
  "Autonomie",
  "Résolution de problèmes",
  "Créativité",
  "Gestion du temps",
  "Adaptabilité",
]

export default function CVAdvancedAnalysis() {
  const cvQualityScore = 85
  const structureScore = 85
  const atsScore = 72
  const softSkillsCount = 8
  const clarityScore = 90

  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle className="text-2xl">Analyse Avancée du CV</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Score global */}
          <div className="flex flex-col items-center justify-center p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">Score Qualité CV</h3>
            <div className="relative w-32 h-32">
              <svg className="w-full h-full" viewBox="0 0 100 100">
                <circle
                  className="text-gray-200 stroke-current"
                  strokeWidth="10"
                  cx="50"
                  cy="50"
                  r="40"
                  fill="transparent"
                />
                <circle
                  className="text-blue-600 stroke-current"
                  strokeWidth="10"
                  strokeLinecap="round"
                  cx="50"
                  cy="50"
                  r="40"
                  fill="transparent"
                  strokeDasharray={`${(cvQualityScore / 100) * 251.2} 251.2`}
                  transform="rotate(-90 50 50)"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl font-bold text-gray-900">{cvQualityScore}</span>
              </div>
            </div>
            <p className="text-sm text-gray-600 mt-4">Excellente qualité</p>
          </div>

          {/* Sous-scores */}
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Layout className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Structure & Mise en forme</p>
                  <p className="text-sm text-gray-600">Excellente organisation</p>
                </div>
              </div>
              <span className="text-2xl font-bold text-blue-600">{structureScore}</span>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Bot className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Compatibilité ATS</p>
                  <p className="text-sm text-gray-600">Bonne compatibilité</p>
                </div>
              </div>
              <span className="text-2xl font-bold text-green-600">{atsScore}</span>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Users className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Soft Skills détectées</p>
                  <p className="text-sm text-gray-600">{softSkillsCount} compétences</p>
                </div>
              </div>
              <span className="text-2xl font-bold text-purple-600">{softSkillsCount}</span>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <FileText className="h-5 w-5 text-orange-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Clarté du contenu</p>
                  <p className="text-sm text-gray-600">Très clair</p>
                </div>
              </div>
              <span className="text-2xl font-bold text-orange-600">{clarityScore}</span>
            </div>
          </div>
        </div>

        {/* Soft Skills */}
        <div className="mt-6">
          <h4 className="font-semibold text-gray-900 mb-3">Soft Skills détectées</h4>
          <div className="flex flex-wrap gap-2">
            {softSkills.map((skill, index) => (
              <Badge key={index} className="bg-blue-100 text-blue-700 border-blue-200">
                {skill}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}


