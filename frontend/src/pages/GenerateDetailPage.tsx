/**
 * 一点灵光 - 生成详情页
 * 对应设计图：
 * - 顶部 5 步骤进度（输入创意→剧本生成→分镜设计→生成中→完成）
 * - 左侧 6 阶段任务进度（剧本解析/分镜处理/素材生成/视频合成/音频生成/画面优化/导出视频）
 * - 右侧 实时预览视频 + 生成信息 + 生成日志
 */
import React, { useEffect, useState, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTaskStatus, getTaskResultUrl, getTaskLogs, getTaskThumbnailUrl } from '@/services/api'
import type { TaskStatusData, GenerationLogItem, StageProgress } from '@/types'
import StepProgress from '@/components/ui/StepProgress'
import Button from '@/components/ui/Button'
import { formatTime } from '@/utils/format'
import './GenerateDetailPage.css'

// 5 步骤
const STEPS = [
  { key: 'idea', label: '输入创意' },
  { key: 'script', label: '剧本生成' },
  { key: 'storyboard', label: '分镜设计' },
  { key: 'generating', label: '生成中' },
  { key: 'done', label: '完成' }
]

// 阶段图标映射
const STAGE_ICONS: Record<string, string> = {
  SCRIPT_PARSING: '📄',
  STORYBOARD: '🖼',
  ASSET_GENERATION: '🎨',
  VIDEO_SYNTHESIS: '🎬',
  AUDIO_GENERATION: '🎵',
  IMAGE_OPTIMIZATION: '✨',
  VIDEO_EXPORT: '📤',
  COMPLETED: '✓'
}

