import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  
  if (import.meta.client) {
    authStore.initializeAuth()
  }
})
