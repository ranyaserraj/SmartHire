"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Search, Building2, MapPin, TrendingUp, Clock, Briefcase } from "lucide-react"
import { toast } from "sonner"

const recommendedOffers = [
  {
    id: 1,
    titre: "Développeur Full Stack Senior",
    entreprise: "TechVision Solutions",
    ville: "Casablanca",
    scoreML: 95,
    probabilite: 82,
    competences: ["React", "Node.js", "PostgreSQL", "Docker"],
    salaire: "15000-20000 MAD",
    type: "CDI",
    datePublication: "Il y a 2 jours",
  },
  {
    id: 2,
    titre: "Ingénieur DevOps",
    entreprise: "CloudTech Morocco",
    ville: "Rabat",
    scoreML: 88,
    probabilite: 75,
    competences: ["AWS", "Kubernetes", "Docker", "CI/CD"],
    salaire: "18000-25000 MAD",
    type: "CDI",
    datePublication: "Il y a 1 jour",
  },
  {
    id: 3,
    titre: "Tech Lead React",
    entreprise: "Digital Innovations",
    ville: "Casablanca",
    scoreML: 92,
    probabilite: 80,
    competences: ["React", "TypeScript", "Leadership", "Agile"],
    salaire: "20000-28000 MAD",
    type: "CDI",
    datePublication: "Il y a 3 jours",
  },
]

interface JobSearchTabsProps {
  onJobSelect: (jobText: string) => void
}

