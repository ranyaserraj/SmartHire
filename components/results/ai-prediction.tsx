"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles } from "lucide-react"

const factors = [
  { name: "Compétences techniques", score: 85, color: "bg-green-500" },
  { name: "Expérience requise", score: 60, color: "bg-yellow-500" },
  { name: "Localisation", score: 95, color: "bg-green-500" },
  { name: "Formation", score: 75, color: "bg-blue-500" },
]

export default function AIPrediction() {
  const acceptanceProbability = 78

  return (
    <Card className="mb-8 bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200">
      <CardHeader>
        <div className="flex items-center gap-3">
          <div className="p-3 bg-purple-500 rounded-lg">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <div>
            <CardTitle className="text-2xl">Prédiction IA</CardTitle>
            <p className="text-sm text-gray-600 mt-1">Analyse prédictive basée sur l'intelligence artificielle</p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-center mb-6">
          <div className="inline-block p-8 bg-white rounded-2xl shadow-lg">
            <p className="text-6xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              {acceptanceProbability}%
            </p>
            <p className="text-lg font-semibold text-gray-700 mt-2">Probabilité d'être sélectionné</p>
          </div>
          <p className="text-sm text-gray-600 mt-4">
            Basé sur l'analyse de <span className="font-semibold">1,247 candidatures similaires</span>
          </p>
        </div>

        <div className="space-y-4">
          <h4 className="font-semibold text-gray-900 mb-3">Facteurs d'influence</h4>
          {factors.map((factor, index) => (
            <div key={index} className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{factor.name}</span>
                <span className="text-sm font-bold text-gray-900">{factor.score}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className={`${factor.color} h-3 rounded-full transition-all duration-500`}
                  style={{ width: `${factor.score}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-white rounded-lg border border-purple-200">
          <p className="text-sm text-gray-700">
            💡 <span className="font-semibold">Conseil IA:</span> Vos compétences techniques et votre localisation sont
            des atouts majeurs. Focus sur l'expérience pour maximiser vos chances.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}


