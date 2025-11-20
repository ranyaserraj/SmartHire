"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import {
  ArrowLeft,
  Copy,
  Download,
  RotateCcw,
  Check,
  Lightbulb,
  Mail,
  Edit,
  Target,
  HelpCircle,
  ChevronDown
} from "lucide-react"
import { DashboardLayout } from "@/components/layouts/DashboardLayout"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import { toast } from "sonner"

const letterData = {
  candidateName: "Ranya SERRAJ ANDALOUSSI",
  candidateAddress: "Hay Riad, Rabat",
  candidatePhone: "+212 6XX XX XX XX",
  candidateEmail: "ranya.serraj@email.com",
  companyName: "TechVision Solutions",
  companyCity: "Casablanca",
  jobTitle: "Développeur Full Stack",
  jobSource: "Rekrute.com",
  matchingSkills: ["React.js", "Node.js", "PostgreSQL", "Git"],
  missingSkills: ["Docker", "CI/CD"],
  currentSituation: "étudiante en dernière année à l'ENSIAS",
  relevantProject: "SmartHire, une plateforme d'analyse de CV intégrant FastAPI, Next.js et des techniques d'IA",
}

const generateLetter = (tone = "formal") => {
  const today = new Date()
  const dateStr = `${today.getDate()} novembre ${today.getFullYear()}`

  let intro = ""
  let motivation = ""

  if (tone === "formal") {
    intro = `Actuellement ${letterData.currentSituation}, je me permets de vous adresser ma candidature pour le poste de ${letterData.jobTitle} au sein de ${letterData.companyName}.`
    motivation = `Votre offre a particulièrement retenu mon attention car elle combine développement technique et innovation, dans un environnement dynamique qui correspond parfaitement à mes aspirations professionnelles.`
  } else if (tone === "dynamic") {
    intro = `Passionnée par les technologies innovantes et enthousiaste à l'idée de relever de nouveaux défis, je suis ravie de soumettre ma candidature pour le poste de ${letterData.jobTitle} chez ${letterData.companyName}.`
    motivation = `Je suis particulièrement attirée par votre entreprise pour son approche novatrice et son engagement envers l'excellence technique.`
  } else {
    intro = `En tant que développeuse créative et curieuse, j'ai toujours cherché une opportunité comme celle-ci. Je suis donc enthousiaste de candidater au poste de ${letterData.jobTitle} au sein de ${letterData.companyName}.`
    motivation = `Votre entreprise représente exactement le type d'environnement où je souhaite évoluer : innovant, dynamique, et axé sur la qualité technique.`
  }

  return `${letterData.candidateName}
${letterData.candidateAddress}
${letterData.candidatePhone} | ${letterData.candidateEmail}

${letterData.companyCity}, le ${dateStr}

À l'attention du Service Recrutement
${letterData.companyName}
${letterData.companyCity}, Maroc

Objet : Candidature au poste de ${letterData.jobTitle}

Madame, Monsieur,

${intro}

Mon parcours académique et mes expériences de projets m'ont permis de développer une solide expertise en développement web moderne. J'ai notamment travaillé sur des projets utilisant ${letterData.matchingSkills.join(", ")}, technologies que vous recherchez pour ce poste. Mon projet actuel, ${letterData.relevantProject}, démontre ma capacité à mener un projet Full Stack de bout en bout.

${motivation} Je suis convaincue que mes compétences en ${letterData.matchingSkills.slice(0, 3).join(", ")} me permettront de contribuer efficacement à vos projets dès mon arrivée.

Concernant les compétences que je n'ai pas encore maîtrisées comme ${letterData.missingSkills.join(" et ")}, je suis actuellement en train de me former et je suis déterminée à les acquérir rapidement grâce à votre accompagnement.

Je serais ravie de vous rencontrer pour échanger sur ma candidature et vous démontrer ma motivation à rejoindre votre équipe.

Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

${letterData.candidateName}`
}

const emailData = {
  subject: `Candidature au poste de ${letterData.jobTitle} - ${letterData.candidateName}`,
  content: `Madame, Monsieur,

Je me permets de vous adresser ma candidature pour le poste de ${letterData.jobTitle} au sein de ${letterData.companyName}, dont j'ai pris connaissance sur ${letterData.jobSource}.

Diplômée de l'ENSIAS et forte d'une expérience en développement web, je suis particulièrement intéressée par votre offre qui correspond parfaitement à mon profil et à mes aspirations professionnelles.

Vous trouverez ci-joint mon CV ainsi qu'une lettre de motivation détaillant mes compétences et ma motivation pour rejoindre vos équipes.

Je reste à votre disposition pour un entretien à votre convenance afin d'échanger sur ma candidature.

Dans l'attente de votre retour, je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.

Cordialement,
${letterData.candidateName}
${letterData.candidatePhone}
${letterData.candidateEmail}`,
}

