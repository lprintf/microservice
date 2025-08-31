<template>
  <div class="home-container">
    <h2>欢迎使用微服务系统</h2>
    
    <!-- 仪表板统计卡片 -->
    <div class="dashboard-cards">
      <div class="card">
        <div class="card-icon user-icon">👥</div>
        <div class="card-content">
          <h3>用户总数</h3>
          <p class="card-value">{{ userCount }}</p>
          <p class="card-link"><router-link to="/users">查看详情 →</router-link></p>
        </div>
      </div>
      
      <div class="card">
        <div class="card-icon product-icon">🛍️</div>
        <div class="card-content">
          <h3>产品总数</h3>
          <p class="card-value">{{ productCount }}</p>
          <p class="card-link"><router-link to="/products">查看详情 →</router-link></p>
        </div>
      </div>
    </div>
    
    <!-- 最近活动 -->
    <div class="recent-activity">
      <h3>系统信息</h3>
      <div class="activity-list">
        <div class="activity-item">
          <span class="activity-label">当前登录用户:</span>
          <span class="activity-value">{{ currentUser?.username }}</span>
        </div>
        <div class="activity-item">
          <span class="activity-label">用户角色:</span>
          <span class="activity-value">{{ currentUser?.role }}</span>
        </div>
        <div class="activity-item">
          <span class="activity-label">系统状态:</span>
          <span class="activity-value status-online">正常运行</span>
        </div>
      </div>
    </div>
    
    <!-- 快速操作 -->
    <div class="quick-actions">
      <h3>快速操作</h3>
      <div class="actions-grid">
        <router-link to="/users" class="action-button users-button">
          <span class="action-icon">👥</span>
          <span class="action-text">管理用户</span>
        </router-link>
        
        <router-link to="/products" class="action-button products-button">
          <span class="action-icon">🛍️</span>
          <span class="action-text">管理产品</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { userAPI, productAPI } from '../utils/api.js';

export default {
  name: 'Home',
  data() {
    return {
      userCount: 0,
      productCount: 0,
      currentUser: null,
      loading: false,
      error: ''
    };
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = '';
      try {
        // 并行获取用户和产品数量
        const [users, products] = await Promise.all([
          userAPI.getUsers(),
          productAPI.getProducts()
        ]);
        
        this.userCount = users.length;
        this.productCount = products.length;
      } catch (err) {
        this.error = '获取仪表板数据失败: ' + (err.response?.data?.detail || err.message);
      } finally {
        this.loading = false;
      }
    },
    getCurrentUser() {
      // 从localStorage获取当前用户信息
      const user = localStorage.getItem('user');
      this.currentUser = user ? JSON.parse(user) : null;
    }
  },
  mounted() {
    this.getCurrentUser();
    this.fetchDashboardData();
  }
};
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  margin-bottom: 2rem;
  color: #333;
  text-align: center;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 2.5rem;
  margin-right: 1rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border-radius: 50%;
}

.user-icon {
  background-color: #e3f2fd;
}

.product-icon {
  background-color: #e8f5e9;
}

.card-content h3 {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 1rem;
  font-weight: 500;
}

.card-value {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.card-link a {
  color: #4CAF50;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
}

.card-link a:hover {
  text-decoration: underline;
}

.recent-activity {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.recent-activity h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.activity-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-label {
  color: #666;
  font-size: 0.9rem;
}

.activity-value {
  font-weight: 600;
  color: #333;
}

.status-online {
  color: #4CAF50;
}

.quick-actions {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.quick-actions h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  color: white;
  transition: transform 0.3s, box-shadow 0.3s;
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.users-button {
  background-color: #2196F3;
}

.products-button {
  background-color: #4CAF50;
}

.action-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.action-text {
  font-weight: 500;
}

@media (max-width: 768px) {
  .home-container {
    padding: 1rem;
  }
  
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
  
  .activity-list {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>