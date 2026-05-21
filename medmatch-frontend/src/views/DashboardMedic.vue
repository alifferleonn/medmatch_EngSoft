<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div>
        <div class="brand-header">
          <h1 class="brand-title">
            <span class="med">Med</span> <span class="match">Match</span>
          </h1>
        </div>
        
        <nav class="nav-menu">
          <a href="#" class="nav-item active">
            Visão Geral
          </a>
          <a href="#" class="nav-item">
            Meus Pacientes
          </a>
        </nav>
      </div>
      
      <div class="sidebar-footer">
        <a href="#" class="nav-item settings-link">
          <svg class="icon-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
          Configurações
        </a>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-header">
        <div class="user-profile">
          <span class="badge-pro">Conta Pro</span>
          
          <span class="doctor-name" v-if="!carregandoNome">Dr. {{ nomeMedico }}</span>
          <span class="doctor-name" v-else>Carregando...</span>
          
          <div class="doctor-avatar">
            {{ iniciais }}
          </div>
        </div>
      </header>

      <div class="dashboard-body">
        <h2 class="page-title">Bom dia, Dr. {{ nomeMedico }}!</h2>
        <p class="page-subtitle">Resumo dos seus atendimentos de hoje.</p>

        <div class="cards-grid">
          <div class="stat-card">
            <div class="icon-wrapper green-bg">
              <svg class="stat-icon green-icon" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"></path>
              </svg>
            </div>
            <div class="stat-info">
              <h4>Pacientes Hoje</h4>
              <p>12</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="icon-wrapper red-bg">
              <svg class="stat-icon red-icon" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
              </svg>
            </div>
            <div class="stat-info">
              <h4>Alta Prioridade</h4>
              <p>2</p>
            </div>
          </div>
        </div>

        <h3 class="section-title">Próximas Consultas</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Horário</th>
                <th>Paciente</th>
                <th>Status Medmatch (IA)</th>
                <th class="text-center">Ação</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="consulta in consultas" :key="consulta.id">
                <td class="time-cell">{{ consulta.horario }}</td>
                <td>
                  <div class="patient-cell">
                    <div class="patient-avatar" :class="consulta.avatarTheme">
                      {{ consulta.iniciais }}
                    </div>
                    <div>
                      <p class="patient-name">{{ consulta.nome }}</p>
                      <p class="patient-plan">{{ consulta.convenio }}</p>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="status-badge" :class="consulta.statusTheme">
                    {{ consulta.status }}
                  </span>
                </td>
                <td class="text-center">
                  <button class="btn-action">Prontuário</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { supabase } from '../supabase.js' // Importando sua conexão

const nomeMedico = ref('...')
const carregandoNome = ref(true)

// Buscar o nome do médico no banco de dados
const buscarDadosMedico = async () => {
  try {
    carregandoNome.value = true
    
    // 1. Pegamos o ID do usuário que salvamos no localStorage durante o registro
    const userId = localStorage.getItem('userId')
    
    if (!userId) {
      nomeMedico.value = 'Médico'
      return
    }

    // 2. Fazemos a query na tabela Usuario para pegar o nome
    const { data, error } = await supabase
      .from('Usuario')
      .select('nome')
      .eq('id', userId)
      .single()

    if (error) throw error

    if (data) {
      nomeMedico.value = data.nome
    }
  } catch (error) {
    console.error('Erro ao buscar nome do médico:', error.message)
    nomeMedico.value = 'Médico'
  } finally {
    carregandoNome.value = false
  }
}

onMounted(() => {
  buscarDadosMedico()
})

// Gerador de iniciais automático
const iniciais = computed(() => {
  if (!nomeMedico.value || nomeMedico.value === '...') return 'MD'
  const partes = nomeMedico.value.trim().split(' ')
  if (partes.length >= 2) {
    return (partes[0][0] + partes[1][0]).toUpperCase()
  }
  return partes[0][0].toUpperCase()
})

// Dados mockados da tabela
const consultas = ref([
  {
    id: 1,
    horario: '08:30',
    nome: 'Aliffer Leonn',
    iniciais: 'AL',
    convenio: 'Unimed',
    status: 'Sintoma: Cefaleia Intensa',
    avatarTheme: 'avatar-green',
    statusTheme: 'badge-red'
  },
  {
    id: 2,
    horario: '10:00',
    nome: 'João Ricardo',
    iniciais: 'JR',
    convenio: 'Particular',
    status: 'Check-up de Rotina',
    avatarTheme: 'avatar-blue',
    statusTheme: 'badge-green'
  }
])
</script>

