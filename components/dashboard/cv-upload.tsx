"use client"

import type React from "react"

import { Upload, Loader2 } from "lucide-react"
import { Card } from "@/components/ui/card"
import { useRef } from "react"

interface CVUploadSectionProps {
  uploadedCV: File | null
  onUpload: (file: File) => void
  isUploading?: boolean
}

export default function CVUploadSection({ uploadedCV, onUpload, isUploading = false }: CVUploadSectionProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()

    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      if (file.type === "application/pdf" || file.type.startsWith("image/")) {
        onUpload(file)
      }
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onUpload(e.target.files[0])
    }
  }

  return (
    <Card className="p-6 border border-border">
      <h3 className="text-lg font-semibold text-foreground mb-4">Upload CV</h3>

      <div
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`border-2 border-dashed border-border rounded-lg p-8 text-center transition-colors ${
          isUploading ? "opacity-50 cursor-not-allowed" : "hover:border-primary/50 cursor-pointer"
        }`}
        onClick={() => !isUploading && fileInputRef.current?.click()}
      >
        <input 
          ref={fileInputRef} 
          type="file" 
          accept=".pdf,image/*" 
          onChange={handleFileSelect} 
          className="hidden"
          disabled={isUploading}
        />

        {isUploading ? (
          <>
            <Loader2 className="w-12 h-12 text-primary mx-auto mb-3 animate-spin" />
            <p className="text-foreground font-medium mb-1">Extraction des données en cours...</p>
            <p className="text-sm text-muted-foreground">Veuillez patienter</p>
          </>
        ) : (
          <>
            <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
            <p className="text-foreground font-medium mb-1">Déposez votre CV ici</p>
            <p className="text-sm text-muted-foreground">ou cliquez pour sélectionner (PDF ou Image)</p>
          </>
        )}

        {uploadedCV && !isUploading && (
          <div className="mt-4 p-3 bg-primary/10 rounded-lg">
            <p className="text-sm text-primary font-medium">{uploadedCV.name}</p>
          </div>
        )}
      </div>
    </Card>
  )
}
