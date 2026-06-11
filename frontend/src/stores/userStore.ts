/**
 * 一点灵光 - 全局状态管理
 */
import { create } from 'zustand'
import type { UserInfo } from '@/types'

interface UserState {
  user: UserInfo | null
  setUser: (user: UserInfo) => void
  updateUser: (partial: Partial<UserInfo>) => void
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  updateUser: (partial) => set((state) => ({
    user: state.user ? { ...state.user, ...partial } : null
  }))
}))