<style scoped>
/* TODO O CSS QUE ENVIEI ANTES - MANTENHA EXATAMENTE IGUAL */
* { box-sizing: border-box; margin: 0; padding: 0; }
.dashboard-layout { display: flex; height: 100vh; background-color: #F8F9FA; font-family: 'Inter', sans-serif; color: #1a202c; }
.sidebar { width: 260px; background-color: #ffffff; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; flex-shrink: 0; }
.brand-header { height: 80px; display: flex; align-items: center; padding: 0 32px; }
.brand-title { font-size: 1.25rem; font-weight: 800; }
.brand-title .med { color: #008767; }
.brand-title .match { color: #1a202c; }
.nav-menu { padding: 16px 16px 0; display: flex; flex-direction: column; gap: 8px; }
.nav-item { display: flex; align-items: center; padding: 12px 16px; border-radius: 8px; text-decoration: none; color: #64748b; font-weight: 600; font-size: 0.95rem; transition: all 0.2s; }
.nav-item:hover { background-color: #f8fafc; color: #1a202c; }
.nav-item.active { background-color: #e6f3f0; color: #008767; }
.sidebar-footer { padding: 16px; }
.icon-svg { width: 20px; height: 20px; margin-right: 12px; }
.main-content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.top-header { height: 80px; background-color: #ffffff; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: flex-end; padding: 0 32px; flex-shrink: 0; }
.user-profile { display: flex; align-items: center; gap: 16px; }
.badge-pro { background-color: #e6f3f0; color: #008767; padding: 6px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;}
.doctor-name { font-weight: 600; color: #1a202c; font-size: 0.95rem; }
.doctor-avatar { width: 40px; height: 40px; border-radius: 50%; background-color: #111827; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; }
.dashboard-body { padding: 40px; overflow-y: auto; }
.page-title { font-size: 1.8rem; font-weight: 700; color: #111827; margin-bottom: 4px; }
.page-subtitle { color: #64748b; font-size: 1rem; margin-bottom: 32px; }
.cards-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 600px; margin-bottom: 48px; }
.stat-card { background-color: #ffffff; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; display: flex; align-items: center; gap: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.icon-wrapper { width: 56px; height: 56px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-icon { width: 32px; height: 32px; }
.green-bg { background-color: #e6f3f0; }
.green-icon { color: #008767; }
.red-bg { background-color: #fee2e2; }
.red-icon { color: #dc2626; }
.stat-info h4 { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #94a3b8; margin-bottom: 4px; letter-spacing: 0.5px; }
.stat-info p { font-size: 2rem; font-weight: 800; color: #111827; line-height: 1; }
.section-title { font-size: 1.25rem; font-weight: 700; color: #111827; margin-bottom: 16px; }
.table-container { background-color: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
table { width: 100%; border-collapse: collapse; text-align: left; }
th { padding: 16px 24px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #94a3b8; border-bottom: 1px solid #e2e8f0; letter-spacing: 0.5px; }
td { padding: 16px 24px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
.time-cell { font-weight: 700; color: #111827; font-size: 0.95rem; }
.patient-cell { display: flex; align-items: center; gap: 16px; }
.patient-avatar { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; flex-shrink: 0; }
.avatar-green { background-color: #e6f3f0; color: #008767; }
.avatar-blue { background-color: #e0e7ff; color: #4338ca; }
.patient-name { font-weight: 700; color: #111827; font-size: 0.95rem; margin-bottom: 2px; }
.patient-plan { font-size: 0.85rem; color: #64748b; }
.status-badge { padding: 6px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 700; display: inline-block; }
.badge-red { background-color: #fee2e2; color: #dc2626; }
.badge-green { background-color: #e6f3f0; color: #008767; }
.btn-action { padding: 8px 24px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #ffffff; font-family: inherit; font-weight: 600; font-size: 0.85rem; color: #475569; cursor: pointer; transition: all 0.2s; }
.btn-action:hover { background-color: #f1f5f9; color: #111827; border-color: #cbd5e1; }
.text-center { text-align: center; }
</style>