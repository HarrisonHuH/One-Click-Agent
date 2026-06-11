/**
 * 一点灵光 - 侧边栏导航
 * 暗色风格，含 LOGO、导航菜单和底部用户信息
 */
import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useUserStore } from '@/stores/userStore'
import './Sidebar.css'

// 导航菜单项
const MENU_ITEMS = [
  { key: 'create', icon: '🎬', label: '创作工作台', path: '/create' },
  { key: 'projects', icon: '📁', label: '我的项目', path: '/projects' },
  { key: 'videos', icon: '▶', label: '我的视频', path: '/videos' },
  { key: 'skills', icon: '🧠', label: 'Skill 知识库', path: '/skills' },
  { key: 'templates', icon: '🧩', label: '模板市场', path: '/templates' },
  { key: 'quality', icon: '🎯', label: '质量评估', path: '/quality' },
  { key: 'api', icon: '🔌', label: 'API 接口', path: '/api-docs' },
  { key: 'help', icon: '❓', label: '帮助文档', path: '/help' },
  { key: 'settings', icon: '⚙', label: '设置中心', path: '/settings' }
]

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  free: '免费版',
  creator: '创作者',
  professional: '专业版'
}

const Sidebar: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user } = useUserStore()

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="logo-icon">
          <svg viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="14" fill="url(#logoGrad)" />
            <circle cx="16" cy="16" r="6" fill="#111827" />
            <circle cx="16" cy="16" r="3" fill="url(#logoGrad)" />
            <defs>
              <linearGradient id="logoGrad" x1="0" y1="0" x2="32" y2="32">
                <stop offset="0%" stopColor="#8b5cf6" />
                <stop offset="100%" stopColor="#6366f1" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div className="logo-text">
          <div className="logo-title">One-Click</div>
          <div className="logo-subtitle">智能视频生成系统</div>
        </div>
      </div>

      {/* 新建视频创作按钮 */}
      <button className="new-project-btn" onClick={() => navigate('/create')}>
        <span className="plus-icon">+</span>
        <span>新建视频创作</span>
      </button>

      {/* 导航菜单 */}
      <nav className="sidebar-nav">
        {MENU_ITEMS.map((item) => {
          const isActive = location.pathname === item.path ||
            (item.path === '/projects' && location.pathname.startsWith('/task'))
          return (
            <div
              key={item.key}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => navigate(item.path)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </div>
          )
        })}
      </nav>

      {/* 底部用户信息 */}
      {user && (
        <div className="sidebar-footer">
          <div className="user-card">
            <img
              className="user-avatar"
              src={user.avatar_url || 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=anime%20boy%20avatar%20cute%20chinese%20style&image_size=square'}
              alt={user.nickname}
            />
            <div className="user-info">
              <div className="user-name-row">
                <span className="user-name">{user.nickname}</span>
                <span className="user-badge">{ACCOUNT_TYPE_LABELS[user.account_type] || '创作者'}</span>
              </div>
            </div>
          </div>
          <div className="user-stats">
            <div className="stat-row">
              <span className="stat-label">账户余额</span>
              <span className="stat-value">{user.credits.toFixed(2)} 元</span>
            </div>
            <div className="stat-row">
              <span className="stat-label">剩余生成时长</span>
              <span className="stat-value">{user.remaining_minutes} 分钟</span>
            </div>
          </div>
        </div>
      )}
    </aside>
  )
}

export default Sidebar
