# PaperClarity V2

## 当前进度（截至 2026-04-02）

### ✅ 已完成
- 后端 FastAPI MVP 主链路：文档加载、PDF 解析、上下文构建、Skill 执行、笔记保存、Markdown 导出。
- Skills 可插拔框架与 6 个内置技能。
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
- `GET /api/skills`
- `POST /api/skills/{skill_name}/run`
- `POST /api/notes`
- `POST /api/export/markdown`
