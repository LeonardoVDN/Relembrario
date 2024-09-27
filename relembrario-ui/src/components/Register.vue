<template>
    <div>
      <h2>Registro</h2>
      <form @submit.prevent="handleRegister">
        <!-- Campos de registro -->
        <!-- ... -->
        <button type="submit">Registrar</button>
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
          email: '',
          password: '',
          password2: '',
          first_name: '',
          last_name: ''
        },
        message: ''
      };
    },
    methods: {
      handleRegister() {
        AuthService.register(this.user)
          .then(() => {
            this.message = 'Registrado com sucesso!';
            this.$router.push('/login');
          })
          .catch(error => {
            this.message = error.response.data;
          });
      }
    }
  };
  </script>
  