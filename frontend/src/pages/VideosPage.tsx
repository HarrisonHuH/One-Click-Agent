/**
 * 一点灵光 - 我的视频页面
 * 展示所有成功生成的作品
 */
import React, { useEffect, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTaskList, deleteTask, getTaskResultUrl } from '@/services/api'
import type { TaskListItem } from '@/types'
import StatusBadge from '@/components/ui/StatusBadge'
import Button from '@/components/ui/Button'
import { formatTime } from '@/utils/format'
import './VideosPage.css'

const VideosPage: React.FC = () => {
  const navigate = useNavigate()

  const [videos, setVideos] = useState<TaskListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

  const fetchVideos = useCallback(async () => {
    setLoading(true)
    try {
      const res = await getTaskList({ page: 1, limit: 50, status: 'SUCCESS' })
      setVideos(res.data.items)
    } catch (err) {
      setError('加载失败')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchVideos()
  }, [fetchVideos])

  const handleDelete = async (taskId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!window.confirm('确定要删除该视频吗？')) return
    try {
      await deleteTask(taskId)
      setVideos(videos.filter(v => v.task_id !== taskId))
    } catch (err) {
      alert('删除失败')
    }
  }

  return (
    <div className="videos-page">
      <div className="page-header-block">
        <h1 className="page-main-title">我的视频</h1>
        <p className="page-desc">展示您所有已成功生成的视频作品</p>
      </div>

      <div className="videos-toolbar">
        <div className="videos-stats">
          共 <strong>{videos.length}</strong> 个视频
        </div>
        <div className="videos-actions">
          <div className="view-toggle">
            <button
              className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
            >⊞</button>
            <button
              className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
            >☰</button>
          </div>
          <Button variant="primary" onClick={() => navigate('/create')}>
            + 新建视频
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="state-block">
          <div className="spinner-large" />
          <p>加载中...</p>
        </div>
      ) : error ? (
        <div className="state-block">
          <p className="error-text">{error}</p>
          <Button onClick={fetchVideos}>重试</Button>
        </div>
      ) : videos.length === 0 ? (
        <div className="state-block empty">
          <div className="empty-icon">🎬</div>
          <p>还没有视频作品</p>
          <Button variant="gradient" onClick={() => navigate('/create')}>
            去创作
          </Button>
        </div>
      ) : (
        <div className={`videos-${viewMode}`}>
          {videos.map(video => (
            <div
              key={video.task_id}
              className="video-card"
              onClick={() => navigate(`/task/${video.task_id}`)}
            >
              <div className="video-thumb">
                <img src={video.thumbnail_url || ''} alt={video.title} />
                <div className="video-overlay">
                  <div className="play-icon">▶</div>
                </div>
                <span className="video-duration">{video.duration_display}</span>
              </div>
              <div className="video-info">
                <h4 className="video-title">{video.title}</h4>
                <div className="video-meta">
                  <span className="meta-item">{video.style}</span>
                  <span className="meta-item">{video.resolution}</span>
                </div>
                <div className="video-time">{formatTime(video.created_at)}</div>
              </div>
              <div className="video-actions">
                <button
                  className="action-btn"
                  onClick={(e) => {
                    e.stopPropagation()
                    const a = document.createElement('a')
                    a.href = getTaskResultUrl(video.task_id)
                    a.download = `${video.title}.mp4`
                    a.click()
                  }}
                  title="下载"
                >📥</button>
                <button
                  className="action-btn danger"
                  onClick={(e) => handleDelete(video.task_id, e)}
                  title="删除"
                >🗑</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default VideosPage
