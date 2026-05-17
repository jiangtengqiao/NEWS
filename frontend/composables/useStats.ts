import { useStatsStore } from '~/stores/stats'
import { useAuth } from '~/composables/useAuth'

export function useStats() {
    const statsStore = useStatsStore()
    const { apiFetch } = useAuth()

    async function fetchStats() {
        try {
            statsStore.setLoading(true)
            const response = await apiFetch<{ stats: any }>('/api/stats')
            statsStore.setStats(response.stats)
            return response.stats
        } catch (error) {
            console.error('Failed to fetch stats:', error)
            throw error
        } finally {
            statsStore.setLoading(false)
        }
    }

    return {
        fetchStats
    }
}
