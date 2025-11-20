"use client"

import { useState } from "react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import CVUploadSection from "@/components/dashboard/cv-upload"
import JobSearchTabs from "@/components/dashboard/job-search-tabs"
import { Card, CardContent } from "@/components/ui/card"

export default function DashboardPage() {
  const [uploadedCV, setUploadedCV] = useState<File | null>(null)
  const [jobOffer, setJobOffer] = useState("")

  const handleJobSelect = (jobText: string) => {
    setJobOffer(jobText)
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

        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyse de CV</h2>
            <p className="text-gray-600">
              Uploadez votre CV et une offre d'emploi pour obtenir un score de matching
            </p>
          </div>

          <div className="mb-8">
            <CVUploadSection uploadedCV={uploadedCV} onUpload={setUploadedCV} />
          </div>

          <div className="mb-8">
            <JobSearchTabs onJobSelect={handleJobSelect} />
          </div>

          <div className="flex justify-center">
            <button
              onClick={handleAnalyze}
              disabled={!uploadedCV || !jobOffer}
              className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
            >
              Analyser le matching
            </button>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}
