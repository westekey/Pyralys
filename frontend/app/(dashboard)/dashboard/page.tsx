'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Welcome to Pyralys</h1>
        <p className="text-gray-600">
          Start creating amazing social media content with AI
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-6">
        <Link
          href="/dashboard/generate"
          className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
        >
          <div className="text-4xl mb-4">✨</div>
          <h3 className="text-xl font-semibold mb-2">AI Generate</h3>
          <p className="text-gray-600 mb-4">
            Create captions and images with AI
          </p>
          <Button className="w-full">Start Creating</Button>
        </Link>

        <Link
          href="/dashboard/content"
          className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
        >
          <div className="text-4xl mb-4">📝</div>
          <h3 className="text-xl font-semibold mb-2">Content Library</h3>
          <p className="text-gray-600 mb-4">Manage your posts and drafts</p>
          <Button variant="outline" className="w-full">
            View Content
          </Button>
        </Link>

        <Link
          href="/dashboard/analytics"
          className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
        >
          <div className="text-4xl mb-4">📊</div>
          <h3 className="text-xl font-semibold mb-2">Analytics</h3>
          <p className="text-gray-600 mb-4">Track your performance</p>
          <Button variant="outline" className="w-full">
            View Stats
          </Button>
        </Link>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
        <p className="text-gray-600">No recent activity yet. Start creating!</p>
      </div>
    </div>
  )
}
