# FastAPI微服务框架 / FastAPI Microservice Framework

<div class="language-tabs">
  <button class="tab-button active" onclick="switchLanguage('zh')">中文</button>
  <button class="tab-button" onclick="switchLanguage('en')">English</button>
</div>

<!-- 中文内容 -->
<div id="zh" class="language-content">

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
# 克隆仓库
git clone <仓库地址>
cd fastapi-microservice-framework

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
### 访问服务

- Traefik管理面板：http://localhost:8080
- Consul管理界面：http://localhost:8500
- API网关入口：http://localhost

### 示例使用
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

</div>

<!-- 英文内容 -->
<div id="en" class="language-content" style="display: none;">

## Overview

A microservice framework based on FastAPI, Traefik and Consul, featuring complete service discovery, API gateway and authentication mechanisms, with one-click deployment via Docker Compose.

## Features

- **Service Discovery**: Service registration and health checks using Consul
- **API Gateway**: Request routing, load balancing and authentication middleware via Traefik
- **Authentication & Authorization**: JWT-based unified authentication service
- **Containerized Deployment**: All components are Dockerized, with one-click startup via docker-compose
- **Scalability**: Easily add new microservices that automatically integrate into the existing framework

## Architecture Components

1. **Consul**: Service registration and discovery center
2. **Traefik**: API gateway responsible for routing and load balancing
3. **Auth Service**: Handles user authentication and JWT token issuance
4. **User Service**: APIs for user management
5. **Product Service**: APIs for product management (example service)

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Starting Services
# Clone the repository
git clone <repository-url>
cd fastapi-microservice-framework

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
### Accessing Services

- Traefik management dashboard: http://localhost:8080
- Consul management interface: http://localhost:8500
- API gateway entry: http://localhost

### Example Usage
# Get access token
curl -X POST "http://localhost/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# Access user service with token
curl "http://localhost/users" \
  -H "Authorization: Bearer <your_token>"

# Access product service with token
curl "http://localhost/products" \
  -H "Authorization: Bearer <your_token>"
## Directory Structure
```
.
├── docker-compose.yml          # Service orchestration configuration
├── traefik/                    # Traefik gateway configuration
│   └── traefik.yml
├── services/
│   ├── auth/                   # Authentication service
│   ├── user/                   # User service
│   └── product/                # Product service
├── .env.example                # Environment variables example
└── README.md
```
## Extension Guide

To add a new microservice, simply follow these steps:

1. Create a new service folder under the `services` directory
2. Implement the FastAPI application with Consul service registration logic
3. Add service configuration in `docker-compose.yml`
4. Configure Traefik routing rules

## Production Environment Considerations

1. Replace all default secrets and passwords
2. Configure HTTPS certificates
3. Add persistent data storage
4. Configure appropriate resource limits
5. Add monitoring and log collection

</div>

<script>
function switchLanguage(lang) {
  // Hide all content sections
  document.querySelectorAll('.language-content').forEach(el => {
    el.style.display = 'none';
  });
  
  // Show selected language content
  document.getElementById(lang).style.display = 'block';
  
  // Update active button styling
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.remove('active');
  });
  event.currentTarget.classList.add('active');
}
</script>

<style>
.language-tabs {
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.tab-button {
  background-color: #f5f5f5;
  border: none;
  padding: 8px 16px;
  margin-right: 8px;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.tab-button.active {
  background-color: #0366d6;
  color: white;
}

.tab-button:hover:not(.active) {
  background-color: #e0e0e0;
}

.language-content h2 {
  border-bottom: 1px solid #eee;
  padding-bottom: 0.3em;
  margin-top: 24px;
  margin-bottom: 16px;
}

.language-content pre {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
}
</style>
