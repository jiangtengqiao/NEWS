import { useAuthStore } from '~/stores/auth'

export function useAuth() {
  const authStore = useAuthStore()
  const config = useRuntimeConfig()

  const apiFetch = $fetch.create({
    baseURL: config.public.apiBase,
    headers: {
      Authorization: authStore.token ? `Bearer ${authStore.token}` : undefined
    }
  })

  async function login(email: string, password: string) {
    const response = await apiFetch('/api/auth/login', {
      method: 'POST',
      body: { email, password }
    })
    authStore.setToken(response.access_token)
    await fetchCurrentUser()
    return response
  }

  async function register(email: string, password: string, nickname?: string) {
    return await apiFetch('/api/auth/register', {
      method: 'POST',
      body: { email, password, nickname }
    })
  }

  async function fetchCurrentUser() {
    const user = await apiFetch('/api/auth/me')
    authStore.setUser(user)
    return user
  }

  function logout() {
    authStore.logout()
  }

  return {
    login,
    register,
    fetchCurrentUser,
    logout,
    apiFetch
  }
}
