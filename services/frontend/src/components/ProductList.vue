<template>
  <div class="product-list-container">
    <h2>产品列表</h2>
    
    <!-- 添加产品按钮 -->
    <div class="add-product-button-container">
      <button @click="showAddProductForm = !showAddProductForm">
        {{ showAddProductForm ? '取消添加' : '添加产品' }}
      </button>
    </div>
    
    <!-- 添加产品表单 -->
    <div v-if="showAddProductForm" class="add-product-form">
      <form @submit.prevent="handleAddProduct">
        <div class="form-row">
          <div class="form-group">
            <label>产品名称</label>
            <input v-model="newProduct.name" placeholder="产品名称" required />
          </div>
          <div class="form-group">
            <label>价格</label>
            <input v-model="newProduct.price" type="number" step="0.01" placeholder="价格" required />
          </div>
          <div class="form-group">
            <label>用户ID</label>
            <input v-model="newProduct.user_id" type="number" placeholder="用户ID" required />
          </div>
        </div>
        <button type="submit" :disabled="addingProduct">
          {{ addingProduct ? '添加中...' : '添加产品' }}
        </button>
      </form>
    </div>
    
    <!-- 产品列表 -->
    <div class="product-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="products.length === 0" class="empty">暂无产品</div>
      <table v-else class="products-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>产品名称</th>
            <th>价格</th>
            <th>用户ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.price.toFixed(2) }}</td>
            <td>{{ product.user_id }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { productAPI } from '../utils/api.js';

export default {
  name: 'ProductList',
  data() {
    return {
      products: [],
      loading: false,
      error: '',
      showAddProductForm: false,
      newProduct: {
        name: '',
        price: '',
        user_id: ''
      },
      addingProduct: false
    };
  },
  methods: {
    async fetchProducts() {
      this.loading = true;
      this.error = '';
      try {
        // 检查是否有userId查询参数
        const userId = this.$route.query.userId;
        if (userId) {
          // 如果有，只获取指定用户的产品
          this.products = await productAPI.getProducts(userId);
        } else {
          // 否则获取所有产品
          this.products = await productAPI.getProducts();
        }
      } catch (err) {
        this.error = '获取产品列表失败: ' + (err.response?.data?.detail || err.message);
      } finally {
        this.loading = false;
      }
    },
    async handleAddProduct() {
      this.addingProduct = true;
      this.error = '';
      try {
        // 转换价格为数字类型
        const productData = {
          ...this.newProduct,
          price: parseFloat(this.newProduct.price)
        };
        
        const addedProduct = await productAPI.createProduct(productData);
        this.products.push(addedProduct);
        
        // 重置表单
        this.newProduct = {
          name: '',
          price: '',
          user_id: ''
        };
        this.showAddProductForm = false;
      } catch (err) {
        this.error = '添加产品失败: ' + (err.response?.data?.detail || err.message);
      } finally {
        this.addingProduct = false;
      }
    }
  },
  mounted() {
    this.fetchProducts();
  },
  watch: {
    // 监听路由参数变化，重新获取产品列表
    '$route.query': {
      handler() {
        this.fetchProducts();
      },
      deep: true
    }
  }
};
</script>

<style scoped>
.product-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

.add-product-button-container {
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

.add-product-form {
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

.product-list {
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

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th, .products-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  color: #000;
}

.products-table th {
  background-color: #f2f2f2;
  font-weight: 600;
}

.products-table tr:hover {
  background-color: #f5f5f5;
}
</style>