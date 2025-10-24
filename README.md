# Mumo FastAPI Project

基于 FastAPI 的现代 Web 应用项目，遵循最佳实践和分层架构设计。

## 项目简介

这是一个使用 FastAPI 构建的现代 Web 应用项目，采用分层架构设计，包含完整的 API 开发、数据库操作、业务逻辑处理等功能模块。项目严格遵循 FastAPI 开发规范，提供高性能、类型安全的 API 服务。

## 技术栈

- **Python**: ≥ 3.9
- **FastAPI**: ≥ 0.100.0 (Web 框架)
- **Pydantic**: v2 (数据验证)
- **SQLAlchemy**: 2.0 (ORM)
- **Alembic**: 数据库迁移
- **Uvicorn**: ASGI 服务器
- **Poetry**: 依赖管理

## 项目结构

```
mumo_fastapi_project/
├── app/                    # 应用主目录
│   ├── __init__.py
│   ├── main.py            # FastAPI 应用入口
│   ├── core/              # 核心配置、安全、工具
│   │   ├── config.py      # Pydantic Settings
│   │   ├── session.py     # 数据库会话管理
│   │   ├── security.py    # 认证、JWT 等
│   │   └── logger.py      # 日志配置
│   ├── api/               # API 路由层
│   │   ├── deps.py        # 依赖注入
│   │   └── v1/            # API 版本控制
│   │       ├── routes/    # 路由模块
│   │       └── router.py  # 路由汇总
│   ├── models/            # SQLAlchemy 模型
│   ├── schemas/           # Pydantic 模型
│   ├── crud/              # 数据库操作
│   └── services/          # 业务逻辑
├── docs/                  # 项目文档
├── tests/                 # 单元测试 & 集成测试
├── alembic/               # 数据库迁移
├── .env.example           # 环境变量示例
├── pyproject.toml         # Poetry 依赖配置
└── README.md
```

## 快速开始

### 1. 环境要求

- Python 3.9+
- Poetry (推荐) 或 pip

### 2. 安装依赖

使用 Poetry (推荐):
```bash
# 安装 Poetry (如果未安装)
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install
```

使用 pip:
```bash
pip install -r requirements.txt  # 需要先生成 requirements.txt
```

### 3. 环境配置

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，配置必要的环境变量
# 特别注意修改 SECRET_KEY 和数据库配置
```

### 4. 数据库初始化

```bash
# 初始化 Alembic (首次运行)
poetry run alembic init alembic

# 创建初始迁移
poetry run alembic revision --autogenerate -m "Initial migration"

# 执行迁移
poetry run alembic upgrade head
```

### 5. 启动应用

```bash
# 开发模式启动
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或者使用 Python 模块方式
poetry run python -m uvicorn app.main:app --reload
```

### 6. 访问应用

- **应用首页**: http://localhost:8000
- **API 文档 (Swagger UI)**: http://localhost:8000/docs
- **API 文档 (ReDoc)**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 环境变量说明

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `PROJECT_NAME` | 项目名称 | Mumo FastAPI Project | 否 |
| `API_V1_STR` | API v1 前缀 | /api/v1 | 否 |
| `DATABASE_URL` | 数据库连接字符串 | sqlite:///./mumo_fastapi.db | 是 |
| `SECRET_KEY` | JWT 密钥 | - | 是 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 过期时间(分钟) | 30 | 否 |
| `BACKEND_CORS_ORIGINS` | CORS 允许的源 | http://localhost:3000,http://localhost:8080 | 否 |
| `LOG_LEVEL` | 日志级别 | INFO | 否 |

## 开发指南

### 代码规范

项目遵循以下代码规范：
- [PEP 8](https://peps.python.org/pep-0008/) Python 代码风格
- [PEP 484](https://peps.python.org/pep-0484/) 类型提示
- 使用 Black 进行代码格式化
- 使用 isort 管理导入顺序
- 使用 Ruff 进行静态检查

### 代码格式化

```bash
# 格式化代码
poetry run black app/ tests/

# 排序导入
poetry run isort app/ tests/

# 静态检查
poetry run ruff check app/ tests/

# 类型检查
poetry run mypy app/
```

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行测试并生成覆盖率报告
poetry run pytest --cov=app --cov-report=html

# 运行特定测试文件
poetry run pytest tests/test_items.py
```

## API 使用示例

### 获取物品列表

```bash
curl -X GET "http://localhost:8000/api/v1/items/" \
  -H "accept: application/json"
```

### 获取单个物品

```bash
curl -X GET "http://localhost:8000/api/v1/items/1" \
  -H "accept: application/json"
```

### WebSocket 连接

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/websocket/ws/client123');
ws.onmessage = function(event) {
    console.log('Message from server:', event.data);
};
ws.send('Hello Server!');
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t mumo-fastapi .

# 运行容器
docker run -d -p 8000:8000 --env-file .env mumo-fastapi
```

### 生产环境部署

```bash
# 使用 Gunicorn + Uvicorn
poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 扩展功能

项目提供了丰富的扩展建议，详见 [优化建议文档](docs/optimization_suggestions.md)，包括：

- 缓存系统 (Redis)
- 消息队列 (Celery)
- 监控和日志 (Prometheus, Grafana)
- 安全增强 (API 限流, 数据加密)
- 测试覆盖率提升
- 容器化和 CI/CD

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目链接: [https://github.com/yourusername/mumo_fastapi_project](https://github.com/yourusername/mumo_fastapi_project)
Basic FastAPI Project Scaffold.
