<!-- src/views/HomeView.vue -->
<template>
  <div class="home-view">
    <!-- Seção de Alertas de Sucesso e Erro -->
    <div class="container mt-3">
      <!-- Alerta de Sucesso -->
      <div
        v-if="successMessage"
        class="alert alert-success alert-dismissible fade show"
        role="alert"
      >
        {{ successMessage }}
        <button
          type="button"
          class="btn-close"
          @click="clearSuccessMessage"
          aria-label="Close"
        ></button>
      </div>

      <!-- Alerta de Erro -->
      <div
        v-if="errorMessage"
        class="alert alert-danger alert-dismissible fade show"
        role="alert"
      >
        {{ errorMessage }}
        <button
          type="button"
          class="btn-close"
          @click="clearErrorMessage"
          aria-label="Close"
        ></button>
      </div>
    </div>

    <!-- Sidebar à esquerda -->
    <div :class="['sidebar', { collapsed: isCollapsed }]">
      <!-- Botão de retração -->
      <button @click="toggleSidebar" class="toggle-btn">
        <i class="bi" :class="isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
      </button>

      <!-- Header com o nome e imagem de perfil -->
      <div class="header text-center my-4">
        <img
          :src="profilePictureUrl || defaultProfileImage"
          alt="Profile"
          class="profile-image mb-2"
        />
        <h5 v-if="!isCollapsed" class="username">{{ displayName || userName }}</h5>
      </div>

      <!-- Campo de Pesquisa -->
      <div v-if="!isCollapsed && !showProfile" class="search px-3 mb-3">
        <input
          type="text"
          v-model="searchQuery"
          class="form-control"
          placeholder="Pesquisar"
        />
      </div>

      <!-- Botões de ação -->
      <div v-if="!isCollapsed" class="actions px-3 mb-3">
        <div class="mb-3 align-items-center">
          <!-- Mostrar botões somente quando na visualização das memórias -->
          <div v-if="!showProfile">
            <add-tag-component
              @tag-added="handleTagAdded"
              @tag-add-error="handleTagAddError"
              @tag-edit-success="handleTagEditSuccess"
              @tag-edit-error="handleTagEditError"
              @tag-delete-success="handleTagDeleteSuccess"
              @tag-delete-error="handleTagDeleteError"
              @tag-fetch-error="handleTagFetchError"
            />
            <div class="mb-3">
              <add-memory-modal
                ref="addMemoryModal"
                @memory-added="handleMemoryAdded"
                @memory-add-error="handleMemoryAddError"
              />
            </div>
          </div>
          <!-- Botão "Meu Perfil" ou "Voltar" -->
          <button @click="toggleProfile" class="btn btn-primary mb-2">
            {{ showProfile ? 'Voltar' : 'Meu Perfil' }}
          </button>
          <router-link to="/logout">
            <button type="button" class="btn btn-danger">Sair</button>
          </router-link>
        </div>
      </div>

      <!-- Lista de Categorias (exibir somente na visualização das memórias) -->
      <div v-if="!isCollapsed && !showProfile" class="categories px-3">
        <ul class="list-group">
          <li
            v-for="(categoria, index) in categorias"
            :key="index"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span>{{ categoria }}</span>
            <!-- Ícone de exemplo -->
            <i v-if="categoria === 'Categoria 2'" class="bi bi-grid-fill"></i>
          </li>
        </ul>
      </div>
    </div>

    <!-- Conteúdo principal -->
    <div :class="['content', { 'collapsed-content': isCollapsed }]">
      <!-- Exibir o título conforme a visualização atual -->
      <h1 class="mb-4">
        {{ showProfile ? 'Meu Perfil' : 'Minhas Lembranças' }}
      </h1>

      <!-- Exibir o componente de perfil ou a lista de memórias -->
      <div v-if="showProfile">
        <!-- Componente de perfil integrado -->
        <user-profile
          @profile-updated="handleProfileUpdated"
          @profile-update-error="handleProfileUpdateError"
        />
      </div>
      <div v-else>
        <!-- Conteúdo das memórias integrado -->
        <div class="lembrancas-container">
          <!-- Estado de Carregamento -->
          <div v-if="isLoading" class="text-center">
            <p>Carregando lembranças...</p>
          </div>

          <!-- Estado de Erro -->
          <div v-else-if="error" class="text-center">
            <p>Não foi possível carregar as lembranças.</p>
            <button @click="fetchLembrancas" class="btn btn-primary mt-3">
              Tentar Novamente
            </button>
          </div>

          <!-- Estado Sem Memórias -->
          <div v-else-if="lembrancas.length === 0" class="text-center">
            <p>Não há lembranças.</p>
            <!-- Botão "Adicionar Memória" aparece somente quando não há memórias -->
            <button @click="openAddMemoryModal" class="btn btn-primary mt-3">
              Adicionar Memória
            </button>
          </div>

          <!-- Lista de Memórias -->
          <div v-else class="inter-container">
            <div
              v-for="lembranca in lembrancas"
              :key="lembranca.id"
              class="card shadow-sm mb-4"
            >
              <!-- Início do conteúdo do card -->
              <div class="card-body d-flex flex-column">
                <!-- Imagem no topo -->
                <div v-if="lembranca.imagem" class="image mb-3">
                  <img
                    :src="lembranca.imagem"
                    alt="Imagem da lembrança"
                    class="img-fluid rounded"
                  />
                </div>

                <!-- Título, badge "Destaque", data e local -->
                <h5 class="card-title">{{ lembranca.titulo }}</h5>
                <div v-if="lembranca.destaque" class="mb-2">
                  <span class="badge bg-warning text-dark">Destaque</span>
                </div>
                <h6 class="card-subtitle mb-2 text-muted">
                  {{ formatDate(lembranca.data_evento) }}
                </h6>
                <p class="card-text"><strong>Local:</strong> {{ lembranca.local }}</p>

                <!-- Descrição limitada a 200 caracteres -->
                <p class="card-text flex-grow-1">
                  {{
                    lembranca.descricao.length > 200
                      ? lembranca.descricao.substring(0, 200) + '...'
                      : lembranca.descricao
                  }}
                </p>

                <!-- Tags -->
                <div class="tags mb-3">
                  <span
                    v-for="tag in lembranca.tagsNames"
                    :key="tag"
                    class="badge bg-primary me-1"
                  >
                    {{ tag }}
                  </span>
                </div>

                <!-- Botões fixados no rodapé do card -->
                <div class="mt-auto">
                  <div class="d-flex justify-content-end">
                    <!-- Botão de Visualizar -->
                    <view-memory-modal
                      :memory="lembranca"
                      @memory-viewed="handleMemoryViewed"
                      @memory-view-error="handleMemoryViewError"
                    />
                    <!-- Botão de Editar -->
                    <edit-memory-modal
                      :memory="lembranca"
                      @memory-edited="handleMemoryEdited"
                      @memory-edit-error="handleMemoryEditError"
                    />
                    <!-- Botão de Excluir -->
                    <delete-memory-component
                      :memoryId="lembranca.id"
                      @memory-deleted="handleMemoryDeleted"
                      @memory-delete-success="handleMemoryDeleteSuccess"
                      @memory-delete-error="handleMemoryDeleteError"
                    />
                  </div>
                </div>
              </div>
              <!-- Fim do conteúdo do card -->
            </div>
          </div>
        </div>
      </div>

      <!-- Modais -->
      <!-- ... (mantido conforme o original) -->
    </div>
  </div>
