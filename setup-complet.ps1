# Script PowerShell pour configuration complète de Pyralys
# Exécutez ce script depuis: C:\Program Files\Docker\Pyralys

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  CONFIGURATION COMPLÈTE PYRALYS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ============================================
# 1. CRÉATION DES FICHIERS LIB
# ============================================
Write-Host "[1/3] Création des fichiers lib..." -ForegroundColor Yellow
Write-Host ""

$libPath = "frontend\lib"
if (-not (Test-Path $libPath)) {
    New-Item -ItemType Directory -Path $libPath -Force | Out-Null
    Write-Host "  ✓ Dossier $libPath créé" -ForegroundColor Green
}

# utils.ts
@"
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"@ | Out-File -FilePath "$libPath\utils.ts" -Encoding UTF8
Write-Host "  ✓ utils.ts créé" -ForegroundColor Green

# api.ts
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
Write-Host "  ✓ api.ts créé" -ForegroundColor Green

# auth.ts
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
Write-Host "  ✓ auth.ts créé" -ForegroundColor Green

# billing.ts
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
Write-Host "  ✓ billing.ts créé" -ForegroundColor Green

# ============================================
# 2. CRÉATION DES FICHIERS .ENV
# ============================================
Write-Host ""
Write-Host "[2/3] Création des fichiers .env..." -ForegroundColor Yellow
Write-Host ""

# Frontend .env.local
$frontendEnv = "frontend\.env.local"
if (-not (Test-Path $frontendEnv)) {
    @"
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# App Configuration
NEXT_PUBLIC_APP_NAME=Pyralys
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Stripe (OPTIONNEL - mode test)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_YOUR-KEY-HERE-OPTIONAL

# Analytics (optional)
NEXT_PUBLIC_GA_TRACKING_ID=
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=
"@ | Out-File -FilePath $frontendEnv -Encoding UTF8
    Write-Host "  ✓ frontend\.env.local créé" -ForegroundColor Green
} else {
    Write-Host "  ⊙ frontend\.env.local existe déjà" -ForegroundColor Gray
}

# Backend .env
$backendEnv = "backend\.env"
if (-not (Test-Path $backendEnv)) {
    @"
# Application
APP_NAME=Pyralys API
APP_ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production-12345678901234567890
JWT_SECRET=dev-jwt-secret-key-change-in-production-12345678901234567890

# Database - Docker configuration (use container hostnames)
DATABASE_URL=postgresql+asyncpg://pyralys:pyralys_dev_password@postgres:5432/pyralys_dev
DATABASE_WRITE_URL=postgresql+asyncpg://pyralys:pyralys_dev_password@postgres:5432/pyralys_dev
DATABASE_READ_URL=postgresql+asyncpg://pyralys:pyralys_dev_password@postgres:5432/pyralys_dev

# Redis - Docker configuration (use container hostnames)
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI (OPTIONAL - add your key to test AI features)
OPENAI_API_KEY=sk-YOUR-KEY-HERE-OPTIONAL

# Anthropic (OPTIONAL)
ANTHROPIC_API_KEY=YOUR-KEY-HERE-OPTIONAL

# AWS (OPTIONAL - for image uploads)
AWS_ACCESS_KEY_ID=YOUR-KEY-HERE-OPTIONAL
AWS_SECRET_ACCESS_KEY=YOUR-KEY-HERE-OPTIONAL
AWS_REGION=eu-west-1
AWS_S3_BUCKET=pyralys-media-dev

# Instagram/Facebook (OPTIONAL)
FACEBOOK_APP_ID=YOUR-APP-ID-OPTIONAL
FACEBOOK_APP_SECRET=YOUR-APP-SECRET-OPTIONAL

# Stripe (OPTIONAL - test mode)
STRIPE_SECRET_KEY=sk_test_YOUR-KEY-HERE-OPTIONAL
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR-KEY-HERE-OPTIONAL
STRIPE_WEBHOOK_SECRET=whsec_YOUR-WEBHOOK-SECRET-OPTIONAL

# TikTok (OPTIONAL)
TIKTOK_CLIENT_KEY=YOUR-KEY-HERE-OPTIONAL
TIKTOK_CLIENT_SECRET=YOUR-SECRET-HERE-OPTIONAL

# SendGrid (OPTIONAL - for email)
SENDGRID_API_KEY=YOUR-KEY-HERE-OPTIONAL

# Sentry (OPTIONAL - for error tracking)
SENTRY_DSN=YOUR-DSN-HERE-OPTIONAL

# Frontend
FRONTEND_URL=http://localhost:3000

# CORS - JSON array format required for Pydantic validation
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
"@ | Out-File -FilePath $backendEnv -Encoding UTF8
    Write-Host "  ✓ backend\.env créé" -ForegroundColor Green
} else {
    Write-Host "  ⊙ backend\.env existe déjà" -ForegroundColor Gray
}

# ============================================
# 3. VÉRIFICATION DOCKERFILE
# ============================================
Write-Host ""
Write-Host "[3/3] Vérification Dockerfile..." -ForegroundColor Yellow
Write-Host ""

$dockerfilePath = "frontend\Dockerfile"
$dockerfileContent = Get-Content $dockerfilePath -Raw

if ($dockerfileContent -match "RUN npm ci") {
    Write-Host "  ⚠ Dockerfile utilise encore 'npm ci'" -ForegroundColor Red
    Write-Host "  → Changement en 'npm install'..." -ForegroundColor Yellow

    $dockerfileContent = $dockerfileContent -replace "RUN npm ci", "RUN npm install"
    $dockerfileContent | Out-File -FilePath $dockerfilePath -Encoding UTF8 -NoNewline

    Write-Host "  ✓ Dockerfile corrigé" -ForegroundColor Green
} else {
    Write-Host "  ✓ Dockerfile utilise déjà 'npm install'" -ForegroundColor Green
}

# ============================================
# RÉSUMÉ
# ============================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✓ CONFIGURATION TERMINÉE AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Fichiers créés:" -ForegroundColor White
Write-Host "  ✓ frontend\lib\utils.ts" -ForegroundColor Green
Write-Host "  ✓ frontend\lib\api.ts" -ForegroundColor Green
Write-Host "  ✓ frontend\lib\auth.ts" -ForegroundColor Green
Write-Host "  ✓ frontend\lib\billing.ts" -ForegroundColor Green
Write-Host "  ✓ frontend\.env.local" -ForegroundColor Green
Write-Host "  ✓ backend\.env" -ForegroundColor Green
Write-Host "  ✓ frontend\Dockerfile (corrigé)" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PROCHAINES ÉTAPES:" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Rebuild Docker frontend:" -ForegroundColor White
Write-Host "   docker-compose build --no-cache frontend" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Démarrer tous les services:" -ForegroundColor White
Write-Host "   docker-compose up -d" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Initialiser la base de données:" -ForegroundColor White
Write-Host "   docker-compose exec backend alembic upgrade head" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Vérifier que tout fonctionne:" -ForegroundColor White
Write-Host "   docker-compose ps" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Ouvrir dans le navigateur:" -ForegroundColor White
Write-Host "   http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
