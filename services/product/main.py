from fastapi import FastAPI, Depends, HTTPException, status, Request
from pydantic import BaseModel
import consul
import os
import uvicorn

# 初始化Consul客户端
consul_host = os.getenv("CONSUL_HOST", "consul")
consul_port = int(os.getenv("CONSUL_PORT", 8500))
consul_client = consul.Consul(host=consul_host, port=consul_port)

# 服务注册
service_name = os.getenv("SERVICE_NAME", "product-service")
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
app = FastAPI(title="Product Service")

# 模拟数据库
fake_products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "user_id": 1},
    {"id": 2, "name": "Smartphone", "price": 699.99, "user_id": 1},
    {"id": 3, "name": "Tablet", "price": 299.99, "user_id": 2}
]

# Pydantic模型
class Product(BaseModel):
    id: int
    name: str
    price: float
    user_id: int

class ProductCreate(BaseModel):
    name: str
    price: float
    user_id: int

# 认证依赖 - 直接从请求头获取用户信息
async def get_current_user(request):
    user_id = request.headers.get("X-User-ID")
    user_role = request.headers.get("X-User-Role")

    if not user_id or not user_role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"username": user_id, "role": user_role}

# API路由
@app.get("/products", response_model=list[Product])
async def get_products(request, user_id: int = None, current_user: dict = Depends(get_current_user)):
    if user_id:
        return [p for p in fake_products_db if p["user_id"] == user_id]
    return fake_products_db

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, request, current_user: dict = Depends(get_current_user)):
    product = next((p for p in fake_products_db if p["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, request, current_user: dict = Depends(get_current_user)):
    new_product = {
        "id": len(fake_products_db) + 1,
        "name": product.name,
        "price": product.price,
        "user_id": product.user_id
    }
    fake_products_db.append(new_product)
    return new_product

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 启动时注册服务
register_service()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
