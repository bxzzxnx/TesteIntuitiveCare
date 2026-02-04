import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'operadoras',
    component: () => import('@/views/OperadorasView.vue'),
    meta: {
      title: 'Operadoras de Saúde'
    }
  },
  {
    path: '/operadora/:cnpj',
    name: 'detalhes',
    component: () => import('@/views/DetalhesOperadoraView.vue'),
    meta: {
      title: 'Detalhes da Operadora'
    }
  },
  {
    // nao encontrar nenhuma rota fora essas vem pá ca
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
