/**
 * 一点灵光 - 主应用
 */
import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import MainLayout from './components/layout/MainLayout'
import CreatePage from './pages/CreatePage'
import ProjectsPage from './pages/ProjectsPage'
import GenerateDetailPage from './pages/GenerateDetailPage'
import VideosPage from './pages/VideosPage'
import SettingsPage from './pages/SettingsPage'
import PlaceholderPage from './pages/PlaceholderPage'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          {/* 默认跳转到创作工作台 */}
          <Route index element={<Navigate to="/create" replace />} />
          
          {/* 创作工作台 */}
          <Route path="create" element={<CreatePage />} />
          
          {/* 我的项目 */}
          <Route path="projects" element={<ProjectsPage />} />
          
          {/* 我的视频 */}
          <Route path="videos" element={<VideosPage />} />
          
          {/* 任务详情/生成详情 */}
          <Route path="task/:taskId" element={<GenerateDetailPage />} />
          
          {/* 设置中心 */}
          <Route path="settings" element={<SettingsPage />} />
          <Route path="settings/:tab" element={<SettingsPage />} />
          
          {/* 占位页面 - 按设计图风格补全 */}
          <Route path="skills" element={<PlaceholderPage title="Skill 知识库" description="管理和复用从高质量视频中提取的创作技能" />} />
          <Route path="templates" element={<PlaceholderPage title="模板市场" description="使用预设模板快速创建视频" />} />
          <Route path="quality" element={<PlaceholderPage title="质量评估" description="查看视频生成质量评估报告" />} />
          <Route path="api-docs" element={<PlaceholderPage title="API 接口" description="查看和管理 API 密钥" />} />
          <Route path="help" element={<PlaceholderPage title="帮助文档" description="查看使用文档和常见问题" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
