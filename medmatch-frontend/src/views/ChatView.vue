<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="logo">
        <span class="brand-med">Med</span><span class="brand-match"> Match</span>
      </div>
      
      <nav class="menu">
        <div class="menu-item active">Nova Triagem (IA)</div>
        <div class="menu-item">Histórico de Consultas</div>
      </nav>

      <!-- HEURÍSTICA 3: Controle e Liberdade - Opção para limpar e recomeçar a triagem atual -->
      <div class="sidebar-actions" v-if="mensagens.length > 1">
        <button class="btn-reset" @click="reiniciarTriagemVisual">🔄 Reiniciar Triagem</button>
      </div>

      <div class="sidebar-footer">
        <div class="menu-item settings">⚙️ Configurações</div>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="user-info">
          <span>Aliffer Leonn</span>
          <div class="avatar">AL</div>
        </div>
      </header>

      <div class="content-grid">
        <section class="chat-section">
          <div class="chat-card">
            <header class="chat-card-header">
              <div class="ia-badge">IA</div>
              <div>
                <strong>MedMatch (IA)</strong>
                <p class="online-status">Online</p>
              </div>
            </header>

            <div class="chat-messages" ref="chatRef">
              <!-- HEURÍSTICA 7: Flexibilidade e Eficiência - Atalhos de cliques para acelerar o uso -->
              <div v-if="mensagens.length === 1" class="quick-tags">
                <p>Sugestões de sintomas comuns:</p>
                <div class="tags-container">
                  <span class="tag" @click="inserirSintomaRapido('Estou com dor de cabeça forte e sensibilidade à luz')">🧠 Dor de Cabeça</span>
                  <span class="tag" @click="inserirSintomaRapido('Sinto dor de estômago e enjoo após comer')">🤢 Dor de Estômago</span>
                </div>
              </div>

              <div v-for="(m, i) in mensagens" :key="i" :class="['msg-box', m.role]">
                <div class="bubble">
                  <p v-if="m.role === 'bot' && m.status" class="status-indicator">✓ {{ m.status }}</p>
                  <p>{{ m.text }}</p>
                  
                  <!-- HEURÍSTICA 9: Diagnóstico e Recuperação de Erros - Feedback explicativo com ação de suporte -->
                  <div v-if="m.text === 'Erro ao conectar com a IA.'" class="error-action-area">
                    <small>Dica: Verifique sua conexão de rede ou clique no botão abaixo para tentar o envio novamente.</small>
                    <button class="btn-retry" @click="retransmitirMensagem">🔄 Tentar Reenviar</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- HEURÍSTICA 10: Ajuda e Documentação - Agrupamento do input com texto de ajuda contextualizado -->
            <footer class="chat-input-area-container">
              <div class="chat-input-area">
                <input 
                  v-model="inputUsuario" 
                  @keyup.enter="enviar"
                  placeholder="Digite sua resposta..."
                />
                <!-- HEURÍSTICA 5: Prevenção de Erros - Botão desabilitado visualmente se o campo estiver vazio -->
                <button 
                  @click="enviar" 
                  :disabled="loading || !inputUsuario.trim()"
                  :class="{ 'btn-disabled': !inputUsuario.trim() || loading }"
                >
                  Enviar
                </button>
              </div>
              <p class="input-help-text">
                💡 <strong>Ajuda:</strong> Informe o sintoma principal, há quanto tempo começou e a intensidade.
              </p>
            </footer>
          </div>
        </section>

        <section class="recommendations">
          
          <h3 v-if="especialidadeAtual">
            {{ especialidadeAtual }} Recomendados
          </h3>
          <h3 v-else>Médicos Recomendados</h3>

          <div v-if="buscandoMedicos" class="loading-state">
            <p>Buscando especialistas...</p>
          </div>

          <div v-else-if="especialidadeAtual && medicosFiltrados.length === 0" class="empty-state">
            <p>Nenhum {{ especialidadeAtual.toLowerCase() }} encontrado na nossa rede no momento.</p>
          </div>

          <div v-else class="docs-list">
            <div v-for="medico in medicosFiltrados" :key="medico.id" class="doc-card">
              <div class="doc-header-row">
                <div class="doc-avatar">👨‍⚕️</div>
                <div class="doc-info">
                  <strong>Dr(a). {{ medico.Usuario?.nome || 'Nome Indisponível' }}</strong>
                  <span class="doc-sub">CRM {{ medico.crm }} • {{ medico.especialidade }}</span>
                </div>
              </div>
              
              <div class="horario">
                <small>Disponibilidade</small>
                <p>Ver agenda</p>
              </div>
              
              <button class="btn-agendar" @click="agendar(medico)">
                Agendar Consulta
              </button>
            </div>
          </div>

          <div v-if="!especialidadeAtual && !buscandoMedicos" class="empty-state">
            <p>Converse com a IA para receber recomendações de especialistas.</p>
          </div>

        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { supabase } from '../supabase.js'; 

