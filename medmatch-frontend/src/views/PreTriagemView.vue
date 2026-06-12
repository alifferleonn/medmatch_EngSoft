<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';

interface Mensagem {
  sender: 'user' | 'ia';
  text: string;
}

const router = useRouter();
const novaMensagem = ref('');
const mensagens = ref<Mensagem[]>([
  { sender: 'ia', text: 'Olá! Sou o MedMatch Brain, seu assistente de pré-triagem. Descreva detalhadamente o que você está sentindo para eu encontrar o especialista ideal para o seu caso.' }
]);
const carregando = ref(false);
const boxMensagens = ref<HTMLElement | null>(null);

const voltarHome = () => {
  router.push('/');
};

const scrollParaBaixo = async () => {
  await nextTick();
  if (boxMensagens.value) {
    boxMensagens.value.scrollTop = boxMensagens.value.scrollHeight;
  }
};

const enviarMensagem = async () => {
  if (!novaMensagem.value.trim() || carregando.value) return;

  const textoUsuario = novaMensagem.value;
  mensagens.value.push({ sender: 'user', text: textoUsuario });
  novaMensagem.value = '';
  carregando.value = true;
  scrollParaBaixo();

try {
    // 1. Rota ajustada para bater com o seu @app.post("/triagem")
    const response = await fetch('http://localhost:8000/triagem', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        // 2. Ajustado para enviar 'texto', conforme o BaseModel SintomaInput do seu Python
        texto: textoUsuario 
      })
    });

    const dados = await response.json();

    // 3. Verifica se a resposta contém o padrão do seu Prompt ("Procure por: #especialidade")
    if (dados.resultado && dados.resultado.includes('Procure por:')) {
      
      // Extrai o nome da especialidade logo após a hashtag
      const especialidade = dados.resultado.split('#')[1]?.trim() || 'Especialista';
      
      mensagens.value.push({ 
        sender: 'ia', 
        text: `✅ Triagem concluída! Estamos redirecionando você para a lista de especialistas: ${especialidade}...` 
      });
      
      // Simula o redirecionamento
      setTimeout(() => {
        router.push(`/register-doctor`); 
      }, 4000);

    } else {
      // 4. Se for só conversa, exibe a variável 'resultado' retornada pelo seu Python
      mensagens.value.push({ 
        sender: 'ia', 
        text: dados.resultado || 'Não consegui compreender. Pode detalhar melhor?' 
      });
    }
  } catch (error) {
    mensagens.value.push({ sender: 'ia', text: '⚠️ Instabilidade na conexão com o MedMatch Brain. Por favor, tente enviar novamente.' });
  } finally {
    carregando.value = false;
    scrollParaBaixo();
  }
};
</script>