</template>

<script>
import AddMemoryModal from "@/components/AddMemoryModal.vue";
import AddTagComponent from "@/components/AddTagComponent.vue";
import UserProfile from "@/components/UserProfile.vue";
import DeleteMemoryComponent from "@/components/DeleteMemoryComponent.vue";
import EditMemoryModal from "@/components/EditMemoryModal.vue";
import ViewMemoryModal from "@/components/ViewMemoryModal.vue"; // Importação do novo componente
import http from "@/services/http";
import defaultProfileImage from "@/assets/default-profile.png";

export default {
  name: "HomeView",
  components: {
    AddMemoryModal,
    AddTagComponent,
    UserProfile,
    DeleteMemoryComponent,
    EditMemoryModal,
    ViewMemoryModal, // Adicionado à lista de componentes
  },
  data() {
    return {
      searchQuery: "",
      isCollapsed: false,
      categorias: ["Categoria 0", "Categoria 1", "Categoria 2", "Categoria 3"],
      showProfile: false,
      profilePictureUrl: null,
      displayName: "",
      userName: "",
      defaultProfileImage,
      // Dados das memórias
      lembrancas: [],
      isLoading: false,
      error: false,
      // Alertas
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    // Atualiza as memórias e define uma mensagem de sucesso
    refreshMemories() {
      this.fetchLembrancas();
      this.setSuccessMessage("Memória adicionada com sucesso!");
    },
    // Manipula o evento de tag adicionada com sucesso
    handleTagAdded(message) {
      this.setSuccessMessage(message || "Tag adicionada com sucesso!");
      console.log("Tag adicionada. Atualizar tags disponíveis.");
    },
    // Manipula o evento de erro ao adicionar uma tag
    handleTagAddError(error) {
      this.setErrorMessage(error || "Erro ao adicionar a tag.");
    },
    // Manipula o evento de edição de tag com sucesso
    handleTagEditSuccess(message) {
      this.setSuccessMessage(message || "Tag atualizada com sucesso!");
    },
    // Manipula o evento de erro ao editar uma tag
    handleTagEditError(error) {
      this.setErrorMessage(error || "Erro ao editar a tag.");
    },
    // Manipula o evento de exclusão de tag com sucesso
    handleTagDeleteSuccess(message) {
      this.setSuccessMessage(message || "Tag excluída com sucesso!");
    },
    // Manipula o evento de erro ao excluir uma tag
    handleTagDeleteError(error) {
      this.setErrorMessage(error || "Erro ao excluir a tag.");
    },
    // Manipula o evento de erro ao buscar tags
    handleTagFetchError(error) {
      this.setErrorMessage(error || "Erro ao buscar tags.");
    },
    // Manipula o evento de memória adicionada com sucesso
    handleMemoryAdded() {
      this.refreshMemories();
    },
    // Manipula o evento de erro ao adicionar uma memória
    handleMemoryAddError(error) {
      this.setErrorMessage(error || "Erro ao adicionar a memória.");
    },
    // Manipula o evento de memória editada com sucesso
    handleMemoryEdited() {
      this.setSuccessMessage("Memória editada com sucesso!");
      this.fetchLembrancas();
    },
    // Manipula o evento de erro ao editar uma memória
    handleMemoryEditError(error) {
      this.setErrorMessage(error || "Erro ao editar a memória.");
    },
    // Manipula o evento de memória deletada com sucesso
    handleMemoryDeleted(memoryId) {
      // Opcional: Pode ser usado para lógica adicional se necessário
      this.setSuccessMessage("Memória excluída com sucesso!");
      this.fetchLembrancas();
    },
    // Manipula o evento de sucesso na exclusão de uma memória
    handleMemoryDeleteSuccess(message) {
      this.setSuccessMessage(message || "Memória excluída com sucesso!");
    },
    // Manipula o evento de erro na exclusão de uma memória
    handleMemoryDeleteError(error) {
      this.setErrorMessage(error || "Erro ao excluir a memória.");
    },
    // Manipula o evento de memória visualizada com sucesso
    handleMemoryViewed() {
      // Opcional: Pode adicionar lógica para quando uma memória é visualizada
      this.setSuccessMessage("Memória visualizada com sucesso!");
    },
    // Manipula o evento de erro ao visualizar uma memória
    handleMemoryViewError(error) {
      this.setErrorMessage(error || "Erro ao visualizar a memória.");
    },
    // Manipula o evento de perfil atualizado com sucesso
    handleProfileUpdated() {
      this.fetchUserProfile();
      this.setSuccessMessage("Perfil atualizado com sucesso!");
    },
    // Manipula o evento de erro ao atualizar o perfil
    handleProfileUpdateError(error) {
      this.setErrorMessage(error || "Erro ao atualizar o perfil.");
    },
    // Alterna a retração da sidebar
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    // Abre o modal de adicionar memória
    openAddMemoryModal() {
      if (this.$refs.addMemoryModal) {
        this.$refs.addMemoryModal.openModal();
      }
    },
    // Alterna a visualização do perfil
    toggleProfile() {
      this.showProfile = !this.showProfile;
    },
    // Limpa a mensagem de sucesso
    clearSuccessMessage() {
      this.successMessage = "";
    },
    // Limpa a mensagem de erro
    clearErrorMessage() {
      this.errorMessage = "";
    },
    // Define a mensagem de sucesso e agenda a limpeza automática após 5 segundos
    setSuccessMessage(message) {
      this.successMessage = message;
      // Limpar a mensagem após 5 segundos
      setTimeout(() => {
        this.clearSuccessMessage();
      }, 5000);
    },
    // Define a mensagem de erro e agenda a limpeza automática após 5 segundos
    setErrorMessage(message) {
      this.errorMessage = message;
      // Limpar a mensagem após 5 segundos
      setTimeout(() => {
        this.clearErrorMessage();
      }, 5000);
    },
    // Busca o perfil do usuário
    async fetchUserProfile() {
      try {
        const response = await http.get("/profile/");
        const user = response.data;
        this.userName = user.username;
        this.displayName = user.profile ? user.profile.display_name : "";
        this.profilePictureUrl = user.profile ? user.profile.profile_picture : null;
      } catch (error) {
        console.error("Erro ao buscar perfil do usuário:", error);
        this.setErrorMessage("Não foi possível carregar o perfil do usuário.");
      }
    },
    // Formata a data no formato "dia de mês de ano"
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("pt-BR", options);
    },
    // Busca o nome da tag pelo ID
    fetchTagName(tagId) {
      return http
        .get(`/tags/${tagId}/`)
        .then((response) => response.data.nome)
        .catch((error) => {
          console.error(`Erro ao buscar a tag de ID ${tagId}:`, error);
          return `Tag ${tagId}`;
        });
    },
    // Busca as memórias do usuário
    async fetchLembrancas() {
      this.isLoading = true;
      this.error = false;
      try {
        const response = await http.get("/lembrancas/");
        const lembrancas = response.data;

        const updatedLembrancas = await Promise.all(
          lembrancas.map(async (lembranca) => {
            const tagsNames = await Promise.all(
              lembranca.tags.map((tagId) => this.fetchTagName(tagId))
            );
            return { ...lembranca, tagsNames };
          })
        );

        this.lembrancas = updatedLembrancas;
      } catch (error) {
        console.error("Erro ao buscar lembranças:", error);
        this.error = true;
        this.setErrorMessage("Não foi possível carregar as lembranças.");
      } finally {
        this.isLoading = false;
      }
    },
  },
  mounted() {
    this.fetchUserProfile();
    this.fetchLembrancas();
  },
};
</script>

