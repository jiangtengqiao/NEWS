<template>
  <div class="fixed bottom-0 left-0 right-0 bg-gray-800 text-white p-4">
    <p>We use cookies to improve your experience.</p>
    <button @click="accept" class="btn btn-primary ml-4">Accept</button>
  </div>
</template>

<script setup lang="ts">
function accept() {
  localStorage.setItem('cookieConsent', 'true')
}
</script>
