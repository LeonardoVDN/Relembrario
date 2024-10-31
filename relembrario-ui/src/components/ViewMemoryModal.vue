<!-- src/components/ViewMemoryModal.vue -->
<template>
    <div>
      <!-- Botão de Visualizar -->
      <button @click="openModal" class="btn btn-info me-2">Visualizar</button>
  
      <!-- Modal -->
      <div
        class="modal fade"
        :id="'viewMemoryModal' + memory.id"
        tabindex="-1"
        aria-labelledby="viewMemoryModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <!-- Cabeçalho do Modal -->
            <div class="modal-header">
              <h5 class="modal-title" id="viewMemoryModalLabel">{{ memory.titulo }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <!-- Corpo do Modal -->
            <div class="modal-body">
              <!-- Conteúdo completo da memória -->
              <p><strong>Data:</strong> {{ formatDate(memory.data_evento) }}</p>
              <p><strong>Local:</strong> {{ memory.local }}</p>
              <p>{{ memory.descricao }}</p>
              <!-- Imagem -->
              <div v-if="memory.imagem" class="image mb-3">
                <img
                  :src="memory.imagem"
                  alt="Imagem da lembrança"
                  class="img-fluid rounded"
                />
              </div>
              <!-- Tags -->
              <div class="tags mb-3">
                <span
                  v-for="tag in memory.tagsNames"
                  :key="tag"
                  class="badge bg-primary me-1"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
            <!-- Rodapé do Modal -->
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  // Importa o Modal do Bootstrap
  import { Modal } from 'bootstrap';
  
  export default {
    name: "ViewMemoryModal",
    props: {
      memory: {
        type: Object,
        required: true,
      },
    },
    methods: {
      openModal() {
        const modalId = `viewMemoryModal${this.memory.id}`;
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
          const modal = new Modal(modalElement);
          modal.show();
        } else {
          console.error(`Elemento do modal com id ${modalId} não encontrado.`);
        }
      },
      formatDate(date) {
        const options = { year: "numeric", month: "long", day: "numeric" };
        return new Date(date).toLocaleDateString("pt-BR", options);
      },
    },
  };
  </script>
  
  <style scoped>
  .image img {
    width: 100%;
    object-fit: cover;
    border-radius: 8px;
  }
  </style>
  