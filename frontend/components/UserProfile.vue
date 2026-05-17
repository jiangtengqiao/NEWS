<template>
  <div class="space-y-4">
    <div v-if="authStore.user">
      <h2 class="text-xl">{{ authStore.user.nickname || authStore.user.email }}</h2>
      <p>Email: {{ authStore.user.email }}</p>
      <button @click="handleLogout" class="btn btn-secondary">Logout</button>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useAuth } from '~/composables/useAuth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const { logout, fetchCurrentUser } = useAuth()
const router = useRouter()

onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    await fetchCurrentUser()
  }
})

function handleLogout() {
  logout()
  router.push('/')
}
</script>
