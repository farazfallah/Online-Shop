<template>
    <div>
      <h2>Products for Category: {{ category.name }}</h2>
      <div v-if="products.length > 0">
        <div v-for="product in products" :key="product.id" class="product-card">
          <img :src="product.image" alt="product image" />
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <p>Price: {{ product.price }} </p>
        </div>
      </div>
      <div v-else>
        <p>No products found for this category.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import { useRoute } from "vue-router";
  
  export default {
    name: "CategoryProducts",
    setup() {
      const route = useRoute();
      const products = ref([]);
      const category = ref({});
  
      const fetchCategoryProducts = async () => {
        try {
          // Get category info
          const categoryId = route.params.id;
          const categoryResponse = await axios.get(`http://127.0.0.1:8000/api/categories/${categoryId}/`);
          category.value = categoryResponse.data;
  
          // Get products for the category
          const productsResponse = await axios.get(`http://127.0.0.1:8000/api/category/${categoryId}/products/`);
          products.value = productsResponse.data.results;
        } catch (error) {
          console.error("Error fetching category products:", error);
        }
      };
  
      onMounted(() => {
        fetchCategoryProducts();
      });
  
      return {
        products,
        category,
      };
    },
  };
  </script>
  
  <style scoped>
  .product-card {
    border: 1px solid #ddd;
    padding: 20px;
    margin: 10px;
    text-align: center;
  }
  .product-card img {
    width: 100px;
    height: 100px;
    object-fit: cover;
  }
  </style>
  