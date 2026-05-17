import { useSettingsStore } from '~/stores/settings'

export function useSettings() {
    const settingsStore = useSettingsStore()
    const { $api } = useNuxtApp()

    async function fetchSettings() {
        try {
            settingsStore.setLoading(true)
            const response = await $api('/settings')
            settingsStore.setSettings(response.settings)
            return response.settings
        } catch (error) {
            console.error('Failed to fetch settings:', error)
            throw error
        } finally {
            settingsStore.setLoading(false)
        }
    }

    async function updateSettings(updates: Partial<any>) {
        try {
            const response = await $api('/settings', {
                method: 'PUT',
                body: updates
            })
            settingsStore.updateSettings(response.settings)
            return response.settings
        } catch (error) {
            console.error('Failed to update settings:', error)
            throw error
        }
    }

    return {
        fetchSettings,
        updateSettings
    }
}
