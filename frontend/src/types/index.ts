/**
 * 一点灵光 - 全局类型定义
 */

// ========== 生成任务 ==========

export type GenerationMode = 'idea' | 'script' | 'novel' | 'reference'

export interface GenerateRequest {
  mode: GenerationMode
  content: string
  style: string
  style_tags?: string[]
  target_duration: number
  aspect_ratio?: '16:9' | '9:16' | '1:1' | '4:3' | '3:4'
  resolution?: string
  reference_url?: string
}

export interface GenerateResponse {
  code: number
  message: string
  data: {
    task_id: string
  }
}

// ========== 任务状态（多阶段） ==========

export type StageStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED'

export interface StageProgress {
  stage: string
  label: string
  status: StageStatus
  progress: number
  duration?: number
  message?: string
  started_at?: string
  completed_at?: string
}

export interface TaskStatusData {
  task_id: string
  title?: string
  status: TaskStatusValue
  overall_progress: number
  current_stage: string
  current_stage_label: string
  stage_progress: Record<string, StageProgress>
  video_url: string | null
  preview_url: string | null
  thumbnail_url: string | null
  error_message: string | null
  credits_consumed: number
  estimated_remaining_minutes: number
}

export interface TaskStatusResponse {
  code: number
  data: TaskStatusData
}

// ========== 任务列表 ==========

export type TaskStatusValue = 'DRAFT' | 'PENDING' | 'PROCESSING' | 'SUCCESS' | 'FAILED' | 'RECYCLED'

export interface TaskListItem {
  task_id: string
  title: string
  mode: GenerationMode
  mode_label: string
  input_preview: string
  style: string
  style_tags: string[]
  status: TaskStatusValue
  status_label: string
  thumbnail_url: string | null
  duration: number
  duration_display: string
  resolution: string
  created_at: string
  updated_at: string
  collaborators: string[]
}

export interface TaskListData {
  total: number
  page: number
  limit: number
  status_counts: Record<string, number>
  items: TaskListItem[]
}

export interface TaskListResponse {
  code: number
  data: TaskListData
}

// ========== 用户信息 ==========

export type AccountType = 'free' | 'creator' | 'professional'

export interface UserInfo {
  user_id: string
  username: string
  nickname: string
  email: string | null
  avatar_url: string | null
  bio: string | null
  credits: number
  remaining_minutes: number
  account_type: AccountType
  user_code: string | null
}

export interface UserInfoResponse {
  code: number
  data: UserInfo
}

// ========== 生成日志 ==========

export type LogLevel = 'INFO' | 'WARNING' | 'ERROR'

export interface GenerationLogItem {
  id: number
  stage: string
  level: LogLevel
  message: string
  progress: number
  created_at: string
}

export interface GenerationLogResponse {
  code: number
  data: GenerationLogItem[]
}