const interviewQuestions = [
  {
    id: 1,
    question: "Parlez-moi de vous et de votre parcours",
    type: "generale",
    suggestedAnswer:
      "Je suis actuellement étudiante en dernière année à l'ENSIAS, spécialisée en développement web. J'ai développé une forte expertise en JavaScript, React et Node.js à travers plusieurs projets académiques et personnels, notamment SmartHire, une plateforme d'analyse de CV intégrant de l'intelligence artificielle.",
    tips: "Restez concis (2-3 minutes max), mettez en avant vos compétences liées au poste",
  },
  {
    id: 2,
    question: "Pourquoi ce poste vous intéresse-t-il ?",
    type: "generale",
    suggestedAnswer: `Ce poste de ${letterData.jobTitle} chez ${letterData.companyName} m'intéresse particulièrement car il combine développement technique et innovation, deux aspects qui me passionnent. De plus, les technologies mentionnées (React, Node.js, PostgreSQL) correspondent exactement à mon domaine d'expertise.`,
    tips: "Personnalisez votre réponse en mentionnant des éléments spécifiques de l'offre",
  },
  {
    id: 3,
    question: "Quelle est votre expérience avec React et Node.js ?",
    type: "technique",
    suggestedAnswer:
      "J'ai travaillé avec React pendant 2 ans sur plusieurs projets, notamment SmartHire où j'ai développé l'interface utilisateur complète avec Next.js et React. Côté backend, j'ai utilisé Node.js avec Express pour créer des APIs RESTful. Je maîtrise également les hooks React, le state management avec Context API, et l'intégration d'APIs.",
    tips: "Donnez des exemples concrets de projets où vous avez utilisé ces technologies",
  },
  {
    id: 4,
    question: "Comment gérez-vous le travail en équipe ?",
    type: "generale",
    suggestedAnswer:
      "Je privilégie la communication transparente et les méthodologies agiles. J'ai l'habitude d'utiliser Git pour le versioning collaboratif, de participer à des code reviews, et de documenter mon code pour faciliter le travail d'équipe. Je suis également à l'aise avec les stand-ups quotidiens et les sprints.",
    tips: "Mettez en avant vos soft skills et donnez des exemples concrets",
  },
  {
    id: 5,
    question: "Vous n'avez pas d'expérience avec Docker. Comment comptez-vous l'acquérir ?",
    type: "technique",
    suggestedAnswer:
      "C'est exact, je n'ai pas encore eu l'occasion de travailler avec Docker en production, mais j'ai commencé à me former via des tutoriels en ligne et de la documentation officielle. Je suis une apprenante rapide et motivée, et je serais ravie d'approfondir cette compétence dans un cadre professionnel avec l'accompagnement de l'équipe.",
    tips: "Montrez votre volonté d'apprendre et votre proactivité",
  },
  {
    id: 6,
    question: "Quelle est votre plus grande réalisation professionnelle ou académique ?",
    type: "generale",
    suggestedAnswer:
      "Mon projet SmartHire est ma plus grande réalisation. J'ai développé de A à Z une plateforme d'analyse de CV intégrant du web scraping, du text mining avec spaCy, du machine learning pour les recommandations, et une interface utilisateur moderne avec Next.js. Ce projet m'a permis de démontrer ma capacité à mener un projet complexe de bout en bout.",
    tips: "Choisissez un projet pertinent pour le poste et quantifiez les résultats si possible",
  },
  {
    id: 7,
    question: "Comment restez-vous à jour avec les nouvelles technologies ?",
    type: "generale",
    suggestedAnswer:
      "Je suis plusieurs blogs techniques (Dev.to, Medium), je participe à des communautés en ligne, et je réalise régulièrement des projets personnels pour expérimenter de nouvelles technologies. Par exemple, pour SmartHire, j'ai appris à utiliser Sentence-BERT et FastAPI qui étaient nouveaux pour moi.",
    tips: "Montrez votre curiosité et votre passion pour la technologie",
  },
  {
    id: 8,
    question: "Quels sont vos points forts et vos axes d'amélioration ?",
    type: "generale",
    suggestedAnswer:
      "Mes points forts sont ma capacité d'apprentissage rapide, ma rigueur dans le code, et ma capacité à comprendre les besoins métier pour les traduire en solutions techniques. Concernant mes axes d'amélioration, je souhaite développer davantage mes compétences en architecture système et en optimisation de performances.",
    tips: "Soyez honnête mais positif, et montrez que vous travaillez sur vos axes d'amélioration",
  },
]

