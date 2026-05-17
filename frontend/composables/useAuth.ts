import type { LoginRequest, RegisterRequest, Token, User } from '~/types'

export function useAuth() {
  const authStore = useAuthStore()

  const apiFetch = $fetch.create({
    baseURL: 'http://localhost:8000',
    onRequest({ options }) {
      if (authStore.token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${authStore.token}`
        }
      }
    }
  })

  function getToast() {
    return useToast()
  }

  function getConfig() {
    return useRuntimeConfig()
  }

  async function login(credentials: LoginRequest): Promise<void> {
    try {
      authStore.setLoading(true)
      const response = await apiFetch<{ access_token: string; token_type: string }>('/api/auth/login', {
        method: 'POST',
        body: credentials
      })
      
      authStore.setToken(response.access_token)
      await fetchCurrentUser()
      getToast().add({
        title: '欢迎回来！',
        color: 'green'
      })
    } catch (error) {
      getToast().add({
        title: '登录失败',
        description: '请检查您的邮箱和密码',
        color: 'red'
      })
      throw error
    } finally {
      authStore.setLoading(false)
    }
  }

  async function register(data: RegisterRequest): Promise<void> {
    try {
      authStore.setLoading(true)
      const response = await apiFetch<User>('/api/auth/register', {
        method: 'POST',
        body: data
      })
      
      getToast().add({
        title: '注册成功！',
        description: '请登录您的账户',
        color: 'green'
      })
    } catch (error) {
      getToast().add({
        title: '注册失败',
        description: '请检查您的信息',
        color: 'red'
      })
      throw error
    } finally {
      authStore.setLoading(false)
    }
  }

  async function fetchCurrentUser(): Promise<void> {
    if (!authStore.token) return
    
    try {
      const user = await apiFetch<User>('/api/auth/me')
      
      authStore.setUser({
        ...user,
        avatarUrl: user.avatarUrl || user.avatar_url,
        isVerified: user.isVerified || user.is_verified,
        isSubscribed: user.isSubscribed || user.is_subscribed
      })
    } catch (error) {
      authStore.logout()
    }
  }

  function handleLogout() {
    authStore.logout()
    getToast().add({
      title: '已退出登录',
      color: 'blue'
    })
  }

  return {
    login,
    register,
    fetchCurrentUser,
    logout: handleLogout,
    apiFetch
  }
}
