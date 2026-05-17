import { useNotificationStore } from '~/stores/notification'
import { useAuth } from '~/composables/useAuth'

export function useNotification() {
    const notificationStore = useNotificationStore()
    const { apiFetch } = useAuth()

    async function fetchNotifications() {
        try {
            notificationStore.setLoading(true)
            const response = await apiFetch<{ notifications: any[] }>('/api/notifications')
            notificationStore.setNotifications(response.notifications)
            return response.notifications
        } catch (error) {
            console.error('Failed to fetch notifications:', error)
            throw error
        } finally {
            notificationStore.setLoading(false)
        }
    }

    async function markAsRead(notificationId: string) {
        try {
            await apiFetch(`/api/notifications/${notificationId}/read`, {
                method: 'POST'
            })
            notificationStore.markAsRead(notificationId)
        } catch (error) {
            console.error('Failed to mark as read:', error)
            throw error
        }
    }

    async function markAllAsRead() {
        try {
            await apiFetch('/api/notifications/read-all', {
                method: 'POST'
            })
            notificationStore.markAllAsRead()
        } catch (error) {
            console.error('Failed to mark all as read:', error)
            throw error
        }
    }

    async function deleteNotification(notificationId: string) {
        try {
            await apiFetch(`/api/notifications/${notificationId}`, {
                method: 'DELETE'
            })
            notificationStore.removeNotification(notificationId)
        } catch (error) {
            console.error('Failed to delete notification:', error)
            throw error
        }
    }

    return {
        fetchNotifications,
        markAsRead,
        markAllAsRead,
        deleteNotification
    }
}