<template>
  <div class="triagem-page">
    <!-- NAVBAR REAPROVEITADA DA HOME -->
    <nav class="navbar">
      <div class="logo-container" @click="voltarHome">
        <div class="logo-icon">M</div>
        <span class="logo-text">Med <strong>Match</strong></span>
      </div>
      <div class="nav-right">
        <button class="btn-back" @click="voltarHome">Voltar ao Início</button>
      </div>
    </nav>

    <!-- ÁREA DO CHAT CONFIGURADA NO PADRÃO DO BRAIN CARD -->
    <main class="chat-wrapper">
      <div class="brain-chat-card">
        <div class="card-header">
          <div class="ia-badge">IA</div>
          <div class="ia-status">
            <strong>MedMatch Brain — Triagem</strong>
            <span class="status-dot">Processamento clínico ativo</span>
          </div>
        </div>

        <!-- Histórico do Chat -->
        <div class="chat-messages" ref="boxMensagens">
          <div 
            v-for="(msg, index) in mensagens" 
            :key="index" 
            :class="['balao', msg.sender === 'user' ? 'usuario' : 'ia']"
          >
            <p>{{ msg.text }}</p>
          </div>
          <div v-if="carregando" class="balao ia digitando">
            <span class="pulse-animation">✨ MedMatch Brain analisando sintomas...</span>
          </div>
        </div>

        <!-- ÁREA DE INPUT DE TEXTO -->
        <div class="chat-input-area">
          <input 
            v-model="novaMensagem" 
            @keyup.enter="enviarMensagem"
            placeholder="Ex: Estou com uma dor forte de cabeça que começou há 2 dias..." 
            :disabled="carregando"
          />
          <button @click="enviarMensagem" :disabled="carregando || !novaMensagem.trim()">
            Analisar
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.triagem-page {
  min-height: 100vh;
  background-color: #f8fafc;
  background-image: 
    radial-gradient(circle at 50% 50%, rgba(0, 135, 103, 0.05) 0%, transparent 50%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cpath d='M40 0 L80 20 L80 60 L40 80 L0 60 L0 20 Z' fill='none' stroke='%23e2e8f0' stroke-width='0.5'/%3E%3C/svg%3E");
  background-size: auto, 60px;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
}

/* NAVBAR */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 80px;
}
.logo-container { 
  display: flex; 
  align-items: center; 
  gap: 12px; 
  cursor: pointer;
}
.logo-icon { background: #008767; color: white; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 8px; font-weight: bold; }
.logo-text { font-size: 1.5rem; color: #1a202c; }
.logo-text strong { color: #000; }

.btn-back {
  background: transparent;
  color: #4a5568;
  border: 1px solid #e2e8f0;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #f1f5f9;
}

/* CHAT WRAPPER */
.chat-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 80px;
}

.brain-chat-card {
  background: white;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
  border: 1px solid #f1f5f9;
  width: 100%;
  max-width: 800px; 
  height: 65vh;
  min-height: 500px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 15px;
}

.ia-badge {
  background: #008767;
  color: white;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  font-weight: bold;
}

.ia-status strong { display: block; font-size: 1rem; color: #1a202c; }
.ia-status span { font-size: 0.8rem; color: #008767; display: flex; align-items: center; gap: 6px; }
.ia-status span::before {
  content: '';
  width: 8px;
  height: 8px;
  background: #008767;
  border-radius: 50%;
  display: inline-block;
  animation: pulse-dot 2s infinite;
}

/* MENSAGENS */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding-right: 12px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Estilização da barra de rolagem */
.chat-messages::-webkit-scrollbar { width: 6px; }
.chat-messages::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
.chat-messages::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

.balao {
  padding: 16px 20px;
  border-radius: 16px;
  font-size: 1rem;
  line-height: 1.6;
  max-width: 85%;
  word-wrap: break-word;
}

.balao p { margin: 0; }

.usuario {
  background: #008767;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 135, 103, 0.15);
}

.ia {
  background: #f8fafc;
  color: #1a202c;
  border: 1px solid #e2e8f0;
  margin-right: auto;
  border-bottom-left-radius: 4px;
}

.digitando {
  background: #e6f3ef;
  color: #008767;
  border: none;
  font-weight: 500;
  padding: 12px 20px;
}

/* INPUT AREA */
.chat-input-area {
  display: flex;
  gap: 12px;
  border-top: 1px solid #f1f5f9;
  padding-top: 20px;
}

.chat-input-area input {
  flex: 1;
  padding: 16px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: all 0.2s;
  background: #f8fafc;
}

.chat-input-area input:focus {
  border-color: #008767;
  background: white;
  box-shadow: 0 0 0 3px rgba(0, 135, 103, 0.1);
}

.chat-input-area button {
  background: #008767;
  color: white;
  border: none;
  padding: 0 32px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.chat-input-area button:hover:not(:disabled) {
  background: #006e54;
  transform: translateY(-1px);
}

.chat-input-area button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

/* ANIMAÇÕES */
.pulse-animation {
  animation: pulse-text 1.5s infinite ease-in-out;
}

@keyframes pulse-text {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

@keyframes pulse-dot {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 135, 103, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(0, 135, 103, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 135, 103, 0); }
}
</style>