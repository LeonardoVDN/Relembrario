<!-- src/components/SideMenuComponent.vue -->
<template>
  <div :class="['sidebar', { 'collapsed': isCollapsed }]">
    <!-- Botão de retração (sempre visível) -->
    <button @click="toggleSidebar" class="toggle-btn">
      <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
    </button>

    <!-- Header com o nome e imagem de perfil -->
    <div class="header text-center my-4">
      <img src="path/to/profile-image.jpg" alt="Profile" class="profile-image mb-2" />
      <h5 v-if="!isCollapsed" class="username">Fulano de Tal</h5>
    </div>

    <!-- Campo de Pesquisa -->
    <div v-if="!isCollapsed" class="search px-3 mb-3">
      <input type="text" v-model="searchQuery" class="form-control" placeholder="Pesquisar" />
    </div>

    <!-- Botões de ação -->
    <div v-if="!isCollapsed" class="actions px-3 mb-3">
      <button @click="addMemoria" class="btn btn-primary w-100 mb-2">Adicionar Memória</button>
      <button @click="addCategoria" class="btn btn-secondary w-100">Adicionar Categoria</button>
    </div>

    <!-- Lista de Categorias -->
    <div class="categories px-3">
      <button class="btn btn-danger w-100 mb-3" @click="removeApp">Remover App</button>
      <ul class="list-group">
        <li
          v-for="(categoria, index) in categorias"
          :key="index"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          <span v-if="!isCollapsed">{{ categoria }}</span>
          <i v-if="categoria === 'Categoria 2'" class="bi bi-grid-fill"></i>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      isCollapsed: false,
      categorias: ["Categoria 0", "Categoria 1", "Categoria 2", "Categoria 3"],
    };
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    addMemoria() {
      // Função para adicionar memória
      console.log("Adicionar Memória");
    },
    addCategoria() {
      // Função para adicionar categoria
      console.log("Adicionar Categoria");
    },
    removeApp() {
      // Função para remover app
      console.log("Remover App");
    },
  },
};
</script>

<style scoped>
.sidebar {
  background-color: #343a40;
  color: #fff;
  min-width: 250px;
  transition: width 0.3s;
  overflow: hidden;
  position: relative;
}

.collapsed {
  width: 60px;
}

.toggle-btn {
  position: absolute;
  top: 20px;
  right: -15px;
  width: 30px;
  height: 30px;
  background-color: #343a40;
  border: none;
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
}

.header {
  text-align: center;
}

.profile-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}

.username {
  font-size: 1rem;
}

.search input {
  background-color: #495057;
  border: none;
  color: #fff;
}

.search input::placeholder {
  color: #ced4da;
}

.actions .btn {
  background-color: #495057;
  border: none;
}

.categories .btn-danger {
  background-color: #dc3545;
  border: none;
}

.list-group-item {
  background-color: #495057;
  border: none;
  color: #fff;
}

.list-group-item:hover {
  background-color: #6c757d;
}

.bi {
  font-size: 1.2rem;
}
</style>
