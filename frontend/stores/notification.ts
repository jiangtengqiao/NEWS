import { defineStore } from 'pinia'
import type { Notification } from '~/types'

interface NotificationState {
    notifications: Notification[]
    loading: boolean
    unreadCount: number
}

export const useNotificationStore = defineStore('notification', {
    state: (): NotificationState => ({
        notifications: [],
        loading: false,
        unreadCount: 0
    }),

    actions: {
        setNotifications(notifications: Notification[]) {
            this.notifications = notifications
            this.updateUnreadCount()
        },

        addNotification(notification: Notification) {
            this.notifications.unshift(notification)
            this.updateUnreadCount()
        },

        markAsRead(notificationId: string) {
            const notification = this.notifications.find(n => n.id === notificationId)
            if (notification && !notification.read) {
                notification.read = true
                notification.readAt = new Date().toISOString()
                this.updateUnreadCount()
            }
        },

        markAllAsRead() {
            this.notifications.forEach(n => {
                if (!n.read) {
                    n.read = true
                    n.readAt = new Date().toISOString()
                }
            })
            this.updateUnreadCount()
        },

        removeNotification(notificationId: string) {
            const index = this.notifications.findIndex(n => n.id === notificationId)
            if (index !== -1) {
                this.notifications.splice(index, 1)
                this.updateUnreadCount()
            }
        },

        updateUnreadCount() {
            this.unreadCount = this.notifications.filter(n => !n.read).length
        },

        setLoading(loading: boolean) {
            this.loading = loading
        }
    }
})
