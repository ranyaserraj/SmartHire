"use client"

import { Card } from "@/components/ui/card"
import { Briefcase } from "lucide-react"

interface JobOfferSectionProps {
  jobOffer: string
  onJobOfferChange: (offer: string) => void
}

export default function JobOfferSection({ jobOffer, onJobOfferChange }: JobOfferSectionProps) {
  return (
    <Card className="p-6 border border-border flex flex-col">
      <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
        <Briefcase size={20} />
        Offre d'emploi
      </h3>

      <div className="space-y-3 flex flex-col flex-1">
        <div>
          <label className="text-sm text-muted-foreground block mb-2">Collez la description d'offre d'emploi</label>
          <textarea
            value={jobOffer}
            onChange={(e) => onJobOfferChange(e.target.value)}
            placeholder="Collez une offre d'emploi pour analyser..."
            className="w-full flex-1 min-h-64 p-3 bg-background border border-input rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary resize-none"
          />
        </div>

        {jobOffer && (
          <div className="p-3 bg-primary/10 rounded-lg">
            <p className="text-xs text-primary font-medium">{jobOffer.split(/\s+/).length} mots</p>
          </div>
        )}
      </div>
    </Card>
  )
}