export default function JobSearchTabs({ onJobSelect }: JobSearchTabsProps) {
  const [manualInput, setManualInput] = useState("")
  const [searchFilters, setSearchFilters] = useState({
    poste: "",
    ville: "",
    typeContrat: "",
    salaireMin: 0,
    remote: false,
  })

  const handleAnalyzeOffer = (offer: any) => {
    const offerText = `${offer.titre}\n${offer.entreprise}\n${offer.ville}\n${offer.type}\n${offer.salaire}\nCompétences requises: ${offer.competences.join(", ")}`
    onJobSelect(offerText)
    toast.success("Offre sélectionnée pour analyse")
  }

  const handleSearch = () => {
    toast.info("Recherche en cours...", {
      description: "Fonctionnalité en développement",
    })
  }

  const getScoreBadgeColor = (score: number) => {
    if (score >= 80) return "bg-green-100 text-green-700 border-green-300"
    if (score >= 60) return "bg-orange-100 text-orange-700 border-orange-300"
    return "bg-red-100 text-red-700 border-red-300"
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recherche d'Offres Intelligente</CardTitle>
        <CardDescription>Trouvez les meilleures offres correspondant à votre profil</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="recommended" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="recommended">Offres Recommandées</TabsTrigger>
            <TabsTrigger value="search">Rechercher</TabsTrigger>
            <TabsTrigger value="manual">Saisie manuelle</TabsTrigger>
          </TabsList>

          {/* Tab 1: Offres Recommandées */}
          <TabsContent value="recommended" className="space-y-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg mb-4">
              <p className="text-sm text-blue-800">
                ✨ Basé sur votre CV, voici les 10 meilleures offres pour vous
              </p>
            </div>

            {/* Filtres rapides */}
            <div className="flex flex-wrap gap-2 mb-4">
              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Localisation" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Toutes</SelectItem>
                  <SelectItem value="casablanca">Casablanca</SelectItem>
                  <SelectItem value="rabat">Rabat</SelectItem>
                  <SelectItem value="tanger">Tanger</SelectItem>
                </SelectContent>
              </Select>

              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Type de contrat" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Tous</SelectItem>
                  <SelectItem value="cdi">CDI</SelectItem>
                  <SelectItem value="cdd">CDD</SelectItem>
                  <SelectItem value="stage">Stage</SelectItem>
                </SelectContent>
              </Select>

              <Select>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Salaire min" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">Tous</SelectItem>
                  <SelectItem value="10000">10000+ MAD</SelectItem>
                  <SelectItem value="15000">15000+ MAD</SelectItem>
                  <SelectItem value="20000">20000+ MAD</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Liste des offres */}
            <div className="space-y-4">
              {recommendedOffers.map((offer) => (
                <Card key={offer.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex gap-4">
                      {/* Logo */}
                      <div className="flex-shrink-0">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold">
                          {offer.entreprise.charAt(0)}
                        </div>
                      </div>

                      {/* Contenu */}
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-1">{offer.titre}</h4>
                            <div className="flex items-center gap-3 text-sm text-gray-600">
                              <div className="flex items-center gap-1">
                                <Building2 className="h-3 w-3" />
                                {offer.entreprise}
                              </div>
                              <div className="flex items-center gap-1">
                                <MapPin className="h-3 w-3" />
                                {offer.ville}
                              </div>
                              <div className="flex items-center gap-1">
                                <Clock className="h-3 w-3" />
                                {offer.datePublication}
                              </div>
                            </div>
                          </div>
                          <div className="flex flex-col gap-1 items-end">
                            <Badge className={`${getScoreBadgeColor(offer.scoreML)} border`}>
                              {offer.scoreML}% match
                            </Badge>
                            <Badge variant="secondary" className="text-xs">
                              {offer.probabilite}% acceptation
                            </Badge>
                          </div>
                        </div>

                        {/* Compétences */}
                        <div className="flex flex-wrap gap-2 mb-3">
                          {offer.competences.map((comp, idx) => (
                            <Badge key={idx} variant="outline" className="bg-green-50 text-green-700 border-green-200">
                              {comp}
                            </Badge>
                          ))}
                        </div>

                        {/* Info et Actions */}
                        <div className="flex items-center justify-between">
                          <div className="text-sm">
                            <span className="font-semibold text-gray-900">{offer.salaire}</span>
                            <span className="text-gray-500"> • {offer.type}</span>
                          </div>
                          <div className="flex gap-2">
                            <Button onClick={() => handleAnalyzeOffer(offer)}>
                              <TrendingUp className="mr-2 h-4 w-4" />
                              Analyser
                            </Button>
                            <Button variant="outline" onClick={() => toast.info("Détails de l'offre")}>
                              Voir détails
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <div className="flex justify-center pt-4">
              <Button variant="outline">Voir plus d'offres</Button>
            </div>
          </TabsContent>

          {/* Tab 2: Rechercher */}
          <TabsContent value="search" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="search-poste">Titre du poste</Label>
                <Input
                  id="search-poste"
                  placeholder="Ex: Développeur Full Stack"
                  value={searchFilters.poste}
                  onChange={(e) => setSearchFilters({ ...searchFilters, poste: e.target.value })}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="search-ville">Ville</Label>
                <Select value={searchFilters.ville} onValueChange={(value) => setSearchFilters({ ...searchFilters, ville: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Toutes" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Toutes</SelectItem>
                    <SelectItem value="casablanca">Casablanca</SelectItem>
                    <SelectItem value="rabat">Rabat</SelectItem>
                    <SelectItem value="tanger">Tanger</SelectItem>
                    <SelectItem value="marrakech">Marrakech</SelectItem>
                    <SelectItem value="fes">Fès</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="search-contrat">Type de contrat</Label>
                <Select value={searchFilters.typeContrat} onValueChange={(value) => setSearchFilters({ ...searchFilters, typeContrat: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Tous" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Tous</SelectItem>
                    <SelectItem value="cdi">CDI</SelectItem>
                    <SelectItem value="cdd">CDD</SelectItem>
                    <SelectItem value="stage">Stage</SelectItem>
                    <SelectItem value="freelance">Freelance</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="search-salaire">Salaire minimum (MAD)</Label>
                <Input
                  id="search-salaire"
                  type="number"
                  placeholder="0"
                  value={searchFilters.salaireMin}
                  onChange={(e) => setSearchFilters({ ...searchFilters, salaireMin: parseInt(e.target.value) || 0 })}
                />
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="remote"
                checked={searchFilters.remote}
                onCheckedChange={(checked) => setSearchFilters({ ...searchFilters, remote: checked as boolean })}
              />
              <label htmlFor="remote" className="text-sm font-medium">
                Accepte télétravail
              </label>
            </div>

            <Button onClick={handleSearch} className="w-full">
              <Search className="mr-2 h-4 w-4" />
              Rechercher
            </Button>

            <div className="text-center text-sm text-gray-500 mt-4">
              Utilisez les filtres pour affiner votre recherche
            </div>
          </TabsContent>

          {/* Tab 3: Saisie manuelle */}
          <TabsContent value="manual" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="manual-input">Coller l'offre d'emploi ou l'URL</Label>
              <Textarea
                id="manual-input"
                placeholder="Collez ici le texte de l'offre d'emploi ou l'URL..."
                className="min-h-[200px]"
                value={manualInput}
                onChange={(e) => setManualInput(e.target.value)}
              />
            </div>
            <Button
              onClick={() => {
                if (manualInput) {
                  onJobSelect(manualInput)
                  toast.success("Offre saisie avec succès")
                }
              }}
              disabled={!manualInput}
              className="w-full"
            >
              Utiliser cette offre
            </Button>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}


