"use client"

import { useState, useEffect } from "react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { useAuth } from "@/contexts/AuthContext"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Checkbox } from "@/components/ui/checkbox"
import { Camera, Save } from "lucide-react"
import { toast } from "sonner"
import { useRouter } from "next/navigation"

function ProfilPage() {
  const { user } = useAuth()
  const router = useRouter()
  
  const [formData, setFormData] = useState({
    prenom: "",
    nom: "",
    email: "",
    telephone: "",
    ville: "",
    ville_preferee: "",
    salaire_minimum: 0,
    type_contrat_prefere: "",
    accepte_remote: false,
    secteur_activite: "",
  })
  const [photoPreview, setPhotoPreview] = useState<string | null>(null)
  const [photoFile, setPhotoFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Charger les données utilisateur au montage et quand elles changent
  useEffect(() => {
    console.log("User data:", user)
    
    if (user) {
      setFormData({
        prenom: user.prenom || "",
        nom: user.nom || "",
        email: user.email || "",
        telephone: user.telephone || "",
        ville: user.ville_preferee || "",
        ville_preferee: user.ville_preferee || "",
        salaire_minimum: user.salaire_minimum || 0,
        type_contrat_prefere: user.type_contrat_prefere || "",
        accepte_remote: user.accepte_teletravail || false,
        secteur_activite: user.secteur_activite || "",
      })
      setIsLoading(false)
    }
  }, [user])

  const getInitials = (prenom?: string, nom?: string) => {
    if (!prenom || !nom) return "U"
    return `${prenom.charAt(0)}${nom.charAt(0)}`.toUpperCase()
  }

  const getPhotoUrl = () => {
    if (photoPreview) return photoPreview
    if (!user?.photo_profil) return undefined
    if (user.photo_profil.startsWith("http")) return user.photo_profil
    return `http://localhost:8080${user.photo_profil}`
  }

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleSave = async () => {
    setIsLoading(true)
    try {
      const token = localStorage.getItem("token")
      if (!token) {
        toast.error("Vous devez être connecté")
        return
      }

      const response = await fetch("http://localhost:8080/api/users/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          nom: formData.nom,
          prenom: formData.prenom,
          telephone: formData.telephone,
          ville_preferee: formData.ville_preferee,
          salaire_minimum: formData.salaire_minimum,
          type_contrat_prefere: formData.type_contrat_prefere,
          secteur_activite: formData.secteur_activite,
          accepte_teletravail: formData.accepte_remote,
        }),
      })

      if (!response.ok) {
        throw new Error("Erreur lors de la mise à jour")
      }

      const updatedUser = await response.json()
      
      toast.success("Profil mis à jour avec succès !")
      
      // Recharger les données utilisateur depuis l'API
      const meResponse = await fetch("http://localhost:8080/api/auth/me", {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })
      
      if (meResponse.ok) {
        const userData = await meResponse.json()
        console.log("Données utilisateur rechargées:", userData)
        
        // Attendre un court instant pour que le toast soit visible
        setTimeout(() => {
          // Rediriger vers le dashboard
          router.push("/dashboard")
        }, 1000)
      }
    } catch (error: any) {
      toast.error(error.message || "Erreur lors de la mise à jour")
    } finally {
      setIsLoading(false)
    }
  }

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast.error("La photo ne doit pas dépasser 5MB")
        return
      }
      
      if (!file.type.startsWith("image/")) {
        toast.error("Le fichier doit être une image")
        return
      }
      
      setPhotoFile(file)
      
      const reader = new FileReader()
      reader.onloadend = () => {
        setPhotoPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleChangePhoto = async () => {
    if (!photoFile) {
      document.getElementById("photo-input")?.click()
      return
    }

    setIsLoading(true)
    try {
      const token = localStorage.getItem("token")
      if (!token) {
        toast.error("Vous devez être connecté")
        return
      }

      const formData = new FormData()
      formData.append("file", photoFile)

      const response = await fetch("http://localhost:8080/api/users/photo", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Erreur lors de l'upload")
      }

      toast.success("Photo mise à jour avec succès !")
      
      // Réinitialiser le preview et le file
      setPhotoPreview(null)
      setPhotoFile(null)
      
      // Recharger les données utilisateur pour avoir la nouvelle photo
      const meResponse = await fetch("http://localhost:8080/api/auth/me", {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })
      
      if (meResponse.ok) {
        // La navbar se mettra à jour automatiquement via le contexte
        // On force juste un refresh de la page pour que tout se mette à jour
        setTimeout(() => {
          window.location.reload()
        }, 500)
      }
    } catch (error: any) {
      toast.error(error.message || "Erreur lors de l'upload")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-5xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Mon Profil</h1>
            <p className="text-gray-600 mt-2">Gérez vos informations personnelles et préférences</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            {/* Photo de profil */}
            <Card>
              <CardHeader>
                <CardTitle>Photo de profil</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col items-center">
                <Avatar className="h-32 w-32 mb-4">
                  <AvatarImage src={getPhotoUrl()} />
                  <AvatarFallback className="bg-blue-600 text-white text-3xl">
                    {getInitials(formData.prenom, formData.nom)}
                  </AvatarFallback>
                </Avatar>
                <input
                  id="photo-input"
                  type="file"
                  accept="image/*"
                  onChange={handlePhotoChange}
                  className="hidden"
                />
                <Button 
                  onClick={handleChangePhoto} 
                  variant="outline" 
                  className="w-full"
                  disabled={isLoading}
                >
                  <Camera className="mr-2 h-4 w-4" />
                  {photoFile ? "Enregistrer la photo" : "Changer la photo"}
                </Button>
              </CardContent>
            </Card>

            {/* Informations personnelles */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Informations personnelles</CardTitle>
                <CardDescription>Mettez à jour vos informations de contact</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="prenom">Prénom</Label>
                    <Input
                      id="prenom"
                      value={formData.prenom}
                      onChange={(e) => handleChange("prenom", e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="nom">Nom</Label>
                    <Input id="nom" value={formData.nom} onChange={(e) => handleChange("nom", e.target.value)} />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" value={formData.email} disabled className="bg-gray-100" />
                  <p className="text-xs text-gray-500">L'email ne peut pas être modifié</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="telephone">Téléphone</Label>
                    <Input
                      id="telephone"
                      value={formData.telephone}
                      onChange={(e) => handleChange("telephone", e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="ville">Ville</Label>
                    <Select value={formData.ville} onValueChange={(value) => handleChange("ville", value)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Casablanca">Casablanca</SelectItem>
                        <SelectItem value="Rabat">Rabat</SelectItem>
                        <SelectItem value="Tanger">Tanger</SelectItem>
                        <SelectItem value="Marrakech">Marrakech</SelectItem>
                        <SelectItem value="Fès">Fès</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Préférences */}
          <Card>
            <CardHeader>
              <CardTitle>Préférences d'emploi</CardTitle>
              <CardDescription>Définissez vos critères de recherche d'emploi</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="ville_preferee">Ville préférée</Label>
                  <Select
                    value={formData.ville_preferee}
                    onValueChange={(value) => handleChange("ville_preferee", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Casablanca">Casablanca</SelectItem>
                      <SelectItem value="Rabat">Rabat</SelectItem>
                      <SelectItem value="Tanger">Tanger</SelectItem>
                      <SelectItem value="Marrakech">Marrakech</SelectItem>
                      <SelectItem value="Fès">Fès</SelectItem>
                      <SelectItem value="Toutes">Toutes</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="salaire_minimum">Salaire minimum (MAD)</Label>
                  <Input
                    id="salaire_minimum"
                    type="number"
                    value={formData.salaire_minimum}
                    onChange={(e) => handleChange("salaire_minimum", parseInt(e.target.value))}
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="type_contrat">Type de contrat préféré</Label>
                  <Select
                    value={formData.type_contrat_prefere}
                    onValueChange={(value) => handleChange("type_contrat_prefere", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="CDI">CDI</SelectItem>
                      <SelectItem value="CDD">CDD</SelectItem>
                      <SelectItem value="Stage">Stage</SelectItem>
                      <SelectItem value="Freelance">Freelance</SelectItem>
                      <SelectItem value="Tous">Tous</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="secteur">Secteur d'activité</Label>
                  <Input
                    id="secteur"
                    value={formData.secteur_activite}
                    onChange={(e) => handleChange("secteur_activite", e.target.value)}
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="remote"
                  checked={formData.accepte_remote}
                  onCheckedChange={(checked) => handleChange("accepte_remote", checked)}
                />
                <label
                  htmlFor="remote"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  J'accepte le télétravail
                </label>
              </div>
            </CardContent>
          </Card>

          {/* Save Button */}
          <div className="mt-6 flex justify-end">
            <Button onClick={handleSave} size="lg" disabled={isLoading}>
              <Save className="mr-2 h-5 w-5" />
              {isLoading ? "Enregistrement..." : "Enregistrer les modifications"}
            </Button>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}

export default ProfilPage


