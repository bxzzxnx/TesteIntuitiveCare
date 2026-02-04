<template>
  <div class="container">
    <h1>Operadoras de Saúde</h1>

    <div class="search-box">
      <input
        v-model="searchTerm"
        type="text"
        placeholder="Buscar por CNPJ ou razão social..."
        @keyup.enter="buscar"
      />
      <button @click="buscar" :disabled="store.loading">Buscar</button>
      <button v-if="searchTerm" @click="limpar" class="btn-secondary">Limpar</button>
    </div>

    <div v-if="store.loading" class="loading">Carregando...</div>

    <div v-else-if="store.erro" class="erro">
      {{ store.erro }}
    </div>

    <template v-else>
      <div class="table-section">
        <div class="table-header">
          <h2>Lista de Operadoras</h2>
          <div class="items-per-page">
            <label>Itens por página:</label>
            <select v-model="itemsPerPage" @change="mudarLimit">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="100">100</option>
            </select>
          </div>
        </div>
        
        <div v-if="store.operadoras.length === 0" class="empty">
          Nenhuma operadora encontrada.
        </div>

        <table v-else>
          <thead>
            <tr>
              <th>CNPJ</th>
              <th>Razão Social</th>
              <th>UF</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="op in store.operadoras" :key="op.cnpj">
              <td>{{ formatarCnpj(op.cnpj) }}</td>
              <td>{{ op.razao_social }}</td>
              <td>{{ op.uf }}</td>
              <td>
                <router-link :to="`/operadora/${op.cnpj}`" class="btn-ver">
                  Ver detalhes
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="paginacao">
          <button 
            @click="mudarPagina(1)" 
            :disabled="store.paginacao.page === 1"
          >
            ⏮ Primeira
          </button>
          <button 
            @click="mudarPagina(store.paginacao.page - 1)" 
            :disabled="store.paginacao.page === 1"
          >
            ← Anterior
          </button>
          <span class="page-info">
            Página {{ store.paginacao.page }} de {{ store.paginacao.totalPages }} 
            ({{ store.paginacao.total }} registros)
          </span>
          <button 
            @click="mudarPagina(store.paginacao.page + 1)" 
            :disabled="store.paginacao.page === store.paginacao.totalPages"
          >
            Próxima →
          </button>
          <button 
            @click="mudarPagina(store.paginacao.totalPages)" 
            :disabled="store.paginacao.page === store.paginacao.totalPages"
          >
            Última ⏭
          </button>
        </div>
      </div>

      <!-- Gráfico -->
      <div v-if="store.estatisticas?.top_5_operadoras" class="chart-section">
        <h2>📊 Top 5 Operadoras por Despesas</h2>
        <div class="chart-container">
          <Bar :data="chartData" :options="chartOptions" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOperadorasStore } from '@/stores/operadoras'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useOperadorasStore()
const searchTerm = ref('')
const itemsPerPage = ref(10)

const chartData = computed(() => {
  if (!store.estatisticas?.top_5_operadoras) return { labels: [], datasets: [] }
  
  const top5 = store.estatisticas.top_5_operadoras
  return {
    labels: top5.map(op => op.razao_social?.substring(0, 25) + '...' || 'N/A'),
    datasets: [{
      label: 'Total de Despesas (R$)',
      data: top5.map(op => op.total_despesas || 0),
      backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'],
      borderRadius: 6
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y',
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => {
          const valor = ctx.parsed.x
          return `R$ ${valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
        }
      }
    }
  },
  scales: {
    x: {
      ticks: {
        callback: (value) => {
          if (value >= 1e9) return `R$ ${(value / 1e9).toFixed(0)}B`
          if (value >= 1e6) return `R$ ${(value / 1e6).toFixed(0)}M`
          return `R$ ${value}`
        }
      }
    }
  }
}

function carregarDados() {
  store.carregarOperadoras(1, '')
  store.carregarEstatisticas()
}

function buscar() {
  store.carregarOperadoras(1, searchTerm.value.trim())
}

function limpar() {
  searchTerm.value = ''
  store.carregarOperadoras(1, '')
}

function mudarPagina(page) {
  store.carregarOperadoras(page, searchTerm.value)
}

function mudarLimit() {
  store.setLimit(itemsPerPage.value)
  store.carregarOperadoras(1, searchTerm.value)
}

function formatarCnpj(cnpj) {
  if (!cnpj) return '-'
  const c = cnpj.replace(/\D/g, '')
  if (c.length !== 14) return cnpj
  return c.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5')
}

onMounted(carregarDados)
</script>

<style scoped>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  h1 {
    color: #2c3e50;
    margin-bottom: 24px;
  }

  h2 {
    color: #34495e;
    margin-bottom: 16px;
    font-size: 20px;
  }

  .search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 24px;
  }

  .search-box input {
    flex: 1;
    max-width: 400px;
    padding: 10px 14px;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
  }

  .search-box input:focus {
    outline: none;
    border-color: #3498db;
  }

  .search-box button {
    padding: 10px 20px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }

  .search-box button:hover:not(:disabled) {
    background: #2980b9;
  }

  .search-box button:disabled {
    background: #bdc3c7;
  }

  .btn-secondary {
    background: #95a5a6 !important;
  }

  .loading {
    text-align: center;
    padding: 40px;
    color: #7f8c8d;
  }

  .erro {
    background: #fee;
    padding: 20px;
    border-radius: 8px;
    color: #c0392b;
    text-align: center;
  }

  .erro button {
    margin-top: 10px;
    padding: 8px 16px;
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .table-section {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 32px;
  }

  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 12px;
  }

  .table-header h2 {
    margin: 0;
  }

  .items-per-page {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .items-per-page label {
    font-size: 14px;
    color: #7f8c8d;
  }

  .items-per-page select {
    padding: 8px 12px;
    border: 2px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }

  th {
    background: #f8f9fa;
    font-weight: 600;
    color: #2c3e50;
  }

  tr:hover {
    background: #f8f9fa;
  }

  .btn-ver {
    padding: 6px 12px;
    background: #3498db;
    color: white;
    border-radius: 4px;
    font-size: 12px;
    text-decoration: none;
    white-space: nowrap;
    display: inline-block;
  }

  .btn-ver:hover {
    background: #2980b9;
  }

  .empty {
    text-align: center;
    padding: 40px;
    color: #7f8c8d;
  }

  .paginacao {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    flex-wrap: wrap;
  }

  .paginacao button {
    padding: 8px 14px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 13px;
  }

  .paginacao button:hover:not(:disabled) {
    background: #2980b9;
  }

  .paginacao button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }

  .page-info {
    padding: 8px 16px;
    background: #ecf0f1;
    border-radius: 4px;
    color: #2c3e50;
    font-weight: 500;
  }

  .chart-section {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }

  .chart-container {
    height: 350px;
  }
</style>
