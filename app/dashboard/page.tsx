"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import CVUploadSection from "@/components/dashboard/cv-upload"
import CVVerificationForm from "@/components/dashboard/cv-verification-form"
import JobSearchTabs from "@/components/dashboard/job-search-tabs"
import { Card, CardContent } from "@/components/ui/card"
import { toast } from "sonner"

export default function DashboardPage() {
  const [uploadedCV, setUploadedCV] = useState<File | null>(null)
  const [jobOffer, setJobOffer] = useState("")
  const [showVerificationForm, setShowVerificationForm] = useState(false)
  const [cvData, setCvData] = useState<any>(null)
  const [isUploading, setIsUploading] = useState(false)

  const handleJobSelect = (jobText: string) => {
    setJobOffer(jobText)
  }

  const handleCVUpload = async (file: File) => {
    setUploadedCV(file)
    setIsUploading(true)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch("http://localhost:8080/api/cvs/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Erreur lors de l'upload du CV")
      }

      const data = await response.json()
      setCvData(data)
      setShowVerificationForm(true)
      toast.success("✅ CV uploadé avec succès! Veuillez vérifier les informations.")
    } catch (error) {
      console.error("Error uploading CV:", error)
      toast.error("❌ Erreur lors de l'upload du CV")
      setUploadedCV(null)
    } finally {
      setIsUploading(false)
    }
  }

  const handleVerificationSubmit = async (verifiedData: any) => {
    try {
      const response = await fetch(`http://localhost:8080/api/cvs/${cvData.id}/update-data`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(verifiedData),
      })

      if (!response.ok) {
        throw new Error("Erreur lors de la mise à jour des données")
      }

      setShowVerificationForm(false)
      toast.success("✅ CV enregistré avec succès!")
    } catch (error) {
      console.error("Error updating CV data:", error)
      throw error
    }
  }

  const handleCancelVerification = () => {
    setShowVerificationForm(false)
    setUploadedCV(null)
    setCvData(null)
  }

  const stats = [
    { label: "CVs analysés", value: "24" },
    { label: "Meilleur score", value: "92%" },
    { label: "Analyses ce mois", value: "8" },
  ]

  const handleAnalyze = () => {
    if (uploadedCV && jobOffer) {
      window.location.href = "/results"
    }
  }

  return (
    <ProtectedRoute>
      <DashboardLayout>
        {/* Stats */}
        {!showVerificationForm && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {stats.map((stat, index) => (
              <Card key={index}>
                <CardContent className="p-6">
                  <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        <div className="max-w-7xl mx-auto">
          {showVerificationForm && cvData ? (
            // Formulaire de vérification des données extraites
            <div className="py-8">
              <CVVerificationForm
                cvId={cvData.id}
                extractedData={cvData.extracted_data}
                onSubmit={handleVerificationSubmit}
                onCancel={handleCancelVerification}
              />
            </div>
          ) : (
            // Interface normale d'analyse de CV
            <>
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyse de CV</h2>
                <p className="text-gray-600">
                  Uploadez votre CV et une offre d'emploi pour obtenir un score de matching
                </p>
              </div>

              <div className="mb-8">
                <CVUploadSection 
                  uploadedCV={uploadedCV} 
                  onUpload={handleCVUpload}
                  isUploading={isUploading}
                />
              </div>

              <div className="mb-8">
                <JobSearchTabs onJobSelect={handleJobSelect} />
              </div>

              <div className="flex justify-center">
                <button
                  onClick={handleAnalyze}
                  disabled={!uploadedCV || !jobOffer || showVerificationForm}
                  className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
                >
                  Analyser le matching
                </button>
              </div>
            </>
          )}
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}
