# Script PowerShell pour créer les fichiers lib manquants
# Exécutez ce script depuis: C:\Program Files\Docker\Pyralys

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Création des fichiers lib manquants" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Créer le dossier lib s'il n'existe pas
$libPath = "frontend\lib"
if (-not (Test-Path $libPath)) {
    New-Item -ItemType Directory -Path $libPath -Force | Out-Null
    Write-Host "✓ Dossier $libPath créé" -ForegroundColor Green
}

# FICHIER 1: utils.ts
Write-Host "Création de utils.ts..." -ForegroundColor Yellow
@"
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"@ | Out-File -FilePath "$libPath\utils.ts" -Encoding UTF8
Write-Host "✓ utils.ts créé" -ForegroundColor Green

# FICHIER 2: api.ts
Write-Host "Création de api.ts..." -ForegroundColor Yellow
@"
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = ``Bearer `${token}``
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token expiration
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
"@ | Out-File -FilePath "$libPath\api.ts" -Encoding UTF8
Write-Host "✓ api.ts créé" -ForegroundColor Green

# FICHIER 3: auth.ts
Write-Host "Création de auth.ts..." -ForegroundColor Yellow
@"
/**
 * Authentication utilities and API calls
 */
import { api } from './api'
import { AuthResponse, LoginCredentials, RegisterData, User } from './types'

export class AuthAPI {
  /**
   * Register a new user
   */
  static async register(data: RegisterData): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/register', data)
    return response.data
  }

  /**
   * Login with email and password
   */
  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // OAuth2 format requires form data
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await api.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    return response.data
  }

  /**
   * Refresh access token
   */
  static async refreshToken(refreshToken: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/refresh', null, {
      params: { refresh_token: refreshToken },
    })
    return response.data
  }

  /**
   * Get current user information
   */
  static async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  }

  /**
   * Update current user
   */
  static async updateProfile(data: { full_name?: string }): Promise<User> {
    const response = await api.put<User>('/auth/me', data)
    return response.data
  }

  /**
   * Change password
   */
  static async changePassword(
    currentPassword: string,
    newPassword: string
  ): Promise<{ message: string }> {
    const response = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
    return response.data
  }

  /**
   * Request password reset
   */
  static async forgotPassword(email: string): Promise<{ message: string }> {
    const response = await api.post('/auth/forgot-password', { email })
    return response.data
  }

  /**
   * Reset password with token
   */
  static async resetPassword(
    token: string,
    newPassword: string
  ): Promise<{ message: string }> {
    const response = await api.post('/auth/reset-password', {
      token,
      new_password: newPassword,
    })
    return response.data
  }
}

/**
 * Token management
 */
export class TokenManager {
  private static ACCESS_TOKEN_KEY = 'access_token'
  private static REFRESH_TOKEN_KEY = 'refresh_token'

  static setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === 'undefined') return

    localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken)
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken)
  }

  static getAccessToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem(this.ACCESS_TOKEN_KEY)
  }

  static getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem(this.REFRESH_TOKEN_KEY)
  }

  static clearTokens(): void {
    if (typeof window === 'undefined') return

    localStorage.removeItem(this.ACCESS_TOKEN_KEY)
    localStorage.removeItem(this.REFRESH_TOKEN_KEY)
  }

  static hasTokens(): boolean {
    return !!this.getAccessToken() && !!this.getRefreshToken()
  }
}
"@ | Out-File -FilePath "$libPath\auth.ts" -Encoding UTF8
Write-Host "✓ auth.ts créé" -ForegroundColor Green

# FICHIER 4: billing.ts
Write-Host "Création de billing.ts..." -ForegroundColor Yellow
@"
/**
 * Billing API service
 */
import { api } from './api'

export const billingApi = {
  // Get available plans
  async getPlans(): Promise<any> {
    const response = await api.get('/billing/plans')
    return response.data
  },

  // Get current subscription
  async getSubscription(): Promise<any> {
    const response = await api.get('/billing/subscription')
    return response.data
  },

  // Create checkout session
  async createCheckout(planType: string): Promise<any> {
    const response = await api.post('/billing/create-checkout', {
      plan_type: planType
    })
    return response.data
  },

  // Create portal session
  async createPortal(): Promise<any> {
    const response = await api.post('/billing/create-portal')
    return response.data
  },

  // Cancel subscription
  async cancelSubscription(atPeriodEnd: boolean = true): Promise<any> {
    const response = await api.post('/billing/cancel-subscription', {
      at_period_end: atPeriodEnd
    })
    return response.data
  },

  // Get invoices
  async getInvoices(): Promise<any> {
    const response = await api.get('/billing/invoices')
    return response.data
  },

  // Get payment methods
  async getPaymentMethods(): Promise<any> {
    const response = await api.get('/billing/payment-methods')
    return response.data
  }
}
"@ | Out-File -FilePath "$libPath\billing.ts" -Encoding UTF8
Write-Host "✓ billing.ts créé" -ForegroundColor Green

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "✓ Tous les fichiers lib ont été créés avec succès!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines étapes:" -ForegroundColor Yellow
Write-Host "1. docker-compose build --no-cache frontend" -ForegroundColor White
Write-Host "2. docker-compose up -d" -ForegroundColor White
Write-Host ""
