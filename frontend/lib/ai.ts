/**
 * AI Generation API Client
 */
import axios from 'axios'
import { TokenManager } from './auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface CaptionGenerationRequest {
  prompt: string
  platform: 'instagram' | 'tiktok' | 'linkedin' | 'facebook'
  tone: 'casual' | 'professional' | 'funny' | 'inspirational'
}

export interface CaptionGenerationResponse {
  caption: string
  hashtags: string[]
  metadata: {
    model: string
    tone: string
    platform: string
    tokens_used: number
    finish_reason: string
  }
}

export interface ImageGenerationRequest {
  prompt: string
  style?: string
  size: '1024x1024' | '1024x1792' | '1792x1024'
  quality?: 'standard' | 'hd'
  platform?: string
}

export interface ImageGenerationResponse {
  image_url: string
  revised_prompt: string
  metadata: {
    model: string
    size: string
    quality: string
    style: string | null
  }
}

export interface HashtagGenerationRequest {
  topic: string
  platform: 'instagram' | 'tiktok' | 'linkedin' | 'facebook'
  count: number
}

export interface HashtagGenerationResponse {
  hashtags: string[]
  count: number
  platform: string
}

export class AIAPI {
  private static getAuthHeader() {
    const token = TokenManager.getAccessToken()
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  }

  /**
   * Generate AI-powered caption for social media
   */
  static async generateCaption(
    request: CaptionGenerationRequest
  ): Promise<CaptionGenerationResponse> {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/ai/generate-caption`,
      request,
      this.getAuthHeader()
    )
    return response.data
  }

  /**
   * Generate image with DALL-E 3
   */
  static async generateImage(
    request: ImageGenerationRequest
  ): Promise<ImageGenerationResponse> {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/ai/generate-image`,
      request,
      this.getAuthHeader()
    )
    return response.data
  }

  /**
   * Generate optimized hashtags
   */
  static async generateHashtags(
    request: HashtagGenerationRequest
  ): Promise<HashtagGenerationResponse> {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/ai/generate-hashtags`,
      request,
      this.getAuthHeader()
    )
    return response.data
  }

  /**
   * Optimize existing content
   */
  static async optimizeContent(content: string, platform: string): Promise<any> {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/ai/optimize-content`,
      null,
      {
        ...this.getAuthHeader(),
        params: { content, platform },
      }
    )
    return response.data
  }
}
