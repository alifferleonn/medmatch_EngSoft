<template>
  <div class="confirmation-overlay">
    <div class="confirmation-card">
      <div class="success-icon-circle">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>

      <h1 class="title">Match Confirmado!</h1>
      <p class="subtitle">
        Sua triagem foi salva no prontuário eletrônico e o especialista já foi notificado.
      </p>

      <div class="appointment-summary">
        <span class="summary-label">RESUMO DO AGENDAMENTO</span>
        
        <div class="doctor-info">
          <div class="doc-avatar">👨‍⚕️</div>
          <div class="doc-text">
            <strong>Dr. {{ doctorName }}</strong>
            <span>{{ especialidade }} • {{ convenio }}</span>
          </div>
        </div>

        <div class="details-row">
          <div class="detail-item">
            <span class="detail-label">DATA</span>
            <p class="detail-value">{{ dataAgendamento }}</p>
          </div>
          <div class="detail-item">
            <span class="detail-label">HORÁRIO</span>
            <p class="detail-value time">{{ horarioAgendamento }} <span>(Manhã)</span></p>
          </div>
        </div>
      </div>

      <button class="btn-panel" @click="irParaPainel">
        Ir para Meu Painel
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Pegamos os dados via Query Params para ser dinâmico
const doctorName = ref(route.query.nome || 'Médico');
const especialidade = ref(route.query.especialidade || 'Especialista');
const convenio = ref(route.query.convenio || 'Particular');
const dataAgendamento = ref('30 de Março, 2026'); // Exemplo estático ou via query
const horarioAgendamento = ref('08:30');

const irParaPainel = () => {
  router.push('/chat'); // Ou para a home do paciente
};
</script>

<style scoped>
.confirmation-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #111827; /* Fundo escuro do Figma */
  padding: 20px;
  font-family: 'Inter', sans-serif;
}

.confirmation-card {
  background: white;
  width: 100%;
  max-width: 600px;
  border-radius: 24px;
  padding: 60px 40px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* ÍCONE */
.success-icon-circle {
  width: 80px;
  height: 80px;
  background-color: #10b981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 32px;
}

.title {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  margin-bottom: 16px;
}

.subtitle {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 40px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

/* CARD DE RESUMO */
.appointment-summary {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  text-align: left;
  margin-bottom: 40px;
}

.summary-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.05em;
  margin-bottom: 20px;
}

.doctor-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.doc-avatar {
  font-size: 2rem;
}

.doc-text strong {
  display: block;
  font-size: 1.1rem;
  color: #111827;
}

.doc-text span {
  font-size: 0.9rem;
  color: #008767;
  font-weight: 600;
}

.details-row {
  display: flex;
  gap: 40px;
}

.detail-label {
  font-size: 0.65rem;
  font-weight: 800;
  color: #94a3b8;
  display: block;
  margin-bottom: 4px;
}

.detail-value {
  font-weight: 700;
  color: #111827;
  font-size: 1rem;
}

.detail-value.time {
  color: #008767;
}

.detail-value span {
  font-weight: 400;
  color: #64748b;
}

/* BOTÃO */
.btn-panel {
  background-color: #008767;
  color: white;
  border: none;
  padding: 16px 48px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, background 0.2s;
}

.btn-panel:hover {
  background-color: #006c52;
  transform: translateY(-2px);
}
</style>