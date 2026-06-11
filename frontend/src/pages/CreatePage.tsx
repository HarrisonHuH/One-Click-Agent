/**
 * 一点灵光 - 创作工作台
 * 严格对照设计图：左侧输入区 + 右侧创意预览
 * 顶部 5 步骤进度条（输入创意 → 剧本生成 → 分镜设计 → 生成中 → 完成）
 */
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { submitGenerateTask } from '@/services/api'
import type { GenerationMode } from '@/types'
import StepProgress from '@/components/ui/StepProgress'
import Button from '@/components/ui/Button'
import './CreatePage.css'

// 步骤配置
const STEPS = [
  { key: 'idea', label: '输入创意' },
  { key: 'script', label: '剧本生成' },
  { key: 'storyboard', label: '分镜设计' },
  { key: 'generating', label: '生成中' },
  { key: 'done', label: '完成' }
]

// 模式选项
const MODE_TABS: { key: GenerationMode; label: string }[] = [
  { key: 'idea', label: '一句话创意' },
  { key: 'script', label: '详细剧本' },
  { key: 'novel', label: '小说改编' },
  { key: 'reference', label: '参考图/视频' }
]

// 视频风格选项
const STYLE_OPTIONS = [
  { value: '短剧', label: '短剧' },
  { value: '电影感', label: '电影感' },
  { value: '小红书', label: '小红书' },
  { value: '广告', label: '广告' },
  { value: '旅拍', label: '旅拍' },
  { value: '古风', label: '古装' }
]

// 视频时长选项
const DURATION_OPTIONS = [
  { value: 15, label: '15秒' },
  { value: 30, label: '30秒' },
  { value: 60, label: '60秒' },
  { value: 90, label: '90秒' },
  { value: 120, label: '120秒+' }
]

// 画面比例选项
const ASPECT_RATIO_OPTIONS = [
  { value: '16:9', label: '16:9' },
  { value: '9:16', label: '9:16' },
  { value: '1:1', label: '1:1' },
  { value: '4:3', label: '4:3' },
  { value: '3:4', label: '3:4' }
]

// 示例占位文案
const PLACEHOLDER_TEXT = '一个年轻人在雨夜的街头遇到一只流浪猫，最终决定收养它的温暖故事，风格温馨治愈。'

