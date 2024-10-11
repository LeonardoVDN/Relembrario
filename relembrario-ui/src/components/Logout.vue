<!-- src/components/Logout.vue -->
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
    }).catch(error => {
      console.error("Erro ao efetuar logout:", error);
      // Opcional: redirecionar mesmo em caso de erro ou mostrar uma mensagem
      this.$router.push('/login');
    });
  }
};
</script>

<style scoped>
/* Estilos opcionais */
</style>
