/**
 * 一点灵光 - 工具函数
 */

/** 格式化时间戳为简洁显示 */
export const formatTime = (dateString: string, format: 'datetime' | 'date' | 'time' = 'datetime'): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return ''

  const pad = (n: number) => String(n).padStart(2, '0')

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1)
  const day = pad(date.getDate())
  const hour = pad(date.getHours())
  const minute = pad(date.getMinutes())
  const second = pad(date.getSeconds())

  if (format === 'date') return `${year}-${month}-${day}`
  if (format === 'time') return `${hour}:${minute}`
  return `${year}-${month}-${day} ${hour}:${minute}`
}

/** 格式化时长（秒 → mm:ss）*/
export const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

/** 相对时间（多久之前）*/
export const timeAgo = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffSec = Math.floor(diffMs / 1000)
  const diffMin = Math.floor(diffSec / 60)
  const diffHour = Math.floor(diffMin / 60)
  const diffDay = Math.floor(diffHour / 24)

  if (diffDay > 7) return formatTime(dateString, 'date')
  if (diffDay > 0) return `${diffDay}天前`
  if (diffHour > 0) return `${diffHour}小时前`
  if (diffMin > 0) return `${diffMin}分钟前`
  return '刚刚'
}
