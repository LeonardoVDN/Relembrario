<template>
    <div>
      <!-- Sidebar retrátil -->
      <div :class="['sidebar', { 'collapsed': isCollapsed }]">
        <!-- Header com o nome e imagem de perfil -->
        <div class="header">
          <img src="path/to/profile-image" alt="Profile" class="profile-image" />
          <span v-if="!isCollapsed" class="username">Fulano de tal</span>
        </div>
  
        <!-- Campo de Pesquisa (visível apenas se não estiver recolhido) -->
        <div v-if="!isCollapsed" class="search">
          <input type="text" v-model="searchQuery" placeholder="Search" />
        </div>
  
        <!-- Botões de ação (visíveis apenas se não estiver recolhido) -->
        <div v-if="!isCollapsed" class="actions">
          <button @click="addMemoria">Adicionar Memoria</button>
          <button @click="addCategoria">Adicionar Categorias</button>
        </div>
  
        <!-- Lista de Categorias -->
        <div class="categories">
          <button class="remove-app" @click="removeApp">Remove App</button>
          <ul>
            <li v-for="(categoria, index) in categorias" :key="index">
              <span v-if="!isCollapsed">{{ categoria }}</span>
              <i v-if="categoria === 'Categoria 2'" class="grid-icon"></i>
            </li>
          </ul>
        </div>
  
        <!-- Botão de retração (sempre visível à direita) -->
        <button @click="toggleSidebar" class="toggle-btn">
          <i class="icon">{{ isCollapsed ? '>>' : '<<' }}</i>
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: "",
        isCollapsed: false,
        categorias: ["Categoria 0", "Categoria 1", "Categoria 2", "Categoria 3"]
      };
    },
    methods: {
      toggleSidebar() {
        this.isCollapsed = !this.isCollapsed;
      },
      addMemoria() {
        // Função para adicionar memória
        console.log("Adicionar Memoria");
      },
      addCategoria() {
        // Função para adicionar categoria
        console.log("Adicionar Categoria");
      },
      removeApp() {
        // Função para remover app
        console.log("Remover App");
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilo para a sidebar */
  .sidebar {
    width: 250px;
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 10px;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    transition: transform 0.3s ease; /* Transição suave */
  }
  
  /* Quando a sidebar está recolhida */
  .collapsed {
    transform: translateX(-260px); /* Move a maior parte da barra lateral para fora, deixando uma borda visível */
  }
  
  /* Header da sidebar */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .profile-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  
  .username {
    font-weight: bold;
  }
  
  /* Botão de retração */
  .toggle-btn {
    position: absolute;
    right: -30px; /* Coloca o botão na borda direita da sidebar, fora dela */
    top: 20px;
    width: 30px;
    height: 30px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 50%;
    cursor: pointer;
    z-index: 1000; /* Garante que o botão fique acima de outros elementos */
  }
  
  .search input {
    width: 100%;
    padding: 5px;
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .actions {
    margin-top: 20px;
  }
  
  .actions button {
    display: block;
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .categories {
    margin-top: 20px;
  }
  
  .remove-app {
    color: red;
    font-weight: bold;
  }
  
  .categories ul {
    list-style: none;
    padding: 0;
  }
  
  .categories li {
    padding: 10px;
    background-color: #fff;
    margin-bottom: 5px;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
  }

  </style>
  