"use client"

import { createContext, useContext, useState, useEffect, ReactNode } from "react"

// Flag pour basculer entre mode mock (frontend seul) et mode API réel
const USE_MOCK_AUTH = false  // Utiliser le vrai backend FastAPI

interface User {
  id: number
  email: string
  nom: string
  prenom: string
  telephone?: string
  ville_preferee?: string
  photo_profil?: string
  salaire_minimum?: number
  type_contrat_prefere?: string
  secteur_activite?: string
  accepte_teletravail?: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (
    email: string, 
    password: string, 
    nom: string, 
    prenom: string, 
    telephone?: string, 
    ville_preferee?: string,
    photo?: File | null
  ) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Vérifier si l'utilisateur est connecté au chargement
    if (USE_MOCK_AUTH) {
      const storedUser = localStorage.getItem("mockUser")
      if (storedUser) {
        setUser(JSON.parse(storedUser))
      }
      setLoading(false)
    } else {
      const token = localStorage.getItem("token")
      if (token) {
        fetchUser(token)
      } else {
        setLoading(false)
      }
    }
  }, [])

  const fetchUser = async (token: string) => {
    try {
      const response = await fetch("http://localhost:8080/api/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      const userData = await response.json()
      setUser(userData)
    } catch (error) {
      console.error(error)
      localStorage.removeItem("token")
    }
    setLoading(false)
  }

  const login = async (email: string, password: string) => {
    if (USE_MOCK_AUTH) {
      // Mode mock - authentification locale
      const storedUsers = localStorage.getItem("mockUsers")
      const users = storedUsers ? JSON.parse(storedUsers) : []
      
      const foundUser = users.find((u: any) => u.email === email && u.password === password)
      
      if (foundUser) {
        const userData = {
          id: foundUser.id,
          email: foundUser.email,
          full_name: foundUser.full_name,
        }
        setUser(userData)
        localStorage.setItem("mockUser", JSON.stringify(userData))
      } else {
        throw new Error("Email ou mot de passe incorrect")
      }
    } else {
      // Mode API réel
      const response = await fetch("http://localhost:8080/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, mot_de_passe: password }),
      })

      if (!response.ok) {
        throw new Error("Email ou mot de passe incorrect")
      }

      const data = await response.json()
      localStorage.setItem("token", data.access_token)
      await fetchUser(data.access_token)
    }
  }

  const register = async (
    email: string, 
    password: string, 
    nom: string, 
    prenom: string, 
    telephone?: string, 
    ville_preferee?: string,
    photo?: File | null
  ) => {
    if (USE_MOCK_AUTH) {
      // Mode mock - enregistrement local
      const storedUsers = localStorage.getItem("mockUsers")
      const users = storedUsers ? JSON.parse(storedUsers) : []
      
      // Vérifier si l'email existe déjà
      if (users.find((u: any) => u.email === email)) {
        throw new Error("Cet email est déjà utilisé")
      }
      
      // Créer le nouvel utilisateur
      const newUser = {
        id: users.length + 1,
        email,
        password,
        nom,
        prenom,
        telephone,
        ville_preferee,
      }
      
      users.push(newUser)
      localStorage.setItem("mockUsers", JSON.stringify(users))
      
      // Connecter automatiquement l'utilisateur
      const userData = {
        id: newUser.id,
        email: newUser.email,
        nom: newUser.nom,
        prenom: newUser.prenom,
        telephone: newUser.telephone,
        ville_preferee: newUser.ville_preferee,
      }
      setUser(userData)
      localStorage.setItem("mockUser", JSON.stringify(userData))
    } else {
      // Mode API réel - Appeler le backend FastAPI
      const response = await fetch("http://localhost:8080/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          mot_de_passe: password,
          nom,
          prenom,
          telephone: telephone || null,
          ville_preferee: ville_preferee || null,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Erreur lors de l'inscription")
      }

      // Connecter automatiquement après l'inscription
      await login(email, password)

      // Si photo fournie, l'uploader
      if (photo) {
        try {
          const token = localStorage.getItem("token")
          if (token) {
            const formData = new FormData()
            formData.append("file", photo)

            await fetch("http://localhost:8080/api/users/photo", {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`,
              },
              body: formData,
            })

            // Recharger les infos utilisateur pour avoir la photo
            await fetchUser(token)
          }
        } catch (error) {
          console.error("Erreur upload photo:", error)
          // Ne pas bloquer l'inscription si l'upload photo échoue
        }
      }
    }
  }

  const logout = () => {
    if (USE_MOCK_AUTH) {
      localStorage.removeItem("mockUser")
    } else {
      localStorage.removeItem("token")
    }
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

