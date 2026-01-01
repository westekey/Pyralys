'use client'

import { useState, useEffect } from 'react'
import { Post, PostCreate } from '@/lib/types'
import { postsApi } from '@/lib/posts'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export default function ContentPage() {
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [showCreateModal, setShowCreateModal] = useState(false)

  useEffect(() => {
    loadPosts()
  }, [statusFilter])

  const loadPosts = async () => {
    try {
      setLoading(true)
      const params = statusFilter !== 'all' ? { status: statusFilter } : {}
      const data = await postsApi.list(params)
      setPosts(data)
    } catch (error) {
      console.error('Error loading posts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (postId: string) => {
    if (!confirm('Are you sure you want to delete this post?')) return

    try {
      await postsApi.delete(postId)
      setPosts(posts.filter(p => p.id !== postId))
    } catch (error) {
      console.error('Error deleting post:', error)
      alert('Failed to delete post')
    }
  }

  const filteredPosts = searchQuery
    ? posts.filter(post =>
        post.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.caption?.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : posts

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800'
      case 'scheduled':
        return 'bg-blue-100 text-blue-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPostTypeIcon = (type: string) => {
    switch (type) {
      case 'photo':
        return '📷'
      case 'video':
        return '🎥'
      case 'carousel':
        return '🖼️'
      case 'story':
        return '⚡'
      default:
        return '📝'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2">Content Library</h1>
          <p className="text-gray-600">
            Manage your posts, drafts, and scheduled content
          </p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          + New Post
        </Button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm p-4 space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <Input
              type="text"
              placeholder="Search posts..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full"
            />
          </div>

          {/* Status filter */}
          <div className="flex gap-2 flex-wrap">
            {['all', 'draft', 'scheduled', 'published', 'failed'].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  statusFilter === status
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Posts Grid */}
      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Loading posts...</p>
        </div>
      ) : filteredPosts.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold mb-2">No posts found</h3>
          <p className="text-gray-600 mb-4">
            {searchQuery
              ? 'Try adjusting your search or filters'
              : 'Get started by creating your first post'}
          </p>
          <Button onClick={() => setShowCreateModal(true)}>
            Create Post
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPosts.map((post) => (
            <PostCard
              key={post.id}
              post={post}
              onDelete={handleDelete}
              onRefresh={loadPosts}
            />
          ))}
        </div>
      )}

      {/* Create Post Modal */}
      {showCreateModal && (
        <CreatePostModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            setShowCreateModal(false)
            loadPosts()
          }}
        />
      )}
    </div>
  )
}

// PostCard Component
function PostCard({
  post,
  onDelete,
  onRefresh
}: {
  post: Post
  onDelete: (id: string) => void
  onRefresh: () => void
}) {
  const [showActions, setShowActions] = useState(false)

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800'
      case 'scheduled':
        return 'bg-blue-100 text-blue-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPostTypeIcon = (type: string) => {
    switch (type) {
      case 'photo':
        return '📷'
      case 'video':
        return '🎥'
      case 'carousel':
        return '🖼️'
      case 'story':
        return '⚡'
      default:
        return '📝'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      {/* Media Preview */}
      {post.media_urls && post.media_urls.length > 0 ? (
        <div className="aspect-video bg-gray-100 relative">
          <img
            src={post.media_urls[0]}
            alt={post.title || 'Post image'}
            className="w-full h-full object-cover"
          />
          {post.media_urls.length > 1 && (
            <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
              +{post.media_urls.length - 1} more
            </div>
          )}
        </div>
      ) : (
        <div className="aspect-video bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
          <span className="text-6xl">{getPostTypeIcon(post.post_type)}</span>
        </div>
      )}

      {/* Content */}
      <div className="p-4">
        {/* Status Badge */}
        <div className="flex items-center justify-between mb-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(post.status)}`}>
            {post.status}
          </span>
          <span className="text-xs text-gray-500">
            {getPostTypeIcon(post.post_type)} {post.post_type}
          </span>
        </div>

        {/* Title/Caption */}
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">
          {post.title || 'Untitled Post'}
        </h3>
        {post.caption && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-3">
            {post.caption}
          </p>
        )}

        {/* Platforms */}
        {post.target_platforms && post.target_platforms.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {post.target_platforms.map((platform) => (
              <span
                key={platform}
                className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
              >
                {platform}
              </span>
            ))}
          </div>
        )}

        {/* Hashtags */}
        {post.hashtags && post.hashtags.length > 0 && (
          <div className="text-xs text-blue-600 mb-3">
            {post.hashtags.slice(0, 3).join(' ')}
            {post.hashtags.length > 3 && ' ...'}
          </div>
        )}

        {/* Meta */}
        <div className="text-xs text-gray-500 mb-3">
          {post.ai_generated && <span className="mr-2">🤖 AI Generated</span>}
          {post.scheduled_at && (
            <span>📅 {new Date(post.scheduled_at).toLocaleDateString()}</span>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <Button
            size="sm"
            variant="outline"
            className="flex-1"
            onClick={() => alert('Edit functionality coming soon!')}
          >
            Edit
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => alert('Publish functionality will be added in Sprint 5!')}
          >
            Publish
          </Button>
          <Button
            size="sm"
            variant="destructive"
            onClick={() => onDelete(post.id)}
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  )
}

