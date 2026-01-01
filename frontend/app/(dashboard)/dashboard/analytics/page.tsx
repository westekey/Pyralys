'use client'

import { useState, useEffect } from 'react'
import { analyticsApi } from '@/lib/analytics'

export default function AnalyticsPage() {
  const [dashboard, setDashboard] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [period, setPeriod] = useState(30)

  useEffect(() => {
    loadDashboard()
  }, [period])

  const loadDashboard = async () => {
    try {
      setLoading(true)
      const data = await analyticsApi.getDashboard(period)
      setDashboard(data)
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (!dashboard) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No analytics data available</p>
      </div>
    )
  }

  const { overview, performance, timeline, top_posts, content_types, posting_patterns, growth } = dashboard

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2">Analytics</h1>
          <p className="text-gray-600">
            Track your performance and engagement across platforms
          </p>
        </div>

        {/* Period Selector */}
        <div className="flex gap-2">
          {[7, 30, 90].map((days) => (
            <button
              key={days}
              onClick={() => setPeriod(days)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                period === days
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {days}d
            </button>
          ))}
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Posts"
          value={overview.total_posts}
          icon="📝"
          color="blue"
        />
        <StatCard
          title="Published"
          value={overview.published}
          icon="✅"
          color="green"
          subtitle={`${((overview.published / overview.total_posts) * 100 || 0).toFixed(0)}% of total`}
        />
        <StatCard
          title="Total Engagement"
          value={overview.total_engagement.toLocaleString()}
          icon="❤️"
          color="red"
        />
        <StatCard
          title="Engagement Rate"
          value={`${overview.avg_engagement_rate.toFixed(1)}%`}
          icon="📈"
          color="purple"
        />
      </div>

      {/* Growth Metrics */}
      {growth && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Growth Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Current Period ({period}d)</p>
              <p className="text-2xl font-bold">{growth.current_period.posts} posts</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Previous Period</p>
              <p className="text-2xl font-bold">{growth.previous_period.posts} posts</p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Growth Rate</p>
              <p className={`text-2xl font-bold ${
                growth.growth_rate >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {growth.growth_rate >= 0 ? '+' : ''}{growth.growth_rate.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Platform Performance */}
      {performance && Object.keys(performance.platforms).length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Platform Performance</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(performance.platforms).map(([platform, stats]: [string, any]) => (
              <PlatformCard key={platform} platform={platform} stats={stats} />
            ))}
          </div>
        </div>
      )}

      {/* Timeline Chart */}
      {timeline && timeline.timeline.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Posts Timeline</h2>
          <TimelineChart data={timeline.timeline} />
        </div>
      )}

      {/* Content Type Distribution */}
      {content_types && Object.keys(content_types).length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Content Types</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(content_types).map(([type, count]: [string, any]) => (
              <div key={type} className="text-center">
                <div className="text-3xl mb-2">
                  {type === 'photo' ? '📷' : type === 'video' ? '🎥' : type === 'carousel' ? '🖼️' : '⚡'}
                </div>
                <p className="text-2xl font-bold">{count}</p>
                <p className="text-sm text-gray-600 capitalize">{type}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top Posts */}
      {top_posts && top_posts.posts.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Top Performing Posts</h2>
          <div className="space-y-3">
            {top_posts.posts.map((post: any, index: number) => (
              <div key={post.id} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-400">#{index + 1}</div>
                <div className="flex-1">
                  <p className="font-medium">{post.title || 'Untitled'}</p>
                  <p className="text-sm text-gray-600 line-clamp-1">{post.caption}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold">{post.engagement.toLocaleString()}</p>
                  <p className="text-xs text-gray-600">engagements</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Posting Patterns */}
      {posting_patterns && (posting_patterns.best_day || posting_patterns.best_hour) && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Best Time to Post</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {posting_patterns.best_day && (
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-2">Best Day</p>
                <p className="text-2xl font-bold text-blue-600">{posting_patterns.best_day}</p>
              </div>
            )}
            {posting_patterns.best_hour !== null && (
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-2">Best Hour</p>
                <p className="text-2xl font-bold text-purple-600">
                  {posting_patterns.best_hour}:00
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

// StatCard Component
function StatCard({
  title,
  value,
  icon,
  color,
  subtitle
}: {
  title: string
  value: string | number
  icon: string
  color: string
  subtitle?: string
}) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    red: 'bg-red-50 text-red-600',
    purple: 'bg-purple-50 text-purple-600',
    yellow: 'bg-yellow-50 text-yellow-600'
  }

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm text-gray-600">{title}</p>
        <span className="text-2xl">{icon}</span>
      </div>
      <p className="text-2xl font-bold mb-1">{value}</p>
      {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
    </div>
  )
}

// PlatformCard Component
function PlatformCard({ platform, stats }: { platform: string; stats: any }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <h3 className="font-semibold capitalize mb-3">{platform}</h3>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">Posts:</span>
          <span className="font-medium">{stats.posts_count}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Success Rate:</span>
          <span className="font-medium text-green-600">
            {stats.success_rate?.toFixed(0) || 0}%
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Avg Engagement:</span>
          <span className="font-medium">{stats.avg_engagement?.toFixed(0) || 0}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Engagement Rate:</span>
          <span className="font-medium text-blue-600">
            {stats.engagement_rate?.toFixed(1) || 0}%
          </span>
        </div>
      </div>
    </div>
  )
}

// TimelineChart Component (Simple Bar Chart)
function TimelineChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null

  const maxPosts = Math.max(...data.map(d => d.posts))

  return (
    <div className="space-y-2">
      {data.slice(-14).map((item) => (
        <div key={item.date} className="flex items-center gap-3">
          <div className="w-24 text-xs text-gray-600">{item.date.slice(5)}</div>
          <div className="flex-1 bg-gray-100 rounded-full h-8 relative overflow-hidden">
            <div
              className="bg-blue-500 h-full rounded-full flex items-center px-3 text-white text-sm font-medium"
              style={{ width: `${(item.posts / maxPosts) * 100}%`, minWidth: '30px' }}
            >
              {item.posts}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
