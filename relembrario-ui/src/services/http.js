// src/services/http.js

import axios from 'axios';

const http = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json'
  }
});

http.interceptors.request.use(config => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user && user.access) {
    config.headers['Authorization'] = 'Bearer ' + user.access;
  }
  return config;
});

http.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // Verifica se a resposta é 401 e se a requisição original não é para login ou refresh
    const isAuthRoute = originalRequest.url.includes('login/') ||
                       originalRequest.url.includes('register/') ||
                       originalRequest.url.includes('token/refresh/');
                       
    if (error.response.status === 401 && !originalRequest._retry && !isAuthRoute) {
      originalRequest._retry = true;

      const user = JSON.parse(localStorage.getItem('user'));
      if (user && user.refresh) {
        try {
          const response = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: user.refresh
          });

          // Atualiza o token no localStorage
          user.access = response.data.access;
          localStorage.setItem('user', JSON.stringify(user));

          // Atualiza o header e reenvia a requisição original
          originalRequest.headers['Authorization'] = 'Bearer ' + response.data.access;
          return http(originalRequest);
        } catch (err) {
          // Se o refresh falhar, redireciona para login
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
      } else {
        // Se não houver refresh token, redireciona para login
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default http;
