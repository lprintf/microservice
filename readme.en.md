# FastAPI Microservice Framework

[中文版](./readme.md)

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
6. **Frontend Service**: Vue.js-based user interface providing visual operations

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Starting Services
```bash
# Clone the repository
git clone <repository-url>
cd fastapi-microservice-framework

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```
### Accessing Services

- Traefik management dashboard: http://localhost:8080
- Consul management interface: http://localhost:8500
- API gateway entry: http://localhost
- Frontend service: http://localhost (accessed through API gateway)

### Example Usage
```bash
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
```
## Directory Structure
```
.
├── docker-compose.yml          # Service orchestration configuration
├── traefik/                    # Traefik gateway configuration
│   └── traefik.yml
├── services/
│   ├── auth/                   # Authentication service
│   ├── frontend/               # Frontend service
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