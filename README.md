# PaperClarity V2

## 当前进度（截至 2026-04-02）

### ✅ 已完成
- 后端 FastAPI MVP 主链路：文档加载、PDF 解析、上下文构建、Skill 执行、笔记保存、Markdown 导出。
- Skills 可插拔框架与 6 个内置技能。
- 前端 React+TypeScript+Vite 基础骨架：
  - 主布局（左阅读区/右AI工作台）
  - 文档路径加载入口（调用 `/api/documents/load`）
  - 技能执行、笔记保存、Markdown 导出按钮
  - Zustand 状态管理与 API 封装

- 前端 React+TypeScript+Vite 基础骨架：主布局（左阅读区/右AI工作台）、状态管理、API 封装、技能运行与笔记保存入口。

### 🚧 进行中
- 左侧阅读区目前为文本块渲染与选择，占位了 PDF.js 组件接口，下一步替换为真实 PDF 渲染。
- 右侧 Prompt 编辑、引用回跳、多模型设置写入还未完成。

## 目录
- `app/backend`: 后端
- `app/frontend`: 前端
- `tests/backend`: 后端测试
- `scripts`: 启动脚本

## 本地启动

### 后端

# PaperClarity V2 (MVP Scaffold)

## 当前实现范围
- FastAPI 后端骨架
- PDF 加载与解析（PyMuPDF）
- Skills 插件框架 + 6 个内置 skills
- Notes 保存与 Markdown 导出

## 目录
- `app/backend`: 后端代码
- `tests/backend`: 后端基础测试
- `scripts`: 启动脚本

## 本地运行

```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cd ../..
./scripts/dev_backend.sh
```

### 前端
```bash
./scripts/dev_frontend.sh
```

### 同时启动
```bash
./scripts/dev_all.sh
```

## API
- `POST /api/documents/load`
- `GET /api/documents/{doc_id}/blocks`

访问健康检查：`GET http://localhost:8000/api/health`

## 关键 API
- `POST /api/documents/load`

- `GET /api/skills`
- `POST /api/skills/{skill_name}/run`
- `POST /api/notes`
- `POST /api/export/markdown`
