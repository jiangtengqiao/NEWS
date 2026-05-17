<template>
    <div class="bg-gray-50 min-h-screen">
        <AppHeader />
        <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- 返回按钮 -->
            <button 
                @click="goBack"
                class="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
                返回
            </button>

            <div v-if="loading" class="flex justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>

            <div v-else-if="!news" class="text-center py-12">
                <p class="text-gray-600 text-lg">新闻未找到</p>
            </div>

            <div v-else class="bg-white rounded-lg shadow-lg overflow-hidden">
                <!-- 封面图 -->
                <div class="relative h-64 md:h-96 bg-gray-200">
                    <img 
                        v-if="news.imageUrl" 
                        :src="news.imageUrl" 
                        :alt="news.title"
                        class="w-full h-full object-cover"
                    />
                    <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600">
                        <svg class="w-24 h-24 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                    </div>
                    <div class="absolute top-6 left-6">
                        <span v-if="news.category" class="bg-blue-600 text-white text-sm px-3 py-1 rounded">
                            {{ getCategoryDisplayName(news.category) }}
                        </span>
                    </div>
                </div>

                <!-- 内容区域 -->
                <div class="p-6 md:p-10">
                    <h1 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                        {{ news.title }}
                    </h1>

                    <!-- 作者和日期 -->
                    <div class="flex flex-wrap items-center gap-4 text-gray-600 mb-6 pb-6 border-b">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                                {{ (news.author || 'A').charAt(0).toUpperCase() }}
                            </div>
                            <span>{{ news.author || '匿名作者' }}</span>
                        </div>
                        <span>•</span>
                        <span>{{ formatDate(news.publishedAt) }}</span>
                        <div class="flex items-center gap-2 ml-auto">
                            <span class="flex items-center gap-1">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                </svg>
                                {{ news.viewCount }}
                            </span>
                        </div>
                    </div>

                    <!-- 标签 -->
                    <div v-if="news.tags && news.tags.length > 0" class="flex flex-wrap gap-2 mb-6">
                        <span 
                            v-for="tag in news.tags" 
                            :key="tag"
                            class="bg-gray-100 text-gray-700 text-xs px-3 py-1 rounded-full"
                        >
                            #{{ tag }}
                        </span>
                    </div>

                    <!-- 摘要 -->
                    <div v-if="news.summary" class="bg-gray-50 p-4 rounded-lg mb-6 border-l-4 border-blue-500">
                        <p class="text-gray-700 italic">{{ news.summary }}</p>
                    </div>

                    <!-- 主要内容 -->
                    <article class="prose max-w-none mb-10">
                        <p class="text-gray-800 leading-relaxed whitespace-pre-wrap">
                            {{ news.content }}
                        </p>
                    </article>

                    <!-- 互动按钮 -->
                    <div class="flex items-center gap-4 pt-6 border-t">
                        <button 
                            @click="handleLike"
                            :class="[
                                'flex items-center gap-2 px-4 py-2 rounded-lg transition',
                                isLiked ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            ]"
                        >
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path>
                            </svg>
                            <span>{{ likeCount }}</span>
                        </button>
                        <button 
                            @click="handleAddFavorite"
                            :class="[
                                'flex items-center gap-2 px-4 py-2 rounded-lg transition',
                                isFavorited ? 'bg-yellow-100 text-yellow-600' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            ]"
                        >
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                            </svg>
                            <span>{{ isFavorited ? '已收藏' : '收藏' }}</span>
                        </button>
                    </div>

                    <!-- 评论区 -->
                    <div class="mt-10 pt-8 border-t">
                        <h3 class="text-xl font-semibold text-gray-900 mb-6">评论 ({{ comments.length }})</h3>
                        
                        <!-- 添加评论 -->
                        <div class="mb-8">
                            <UTextarea 
                                v-model="newComment" 
                                placeholder="写下你的评论..." 
                                rows="3"
                                class="mb-3"
                            />
                            <div class="flex justify-end">
                                <UButton @click="handleAddComment" :loading="addingComment">
                                    发表评论
                                </UButton>
                            </div>
                        </div>

                        <!-- 评论列表 -->
                        <div v-if="comments.length === 0" class="text-center text-gray-500 py-8">
                            暂无评论，来发表第一个吧！
                        </div>
                        <div v-else class="space-y-6">
                            <div 
                                v-for="comment in comments" 
                                :key="comment.id"
                                class="flex gap-3"
                            >
                                <div class="w-10 h-10 bg-blue-500 rounded-full flex-shrink-0 flex items-center justify-center text-white font-semibold">
                                    U
                                </div>
                                <div class="flex-1">
                                    <div class="flex items-center gap-2 mb-1">
                                        <span class="font-medium text-gray-900">用户</span>
                                        <span class="text-sm text-gray-500">{{ formatDate(comment.createdAt) }}</span>
                                    </div>
                                    <p class="text-gray-700">{{ comment.content }}</p>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNews } from '~/composables/useNews'
import { useNewsStore } from '~/stores/news'
import { useAuthStore } from '~/stores/auth'

const router = useRouter()
const route = useRoute()
const { 
    fetchNewsById, 
    recordRead, 
    toggleLike, 
    fetchFavorites, 
    addFavorite, 
    removeFavorite, 
    fetchComments, 
    addComment 
} = useNews()
const newsStore = useNewsStore()
const authStore = useAuthStore()

const loading = ref(false)
const addingComment = ref(false)
const newComment = ref('')
const comments = ref<any[]>([])
const isLiked = ref(false)
const likeCount = ref(0)

const news = computed(() => newsStore.currentNews)
const isFavorited = computed(() => {
    if (!news.value) return false
    return newsStore.favoriteNewsIds.has(news.value.id)
})

function getCategoryDisplayName(categoryName: string) {
    const category = newsStore.categories.find(c => c.name === categoryName)
    return category?.displayName || categoryName
}

function formatDate(dateStr: string) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

function goBack() {
    router.push('/')
}

async function handleLike() {
    if (!news.value) return
    try {
        const result = await toggleLike(news.value.id)
        isLiked.value = result.liked
        likeCount.value += result.liked ? 1 : -1
    } catch (error) {
        console.error('Failed to like:', error)
    }
}

async function handleAddFavorite() {
    if (!news.value) return
    try {
        if (isFavorited.value) {
            const favorite = newsStore.favorites.find(f => f.newsId === news.value!.id)
            if (favorite) {
                await removeFavorite(favorite.id)
            }
        } else {
            await addFavorite(news.value.id)
        }
    } catch (error) {
        console.error('Failed to favorite:', error)
    }
}

async function handleAddComment() {
    if (!newComment.value.trim() || !news.value) return
    try {
        addingComment.value = true
        await addComment(news.value.id, newComment.value)
        newComment.value = ''
        await loadComments()
    } catch (error) {
        console.error('Failed to add comment:', error)
    } finally {
        addingComment.value = false
    }
}

async function loadComments() {
    if (!news.value) return
    try {
        comments.value = await fetchComments(news.value.id)
    } catch (error) {
        console.error('Failed to load comments:', error)
    }
}

onMounted(async () => {
    const newsId = route.params.id as string
    loading.value = true
    try {
        await Promise.all([
            fetchNewsById(newsId),
            fetchFavorites()
        ])
        
        if (news.value) {
            await recordRead(news.value.id)
            likeCount.value = news.value.likeCount
            await loadComments()
        }
    } catch (error) {
        console.error('Failed to load news:', error)
    } finally {
        loading.value = false
    }
})
</script>
