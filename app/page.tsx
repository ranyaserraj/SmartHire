"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Upload, Briefcase, Zap, FileText, CheckCircle, ArrowRight } from "lucide-react"
import Navbar from "@/components/navbar"
import Footer from "@/components/footer"
import { useEffect, useState } from "react"
import HeroAnimation from "@/components/hero-animation"

export default function HomePage() {
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const features = [
    {
      icon: Upload,
      title: "Upload CV",
      description: "Upload your CV in PDF or image format",
      gradient: "from-blue-400 to-blue-600",
    },
    {
      icon: Briefcase,
      title: "Analyse d'offres",
      description: "Paste a job description for analysis",
      gradient: "from-purple-400 to-purple-600",
    },
    {
      icon: Zap,
      title: "Score de matching",
      description: "Get instant compatibility scores",
      gradient: "from-cyan-400 to-cyan-600",
    },
    {
      icon: FileText,
      title: "Lettre de motivation",
      description: "Generate tailored cover letters",
      gradient: "from-blue-400 to-purple-600",
    },
  ]

  const steps = [
    {
      number: 1,
      title: "Téléchargez votre CV",
      description: "Importez votre CV en PDF ou image",
      icon: Upload,
    },
    {
      number: 2,
      title: "Collez l'offre d'emploi",
      description: "Insérez la description du poste",
      icon: Briefcase,
    },
    {
      number: 3,
      title: "Obtenez votre score",
      description: "Analyse complète en secondes",
      icon: Zap,
    },
  ]

  const stats = [
    { label: "Taux de matching", value: "95%" },
    { label: "CV analysés", value: "10K+" },
    { label: "Utilisateurs satisfaits", value: "2K+" },
    { label: "Lettres générées", value: "50K+" },
  ]

  return (
    <div className="min-h-screen bg-background smooth-scroll">
      <Navbar />

      <section id="hero" className="relative overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 dots-pattern opacity-40" />
        <div
          className="absolute inset-0 bg-gradient-to-br from-blue-400 via-purple-400 to-cyan-400 opacity-20 blur-3xl animate-gradient"
          style={{
            backgroundSize: "200% 200%",
          }}
        />

        <div className="relative px-6 py-20 md:py-32 lg:py-40 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Text Content */}
            <div className="space-y-8 z-10">
              <div>
                <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent text-balance">
                  Trouvez votre emploi idéal avec l'IA
                </h1>
              </div>

              <p className="text-lg md:text-xl text-muted-foreground max-w-2xl text-pretty leading-relaxed">
                SmartHire analyse votre CV et compare-le avec les offres d'emploi pour vous montrer le meilleur matching
                possible. Optimisez vos candidatures en temps réel.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Link href="/auth">
                  <Button
                    size="lg"
                    className="w-full sm:w-auto bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white border-0 group relative overflow-hidden"
                  >
                    <span className="relative z-10 flex items-center gap-2">
                      Commencer maintenant
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </span>
                    <span className="absolute inset-0 bg-gradient-to-r from-purple-600 to-cyan-600 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </Button>
                </Link>
                <Button
                  size="lg"
                  variant="outline"
                  className="w-full sm:w-auto glass hover:glass-dark transition-all duration-300 bg-transparent"
                >
                  En savoir plus
                </Button>
              </div>

              {/* Trust badges */}
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                {["Analyse IA rapide", "100% sécurisé", "Gratuit pour commencer"].map((badge, i) => (
                  <div key={i} className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-cyan-500" />
                    <span className="text-foreground/80">{badge}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* 3D Animation */}
            <div className="hidden lg:flex items-center justify-center">
              <HeroAnimation />
            </div>
          </div>
        </div>
      </section>

      <section className="px-6 py-20 md:py-32 bg-muted/50 relative overflow-hidden">
        <div className="absolute inset-0 dots-pattern opacity-20" />
        <div className="relative max-w-7xl mx-auto">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">Comment ça marche</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Trois étapes simples pour trouver votre meilleure correspondance d'emploi
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 stagger-in">
            {steps.map((step) => {
              const Icon = step.icon
              return (
                <div key={step.number} className="relative group">
                  {/* Gradient background */}
                  <div className="absolute -inset-0.5 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl opacity-0 group-hover:opacity-100 blur transition-all duration-500" />

                  <div className="relative bg-background p-8 rounded-2xl border border-border group-hover:border-primary/50 transition-all duration-300">
                    {/* Number badge */}
                    <div className="absolute -top-4 -left-4 w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {step.number}
                    </div>

                    <div className="space-y-4">
                      <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-400/20 to-purple-400/20 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                        <Icon className="w-8 h-8 text-primary" />
                      </div>
                      <h3 className="text-xl font-semibold text-foreground">{step.title}</h3>
                      <p className="text-muted-foreground leading-relaxed">{step.description}</p>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      <section id="features" className="px-6 py-20 md:py-32 max-w-7xl mx-auto">
        <div className="text-center mb-16 space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground">Fonctionnalités principales</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Outils puissants pour optimiser vos candidatures
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 stagger-in">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div key={index} className="group relative">
                {/* Gradient border */}
                <div className="absolute -inset-0.5 bg-gradient-to-br from-blue-600 via-purple-600 to-cyan-600 rounded-2xl opacity-0 group-hover:opacity-100 blur transition-all duration-500" />

                {/* Glass card */}
                <div className="relative glass rounded-2xl p-8 h-full transition-all duration-300 hover:backdrop-blur-lg group-hover:glass-dark">
                  <div className="space-y-4">
                    {/* Icon with gradient background */}
                    <div
                      className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}
                    >
                      <Icon className="w-7 h-7 text-white" />
                    </div>

                    <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>

                    {/* Arrow indicator */}
                    <div className="pt-4">
                      <ArrowRight className="w-5 h-5 text-primary opacity-0 group-hover:opacity-100 group-hover:translate-x-2 transition-all duration-300" />
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </section>

      <section
        className="px-6 py-20 md:py-32 relative overflow-hidden"
        style={{
          backgroundPosition: `0 ${scrollY * 0.5}px`,
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-purple-600/10 to-cyan-600/10 dots-pattern" />

        <div className="relative max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center space-y-2 stagger-in">
                <p className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  {stat.value}
                </p>
                <p className="text-sm md:text-base text-muted-foreground">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-6 py-20 md:py-32 max-w-4xl mx-auto text-center space-y-8">
        <div className="space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground text-balance">
            Prêt à optimiser vos candidatures?
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Rejoignez les milliers d'utilisateurs qui trouvent leurs emplois avec SmartHire
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link href="/auth">
            <Button
              size="lg"
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white border-0 group relative overflow-hidden"
            >
              <span className="relative z-10 flex items-center gap-2">
                Démarrer maintenant
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </span>
            </Button>
          </Link>
          <Button size="lg" variant="outline" className="glass bg-transparent">
            Voir la démo
          </Button>
        </div>

        {/* Decorative gradient orbs */}
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full blur-3xl opacity-20 pointer-events-none" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-full blur-3xl opacity-20 pointer-events-none" />
      </section>

      <div id="about">
        <Footer />
      </div>
    </div>
  )
}
