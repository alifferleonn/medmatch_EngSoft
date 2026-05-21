<template>
  <div class="login-layout">
    <!-- LADO ESQUERDO: Formulário -->
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
          <h1>Criar Perfil de Paciente</h1>
        </div>

        <form @submit.prevent="cadastrarPaciente" class="auth-form">
          <div class="form-grid">
            <div class="form-group">
              <label>Nome Completo</label>
              <input type="text" v-model="form.nome" placeholder="Nome Completo" required />
            </div>
            
            <div class="form-group">
              <label>CPF</label>
              <input type="text" v-model="form.cpf" placeholder="123.456.789-00" required />
            </div>

            <div class="form-group">
              <label>E-mail</label>
              <input type="email" v-model="form.email" placeholder="seu-email@gmail.com" required />
            </div>
            
            <div class="form-group">
              <label>Senha</label>
              <input type="password" v-model="form.senha" placeholder="••••••••" required />
            </div>

            <div class="form-group">
              <label>Telefone</label>
              <input type="text" v-model="form.telefone" placeholder="(99)99999-9999" required />
            </div>
            
            <div class="form-group">
              <label>Data de Nascimento</label>
              <!-- Alterado para type="date" para facilitar o formato pro banco de dados (YYYY-MM-DD) -->
              <input type="date" v-model="form.data_nascimento" required />
            </div>

            <div class="form-group full-width">
              <label>Possui Convênio Médico?</label>
              <input type="text" v-model="form.convenio" placeholder="Particular (Sem convênio)" />
            </div>
          </div>

          <button type="submit" class="btn-submit patient-btn" :disabled="carregando">
            {{ carregando ? 'Salvando dados...' : 'Finalizar Cadastro' }}
          </button>
        </form>
      </div>
    </div>

    <!-- LADO DIREITO: Banner Escuro -->
    <div class="banner-section">
      <div class="banner-content">
        <div class="icon-box patient-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        
        <h2>Cuidado médico inteligente e sem burocracia.</h2>
        <p>
          O MedMatch encontra o especialista certo para o seu sintoma através de inteligência artificial.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// Importação do Supabase (Ajuste o camnho se o seu arquivo estiver em outro lugar)
import { supabase } from '../supabase.js'; 

const router = useRouter();
const carregando = ref(false);

// Objeto reativo para guardar os dados do formulário
const form = ref({
  nome: '',
  cpf: '',
  email: '',
  senha: '',
  telefone: '',
  data_nascimento: '',
  convenio: '' // Não está no diagrama, mas mantive na interface
});

const voltarParaHome = () => {
  router.push('/');
};

const cadastrarPaciente = async () => {
  carregando.value = true;

  try {
    // 1. Inserir dados na tabela Usuario
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

    // 2. Com o ID do Usuario criado, inserir na tabela Paciente
    const { error: pacienteError } = await supabase
      .from('Paciente')
      .insert([
        {
          usuario_id: usuarioData.id, // Chave estrangeira do ERD
          cpf: form.value.cpf,
          data_nascimento: form.value.data_nascimento
        }
      ]);

    if (pacienteError) throw pacienteError;

    // 3. Sucesso! Limpar formulário (opcional) e ir para o chat
    console.log("Cadastro Leonntech realizado com sucesso!");
    router.push('/chat');

  } catch (error: any) {
    console.error('Erro detalhado:', error);
    alert('Não foi possível realizar o cadastro: ' + error.message);
  } finally {
    carregando.value = false;
  }
};
</script>

<style scoped>
/* TODO O SEU CSS ANTERIOR FICA AQUI - Exatamente como estava */
.login-layout { display: flex; min-height: 100vh; font-family: 'Inter', sans-serif; }
.form-section { flex: 1; display: flex; flex-direction: column; background-color: #ffffff; padding: 40px; position: relative; }
.btn-back { background: transparent; border: none; color: #4a5568; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 0.95rem; transition: color 0.2s, transform 0.2s; padding: 0; width: fit-content; margin-bottom: 20px;}
.btn-back:hover { color: #008767; transform: translateX(-4px); }
.btn-back:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.form-wrapper { max-width: 550px; width: 100%; margin: auto; }
.brand { font-size: 1.6rem; font-weight: 800; margin-bottom: 40px; }
.brand .med { color: #008767; }
.brand .match { color: #1a202c; }
.welcome-text h1 { font-size: 1.8rem; color: #1a202c; margin-bottom: 30px; }
.auth-form { display: flex; flex-direction: column; gap: 24px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 16px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.full-width { grid-column: span 2; }
label { font-size: 0.85rem; font-weight: 700; color: #1a202c; }
input { padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.95rem; outline: none; transition: border-color 0.2s; color: #1a202c; }
input::placeholder { color: #a0aec0; }
input:focus { border-color: #008767; box-shadow: 0 0 0 3px rgba(0, 135, 103, 0.1); }
.btn-submit { color: white; border: none; padding: 16px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: background 0.2s; margin-top: 8px; width: 100%; }
.patient-btn { background: #008767; }
.patient-btn:hover { background: #006c52; }
.patient-btn:disabled { background: #94a3b8; cursor: not-allowed; }
.banner-section { flex: 1; background-color: #111827; display: flex; flex-direction: column; justify-content: center; padding: 80px; position: relative; border-left: 1px solid #1f2937; }
.banner-content { position: relative; z-index: 2; max-width: 450px; }
.icon-box { width: 56px; height: 56px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; }
.patient-icon { background-color: #008767; color: white; }
.banner-content h2 { color: #ffffff; font-size: 2.4rem; line-height: 1.2; margin-bottom: 20px; font-weight: 700; }
.banner-content p { color: #9ca3af; font-size: 1.1rem; line-height: 1.6; }
@media (max-width: 900px) {
  .banner-section { display: none; }
  .form-grid { grid-template-columns: 1fr; }
  .full-width { grid-column: span 1; }
}
</style>