const GenerateDetailPage: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>()
  const navigate = useNavigate()

  const [taskStatus, setTaskStatus] = useState<TaskStatusData | null>(null)
  const [logs, setLogs] = useState<GenerationLogItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 防止组件卸载后更新状态
  const mountedRef = useRef(true)

  // 加载状态
  const fetchStatus = useCallback(async () => {
    if (!taskId) return
    try {
      const res = await getTaskStatus(taskId)
      if (mountedRef.current) {
        setTaskStatus(res.data)
        setError(null)
      }
    } catch (err) {
      console.error(err)
      if (mountedRef.current) setError('加载失败')
    } finally {
      if (mountedRef.current) setLoading(false)
    }
  }, [taskId])

  // 加载日志
  const fetchLogs = useCallback(async () => {
    if (!taskId) return
    try {
      const res = await getTaskLogs(taskId)
      if (mountedRef.current) setLogs(res.data)
    } catch (err) {
      console.error(err)
    }
  }, [taskId])

  // 初始加载 + 轮询
  useEffect(() => {
    mountedRef.current = true
    fetchStatus()
    fetchLogs()

    const interval = setInterval(() => {
      if (taskStatus?.status === 'PROCESSING' || taskStatus?.status === 'PENDING') {
        fetchStatus()
        fetchLogs()
      }
    }, 3000)

    return () => {
      mountedRef.current = false
      clearInterval(interval)
    }
  }, [fetchStatus, fetchLogs, taskStatus?.status])

  if (loading) {
    return (
      <div className="state-center">
        <div className="spinner-large" />
        <p>加载中...</p>
      </div>
    )
  }

  if (error || !taskStatus) {
    return (
      <div className="state-center">
        <p className="error-text">{error || '任务不存在'}</p>
        <Button onClick={() => navigate('/projects')}>返回项目</Button>
      </div>
    )
  }

  // 根据状态计算 5 步骤进度
  const getStepIndex = () => {
    if (taskStatus.status === 'SUCCESS') return 4
    if (taskStatus.status === 'FAILED') return 3
    if (taskStatus.status === 'PROCESSING') return 3
    return 0
  }

  // 是否完成
  const isSuccess = taskStatus.status === 'SUCCESS'
  const isFailed = taskStatus.status === 'FAILED'

  return (
    <div className="generate-detail-page">
      {/* 顶部返回栏 */}
      <div className="back-bar">
        <button className="back-btn" onClick={() => navigate('/projects')}>
          ‹ 返回项目
        </button>
        <div className="title-row">
          <h2 className="detail-title">
            生成视频：{taskStatus.title || '未命名项目'}
            <button className="edit-btn" title="编辑">✏</button>
          </h2>
        </div>
        <div className="right-actions">
          <Button variant="secondary" size="sm">查看项目</Button>
          <Button variant="secondary" size="sm" icon={<span>↑</span>}>导出记录</Button>
        </div>
      </div>

      {/* 5 步骤进度 */}
      <div className="step-wrapper">
        <StepProgress
          steps={STEPS}
          currentIndex={getStepIndex()}
          status={isSuccess ? 'success' : isFailed ? 'failed' : 'processing'}
        />
      </div>

      {/* 主体双栏 */}
      <div className="detail-content">
        {/* 左侧：6 阶段进度 */}
        <div className="stages-panel">
          <div className="stages-header">
            <h3>生成进度</h3>
            {!isSuccess && !isFailed && (
              <div className="estimated-time">
                预计剩余时间：
                <span className="time-value">
                  {String(Math.floor(taskStatus.estimated_remaining_minutes / 60)).padStart(2, '0')}:
                  {String(taskStatus.estimated_remaining_minutes % 60).padStart(2, '0')}
                </span>
              </div>
            )}
          </div>
          <p className="stages-subtitle">
            {isSuccess ? '视频已生成完成！' :
             isFailed ? '生成失败，请重试' :
             'AI 正在为您生成视频，请稍候片刻'}
          </p>

          <div className="stage-list">
            {Object.values(taskStatus.stage_progress).map((stage) => (
              <StageItem
                key={stage.stage}
                stage={stage}
                isCurrent={stage.stage === taskStatus.current_stage}
              />
            ))}
          </div>

          {/* 小贴士 */}
          <div className="tip-box">
            <span className="tip-icon">💡</span>
            <span className="tip-text">
              小贴士：您可以离开此页面，生成完成后将通过站内通知告诉您
            </span>
          </div>
        </div>

        {/* 右侧：实时预览 + 信息 + 日志 */}
        <div className="preview-panel">
          <div className="preview-header">
            <h3>实时预览</h3>
            <span className="preview-hint">（开发中效果，最终效果可能会有差异）</span>
          </div>

          {/* 视频播放器 */}
          <div className="video-container">
            {isSuccess && taskStatus.video_url ? (
              <video
                src={getTaskResultUrl(taskId!)}
                poster={getTaskThumbnailUrl(taskId!)}
                controls
                autoPlay
                className="preview-video"
              >
                您的浏览器不支持视频播放
              </video>
            ) : isFailed ? (
              <div className="video-placeholder failed">
                <div className="placeholder-icon">😢</div>
                <p>生成失败</p>
                <p className="placeholder-sub">{taskStatus.error_message}</p>
              </div>
            ) : (
              <div className="video-placeholder">
                <img
                  src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cinematic%20night%20street%20rain%20young%20man%20petting%20stray%20cat%2C%20warm%20light%2C%20emotional%2C%20movie%20still&image_size=landscape_16_9"
                  alt="预览"
                  className="preview-image"
                />
                <div className="placeholder-overlay">
                  <div className="play-circle">▶</div>
                  <div className="preview-progress">
                    <div
                      className="preview-progress-fill"
                      style={{ width: `${taskStatus.overall_progress}%` }}
                    />
                  </div>
                  <div className="preview-time">
                    00:{String(Math.floor((taskStatus.overall_progress * 60) / 100)).padStart(2, '0')} / 01:00
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* 底部信息 + 日志 */}
          <div className="info-logs-grid">
            <div className="info-section">
              <h4>生成信息</h4>
              <div className="info-list">
                <div className="info-item">
                  <span className="info-label">视频名称</span>
                  <span className="info-value">{taskStatus.title || '雨夜的温暖'}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">视频时长</span>
                  <span className="info-value">01:00</span>
                </div>
                <div className="info-item">
                  <span className="info-label">分辨率</span>
                  <span className="info-value">1920 × 1080</span>
                </div>
                <div className="info-item">
                  <span className="info-label">生成模式</span>
                  <span className="info-value">电影感</span>
                </div>
                <div className="info-item">
                  <span className="info-label">创建时间</span>
                  <span className="info-value">2024-05-20 14:30:25</span>
                </div>
                <div className="info-item full">
                  <span className="info-label">创意描述</span>
                  <p className="info-desc">
                    一个年轻人在雨夜的街头遇到一只流浪猫，最终决定收养它的温暖故事，风格温馨治愈。
                  </p>
                </div>
                <div className="info-item full">
                  <span className="info-label">使用设置</span>
                  <div className="info-tags">
                    <span className="info-tag">电影感</span>
                    <span className="info-tag">60秒</span>
                    <span className="info-tag">16:9</span>
                    <span className="info-tag">1080P</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="logs-section">
              <div className="logs-header">
                <h4>生成日志</h4>
                <a className="logs-more">查看全部 ›</a>
              </div>
              <div className="logs-list">
                {logs.length === 0 ? (
                  <p className="logs-empty">暂无日志</p>
                ) : (
                  logs.slice(-12).map((log) => (
                    <div key={log.id} className="log-item">
                      <span className={`log-dot ${log.level.toLowerCase()}`} />
                      <span className="log-time">{formatTime(log.created_at, 'time')}</span>
                      <span className="log-message">{log.message}</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// 单个阶段项
interface StageItemProps {
  stage: StageProgress
  isCurrent: boolean
}

const StageItem: React.FC<StageItemProps> = ({ stage, isCurrent }) => {
  const isCompleted = stage.status === 'COMPLETED'
  const isFailed = stage.status === 'FAILED'
  const isProcessing = stage.status === 'PROCESSING' || isCurrent

  return (
    <div className={`stage-item ${isCompleted ? 'completed' : ''} ${isProcessing ? 'processing' : ''} ${isFailed ? 'failed' : ''}`}>
      <div className="stage-icon">
        {isCompleted ? '✓' : isFailed ? '✕' : STAGE_ICONS[stage.stage] || '○'}
      </div>
      <div className="stage-content">
        <div className="stage-label">{stage.label}</div>
        <div className="stage-desc">{stage.message || '等待开始'}</div>
        {isProcessing && stage.progress > 0 && stage.progress < 100 && (
          <div className="stage-progress">
            <div className="stage-progress-fill" style={{ width: `${stage.progress}%` }} />
          </div>
        )}
      </div>
      <div className="stage-status">
        {isCompleted && (
          <>
            <span className="status-text success">已完成</span>
            <span className="status-time">
              {stage.duration ? `00:${String(stage.duration).padStart(2, '0')}` : '00:08'}
            </span>
          </>
        )}
        {isProcessing && (
          <>
            <span className="status-text processing">
              {stage.progress}%
            </span>
            <span className="status-time">处理中</span>
          </>
        )}
        {isFailed && <span className="status-text failed">失败</span>}
        {!isCompleted && !isProcessing && !isFailed && (
          <span className="status-text pending">等待中</span>
        )}
      </div>
    </div>
  )
}

export default GenerateDetailPage
