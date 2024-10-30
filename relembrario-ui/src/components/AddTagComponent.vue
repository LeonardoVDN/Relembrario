<!-- src/components/AddTagComponent.vue -->
<template>
  <div>
    <!-- Botão para abrir o modal de gerenciamento de tags -->
    <button @click="openModal" class="btn btn-secondary mb-3">Gerenciar Tags</button>

    <!-- Modal de gerenciamento de tags -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Gerenciar Tags</h5>
          <button @click="closeModal" class="btn-close">&times;</button>
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
                  @click="confirmDelete(tag.id)"
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
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
      tagName: "",
      tags: [],
      editingTagId: null,
      editingTagName: "",
    };
  },
  methods: {
    openModal() {
      this.showModal = true;
      this.fetchTags(); // Buscar as tags quando o modal for aberto
    },
    closeModal() {
      this.showModal = false;
      this.resetForm();
    },
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
        alert(error.message);
      }
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
        this.$emit("tag-added");
        alert("Tag adicionada com sucesso!");
      } catch (error) {
        console.error("Erro ao adicionar tag:", error);
        alert(error.message);
      }
    },
    async confirmDelete(tagId) {
      const isConfirmed = confirm("Tem certeza que deseja excluir esta tag?");
      if (isConfirmed) {
        await this.deleteTag(tagId);
      }
    },
    async deleteTag(tagId) {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const token = user?.access;

        if (!token) {
          throw new Error("Token não encontrado");
        }

        const response = await fetch(
          `http://localhost:8000/api/tags/${tagId}/`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Erro ao excluir tag:", errorData);
          throw new Error("Erro ao excluir tag");
        }

        await this.fetchTags(); // Atualizar a lista após exclusão
        alert("Tag excluída com sucesso!");
      } catch (error) {
        console.error("Erro ao excluir tag:", error);
        alert(error.message);
      }
    },
    startEditing(tag) {
      this.editingTagId = tag.id;
      this.editingTagName = tag.nome;
    },
    cancelEdit() {
      this.editingTagId = null;
      this.editingTagName = "";
    },
    async saveEdit(tagId) {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const token = user?.access;

        if (!token) {
          throw new Error("Token não encontrado");
        }

        const response = await fetch(
          `http://localhost:8000/api/tags/${tagId}/`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ nome: this.editingTagName }),
          }
        );

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
        alert("Tag atualizada com sucesso!");
      } catch (error) {
        console.error("Erro ao editar tag:", error);
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
  color: black;
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
