/**
 * 一点灵光 - 顶部栏
 * 包含返回按钮、面包屑、通知、文档链接、主题切换
 */
import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import './TopBar.css'

const TopBar: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  // 标题映射
  const getTitle = () => {
    const path = location.pathname
    if (path === '/' || path === '/create') return '创作工作台'
    if (path === '/projects') return '我的项目'
    if (path === '/videos') return '我的视频'
    if (path.startsWith('/task/')) return '生成视频'
    if (path === '/settings') return '设置中心'
    if (path === '/api-docs') return 'API 接口'
    if (path === '/help') return '帮助文档'
    if (path === '/quality') return '质量评估'
    if (path === '/templates') return '模板市场'
    if (path === '/skills') return 'Skill 知识库'
    return '一点灵光'
  }

  return (
    <header className="top-bar">
      <div className="top-bar-left">
        <h1 className="page-title">{getTitle()}</h1>
      </div>

      <div className="top-bar-right">
        {/* 通知按钮 */}
        <button className="top-bar-btn" title="通知">
          <span className="btn-icon">🔔</span>
          <span className="notification-dot" />
        </button>

        {/* 文档链接 */}
        <button className="top-bar-btn doc-btn" onClick={() => navigate('/help')}>
          <span className="btn-icon">📖</span>
          <span>文档</span>
        </button>

        {/* 主题切换 */}
        <button className="top-bar-btn" title="主题">
          <span className="btn-icon">☀</span>
        </button>
      </div>
    </header>
  )
}

export default TopBar
