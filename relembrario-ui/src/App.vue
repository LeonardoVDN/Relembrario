<template>
  <div id="app">
    <!-- Remova o <nav> com os links de navegação -->
    <!-- Conteúdo das rotas será renderizado aqui -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Remova qualquer estilo que esteja ligado à navegação se não for mais necessário */
</style>
