<template>
  <div id="app">
    <header>
      <!-- می‌توانید هدر یا منو را در اینجا قرار دهید -->
    </header>

    <router-view></router-view> <!-- کامپوننت‌ها براساس روت در اینجا نمایش داده می‌شوند -->

    <footer>
      <!-- می‌توانید فوتر را در اینجا قرار دهید -->
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* استایل‌های کلی */
</style>
