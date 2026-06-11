/**
 * 一点灵光 - 主布局组件
 * 暗色侧边栏 + 浅色主内容区
 */
import React, { useEffect } from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'
import { useUserStore } from '@/stores/userStore'
import { getUserInfo } from '@/services/api'
import './MainLayout.css'

const MainLayout: React.FC = () => {
  const navigate = useNavigate()
  const { user, setUser } = useUserStore()

  // 加载用户信息
  useEffect(() => {
    if (!user) {
      getUserInfo()
        .then((res) => setUser(res.data))
        .catch((err) => console.error('Failed to load user info', err))
    }
  }, [user, setUser])

  return (
    <div className="main-layout">
      <Sidebar />
      <div className="layout-content">
        <TopBar />
        <div className="layout-main scrollbar-thin">
          <Outlet />
        </div>
      </div>
    </div>
  )
}

export default MainLayout
