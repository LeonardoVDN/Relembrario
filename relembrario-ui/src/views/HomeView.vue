<!-- src/views/HomeView.vue -->
<template>
  <div class="home-view">
    <!-- Sidebar à esquerda (Integrado) -->
    <div :class="['sidebar', { 'collapsed': isCollapsed }]" class="side-menu">
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
        <div class="mb-3 align-items-center">  
          <add-memory-modal @memory-added="refreshMemories" />
          <add-tag-component @tag-added="handleTagAdded" />
          <router-link to="/logout" class="ml-auto">
            <button type="button" class="btn btn-danger">Sair</button>
          </router-link>
        </div>
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

    <!-- Conteúdo das Memórias -->
    <div class="content">
      <h1 class="mb-4">Minhas Lembranças</h1>

      <!-- Lista de Memórias -->
      <div class="memories-list">
        <card-memory ref="cardMemory" />
      </div>
    </div>
  </div>
</template>

<script>
import CardMemory from "@/components/CardMemory.vue";
import AddMemoryModal from "@/components/AddMemoryModal.vue";
import AddTagComponent from "@/components/AddTagComponent.vue";

export default {
  name: "HomeView",
  components: {
    CardMemory,
    AddMemoryModal,
    AddTagComponent,
  },
  data() {
    return {
      // Dados do SideMenuComponent
      searchQuery: "",
      isCollapsed: false,
      categorias: ["Categoria 0", "Categoria 1", "Categoria 2", "Categoria 3"],
    };
  },
  methods: {
    // Métodos do HomeView
    refreshMemories() {
      // Chama o método 'fetchLembrancas' do componente 'CardMemory.vue' para atualizar a lista
      if (this.$refs.cardMemory) {
        this.$refs.cardMemory.fetchLembrancas();
      }
      console.log("Memória adicionada. Lista de memórias atualizada.");
    },
    handleTagAdded() {
      // Lógica para lidar com a adição de uma nova tag
      console.log("Tag adicionada. Atualizar tags disponíveis.");
      // Os modais que buscam tags novamente ao serem abertos já refletirão a nova tag
    },

    // Métodos do SideMenuComponent
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    addMemoria() {
      // Função para adicionar memória
      console.log("Adicionar Memória");
      // Você pode reutilizar o componente AddMemoryModal aqui, se aplicável
    },
    addCategoria() {
      // Função para adicionar categoria
      console.log("Adicionar Categoria");
      // Implementar lógica conforme necessário
    },
    removeApp() {
      // Função para remover app
      console.log("Remover App");
      // Implementar lógica conforme necessário
    },
  },
};
</script>

<style scoped>
.home-view {
  display: flex;
  min-height: 100vh;
}

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

.mb-3.d-flex {
  gap: 10px;
}

.ml-auto {
  margin-left: auto;
}

/* Ajustes adicionais para garantir que o conteúdo não seja ocultado quando a sidebar estiver colapsada */
.sidebar.collapsed + .content {
  margin-left: 60px;
}

@media (max-width: 768px) {
  .home-view {
    flex-direction: column;
  }

  .sidebar {
    min-width: 100%;
    width: 100%;
    height: auto;
  }

  .collapsed {
    width: 100%;
  }
}
</style>
