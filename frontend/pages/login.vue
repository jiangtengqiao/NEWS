<template>
  <div class="container mx-auto p-4 max-w-md">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    <AuthForm type="login" />
  </div>
</template>

<script setup lang="ts">
import AuthForm from '~/components/AuthForm.vue'
</script>
