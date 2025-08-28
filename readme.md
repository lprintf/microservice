# FastAPI微服务框架

[English Version](./readme.en.md)

## 概述

一个基于FastAPI、Traefik和Consul的微服务框架，包含完整的服务发现、API网关和认证机制，支持Docker Compose一键部署。

## 特性

- **服务发现**：使用Consul实现服务注册与健康检查
- **API网关**：通过Traefik实现请求路由、负载均衡和认证中间件
- **认证授权**：基于JWT的统一认证服务
- **容器化部署**：所有组件Docker化，通过docker-compose一键启动
- **可扩展性**：轻松添加新的微服务，自动集成到现有框架

## 架构组成

1. **Consul**：服务注册与发现中心
2. **Traefik**：API网关，负责路由和负载均衡
3. **认证服务**：处理用户认证和JWT令牌发放
4. **用户服务**：用户管理相关API
5. **产品服务**：产品管理相关API（示例服务）

## 快速开始

### 前置要求

- Docker
- Docker Compose

### 启动服务
```bash
```bash
# 克隆仓库
git clone <仓库地址>
cd fastapi-microservice-framework

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```
```
### 访问服务

- Traefik管理面板：http://localhost:8080
- Consul管理界面：http://localhost:8500
- API网关入口：http://localhost

### 示例使用
```bash
```bash
# 获取访问令牌
curl -X POST "http://localhost/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# 使用令牌访问用户服务
curl "http://localhost/users" \
  -H "Authorization: Bearer <your_token>"

# 使用令牌访问产品服务
curl "http://localhost/products" \
  -H "Authorization: Bearer <your_token>"
```
```
## 目录结构
```
.
├── docker-compose.yml          # 服务编排配置
├── traefik/                    # Traefik网关配置
│   └── traefik.yml
├── services/
│   ├── auth/                   # 认证服务
│   ├── user/                   # 用户服务
│   └── product/                # 产品服务
├── .env.example                # 环境变量示例
└── README.md
```
## 扩展指南

添加新的微服务只需以下步骤：

1. 在`services`目录下创建新服务文件夹
2. 实现FastAPI应用并添加Consul服务注册逻辑
3. 在`docker-compose.yml`中添加服务配置
4. 配置Traefik路由规则

## 生产环境注意事项

1. 替换所有默认密钥和密码
2. 配置HTTPS证书
3. 添加数据持久化存储
4. 配置适当的资源限制
5. 添加监控和日志收集