const router = useRouter();
const inputUsuario = ref('');
const loading = ref(false);
const chatRef = ref(null);
const mensagens = ref([
  { role: 'bot', text: 'Olá, Aliffer! Me descreva detalhadamente o que você está sentindo.' }
]);

const medicosFiltrados = ref([]);
const especialidadeAtual = ref('');
const buscandoMedicos = ref(false);

const cacheUltimoTexto = ref(''); // Armazena a última string para retransmissão de segurança

// --- ADICIONADO APENAS FUNÇÕES ACESSÓRIAS VISUAIS ---

// H3: Controle e Liberdade - Reinicia o estado da tela sem alterar métodos de negócio
const reiniciarTriagemVisual = () => {
  mensagens.value = [{ role: 'bot', text: 'Olá, Aliffer! Me descreva detalhadamente o que você está sentindo.' }];
  medicosFiltrados.value = [];
  especialidadeAtual.value = '';
  inputUsuario.value = '';
};

// H7: Flexibilidade e Eficiência - Atalho para injetar texto rápido
const inserirSintomaRapido = (texto) => {
  inputUsuario.value = texto;
};

// H9: Recuperação de Erros - Re-executa o envio caso a requisição caia no catch
const retransmitirMensagem = () => {
  mensagens.value = mensagens.value.filter(m => m.text !== 'Erro ao conectar com a IA.');
  inputUsuario.value = cacheUltimoTexto.value;
  enviar();
};

// --- SUAS FUNÇÕES ORIGINAIS (INALTERADAS) ---

const buscarMedicosDaEspecialidade = async (especialidade) => {
  buscandoMedicos.value = true;
  medicosFiltrados.value = [];
  especialidadeAtual.value = especialidade + 's'; 

  try {
    const { data, error } = await supabase
      .from('Medico')
      .select(`
        id,
        crm,
        especialidade,
        Usuario (
          nome
        )
      `)
      .ilike('especialidade', especialidade); 

    if (error) throw error;
    medicosFiltrados.value = data;
  } catch (err) {
    console.error("Erro ao buscar médicos:", err.message);
  } finally {
    buscandoMedicos.value = false;
  }
};

