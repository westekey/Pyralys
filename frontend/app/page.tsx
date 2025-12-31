import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent">
            Pyralys
          </div>
          <nav className="flex items-center gap-6">
            <Link href="/login" className="text-gray-600 hover:text-gray-900">
              Login
            </Link>
            <Button asChild>
              <Link href="/register">Get Started</Link>
            </Button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6">
          Créez du contenu viral en{' '}
          <span className="bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent">
            5 minutes
          </span>
          , pas 5 heures
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Pyralys transforme vos idées en posts Instagram, TikTok et LinkedIn
          magnifiques grâce à l&apos;IA.
        </p>
        <div className="flex gap-4 justify-center">
          <Button size="lg" asChild>
            <Link href="/register">Essayer gratuitement</Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link href="#demo">Voir une démo</Link>
          </Button>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            Tout ce dont vous avez besoin pour dominer les réseaux sociaux
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-semibold mb-2">Génération IA</h3>
              <p className="text-gray-600">
                Du texte aux images en un clic. Notre IA crée du contenu qui
                engage votre audience.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">📅</div>
              <h3 className="text-xl font-semibold mb-2">
                Programmation intelligente
              </h3>
              <p className="text-gray-600">
                Publiez au meilleur moment pour maximiser votre portée et votre
                engagement.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">Analytics prédictifs</h3>
              <p className="text-gray-600">
                Sachez ce qui marchera avant de publier grâce à notre IA
                prédictive.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">
          Prêt à transformer votre présence sur les réseaux sociaux ?
        </h2>
        <p className="text-xl text-gray-600 mb-8">
          Rejoignez des milliers de créateurs qui utilisent Pyralys
        </p>
        <Button size="lg" asChild>
          <Link href="/register">Commencer gratuitement</Link>
        </Button>
      </section>

      {/* Footer */}
      <footer className="border-t bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            © 2025 Pyralys. Tous droits réservés.
          </div>
        </div>
      </footer>
    </div>
  )
}
