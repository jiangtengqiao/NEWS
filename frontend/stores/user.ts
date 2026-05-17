import { defineStore } from 'pinia'
import { ref } from 'vue'

interface User {
  id: string
  email: string
  nickname?: string
  avatar_url?: string
}

export const useUserStore = defineStore('user', () => {
  const users = ref<Map<string, User>>(new Map())

  function setUser(user: User) {
    users.value.set(user.id, user)
  }

  function getUser(id: string) {
    return users.value.get(id)
  }

  return {
    users,
    setUser,
    getUser
  }
})
