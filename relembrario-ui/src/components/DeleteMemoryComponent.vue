<!-- src/components/DeleteMemoryComponent.vue -->
<template>
  <div>
    <!-- Botão de Excluir -->
    <button @click="openConfirmModal" class="btn btn-danger btn-sm ms-2">
      Excluir
    </button>

    <!-- Modal de Confirmação -->
    <div
      class="modal fade"
      tabindex="-1"
      :class="{ show: showConfirmModal }"
      :style="{ display: showConfirmModal ? 'block' : 'none' }"
      aria-labelledby="confirmDeleteModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmDeleteModalLabel">Confirmar Exclusão</h5>
            <button type="button" class="btn-close" @click="closeConfirmModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Tem certeza que deseja excluir esta memória?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeConfirmModal">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="confirmDelete">Excluir</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Overlay do Modal -->
    <div
      v-if="showConfirmModal"
      class="modal-backdrop fade show"
    ></div>
  </div>
</template>

<script>
import http from "@/services/http"; // Assegure-se de que o caminho está correto

export default {
  name: "DeleteMemoryComponent",
  props: {
    memoryId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      showConfirmModal: false,
    };
  },
  methods: {
    openConfirmModal() {
      this.showConfirmModal = true;
    },
    closeConfirmModal() {
      this.showConfirmModal = false;
    },
    async confirmDelete() {
      try {
        await this.deleteMemory();
        this.$emit("memory-deleted", this.memoryId);
        this.$emit("memory-delete-success", "Memória excluída com sucesso!");
      } catch (error) {
        console.error("Erro ao excluir memória:", error);
        this.$emit("memory-delete-error", "Não foi possível excluir a memória. Tente novamente.");
      } finally {
        this.closeConfirmModal();
      }
    },
    async deleteMemory() {
      await http.delete(`/lembrancas/${this.memoryId}/`);
    },
  },
};
</script>

<style scoped>
/* Estilos para o Modal */
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
</style>
