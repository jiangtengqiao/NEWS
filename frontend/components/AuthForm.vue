<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div v-if="type === 'register'">
      <label class="block">Nickname</label>
      <input v-model="nickname" type="text" class="border p-2 w-full" />
    </div>
    <div>
      <label class="block">Email</label>
      <input v-model="email" type="email" required class="border p-2 w-full" />
    </div>
    <div>
      <label class="block">Password</label>
      <input v-model="password" type="password" required class="border p-2 w-full" />
    </div>
    <button type="submit" class="btn btn-primary">
      {{ type === 'login' ? 'Login' : 'Register' }}
    </button>
    <div v-if="error" class="text-red-500">{{ error }}</div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '~/composables/useAuth'
import { useRouter } from 'vue-router'

interface Props {
  type: 'login' | 'register'
}

const props = defineProps<Props>()
const { login, register } = useAuth()
const router = useRouter()

const email = ref('')
const password = ref('')
const nickname = ref('')
const error = ref('')

async function handleSubmit() {
  try {
    error.value = ''
    if (props.type === 'login') {
      await login(email.value, password.value)
    } else {
      await register(email.value, password.value, nickname.value)
    }
    await router.push('/profile')
  } catch (e) {
    error.value = 'An error occurred'
  }
}
</script>