const enviar = async () => {
  if (!inputUsuario.value.trim() || loading.value) return;

  const texto = inputUsuario.value;
  cacheUltimoTexto.value = texto; // Salva o texto antes de limpar o input para segurança de reenvio
  mensagens.value.push({ role: 'user', text: texto });
  inputUsuario.value = '';
  loading.value = true;

  await nextTick();
  chatRef.value.scrollTop = chatRef.value.scrollHeight;

  try {
    const { data } = await api.post('/triagem', { texto });
    const respostaBot = data.resultado;

    mensagens.value.push({ 
      role: 'bot', 
      status: 'Análise Concluída',
      text: respostaBot 
    });

    const matchHashtag = respostaBot.match(/#([a-zA-ZÀ-ÿ]+)/); 
    if (matchHashtag) {
      await buscarMedicosDaEspecialidade(matchHashtag[1]);
    }

  } catch (e) {
    mensagens.value.push({ role: 'bot', text: 'Erro ao conectar com a IA.' });
  } finally {
    loading.value = false;
    await nextTick();
    chatRef.value.scrollTop = chatRef.value.scrollHeight;
  }
};

const agendar = (medico) => {
  router.push({
    path: '/confirmacao',
    query: {
      nome: medico.Usuario.nome,
      especialidade: medico.especialidade,
      convenio: 'Unimed'
    }
  });
};
</script>

<style scoped>
/* SEUS ESTILOS ORIGINAIS INTEGRALMENTE MANTIDOS */
.dashboard-container { display: flex; height: 100vh; background-color: #f8fafc; font-family: 'Inter', sans-serif; }
.sidebar { width: 240px; background: white; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; padding: 24px; }
.brand-med { color: #008767; font-weight: bold; font-size: 1.5rem; }
.brand-match { color: #1a202c; font-weight: bold; font-size: 1.5rem; }
.menu { margin-top: 40px; flex: 1; }
.menu-item { padding: 12px 16px; border-radius: 8px; color: #64748b; cursor: pointer; margin-bottom: 8px; font-size: 0.9rem; }
.menu-item.active { background-color: #e6f3ef; color: #008767; font-weight: 500; }
.settings { margin-top: auto; color: #94a3b8; }
.main-content { flex: 1; display: flex; flex-direction: column; }
.top-bar { height: 70px; background: white; display: flex; justify-content: flex-end; align-items: center; padding: 0 40px; border-bottom: 1px solid #e2e8f0; }
.user-info { display: flex; align-items: center; gap: 12px; font-weight: 500; }
.avatar { width: 35px; height: 35px; background: #e6f3ef; color: #008767; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; }
.content-grid { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 24px; padding: 30px; height: calc(100vh - 70px); }
.chat-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; display: flex; flex-direction: column; height: 100%; }
.chat-card-header { padding: 16px; border-bottom: 1px solid #f1f5f9; display: flex; gap: 12px; align-items: center; }
.ia-badge { background: #008767; color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: bold; }
.online-status { font-size: 0.7rem; color: #008767; margin:0; }
.chat-messages { flex: 1; padding: 20px; overflow-y: auto; }
.msg-box { display: flex; margin-bottom: 16px; }
.msg-box.user { justify-content: flex-end; }
.msg-box.bot { justify-content: flex-start; }
.bubble { max-width: 80%; padding: 14px; border-radius: 12px; font-size: 0.9rem; }
.user .bubble { background: #008767; color: white; }
.bot .bubble { background: #f8fafc; border: 1px solid #e2e8f0; }
.status-indicator { color: #008767; font-weight: bold; font-size: 0.8rem; margin-bottom: 4px; }
.chat-input-area { padding: 16px; display: flex; gap: 12px; border-top: 1px solid #f1f5f9; }
input { flex: 1; background: #f8fafc; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; outline: none; }
button { background: #008767; color: white; border: none; padding: 0 24px; border-radius: 8px; cursor: pointer; font-weight: 600; }
.recommendations h3 { margin-top: 0; color: #1a202c; font-size: 1.1rem;}
.docs-list { display: flex; flex-direction: column; gap: 16px; margin-top: 16px; overflow-y: auto; max-height: calc(100vh - 180px); }
.doc-card { background: white; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; display: flex; flex-direction: column; gap: 12px; }
.doc-header-row { display: flex; align-items: center; gap: 12px;}
.doc-avatar { width: 40px; height: 40px; background: #e2e8f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;}
.doc-info { display: flex; flex-direction: column; gap: 2px; }
.doc-sub { color: #64748b; font-size: 0.8rem;}
.horario { background: #f8fafc; padding: 10px; border-radius: 8px; margin-top: 4px; }
.horario p { color: #008767; font-weight: bold; margin: 0; font-size: 0.9rem;}
.btn-agendar { background: #008767; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 500; cursor: pointer; margin-top: 4px; }
.loading-state, .empty-state { background: white; padding: 20px; border-radius: 12px; border: 1px dashed #cbd5e1; text-align: center; color: #64748b; margin-top: 16px; }

/* NOVOS COMPLEMENTOS DE DESIGN ADICIONADOS PARA AS REGRAS FALTANTES */
.sidebar-actions { padding: 0 16px; margin-top: 10px; }
.btn-reset { width: 100%; background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; padding: 8px; border-radius: 6px; cursor: pointer; font-size: 0.85rem; font-weight: 500; transition: all 0.2s; }
.btn-reset:hover { background: #fee2e2; color: #ef4444; border-color: #fca5a5; }

.quick-tags { margin-bottom: 20px; background: #f8fafc; padding: 12px; border-radius: 8px; border: 1px dashed #e2e8f0; }
.quick-tags p { margin: 0 0 8px 0; font-size: 0.8rem; color: #64748b; font-weight: 500; }
.tags-container { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { background: white; border: 1px solid #e2e8f0; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #008767; cursor: pointer; font-weight: 500; transition: 0.2s; }
.tag:hover { background: #e6f3ef; border-color: #008767; }

.chat-input-area-container { border-top: 1px solid #f1f5f9; display: flex; flex-direction: column; gap: 6px; background: white; border-radius: 0 0 12px 12px; }
.chat-input-area-container .chat-input-area { border-top: none; padding: 16px 16px 4px 16px; }
.input-help-text { margin: 0 16px 12px 16px; font-size: 0.75rem; color: #64748b; }

.btn-disabled { background: #cbd5e1 !important; color: #94a3b8 !important; cursor: not-allowed !important; }

.error-action-area { margin-top: 10px; padding-top: 8px; border-top: 1px dashed #fca5a5; }
.error-action-area small { display: block; color: #64748b; margin-bottom: 8px; font-size: 0.75rem; }
.btn-retry { background: #ef4444; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer; font-weight: 600; }
.btn-retry:hover { background: #dc2626; }
</style>