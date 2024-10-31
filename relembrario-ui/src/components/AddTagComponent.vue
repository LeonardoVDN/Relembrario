<!-- src/components/AddTagComponent.vue -->
<template>
  <div>
    <!-- Botão para abrir o modal de gerenciamento de tags -->
    <button @click="openModal" class="btn btn-secondary mb-3">Gerenciar Tags</button>

    <!-- Modal de Gerenciamento de Tags -->
    <div
      v-if="showModal"
      class="modal fade show"
      tabindex="-1"
      role="dialog"
      aria-labelledby="manageTagsModalLabel"
      aria-hidden="true"
      style="display: block;"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="manageTagsModalLabel">Gerenciar Tags</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <div class="modal-body">
            <!-- Formulário para adicionar nova tag -->
            <form @submit.prevent="submitTag">
              <div class="mb-3">
                <label for="tagName" class="form-label">Nome da Tag</label>
                <input
                  type="text"
                  v-model="tagName"
                  id="tagName"
                  class="form-control"
                  required
                />
              </div>
              <button type="submit" class="btn btn-success">Adicionar Tag</button>
            </form>

            <!-- Divisor -->
            <hr />

            <!-- Lista de tags existentes -->
            <h5>Tags Existentes</h5>
            <ul class="list-group">
              <li
                v-for="tag in tags"
                :key="tag.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div v-if="editingTagId !== tag.id">
                  {{ tag.nome }}
                </div>
                <div v-else>
                  <input
                    type="text"
                    v-model="editingTagName"
                    class="form-control"
                  />
                </div>

                <div>
                  <button
                    v-if="editingTagId !== tag.id"
                    @click="startEditing(tag)"
                    class="btn btn-primary btn-sm me-2"
                  >
                    Editar
                  </button>
                  <button
                    v-else
                    @click="saveEdit(tag.id)"
                    class="btn btn-success btn-sm me-2"
                  >
                    Salvar
                  </button>
                  <button
                    v-if="editingTagId === tag.id"
                    @click="cancelEdit"
                    class="btn btn-secondary btn-sm me-2"
                  >
                    Cancelar
                  </button>
                  <button
                    @click="openDeleteConfirmModal(tag.id)"
                    class="btn btn-danger btn-sm"
                  >
                    Excluir
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay do Modal de Gerenciamento -->
    <div
      v-if="showModal"
      class="modal-backdrop fade show"
    ></div>

    <!-- Modal de Confirmação de Exclusão -->
    <div
      v-if="showDeleteConfirmModal"
      class="modal fade show"
      tabindex="-1"
      role="dialog"
      aria-labelledby="confirmDeleteTagModalLabel"
      aria-hidden="true"
      style="display: block;"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmDeleteTagModalLabel">Confirmar Exclusão</h5>
            <button type="button" class="close" @click="closeDeleteConfirmModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <div class="modal-body">
            Tem certeza que deseja excluir esta tag?
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteConfirmModal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="confirmDelete">Excluir</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Overlay do Modal de Confirmação de Exclusão -->
    <div
      v-if="showDeleteConfirmModal"
      class="modal-backdrop fade show"
    ></div>
  </div>
</template>

<script>
import http from "@/services/http"; // Assegure-se de que o caminho está correto

export default {
  name: "AddTagComponent",
  data() {
    return {
      showModal: false,
      tagName: "",
      tags: [],
      editingTagId: null,
      editingTagName: "",
      showDeleteConfirmModal: false,
      tagIdToDelete: null,
    };
  },
  methods: {
    // Abre o modal de gerenciamento de tags
    openModal() {
      this.showModal = true;
      this.fetchTags(); // Buscar as tags quando o modal for aberto
    },
    // Fecha o modal de gerenciamento de tags
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
    // Abre o modal de confirmação de exclusão
    openDeleteConfirmModal(tagId) {
      this.tagIdToDelete = tagId;
      this.showDeleteConfirmModal = true;
    },
    // Fecha o modal de confirmação de exclusão
    closeDeleteConfirmModal() {
      this.showDeleteConfirmModal = false;
      this.tagIdToDelete = null;
    },
    // Busca as tags existentes
    async fetchTags() {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const token = user?.access;

        if (!token) {
          throw new Error("Token não encontrado");
        }

        const response = await fetch("http://localhost:8000/api/tags/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Erro ao buscar tags:", errorData);
          throw new Error("Erro ao buscar tags");
        }

        const data = await response.json();
        this.tags = data;
      } catch (error) {
        console.error("Erro ao buscar tags:", error);
        this.$emit("tag-fetch-error", error.message || "Erro ao buscar tags.");
      }
    },
    // Submete o formulário para adicionar uma nova tag
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
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ nome: this.tagName }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Erro ao adicionar tag:", errorData);
          const errorMessage = errorData.nome
            ? errorData.nome[0]
            : "Erro ao adicionar tag";
          throw new Error(errorMessage);
        }

        this.resetForm();
        await this.fetchTags(); // Atualizar a lista de tags após adicionar
        this.$emit("tag-added", "Tag adicionada com sucesso!");
      } catch (error) {
        console.error("Erro ao adicionar tag:", error);
        this.$emit("tag-add-error", error.message || "Erro ao adicionar a tag.");
      }
    },
    // Inicia a edição de uma tag
    startEditing(tag) {
      this.editingTagId = tag.id;
      this.editingTagName = tag.nome;
    },
    // Cancela a edição de uma tag
    cancelEdit() {
      this.editingTagId = null;
      this.editingTagName = "";
    },
    // Salva a edição de uma tag
    async saveEdit(tagId) {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const token = user?.access;

        if (!token) {
          throw new Error("Token não encontrado");
        }

        const response = await fetch(`http://localhost:8000/api/tags/${tagId}/`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ nome: this.editingTagName }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Erro ao editar tag:", errorData);
          const errorMessage = errorData.nome
            ? errorData.nome[0]
            : "Erro ao editar tag";
          throw new Error(errorMessage);
        }

        this.editingTagId = null;
        this.editingTagName = "";
        await this.fetchTags(); // Atualizar a lista após edição
        this.$emit("tag-edit-success", "Tag atualizada com sucesso!");
      } catch (error) {
        console.error("Erro ao editar tag:", error);
        this.$emit("tag-edit-error", error.message || "Erro ao editar a tag.");
      }
    },
    // Confirma a exclusão de uma tag
    async confirmDelete() {
      if (!this.tagIdToDelete) return;

      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const token = user?.access;

        if (!token) {
          throw new Error("Token não encontrado");
        }

        const response = await fetch(`http://localhost:8000/api/tags/${this.tagIdToDelete}/`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Erro ao excluir tag:", errorData);
          throw new Error(errorData.detail || "Erro ao excluir tag");
        }

        await this.fetchTags(); // Atualizar a lista após exclusão
        this.$emit("tag-delete-success", "Tag excluída com sucesso!");
      } catch (error) {
        console.error("Erro ao excluir tag:", error);
        this.$emit("tag-delete-error", error.message || "Erro ao excluir a tag.");
      } finally {
        this.closeDeleteConfirmModal();
      }
    },
    // Reseta o formulário
    resetForm() {
      this.tagName = "";
      this.editingTagId = null;
      this.editingTagName = "";
    },
  },
};
</script>

<style scoped>
/* Estilos para os Modais */
.modal {
  transition: opacity 0.15s linear;
}

.modal.show {
  display: block;
  opacity: 1;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}

.modal-dialog {
  z-index: 1050;
}

.modal-content {
  color: black;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-group-item input {
  width: 200px;
  margin-right: 10px;
}
</style>
