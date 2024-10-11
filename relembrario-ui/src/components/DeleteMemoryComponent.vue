<!-- src/components/DeleteMemoryComponent.vue -->
<template>
    <button @click="confirmDelete" class="btn btn-danger btn-sm ms-2">
      Excluir
    </button>
  </template>
  
  <script>
  import http from "@/services/http"; // Assegure-se de que o caminho está correto
  
  export default {
    props: {
      memoryId: {
        type: Number,
        required: true,
      },
    },
    methods: {
      async confirmDelete() {
        const isConfirmed = confirm("Tem certeza que deseja excluir esta memória?");
        if (isConfirmed) {
          try {
            await this.deleteMemory();
            this.$emit("memory-deleted", this.memoryId);
            alert("Memória excluída com sucesso!");
          } catch (error) {
            console.error("Erro ao excluir memória:", error);
            alert("Não foi possível excluir a memória. Tente novamente.");
          }
        }
      },
      async deleteMemory() {
        await http.delete(`/lembrancas/${this.memoryId}/`);
      },
    },
  };
  </script>
  
  <style scoped>
  .btn-danger {
    /* Personalize o botão conforme necessário */
  }
  </style>
  