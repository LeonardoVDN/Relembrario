<!-- src/components/AddTagComponent.vue -->
<template>
    <div>
      <!-- Botão para abrir o modal de adicionar tag -->
      <button @click="openModal" class="btn btn-secondary mb-3">Adicionar Tag</button>
  
      <!-- Modal de adicionar tag -->
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Adicionar Nova Tag</h5>
            <button @click="closeModal" class="btn-close">&times;</button>
          </div>
  
          <div class="modal-body">
            <form @submit.prevent="submitTag">
              <div class="mb-3">
                <label for="tagName" class="form-label">Nome da Tag</label>
                <input type="text" v-model="tagName" id="tagName" class="form-control" required />
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
        tagName: "",
      };
    },
    methods: {
      openModal() {
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
        this.resetForm();
      },
      async submitTag() {
        try {
          const user = JSON.parse(localStorage.getItem("user"));
          const token = user?.access;
  
          if (!token) {
            throw new Error("Token não encontrado");
          }
  
          const response = await fetch("http://localhost:8000/api/tags/", {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ nome: this.tagName }), // Alterado de 'name' para 'nome'
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro ao adicionar tag:", errorData);
            // Extrair a mensagem específica de erro, se disponível
            const errorMessage = errorData.nome ? errorData.nome[0] : "Erro ao adicionar tag";
            throw new Error(errorMessage);
          }
  
          this.closeModal();
          this.$emit("tag-added");
          alert("Tag adicionada com sucesso!");
        } catch (error) {
          console.error("Erro ao adicionar tag:", error);
          alert(error.message);
        }
      },
      resetForm() {
        this.tagName = "";
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
    width: 400px;
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
  