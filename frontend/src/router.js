import { createRouter, createWebHistory } from 'vue-router';
import CategoryList from './components/CategoryList.vue'; // مسیر کامپوننت شما

const routes = [
  {
    path: '/categories',
    name: 'categories',
    component: CategoryList,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
