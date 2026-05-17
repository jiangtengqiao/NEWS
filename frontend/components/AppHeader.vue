<template>
  <header class="bg-white shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center">
          <NuxtLink to="/" class="text-2xl font-bold text-blue-600">
            Customize News
          </NuxtLink>
        </div>
        
        <nav class="flex items-center space-x-4">
          <NuxtLink 
            v-if="isAuthenticated" 
            to="/" 
            class="text-gray-700 hover:text-blue-600 transition"
          >
            首页
          </NuxtLink>
          
          <NuxtLink 
            v-if="isAuthenticated" 
            to="/news" 
            class="text-gray-700 hover:text-blue-600 transition"
          >
            新闻
          </NuxtLink>
          
          <NuxtLink 
            v-if="isAuthenticated" 
            to="/friends" 
            class="text-gray-700 hover:text-blue-600 transition"
          >
            好友
          </NuxtLink>
          
          <NuxtLink 
            v-if="isAuthenticated" 
            to="/messages" 
            class="text-gray-700 hover:text-blue-600 transition"
          >
            消息
          </NuxtLink>
          
          <template v-if="isAuthenticated">
            <NuxtLink 
              to="/notifications" 
              class="relative text-gray-700 hover:text-blue-600 transition"
            >
              <UIcon name="heroicons:bell" class="w-6 h-6" />
              <span 
                v-if="unreadCount > 0" 
                class="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center"
              >
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </NuxtLink>
            
            <NuxtLink 
              to="/profile" 
              class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition"
            >
              <UIcon name="heroicons:user-circle" class="w-8 h-8" />
              <span>{{ user?.nickname || user?.email?.split('@')[0] }}</span>
            </NuxtLink>
            
            <UButton 
              @click="handleLogout" 
              variant="outline" 
              size="sm"
            >
              退出登录
            </UButton>
          </template>
          
          <template v-else>
            <NuxtLink 
              to="/login" 
              class="text-gray-700 hover:text-blue-600 transition"
            >
              登录
            </NuxtLink>
            <NuxtLink 
              to="/register" 
            >
              <UButton>
                注册
              </UButton>
            </NuxtLink>
          </template>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useNotificationStore } from '~/stores/notification'
import { useAuth } from '~/composables/useAuth'
import { useNotification } from '~/composables/useNotification'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const { logout } = useAuth()
const { fetchNotifications } = useNotification()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)
const unreadCount = computed(() => notificationStore.unreadCount)

const handleLogout = () => {
  logout()
  navigateTo('/')
}

onMounted(async () => {
  if (isAuthenticated.value) {
    try {
      await fetchNotifications()
    } catch (error) {
      console.error('Failed to fetch notifications on mount:', error)
    }
  }
})
</script>
