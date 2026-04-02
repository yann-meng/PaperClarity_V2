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

访问健康检查：`GET http://localhost:8000/api/health`

## 关键 API
- `POST /api/documents/load`
- `GET /api/skills`
- `POST /api/skills/{skill_name}/run`
- `POST /api/notes`
- `POST /api/export/markdown`
