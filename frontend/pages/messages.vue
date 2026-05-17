<template>
  <div>
    <AppHeader />
    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">消息</h1>
      
      <div v-if="messages.length === 0" class="text-center text-gray-500 py-16 bg-white rounded-xl shadow-lg">
        <UIcon name="heroicons:chat-bubble-oval-left-right" class="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <h2 class="text-xl font-semibold mb-2">暂无消息</h2>
        <p>去添加好友开始聊天吧！</p>
        <NuxtLink to="/friends" class="mt-4 inline-block">
          <UButton>查看好友</UButton>
        </NuxtLink>
      </div>
      
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 对话列表 -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="p-4 border-b bg-gray-50">
              <h3 class="font-semibold text-gray-900">对话</h3>
            </div>
            <div class="divide-y">
              <div 
                v-for="(conversation, index) in conversations" 
                :key="index"
                class="p-4 hover:bg-gray-50 cursor-pointer transition"
                @click="selectConversation(conversation)"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                    {{ 'U' }}
                  </div>
                  <div class="flex-1">
                    <p class="font-medium">用户 #{{ conversation.userId.substring(0, 8) }}</p>
                    <p class="text-sm text-gray-500 truncate">{{ conversation.lastMessage }}</p>
                  </div>
                  <div class="text-xs text-gray-400">
                    {{ formatTime(conversation.lastTime) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 聊天区域 -->
        <div class="lg:col-span-2">
          <div v-if="selectedConversation" class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="p-4 border-b bg-gray-50 flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                  {{ 'U' }}
                </div>
                <div>
                  <p class="font-medium">用户 #{{ selectedConversation.userId.substring(0, 8) }}</p>
                  <p class="text-xs text-gray-500">在线</p>
                </div>
              </div>
            </div>
            
            <!-- 消息列表 -->
            <div class="p-4 h-96 overflow-y-auto space-y-4">
              <div 
                v-for="(message, index) in filteredMessages" 
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
          
          <div v-else class="bg-white rounded-xl shadow-lg p-16 text-center">
            <UIcon name="heroicons:chat-bubble-left-right" class="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p class="text-gray-500">选择一个对话开始聊天</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const { getMessages, getConversation, sendMessage: sendMessageApi } = useMessages()

const messages = ref([])
const conversations = ref([])
const selectedConversation = ref(null)
const filteredMessages = ref([])
const newMessage = ref('')
const sending = ref(false)

const loadData = async () => {
  try {
    messages.value = await getMessages()
    processConversations()
  } catch (error) {
    console.error('Failed to load messages:', error)
  }
}

const processConversations = () => {
  const convMap = new Map()
  
  for (const msg of messages.value) {
    const otherUserId = msg.senderId === authStore.user?.id ? msg.receiverId : msg.senderId
    
    if (!convMap.has(otherUserId) || new Date(msg.createdAt) > new Date(convMap.get(otherUserId).lastTime)) {
      convMap.set(otherUserId, {
        userId: otherUserId,
        lastMessage: msg.content,
        lastTime: msg.createdAt
      })
    }
  }
  
  conversations.value = Array.from(convMap.values())
    .sort((a, b) => new Date(b.lastTime) - new Date(a.lastTime))
}

onMounted(() => {
  loadData()
})

const selectConversation = async (conversation) => {
  selectedConversation.value = conversation
  try {
    filteredMessages.value = await getConversation(conversation.userId)
  } catch (error) {
    console.error('Failed to load conversation:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !selectedConversation.value) return
  
  try {
    sending.value = true
    await sendMessageApi(selectedConversation.value.userId, newMessage.value)
    newMessage.value = ''
    await loadData()
    if (selectedConversation.value) {
      await selectConversation(selectedConversation.value)
    }
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
