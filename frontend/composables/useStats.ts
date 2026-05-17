import { useStatsStore } from '~/stores/stats'

export function useStats() {
    const statsStore = useStatsStore()
    const { $api } = useNuxtApp()

    async function fetchStats() {
        try {
            statsStore.setLoading(true)
            const response = await $api('/stats')
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
