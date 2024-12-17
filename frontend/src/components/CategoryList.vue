<template>
    <div>
      <h1>دسته‌بندی‌ها</h1>
      <ul>
        <li v-for="category in categories" :key="category.id">{{ category.name }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  import { getCategories } from '../services/api';
  
  export default {
    name: 'CategoryList',
    data() {
      return {
        categories: [],
      };
    },
    async created() {
      try {
        this.categories = await getCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  };
  </script>
  