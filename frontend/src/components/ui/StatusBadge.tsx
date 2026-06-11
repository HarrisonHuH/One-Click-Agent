/**
 * 状态徽章组件
 */
import React from 'react'
import './StatusBadge.css'

type StatusType = 'success' | 'processing' | 'failed' | 'pending' | 'recycled' | 'draft'

interface StatusBadgeProps {
  status: string
  label?: string
  type?: StatusType
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, type }) => {
  const computedType: StatusType = type || (status.toLowerCase() as StatusType)
  const displayLabel = label || status

  return (
    <span className={`status-badge status-${computedType}`}>
      {computedType === 'processing' && <span className="badge-dot" />}
      {displayLabel}
    </span>
  )
}

export default StatusBadge
