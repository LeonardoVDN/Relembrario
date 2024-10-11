<template>
    <div>
      <!-- Botão que abre o modal -->
      <button @click="openModal" class="btn btn-primary">Adicionar Memória</button>
  
      <!-- Modal de adicionar memória -->
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Adicionar Memória</h5>
            <button @click="closeModal" class="btn-close">&times;</button>
          </div>
  
          <div class="modal-body">
            <form @submit.prevent="submitMemory">
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
                      :id="'tag-' + tag.id"
                      :value="tag.id"
                      v-model="selectedTags"
                    />
                    <label class="form-check-label" :for="'tag-' + tag.id">
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
              </div>
  
              <button type="submit" class="btn btn-success">Salvar</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showModal: false,
        title: "",
        description: "",
        location: "",
        eventDate: null,
        availableTags: [], // Lista de tags disponíveis da API
        selectedTags: [],  // IDs das tags selecionadas
        image: null,
        isLoadingTags: false, // Indicador de carregamento de tags
      };
    },
    methods: {
      openModal() {
        this.showModal = true;
        this.fetchTags(); // Buscar as tags quando o modal é aberto
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
  
          if (!token) {
            throw new Error("Token não encontrado");
          }
  
          const response = await fetch("http://localhost:8000/api/tags/", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${token}`,
              // "Content-Type": "application/json", // Não é necessário para GET
            },
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro ao buscar tags:", errorData);
            throw new Error("Erro ao buscar tags");
          }
  
          const data = await response.json();
          console.log("Tags recebidas da API:", data); // Log para depuração
          this.availableTags = data; // Assumindo que a resposta é uma lista de tags com 'id' e 'name'
        } catch (error) {
          console.error("Erro ao buscar tags:", error);
          alert("Não foi possível carregar as tags. Tente novamente mais tarde.");
        } finally {
          this.isLoadingTags = false;
        }
      },
      async submitMemory() {
        const formData = new FormData();
        formData.append("titulo", this.title);
        formData.append("descricao", this.description);
        formData.append("local", this.location);
  
        // Certificar que a data está no formato correto
        if (this.eventDate) {
          formData.append("data_evento", this.eventDate); // Formato YYYY-MM-DD
        }
  
        if (this.image) {
          formData.append("imagem", this.image);
        }
  
        // Enviar as tags como múltiplas entradas 'tags'
        this.selectedTags.forEach(tagId => {
          formData.append("tags", tagId); // Alterado de "tags[]" para "tags"
        });
  
        // Inspeciona o FormData
        for (let pair of formData.entries()) {
          console.log(`${pair[0]}: ${pair[1]}`);
        }
  
        try {
          const user = JSON.parse(localStorage.getItem("user"));
          const token = user?.access;
  
          if (!token) {
            throw new Error("Token não encontrado");
          }
  
          const response = await fetch("http://localhost:8000/api/lembrancas/", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${token}`,
              // Não definir 'Content-Type' para multipart/form-data, o navegador define automaticamente
            },
            body: formData,
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro ao adicionar memória:", errorData);
            // Extrair a mensagem específica de erro das tags, se disponível
            throw new Error(
              errorData.tags?.[0] || "Erro ao adicionar memória"
            );
          }
  
          const addedMemory = await response.json();
          console.log("Memória adicionada com sucesso:", addedMemory); // Log para depuração
  
          this.closeModal();
          this.resetForm();
  
          this.$emit("memory-added");
          alert("Memória adicionada com sucesso!");
        } catch (error) {
          console.error("Erro ao adicionar memória:", error);
          alert(error.message);
        }
      },
      resetForm() {
        this.title = "";
        this.description = "";
        this.location = "";
        this.eventDate = null;
        this.selectedTags = [];
        this.image = null;
      },
    },
    mounted() {
      // Opcional: Buscar as tags quando o componente é montado
      // Se preferir buscar apenas quando o modal é aberto, remova esta linha
      // this.fetchTags();
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
    z-index: 1000; /* Assegura que o modal fique acima de outros elementos */
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 500px;
    max-height: 90vh;
    overflow-y: auto; /* Permite rolagem se o conteúdo for muito longo */
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .modal-body {
    margin-top: 10px;
  }
  
  .btn-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }
  </style>
  