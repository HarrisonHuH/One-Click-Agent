# 一点灵光 - One-Click 智能视频生成系统

基于多智能体协作的Web应用，实现从文本创意到高质量视频的自动化生成。

## 项目结构

```
One-Click-Agent/
├── backend/                       # 后端服务
│   ├── app/
│   │   ├── api/v1/                # API 路由
│   │   │   ├── generate.py        # 提交生成任务
│   │   │   ├── task.py            # 任务状态/结果/日志
│   │   │   ├── tasks.py           # 任务列表/删除
│   │   │   └── user.py            # 用户信息
│   │   ├── agents/                # 多智能体模块
│   │   │   ├── writer_agent.py    # 编剧 Agent
│   │   │   ├── storyboard_agent.py# 分镜师 Agent
│   │   │   ├── director_agent.py  # 导演 Agent
│   │   │   └── producer_agent.py  # 制片人 Agent
│   │   ├── core/                  # 核心模块
│   │   │   ├── celery_app.py      # Celery 任务队列
│   │   │   └── task_manager.py    # 任务管理器
│   │   ├── models/                # 数据模型
│   │   ├── schemas/               # Pydantic 模型
│   │   ├── services/              # 服务层
│   │   └── workers/               # Celery Workers（6 阶段执行）
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                      # 前端应用
│   ├── src/
│   │   ├── components/            # 组件
│   │   │   ├── layout/            # 布局组件
│   │   │   │   ├── MainLayout.tsx # 主布局
│   │   │   │   ├── Sidebar.tsx    # 侧边栏
│   │   │   │   └── TopBar.tsx     # 顶部栏
│   │   │   └── ui/                # 通用 UI
│   │   │       ├── StepProgress.tsx  # 步骤进度
│   │   │       ├── Button.tsx        # 按钮
│   │   │       └── StatusBadge.tsx   # 状态徽章
│   │   ├── pages/                 # 页面
│   │   │   ├── CreatePage.tsx        # 创作工作台
│   │   │   ├── ProjectsPage.tsx      # 我的项目
│   │   │   ├── GenerateDetailPage.tsx# 生成详情
│   │   │   ├── VideosPage.tsx        # 我的视频
│   │   │   ├── SettingsPage.tsx      # 设置中心
│   │   │   └── PlaceholderPage.tsx   # 占位页面
│   │   ├── services/api.ts        # API 服务
│   │   ├── stores/                # 状态管理
│   │   ├── styles/global.css      # 全局设计系统
│   │   ├── types/                 # 类型定义
│   │   ├── utils/                 # 工具函数
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── index.html
│
└── 项目计划书.md
```

## 核心功能

### 6 阶段视频生成流水线
1. **剧本解析** - 解析脚本内容，提取关键信息与场景
2. **分镜处理** - 处理分镜画面，理解镜头语言
3. **素材生成** - 生成画面与视频片段素材
4. **视频合成** - 合成视频片段，添加转场与特效
5. **音频生成** - 生成配乐、音效与配音
6. **画面优化** - 提升画质，优化色彩与细节
7. **导出视频** - 渲染并导出最终视频文件

### 4 种创作模式
- **一句话创意** - 简单创意描述，AI 自动扩写
- **详细剧本** - 上传或输入完整剧本
- **小说改编** - 长文本小说改编
- **参考图/视频** - 基于参考素材生成

### 多状态项目管理
- 全部项目 / 进行中 / 已完成 / 草稿 / 回收站
- 关键字搜索、类型过滤、排序
- 网格/列表双视图

## 技术栈

### 后端
- Python 3.10+
- FastAPI - Web 框架
- Celery + Redis - 异步任务队列
- SQLAlchemy + SQLite - 数据持久化
- 多智能体架构（编剧/分镜师/导演/制片人）

### 前端
- React 18 + TypeScript
- Vite - 构建工具
- React Router v6
- Zustand - 状态管理
- Axios - HTTP 客户端
- 暗色侧边栏 + 浅色主内容区设计

## 快速开始

### 1. 环境要求
- Python 3.10+
- Node.js 18+
- Redis Server
- FFmpeg (可选，用于视频处理)

### 2. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env

# 启动 Redis (需先安装 Redis)
# macOS: brew services start redis
# Linux: sudo systemctl start redis
# Windows: 启动 Redis 服务或使用 Docker

# 启动 Celery Worker
celery -A app.core.celery_app worker --loglevel=info

# 启动 FastAPI 服务
uvicorn app.main:app --reload --port 8000
```

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用
- 前端：http://localhost:3000
- 后端 API 文档：http://localhost:8000/docs

## API 接口

### 任务生成
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/generate` | POST | 提交生成任务 |
| `/api/v1/task/{id}/status` | GET | 获取多阶段进度 |
| `/api/v1/task/{id}/result` | GET | 获取视频文件 |
| `/api/v1/task/{id}/thumbnail` | GET | 获取缩略图 |
| `/api/v1/task/{id}/logs` | GET | 获取生成日志 |

### 任务列表
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/tasks` | GET | 获取任务列表（支持分页/筛选/搜索）|
| `/api/v1/tasks/{id}` | DELETE | 删除任务（移到回收站） |

### 用户信息
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/user/info` | GET | 获取用户信息 |
| `/api/v1/user/info` | PUT | 更新用户信息 |

## 数据模型

### 任务 (Task)
- `id` - 任务 ID
- `mode` - 生成模式（idea/script/novel/reference）
- `input_content` - 输入内容
- `style` - 主风格
- `style_tags` - 风格标签
- `target_duration` - 目标时长（秒）
- `aspect_ratio` - 画面比例
- `status` - 状态（DRAFT/PENDING/PROCESSING/SUCCESS/FAILED/RECYCLED）
- `stage_progress` - 6 阶段进度
- `overall_progress` - 总进度
- `video_url` - 视频 URL
- `thumbnail_url` - 缩略图 URL
- `credits_consumed` - 消耗积分
- `collaborators` - 协作者列表

### 用户 (User)
- `id`, `nickname`, `email`, `avatar_url`, `bio`
- `credits` - 账户余额
- `remaining_minutes` - 剩余生成时长
- `account_type` - 账户类型（free/creator/professional）
- `user_code` - 用户唯一标识

### 生成日志 (GenerationLog)
- `task_id`, `stage`, `level`, `message`, `progress`

## 注意事项

1. 首次运行需要配置有效的 API 密钥（LLM/图像/视频）
2. 视频生成是异步任务，可能需要 3-5 分钟
3. 定期清理 `./workspace` 目录
4. 默认包含演示用户 `default-user-001`

## 许可证

MIT License
