<template>
  <div class="login-layout">
    <div class="form-section">
      <button class="btn-back" @click="voltarParaHome" :disabled="carregando">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        Voltar
      </button>

      <div class="form-wrapper">
        <div class="brand">
          <span class="med">Med</span> <span class="match">Match</span>
        </div>
        
        <div class="welcome-text">
          <h1>Credenciamento Médico</h1>
        </div>

        <form @submit.prevent="cadastrarMedico" class="auth-form">
          <div class="form-grid">
            <div class="form-group">
              <label>Nome do Médico</label>
              <input type="text" v-model="form.nome" placeholder="Nome Completo" required />
            </div>
            
            <div class="form-group">
              <label>Especialidade</label>
              <input type="text" v-model="form.especialidade" placeholder="Especialidade" required />
            </div>

            <div class="form-group">
              <label>CRM</label>
              <input type="text" v-model="form.crm" placeholder="123456" required />
            </div>
            
            <div class="form-group">
              <label>E-mail Corporativo</label>
              <input type="email" v-model="form.email" placeholder="seu-email@gmail.com" required />
            </div>

            <div class="form-group">
              <label>Telefone</label>
              <input type="text" v-model="form.telefone" placeholder="(99)99999-9999" required />
            </div>
            
            <div class="form-group empty-space"></div>

            <div class="form-group full-width">
              <label>Definir Senha de Acesso</label>
              <input type="password" v-model="form.senha" placeholder="••••••••" required />
            </div>
          </div>

          <button type="submit" class="btn-submit doctor-btn" :disabled="carregando">
            {{ carregando ? 'Salvando dados...' : 'Solicitar Credenciamento' }}
          </button>
        </form>
      </div>
    </div>

    <div class="banner-section">
      <div class="banner-content">
        <div class="icon-box doctor-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
          </svg>
        </div>
        
        <h2>Conecte-se aos pacientes que precisam de você.</h2>
        <p>
          Aumente a eficiência da sua clínica recebendo pacientes pré-triados pela nossa IA.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// Importação do Supabase (Ajuste o caminho se necessário)
import { supabase } from '../supabase.js';

const router = useRouter();
const carregando = ref(false);

// Objeto reativo para guardar os dados do formulário
const form = ref({
  nome: '',
  especialidade: '',
  crm: '',
  email: '',
  telefone: '',
  senha: ''
});

const voltarParaHome = () => {
  router.push('/');
};

const cadastrarMedico = async () => {
  carregando.value = true;

  try {
    // 1. Inserir dados na tabela genérica "Usuario"
    const { data: usuarioData, error: usuarioError } = await supabase
      .from('Usuario')
      .insert([
        {
          nome: form.value.nome,
          email: form.value.email,
          senha_hash: form.value.senha, 
          telefone: form.value.telefone
        }
      ])
      .select()
      .single(); // Retorna a linha que acabou de ser criada

    if (usuarioError) throw usuarioError;

    // 2. Com o ID do Usuario criado, inserir na tabela específica "Medico"
    const { error: medicoError } = await supabase
      .from('Medico') 
      .insert([
        {
          usuario_id: usuarioData.id, // Chave estrangeira ligando ao Usuario
          crm: form.value.crm,
          especialidade: form.value.especialidade
        }
      ]);

    if (medicoError) throw medicoError;

    // 3. Sucesso! Definir as variáveis locais e redirecionar
    console.log("Cadastro de Médico realizado com sucesso!");
    
    // 👇 A MÁGICA ACONTECE AQUI: Salvamos o ID e a Role para a Dashboard usar
    localStorage.setItem('userId', usuarioData.id);
    localStorage.setItem('userRole', 'doctor');
    
    router.push('/dashboard-medico');

  } catch (error: any) {
    console.error('Erro detalhado:', error);
    alert('Não foi possível realizar o cadastro: ' + error.message);
  } finally {
    carregando.value = false;
  }
};
</script>

<style scoped>
/* RESET E LAYOUT PRINCIPAL */
.login-layout { display: flex; min-height: 100vh; font-family: 'Inter', sans-serif; }

/* LADO ESQUERDO: FORMULÁRIO */
.form-section { flex: 1; display: flex; flex-direction: column; background-color: #ffffff; padding: 40px; position: relative; }

.btn-back { background: transparent; border: none; color: #4a5568; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 0.95rem; transition: color 0.2s, transform 0.2s; padding: 0; width: fit-content; margin-bottom: 20px;}
.btn-back:hover { color: #111827; transform: translateX(-4px); }
.btn-back:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.form-wrapper { max-width: 550px; width: 100%; margin: auto; }

.brand { font-size: 1.6rem; font-weight: 800; margin-bottom: 40px; }
.brand .med { color: #008767; }
.brand .match { color: #1a202c; }

.welcome-text h1 { font-size: 1.8rem; color: #1a202c; margin-bottom: 30px; }

/* GRID DO FORMULÁRIO */
.auth-form { display: flex; flex-direction: column; gap: 24px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 16px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.full-width { grid-column: span 2; }
.empty-space { display: block; }

label { font-size: 0.85rem; font-weight: 700; color: #1a202c; }
input { padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.95rem; outline: none; transition: border-color 0.2s; color: #1a202c; }
input::placeholder { color: #a0aec0; }
input:focus { border-color: #111827; box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.1); }

.btn-submit { color: white; border: none; padding: 16px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: background 0.2s; margin-top: 8px; width: 100%; }
.doctor-btn { background: #111827; }
.doctor-btn:hover { background: #1f2937; }
.doctor-btn:disabled { background: #4b5563; cursor: not-allowed; }

/* LADO DIREITO: BANNER ESCURO */
.banner-section { flex: 1; background-color: #111827; display: flex; flex-direction: column; justify-content: center; padding: 80px; position: relative; border-left: 1px solid #1f2937; }
.banner-content { position: relative; z-index: 2; max-width: 450px; }

.icon-box { width: 56px; height: 56px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; }
.doctor-icon { background-color: #ffffff; color: #111827; }

.banner-content h2 { color: #ffffff; font-size: 2.4rem; line-height: 1.2; margin-bottom: 20px; font-weight: 700; }
.banner-content p { color: #9ca3af; font-size: 1.1rem; line-height: 1.6; }

@media (max-width: 900px) {
  .banner-section { display: none; }
  .form-grid { grid-template-columns: 1fr; }
  .full-width { grid-column: span 1; }
  .empty-space { display: none; }
}
</style>