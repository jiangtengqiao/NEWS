import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Token } from '~/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<User | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  function initializeAuth() {
    if (import.meta.client && typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('token')
      if (storedToken) {
        token.value = storedToken
      }
    }
  }

  function setToken(newToken: string) {
    token.value = newToken
    if (import.meta.client && typeof window !== 'undefined') {
      localStorage.setItem('token', newToken)
    }
  }

  function setUser(newUser: User) {
    user.value = newUser
  }

  function logout() {
    token.value = null
    user.value = null
    if (import.meta.client && typeof window !== 'undefined') {
      localStorage.removeItem('token')
    }
  }

  function setLoading(newLoading: boolean) {
    loading.value = newLoading
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    initializeAuth,
    setToken,
    setUser,
    logout,
    setLoading
  }
})
