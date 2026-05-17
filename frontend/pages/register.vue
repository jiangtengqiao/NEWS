<template>
  <div>
    <AppHeader />
    <main class="min-h-[calc(100vh-64px)] flex items-center justify-center py-12 px-4">
      <div class="max-w-md w-full">
        <div class="bg-white rounded-xl shadow-lg p-8">
          <h1 class="text-2xl font-bold text-center text-gray-900 mb-8">
            创建账户
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
                <label for="nickname" class="block text-sm font-medium text-gray-700 mb-2">
                  昵称 (可选)
                </label>
                <UInput
                  v-model="formData.nickname"
                  type="text"
                  id="nickname"
                  placeholder="您的昵称"
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
                  placeholder="至少8个字符"
                  size="lg"
                />
              </div>
              
              <div>
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
                  确认密码
                </label>
                <UInput
                  v-model="formData.confirmPassword"
                  type="password"
                  id="confirmPassword"
                  required
                  placeholder="再次输入密码"
                  size="lg"
                />
              </div>
              
              <UButton
                type="submit"
                size="xl"
                class="w-full"
                :loading="loading"
                :disabled="formData.password !== formData.confirmPassword"
              >
                {{ loading ? '注册中...' : '注册' }}
              </UButton>
            </div>
          </UForm>
          
          <div class="mt-6 text-center">
            <p class="text-gray-600">
              已有账户？
              <NuxtLink to="/login" class="text-blue-600 hover:text-blue-700 font-medium">
                立即登录
              </NuxtLink>
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const { register } = useAuth()
const router = useRouter()

const formData = reactive({
  email: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  if (formData.password !== formData.confirmPassword) return
  
  try {
    loading.value = true
    await register({
      email: formData.email,
      password: formData.password,
      nickname: formData.nickname
    })
    await router.push('/login')
  } catch (error) {
    console.error('Register failed:', error)
  } finally {
    loading.value = false
  }
}
</script>
