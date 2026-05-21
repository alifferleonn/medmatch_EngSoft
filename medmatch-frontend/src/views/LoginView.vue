<template>
  <div class="login-layout">
    <!-- LADO ESQUERDO: Formulário -->
    <div class="form-section">
      <!-- Seta de Voltar com bloqueio durante o carregamento -->
      <button class="btn-back" @click="voltarParaHome" :disabled="carregando">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        Voltar
      </button>

      <div class="form-wrapper">
        <!-- Logo -->
        <div class="brand">
          <span class="med">Med</span> <span class="match">Match</span>
        </div>
        
        <!-- Textos de Boas-vindas -->
        <div class="welcome-text">
          <h1>Bem-vindo de volta</h1>
          <p>Insira suas credenciais para acessar seu painel.</p>
        </div>

        <!-- Formulário -->
        <form @submit.prevent="fazerLogin" class="auth-form">
          <div class="form-group">
            <label>E-mail Corporativo ou Pessoal</label>
            <!-- v-model para o e-mail -->
            <input type="email" v-model="email" placeholder="seu-email@gmail.com" required />
          </div>
          
          <div class="form-group">
            <div class="password-header">
              <label>Senha</label>
              <a href="#" class="forgot-password">Esqueceu?</a>
            </div>
            <!-- v-model para a senha -->
            <input type="password" v-model="senha" placeholder="••••••••" required />
          </div>

          <button type="submit" class="btn-submit" :disabled="carregando">
            {{ carregando ? 'Autenticando...' : 'Entrar na Plataforma' }}
          </button>
        </form>
      </div>
    </div>

    <!-- LADO DIREITO: Banner Visual -->
    <div class="banner-section">
      <div class="banner-content">
        <h2>A saúde do futuro,<br>agora nas suas mãos.</h2>
        <p>
          Junte-se a mais de 500 profissionais e milhares de pacientes que simplificaram a jornada médica.
        </p>
      </div>
      <div class="circle-decoration"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// Importação do Supabase
import { supabase } from '../supabase.js'; 

const router = useRouter();

// Variáveis reativas
const email = ref('');
const senha = ref('');
const carregando = ref(false);

const voltarParaHome = () => {
  router.push('/');
};

const fazerLogin = async () => {
  carregando.value = true;

  try {
    // 1. Busca o usuário batendo e-mail e senha
    const { data: usuario, error: erroUsuario } = await supabase
      .from('Usuario')
      .select('id')
      .eq('email', email.value)
      .eq('senha_hash', senha.value)
      .single();

    if (erroUsuario || !usuario) {
      throw new Error('E-mail ou senha incorretos.');
    }

    // 2. Verifica se esse usuário é um PACIENTE
    // Usamos .maybeSingle() porque pode retornar vazio e não queremos que dê erro
    const { data: paciente } = await supabase
      .from('Paciente')
      .select('id')
      .eq('usuario_id', usuario.id)
      .maybeSingle();

    if (paciente) {
      console.log('Login de Paciente detectado!');
      router.push('/chat');
      return; // Para a execução da função aqui
    }

    // 3. Verifica se esse usuário é um MÉDICO
    const { data: medico } = await supabase
      .from('Medico')
      .select('id')
      .eq('usuario_id', usuario.id)
      .maybeSingle();

    if (medico) {
      console.log('Login de Médico detectado!');
      // Quando você criar a tela do médico, lembre-se de configurar essa rota no router/index.ts
      router.push('/dashboard-medico'); 
      return; 
    }

    // Se achou o usuário mas ele não tá nem na tabela de paciente nem de médico
    throw new Error('Conta incompleta. Perfil de paciente ou médico não encontrado.');

  } catch (error: any) {
    console.error('Erro ao fazer login:', error);
    alert(error.message);
  } finally {
    carregando.value = false;
  }
};
</script>

<style scoped>
/* O CSS se mantém exatamente igual ao layout do Figma que fizemos */
.login-layout { display: flex; min-height: 100vh; font-family: 'Inter', sans-serif; }
.form-section { flex: 1; display: flex; flex-direction: column; background-color: #ffffff; padding: 40px; position: relative; }
.btn-back { background: transparent; border: none; color: #4a5568; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 0.95rem; transition: color 0.2s, transform 0.2s; padding: 0; width: fit-content; }
.btn-back:hover { color: #008767; transform: translateX(-4px); }
.btn-back:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
.form-wrapper { max-width: 420px; width: 100%; margin: auto; }
.brand { font-size: 1.8rem; font-weight: 800; margin-bottom: 40px; }
.brand .med { color: #008767; }
.brand .match { color: #1a202c; }
.welcome-text h1 { font-size: 2rem; color: #1a202c; margin-bottom: 8px; }
.welcome-text p { color: #718096; font-size: 0.95rem; margin-bottom: 40px; }
.auth-form { display: flex; flex-direction: column; gap: 24px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.password-header { display: flex; justify-content: space-between; align-items: center; }
label { font-size: 0.85rem; font-weight: 700; color: #2d3748; }
.forgot-password { font-size: 0.85rem; color: #008767; text-decoration: none; font-weight: 600; }
.forgot-password:hover { text-decoration: underline; }
input { padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 1rem; outline: none; transition: border-color 0.2s; color: #1a202c; }
input::placeholder { color: #a0aec0; }
input:focus { border-color: #008767; box-shadow: 0 0 0 3px rgba(0, 135, 103, 0.1); }
.btn-submit { background: #008767; color: white; border: none; padding: 16px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: background 0.2s; margin-top: 8px; }
.btn-submit:hover { background: #006c52; }
.btn-submit:disabled { background: #94a3b8; cursor: not-allowed; }
.banner-section { flex: 1; background-color: #006c52; display: flex; flex-direction: column; justify-content: center; padding: 80px; position: relative; overflow: hidden; }
.banner-content { position: relative; z-index: 2; max-width: 500px; }
.banner-content h2 { color: #ffffff; font-size: 2.8rem; line-height: 1.2; margin-bottom: 24px; }
.banner-content p { color: rgba(255, 255, 255, 0.85); font-size: 1.1rem; line-height: 1.6; }
.circle-decoration { position: absolute; bottom: -15%; right: -10%; width: 600px; height: 600px; background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; z-index: 1; pointer-events: none; }
@media (max-width: 900px) { .banner-section { display: none; } }
</style>