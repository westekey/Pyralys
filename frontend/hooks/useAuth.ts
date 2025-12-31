/**
 * Authentication hook using Zustand
 */
'use client'

import { create } from 'zustand'
import { User, LoginCredentials, RegisterData } from '@/lib/types'
import { AuthAPI, TokenManager } from '@/lib/auth'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (credentials: LoginCredentials) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
  clearError: () => void
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (credentials: LoginCredentials) => {
    try {
      set({ isLoading: true, error: null })

      const response = await AuthAPI.login(credentials)

      // Store tokens
      TokenManager.setTokens(response.access_token, response.refresh_token)

      // Update state
      set({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      })

      toast.success('Welcome back!')
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login failed'
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: errorMessage,
      })
      toast.error(errorMessage)
      throw error
    }
  },

  register: async (data: RegisterData) => {
    try {
      set({ isLoading: true, error: null })

      const response = await AuthAPI.register(data)

      // Store tokens
      TokenManager.setTokens(response.access_token, response.refresh_token)

      // Update state
      set({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      })

      toast.success(`Welcome to Pyralys, ${response.user.full_name}!`)
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed'
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: errorMessage,
      })
      toast.error(errorMessage)
      throw error
    }
  },

  logout: () => {
    TokenManager.clearTokens()
    set({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    })
    toast.success('Logged out successfully')
  },

  refreshUser: async () => {
    try {
      if (!TokenManager.hasTokens()) {
        set({ user: null, isAuthenticated: false })
        return
      }

      const user = await AuthAPI.getCurrentUser()

      set({
        user,
        isAuthenticated: true,
        error: null,
      })
    } catch (error) {
      // If refresh fails, clear tokens and log out
      TokenManager.clearTokens()
      set({
        user: null,
        isAuthenticated: false,
        error: 'Session expired',
      })
    }
  },

  clearError: () => {
    set({ error: null })
  },
}))

/**
 * Custom hook for authentication
 */
export function useAuth() {
  const router = useRouter()
  const store = useAuthStore()

  const loginAndRedirect = async (credentials: LoginCredentials) => {
    await store.login(credentials)
    router.push('/dashboard')
  }

  const registerAndRedirect = async (data: RegisterData) => {
    await store.register(data)
    router.push('/dashboard')
  }

  const logoutAndRedirect = () => {
    store.logout()
    router.push('/')
  }

  return {
    ...store,
    loginAndRedirect,
    registerAndRedirect,
    logoutAndRedirect,
  }
}
