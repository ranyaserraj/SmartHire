"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Bell, Plus, Trash2, MapPin, Briefcase, DollarSign } from "lucide-react"
import { toast } from "sonner"

function AlertesPage() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      nom: "Dev Python - Rabat",
      poste: "Python Developer",
      ville: "Rabat",
      type_contrat: "CDI",
      salaire_min: 12000,
      frequence: "quotidienne",
      active: true,
      offresCount: 12,
    },
    {
      id: 2,
      nom: "Full Stack - Casablanca",
      poste: "Full Stack Developer",
      ville: "Casablanca",
      type_contrat: "CDI",
      salaire_min: 15000,
      frequence: "hebdomadaire",
      active: false,
      offresCount: 8,
    },
  ])

  const [newAlert, setNewAlert] = useState({
    nom: "",
    poste: "",
    ville: "",
    type_contrat: "",
    salaire_min: 0,
    frequence: "quotidienne",
  })

  const handleToggle = (id: number) => {
    setAlerts(alerts.map((alert) => (alert.id === id ? { ...alert, active: !alert.active } : alert)))
    toast.success("Alerte mise à jour")
  }

  const handleDelete = (id: number) => {
    setAlerts(alerts.filter((alert) => alert.id !== id))
    toast.success("Alerte supprimée")
  }

  const handleCreate = () => {
    if (!newAlert.nom || !newAlert.poste) {
      toast.error("Veuillez remplir tous les champs obligatoires")
      return
    }

    const alert = {
      id: alerts.length + 1,
      ...newAlert,
      active: true,
      offresCount: 0,
    }

    setAlerts([...alerts, alert])
    setShowCreateModal(false)
    setNewAlert({
      nom: "",
      poste: "",
      ville: "",
      type_contrat: "",
      salaire_min: 0,
      frequence: "quotidienne",
    })
    toast.success("Alerte créée avec succès !")
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Mes Alertes Emploi</h1>
              <p className="text-gray-600 mt-2">Recevez des notifications quand de nouvelles offres correspondent à votre profil</p>
            </div>
            <Dialog open={showCreateModal} onOpenChange={setShowCreateModal}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Créer une alerte
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                  <DialogTitle>Créer une nouvelle alerte</DialogTitle>
                  <DialogDescription>
                    Définissez vos critères de recherche et recevez des notifications automatiques
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label htmlFor="nom">Nom de l'alerte *</Label>
                    <Input
                      id="nom"
                      value={newAlert.nom}
                      onChange={(e) => setNewAlert({ ...newAlert, nom: e.target.value })}
                      placeholder="Ex: Dev React - Casablanca"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="poste">Mots-clés / Titre du poste *</Label>
                    <Input
                      id="poste"
                      value={newAlert.poste}
                      onChange={(e) => setNewAlert({ ...newAlert, poste: e.target.value })}
                      placeholder="Ex: Développeur React"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="ville">Localisation</Label>
                      <Select value={newAlert.ville} onValueChange={(value) => setNewAlert({ ...newAlert, ville: value })}>
                        <SelectTrigger>
                          <SelectValue placeholder="Toutes" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Toutes</SelectItem>
                          <SelectItem value="Casablanca">Casablanca</SelectItem>
                          <SelectItem value="Rabat">Rabat</SelectItem>
                          <SelectItem value="Tanger">Tanger</SelectItem>
                          <SelectItem value="Marrakech">Marrakech</SelectItem>
                          <SelectItem value="Fès">Fès</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="type_contrat">Type de contrat</Label>
                      <Select
                        value={newAlert.type_contrat}
                        onValueChange={(value) => setNewAlert({ ...newAlert, type_contrat: value })}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Tous" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Tous</SelectItem>
                          <SelectItem value="CDI">CDI</SelectItem>
                          <SelectItem value="CDD">CDD</SelectItem>
                          <SelectItem value="Stage">Stage</SelectItem>
                          <SelectItem value="Freelance">Freelance</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="salaire">Salaire minimum (MAD)</Label>
                    <Input
                      id="salaire"
                      type="number"
                      value={newAlert.salaire_min}
                      onChange={(e) => setNewAlert({ ...newAlert, salaire_min: parseInt(e.target.value) || 0 })}
                      placeholder="0"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="frequence">Fréquence des notifications</Label>
                    <Select
                      value={newAlert.frequence}
                      onValueChange={(value) => setNewAlert({ ...newAlert, frequence: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="quotidienne">Quotidienne</SelectItem>
                        <SelectItem value="hebdomadaire">Hebdomadaire</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="flex gap-3">
                  <Button variant="outline" onClick={() => setShowCreateModal(false)} className="flex-1">
                    Annuler
                  </Button>
                  <Button onClick={handleCreate} className="flex-1">
                    Créer l'alerte
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {alerts.length === 0 ? (
            <Card className="p-12">
              <div className="flex flex-col items-center justify-center text-center">
                <Bell className="h-16 w-16 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Aucune alerte créée</h3>
                <p className="text-gray-500 mb-4 max-w-md">
                  Créez votre première alerte pour recevoir des notifications automatiques sur les nouvelles offres
                </p>
                <Button onClick={() => setShowCreateModal(true)}>
                  <Plus className="mr-2 h-4 w-4" />
                  Créer ma première alerte
                </Button>
              </div>
            </Card>
          ) : (
            <div className="space-y-4">
              {alerts.map((alert) => (
                <Card key={alert.id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      {/* Toggle ON/OFF */}
                      <Switch checked={alert.active} onCheckedChange={() => handleToggle(alert.id)} />

                      {/* Infos de l'alerte */}
                      <div className="flex-1 mx-6">
                        <h3 className="font-semibold text-gray-900 text-lg mb-2">{alert.nom}</h3>
                        <div className="flex flex-wrap gap-2 mb-3">
                          <Badge variant="outline" className="flex items-center gap-1">
                            <Briefcase className="h-3 w-3" />
                            {alert.poste}
                          </Badge>
                          {alert.ville && (
                            <Badge variant="outline" className="flex items-center gap-1">
                              <MapPin className="h-3 w-3" />
                              {alert.ville}
                            </Badge>
                          )}
                          {alert.type_contrat && <Badge variant="outline">{alert.type_contrat}</Badge>}
                          {alert.salaire_min > 0 && (
                            <Badge variant="outline" className="flex items-center gap-1">
                              <DollarSign className="h-3 w-3" />
                              {alert.salaire_min}+ MAD
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-gray-600">
                          <span className="font-medium">{alert.offresCount} offres trouvées</span> • Notifications {alert.frequence}
                        </p>
                      </div>

                      {/* Action : UNIQUEMENT Supprimer */}
                      <Button variant="ghost" size="sm" onClick={() => handleDelete(alert.id)}>
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
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

export default AlertesPage


