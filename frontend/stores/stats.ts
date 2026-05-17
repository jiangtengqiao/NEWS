import { defineStore } from 'pinia'
import type { UserActivityStat } from '~/types'

export const useStatsStore = defineStore('stats', {
    state: () => ({
        stats: null as UserActivityStat | null,
        loading: false
    }),

    actions: {
        setStats(stats: UserActivityStat) {
            this.stats = stats
        },

        setLoading(loading: boolean) {
            this.loading = loading
        }
    }
})
