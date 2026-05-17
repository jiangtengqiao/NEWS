<template>
    <div class="bg-gray-50 min-h-screen">
        <AppHeader />
        <main class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div class="flex items-center justify-between mb-6">
                <h1 class="text-2xl font-bold text-gray-900">通知</h1>
                <UButton 
                    v-if="unreadCount > 0" 
                    size="sm" 
                    variant="outline"
                    @click="handleMarkAllAsRead"
                >
                    全部标记为已读
                </UButton>
            </div>

            <div v-if="loading" class="flex justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <div v-else-if="notifications.length === 0" class="text-center py-12">
                <UIcon name="heroicons:inbox" class="w-16 h-16 mx-auto text-gray-300 mb-4" />
                <p class="text-gray-600 text-lg">暂无通知</p>
            </div>

            <div v-else class="space-y-4">
                <div 
                    v-for="notification in notifications" 
                    :key="notification.id"
                    @click="handleNotificationClick(notification)"
                    class="bg-white rounded-lg shadow p-4 cursor-pointer transition hover:shadow-md"
                    :class="{
                        'bg-blue-50': !notification.read,
                        'bg-gray-50': notification.read
                    }"
                >
                    <div class="flex items-start gap-4">
                        <div class="flex-shrink-0">
                            <div 
                                class="w-10 h-10 rounded-full flex items-center justify-center"
                                :class="getIconClass(notification.type)"
                            >
                                <UIcon :name="getIconName(notification.type)" class="w-5 h-5 text-white" />
                            </div>
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center justify-between mb-1">
                                <p class="font-medium text-gray-900">
                                    {{ notification.title }}
                                </p>
                                <button 
                                    @click.stop="handleDelete(notification.id)"
                                    class="text-gray-400 hover:text-red-500 transition"
                                >
                                    <UIcon name="heroicons:x-mark" class="w-4 h-4" />
                                </button>
                            </div>
                            <p class="text-gray-600 text-sm mb-2">{{ notification.content }}</p>
                            <p class="text-gray-400 text-xs">{{ formatDate(notification.createdAt) }}</p>
                        </div>
                        <div v-if="!notification.read" class="flex-shrink-0">
                            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '~/stores/notification'
import { useNotification } from '~/composables/useNotification'

const router = useRouter()
const notificationStore = useNotificationStore()
const { fetchNotifications, markAsRead, markAllAsRead, deleteNotification } = useNotification()

const notifications = computed(() => notificationStore.notifications)
const loading = computed(() => notificationStore.loading)
const unreadCount = computed(() => notificationStore.unreadCount)

function getIconClass(type: string) {
    const classes: Record<string, string> = {
        'like': 'bg-red-500',
        'comment': 'bg-green-500',
        'favorite': 'bg-yellow-500',
        'follow': 'bg-blue-500',
        'system': 'bg-purple-500'
    }
    return classes[type] || 'bg-gray-500'
}

function getIconName(type: string) {
    const icons: Record<string, string> = {
        'like': 'heroicons:heart',
        'comment': 'heroicons:chat-bubble',
        'favorite': 'heroicons:star',
        'follow': 'heroicons:user-plus',
        'system': 'heroicons:bell'
    }
    return icons[type] || 'heroicons:bell'
}

function formatDate(dateStr: string) {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    
    if (minutes < 1) return '刚刚'
    if (minutes < 60) return `${minutes}分钟前`
    if (hours < 24) return `${hours}小时前`
    if (days < 7) return `${days}天前`
    
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

async function handleNotificationClick(notification: any) {
    if (!notification.read) {
        await markAsRead(notification.id)
    }
    
    if (notification.relatedType === 'news' && notification.relatedId) {
        router.push(`/news/${notification.relatedId}`)
    }
}

async function handleMarkAllAsRead() {
    try {
        await markAllAsRead()
    } catch (error) {
        console.error('Failed to mark all as read:', error)
    }
}

async function handleDelete(notificationId: string) {
    try {
        await deleteNotification(notificationId)
    } catch (error) {
        console.error('Failed to delete notification:', error)
    }
}

onMounted(async () => {
    try {
        await fetchNotifications()
    } catch (error) {
        console.error('Failed to fetch notifications:', error)
    }
})
</script>
