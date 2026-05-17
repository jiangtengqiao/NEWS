import { defineStore } from 'pinia'
import type { UserSetting } from '~/types'

export const useSettingsStore = defineStore('settings', {
    state: () => ({
        settings: null as UserSetting | null,
        loading: false
    }),

    actions: {
        setSettings(settings: UserSetting) {
            this.settings = settings
        },

        updateSettings(updates: Partial<UserSetting>) {
            if (this.settings) {
                this.settings = { ...this.settings, ...updates }
            }
        },

        setLoading(loading: boolean) {
            this.loading = loading
        }
    }
})
