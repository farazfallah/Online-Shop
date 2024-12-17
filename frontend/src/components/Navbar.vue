<template>
    <nav>
      <ul>
        <li><router-link to="/">صفحه اصلی</router-link></li>
        <li><router-link to="/categories">دسته‌بندی‌ها</router-link></li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'Navbar',
  };
  </script>
  
  <style scoped>
  nav ul {
    list-style: none;
    display: flex;
    gap: 1rem;
  }
  </style>
  