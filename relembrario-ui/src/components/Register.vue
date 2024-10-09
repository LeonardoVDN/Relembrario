<!-- src/components/Register.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card shadow-sm">
          <div class="bgColor card-body">
            <h2 class="card-title text-center mb-4">Crie sua conta</h2>
            <form @submit.prevent="handleRegister" novalidate>
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

              <!-- Email -->
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-envelope-fill"></i>
                  </span>
                  <input
                    type="email"
                    id="email"
                    v-model="user.email"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <!-- Senha -->
              <div class="mb-3">
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

              <!-- Confirmação de Senha -->
              <div class="mb-3">
                <label for="password2" class="form-label">Confirme a Senha</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="bi bi-lock-fill"></i>
                  </span>
                  <input
                    type="password"
                    id="password2"
                    v-model="user.password2"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <!-- Nome e Sobrenome -->
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="first_name" class="form-label">Nome</label>
                  <input
                    type="text"
                    id="first_name"
                    v-model="user.first_name"
                    class="form-control"
                  />
                </div>
                <div class="col-md-6 mb-3">
                  <label for="last_name" class="form-label">Sobrenome</label>
                  <input
                    type="text"
                    id="last_name"
                    v-model="user.last_name"
                    class="form-control"
                  />
                </div>
              </div>

              <!-- Botão de Registro -->
              <button type="submit" class="btn btn-primary w-100">Registrar</button>

              <!-- Mensagem de feedback -->
              <div v-if="message" class="alert mt-3" :class="{'alert-success': success, 'alert-danger': !success}">
                {{ message }}
              </div>
            </form>
            <p class="text-center mt-3">
              Já tem uma conta?
              <router-link to="/login">Entre aqui</router-link>
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
        email: '',
        password: '',
        password2: '',
        first_name: '',
        last_name: ''
      },
      message: '',
      success: false
    };
  },
  methods: {
    handleRegister() {
      // Validação das senhas
      if (this.user.password !== this.user.password2) {
        this.message = 'As senhas não coincidem.';
        this.success = false;
        return;
      }

      // Chamada ao serviço de registro
      AuthService.register(this.user)
        .then(() => {
          this.message = 'Registrado com sucesso!';
          this.success = true;
          // Redireciona para a página de login após alguns segundos
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000);
        })
        .catch(error => {
          // Trata erros de registro
          if (error.response && error.response.data) {
            this.message = this.parseErrorMessages(error.response.data);
          } else {
            this.message = 'Ocorreu um erro no registro.';
          }
          this.success = false;
        });
    },
    parseErrorMessages(errors) {
      let messages = '';
      for (let key in errors) {
        messages += `${errors[key]} `;
      }
      return messages.trim();
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
