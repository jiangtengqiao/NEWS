<template>
  <div>
    <AppHeader />
    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">好友</h1>
        <UButton @click="showAddFriendModal = true">
          <UIcon name="heroicons:plus" class="w-5 h-5 mr-2" />
          添加好友
        </UButton>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- 好友请求 -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">好友请求</h2>
          <div v-if="friendRequests.length === 0" class="text-center text-gray-500 py-8">
            暂无好友请求
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="request in friendRequests" 
              :key="request.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div>
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                    {{ 'U' }}
                  </div>
                  <span class="font-medium">用户 #{{ request.id.substring(0, 8) }}</span>
                </div>
                <p class="text-sm text-gray-500">{{ formatDate(request.createdAt) }}</p>
              </div>
              <div class="flex space-x-2">
                <UButton 
                  size="sm" 
                  color="green"
                  @click="acceptRequest(request.id)"
                >
                  接受
                </UButton>
                <UButton 
                  size="sm" 
                  variant="outline"
                  @click="rejectRequest(request.id)"
                >
                  拒绝
                </UButton>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 好友列表 -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">我的好友</h2>
          <div v-if="friends.length === 0" class="text-center text-gray-500 py-8">
            暂无好友，快去添加吧！
          </div>
          <div v-else class="space-y-4">
            <div 
              v-for="friendship in friends" 
              :key="friendship.id"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                  {{ 'F' }}
                </div>
                <div>
                  <p class="font-medium">好友 #{{ getFriendId(friendship).substring(0, 8) }}</p>
                  <p class="text-sm text-gray-500">{{ formatDate(friendship.createdAt) }}</p>
                </div>
              </div>
              <NuxtLink :to="`/messages/${getFriendId(friendship)}`">
                <UButton size="sm" variant="outline">
                  发消息
                </UButton>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 添加好友模态框 -->
    <UModal v-model="showAddFriendModal">
      <div class="p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">添加好友</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">输入好友码</label>
            <UInput
              v-model="friendCode"
              placeholder="输入好友码"
              size="lg"
            />
          </div>
          <div class="flex space-x-4">
            <UButton 
              @click="showAddFriendModal = false" 
              variant="outline"
              class="flex-1"
            >
              取消
            </UButton>
            <UButton 
              @click="addFriend" 
              :loading="addingFriend"
              class="flex-1"
            >
              添加
            </UButton>
          </div>
        </div>
      </div>
    </UModal>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const { getFriends, getFriendRequests, sendFriendRequest, acceptFriendRequest, rejectFriendRequest } = useFriends()
const { getUserByCode } = useUser()

const showAddFriendModal = ref(false)
const friendCode = ref('')
const addingFriend = ref(false)
const friends = ref([])
const friendRequests = ref([])

const loadData = async () => {
  try {
    friends.value = await getFriends()
    friendRequests.value = await getFriendRequests()
  } catch (error) {
    console.error('Failed to load friends:', error)
  }
}

onMounted(() => {
  loadData()
})

const getFriendId = (friendship) => {
  return friendship.userId === authStore.user?.id ? friendship.friendId : friendship.userId
}

const acceptRequest = async (requestId) => {
  try {
    await acceptFriendRequest(requestId)
    await loadData()
  } catch (error) {
    console.error('Failed to accept request:', error)
  }
}

const rejectRequest = async (requestId) => {
  try {
    await rejectFriendRequest(requestId)
    await loadData()
  } catch (error) {
    console.error('Failed to reject request:', error)
  }
}

const addFriend = async () => {
  if (!friendCode.value.trim()) return
  
  try {
    addingFriend.value = true
    const friend = await getUserByCode(friendCode.value)
    await sendFriendRequest(friend.id)
    showAddFriendModal.value = false
    friendCode.value = ''
  } catch (error) {
    console.error('Failed to add friend:', error)
    const toast = useToast()
    toast.add({
      title: '添加失败',
      description: '请检查好友码是否正确',
      color: 'red'
    })
  } finally {
    addingFriend.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}
</script>
