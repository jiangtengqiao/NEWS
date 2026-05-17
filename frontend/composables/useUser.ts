import type { User, UpdateUserRequest, UserCode, Friendship, Message } from '~/types'

export function useUser() {
  const { apiFetch } = useAuth()
  const toast = useToast()

  async function updateProfile(data: UpdateUserRequest): Promise<User> {
    try {
      const response = await apiFetch<User>('/api/users/me', {
        method: 'PUT',
        body: data
      })
      toast.add({
        title: '个人信息更新成功',
        color: 'green'
      })
      return response
    } catch (error) {
      toast.add({
        title: '更新失败',
        color: 'red'
      })
      throw error
    }
  }

  async function getUserById(userId: string): Promise<User> {
    return await apiFetch<User>(`/api/users/${userId}`)
  }

  async function getUserByCode(code: string): Promise<User> {
    return await apiFetch<User>(`/api/users/code/${code}`)
  }

  async function getMyCode(): Promise<UserCode> {
    return await apiFetch<UserCode>('/api/users/me/code')
  }

  async function uploadAvatar(file: File): Promise<{ avatar_url: string }> {
    const formData = new FormData()
    formData.append('file', file)
    return await apiFetch('/api/users/me/avatar', {
      method: 'POST',
      body: formData
    })
  }

  return {
    updateProfile,
    getUserById,
    getUserByCode,
    getMyCode,
    uploadAvatar
  }
}

export function useFriends() {
  const { apiFetch } = useAuth()
  const toast = useToast()

  async function getFriends(): Promise<Friendship[]> {
    return await apiFetch<Friendship[]>('/api/friends')
  }

  async function getFriendRequests(): Promise<Friendship[]> {
    return await apiFetch<Friendship[]>('/api/friends/requests')
  }

  async function sendFriendRequest(friendId: string): Promise<Friendship> {
    try {
      const response = await apiFetch<Friendship>(`/api/friends/request/${friendId}`, {
        method: 'POST'
      })
      toast.add({
        title: '好友请求已发送',
        color: 'green'
      })
      return response
    } catch (error) {
      toast.add({
        title: '发送失败',
        color: 'red'
      })
      throw error
    }
  }

  async function acceptFriendRequest(requestId: string): Promise<Friendship> {
    try {
      const response = await apiFetch<Friendship>(`/api/friends/request/${requestId}/accept`, {
        method: 'PUT'
      })
      toast.add({
        title: '已接受好友请求',
        color: 'green'
      })
      return response
    } catch (error) {
      toast.add({
        title: '操作失败',
        color: 'red'
      })
      throw error
    }
  }

  async function rejectFriendRequest(requestId: string): Promise<void> {
    try {
      await apiFetch(`/api/friends/request/${requestId}/reject`, {
        method: 'PUT'
      })
      toast.add({
        title: '已拒绝好友请求',
        color: 'blue'
      })
    } catch (error) {
      toast.add({
        title: '操作失败',
        color: 'red'
      })
      throw error
    }
  }

  return {
    getFriends,
    getFriendRequests,
    sendFriendRequest,
    acceptFriendRequest,
    rejectFriendRequest
  }
}

export function useMessages() {
  const { apiFetch } = useAuth()

  async function getMessages(): Promise<Message[]> {
    return await apiFetch<Message[]>('/api/messages')
  }

  async function getConversation(userId: string): Promise<Message[]> {
    return await apiFetch<Message[]>(`/api/messages/${userId}`)
  }

  async function sendMessage(receiverId: string, content: string): Promise<Message> {
    return await apiFetch<Message>('/api/messages', {
      method: 'POST',
      body: { receiverId, content }
    })
  }

  async function markAsRead(messageId: string): Promise<Message> {
    return await apiFetch<Message>(`/api/messages/${messageId}/read`, {
      method: 'PUT'
    })
  }

  return {
    getMessages,
    getConversation,
    sendMessage,
    markAsRead
  }
}
