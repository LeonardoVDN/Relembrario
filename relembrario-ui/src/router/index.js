// src/router/index.js

import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';
import Profile from '@/components/Profile.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue')
  },
  // Rotas públicas
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  // Rotas protegidas
  {
    path: '/perfil',
    name: 'perfil',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/logout',
    name: 'logout',
    component: Logout,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

// Guardião de rota para proteção de rotas
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('user');

  if (to.meta.requiresAuth && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;
