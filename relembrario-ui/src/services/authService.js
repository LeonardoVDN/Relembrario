// src/services/authService.js

import http from './http';

class AuthService {
  login(user) {
    return http
      .post('login/', {
        username: user.username,
        password: user.password
      })
      .then(response => {
        if (response.data.access && response.data.refresh) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
      });
  }

  logout() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.refresh) {
      return http
        .post('logout/', { refresh_token: user.refresh })
        .then(() => {
          localStorage.removeItem('user');
        })
        .catch(error => {
          console.error(error);
          localStorage.removeItem('user');
        });
    } else {
      localStorage.removeItem('user');
    }
  }

  register(user) {
    return http.post('register/', {
      username: user.username,
      email: user.email,
      password: user.password,
      password2: user.password2,
      first_name: user.first_name,
      last_name: user.last_name
    });
  }
}

export default new AuthService();
