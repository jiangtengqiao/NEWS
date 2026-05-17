<template>
  <div v-if="!consentGiven" class="fixed bottom-0 left-0 right-0 bg-gray-900 text-white p-4 z-50">
    <div class="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex-1">
        <p class="text-sm">
          我们使用 Cookie 来改善您的体验。继续使用本网站即表示您同意我们的 Cookie 政策。
        </p>
      </div>
      <div class="flex space-x-3">
        <UButton @click="acceptConsent" size="sm" color="blue">
          接受
        </UButton>
        <UButton @click="declineConsent" size="sm" variant="outline" class="text-white border-white hover:bg-white hover:text-gray-900">
          拒绝
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const consentGiven = ref(false)

onMounted(() => {
  if (import.meta.client) {
    const savedConsent = localStorage.getItem('cookieConsent')
    consentGiven.value = savedConsent !== null
  }
})

const acceptConsent = () => {
  localStorage.setItem('cookieConsent', 'accepted')
  consentGiven.value = true
}

const declineConsent = () => {
  localStorage.setItem('cookieConsent', 'declined')
  consentGiven.value = true
}
</script>
