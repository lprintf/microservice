from fastapi import FastAPI, Depends, HTTPException, status, Request
from jose import JWTError, jwt
from pydantic import BaseModel
import consul
import os
import requests
import uvicorn

# 初始化Consul客户端
consul_host = os.getenv("CONSUL_HOST", "consul")
consul_port = int(os.getenv("CONSUL_PORT", 8500))
consul_client = consul.Consul(host=consul_host, port=consul_port)

# 服务注册
service_name = os.getenv("SERVICE_NAME", "user-service")
service_host = os.getenv("SERVICE_HOST", service_name)
service_port = int(os.getenv("SERVICE_PORT", 8000))

def register_service():
    consul_client.agent.service.register(
        name=service_name,
        service_id=f"{service_name}-1",
        address=service_host,
        port=service_port,
        check=consul.Check.http(
            f"http://{service_host}:{service_port}/health",
            interval="10s",
            timeout="5s"
        )
    )

# 初始化FastAPI应用
app = FastAPI(title="User Service")

# JWT配置
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")

# 模拟数据库
fake_users_db = [
    {"id": 1, "username": "johndoe", "email": "johndoe@example.com", "name": "John Doe"},
    {"id": 2, "username": "janedoe", "email": "janedoe@example.com", "name": "Jane Doe"}
]

# Pydantic模型
class User(BaseModel):
    id: int
    username: str
    email: str
    name: str

class UserCreate(BaseModel):
    username: str
    email: str
    name: str

# 认证依赖
async def get_current_user(request: Request):
    user_id = request.headers.get("X-User-ID")
    user_role = request.headers.get("X-User-Role")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"username": user_id, "role": user_role}

# 权限检查依赖
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# 服务发现工具函数
def discover_service(service_name):
    _, services = consul_client.health.service(service_name, passing=True)
    if not services:
        raise HTTPException(status_code=503, detail=f"Service {service_name} not available")
    return services[0]['Service']

# API路由
@app.get("/users", response_model=list[User])
async def get_users(current_user: dict = Depends(get_current_user)):
    return fake_users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    user = next((u for u in fake_users_db if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, current_user: dict = Depends(require_admin)):
    new_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "name": user.name
    }
    fake_users_db.append(new_user)
    return new_user

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 服务间调用示例
@app.get("/users/{user_id}/products")
async def get_user_products(user_id: int, current_user: dict = Depends(get_current_user)):
    # 发现产品服务
    try:
        product_service = discover_service("product-service")
        product_service_url = f"http://{product_service['Address']}:{product_service['Port']}"
        
        # 调用产品服务
        response = requests.get(f"{product_service_url}/products?user_id={user_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling product service: {str(e)}")

# 启动时注册服务
register_service()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
