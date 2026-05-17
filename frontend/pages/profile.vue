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
          <div class="bg-white rounded-xl shadow-lg">
            <div class="border-b">
              <div class="flex">
                <button
                  v-for="tab in tabs"
                  :key="tab.id"
                  @click="activeTab = tab.id"
                  class="px-6 py-4 text-sm font-medium border-b-2 transition"
                  :class="[
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  ]"
                >
                  {{ tab.name }}
                </button>
              </div>
            </div>
            
            <div class="p-6">
              <div v-if="activeTab === 'profile'">
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

              <div v-if="activeTab === 'settings'">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">偏好设置</h3>
                
                <div v-if="settingsLoading" class="flex justify-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
                
                <div v-else class="space-y-6">
                  <div>
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium text-gray-900">接收点赞通知</p>
                        <p class="text-sm text-gray-500">当有人点赞您的内容时发送通知</p>
                      </div>
                      <UToggle
                        v-model="settingsData.notificationLike"
                      />
                    </div>
                  </div>

                  <div class="border-t pt-6">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium text-gray-900">接收评论通知</p>
                        <p class="text-sm text-gray-500">当有人评论您的内容时发送通知</p>
                      </div>
                      <UToggle
                        v-model="settingsData.notificationComment"
                      />
                    </div>
                  </div>

                  <div class="border-t pt-6">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium text-gray-900">接收收藏通知</p>
                        <p class="text-sm text-gray-500">当有人收藏您的内容时发送通知</p>
                      </div>
                      <UToggle
                        v-model="settingsData.notificationFavorite"
                      />
                    </div>
                  </div>

                  <div class="border-t pt-6">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium text-gray-900">接收关注通知</p>
                        <p class="text-sm text-gray-500">当有人关注您时发送通知</p>
                      </div>
                      <UToggle
                        v-model="settingsData.notificationFollow"
                      />
                    </div>
                  </div>

                  <div class="border-t pt-6">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium text-gray-900">接收系统通知</p>
                        <p class="text-sm text-gray-500">接收系统重要公告和更新通知</p>
                      </div>
                      <UToggle
                        v-model="settingsData.notificationSystem"
                      />
                    </div>
                  </div>

                  <div class="border-t pt-6">
                    <UButton
                      size="lg"
                      class="w-full"
                      @click="handleSaveSettings"
                      :loading="settingsSaving"
                    >
                      {{ settingsSaving ? '保存中...' : '保存设置' }}
                    </UButton>
                  </div>
                </div>
              </div>

              <div v-if="activeTab === 'stats'">
                <h3 class="text-lg font-semibold text-gray-900 mb-6">活动统计</h3>
                
                <div v-if="statsLoading" class="flex justify-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
                
                <div v-else-if="!stats" class="text-center py-8 text-gray-500">
                  暂无统计数据
                </div>
                
                <div v-else class="grid grid-cols-2 gap-4">
                  <div class="bg-blue-50 rounded-lg p-4 text-center">
                    <p class="text-2xl font-bold text-blue-600">{{ stats.newsRead || 0 }}</p>
                    <p class="text-sm text-gray-600">阅读新闻</p>
                  </div>
                  <div class="bg-green-50 rounded-lg p-4 text-center">
                    <p class="text-2xl font-bold text-green-600">{{ stats.newsLiked || 0 }}</p>
                    <p class="text-sm text-gray-600">点赞内容</p>
                  </div>
                  <div class="bg-yellow-50 rounded-lg p-4 text-center">
                    <p class="text-2xl font-bold text-yellow-600">{{ stats.newsFavorited || 0 }}</p>
                    <p class="text-sm text-gray-600">收藏内容</p>
                  </div>
                  <div class="bg-purple-50 rounded-lg p-4 text-center">
                    <p class="text-2xl font-bold text-purple-600">{{ stats.commentsPosted || 0 }}</p>
                    <p class="text-sm text-gray-600">发表评论</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useSettingsStore } from '~/stores/settings'
import { useStatsStore } from '~/stores/stats'
import { useUser } from '~/composables/useUser'
import { useSettings } from '~/composables/useSettings'
import { useStats } from '~/composables/useStats'

const authStore = useAuthStore()
const settingsStore = useSettingsStore()
const statsStore = useStatsStore()

const { updateProfile, getMyCode } = useUser()
const { fetchSettings: fetchUserSettings, updateSettings: updateUserSettings } = useSettings()
const { fetchStats: fetchUserStats } = useStats()

const user = computed(() => authStore.user)
const settings = computed(() => settingsStore.settings)
const stats = computed(() => statsStore.stats)

const userCode = ref<string>('')
const loading = ref(false)
const settingsLoading = ref(false)
const settingsSaving = ref(false)
const statsLoading = ref(false)

const activeTab = ref('profile')

const tabs = [
  { id: 'profile', name: '个人资料' },
  { id: 'settings', name: '偏好设置' },
  { id: 'stats', name: '活动统计' }
]

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

const settingsData = reactive({
  notificationLike: true,
  notificationComment: true,
  notificationFavorite: true,
  notificationFollow: true,
  notificationSystem: true
})

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

  try {
    await loadSettings()
  } catch (error) {
    console.error('Failed to load settings:', error)
  }

  try {
    await loadStats()
  } catch (error) {
    console.error('Failed to load stats:', error)
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

const loadSettings = async () => {
  try {
    settingsLoading.value = true
    const settings = await fetchUserSettings()
    if (settings) {
      settingsData.notificationLike = settings.notificationLike ?? true
      settingsData.notificationComment = settings.notificationComment ?? true
      settingsData.notificationFavorite = settings.notificationFavorite ?? true
      settingsData.notificationFollow = settings.notificationFollow ?? true
      settingsData.notificationSystem = settings.notificationSystem ?? true
    }
  } finally {
    settingsLoading.value = false
  }
}

const handleSaveSettings = async () => {
  try {
    settingsSaving.value = true
    await updateUserSettings({
      notificationLike: settingsData.notificationLike,
      notificationComment: settingsData.notificationComment,
      notificationFavorite: settingsData.notificationFavorite,
      notificationFollow: settingsData.notificationFollow,
      notificationSystem: settingsData.notificationSystem
    })
    const toast = useToast()
    toast.add({
      title: '设置已保存',
      color: 'green'
    })
  } catch (error) {
    console.error('Failed to save settings:', error)
  } finally {
    settingsSaving.value = false
  }
}

const loadStats = async () => {
  try {
    statsLoading.value = true
    await fetchUserStats()
  } finally {
    statsLoading.value = false
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
