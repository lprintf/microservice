import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '/', // Traefik会将请求转发到对应的服务
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      delete config.headers.Authorization;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    // 处理认证错误
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// 认证相关API
export const authAPI = {
  // 登录
  login(credentials) {
    return api.post('/auth/token', credentials, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },
  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/auth/users/me/');
  },
  // 验证token
  verifyToken(token) {
    return api.get('/auth/verify', { headers: { Authorization: `Bearer ${token}` } });
  }
};

// 用户相关API
export const userAPI = {
  // 获取所有用户
  getUsers() {
    return api.get('/users');
  },
  // 获取单个用户
  getUser(id) {
    return api.get(`/users/${id}`);
  },
  // 创建用户（需要管理员权限）
  createUser(userData) {
    return api.post('/users', userData);
  },
  // 获取用户的产品
  getUserProducts(userId) {
    return api.get(`/users/${userId}/products`);
  }
};

// 产品相关API
export const productAPI = {
  // 获取所有产品
  getProducts() {
    return api.get('/products');
  },
  // 获取单个产品
  getProduct(id) {
    return api.get(`/products/${id}`);
  },
  // 创建产品
  createProduct(productData) {
    return api.post('/products', productData);
  }
};

export default api;