"use client"

import React, { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { X, Plus, CheckCircle2 } from "lucide-react"
import { toast } from "sonner"

interface CVExtractedData {
  nom_complet: string | null
  email: string | null
  telephone: string | null
  ville: string | null
  competences: string[]
  experience: Array<{ periode: string; description: string }>
  formation: Array<{ diplome: string; description: string }>
  langues: string[]
  contenu_texte: string
}

interface CVVerificationFormProps {
  cvId: number
  extractedData: CVExtractedData
  onSubmit: (data: any) => Promise<void>
  onCancel: () => void
}

export default function CVVerificationForm({
  cvId,
  extractedData,
  onSubmit,
  onCancel,
}: CVVerificationFormProps) {
  const [formData, setFormData] = useState({
    nom_complet: extractedData.nom_complet || "",
    email: extractedData.email || "",
    telephone: extractedData.telephone || "",
    ville: extractedData.ville || "",
    competences: extractedData.competences || [],
  })

  const [newCompetence, setNewCompetence] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleAddCompetence = () => {
    if (newCompetence.trim() && !formData.competences.includes(newCompetence.trim())) {
      setFormData((prev) => ({
        ...prev,
        competences: [...prev.competences, newCompetence.trim()],
      }))
      setNewCompetence("")
    }
  }

  const handleRemoveCompetence = (competence: string) => {
    setFormData((prev) => ({
      ...prev,
      competences: prev.competences.filter((c) => c !== competence),
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      await onSubmit({
        cv_id: cvId,
        nom_complet: formData.nom_complet || null,
        email_cv: formData.email || null,
        telephone_cv: formData.telephone || null,
        ville: formData.ville || null,
        competences_extraites: formData.competences,
      })
      toast.success("✅ CV enregistré avec succès!")
    } catch (error) {
      toast.error("❌ Erreur lors de l'enregistrement du CV")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card className="w-full max-w-3xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-primary" />
          Vérifiez les informations extraites
        </CardTitle>
        <CardDescription>
          Nous avons extrait ces informations de votre CV. Veuillez les vérifier et les corriger si nécessaire.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Nom complet */}
          <div className="space-y-2">
            <Label htmlFor="nom_complet">
              Nom complet <span className="text-muted-foreground text-sm">(optionnel)</span>
            </Label>
            <Input
              id="nom_complet"
              value={formData.nom_complet}
              onChange={(e) => setFormData((prev) => ({ ...prev, nom_complet: e.target.value }))}
              placeholder="Prénom NOM"
              className="w-full"
            />
          </div>

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email">
              Email <span className="text-muted-foreground text-sm">(optionnel)</span>
            </Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData((prev) => ({ ...prev, email: e.target.value }))}
              placeholder="email@example.com"
              className="w-full"
            />
          </div>

          {/* Téléphone */}
          <div className="space-y-2">
            <Label htmlFor="telephone">
              Téléphone <span className="text-muted-foreground text-sm">(optionnel)</span>
            </Label>
            <Input
              id="telephone"
              value={formData.telephone}
              onChange={(e) => setFormData((prev) => ({ ...prev, telephone: e.target.value }))}
              placeholder="+212 6 XX XX XX XX"
              className="w-full"
            />
          </div>

          {/* Ville */}
          <div className="space-y-2">
            <Label htmlFor="ville">
              Ville <span className="text-muted-foreground text-sm">(optionnel)</span>
            </Label>
            <Input
              id="ville"
              value={formData.ville}
              onChange={(e) => setFormData((prev) => ({ ...prev, ville: e.target.value }))}
              placeholder="Casablanca, Rabat, Marrakech..."
              className="w-full"
            />
          </div>

          {/* Compétences */}
          <div className="space-y-3">
            <Label>Compétences</Label>
            <div className="flex gap-2">
              <Input
                value={newCompetence}
                onChange={(e) => setNewCompetence(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault()
                    handleAddCompetence()
                  }
                }}
                placeholder="Ajouter une compétence..."
                className="flex-1"
              />
              <Button type="button" onClick={handleAddCompetence} size="icon" variant="outline">
                <Plus className="w-4 h-4" />
              </Button>
            </div>

            {formData.competences.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-3 p-3 bg-muted rounded-lg">
                {formData.competences.map((comp, index) => (
                  <Badge key={index} variant="secondary" className="text-sm py-1.5 px-3">
                    {comp}
                    <button
                      type="button"
                      onClick={() => handleRemoveCompetence(comp)}
                      className="ml-2 hover:text-destructive"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Informations supplémentaires */}
          {(extractedData.experience.length > 0 ||
            extractedData.formation.length > 0 ||
            extractedData.langues.length > 0) && (
            <div className="space-y-3 p-4 bg-muted/50 rounded-lg">
              <h4 className="font-medium text-sm text-muted-foreground">
                Autres informations détectées (pour référence)
              </h4>

              {extractedData.langues.length > 0 && (
                <div>
                  <span className="text-sm font-medium">Langues: </span>
                  <span className="text-sm text-muted-foreground">{extractedData.langues.join(", ")}</span>
                </div>
              )}

              {extractedData.experience.length > 0 && (
                <div>
                  <span className="text-sm font-medium">Expérience détectée</span>
                </div>
              )}

              {extractedData.formation.length > 0 && (
                <div>
                  <span className="text-sm font-medium">Formation détectée</span>
                </div>
              )}
            </div>
          )}

          {/* Boutons d'action */}
          <div className="flex gap-3 pt-4">
            <Button type="submit" className="flex-1" disabled={isSubmitting}>
              {isSubmitting ? "Enregistrement..." : "✓ Confirmer et Enregistrer"}
            </Button>
            <Button type="button" variant="outline" onClick={onCancel} disabled={isSubmitting}>
              Annuler
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

