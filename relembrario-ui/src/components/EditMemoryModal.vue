<!-- src/components/EditMemoryModal.vue -->
<template>
    <div>
      <button @click="openModal" class="btn btn-warning btn-sm">Editar</button>
  
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Editar Memória</h5>
            <button @click="closeModal" class="btn-close">&times;</button>
          </div>
  
          <div class="modal-body">
            <form @submit.prevent="submitEdit">
              <div class="mb-3">
                <label for="title" class="form-label">Título</label>
                <input type="text" v-model="title" id="title" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Descrição</label>
                <textarea v-model="description" id="description" class="form-control" rows="3" required></textarea>
              </div>
              <div class="mb-3">
                <label for="location" class="form-label">Local</label>
                <input type="text" v-model="location" id="location" class="form-control" />
              </div>
              <div class="mb-3">
                <label for="eventDate" class="form-label">Data do Evento</label>
                <input type="date" v-model="eventDate" id="eventDate" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">Tags</label>
                <div v-if="availableTags.length">
                  <div v-for="tag in availableTags" :key="tag.id" class="form-check">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      :id="'edit-tag-' + tag.id"
                      :value="tag.id"
                      v-model="selectedTags"
                    />
                    <label class="form-check-label" :for="'edit-tag-' + tag.id">
                      {{ tag.name || tag.nome }}
                    </label>
                  </div>
                </div>
                <div v-else>
                  <p v-if="isLoadingTags">Carregando tags...</p>
                  <p v-else>Não há tags disponíveis.</p>
                </div>
              </div>
              <div class="mb-3">
                <label for="image" class="form-label">Imagem</label>
                <input type="file" @change="handleFileUpload" id="image" class="form-control" />
                <div v-if="currentImage" class="mt-2">
                  <img :src="currentImage" alt="Imagem Atual" class="img-fluid rounded" />
                </div>
              </div>
  
              <button type="submit" class="btn btn-success">Salvar Alterações</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      memory: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        showModal: false,
        title: this.memory.titulo,
        description: this.memory.descricao,
        location: this.memory.local,
        eventDate: this.memory.data_evento ? this.memory.data_evento.substring(0,10) : null,
        availableTags: [],
        selectedTags: this.memory.tags, // IDs das tags
        image: null,
        currentImage: this.memory.imagem,
        isLoadingTags: false,
      };
    },
    methods: {
      openModal() {
        this.showModal = true;
        this.fetchTags();
      },
      closeModal() {
        this.showModal = false;
        this.resetForm();
      },
      handleFileUpload(event) {
        this.image = event.target.files[0];
      },
      async fetchTags() {
        this.isLoadingTags = true;
        try {
          const user = JSON.parse(localStorage.getItem("user"));
          const token = user?.access;
  
          if (!token) throw new Error("Token não encontrado");
  
          const response = await fetch("http://localhost:8000/api/tags/", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` },
          });
  
          if (!response.ok) throw new Error("Erro ao buscar tags");
  
          const data = await response.json();
          this.availableTags = data;
        } catch (error) {
          console.error("Erro ao buscar tags:", error);
          alert("Não foi possível carregar as tags.");
        } finally {
          this.isLoadingTags = false;
        }
      },
      async submitEdit() {
        const formData = new FormData();
        formData.append("titulo", this.title);
        formData.append("descricao", this.description);
        formData.append("local", this.location);
        if (this.eventDate) formData.append("data_evento", this.eventDate);
        if (this.image) formData.append("imagem", this.image);
        this.selectedTags.forEach(tagId => formData.append("tags", tagId));
  
        try {
          const user = JSON.parse(localStorage.getItem("user"));
          const token = user?.access;
          if (!token) throw new Error("Token não encontrado");
  
          const response = await fetch(`http://localhost:8000/api/lembrancas/${this.memory.id}/`, {
            method: "PUT",
            headers: { "Authorization": `Bearer ${token}` },
            body: formData,
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Erro ao editar memória");
          }
  
          this.closeModal();
          this.$emit("memory-edited");
          alert("Memória editada com sucesso!");
        } catch (error) {
          console.error("Erro ao editar memória:", error);
          alert(error.message);
        }
      },
      resetForm() {
        this.title = this.memory.titulo;
        this.description = this.memory.descricao;
        this.location = this.memory.local;
        this.eventDate = this.memory.data_evento ? this.memory.data_evento.substring(0,10) : null;
        this.selectedTags = this.memory.tags;
        this.image = null;
        this.currentImage = this.memory.imagem;
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 500px;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .btn-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }
  </style>
  