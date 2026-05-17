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
