<template>
    <div>
      <p>Saindo...</p>
    </div>
  </template>
  
  <script>
  import AuthService from '../services/authService';
  
  export default {
    name: 'Logout',
    created() {
      AuthService.logout().then(() => {
        this.$router.push('/login');
      });
    }
  };
  </script>
  
  <style scoped>
  /* Estilos opcionais */
  </style>
  