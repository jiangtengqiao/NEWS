<template>
  <div>
    <AppHeader />
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="md:col-span-1">
          <div class="bg-white rounded-xl shadow-lg p-6">
            <div class="text-center">
              <div class="w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mx-auto flex items-center justify-center text-white text-4xl font-bold">
                {{ userInitial }}
              </div>
              <h2 class="mt-4 text-xl font-semibold text-gray-900">
                {{ user?.nickname || '用户' }}
              </h2>
              <p class="text-gray-600">{{ user?.email }}</p>
            </div>
            
            <div class="mt-6 space-y-4">
              <div class="border-t pt-4">
                <p class="text-sm text-gray-500">用户码</p>
                <div class="flex items-center space-x-2">
                  <span class="font-mono font-bold text-blue-600">{{ userCode || '加载中...' }}</span>
                  <UButton 
                    v-if="userCode"
                    size="sm" 
                    variant="outline"
                    @click="copyCode"
                  >
                    复制
                  </UButton>
                </div>
                <p class="text-xs text-gray-400 mt-1">分享此码给好友添加</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="md:col-span-2">
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-6">编辑个人资料</h3>
            
            <UForm @submit="handleSubmit" state="ready">
              <div class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">昵称</label>
                  <UInput
                    v-model="formData.nickname"
                    placeholder="您的昵称"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">性别</label>
                  <USelect
                    v-model="formData.gender"
                    :options="[
                      { value: '', label: '选择性别' },
                      { value: 'male', label: '男' },
                      { value: 'female', label: '女' },
                      { value: 'other', label: '其他' }
                    ]"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">生日</label>
                  <UInput
                    v-model="formData.birthday"
                    type="date"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">个人简介</label>
                  <UTextarea
                    v-model="formData.bio"
                    placeholder="写点什么介绍一下自己吧..."
                    rows="4"
                  />
                </div>
                
                <UButton
                  type="submit"
                  size="lg"
                  class="w-full"
                  :loading="loading"
                >
                  {{ loading ? '保存中...' : '保存更改' }}
                </UButton>
              </div>
            </UForm>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const { updateProfile, getMyCode } = useUser()

const user = computed(() => authStore.user)
const userCode = ref<string>('')

const userInitial = computed(() => {
  const name = user.value?.nickname || user.value?.email?.[0]
  return name ? name.toUpperCase() : 'U'
})

const formData = reactive({
  nickname: '',
  gender: '',
  birthday: '',
  bio: ''
})

const loading = ref(false)

onMounted(async () => {
  if (user.value) {
    formData.nickname = user.value.nickname || ''
    formData.gender = user.value.gender || ''
    formData.birthday = user.value.birthday || ''
    formData.bio = user.value.bio || ''
  }
  
  try {
    const codeData = await getMyCode()
    userCode.value = codeData.code
  } catch (error) {
    console.error('Failed to get user code:', error)
  }
})

watch(user, (newUser) => {
  if (newUser) {
    formData.nickname = newUser.nickname || ''
    formData.gender = newUser.gender || ''
    formData.birthday = newUser.birthday || ''
    formData.bio = newUser.bio || ''
  }
}, { immediate: true })

const handleSubmit = async () => {
  try {
    loading.value = true
    const updatedUser = await updateProfile(formData)
    authStore.setUser(updatedUser)
  } catch (error) {
    console.error('Update failed:', error)
  } finally {
    loading.value = false
  }
}

const copyCode = () => {
  if (userCode.value) {
    navigator.clipboard.writeText(userCode.value)
    const toast = useToast()
    toast.add({
      title: '已复制到剪贴板',
      color: 'green'
    })
  }
}
</script>
