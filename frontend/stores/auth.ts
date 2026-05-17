import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Token } from '~/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(
    import.meta.client ? localStorage.getItem('token') : null
  )
  const user = ref<User | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    if (import.meta.client) {
      localStorage.setItem('token', newToken)
    }
  }

  function setUser(newUser: User) {
    user.value = newUser
  }

  function logout() {
    token.value = null
    user.value = null
    if (import.meta.client) {
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
    setToken,
    setUser,
    logout,
    setLoading
  }
})
