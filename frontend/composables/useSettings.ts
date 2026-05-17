import { useSettingsStore } from '~/stores/settings'
import { useAuth } from '~/composables/useAuth'

export function useSettings() {
    const settingsStore = useSettingsStore()
    const { apiFetch } = useAuth()

    async function fetchSettings() {
        try {
            settingsStore.setLoading(true)
            const response = await apiFetch<{ settings: any }>('/api/settings')
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
            const response = await apiFetch<{ settings: any }>('/api/settings', {
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
