<!-- src/components/CardMemory.vue -->
<template>
  <div class="lembrancas-container">
    <!-- Estado de Carregamento -->
    <div v-if="isLoading" class="text-center">
      <p>Carregando lembranças...</p>
    </div>

    <!-- Estado de Erro -->
    <div v-else-if="error" class="text-center">
      <p>Não foi possível carregar as lembranças.</p>
      <button @click="$emit('open-add-memory')" class="btn btn-primary mt-3">
        Adicionar Memória
      </button>
    </div>

    <!-- Estado Sem Memórias -->
    <div v-else-if="lembrancas.length === 0" class="text-center">
      <p>Não há lembranças.</p>
      <button @click="$emit('open-add-memory')" class="btn btn-primary mt-3">
        Adicionar Memória
      </button>
    </div>

    <!-- Lista de Memórias -->
    <div v-else>
      <div v-for="lembranca in lembrancas" :key="lembranca.id" class="card shadow-sm mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h5 class="card-title">{{ lembranca.titulo }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ formatDate(lembranca.data_evento) }}</h6>
            </div>
            <div>
              <edit-memory-modal :memory="lembranca" @memory-edited="fetchLembrancas" />
              <delete-memory-component :memoryId="lembranca.id" @memory-deleted="fetchLembrancas" />
            </div>
          </div>
          <p class="card-text">{{ lembranca.descricao }}</p>
          <p class="card-text"><strong>Local:</strong> {{ lembranca.local }}</p>
          <div v-if="lembranca.imagem" class="image mb-3">
            <img :src="lembranca.imagem" alt="Imagem da lembrança" class="img-fluid rounded" />
          </div>
          <div v-if="lembranca.destaque" class="mb-2">
            <span class="badge bg-warning text-dark">Destaque</span>
          </div>
          <div class="tags">
            <span v-for="tag in lembranca.tagsNames" :key="tag" class="badge bg-primary me-1">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import http from "@/services/http";
import DeleteMemoryComponent from "@/components/DeleteMemoryComponent.vue";
import EditMemoryModal from "@/components/EditMemoryModal.vue";

export default {
  components: {
    DeleteMemoryComponent,
    EditMemoryModal,
  },
  data() {
    return {
      lembrancas: [],
      isLoading: false,
      error: false,
    };
  },
  methods: {
    // Formata a data para exibição
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("pt-BR", options);
    },
    // Busca o nome da tag pelo ID
    fetchTagName(tagId) {
      return http.get(`/tags/${tagId}/`)
        .then(response => response.data.nome)
        .catch(error => {
          console.error(`Erro ao buscar a tag de ID ${tagId}:`, error);
          return `Tag ${tagId}`;
        });
    },
    // Busca todas as lembranças e seus nomes de tags
    async fetchLembrancas() {
      this.isLoading = true;
      this.error = false;
      try {
        const response = await http.get("/lembrancas/");
        const lembrancas = response.data;

        const updatedLembrancas = await Promise.all(
          lembrancas.map(async (lembranca) => {
            const tagsNames = await Promise.all(
              lembranca.tags.map(tagId => this.fetchTagName(tagId))
            );
            return { ...lembranca, tagsNames };
          })
        );

        this.lembrancas = updatedLembrancas;
      } catch (error) {
        console.error("Erro ao buscar lembranças:", error);
        this.error = true;
      } finally {
        this.isLoading = false;
      }
    },
  },
  mounted() {
    this.fetchLembrancas();
  },
};
</script>

<style scoped>
.lembrancas-container {
  padding: 20px;
}
.card {
  border: none;
}
.card-title {
  font-size: 1.25rem;
  color: #007bff;
}
.card-subtitle {
  font-size: 0.9rem;
}
.card-text {
  color: #333;
}
.image img {
  max-height: 200px;
  object-fit: cover;
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
</style>
