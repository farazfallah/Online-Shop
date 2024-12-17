import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import CategoryList from '../components/CategoryList.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/categories', name: 'Categories', component: CategoryList },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