// CreatePostModal Component
function CreatePostModal({
  onClose,
  onSuccess
}: {
  onClose: () => void
  onSuccess: () => void
}) {
  const [formData, setFormData] = useState<PostCreate>({
    title: '',
    caption: '',
    hashtags: [],
    post_type: 'photo',
    target_platforms: [],
    ai_generated: false
  })
  const [hashtagInput, setHashtagInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      setLoading(true)
      await postsApi.create(formData)
      onSuccess()
    } catch (error) {
      console.error('Error creating post:', error)
      alert('Failed to create post')
    } finally {
      setLoading(false)
    }
  }

  const addHashtag = () => {
    if (hashtagInput && !formData.hashtags?.includes(hashtagInput)) {
      setFormData({
        ...formData,
        hashtags: [...(formData.hashtags || []), hashtagInput.replace('#', '')]
      })
      setHashtagInput('')
    }
  }

  const removeHashtag = (tag: string) => {
    setFormData({
      ...formData,
      hashtags: formData.hashtags?.filter(t => t !== tag) || []
    })
  }

  const togglePlatform = (platform: string) => {
    const platforms = formData.target_platforms || []
    if (platforms.includes(platform)) {
      setFormData({
        ...formData,
        target_platforms: platforms.filter(p => p !== platform)
      })
    } else {
      setFormData({
        ...formData,
        target_platforms: [...platforms, platform]
      })
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-2xl font-bold">Create New Post</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium mb-2">Title</label>
            <Input
              type="text"
              value={formData.title || ''}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="Enter post title (optional)"
            />
          </div>

          {/* Caption */}
          <div>
            <label className="block text-sm font-medium mb-2">Caption</label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={4}
              value={formData.caption || ''}
              onChange={(e) => setFormData({ ...formData, caption: e.target.value })}
              placeholder="Write your caption..."
            />
          </div>

          {/* Post Type */}
          <div>
            <label className="block text-sm font-medium mb-2">Post Type</label>
            <div className="grid grid-cols-4 gap-2">
              {['photo', 'video', 'carousel', 'story'].map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setFormData({ ...formData, post_type: type })}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    formData.post_type === type
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>

          {/* Target Platforms */}
          <div>
            <label className="block text-sm font-medium mb-2">Target Platforms</label>
            <div className="grid grid-cols-3 gap-2">
              {['instagram', 'tiktok', 'linkedin', 'facebook', 'wordpress'].map((platform) => (
                <button
                  key={platform}
                  type="button"
                  onClick={() => togglePlatform(platform)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    formData.target_platforms?.includes(platform)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {platform}
                </button>
              ))}
            </div>
          </div>

          {/* Hashtags */}
          <div>
            <label className="block text-sm font-medium mb-2">Hashtags</label>
            <div className="flex gap-2 mb-2">
              <Input
                type="text"
                value={hashtagInput}
                onChange={(e) => setHashtagInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addHashtag())}
                placeholder="Add hashtag"
              />
              <Button type="button" onClick={addHashtag}>
                Add
              </Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {formData.hashtags?.map((tag) => (
                <span
                  key={tag}
                  className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center gap-2"
                >
                  #{tag}
                  <button
                    type="button"
                    onClick={() => removeHashtag(tag)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              className="flex-1"
              disabled={loading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1"
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Post'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
