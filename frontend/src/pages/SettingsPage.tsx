/**
 * 一点灵光 - 设置中心
 * 对应设计图：左侧设置分类 + 右侧设置内容
 */
import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useUserStore } from '@/stores/userStore'
import { updateUserInfo } from '@/services/api'
import Button from '@/components/ui/Button'
import './SettingsPage.css'

// 设置分类
const SETTINGS_TABS = [
  { key: 'account', icon: '👤', label: '账户设置', desc: '管理个人信息和安全' },
  { key: 'preferences', icon: '🎛', label: '偏好设置', desc: '自定义界面与创作偏好' },
  { key: 'notifications', icon: '🔔', label: '通知设置', desc: '配置系统通知与提醒方式' },
  { key: 'security', icon: '🛡', label: '安全设置', desc: '密码修改与登录保护' },
  { key: 'billing', icon: '💳', label: '套餐与支付', desc: '查看套餐信息与消费记录' },
  { key: 'team', icon: '👥', label: '团队管理', desc: '管理团队成员与权限' },
  { key: 'api', icon: '<>', label: 'API 设置', desc: '管理 API 密钥与调用限制' },
  { key: 'system', icon: '⚙', label: '系统设置', desc: '系统版本与功能开关' }
]

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  free: '免费版',
  creator: '创作者',
  professional: '专业版'
}

const SettingsPage: React.FC = () => {
  const { tab } = useParams<{ tab?: string }>()
  const navigate = useNavigate()
  const { user, updateUser } = useUserStore()

  const [activeTab, setActiveTab] = useState(tab || 'account')

  useEffect(() => {
    if (tab) setActiveTab(tab)
  }, [tab])

  const handleTabClick = (key: string) => {
    setActiveTab(key)
    navigate(`/settings/${key}`)
  }

  return (
    <div className="settings-page">
      {/* 页面标题 */}
      <div className="page-header-block">
        <h1 className="page-main-title">设置中心</h1>
        <p className="page-desc">管理您的账户、偏好设置和系统配置</p>
      </div>

      <div className="settings-content">
        {/* 左侧分类 */}
        <div className="settings-sidebar">
          {SETTINGS_TABS.map((item) => (
            <div
              key={item.key}
              className={`settings-nav-item ${activeTab === item.key ? 'active' : ''}`}
              onClick={() => handleTabClick(item.key)}
            >
              <div className="settings-nav-icon">{item.icon}</div>
              <div className="settings-nav-text">
                <div className="settings-nav-label">{item.label}</div>
                <div className="settings-nav-desc">{item.desc}</div>
              </div>
            </div>
          ))}
        </div>

        {/* 右侧内容 */}
        <div className="settings-main">
          {activeTab === 'account' && <AccountSettings user={user} onUpdate={updateUser} />}
          {activeTab === 'preferences' && <PreferencesSettings />}
          {activeTab === 'notifications' && <NotificationSettings />}
          {activeTab === 'security' && <SecuritySettings />}
          {activeTab === 'billing' && <BillingSettings user={user} />}
          {activeTab !== 'account' && activeTab !== 'preferences' &&
           activeTab !== 'notifications' && activeTab !== 'security' &&
           activeTab !== 'billing' && <PlaceholderTab name={SETTINGS_TABS.find(t => t.key === activeTab)?.label || ''} />}
        </div>
      </div>
    </div>
  )
}

