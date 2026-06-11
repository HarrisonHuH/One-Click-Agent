/**
 * 一点灵光 - API请求封装
 */
import axios from 'axios'
import type {
  GenerateRequest,
  GenerateResponse,
  TaskStatusResponse,
  TaskListResponse,
  UserInfoResponse,
  GenerationLogResponse
} from '@/types'

const API_BASE_URL = '/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ========== 生成任务 ==========

/** 提交生成任务 */
export const submitGenerateTask = (data: GenerateRequest): Promise<GenerateResponse> =>
  apiClient.post('/generate', data)

// ========== 任务状态 ==========

/** 获取任务多阶段状态 */
export const getTaskStatus = (taskId: string): Promise<TaskStatusResponse> =>
  apiClient.get(`/task/${taskId}/status`)

/** 获取任务视频URL */
export const getTaskResultUrl = (taskId: string): string =>
  `${API_BASE_URL}/task/${taskId}/result`

/** 获取任务缩略图URL */
export const getTaskThumbnailUrl = (taskId: string): string =>
  `${API_BASE_URL}/task/${taskId}/thumbnail`

/** 获取任务日志 */
export const getTaskLogs = (taskId: string): Promise<GenerationLogResponse> =>
  apiClient.get(`/task/${taskId}/logs`)

// ========== 任务列表 ==========

export interface TaskListParams {
  page?: number
  limit?: number
  status?: string
  keyword?: string
}

/** 获取任务列表 */
export const getTaskList = (params: TaskListParams = {}): Promise<TaskListResponse> => {
  const { page = 1, limit = 20, status = 'all', keyword } = params
  return apiClient.get('/tasks', {
    params: { page, limit, status, keyword }
  })
}

/** 删除任务（移到回收站） */
export const deleteTask = (taskId: string, permanent = false): Promise<{ code: number; message: string }> =>
  apiClient.delete(`/tasks/${taskId}`, { params: { permanent } })

// ========== 用户信息 ==========

/** 获取当前用户信息 */
export const getUserInfo = (): Promise<UserInfoResponse> =>
  apiClient.get('/user/info')

/** 更新用户信息 */
export const updateUserInfo = (data: { nickname?: string; email?: string; bio?: string; avatar_url?: string }): Promise<UserInfoResponse> =>
  apiClient.put('/user/info', data)