const CreatePage: React.FC = () => {
  const navigate = useNavigate()

  // 表单状态
  const [mode, setMode] = useState<GenerationMode>('idea')
  const [content, setContent] = useState('')
  const [style, setStyle] = useState('电影感')
  const [duration, setDuration] = useState(60)
  const [aspectRatio, setAspectRatio] = useState<'16:9' | '9:16' | '1:1' | '4:3' | '3:4'>('16:9')
  const [advancedOpen, setAdvancedOpen] = useState(false)

  // 提交状态
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 计算预计消耗
  const estimatedCredits = Math.max(5, Math.ceil(duration / 10))
  const estimatedMinutes = Math.max(1, Math.ceil(duration / 30))

  // 处理提交
  const handleSubmit = async () => {
    if (!content.trim()) {
      setError('请输入创意内容')
      return
    }

    setSubmitting(true)
    setError(null)

    try {
      const res = await submitGenerateTask({
        mode,
        content: content.trim(),
        style,
        style_tags: [style],
        target_duration: duration,
        aspect_ratio: aspectRatio
      })

      if (res.code === 0) {
        navigate(`/task/${res.data.task_id}`)
      } else {
        setError(res.message || '提交失败')
      }
    } catch (err) {
      console.error(err)
      setError('网络错误，请重试')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="create-page">
      {/* 顶部步骤进度 */}
      <div className="step-progress-wrapper">
        <StepProgress steps={STEPS} currentIndex={0} />
      </div>

      <div className="create-content">
        {/* 左侧输入卡片 */}
        <div className="create-card-left">
          <div className="card-header">
            <div className="card-title-row">
              <span className="card-step-num">1</span>
              <h2 className="card-title">输入创意</h2>
            </div>
            <p className="card-subtitle">用一句话或几句话描述你想要的视频创意，AI 将为你生成完整视频</p>
          </div>

          {/* 模式切换 */}
          <div className="mode-tabs">
            {MODE_TABS.map((tab) => (
              <button
                key={tab.key}
                className={`mode-tab ${mode === tab.key ? 'active' : ''}`}
                onClick={() => setMode(tab.key)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* 输入框 */}
          <div className="input-wrapper">
            <textarea
              className="idea-textarea"
              placeholder={PLACEHOLDER_TEXT}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              maxLength={500}
              rows={4}
            />
            <div className="char-counter">{content.length}/500</div>
          </div>

          {/* 视频风格 */}
          <div className="form-section">
            <label className="form-label">视频风格</label>
            <div className="option-pills">
              {STYLE_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  className={`pill ${style === opt.value ? 'active' : ''}`}
                  onClick={() => setStyle(opt.value)}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* 视频时长 */}
          <div className="form-section">
            <label className="form-label">视频时长</label>
            <div className="option-pills">
              {DURATION_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  className={`pill ${duration === opt.value ? 'active' : ''}`}
                  onClick={() => setDuration(opt.value)}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* 画面比例 */}
          <div className="form-section">
            <label className="form-label">画面比例</label>
            <div className="option-pills">
              {ASPECT_RATIO_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  className={`pill ${aspectRatio === opt.value ? 'active' : ''}`}
                  onClick={() => setAspectRatio(opt.value as any)}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* 高级设置 */}
          <div className="advanced-section">
            <button
              className="advanced-toggle"
              onClick={() => setAdvancedOpen(!advancedOpen)}
            >
              <span>高级设置</span>
              <span className={`arrow ${advancedOpen ? 'open' : ''}`}>▾</span>
            </button>
            {advancedOpen && (
              <div className="advanced-content">
                <div className="form-section">
                  <label className="form-label">分辨率</label>
                  <div className="option-pills">
                    {['720P', '1080P', '2K', '4K'].map((r) => (
                      <button key={r} className="pill">{r}</button>
                    ))}
                  </div>
                </div>
                <div className="form-section">
                  <label className="form-label">角色一致性</label>
                  <div className="option-pills">
                    <button className="pill active">标准</button>
                    <button className="pill">增强</button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {error && <div className="error-msg">{error}</div>}

          {/* 提交按钮 */}
          <Button
            variant="gradient"
            size="lg"
            block
            loading={submitting}
            onClick={handleSubmit}
            icon={<span>→</span>}
          >
            生成剧本
          </Button>
          <div className="submit-hint">
            预计消耗 {estimatedCredits} 积分，预计用时 1-{Math.max(1, estimatedMinutes)} 分钟
          </div>
        </div>

        {/* 右侧创意预览卡片 */}
        <div className="create-card-right">
          <div className="card-header">
            <h3 className="preview-title">
              创意预览 <span className="preview-tag">（示例）</span>
            </h3>
          </div>

          {/* 视频示例 */}
          <div className="video-preview">
            <img
              src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cinematic%20night%20street%20scene%20young%20man%20crouching%20down%20to%20pet%20a%20stray%20cat%2C%20rain%2C%20warm%20lighting%2C%20emotional%20moment%2C%20movie%20still&image_size=landscape_16_9"
              alt="创意预览"
              className="preview-image"
            />
            <div className="video-controls">
              <div className="play-btn">▶</div>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: '0%' }} />
              </div>
              <div className="time-display">00:00 / 01:00</div>
              <div className="control-icons">
                <span>🔇</span>
                <span>⛶</span>
              </div>
            </div>
          </div>

          {/* 创意描述 */}
          <div className="preview-description">
            <p>
              <strong>创意描述：</strong>
              雨夜的城市街头，年轻人蹲下身子，轻轻向流浪猫伸出......
              温暖治愈的故事，展现人与动物之间的温情与善意。
            </p>
          </div>

          {/* 风格标签 */}
          <div className="preview-tags">
            <span className="preview-tags-label">风格标签：</span>
            {['温馨', '治愈', '电影感', '情感', '雨夜'].map((tag) => (
              <span key={tag} className="style-tag">{tag}</span>
            ))}
          </div>
        </div>
      </div>

      {/* 历史创作记录 */}
      <HistoryRecords />
    </div>
  )
}

// 历史创作记录组件
const HistoryRecords: React.FC = () => {
  const navigate = useNavigate()

  // 模拟数据
  const records = [
    {
      id: '1',
      title: '古装江湖短剧',
      duration: '01:20',
      time: '2024-05-20 14:30',
      thumbnail: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=ancient%20chinese%20wuxia%20martial%20arts%20scene%2C%20silk%20robed%20warrior%2C%20mountain%20backdrop%2C%20sunset%2C%20cinematic&image_size=portrait_4_3',
      status: 'completed'
    },
    {
      id: '2',
      title: '美妆产品广告',
      duration: '00:30',
      time: '2024-05-20 10:15',
      thumbnail: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=luxury%20skincare%20product%20advertising%2C%20pink%20rose%20petals%2C%20elegant%20bottle%2C%20soft%20lighting&image_size=portrait_4_3',
      status: 'completed'
    },
    {
      id: '3',
      title: '海边旅行日记',
      duration: '00:60',
      time: '2024-05-19 16:45',
      thumbnail: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20beach%20travel%20vlog%2C%20young%20woman%20sitting%20on%20rocks%2C%20turquoise%20sea%2C%20sunny%20day&image_size=portrait_4_3',
      status: 'completed'
    },
    {
      id: '4',
      title: '萌宠百科视频',
      duration: '00:45',
      time: '2024-05-19 09:20',
      thumbnail: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cute%20tabby%20cat%20close-up%20portrait%2C%20big%20eyes%2C%20soft%20background&image_size=portrait_4_3',
      status: 'completed'
    }
  ]

  return (
    <div className="history-section">
      <div className="history-header">
        <h3>历史创作记录</h3>
        <button className="view-all-btn" onClick={() => navigate('/projects')}>
          查看全部 →
        </button>
      </div>
      <div className="history-grid">
        {records.map((record) => (
          <div
            key={record.id}
            className="history-card"
            onClick={() => navigate(`/task/${record.id}`)}
          >
            <div className="history-thumb">
              <img src={record.thumbnail} alt={record.title} />
              <span className="duration-badge">{record.duration}</span>
            </div>
            <div className="history-info">
              <div className="history-title">{record.title}</div>
              <div className="history-time">{record.time}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CreatePage
