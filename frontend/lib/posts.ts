/**
 * Posts API service
 */
import { api } from './api'
import { Post, PostCreate, PostUpdate } from './types'

export interface ListPostsParams {
  status?: string
  platform?: string
  post_type?: string
  search?: string
  skip?: number
  limit?: number
}

export interface PublishRequest {
  platforms: string[]
  publish_immediately?: boolean
  scheduled_for?: string
}

export const postsApi = {
  // Create a new post
  async create(data: PostCreate): Promise<Post> {
    const response = await api.post('/content/posts', data)
    return response.data
  },

  // List posts with filters
  async list(params: ListPostsParams = {}): Promise<Post[]> {
    const response = await api.get('/content/posts', { params })
    return response.data
  },

  // Get a specific post
  async get(postId: string): Promise<Post> {
    const response = await api.get(`/content/posts/${postId}`)
    return response.data
  },

  // Update a post
  async update(postId: string, data: PostUpdate): Promise<Post> {
    const response = await api.put(`/content/posts/${postId}`, data)
    return response.data
  },

  // Delete a post
  async delete(postId: string): Promise<void> {
    await api.delete(`/content/posts/${postId}`)
  },

  // Publish a post
  async publish(postId: string, request: PublishRequest): Promise<any> {
    const response = await api.post(`/content/posts/${postId}/publish`, request)
    return response.data
  },

  // Schedule a post
  async schedule(postId: string, scheduledAt: string): Promise<any> {
    const response = await api.post(`/content/posts/${postId}/schedule`, null, {
      params: { scheduled_at: scheduledAt }
    })
    return response.data
  },

  // Upload media
  async uploadMedia(file: File): Promise<{ url: string; filename: string }> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/content/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Get calendar data
  async getCalendar(startDate: string, endDate: string): Promise<any> {
    const response = await api.get('/content/calendar', {
      params: { start_date: startDate, end_date: endDate }
    })
    return response.data
  },

  // Get stats
  async getStats(): Promise<any> {
    const response = await api.get('/content/stats')
    return response.data
  }
}
