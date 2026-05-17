<template>
    <div class="bg-gray-50 min-h-screen">
        <AppHeader />
        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- 搜索和筛选区域 -->
            <div class="mb-8">
                <div class="flex flex-col md:flex-row gap-4 mb-6">
                    <div class="flex-1">
                        <UInput 
                            v-model="searchQuery" 
                            placeholder="搜索新闻..." 
                            @input="handleSearch"
                        />
                    </div>
                    <USelect 
                        v-model="selectedCategory" 
                        :options="categoryOptions"
                        placeholder="选择分类"
                        class="w-full md:w-48"
                    />
                </div>
            </div>

            <!-- 新闻列表 -->
            <div v-if="loading" class="flex justify-center py-12">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
            <div v-else-if="newsStore.filteredNews.length === 0" class="text-center py-12">
                <div class="text-gray-500 mb-4">
                    <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v8H7V8z"></path>
                    </svg>
                </div>
                <p class="text-gray-600 text-lg">没有找到新闻</p>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div 
                    v-for="newsItem in newsStore.filteredNews" 
                    :key="newsItem.id"
                    class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
                    @click="goToDetail(newsItem.id)"
                >
                    <div class="relative h-48 bg-gray-200">
                        <img 
                            v-if="newsItem.imageUrl" 
                            :src="newsItem.imageUrl" 
                            :alt="newsItem.title"
                            class="w-full h-full object-cover"
                        />
                        <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-600">
                            <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                        </div>
                        <div class="absolute top-4 left-4">
                            <span v-if="newsItem.category" class="bg-blue-600 text-white text-xs px-2 py-1 rounded">
                                {{ getCategoryDisplayName(newsItem.category) }}
                            </span>
                        </div>
                    </div>
                    <div class="p-4">
                        <h3 class="font-semibold text-lg text-gray-900 mb-2 line-clamp-2">
                            {{ newsItem.title }}
                        </h3>
                        <p v-if="newsItem.summary" class="text-gray-600 text-sm mb-3 line-clamp-3">
                            {{ newsItem.summary }}
                        </p>
                        <div class="flex items-center justify-between text-sm text-gray-500">
                            <div class="flex items-center gap-2">
                                <span v-if="newsItem.author">{{ newsItem.author }}</span>
                                <span>{{ formatDate(newsItem.publishedAt) }}</span>
                            </div>
                            <div class="flex items-center gap-3">
                                <span class="flex items-center gap-1">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                                    </svg>
                                    {{ newsItem.viewCount }}
                                </span>
                                <span class="flex items-center gap-1">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                                    </svg>
                                    {{ newsItem.likeCount }}
                                </span>
                                <span class="flex items-center gap-1">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                                    </svg>
                                    {{ newsItem.commentCount }}
                                </span>
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
import { useRouter } from 'vue-router'
import { useNews } from '~/composables/useNews'
import { useNewsStore } from '~/stores/news'

const router = useRouter()
const { fetchNews, fetchCategories } = useNews()
const newsStore = useNewsStore()

const searchQuery = ref('')
const selectedCategory = ref<string | null>(null)
const loading = ref(false)

const categoryOptions = computed(() => [
    { label: '全部分类', value: null },
    ...newsStore.categories.map(cat => ({ label: cat.displayName, value: cat.name }))
])

function getCategoryDisplayName(categoryName: string) {
    const category = newsStore.categories.find(c => c.name === categoryName)
    return category?.displayName || categoryName
}

function formatDate(dateStr: string) {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    })
}

function goToDetail(newsId: string) {
    router.push(`/news/${newsId}`)
}

async function handleSearch() {
    newsStore.setSearch(searchQuery.value)
    await loadNews()
}

async function loadNews() {
    loading.value = true
    try {
        await fetchNews(0, 20, selectedCategory.value || undefined, searchQuery.value || undefined)
    } finally {
        loading.value = false
    }
}

onMounted(async () => {
    await Promise.all([
        fetchCategories(),
        loadNews()
    ])
})
</script>
