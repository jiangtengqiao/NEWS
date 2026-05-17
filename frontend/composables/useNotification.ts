import { useNotificationStore } from '~/stores/notification'

export function useNotification() {
    const notificationStore = useNotificationStore()
    const { $api } = useNuxtApp()

    async function fetchNotifications() {
        try {
            notificationStore.setLoading(true)
            const response = await $api('/notifications')
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
            await $api(`/notifications/${notificationId}/read`, {
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
            await $api('/notifications/read-all', {
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
            await $api(`/notifications/${notificationId}`, {
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
