/**
 * Analytics API service
 */
import { api } from './api'

export const analyticsApi = {
  // Get overview statistics
  async getOverview(): Promise<any> {
    const response = await api.get('/analytics/overview')
    return response.data
  },

  // Get performance by platform
  async getPerformance(days: number = 30): Promise<any> {
    const response = await api.get('/analytics/performance', {
      params: { days }
    })
    return response.data
  },

  // Get posts timeline
  async getTimeline(days: number = 30): Promise<any> {
    const response = await api.get('/analytics/timeline', {
      params: { days }
    })
    return response.data
  },

  // Get top performing posts
  async getTopPosts(limit: number = 10, metric: string = 'engagement'): Promise<any> {
    const response = await api.get('/analytics/top-posts', {
      params: { limit, metric }
    })
    return response.data
  },

  // Get content type distribution
  async getContentTypes(): Promise<any> {
    const response = await api.get('/analytics/content-types')
    return response.data
  },

  // Get posting patterns
  async getPostingPatterns(): Promise<any> {
    const response = await api.get('/analytics/posting-patterns')
    return response.data
  },

  // Get growth metrics
  async getGrowth(days: number = 30): Promise<any> {
    const response = await api.get('/analytics/growth', {
      params: { days }
    })
    return response.data
  },

  // Get complete dashboard
  async getDashboard(days: number = 30): Promise<any> {
    const response = await api.get('/analytics/dashboard', {
      params: { days }
    })
    return response.data
  },

  // Export analytics
  async exportData(format: string = 'json', days: number = 30): Promise<any> {
    const response = await api.get('/analytics/export', {
      params: { format, days }
    })
    return response.data
  }
}
