<template>
  <div class="min-h-screen bg-gray-50">
    <NuxtPage />
    <CookieConsent />
  </div>
</template>

<script setup lang="ts">
onMounted(async () => {
  if (import.meta.client) {
    const authStore = useAuthStore()
    if (authStore.token) {
      const { fetchCurrentUser } = useAuth()
      await fetchCurrentUser()
    }
  }
})
</script>
