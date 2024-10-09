<!-- src/views/HomeView.vue -->
<template>
  <div class="home-view">
    <!-- Sidebar à esquerda -->
    <side-menu-component class="side-menu" />

    <!-- Conteúdo das Memórias -->
    <div class="content">
      <h1 class="mb-4">Minhas Lembranças</h1>
      <div class="memories-list">
        <!-- O componente CardMemory vai lidar com suas próprias requisições -->
        <card-memory />
      </div>
    </div>
  </div>
</template>

<script>
// Importando os componentes
import SideMenuComponent from "@/components/SideMenuComponent.vue";
import CardMemory from "@/components/CardMemory.vue";

export default {
  name: "HomeView",
  components: {
    SideMenuComponent,
    CardMemory,
  },
};
</script>

<style scoped>
.home-view {
  display: flex;
  min-height: 100vh;
}

.side-menu {
  width: 250px;
}

.content {
  flex-grow: 1;
  padding: 20px;
  background-color: #f8f9fa;
}

h1 {
  font-size: 28px;
  color: #007bff;
}

.memories-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  grid-gap: 20px;
}
</style>
