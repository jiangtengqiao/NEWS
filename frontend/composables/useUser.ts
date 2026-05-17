import { useUserStore } from '~/stores/user'
import { useAuth } from '~/composables/useAuth'

export function useUser() {
  const userStore = useUserStore()
  const { apiFetch } = useAuth()

  async function updateProfile(data: any) {
    return await apiFetch('/api/users/me', {
      method: 'PUT',
      body: data
    })
  }

  async function getUserById(id: string) {
    const user = await apiFetch(`/api/users/${id}`)
    userStore.setUser(user)
    return user
  }

  async function getUserByCode(code: string) {
    return await apiFetch(`/api/users/code/${code}`)
  }

  return {
    updateProfile,
    getUserById,
    getUserByCode
  }
}
