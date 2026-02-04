import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const message = error.response.data?.detail || 'Erro no servidor' // Erro server
      console.error('Erro API:', message)
    } else if (error.request) {
      console.error('Erro de rede: Não foi possível conectar ao servidor') // Erro de rede
    } else {
      console.error('Erro:', error.message)
    }
    return Promise.reject(error)
  }
)

export const operadorasService = {
  async listar(page = 1, limit = 10, search = '') {
    const params = { page, limit }
    if (search) {
      params.search = search
    }
    const response = await api.get('/operadoras', { params })
    return response.data
  },


  async obterPorCnpj(cnpj) {
    const response = await api.get(`/operadoras/${cnpj}`)
    return response.data
  },


  async obterDespesas(cnpj, page = 1, limit = 10) {
    const response = await api.get(`/operadoras/${cnpj}/despesas`, {
      params: { page, limit }
    })
    return response.data
  }
}

export const estatisticasService = {
  async obter() {
    const response = await api.get('/estatisticas')
    return response.data
  }
}

export default api
