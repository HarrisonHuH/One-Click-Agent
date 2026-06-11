/**
 * 一点灵光 - 我的项目页面
 * 对应设计图：状态筛选Tab + 搜索/排序 + 项目网格 + 分页
 */
import React, { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTaskList, deleteTask } from '@/services/api'
import type { TaskListItem, TaskStatusValue } from '@/types'
import StatusBadge from '@/components/ui/StatusBadge'
import Button from '@/components/ui/Button'
import { formatTime, timeAgo } from '@/utils/format'
import './ProjectsPage.css'

// 状态选项 - 对应设计图：全部项目/进行中/已完成/草稿/回收站
const STATUS_TABS: { key: string; label: string }[] = [
  { key: 'all', label: '全部项目' },
  { key: 'PROCESSING', label: '进行中' },
  { key: 'SUCCESS', label: '已完成' },
  { key: 'DRAFT', label: '草稿' },
  { key: 'RECYCLED', label: '回收站' }
]

// 排序选项
const SORT_OPTIONS = [
  { value: 'updated_desc', label: '最近更新时间' },
  { value: 'created_desc', label: '创建时间' },
  { value: 'duration_desc', label: '时长（长到短）' }
]

// 视图模式
type ViewMode = 'grid' | 'list'

const ProjectsPage: React.FC = () => {
  const navigate = useNavigate()

  // 状态
  const [tasks, setTasks] = useState<TaskListItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [statusTab, setStatusTab] = useState('all')
  const [keyword, setKeyword] = useState('')
  const [sortBy, setSortBy] = useState('updated_desc')
  const [viewMode, setViewMode] = useState<ViewMode>('grid')
  const [statusCounts, setStatusCounts] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const limit = 8

  // 加载任务列表
  const fetchTasks = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await getTaskList({
        page,
        limit,
        status: statusTab,
        keyword: keyword || undefined
      })
      setTasks(res.data.items)
      setTotal(res.data.total)
      setStatusCounts(res.data.status_counts)
    } catch (err) {
      console.error(err)
      setError('加载失败')
    } finally {
      setLoading(false)
    }
  }, [page, statusTab, keyword])

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  // 处理搜索
  const handleSearch = () => {
    setPage(1)
    fetchTasks()
  }

  // 处理删除（移到回收站）
  const handleDelete = async (taskId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!window.confirm('确定要删除该项目吗？')) return

    try {
      await deleteTask(taskId)
      fetchTasks()
    } catch (err) {
      alert('删除失败')
    }
  }

  // 总页数
  const totalPages = Math.max(1, Math.ceil(total / limit))

  return (
    <div className="projects-page">
      {/* 标题区 */}
      <div className="page-header-block">
        <h1 className="page-main-title">我的项目</h1>
        <p className="page-desc">管理你的所有视频创作项目，支持编辑、分享和端到端协作</p>
      </div>

      {/* 状态Tab */}
      <div className="status-tabs">
        {STATUS_TABS.map((tab) => {
          const count = tab.key === 'all'
            ? total
            : statusCounts[tab.key] || 0
          return (
            <button
              key={tab.key}
              className={`status-tab ${statusTab === tab.key ? 'active' : ''}`}
              onClick={() => { setStatusTab(tab.key); setPage(1) }}
            >
              {tab.label}
              <span className="tab-count">{count}</span>
            </button>
          )
        })}
      </div>

      {/* 工具栏 */}
      <div className="toolbar">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="搜索项目名称、描述或标签"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
        </div>

        <select
          className="sort-select"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          {SORT_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>

        <select className="sort-select" defaultValue="all">
          <option value="all">全部类型</option>
          <option value="idea">创意</option>
          <option value="script">剧本</option>
          <option value="novel">小说</option>
        </select>

        <div className="view-toggle">
          <button
            className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
            onClick={() => setViewMode('grid')}
            title="网格视图"
          >
            ⊞
          </button>
          <button
            className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
            onClick={() => setViewMode('list')}
            title="列表视图"
          >
            ☰
          </button>
        </div>

        <Button
          variant="gradient"
          icon={<span>+</span>}
          onClick={() => navigate('/create')}
        >
          新建项目
        </Button>
      </div>

      {/* 项目列表 */}
      {loading ? (
        <div className="state-block">
          <div className="spinner-large" />
          <p>加载中...</p>
        </div>
      ) : error ? (
        <div className="state-block">
          <p className="error-text">{error}</p>
          <Button onClick={fetchTasks}>重试</Button>
        </div>
      ) : tasks.length === 0 ? (
        <div className="state-block empty">
          <div className="empty-icon">📂</div>
          <p>暂无项目</p>
          <Button variant="primary" onClick={() => navigate('/create')}>
            去创建
          </Button>
        </div>
      ) : (
        <>
          <div className={`projects-${viewMode}`}>
            {tasks.map(task => (
              <ProjectCard
                key={task.task_id}
                task={task}
                onClick={() => navigate(`/task/${task.task_id}`)}
                onDelete={(e) => handleDelete(task.task_id, e)}
              />
            ))}
          </div>

          {/* 分页 */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="page-btn"
                disabled={page === 1}
                onClick={() => setPage(page - 1)}
              >
                ‹
              </button>
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .filter(p => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                .map((p, idx, arr) => (
                  <React.Fragment key={p}>
                    {idx > 0 && arr[idx - 1] !== p - 1 && (
                      <span className="page-ellipsis">...</span>
                    )}
                    <button
                      className={`page-num ${page === p ? 'active' : ''}`}
                      onClick={() => setPage(p)}
                    >
                      {p}
                    </button>
                  </React.Fragment>
                ))}
              <button
                className="page-btn"
                disabled={page === totalPages}
                onClick={() => setPage(page + 1)}
              >
                ›
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

// 项目卡片
interface ProjectCardProps {
  task: TaskListItem
  onClick: () => void
  onDelete: (e: React.MouseEvent) => void
}

const ProjectCard: React.FC<ProjectCardProps> = ({ task, onClick, onDelete }) => {
  // 状态类型映射
  const getStatusType = (status: TaskStatusValue) => {
    switch (status) {
      case 'SUCCESS': return 'success'
      case 'PROCESSING': return 'processing'
      case 'FAILED': return 'failed'
      case 'PENDING': return 'pending'
      case 'DRAFT': return 'draft'
      case 'RECYCLED': return 'recycled'
      default: return 'pending'
    }
  }

  return (
    <div className="project-card" onClick={onClick}>
      <div className="card-thumb">
        <img
          src={task.thumbnail_url || `https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(task.input_preview)}&image_size=landscape_16_9`}
          alt={task.title}
        />
        <div className="thumb-overlay">
          <div className="play-icon">▶</div>
        </div>
        <span className="thumb-duration">{task.duration_display}</span>
        <div className="thumb-status">
          <StatusBadge status={task.status_label} type={getStatusType(task.status)} />
        </div>
      </div>

      <div className="card-body">
        <h4 className="card-title">{task.title}</h4>
        <div className="card-tags">
          <span className="tag">{task.style}</span>
          {task.style_tags.slice(0, 2).map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
        <div className="card-meta">
          <span className="meta-time">更新于 {formatTime(task.updated_at, 'date')}</span>
          <div className="meta-right">
            {task.collaborators.length > 0 && (
              <div className="avatar-stack">
                {task.collaborators.slice(0, 2).map((c, i) => (
                  <img
                    key={i}
                    className="avatar"
                    src={`https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=avatar%20${i}&image_size=square`}
                    alt=""
                  />
                ))}
                {task.collaborators.length > 2 && (
                  <span className="avatar-more">+{task.collaborators.length - 2}</span>
                )}
              </div>
            )}
            <button className="more-btn" onClick={onDelete} title="删除">···</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProjectsPage
