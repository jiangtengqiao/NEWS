export interface User {
    id: string
    email: string
    nickname?: string
    avatarUrl?: string
    isVerified: boolean
    isSubscribed: boolean
    createdAt: string
}

export interface UserCode {
    code: string
}

export interface Message {
    id: string
    senderId: string
    receiverId: string
    content: string
    isRead: boolean
    createdAt: string
}

export interface Friendship {
    id: string
    userId: string
    friendId: string
    status: 'pending' | 'accepted' | 'rejected'
    createdAt: string
}

export interface LoginRequest {
    email: string
    password: string
}

export interface RegisterRequest {
    email: string
    password: string
    nickname?: string
}

export interface Token {
    accessToken: string
    tokenType: string
}

export interface UpdateUserRequest {
    nickname?: string
    avatarUrl?: string
    gender?: string
    birthday?: string
    bio?: string
}

// 新闻相关类型
export interface Category {
    id: string
    name: string
    displayName: string
    icon?: string
    priority: number
    createdAt: string
}

export interface News {
    id: string
    title: string
    content: string
    summary?: string
    source?: string
    author?: string
    imageUrl?: string
    category?: string
    tags?: string[]
    publishedAt: string
    viewCount: number
    likeCount: number
    commentCount: number
    createdAt: string
    updatedAt: string
}

export interface NewsComment {
    id: string
    userId: string
    newsId: string
    content: string
    parentCommentId?: string
    createdAt: string
}

export interface NewsFavorite {
    id: string
    userId: string
    newsId: string
    createdAt: string
}

export interface NewsRead {
    id: string
    userId: string
    newsId: string
    readAt: string
    readDuration?: number
}

// 高级功能类型
export interface Notification {
    id: string
    userId: string
    type: string
    title: string
    content?: string
    relatedId?: string
    relatedType?: string
    read: boolean
    readAt?: string
    createdAt: string
}

export interface UserSetting {
    id: string
    userId: string
    notificationLike: boolean
    notificationComment: boolean
    notificationFavorite: boolean
    notificationFollow: boolean
    notificationSystem: boolean
    createdAt: string
    updatedAt: string
}

export interface UserActivityStat {
    id: string
    userId: string
    newsRead: number
    newsLiked: number
    newsFavorited: number
    commentsPosted: number
    date: string
    createdAt: string
}

export interface UserSettings {
    id: string
    userId: string
    emailNotifications: boolean
    pushNotifications: boolean
    publicProfile: boolean
    allowFriendRequests: boolean
    showOnlineStatus: boolean
    language: string
    theme: string
    createdAt: string
    updatedAt: string
}

export interface UserActivityStats {
    id: string
    userId: string
    date: string
    newsReadCount: number
    commentCount: number
    likeCount: number
    friendRequestCount: number
    messageCount: number
    createdAt: string
}

export interface ReadingStats {
    totalRead: number
}
