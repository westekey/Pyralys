'use client'

export default function ContentPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Content Library</h1>
        <p className="text-gray-600">
          Manage your posts, drafts, and scheduled content
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <div className="text-6xl mb-4">📝</div>
        <h3 className="text-xl font-semibold mb-2">Coming Soon</h3>
        <p className="text-gray-600">
          Content management will be available in Sprint 4
        </p>
      </div>
    </div>
  )
}
