<template>
  <div class="landing-page">
    <!-- NAVBAR -->
    <nav class="navbar">
      <div class="logo-container">
        <div class="logo-icon">M</div>
        <span class="logo-text">Med <strong>Match</strong></span>
      </div>
      <div class="nav-right">
        <a href="#">Soluções</a>
        <a href="#">Para Clínicas</a>
        <button class="btn-access" @click="irParaLogin">Acessar Sistema</button>
      </div>
    </nav>

    <!-- HERO SECTION -->
    <main class="hero">
      <div class="hero-content">
        <div class="ia-tag">
          <span class="sparkle">✨</span> Nova Triagem com IA Generativa
        </div>
        
        <h1>O match exato para a sua <span>saúde.</span></h1>
        
        <p>
          Nossa IA analisa seus sintomas clínicos em segundos e conecta você à agenda do especialista ideal. Mais assertividade, zero filas.
        </p>

        <div class="cta-buttons">
          <button class="btn-patient" @click="irParaPaciente">Sou Paciente</button>
          <button class="btn-doctor" @click="irParaMedico">Sou Médico</button>
        </div>
      </div>

      <!-- CARD MEDMATCH BRAIN -->
      <div class="hero-visual">
        <div class="brain-card">
          <div class="card-header">
            <div class="ia-badge">IA</div>
            <div class="ia-status">
              <strong>MedMatch Brain</strong>
              <span class="status-dot">Analisando sintomas</span>
            </div>
          </div>
          
          <div class="card-body">
            <div class="quote-box">
              "Paciente relata dor torácica irradiando para o braço esquerdo há 20 minutos."
            </div>
            
            <div class="alert-danger">
              ⚠️ Prioridade Vermelha Detectada
            </div>
            
            <button class="btn-confirm">Confirmar Encaminhamento Rápido</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const irParaLogin = () => {
  router.push('/login');
};

const irParaPaciente = () => {
  router.push('/register-patient');
};

const irParaMedico = () => {
  router.push('/register-doctor');
};
</script>

<style scoped>
.landing-page {
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
}

.logo-icon {
  background: #008767;
  color: white;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: bold;
}

.logo-text {
  font-size: 1.5rem;
  color: #1a202c;
}

.logo-text strong { color: #000; }

.nav-right {
  display: flex;
  align-items: center;
  gap: 35px;
}

.nav-right a {
  text-decoration: none;
  color: #4a5568;
  font-weight: 500;
  font-size: 0.95rem;
}

.btn-access {
  background: #008767;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

/* HERO */
.hero {
  flex: 1;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  align-items: center;
  padding: 0 80px;
  max-width: 1400px;
  margin: 0 auto;
}

.ia-tag {
  background: #e6f3ef;
  color: #008767;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 30px;
}

.hero-content h1 {
  font-size: 4rem;
  color: #1a202c;
  line-height: 1.1;
  margin-bottom: 25px;
}

.hero-content h1 span { color: #008767; }

.hero-content p {
  color: #718096;
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 45px;
  max-width: 520px;
}

.cta-buttons {
  display: flex;
  gap: 20px;
}

.btn-patient {
  background: #008767;
  color: white;
  border: none;
  padding: 18px 40px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
}

.btn-doctor {
  background: white;
  color: #1a202c;
  border: 1px solid #e2e8f0;
  padding: 18px 40px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
}

/* BRAIN CARD */
.brain-card {
  background: white;
  padding: 30px;
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
  border: 1px solid #f1f5f9;
  width: 100%;
  max-width: 420px;
  margin-left: auto;
}

.card-header {
  display: flex;
  gap: 16px;
  margin-bottom: 25px;
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
}

.quote-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 20px;
  border-radius: 12px;
  font-style: italic;
  font-size: 0.95rem;
  color: #4a5568;
  margin-bottom: 20px;
}

.alert-danger {
  background: #fee2e2;
  color: #b91c1c;
  padding: 14px;
  border-radius: 10px;
  text-align: center;
  font-weight: 700;
  font-size: 0.85rem;
  margin-bottom: 20px;
}

.btn-confirm {
  width: 100%;
  background: #008767;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
}
</style>