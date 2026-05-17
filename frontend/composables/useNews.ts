import type { News, Category, NewsComment, NewsFavorite } from '~/types'
import { useAuth } from '~/composables/useAuth'
import { useNewsStore } from '~/stores/news'

export function useNews() {
    const { apiFetch } = useAuth()
    const newsStore = useNewsStore()

    async function fetchNews(skip = 0, limit = 20, category?: string, search?: string) {
        newsStore.setLoading(true)
        try {
            let url = `/api/news/?skip=${skip}&limit=${limit}`
            if (category) {
                url += `&category=${category}`
            }
            if (search) {
                url += `&search=${encodeURIComponent(search)}`
            }
            const data = await apiFetch<News[]>(url)
            
            const converted = data.map(item => ({
                ...item,
                imageUrl: item.imageUrl || (item as any).image_url,
                publishedAt: item.publishedAt || (item as any).published_at,
                viewCount: item.viewCount || (item as any).view_count,
                likeCount: item.likeCount || (item as any).like_count,
                commentCount: item.commentCount || (item as any).comment_count,
                createdAt: item.createdAt || (item as any).created_at,
                updatedAt: item.updatedAt || (item as any).updated_at
            }))
            newsStore.setNews(converted)
            return converted
        } catch (error) {
            console.error('Failed to fetch news:', error)
            throw error
        } finally {
            newsStore.setLoading(false)
        }
    }

    async function fetchCategories() {
        try {
            const data = await apiFetch<Category[]>('/api/news/categories')
            newsStore.setCategories(data)
            return data
        } catch (error) {
            console.error('Failed to fetch categories:', error)
            throw error
        }
    }

    async function fetchNewsById(newsId: string) {
        try {
            const data = await apiFetch<News>(`/api/news/${newsId}`)
            const converted = {
                ...data,
                imageUrl: data.imageUrl || (data as any).image_url,
                publishedAt: data.publishedAt || (data as any).published_at,
                viewCount: data.viewCount || (data as any).view_count,
                likeCount: data.likeCount || (data as any).like_count,
                commentCount: data.commentCount || (data as any).comment_count,
                createdAt: data.createdAt || (data as any).created_at,
                updatedAt: data.updatedAt || (data as any).updated_at
            }
            newsStore.setCurrentNews(converted)
            return converted
        } catch (error) {
            console.error('Failed to fetch news:', error)
            throw error
        }
    }

    async function recordRead(newsId: string) {
        try {
            return await apiFetch(`/api/news/${newsId}/read`, {
                method: 'POST'
            })
        } catch (error) {
            console.error('Failed to record read:', error)
            throw error
        }
    }

    async function toggleLike(newsId: string) {
        try {
            const result = await apiFetch<{ liked: boolean }>(`/api/news/${newsId}/like`, {
                method: 'POST'
            })
            return result
        } catch (error) {
            console.error('Failed to toggle like:', error)
            throw error
        }
    }

    async function fetchFavorites() {
        try {
            const data = await apiFetch<NewsFavorite[]>('/api/news/favorites')
            newsStore.setFavorites(data)
            return data
        } catch (error) {
            console.error('Failed to fetch favorites:', error)
            throw error
        }
    }

    async function addFavorite(newsId: string) {
        try {
            const data = await apiFetch<NewsFavorite>('/api/news/favorites', {
                method: 'POST',
                body: { newsId }
            })
            newsStore.addFavorite(data)
            return data
        } catch (error) {
            console.error('Failed to add favorite:', error)
            throw error
        }
    }

    async function removeFavorite(favoriteId: string) {
        try {
            await apiFetch(`/api/news/favorites/${favoriteId}`, {
                method: 'DELETE'
            })
            newsStore.removeFavorite(favoriteId)
        } catch (error) {
            console.error('Failed to remove favorite:', error)
            throw error
        }
    }

    async function fetchComments(newsId: string) {
        try {
            return await apiFetch<NewsComment[]>(`/api/news/${newsId}/comments`)
        } catch (error) {
            console.error('Failed to fetch comments:', error)
            throw error
        }
    }

    async function addComment(newsId: string, content: string, parentCommentId?: string) {
        try {
            return await apiFetch<NewsComment>('/api/news/comments', {
                method: 'POST',
                body: { newsId, content, parentCommentId }
            })
        } catch (error) {
            console.error('Failed to add comment:', error)
            throw error
        }
    }

    return {
        fetchNews,
        fetchCategories,
        fetchNewsById,
        recordRead,
        toggleLike,
        fetchFavorites,
        addFavorite,
        removeFavorite,
        fetchComments,
        addComment
    }
}
