# 关键代码模式

生成代码时必须遵循这些模式，确保前后端正确通信。

## 后端

### FastAPI CORS（backend/app/main.py）

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import router

app = FastAPI(title="应用名称 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
```

### SQLite 数据库（backend/app/database.py）

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库已初始化")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 后端依赖（backend/requirements.txt）

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.6.0
python-multipart==0.0.9
```

## 前端

### Vite 代理（frontend/vite.config.js）

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### PostCSS（frontend/postcss.config.js）⚠️ 必需

```javascript
export default {
  plugins: { tailwindcss: {}, autoprefixer: {} }
}
```

### API 客户端（frontend/src/api/client.js）

```javascript
const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '请求失败' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  get: (endpoint) => request(endpoint),
  post: (endpoint, data) => request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  put: (endpoint, data) => request(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (endpoint) => request(endpoint, { method: 'DELETE' }),
};
```

### 前端依赖（frontend/package.json 核心部分）

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "vite": "^5.0.11"
  }
}
```

## 常见陷阱

| 陷阱 | 正确做法 |
|---|---|
| CORS 缺失或 origins 错误 | `allow_origins=["http://localhost:5173"]` |
| 缺少 Vite proxy | 必须配置 `/api` proxy 到 8000 |
| SQLite 用绝对路径 | 必须用 `sqlite:///./app.db`（相对路径） |
| 缺少 `__init__.py` | 每个 Python 包目录都要有 |
| 缺少 postcss.config.js | Tailwind 不生效的首要原因 |

## 端口约定

- 后端：8000（FastAPI / uvicorn）
- 前端：5173（Vite dev server）
