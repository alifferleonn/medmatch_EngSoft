import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ChatView from '@/views/ChatView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterPatient from '@/views/RegisterPatient.vue'
import RegisterDoctor from '@/views/RegisterDoctor.vue'
import DashboardMedic from '@/views/DashboardMedic.vue' // <-- Importação da dashboard
import PreTriagemView from '@/views/PreTriagemView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register-patient',
      name: 'register-patient',
      component: RegisterPatient
    },
    {
      path: '/register-doctor',
      name: 'register-doctor',
      component: RegisterDoctor
    },
    // <-- Nova rota protegida do médico
    {
      path: '/dashboard-medico',
      name: 'dashboard-medico',
      component: DashboardMedic,
      meta: { requiresAuth: true, role: 'doctor' } 
    },
    {
      path: '/confirmacao',
    name: 'Confirmacao',
    component: () => import('../views/ConfirmacaoAgendamento.vue')
    },
    {
      path: '/pretriagem',
      name: 'PreTriagem',
      component: PreTriagemView
    }
  ]
})

// <-- Guarda de rotas (Proteção)
router.beforeEach((to, from, next) => {
  // Simulação: Adapte isso para como você está salvando a sessão do usuário (Pinia, localStorage, etc)
  // Exemplo: assumindo que você salva no localStorage após o login
  const userRole = localStorage.getItem('userRole') // Espera-se 'doctor' ou 'patient'
  const isAuthenticated = !!userRole // Se existe uma role, consideramos autenticado neste exemplo
  
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      // Tenta acessar rota protegida sem estar logado -> vai pro login
      next({ name: 'login' })
    } else if (to.meta.role && to.meta.role !== userRole) {
      // Tenta acessar área de médico sendo paciente -> vai pro chat (ou home)
      next({ name: 'chat' }) 
    } else {
      // Logado e com a permissão correta -> pode passar
      next()
    }
  } else {
    // Rota pública (login, home, registros) -> pode passar
    next()
  }
})

export default router