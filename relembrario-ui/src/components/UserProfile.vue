<!-- src/components/UserProfile.vue -->
<template>
    <div class="user-profile">
      <h2>Meu Perfil</h2>
      <form @submit.prevent="updateProfile">
        <!-- Campos do Perfil -->
        <div class="mb-3">
          <label for="username" class="form-label">Nome de Usuário</label>
          <input type="text" v-model="user.username" id="username" class="form-control" disabled />
        </div>
  
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" v-model="user.email" id="email" class="form-control" />
        </div>
  
        <div class="mb-3" v-if="user.profile">
          <label for="display_name" class="form-label">Nome Visível</label>
          <input
            type="text"
            v-model="user.profile.display_name"
            id="display_name"
            class="form-control"
          />
        </div>
  
        <div class="mb-3">
          <label for="profile_picture" class="form-label">Foto de Perfil</label>
          <input type="file" @change="onFileChange" id="profile_picture" class="form-control" />
          <div v-if="profilePictureUrl" class="mt-2">
            <img :src="profilePictureUrl" alt="Foto de Perfil" class="img-thumbnail" width="150" />
          </div>
        </div>
  
        <!-- Alteração de Senha -->
        <h3>Alterar Senha</h3>
        <div class="mb-3">
          <label for="current_password" class="form-label">Senha Atual</label>
          <input
            type="password"
            v-model="passwords.current_password"
            id="current_password"
            class="form-control"
          />
        </div>
  
        <div class="mb-3">
          <label for="new_password" class="form-label">Nova Senha</label>
          <input
            type="password"
            v-model="passwords.new_password"
            id="new_password"
            class="form-control"
          />
        </div>
  
        <div class="mb-3">
          <label for="confirm_new_password" class="form-label">Confirme a Nova Senha</label>
          <input
            type="password"
            v-model="passwords.confirm_new_password"
            id="confirm_new_password"
            class="form-control"
          />
        </div>
  
        <button type="submit" class="btn btn-primary">Salvar Alterações</button>
      </form>
    </div>
  </template>
  
  <script>
  import http from "@/services/http";
  
  export default {
    data() {
      return {
        user: {
          username: "",
          email: "",
          profile: {
            display_name: "",
            profile_picture: null,
          },
        },
        passwords: {
          current_password: "",
          new_password: "",
          confirm_new_password: "",
        },
        selectedFile: null,
        profilePictureUrl: null,
      };
    },
    methods: {
      async fetchUserProfile() {
        try {
          const response = await http.get("/profile/");
          console.log(response.data); // Verifique os dados retornados
          this.user = response.data;
  
          // Se o profile não existir, inicialize-o
          if (!this.user.profile) {
            this.user.profile = {
              display_name: "",
              profile_picture: null,
            };
          }
  
          if (this.user.profile.profile_picture) {
            this.profilePictureUrl = this.user.profile.profile_picture;
          }
        } catch (error) {
          console.error("Erro ao buscar perfil do usuário:", error);
          alert("Não foi possível carregar o perfil. Tente novamente mais tarde.");
        }
      },
      onFileChange(event) {
        this.selectedFile = event.target.files[0];
        this.profilePictureUrl = URL.createObjectURL(this.selectedFile);
      },
      async updateProfile() {
        if (this.passwords.new_password !== this.passwords.confirm_new_password) {
          alert("As senhas não correspondem.");
          return;
        }
  
        const formData = new FormData();
        formData.append("email", this.user.email);
        formData.append("profile.display_name", this.user.profile.display_name);
  
        if (this.selectedFile) {
          formData.append("profile.profile_picture", this.selectedFile);
        }
  
        if (this.passwords.current_password && this.passwords.new_password) {
          formData.append("password", this.passwords.current_password);
          formData.append("new_password", this.passwords.new_password);
        }
  
        try {
          await http.put("/profile/", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          });
          alert("Perfil atualizado com sucesso!");
          // Limpar campos de senha
          this.passwords = {
            current_password: "",
            new_password: "",
            confirm_new_password: "",
          };
          await this.fetchUserProfile();
          // Emitir evento para atualizar a sidebar
          this.$emit("profile-updated");
        } catch (error) {
          console.error("Erro ao atualizar perfil:", error);
          alert("Não foi possível atualizar o perfil. Verifique suas informações e tente novamente.");
        }
      },
    },
    mounted() {
      this.fetchUserProfile();
    },
  };
  </script>
  
  <style scoped>
  .user-profile {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>
  