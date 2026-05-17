<template>
  <div>
    <AppHeader />
    <main class="min-h-[calc(100vh-64px)] flex items-center justify-center py-12 px-4">
      <div class="max-w-md w-full">
        <div class="bg-white rounded-xl shadow-lg p-8">
          <h1 class="text-2xl font-bold text-center text-gray-900 mb-8">
            登录账户
          </h1>
          
          <UForm @submit="handleSubmit" state="ready">
            <div class="space-y-6">
              <div>
                <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                  邮箱
                </label>
                <UInput
                  v-model="formData.email"
                  type="email"
                  id="email"
                  required
                  placeholder="your@email.com"
                  size="lg"
                />
              </div>
              
              <div>
                <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                  密码
                </label>
                <UInput
                  v-model="formData.password"
                  type="password"
                  id="password"
                  required
                  placeholder="••••••••"
                  size="lg"
                />
              </div>
              
              <UButton
                type="submit"
                size="xl"
                class="w-full"
                :loading="loading"
              >
                {{ loading ? '登录中...' : '登录' }}
              </UButton>
            </div>
          </UForm>
          
          <div class="mt-6 text-center">
            <p class="text-gray-600">
              还没有账户？
              <NuxtLink to="/register" class="text-blue-600 hover:text-blue-700 font-medium">
                立即注册
              </NuxtLink>
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const { login } = useAuth()
const router = useRouter()

const formData = reactive({
  email: '',
  password: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  try {
    loading.value = true
    await login({
      email: formData.email,
      password: formData.password
    })
    await router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
  } finally {
    loading.value = false
  }
}
</script>
