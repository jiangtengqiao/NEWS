import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { News, Category, NewsComment, NewsFavorite } from '~/types'

export const useNewsStore = defineStore('news', () => {
    const news = ref<News[]>([])
    const categories = ref<Category[]>([])
    const currentNews = ref<News | null>(null)
    const favorites = ref<NewsFavorite[]>([])
    const loading = ref(false)
    const currentCategory = ref<string | null>(null)
    const searchQuery = ref<string>('')

    const filteredNews = computed(() => {
        let filtered = news.value
        if (currentCategory.value) {
            filtered = filtered.filter(n => n.category === currentCategory.value)
        }
        if (searchQuery.value) {
            const query = searchQuery.value.toLowerCase()
            filtered = filtered.filter(n => 
                n.title.toLowerCase().includes(query) || 
                (n.summary && n.summary.toLowerCase().includes(query))
            )
        }
        return filtered
    })

    const favoriteNewsIds = computed(() => 
        new Set(favorites.value.map(f => f.newsId))
    )

    function setNews(data: News[]) {
        news.value = data
    }

    function setCategories(data: Category[]) {
        categories.value = data
    }

    function setCurrentNews(newsItem: News | null) {
        currentNews.value = newsItem
    }

    function setFavorites(data: NewsFavorite[]) {
        favorites.value = data
    }

    function addFavorite(favorite: NewsFavorite) {
        if (!favorites.value.find(f => f.id === favorite.id)) {
            favorites.value.push(favorite)
        }
    }

    function removeFavorite(favoriteId: string) {
        favorites.value = favorites.value.filter(f => f.id !== favoriteId)
    }

    function setCategory(category: string | null) {
        currentCategory.value = category
    }

    function setSearch(query: string) {
        searchQuery.value = query
    }

    function setLoading(state: boolean) {
        loading.value = state
    }

    return {
        news,
        categories,
        currentNews,
        favorites,
        loading,
        currentCategory,
        searchQuery,
        filteredNews,
        favoriteNewsIds,
        setNews,
        setCategories,
        setCurrentNews,
        setFavorites,
        addFavorite,
        removeFavorite,
        setCategory,
        setSearch,
        setLoading
    }
})