const questionsToAsk = [
  {
    question: "Quels sont les projets prioritaires pour ce poste dans les 6 premiers mois ?",
    rationale: "Montre votre volonté de vous projeter dans le poste",
  },
  {
    question: "Comment est organisée l'équipe technique ?",
    rationale: "Démontre votre intérêt pour la collaboration",
  },
  {
    question: "Quelles sont les opportunités d'évolution et de formation ?",
    rationale: "Montre votre ambition et votre volonté de progresser",
  },
  {
    question: "Quelle est la stack technique utilisée au quotidien ?",
    rationale: "Pertinent pour un poste technique",
  },
  {
    question: "Quelles sont les prochaines étapes du processus de recrutement ?",
    rationale: "Question pratique pour conclure l'entretien",
  },
]

function MotivationLetterPage() {
  const [selectedVersion, setSelectedVersion] = useState<"formal" | "dynamic" | "creative">("formal")
  const [letter, setLetter] = useState(() => generateLetter("formal"))
  const [isEditing, setIsEditing] = useState(false)
  const [isEmailEditing, setIsEmailEditing] = useState(false)
  const [isInterviewOpen, setIsInterviewOpen] = useState(false)

  const handleVersionChange = (version: "formal" | "dynamic" | "creative") => {
    setSelectedVersion(version)
    setLetter(generateLetter(version))
  }

  const handleCopyLetter = () => {
    navigator.clipboard.writeText(letter)
    toast.success("Lettre copiée dans le presse-papier !")
  }

  const handleCopyEmail = () => {
    const fullEmail = `Objet: ${emailData.subject}\n\n${emailData.content}`
    navigator.clipboard.writeText(fullEmail)
    toast.success("Email copié dans le presse-papier !")
  }

  const handleDownloadPDF = () => {
    toast.info("Téléchargement du PDF en cours...")
  }

  const handleRegenerate = () => {
    setLetter(generateLetter(selectedVersion))
    toast.success("Lettre régénérée avec succès !")
  }

  const matchingScore = 85

  return (
    <ProtectedRoute>
      <DashboardLayout>
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <Link
              href="/results"
              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4 transition-colors"
            >
              <ArrowLeft className="h-4 w-4" />
              Retour aux résultats
            </Link>
            <div className="flex items-start justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{letterData.jobTitle}</h1>
                <p className="text-gray-600 mt-2">Lettre de motivation pour {letterData.companyName}</p>
              </div>
              <Badge className="bg-green-100 text-green-700 border-green-300">
                {matchingScore}% de matching
              </Badge>
            </div>
          </div>

          {/* Version Selector */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Sélectionnez une version</CardTitle>
              <CardDescription>Choisissez le ton de votre lettre de motivation</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { value: "formal", label: "Version Formelle", desc: "Professionnelle et classique" },
                  { value: "dynamic", label: "Version Dynamique", desc: "Énergique et moderne" },
                  { value: "creative", label: "Version Créative", desc: "Originale et audacieuse" },
                ].map((version) => (
                  <button
                    key={version.value}
                    onClick={() => handleVersionChange(version.value as any)}
                    className={`p-4 rounded-lg border-2 transition-all text-left ${
                      selectedVersion === version.value
                        ? "border-blue-600 bg-blue-50"
                        : "border-gray-200 hover:border-gray-300"
                    }`}
                  >
                    <h4 className="font-semibold text-gray-900 mb-1">{version.label}</h4>
                    <p className="text-sm text-gray-600">{version.desc}</p>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Letter Content */}
          <Card className="mb-8">
            <CardContent className="p-8">
              {isEditing ? (
                <textarea
                  value={letter}
                  onChange={(e) => setLetter(e.target.value)}
                  className="w-full h-96 p-4 border border-gray-300 rounded-lg font-serif text-sm leading-relaxed focus:outline-none focus:ring-2 focus:ring-blue-600 resize-none"
                />
              ) : (
                <div className="whitespace-pre-wrap font-serif text-sm leading-relaxed text-justify">
                  {letter}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3 mb-12">
            <Button onClick={() => setIsEditing(!isEditing)} variant={isEditing ? "default" : "outline"}>
              <Edit className="mr-2 h-4 w-4" />
              {isEditing ? "Terminé" : "Modifier"}
            </Button>
            <Button onClick={handleCopyLetter} variant="outline">
              <Copy className="mr-2 h-4 w-4" />
              Copier le texte
            </Button>
            <Button onClick={handleDownloadPDF} variant="outline">
              <Download className="mr-2 h-4 w-4" />
              Télécharger PDF
            </Button>
            <Button onClick={handleRegenerate} variant="outline">
              <RotateCcw className="mr-2 h-4 w-4" />
              Régénérer
            </Button>
          </div>

          <Separator className="my-12" />

          {/* Email Section */}
          <Card className="mb-12 bg-blue-50 border-blue-200">
            <CardHeader>
              <div className="flex items-center gap-3">
                <div className="p-3 bg-blue-500 rounded-lg">
                  <Mail className="h-6 w-6 text-white" />
                </div>
                <div>
                  <CardTitle>📧 Email d'accompagnement pré-rempli</CardTitle>
                  <CardDescription>Copiez cet email pour envoyer votre candidature</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-white rounded-lg p-6 space-y-4 mb-4">
                <div>
                  <label className="text-sm font-semibold text-gray-700">Objet :</label>
                  <p className="text-gray-900 mt-1">{emailData.subject}</p>
                </div>
                <Separator />
                <div className="text-gray-800 leading-relaxed whitespace-pre-line">{emailData.content}</div>
              </div>

              <div className="flex gap-3">
                <Button onClick={handleCopyEmail} className="flex-1">
                  <Copy className="mr-2 h-4 w-4" />
                  Copier l'email
                </Button>
                <Button variant="outline" onClick={() => setIsEmailEditing(true)}>
                  <Edit className="mr-2 h-4 w-4" />
                  Modifier
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Interview Preparation */}
          <Card className="mb-12">
            <button
              onClick={() => setIsInterviewOpen(!isInterviewOpen)}
              className="w-full p-6 flex items-center justify-between hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className="p-3 bg-purple-500 rounded-lg">
                  <Target className="h-6 w-6 text-white" />
                </div>
                <div className="text-left">
                  <h3 className="text-xl font-bold text-gray-900">🎯 Préparez votre entretien</h3>
                  <p className="text-gray-600 text-sm mt-1">
                    Questions probables et suggestions de réponses basées sur votre profil
                  </p>
                </div>
              </div>
              <ChevronDown className={`h-5 w-5 transition-transform ${isInterviewOpen ? "rotate-180" : ""}`} />
            </button>

            {isInterviewOpen && (
              <div className="p-6 pt-0 space-y-6">
                <Separator />

                {/* Questions probables */}
                <div>
                  <h4 className="text-lg font-bold text-gray-900 mb-4">Questions Probables</h4>
                  <Accordion type="single" collapsible className="space-y-3">
                    {interviewQuestions.map((q, index) => (
                      <AccordionItem key={q.id} value={`item-${q.id}`} className="border rounded-lg">
                        <AccordionTrigger className="px-4 py-3 hover:bg-gray-50">
                          <div className="flex items-start gap-3 text-left">
                            <div className="flex-shrink-0 w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                              <span className="text-purple-600 font-semibold text-sm">{index + 1}</span>
                            </div>
                            <div className="flex-1">
                              <p className="font-medium text-gray-900">{q.question}</p>
                              <Badge variant="outline" className="mt-1">
                                {q.type === "technique" ? "💻 Technique" : "🎯 Générale"}
                              </Badge>
                            </div>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent className="px-4 pb-4">
                          <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded mb-3">
                            <p className="text-sm font-semibold text-green-800 mb-2">💡 Suggestion de réponse :</p>
                            <p className="text-gray-700 leading-relaxed">{q.suggestedAnswer}</p>
                          </div>
                          {q.tips && (
                            <div className="p-3 bg-blue-50 rounded-lg">
                              <p className="text-sm font-semibold text-blue-800 mb-1">📌 Conseil :</p>
                              <p className="text-sm text-gray-700">{q.tips}</p>
                            </div>
                          )}
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </div>

                <Separator />

                {/* Questions à poser */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
                  <h4 className="text-lg font-bold mb-3 flex items-center gap-2">
                    <HelpCircle className="h-5 w-5 text-blue-600" />
                    Questions intelligentes à poser au recruteur
                  </h4>
                  <p className="text-gray-600 text-sm mb-4">
                    Montrez votre intérêt en posant des questions pertinentes
                  </p>
                  <ul className="space-y-3">
                    {questionsToAsk.map((q, index) => (
                      <li key={index} className="flex items-start gap-3">
                        <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                          <Check className="h-4 w-4 text-white" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{q.question}</p>
                          <p className="text-sm text-gray-600 mt-1">{q.rationale}</p>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </Card>

          {/* Navigation Buttons */}
          <div className="flex justify-center gap-4 mb-8">
            <Link href="/results">
              <Button variant="outline">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Retour aux résultats
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button>Nouvelle analyse</Button>
            </Link>
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  )
}

export default MotivationLetterPage
