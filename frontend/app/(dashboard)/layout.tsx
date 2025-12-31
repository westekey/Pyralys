'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuthStore } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const { isAuthenticated, user, logout } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link
              href="/dashboard"
              className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent"
            >
              Pyralys
            </Link>
            <nav className="hidden md:flex items-center gap-6">
              <Link
                href="/dashboard"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/dashboard/generate"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                AI Generate
              </Link>
              <Link
                href="/dashboard/content"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                Content
              </Link>
              <Link
                href="/dashboard/analytics"
                className="text-gray-600 hover:text-gray-900 transition-colors"
              >
                Analytics
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-sm text-gray-600">
              {user?.full_name}
              <span className="ml-2 px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs font-medium">
                {user?.plan_type}
              </span>
            </div>
            <Button variant="outline" size="sm" onClick={logout}>
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  )
}
