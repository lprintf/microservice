#!/bin/bash

# 测试微服务认证流程脚本

# 等待服务启动
echo "等待服务启动..."
sleep 20

# 定义变量
auth_service_url="http://localhost:8000/api/auth"
user_service_url="http://localhost:8001/api/users"
product_service_url="http://localhost:8002/api/products"
username="testuser"
password="testpassword"

# 1. 测试登录获取token
echo -e "\n1. 测试登录获取token..."
login_response=$(curl -s -X POST "${auth_service_url}/login" -H "Content-Type: application/json" -d '{"username": "'${username}'", "password": "'${password}'"}')

token=$(echo "${login_response}" | grep -o '"access_token":"[^"]*' | cut -d':' -f2 | tr -d '"')

if [ -z "${token}" ]; then
    echo "登录失败，无法获取token: ${login_response}"
    exit 1
else
    echo "登录成功，获取到token: ${token:0:20}..."
fi

# 2. 测试verify端点响应头
echo -e "\n2. 测试verify端点响应头..."
verify_response=$(curl -s -I -X GET "${auth_service_url}/verify" -H "Authorization: Bearer ${token}")

# 提取响应头中的用户信息
x_user_id=$(echo "${verify_response}" | grep -i 'X-User-ID' | cut -d':' -f2 | tr -d ' ')
x_user_role=$(echo "${verify_response}" | grep -i 'X-User-Role' | cut -d':' -f2 | tr -d ' ')

if [ -z "${x_user_id}" ] || [ -z "${x_user_role}" ]; then
    echo "verify端点未正确设置响应头:"
    echo "${verify_response}"
else
    echo "verify端点响应头设置成功:"
    echo "X-User-ID: ${x_user_id}"
    echo "X-User-Role: ${x_user_role}"
fi

# 3. 测试访问受保护的API
echo -e "\n3. 测试访问受保护的API (user-service)..."
api_response=$(curl -s -X GET "${user_service_url}" -H "Authorization: Bearer ${token}")

# 检查响应是否包含用户ID
if [[ "${api_response}" == *"${x_user_id}"* ]]; then
    echo "API访问成功，用户信息已正确传递:"
    echo "${api_response}"
else
    echo "API访问失败，未正确传递用户信息:"
    echo "${api_response}"
fi

echo -e "\n测试完成!"