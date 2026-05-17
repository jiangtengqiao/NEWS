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
const authStore = useAuthStore()
const { logout } = useAuth()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

const handleLogout = () => {
  logout()
  navigateTo('/')
}
</script>
