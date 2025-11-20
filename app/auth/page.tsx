"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { AlertCircle, Upload, Camera } from "lucide-react"
import { useAuth } from "@/contexts/AuthContext"
import { toast } from "sonner"

// Villes principales du Maroc
const VILLES_MAROC = [
  "Casablanca",
  "Rabat",
  "Fès",
  "Marrakech",
  "Tanger",
  "Salé",
  "Meknès",
  "Oujda",
  "Kénitra",
  "Agadir",
  "Tétouan",
  "Témara",
  "Safi",
  "Mohammédia",
  "Khouribga",
  "El Jadida",
  "Béni Mellal",
  "Nador",
  "Autre"
]

export default function AuthPage() {
  const router = useRouter()
  const { login, register } = useAuth()
  
  const [isLogin, setIsLogin] = useState(true)
  
  // Champs Login
  const [loginEmail, setLoginEmail] = useState("")
  const [loginPassword, setLoginPassword] = useState("")
  
  // Champs Registration
  const [nom, setNom] = useState("")
  const [prenom, setPrenom] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [telephone, setTelephone] = useState("")
  const [villePreferee, setVillePreferee] = useState("")
  const [photoProfil, setPhotoProfil] = useState<File | null>(null)
  const [photoPreview, setPhotoPreview] = useState<string | null>(null)
  
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)

  const validateLoginForm = () => {
    const newErrors: Record<string, string> = {}

    if (!loginEmail) {
      newErrors.loginEmail = "L'email est requis"
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(loginEmail)) {
      newErrors.loginEmail = "Veuillez entrer un email valide"
    }

    if (!loginPassword) {
      newErrors.loginPassword = "Le mot de passe est requis"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const validateRegisterForm = () => {
    const newErrors: Record<string, string> = {}

    if (!nom) {
      newErrors.nom = "Le nom est requis"
    }

    if (!prenom) {
      newErrors.prenom = "Le prénom est requis"
    }

    if (!email) {
      newErrors.email = "L'email est requis"
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Veuillez entrer un email valide"
    }

    if (!password) {
      newErrors.password = "Le mot de passe est requis"
    } else if (password.length < 6) {
      newErrors.password = "Le mot de passe doit contenir au moins 6 caractères"
    }

      if (!confirmPassword) {
      newErrors.confirmPassword = "Veuillez confirmer votre mot de passe"
      } else if (password !== confirmPassword) {
      newErrors.confirmPassword = "Les mots de passe ne correspondent pas"
      }

    if (telephone && !/^(\+212|0)[5-7][0-9]{8}$/.test(telephone.replace(/\s/g, ''))) {
      newErrors.telephone = "Numéro de téléphone invalide (ex: +212612345678 ou 0612345678)"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateLoginForm()) return

    setIsLoading(true)
    
    try {
      await login(loginEmail, loginPassword)
      toast.success("Connexion réussie !")
      router.push("/dashboard")
    } catch (error: any) {
      toast.error(error.message || "Erreur lors de la connexion")
      setErrors({ loginPassword: "Email ou mot de passe incorrect" })
    } finally {
      setIsLoading(false)
    }
  }

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // Vérifier la taille (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setErrors({ ...errors, photo: "La photo ne doit pas dépasser 5MB" })
        return
      }
      
      // Vérifier le type
      if (!file.type.startsWith("image/")) {
        setErrors({ ...errors, photo: "Le fichier doit être une image" })
        return
      }
      
      setPhotoProfil(file)
      
      // Créer une preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPhotoPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
      
      // Retirer l'erreur photo si elle existe
      const newErrors = { ...errors }
      delete newErrors.photo
      setErrors(newErrors)
    }
  }

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateRegisterForm()) return

    setIsLoading(true)
    
    try {
      // Appeler la fonction register de AuthContext
      await register(email, password, nom, prenom, telephone, villePreferee, photoProfil)
      
      toast.success("Inscription réussie ! Bienvenue sur SmartHire 🎉")
      
      // Redirection automatique vers le dashboard (l'utilisateur est déjà connecté)
      router.push("/dashboard")
    } catch (error: any) {
      toast.error(error.message || "Erreur lors de l'inscription")
      
      if (error.message.includes("email")) {
        setErrors({ email: "Cet email est déjà utilisé" })
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center px-6 py-12">
      <Card className="w-full max-w-2xl p-8 shadow-xl border-2 border-blue-100">
        <div className="space-y-6">
          <div className="space-y-2 text-center">
            <Link href="/" className="text-3xl font-bold text-blue-600 inline-block mb-2">
              SmartHire
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">
              {isLogin ? "Se connecter" : "Créer un compte"}
            </h1>
            <p className="text-sm text-gray-600">
              {isLogin 
                ? "Accédez à votre compte SmartHire" 
                : "Rejoignez SmartHire pour booster votre carrière"}
            </p>
          </div>

          {/* TABS pour switcher entre Login et Register */}
          <div className="flex gap-2 p-1 bg-gray-100 rounded-lg">
            <button
              onClick={() => {
                setIsLogin(true)
                setErrors({})
              }}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                isLogin 
                  ? "bg-white text-blue-600 shadow" 
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              Connexion
            </button>
            <button
              onClick={() => {
                setIsLogin(false)
                setErrors({})
              }}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-all ${
                !isLogin 
                  ? "bg-white text-blue-600 shadow" 
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              S'inscrire
            </button>
          </div>

          {/* FORMULAIRE LOGIN */}
          {isLogin && (
            <form onSubmit={handleLoginSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="loginEmail">Email</Label>
                <Input
                  id="loginEmail"
                  type="email"
                  placeholder="vous@exemple.com"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className={errors.loginEmail ? "border-red-500" : ""}
                />
                {errors.loginEmail && (
                  <div className="flex items-center gap-2 text-red-500 text-xs">
                    <AlertCircle size={14} />
                    {errors.loginEmail}
                  </div>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="loginPassword">Mot de passe</Label>
                <Input
                  id="loginPassword"
                  type="password"
                  placeholder="Minimum 6 caractères"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  className={errors.loginPassword ? "border-red-500" : ""}
                />
                {errors.loginPassword && (
                  <div className="flex items-center gap-2 text-red-500 text-xs">
                    <AlertCircle size={14} />
                    {errors.loginPassword}
                  </div>
                )}
              </div>

              <Button 
                type="submit" 
                disabled={isLoading} 
                className="w-full bg-blue-600 hover:bg-blue-700 text-white h-11"
              >
                {isLoading ? "Connexion..." : "Se connecter"}
              </Button>
            </form>
          )}

          {/* FORMULAIRE INSCRIPTION */}
          {!isLogin && (
            <form onSubmit={handleRegisterSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {/* Prénom */}
                <div className="space-y-2">
                  <Label htmlFor="prenom">Prénom *</Label>
                  <Input
                    id="prenom"
                    type="text"
                    placeholder="Ranya"
                    value={prenom}
                    onChange={(e) => setPrenom(e.target.value)}
                    className={errors.prenom ? "border-red-500" : ""}
                  />
                  {errors.prenom && (
                    <div className="flex items-center gap-2 text-red-500 text-xs">
                      <AlertCircle size={14} />
                      {errors.prenom}
                    </div>
                  )}
                </div>

                {/* Nom */}
                <div className="space-y-2">
                  <Label htmlFor="nom">Nom *</Label>
                  <Input
                    id="nom"
                    type="text"
                    placeholder="SERRAJ"
                    value={nom}
                    onChange={(e) => setNom(e.target.value)}
                    className={errors.nom ? "border-red-500" : ""}
                  />
                  {errors.nom && (
                    <div className="flex items-center gap-2 text-red-500 text-xs">
                      <AlertCircle size={14} />
                      {errors.nom}
                    </div>
                  )}
                </div>
              </div>

              {/* Email */}
              <div className="space-y-2">
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="vous@exemple.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={errors.email ? "border-red-500" : ""}
                />
                {errors.email && (
                  <div className="flex items-center gap-2 text-red-500 text-xs">
                    <AlertCircle size={14} />
                    {errors.email}
                  </div>
                )}
              </div>

              {/* Photo de profil */}
              <div className="space-y-2">
                <Label htmlFor="photo">Photo de profil (optionnel)</Label>
                <div className="flex items-center gap-4">
                  {photoPreview && (
                    <div className="relative w-20 h-20 rounded-full overflow-hidden border-2 border-blue-500">
                      <img
                        src={photoPreview}
                        alt="Preview"
                        className="w-full h-full object-cover"
                      />
                    </div>
                  )}
                  <div className="flex-1">
                    <Input
                      id="photo"
                      type="file"
                      accept="image/*"
                      onChange={handlePhotoChange}
                      className={errors.photo ? "border-red-500" : ""}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Format: JPG, PNG, GIF (Max 5MB)
                    </p>
                  </div>
                </div>
                {errors.photo && (
                  <div className="flex items-center gap-2 text-red-500 text-xs">
                    <AlertCircle size={14} />
                    {errors.photo}
                  </div>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                {/* Téléphone */}
                <div className="space-y-2">
                  <Label htmlFor="telephone">Téléphone</Label>
                  <Input
                    id="telephone"
                    type="tel"
                    placeholder="+212 6XX XX XX XX"
                    value={telephone}
                    onChange={(e) => setTelephone(e.target.value)}
                    className={errors.telephone ? "border-red-500" : ""}
                  />
                  {errors.telephone && (
                    <div className="flex items-center gap-2 text-red-500 text-xs">
                      <AlertCircle size={14} />
                      {errors.telephone}
                    </div>
                  )}
                </div>

                {/* Ville préférée */}
                <div className="space-y-2">
                  <Label htmlFor="ville">Ville préférée</Label>
                  <Select value={villePreferee} onValueChange={setVillePreferee}>
                    <SelectTrigger id="ville">
                      <SelectValue placeholder="Choisir une ville" />
                    </SelectTrigger>
                    <SelectContent>
                      {VILLES_MAROC.map((ville) => (
                        <SelectItem key={ville} value={ville}>
                          {ville}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                {/* Mot de passe */}
            <div className="space-y-2">
                  <Label htmlFor="password">Mot de passe *</Label>
              <Input
                id="password"
                type="password"
                    placeholder="Min. 6 caractères"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={errors.password ? "border-red-500" : ""}
              />
              {errors.password && (
                <div className="flex items-center gap-2 text-red-500 text-xs">
                  <AlertCircle size={14} />
                  {errors.password}
                </div>
              )}
            </div>

                {/* Confirmer mot de passe */}
              <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirmer *</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                    placeholder="Répétez le mot de passe"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={errors.confirmPassword ? "border-red-500" : ""}
                />
                {errors.confirmPassword && (
                  <div className="flex items-center gap-2 text-red-500 text-xs">
                    <AlertCircle size={14} />
                    {errors.confirmPassword}
                  </div>
                )}
              </div>
              </div>

              <Button 
                type="submit" 
                disabled={isLoading} 
                className="w-full bg-blue-600 hover:bg-blue-700 text-white h-11"
              >
                {isLoading ? "Création du compte..." : "Créer mon compte"}
            </Button>

              <p className="text-xs text-gray-500 text-center">
                * Champs obligatoires
              </p>
          </form>
          )}

        </div>
      </Card>
    </div>
  )
}
