<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <h1>微服务前端</h1>
      </div>
      
      <!-- 已登录状态显示的导航 -->
      <div v-if="isLoggedIn" class="navbar-links">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/users" class="nav-link">用户管理</router-link>
        <router-link to="/products" class="nav-link">产品管理</router-link>
        <div class="user-info">
          <span class="welcome-text">欢迎, {{ currentUser?.username || '用户' }}</span>
          <button @click="handleLogout" class="logout-button">退出登录</button>
        </div>
      </div>
      
      <!-- 未登录状态显示的导航 -->
      <div v-else class="navbar-links">
        <router-link to="/login" class="nav-link">登录</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      currentUser: null,
      isLoggedIn: false
    };
  },
  watch: {
    // 监听路由变化，更新登录状态
    '$route': function() {
      this.updateUserStatus();
    }
  },
  methods: {
    updateUserStatus() {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      
      this.isLoggedIn = !!token;
      this.currentUser = user ? JSON.parse(user) : null;
    },
    handleLogout() {
      // 清除localStorage中的token和用户信息
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // 更新登录状态
      this.updateUserStatus();
      
      // 跳转到登录页面
      this.$router.push('/login');
    }
  },
  mounted() {
    this.updateUserStatus();
    
    // 监听storage事件，以便在其他标签页中登出时更新状态
    window.addEventListener('storage', this.updateUserStatus);
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.updateUserStatus);
  }
};
</script>

<style scoped>
.navbar {
  background-color: #333;
  color: white;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.5rem;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 0;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #4CAF50;
  transition: width 0.3s;
}

.nav-link:hover::after {
  width: 100%;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-text {
  font-size: 0.9rem;
  color: #ccc;
}

.logout-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.logout-button:hover {
  background-color: #d32f2f;
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .navbar-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>