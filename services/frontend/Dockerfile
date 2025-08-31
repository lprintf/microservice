# 使用官方Node.js镜像作为构建环境
FROM node:20-alpine AS build

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 构建项目
RUN npm run build

# 使用Nginx作为生产环境的Web服务器
FROM nginx:alpine

# 复制构建好的文件到Nginx的html目录
COPY --from=build /app/dist /usr/share/nginx/html

# 复制自定义的Nginx配置文件（如果需要）
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]