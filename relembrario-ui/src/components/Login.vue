<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <!-- Campos de login -->
        <!-- ... -->
        <button type="submit">Entrar</button>
      </form>
    </div>
  </template>
  
  <script>
  import AuthService from '../services/authService';
  
  export default {
    data() {
      return {
        user: {
          username: '',
          password: ''
        },
        message: ''
      };
    },
    methods: {
      handleLogin() {
        AuthService.login(this.user)
          .then(() => {
            this.$router.push('/perfil');
          })
          .catch(error => {
            this.message = 'Credenciais inválidas.';
          });
      }
    }
  };
  </script>
  