<template>
  <div class="min-h-screen bg-gray-50">
    <NuxtPage />
    <CookieConsent />
  </div>
</template>

<script setup lang="ts">
const { fetchCurrentUser, isAuthenticated } = useAuth()

onMounted(() => {
  if (isAuthenticated.value) {
    fetchCurrentUser()
  }
})
</script>
