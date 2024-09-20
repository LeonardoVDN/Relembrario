<template>
    <div class="lembrancas-container">
      <h1>Lembranças</h1>
      <div v-if="lembrancas.length === 0" class="no-data">
        Carregando lembranças...
      </div>
      <div v-else>
        <div v-for="lembranca in lembrancas" :key="lembranca.id" class="lembranca-card">
          <h2>{{ lembranca.titulo }}</h2>
          <p>{{ lembranca.descricao }}</p>
          <p><strong>Data do evento:</strong> {{ formatDate(lembranca.data_evento) }}</p>
          <p><strong>Local:</strong> {{ lembranca.local }}</p>
          <div v-if="lembranca.imagem" class="image">
            <img :src="lembranca.imagem" alt="Imagem da lembrança" />
          </div>
          <p v-if="lembranca.destaque" class="destaque">Destaque</p>
          <div class="tags">
            <!-- Exibe o nome da tag ao invés do ID -->
            <span v-for="tag in lembranca.tagsNames" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
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
        return new Date(date).toLocaleDateString(undefined, options);
      },
      // Método para buscar o nome das tags
      fetchTagName(tagId) {
        return axios.get(`http://127.0.0.1:8000/tags/${tagId}/`)
          .then(response => response.data.nome) // Supondo que a tag tenha o campo "nome"
          .catch(error => {
            console.error(`Erro ao buscar a tag de ID ${tagId}:`, error);
            return `Tag ${tagId}`; // Retorna o ID se houver um erro
          });
      },
      // Método para buscar todas as lembranças e suas tags
      async fetchLembrancas() {
        try {
          const response = await axios.get("http://127.0.0.1:8000/lembrancas/");
          const lembrancas = response.data;
  
          // Para cada lembrança, busca os nomes das tags
          const updatedLembrancas = await Promise.all(lembrancas.map(async lembranca => {
            const tagsNames = await Promise.all(
              lembranca.tags.map(tagId => this.fetchTagName(tagId))
            );
            return {
              ...lembranca,
              tagsNames, // Adiciona os nomes das tags no lugar dos IDs
            };
          }));
  
          this.lembrancas = updatedLembrancas;
        } catch (error) {
          console.error("Erro ao buscar lembranças:", error);
        }
      }
    },
    mounted() {
      // Faz a requisição para buscar as lembranças ao montar o componente
      this.fetchLembrancas();
    },
  };
  </script>
  
  <style scoped>
  /* Estilo do componente geral */
  .lembrancas-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
    color: #007bff;
  }
  
  .no-data {
    text-align: center;
    font-size: 18px;
    color: #888;
  }
  
  .lembranca-card {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .lembranca-card h2 {
    color: #333;
    margin-bottom: 10px;
  }
  
  .lembranca-card p {
    color: #666;
    margin-bottom: 10px;
  }
  
  .image img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    margin-top: 10px;
  }
  
  .destaque {
    color: #ff0000;
    font-weight: bold;
  }
  
  .tags {
    margin-top: 10px;
  }
  
  .tag {
    background-color: #007bff;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    margin-right: 5px;
  }
  </style>
  