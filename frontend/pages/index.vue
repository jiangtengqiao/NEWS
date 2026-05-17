<template>
  <div>
    <AppHeader />
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-6">
          欢迎来到 Customize News
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          您的个性化新闻平台，与朋友分享精彩内容
        </p>
        
        <NuxtLink to="/news">
          <UButton size="xl" class="bg-blue-600 hover:bg-blue-700">
            浏览新闻
          </UButton>
        </NuxtLink>
      </div>

      <div v-if="!isAuthenticated" class="text-center">
        <div class="flex justify-center gap-4 mt-8">
          <NuxtLink to="/register">
            <UButton size="xl">
              立即注册
            </UButton>
          </NuxtLink>
          <NuxtLink to="/login">
            <UButton size="xl" variant="outline">
              登录账户
            </UButton>
          </NuxtLink>
        </div>
      </div>

      <div v-else class="mt-8">
        <div class="bg-white rounded-xl shadow-lg p-8 max-w-3xl mx-auto">
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">
            欢迎回来，{{ user?.nickname || '用户' }}！
          </h2>
          <p class="text-gray-600 mb-6">
            探索您的个性化新闻，与好友保持联系
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <NuxtLink to="/news" class="text-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition">
              <UIcon name="heroicons:newspaper" class="w-8 h-8 mx-auto text-blue-600 mb-2" />
              <p class="font-medium">新闻</p>
            </NuxtLink>
            <NuxtLink to="/friends" class="text-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition">
              <UIcon name="heroicons:users" class="w-8 h-8 mx-auto text-green-600 mb-2" />
              <p class="font-medium">好友</p>
            </NuxtLink>
            <NuxtLink to="/messages" class="text-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition">
              <UIcon name="heroicons:chat-bubble-left-right" class="w-8 h-8 mx-auto text-purple-600 mb-2" />
              <p class="font-medium">消息</p>
            </NuxtLink>
            <NuxtLink to="/profile" class="text-center p-4 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition">
              <UIcon name="heroicons:user" class="w-8 h-8 mx-auto text-yellow-600 mb-2" />
              <p class="font-medium">个人资料</p>
            </NuxtLink>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
</script>
