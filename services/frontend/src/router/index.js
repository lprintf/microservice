import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import UserList from '../components/UserList.vue';
import ProductList from '../components/ProductList.vue';
import Home from '../components/Home.vue';
import api from '../utils/api.js'; // 导入api实例

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        requiresAuth: true // 需要认证才能访问
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/users',
      name: 'UserList',
      component: UserList,
      meta: {
        requiresAuth: true // 需要认证才能访问
      }
    },
    {
      path: '/products',
      name: 'ProductList',
      component: ProductList,
      meta: {
        requiresAuth: true // 需要认证才能访问
      }
    }
  ]
});

// 全局路由守卫 - 专注于权限控制和token验证
router.beforeEach(async (to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  
  // 从localStorage获取token
  const token = localStorage.getItem('token');
  
  // 如果路由需要认证
  if (requiresAuth) {
    if (!token) {
      next('/login');
    } else {
      try {
        // 直接验证token，不依赖axios拦截器
        const response = await api.get('/auth/verify', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
          }
        });
        
        // 验证通过后，确保设置axios默认头，为后续请求做准备
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        next();
      } catch (error) {
        // 清除无效token
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        delete api.defaults.headers.common['Authorization'];
        
        next('/login');
      }
    }
  } 
  // 如果已经登录且尝试访问登录页面，则重定向到首页
  else if (to.path === '/login' && token) {
    try {
      await api.get('/auth/verify', { 
        headers: { 
          Authorization: `Bearer ${token}`,
          'Cache-Control': 'no-cache'
        } 
      });
      next('/');
    } catch (error) {
      next();
    }
  } 
  // 其他情况，正常通过
  else {
    next();
  }
});

export default router;