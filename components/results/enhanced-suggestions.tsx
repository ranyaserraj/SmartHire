"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { AlertCircle, AlertTriangle, Lightbulb, Eye } from "lucide-react"

const suggestions = {
  critical: [
    {
      title: "Ajouter des verbes d'action",
      description: "Remplacez les phrases passives par des verbes d'action forts pour dynamiser votre CV",
      example: {
        before: "Responsable de la gestion d'une équipe",
        after: "Dirigé et coordonné une équipe de 5 développeurs sur 3 projets majeurs",
      },
    },
  ],
  medium: [
    {
      title: "Quantifier vos réalisations",
      description: "Ajoutez des chiffres concrets pour mesurer l'impact de votre travail",
      example: {
        before: "Géré une équipe",
        after: "Géré une équipe de 5 personnes pendant 2 ans, livrant 12 projets avec 95% de satisfaction client",
      },
    },
    {
      title: "Optimiser pour ATS",
      description: "Utilisez les termes complets plutôt que des abréviations pour passer les systèmes ATS",
      example: {
        before: "JS, TS, API",
        after: "JavaScript, TypeScript, API RESTful",
      },
    },
  ],
  bonus: [
    {
      title: "Ajouter des certifications",
      description: "Mentionnez vos certifications professionnelles pour renforcer votre crédibilité",
      example: {
        before: "Compétences en AWS",
        after: "AWS Certified Solutions Architect (2023) - Conception d'architectures cloud scalables",
      },
    },
  ],
}

export default function EnhancedSuggestions() {
  const [selectedExample, setSelectedExample] = useState<any>(null)

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Suggestions d'Amélioration</h2>

      {/* Critiques */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <AlertCircle className="h-5 w-5 text-red-600" />
          <h3 className="text-lg font-semibold text-red-900">🔴 Critiques (haute priorité)</h3>
        </div>
        <div className="space-y-3">
          {suggestions.critical.map((suggestion, index) => (
            <Card key={index} className="bg-red-50 border-red-200">
              <CardContent className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-semibold text-red-900 mb-1">{suggestion.title}</h4>
                    <p className="text-sm text-red-700">{suggestion.description}</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedExample(suggestion)}
                    className="ml-4"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    Voir exemple
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* À améliorer */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <AlertTriangle className="h-5 w-5 text-orange-600" />
          <h3 className="text-lg font-semibold text-orange-900">🟠 À améliorer (moyenne priorité)</h3>
        </div>
        <div className="space-y-3">
          {suggestions.medium.map((suggestion, index) => (
            <Card key={index} className="bg-orange-50 border-orange-200">
              <CardContent className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-900 mb-1">{suggestion.title}</h4>
                    <p className="text-sm text-orange-700">{suggestion.description}</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedExample(suggestion)}
                    className="ml-4"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    Voir exemple
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Bonus */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb className="h-5 w-5 text-green-600" />
          <h3 className="text-lg font-semibold text-green-900">🟢 Suggestions bonus (basse priorité)</h3>
        </div>
        <div className="space-y-3">
          {suggestions.bonus.map((suggestion, index) => (
            <Card key={index} className="bg-green-50 border-green-200">
              <CardContent className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-semibold text-green-900 mb-1">{suggestion.title}</h4>
                    <p className="text-sm text-green-700">{suggestion.description}</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedExample(suggestion)}
                    className="ml-4"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    Voir exemple
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Modal Exemple */}
      <Dialog open={!!selectedExample} onOpenChange={() => setSelectedExample(null)}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>{selectedExample?.title}</DialogTitle>
            <DialogDescription>{selectedExample?.description}</DialogDescription>
          </DialogHeader>
          {selectedExample && (
            <div className="space-y-4 py-4">
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm font-semibold text-red-900 mb-2">❌ Avant :</p>
                <p className="text-gray-700">{selectedExample.example.before}</p>
              </div>
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm font-semibold text-green-900 mb-2">✅ Après :</p>
                <p className="text-gray-700">{selectedExample.example.after}</p>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}


