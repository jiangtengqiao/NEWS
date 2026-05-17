<template>
  <div>
    <AppHeader />
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="p-4 border-b bg-gray-50 flex items-center space-x-3">
          <UButton @click="$router.back()" variant="outline" size="sm">
            <UIcon name="heroicons:arrow-left" class="w-5 h-5 mr-2" />
            返回
          </UButton>
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
              {{ 'U' }}
            </div>
            <div>
              <p class="font-medium">用户 #{{ userId.substring(0, 8) }}</p>
              <p class="text-xs text-gray-500">在线</p>
            </div>
          </div>
        </div>
        
        <!-- 消息列表 -->
        <div class="p-4 h-96 overflow-y-auto space-y-4">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            class="flex"
            :class="message.senderId === authStore.user?.id ? 'justify-end' : 'justify-start'"
          >
            <div 
              class="max-w-xs px-4 py-2 rounded-lg"
              :class="message.senderId === authStore.user?.id ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-900'"
            >
              <p>{{ message.content }}</p>
              <p class="text-xs mt-1 opacity-70 text-right">
                {{ formatTime(message.createdAt) }}
              </p>
            </div>
          </div>
          
          <div v-if="messages.length === 0" class="text-center text-gray-500 py-8">
            暂无消息，开始聊天吧！
          </div>
        </div>
        
        <!-- 发送消息 -->
        <div class="p-4 border-t">
          <form @submit.prevent="sendMessage" class="flex space-x-2">
            <UInput
              v-model="newMessage"
              placeholder="输入消息..."
              class="flex-1"
            />
            <UButton type="submit" :loading="sending">
              发送
            </UButton>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const { getConversation, sendMessage: sendMessageApi } = useMessages()

const route = useRoute()
const userId = computed(() => route.params.userId as string)
const messages = ref([])
const newMessage = ref('')
const sending = ref(false)

const loadMessages = async () => {
  if (!userId.value) return
  
  try {
    messages.value = await getConversation(userId.value)
  } catch (error) {
    console.error('Failed to load conversation:', error)
  }
}

onMounted(() => {
  loadMessages()
})

watch(userId, () => {
  loadMessages()
})

const sendMessage = async () => {
  if (!newMessage.value.trim() || !userId.value) return
  
  try {
    sending.value = true
    await sendMessageApi(userId.value, newMessage.value)
    newMessage.value = ''
    await loadMessages()
  } catch (error) {
    console.error('Failed to send message:', error)
  } finally {
    sending.value = false
  }
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  return date.toLocaleDateString('zh-CN')
}
</script>
