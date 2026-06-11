/**
 * 占位页面 - 用于尚未详细设计的功能页面
 */
import React from 'react'
import './PlaceholderPage.css'

interface PlaceholderPageProps {
  title: string
  description: string
}

const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ title, description }) => {
  return (
    <div className="placeholder-page">
      <div className="placeholder-content">
        <div className="placeholder-icon">🚧</div>
        <h1 className="placeholder-title">{title}</h1>
        <p className="placeholder-desc">{description}</p>
        <div className="placeholder-tag">功能开发中</div>
      </div>
    </div>
  )
}

export default PlaceholderPage
