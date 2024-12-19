import { createApp } from 'vue';
import App from './App.vue';
import router from './router';  // وارد کردن router

const app = createApp(App);

app.use(router);  // استفاده از Vue Router

app.mount('#app');
