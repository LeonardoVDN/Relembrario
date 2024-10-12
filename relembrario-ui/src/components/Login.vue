<!-- src/components/Login.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card shadow-sm">
          <div class="bgColor card-body">
            <h2 class="card-title text-center mb-4">Entrar na sua conta</h2>
            <form @submit.prevent="handleLogin" novalidate>
              <!-- Nome de usuário -->
              <div class="mb-3">
                <label for="username" class="form-label">Nome de usuário</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-person-fill"></i>
                  </span>
                  <input
                    type="text"
                    id="username"
                    v-model="user.username"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <!-- Senha -->
              <div class="mb-4">
                <label for="password" class="form-label">Senha</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-lock-fill"></i>
                  </span>
                  <input
                    type="password"
                    id="password"
                    v-model="user.password"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <!-- Botão de Login -->
              <button type="submit" class="btn btn-primary w-100">Entrar</button>

              <!-- Mensagem de feedback -->
              <div v-if="message" class="alert mt-3" :class="alertClass">
                {{ message }}
              </div>
            </form>
            <p class="text-center mt-3">
              Não tem uma conta?
              <router-link to="/register">Registre-se aqui</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from '../services/authService';

export default {
  data() {
    return {
      user: {
        username: '',
        password: ''
      },
      message: '',
      alertClass: 'alert-danger'
    };
  },
  methods: {
    async handleLogin() {
      this.message = ''; // Limpa mensagens anteriores
      try {
        await AuthService.login(this.user);
        this.$router.push('/');
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.message = 'Credenciais inválidas.';
        } else {
          this.message = 'Ocorreu um erro ao tentar fazer login.';
        }
      }
    }
  }
};
</script>

<style scoped>
.bgColor {
  background-color: #bddbfa;
  border-radius: 10px;
}
.container {
  max-width: 600px;
}

.card {
  border: none;
}

.card-title {
  font-weight: bold;
}

.input-group-text {
  background-color: #f0f0f0;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.alert {
  font-size: 0.9rem;
}

::placeholder {
  color: #ccc;
}
</style>
