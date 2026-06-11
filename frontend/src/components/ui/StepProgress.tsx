/**
 * 一步骤进度条组件
 * 5 步骤进度展示，对应设计图顶部的步骤条
 */
import React from 'react'
import './StepProgress.css'

export interface Step {
  key: string
  label: string
}

interface StepProgressProps {
  steps: Step[]
  currentIndex: number  // -1 表示全部未开始
  status?: 'pending' | 'processing' | 'success' | 'failed'
}

const StepProgress: React.FC<StepProgressProps> = ({ steps, currentIndex, status = 'processing' }) => {
  return (
    <div className="step-progress">
      {steps.map((step, idx) => {
        const isCompleted = idx < currentIndex || status === 'success'
        const isActive = idx === currentIndex && (status === 'processing' || status === 'pending')
        return (
          <React.Fragment key={step.key}>
            <div className={`step-item ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}>
              <div className="step-number">
                {isCompleted ? '✓' : idx + 1}
              </div>
              <div className="step-label">{step.label}</div>
            </div>
            {idx < steps.length - 1 && (
              <div className={`step-line ${isCompleted ? 'completed' : ''}`} />
            )}
          </React.Fragment>
        )
      })}
    </div>
  )
}

export default StepProgress
