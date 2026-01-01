/**
 * TypeScript type definitions for Pyralys
 */

export interface User {
  id: string
  email: string
  full_name: string
  plan_type: 'free' | 'pro' | 'business' | 'enterprise'
  created_at: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface LoginCredentials {
  username: string  // OAuth2 uses 'username' for email
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
}

export interface Media {
  id: string
  post_id: string
  user_id: string
  file_url: string
  file_type: 'image' | 'video'
  file_size?: number
  width?: number
  height?: number
  duration?: number
  order_position: number
  ai_generated: boolean
  generation_prompt?: string
  created_at: string
}

export interface PostPublication {
  id: string
  post_id: string
  platform: string
  platform_post_id?: string
  platform_url?: string
  status: string
  error_message?: string
  published_at?: string
  insights?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface Post {
  id: string
  user_id: string
  title?: string
  caption?: string
  content?: string
  hashtags: string[]
  post_type: 'photo' | 'video' | 'carousel' | 'story'
  status: 'draft' | 'scheduled' | 'published' | 'failed' | 'archived'
  media_urls: string[]
  target_platforms: string[]
  ai_generated: boolean
  generation_params?: Record<string, any>
  scheduled_at?: string
  published_at?: string
  created_at: string
  updated_at: string
  media?: Media[]
  publications?: PostPublication[]
}

export interface PostCreate {
  title?: string
  caption?: string
  content?: string
  hashtags?: string[]
  post_type?: string
  target_platforms?: string[]
  ai_generated?: boolean
  ai_prompt?: string
  generation_params?: Record<string, any>
  media_urls?: string[]
  scheduled_at?: string
}

export interface PostUpdate {
  title?: string
  caption?: string
  content?: string
  hashtags?: string[]
  post_type?: string
  status?: string
  target_platforms?: string[]
  media_urls?: string[]
  scheduled_at?: string
}

export interface AIGenerationRequest {
  prompt: string
  platform: string
  tone: 'casual' | 'professional' | 'funny' | 'inspirational'
}

export interface AIGenerationResponse {
  caption: string
  hashtags: string[]
  metadata: Record<string, any>
}

export interface SocialAccount {
  id: string
  platform: string
  account_username: string
  is_active: boolean
  created_at: string
}
