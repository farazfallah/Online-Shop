<template>
    <div class="category-list">
      <h1 class="title">Categories</h1>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="category-grid">
        <div class="category-card" v-for="category in categories" :key="category.id">
          <div class="category-card-header">
            <i :class="category.icon" class="category-icon"></i>
            <h3 class="category-name">{{ category.name }}</h3>
          </div>
          <img v-if="category.image" :src="category.image" alt="Category Image" class="category-image" />
          <p class="category-description">{{ category.description }}</p>
          <div class="subcategory-list">
            <span v-if="category.subcategories.length > 0">Subcategories:</span>
            <ul>
              <li v-for="subCategory in category.subcategories" :key="subCategory">{{ subCategory }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CategoryList',
    data() {
      return {
        categories: [],
        loading: true,
        error: null,
      };
    },
    methods: {
      fetchCategories() {
        axios
          .get('http://127.0.0.1:8000/api/categories/')
          .then(response => {
            this.categories = response.data.results;
            this.loading = false;
          })
          .catch(error => {
            this.error = 'Failed to fetch categories';
            console.error(error);
            this.loading = false;
          });
      },
    },
    mounted() {
      this.fetchCategories();
    },
  };
  </script>
  
  <style scoped>
  .category-list {
    padding: 20px;
    font-family: 'Arial', sans-serif;
    background-color: #f9f9f9;
    min-height: 100vh;
  }
  
  .title {
    text-align: center;
    font-size: 2rem;
    color: #333;
    margin-bottom: 30px;
  }
  
  .loading {
    text-align: center;
    font-size: 1.5rem;
    color: #888;
  }
  
  .error {
    text-align: center;
    font-size: 1.5rem;
    color: red;
  }
  
  .category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    padding: 0 20px;
  }
  
  .category-card {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .category-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }
  
  .category-card-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .category-icon {
    font-size: 2rem;
    margin-right: 10px;
    color: #007bff;
  }
  
  .category-name {
    font-size: 1.25rem;
    font-weight: bold;
    color: #333;
  }
  
  .category-image {
    width: 100%;
    height: auto;
    border-radius: 8px;
    margin-top: 10px;
    object-fit: cover;
  }
  
  .category-description {
    margin-top: 10px;
    font-size: 1rem;
    color: #555;
  }
  
  .subcategory-list {
    margin-top: 15px;
    font-size: 0.875rem;
    color: #777;
  }
  
  .subcategory-list ul {
    margin-top: 5px;
    padding-left: 15px;
  }
  
  .subcategory-list ul li {
    list-style-type: circle;
  }
  
  @media (max-width: 768px) {
    .category-grid {
      padding: 0 10px;
    }
    .category-card {
      padding: 15px;
    }
    .title {
      font-size: 1.75rem;
    }
  }
  </style>
  