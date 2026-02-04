import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { operadorasService, estatisticasService } from '@/services/api'

export const useOperadorasStore = defineStore('operadoras', () => {
  const operadoras = ref([])
  const operadoraAtual = ref(null)
  const despesasAtual = ref([])
  const estatisticas = ref(null)
  
  const paginacao = ref({
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 0
  })
  const paginacaoDespesas = ref({
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 0
  })
  

  const loading = ref(false)
  const loadingDetalhes = ref(false)
  const loadingDespesas = ref(false)
  const loadingEstatisticas = ref(false)
  const erro = ref(null)
  const erroDetalhes = ref(null)
  const erroDespesas = ref(null)
  const erroEstatisticas = ref(null)

  const termoBusca = ref('') // filtro

  const temOperadoras = computed(() => operadoras.value.length > 0)
  const temDespesas = computed(() => despesasAtual.value.length > 0)
  
  async function carregarOperadoras(page = 1, search = '') {
    loading.value = true
    erro.value = null
    
    try {
      const response = await operadorasService.listar(page, paginacao.value.limit, search)
      operadoras.value = response.data || []
      paginacao.value = {
        page: response.page,
        limit: response.limit,
        total: response.total,
        totalPages: response.total_pages
      }
      termoBusca.value = search
    } catch (e) {
      erro.value = tratarErro(e, 'Erro ao carregar operadoras')
      operadoras.value = []
    } finally {
      loading.value = false
    }
  }

  async function carregarOperadora(cnpj) {
    loadingDetalhes.value = true
    erroDetalhes.value = null
    
    try {
      operadoraAtual.value = await operadorasService.obterPorCnpj(cnpj)
    } catch (e) {
      erroDetalhes.value = tratarErro(e, 'Erro ao carregar detalhes da operadora')
      operadoraAtual.value = null
    } finally {
      loadingDetalhes.value = false
    }
  }

  async function carregarDespesas(cnpj, page = 1) {
    loadingDespesas.value = true
    erroDespesas.value = null
    
    try {
      const response = await operadorasService.obterDespesas(cnpj, page, paginacaoDespesas.value.limit)
      despesasAtual.value = response.data || []
      paginacaoDespesas.value = {
        page: response.page,
        limit: response.limit,
        total: response.total,
        totalPages: response.total_pages
      }
    } catch (e) {
      erroDespesas.value = tratarErro(e, 'Erro ao carregar despesas')
      despesasAtual.value = []
    } finally {
      loadingDespesas.value = false
    }
  }

  async function carregarEstatisticas() {
    loadingEstatisticas.value = true
    erroEstatisticas.value = null
    
    try {
      estatisticas.value = await estatisticasService.obter()
    } catch (e) {
      erroEstatisticas.value = tratarErro(e, 'Erro ao carregar estatísticas')
      estatisticas.value = null
    } finally {
      loadingEstatisticas.value = false
    }
  }

  // Tratamento de erros
  function tratarErro(error, mensagemPadrao) {
    if (error.response) {
      const status = error.response.status
      switch (status) {
        case 404:
          return 'Recurso não encontrado'
        case 422:
          return 'Dados inválidos fornecidos'
        case 500:
          return 'Erro interno do servidor. Tente novamente mais tarde.'
        default:
          return error.response.data?.detail || mensagemPadrao
      }
    } else if (error.request) {
      return 'Não foi possível conectar ao servidor. Verifique sua conexão.'
    }
    return mensagemPadrao
  }


  function limparOperadoraAtual() {
    operadoraAtual.value = null
    despesasAtual.value = []
    erroDetalhes.value = null
    erroDespesas.value = null
  }

  function setLimit(limit) {
    paginacao.value.limit = limit
  }

  return {
    operadoras,
    operadoraAtual,
    despesasAtual,
    estatisticas,
    paginacao,
    paginacaoDespesas,
    termoBusca,
    loading,
    loadingDetalhes,
    loadingDespesas,
    loadingEstatisticas,
    erro,
    erroDetalhes,
    erroDespesas,
    erroEstatisticas,
    temOperadoras,
    temDespesas,
    carregarOperadoras,
    carregarOperadora,
    carregarDespesas,
    carregarEstatisticas,
    limparOperadoraAtual,
    setLimit
  }
})