// ========== 账户设置 ==========
const AccountSettings: React.FC<{ user: any; onUpdate: (data: any) => void }> = ({ user, onUpdate }) => {
  const [nickname, setNickname] = useState(user?.nickname || '')
  const [email, setEmail] = useState(user?.email || '')
  const [bio, setBio] = useState(user?.bio || '')
  const [saving, setSaving] = useState(false)

  const handleSave = async () => {
    setSaving(true)
    try {
      await updateUserInfo({ nickname, email, bio })
      onUpdate({ nickname, email, bio })
      alert('保存成功')
    } catch (err) {
      alert('保存失败')
    } finally {
      setSaving(false)
    }
  }

  return (
    <>
      <div className="settings-card">
        <h2 className="settings-section-title">个人信息</h2>
        <div className="form-grid">
          <div className="form-item">
            <label className="form-label">头像</label>
            <div className="avatar-section">
              <img
                className="avatar-large"
                src={user?.avatar_url || 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=anime%20boy%20avatar%20cute%20chinese%20style&image_size=square'}
                alt=""
              />
              <div className="avatar-info">
                <Button variant="secondary" size="sm">更换头像</Button>
                <p className="form-hint">支持 JPG、PNG 格式，大小不超过 5MB</p>
              </div>
            </div>
          </div>

          <div className="form-item">
            <label className="form-label">昵称</label>
            <div className="input-with-counter">
              <input
                className="form-input"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                maxLength={20}
              />
              <span className="counter">{nickname.length}/20</span>
            </div>
          </div>

          <div className="form-item">
            <label className="form-label">邮箱</label>
            <div className="input-with-button">
              <input
                className="form-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type="email"
              />
              <Button variant="secondary" size="sm">更换邮箱</Button>
            </div>
          </div>

          <div className="form-item">
            <label className="form-label">个人简介</label>
            <div className="input-with-counter">
              <textarea
                className="form-textarea"
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                maxLength={200}
                rows={3}
                placeholder="一句话介绍下自己..."
              />
              <span className="counter">{bio.length}/200</span>
            </div>
          </div>
        </div>

        <div className="settings-actions">
          <Button variant="primary" loading={saving} onClick={handleSave}>
            保存更改
          </Button>
        </div>
      </div>

      <div className="settings-card">
        <h2 className="settings-section-title">账户信息</h2>
        <div className="info-rows">
          <div className="info-row">
            <span className="info-label">用户 ID</span>
            <div className="info-right">
              <span className="info-text">{user?.user_code || 'U_20240516000123'}</span>
              <Button variant="ghost" size="sm">复制</Button>
            </div>
          </div>
          <div className="info-row">
            <span className="info-label">注册时间</span>
            <span className="info-text">2024-05-16 10:30:45</span>
          </div>
          <div className="info-row">
            <span className="info-label">账户类型</span>
            <div className="info-right">
              <span className="type-badge">{ACCOUNT_TYPE_LABELS[user?.account_type] || '创作者'}</span>
              <span className="info-text">当前套餐：{ACCOUNT_TYPE_LABELS[user?.account_type] || '专业版'}</span>
              <Button variant="ghost" size="sm">查看套餐</Button>
            </div>
          </div>
          <div className="info-row">
            <span className="info-label">账户余额</span>
            <div className="info-right">
              <span className="info-text">{(user?.credits || 128.50).toFixed(2)} 元</span>
              <Button variant="ghost" size="sm">充值</Button>
            </div>
          </div>
          <div className="info-row">
            <span className="info-label">剩余生成时长</span>
            <div className="info-right">
              <span className="info-text">{user?.remaining_minutes || 320} 分钟</span>
              <Button variant="ghost" size="sm">查看详情 ›</Button>
            </div>
          </div>
        </div>
      </div>

      <div className="settings-card">
        <h2 className="settings-section-title">快捷操作</h2>
        <div className="quick-actions">
          <div className="quick-action-item">
            <div className="quick-action-icon">🔒</div>
            <div className="quick-action-text">
              <div className="quick-action-label">修改密码</div>
              <div className="quick-action-desc">定期修改密码，保障账户安全</div>
            </div>
            <span className="quick-action-arrow">›</span>
          </div>
          <div className="quick-action-item">
            <div className="quick-action-icon">📱</div>
            <div className="quick-action-text">
              <div className="quick-action-label">登录设备管理</div>
              <div className="quick-action-desc">查看和管理已登录的设备</div>
            </div>
            <span className="quick-action-arrow">›</span>
          </div>
          <div className="quick-action-item">
            <div className="quick-action-icon">📤</div>
            <div className="quick-action-text">
              <div className="quick-action-label">导出我的数据</div>
              <div className="quick-action-desc">导出我的创作数据与项目信息</div>
            </div>
            <span className="quick-action-arrow">›</span>
          </div>
          <div className="quick-action-item danger">
            <div className="quick-action-icon">🗑</div>
            <div className="quick-action-text">
              <div className="quick-action-label">注销账户</div>
              <div className="quick-action-desc">永久删除账户及所有数据</div>
            </div>
            <span className="quick-action-arrow">›</span>
          </div>
        </div>
      </div>
    </>
  )
}

// ========== 偏好设置 ==========
const PreferencesSettings: React.FC = () => {
  const [theme, setTheme] = useState('light')
  const [language, setLanguage] = useState('zh-CN')
  const [defaultStyle, setDefaultStyle] = useState('电影感')
  const [defaultDuration, setDefaultDuration] = useState(60)

  return (
    <div className="settings-card">
      <h2 className="settings-section-title">偏好设置</h2>
      <div className="form-grid">
        <div className="form-item">
          <label className="form-label">界面主题</label>
          <div className="option-pills">
            {[{ v: 'light', l: '浅色' }, { v: 'dark', l: '深色' }, { v: 'auto', l: '跟随系统' }].map(o => (
              <button
                key={o.v}
                className={`pill ${theme === o.v ? 'active' : ''}`}
                onClick={() => setTheme(o.v)}
              >{o.l}</button>
            ))}
          </div>
        </div>

        <div className="form-item">
          <label className="form-label">语言</label>
          <select className="form-input" value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="zh-CN">简体中文</option>
            <option value="zh-TW">繁體中文</option>
            <option value="en-US">English</option>
            <option value="ja-JP">日本語</option>
          </select>
        </div>

        <div className="form-item">
          <label className="form-label">默认视频风格</label>
          <select className="form-input" value={defaultStyle} onChange={(e) => setDefaultStyle(e.target.value)}>
            <option>电影感</option>
            <option>短剧</option>
            <option>小红书</option>
            <option>广告</option>
            <option>旅拍</option>
          </select>
        </div>

        <div className="form-item">
          <label className="form-label">默认视频时长</label>
          <select className="form-input" value={defaultDuration} onChange={(e) => setDefaultDuration(Number(e.target.value))}>
            <option value={15}>15秒</option>
            <option value={30}>30秒</option>
            <option value={60}>60秒</option>
            <option value={90}>90秒</option>
          </select>
        </div>
      </div>

      <div className="settings-actions">
        <Button variant="primary">保存设置</Button>
      </div>
    </div>
  )
}

// ========== 通知设置 ==========
const NotificationSettings: React.FC = () => {
  const [notifs, setNotifs] = useState({
    taskComplete: true,
    taskFailed: true,
    weeklyReport: false,
    productUpdate: true,
    emailNotif: true,
    pushNotif: true
  })

  const toggle = (key: keyof typeof notifs) => {
    setNotifs({ ...notifs, [key]: !notifs[key] })
  }

  return (
    <div className="settings-card">
      <h2 className="settings-section-title">通知设置</h2>
      <div className="notif-list">
        {[
          { key: 'taskComplete', label: '任务完成通知', desc: '视频生成完成时通知我' },
          { key: 'taskFailed', label: '任务失败通知', desc: '任务失败时立即通知我' },
          { key: 'weeklyReport', label: '每周报告', desc: '每周一发送创作统计报告' },
          { key: 'productUpdate', label: '产品更新', desc: '新功能与产品更新公告' }
        ].map(item => (
          <div key={item.key} className="notif-item">
            <div className="notif-text">
              <div className="notif-label">{item.label}</div>
              <div className="notif-desc">{item.desc}</div>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={notifs[item.key as keyof typeof notifs]}
                onChange={() => toggle(item.key as keyof typeof notifs)}
              />
              <span className="switch-slider" />
            </label>
          </div>
        ))}
      </div>

      <h2 className="settings-section-title" style={{ marginTop: 32 }}>通知方式</h2>
      <div className="notif-list">
        {[
          { key: 'emailNotif', label: '邮件通知', desc: '通过电子邮件发送通知' },
          { key: 'pushNotif', label: '站内消息', desc: '通过站内消息中心通知' }
        ].map(item => (
          <div key={item.key} className="notif-item">
            <div className="notif-text">
              <div className="notif-label">{item.label}</div>
              <div className="notif-desc">{item.desc}</div>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={notifs[item.key as keyof typeof notifs]}
                onChange={() => toggle(item.key as keyof typeof notifs)}
              />
              <span className="switch-slider" />
            </label>
          </div>
        ))}
      </div>

      <div className="settings-actions">
        <Button variant="primary">保存设置</Button>
      </div>
    </div>
  )
}

// ========== 安全设置 ==========
const SecuritySettings: React.FC = () => {
  return (
    <div className="settings-card">
      <h2 className="settings-section-title">密码修改</h2>
      <div className="form-grid">
        <div className="form-item">
          <label className="form-label">当前密码</label>
          <input className="form-input" type="password" placeholder="请输入当前密码" />
        </div>
        <div className="form-item">
          <label className="form-label">新密码</label>
          <input className="form-input" type="password" placeholder="至少 8 位，包含字母和数字" />
        </div>
        <div className="form-item">
          <label className="form-label">确认新密码</label>
          <input className="form-input" type="password" placeholder="请再次输入新密码" />
        </div>
      </div>
      <div className="settings-actions">
        <Button variant="primary">更新密码</Button>
      </div>
    </div>
  )
}

// ========== 套餐与支付 ==========
const BillingSettings: React.FC<{ user: any }> = ({ user }) => {
  return (
    <>
      <div className="settings-card">
        <h2 className="settings-section-title">当前套餐</h2>
        <div className="plan-card">
          <div className="plan-header">
            <div>
              <div className="plan-name">{ACCOUNT_TYPE_LABELS[user?.account_type] || '创作者'}</div>
              <div className="plan-desc">适合个人创作者使用</div>
            </div>
            <Button variant="primary">升级套餐</Button>
          </div>
          <div className="plan-stats">
            <div className="plan-stat">
              <div className="plan-stat-label">已使用</div>
              <div className="plan-stat-value">86 / 320 分钟</div>
            </div>
            <div className="plan-stat">
              <div className="plan-stat-label">余额</div>
              <div className="plan-stat-value">{(user?.credits || 128.50).toFixed(2)} 元</div>
            </div>
            <div className="plan-stat">
              <div className="plan-stat-label">到期时间</div>
              <div className="plan-stat-value">2025-05-16</div>
            </div>
          </div>
        </div>
      </div>

      <div className="settings-card">
        <h2 className="settings-section-title">消费记录</h2>
        <div className="empty-state-small">
          <p>暂无消费记录</p>
        </div>
      </div>
    </>
  )
}

// ========== 占位Tab ==========
const PlaceholderTab: React.FC<{ name: string }> = ({ name }) => {
  return (
    <div className="settings-card">
      <h2 className="settings-section-title">{name}</h2>
      <div className="empty-state-small">
        <p>{name} 功能开发中</p>
      </div>
    </div>
  )
}

export default SettingsPage