<style scoped>
/* Seção de Alertas */
.container.mt-3 {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1050;
}

/* Estilos existentes */
.inter-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 15px;
  padding: 20px;
}

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
  object-fit: cover;
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
  width: 100%;
  margin-bottom: 10px;
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
  margin-left: 250px; /* Ajuste para espaço da sidebar */
  transition: margin-left 0.3s;
}

.collapsed + .content {
  margin-left: 60px; /* Ajuste para sidebar colapsada */
}

h1 {
  font-size: 28px;
  color: #007bff;
}

.memories-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.mb-3.d-flex {
  gap: 10px;
}

.ml-auto {
  margin-left: auto;
}

/* Ajustes para conteúdo quando a sidebar estiver colapsada */
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

  .content {
    margin-left: 0;
  }
}

/* Estilos do Card */
.lembrancas-container {
  padding: 20px;
  display: grid;
}

.card {
  border: none;
  width: 100%;
  height: auto;
  background-color: #fff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-title {
  font-size: 1.25rem;
  color: #007bff;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #666;
}

.card-text {
  color: #333;
}

.card-text.flex-grow-1 {
  flex-grow: 1;
}

.image img {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.tags {
  margin-top: 10px;
}

.badge {
  font-size: 0.8rem;
}

.text-center {
  text-align: center;
}

.btn-primary {
  /* Personalize conforme necessário */
}

.mt-3 {
  margin-top: 1rem;
}

.mt-auto {
  margin-top: auto;
}
</style>
