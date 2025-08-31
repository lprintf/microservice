<template>
  <div class="user-list-container">
    <h2>用户列表</h2>
    
    <!-- 管理员可以添加用户 -->
    <div v-if="currentUser?.role === 'admin'" class="add-user-button-container">
      <button @click="showAddUserForm = !showAddUserForm">
        {{ showAddUserForm ? '取消添加' : '添加用户' }}
      </button>
    </div>
    
    <!-- 添加用户表单 -->
    <div v-if="currentUser?.role === 'admin' && showAddUserForm" class="add-user-form">
      <form @submit.prevent="handleAddUser">
        <div class="form-row">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="newUser.username" placeholder="用户名" required />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="newUser.email" type="email" placeholder="邮箱" required />
          </div>
        </div>
        <div class="form-group">
          <label>姓名</label>
          <input v-model="newUser.name" placeholder="姓名" required />
        </div>
        <button type="submit" :disabled="addingUser">
          {{ addingUser ? '添加中...' : '添加用户' }}
        </button>
      </form>
    </div>
    
    <!-- 用户列表 -->
    <div class="user-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="users.length === 0" class="empty">暂无用户</div>
      <table v-else class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>姓名</th>
            <th v-if="currentUser?.role === 'admin'">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
            <td v-if="currentUser?.role === 'admin'">
              <button @click="getUserProducts(user.id)">查看产品</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { userAPI } from '../utils/api.js';

export default {
  name: 'UserList',
  data() {
    return {
      users: [],
      loading: false,
      error: '',
      currentUser: JSON.parse(localStorage.getItem('user')),
      showAddUserForm: false,
      newUser: {
        username: '',
        email: '',
        name: ''
      },
      addingUser: false
    };
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.error = '';
      try {
        this.users = await userAPI.getUsers();
      } catch (err) {
        this.error = '获取用户列表失败: ' + (err.response?.data?.detail || err.message);
      } finally {
        this.loading = false;
      }
    },
    async handleAddUser() {
      this.addingUser = true;
      this.error = '';
      try {
        const addedUser = await userAPI.createUser(this.newUser);
        this.users.push(addedUser);
        // 重置表单
        this.newUser = {
          username: '',
          email: '',
          name: ''
        };
        this.showAddUserForm = false;
      } catch (err) {
        this.error = '添加用户失败: ' + (err.response?.data?.detail || err.message);
      } finally {
        this.addingUser = false;
      }
    },
    getUserProducts(userId) {
      // 导航到产品页面并带上用户ID参数
      this.$router.push({ path: '/products', query: { userId } });
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.user-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

.add-user-button-container {
  margin-bottom: 20px;
}

button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.add-user-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-group {
  margin-bottom: 15px;
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #111;
  font-weight: 600;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.user-list {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
}

.loading, .error, .empty {
  padding: 40px;
  text-align: center;
}

.error {
  color: #f44336;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th, .users-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  color: #000;
}

.users-table th {
  background-color: #f2f2f2;
  font-weight: 600;
}

.users-table tr:hover {
  background-color: #f5f5f5;
}
</style>