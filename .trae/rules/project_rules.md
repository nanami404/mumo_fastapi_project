# FastAPI 项目开发规范 (v1.0)

## 一、编程规范

### 1.1 语言与版本
- Python ≥ 3.10+
- 使用 FastAPI ≥ 0.100.0
- 使用 Pydantic v2

### 1.2 代码风格
- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 和 [PEP 484](https://peps.python.org/pep-0484/)（类型提示）
- 使用 Black 格式化代码（line-length=88）
- 使用 isort 管理 import 顺序
- 使用 ruff 或 flake8 进行静态检查
- 禁止使用 `from module import *`

### 1.3 类型提示（Type Hints）
- 所有函数、方法、变量必须带类型提示。
- 使用 `pydantic.BaseModel` 定义请求/响应模型。
- 使用 `typing` 模块（如 `Optional`, `List`, `Dict`, `Union` → 推荐使用现代语法）。

示例：
```python
from typing import Annotated
from fastapi import Query
from app.schemas import Item

def get_items(limit: Annotated[int, Query(ge=1, le=100)] = 10) -> list[Item]:

```

### 1.4 异常处理
- 自定义业务异常可以继承 `HTTPException` 或自定义异常类并统一捕获处理。
- 使用中间件或 `@app.exception_handler` 统一处理异常。
- 返回结构化错误响应（含 `code`、`message`、`detail`）。

示例：
```python
from fastapi import HTTPException

class UserNotFoundError(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            detail={"code": "USER_NOT_FOUND", "message": f"User {user_id} not found"}
        )
```

### 1.5 日志
- 使用标准库 `logging`，配置结构化日志（如 JSON）。
- 避免在业务逻辑中直接使用 `print()`。

---

## 二、项目架构（推荐分层架构）

项目目录示例：
```
more_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── core/                   # 核心配置、安全、工具
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic Settings
│   │   ├── session.py          # 会话管理器
│   │   ├── security.py         # 认证、JWT 等
│   │   └── logger.py           # 日志配置
│   ├── api/                    # API 路由层
│   │   ├── __init__.py
│   │   ├── deps.py             # 依赖注入（如 DB session）
│   │   ├── v1/                 # API 版本控制
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── items.py
│   │   │   │   └── ws.py       # WebSocket 路由
│   │   │   └── router.py       # 汇总 v1 路由
│   ├── models/                 # ORM 模型（如 SQLAlchemy）
│   ├── schemas/                # Pydantic 模型（请求/响应）
│   ├── crud/                   # 数据库操作
│   └── services/               # 业务逻辑
├── docs/                       # 项目文档（设计、API、部署等）
├── tests/                      # 单元测试 & 集成测试
├── alembic/                    # 数据库迁移
├── .env                        # 环境变量（加入 .gitignore）
├── pyproject.toml              # ✅ Poetry 依赖与项目元数据（唯一依赖源）
├── poetry.lock                 # ✅ 自动生成，应提交到 Git
└── README.md
```

分层原则：
- 路由层（`api/`）：只处理 HTTP/WebSocket 请求/响应，调用 `service`/`crud`。
- 业务层（`services/`）：封装复杂业务逻辑，可被多个路由复用。
- 数据层（`crud/` + `models/`）：隔离数据库操作。
- 依赖注入（`deps.py`）：统一管理 DB session、当前用户等依赖。

---

## 三、架构内示例代码

### 3.1 main.py（应用入口）
```python
# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)
```

### 3.2 HTTP 接口示例（api/v1/routes/items.py）
```python
# app/api/v1/routes/items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api.deps import get_db

router = APIRouter()

@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.item.get_multi(db, skip=skip, limit=limit)
    return items
```

### 3.3 WebSocket 接口示例（api/v1/routes/ws.py）
```python
# app/api/v1/routes/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left")
```

### 3.4 配置管理（core/config.py）
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 四、文档规范

### 4.1 API 文档
- 利用 FastAPI 自动生成 Swagger UI (/docs) 和 ReDoc (/redoc)。
- 为每个路由添加 `summary` 和 `description`。
- 为 Pydantic 模型字段添加 `description`。

示例：
```python
@router.get("/items/", summary="获取物品列表", description="分页返回所有物品")
def read_items(...):
```

### 4.2 代码注释
- 公共函数/类必须有 Google 风格 docstring。
- 复杂逻辑需行内注释（解释“为什么”，而非“做什么”）。

示例：
```python
def calculate_discount(price: float, user_level: str) -> float:
    """根据用户等级计算折扣价格。

    Args:
        price: 原始价格
        user_level: 用户等级 ('gold', 'silver', 'bronze')

    Returns:
        折扣后价格

    Raises:
        ValueError: 如果 user_level 无效
    """
```

### 4.3 项目 README.md
必须包含：
- 项目简介
- 快速启动（安装、运行）
- 环境变量说明
- API 文档地址
- 测试命令
- 部署说明（可选）

---

## 五、参考文档位置说明

| 类型   | 位置 | 说明 |
| ------ | ---- | ---- |
| 官方文档 | [FastAPI 官网](https://fastapi.tiangolo.com/) | 权威指南、教程、最佳实践 |
| Pydantic | [Pydantic v2 Docs](https://docs.pydantic.dev/latest/) | 数据验证与设置管理 |
| SQLAlchemy2.0 | [SQLAlchemy2.0 ORM](https://docs.sqlalchemy.org/) | 使用数据库 |
| WebSocket | FastAPI 官方 WebSocket 教程 | 实时通信实现 |
| 安全 | FastAPI Security 章节 | OAuth2, JWT, CORS 等 |
| 部署 | FastAPI Deployment | Docker, Gunicorn, Uvicorn |

---

## 六、附加建议
- 使用 Alembic 管理数据库迁移。
- 使用 pytest 编写测试，覆盖路由、crud、service。
- 启用 CORS（`fastapi.middleware.cors`）。
- 生产环境使用 Uvicorn + Gunicorn。