<!-- src/components/CardMemory.vue -->
<template>
  <div class="lembrancas-container">
    <div v-if="lembrancas.length === 0" class="text-center">
      <p>Carregando lembranças...</p>
    </div>
    <div v-else>
      <div v-for="lembranca in lembrancas" :key="lembranca.id" class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="card-title">{{ lembranca.titulo }}</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ formatDate(lembranca.data_evento) }}</h6>
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
import http from "../services/http";

export default {
  data() {
    return {
      lembrancas: [],
    };
  },
  methods: {
    // Método para formatar a data
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("pt-BR", options);
    },
    // Método para buscar o nome das tags
    fetchTagName(tagId) {
      return http.get(`/tags/${tagId}/`)
        .then((response) => response.data.nome) // Supondo que a tag tenha o campo "nome"
        .catch((error) => {
          console.error(`Erro ao buscar a tag de ID ${tagId}:`, error);
          return `Tag ${tagId}`; // Retorna o ID se houver um erro
        });
    },
    // Método para buscar todas as lembranças e suas tags
    async fetchLembrancas() {
      try {
        const response = await http.get("/lembrancas/");
        const lembrancas = response.data;

        // Para cada lembrança, busca os nomes das tags
        const updatedLembrancas = await Promise.all(
          lembrancas.map(async (lembranca) => {
            const tagsNames = await Promise.all(
              lembranca.tags.map((tagId) => this.fetchTagName(tagId))
            );
            return {
              ...lembranca,
              tagsNames, // Adiciona os nomes das tags no lugar dos IDs
            };
          })
        );

        this.lembrancas = updatedLembrancas;
      } catch (error) {
        console.error("Erro ao buscar lembranças:", error);
      }
    },
  },
  mounted() {
    // Faz a requisição para buscar as lembranças ao montar o componente
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
</style>
