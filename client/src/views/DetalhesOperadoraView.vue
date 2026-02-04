<template>
  <div class="container">
    <button @click="$router.push('/')" class="btn-voltar">← Voltar</button>

    <div v-if="store.loadingDetalhes" class="loading">Carregando...</div>

    <div v-else-if="store.erroDetalhes" class="erro">
      {{ store.erroDetalhes }}
    </div>

    <template v-else-if="store.operadoraAtual">
      <div class="header">
        <h1>{{ store.operadoraAtual.razao_social }}</h1>
        <span class="badge">{{ store.operadoraAtual.modalidade || 'N/A' }}</span>
      </div>

      <div class="info-grid">
        <div class="info-item">
          <label>CNPJ</label>
          <span>{{ formatarCnpj(store.operadoraAtual.cnpj) }}</span>
        </div>
        <div class="info-item">
          <label>Registro ANS</label>
          <span>{{ store.operadoraAtual.registro_operadora || 'N/A' }}</span>
        </div>
        <div class="info-item">
          <label>UF</label>
          <span>{{ store.operadoraAtual.uf || 'N/A' }}</span>
        </div>
        <div class="info-item">
          <label>Cidade</label>
          <span>{{ store.operadoraAtual.cidade || 'N/A' }}</span>
        </div>
        <div class="info-item">
          <label>Telefone</label>
          <span>{{ store.operadoraAtual.ddd ? `(${store.operadoraAtual.ddd}) ${store.operadoraAtual.telefone}` : 'N/A' }}</span>
        </div>
        <div class="info-item info-item-wide">
          <label>E-mail</label>
          <span>{{ store.operadoraAtual.endereco_eletronico || 'N/A' }}</span>
        </div>
      </div>

      <div class="despesas-section">
        <h2>📊 Histórico de Despesas</h2>

        <div v-if="store.loadingDespesas" class="loading">Carregando despesas...</div>

        <div v-else-if="store.despesasAtual.length === 0" class="empty">
          Nenhuma despesa registrada.
        </div>

        <table v-else>
          <thead>
            <tr>
              <th>Trimestre</th>
              <th>Ano</th>
              <th>Total Despesas</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(d, i) in store.despesasAtual" :key="i">
              <td>{{ d.trimestre }}</td>
              <td>{{ d.ano }}</td>
              <td>{{ formatarMoeda(d.total_despesas) }}</td>
            </tr>
          </tbody>
        </table>

        <div v-if="store.paginacaoDespesas.totalPages > 1" class="paginacao">
          <button 
            @click="mudarPaginaDespesas(store.paginacaoDespesas.page - 1)" 
            :disabled="store.paginacaoDespesas.page === 1"
          >
            ← Anterior
          </button>
          <span>Página {{ store.paginacaoDespesas.page }} de {{ store.paginacaoDespesas.totalPages }}</span>
          <button 
            @click="mudarPaginaDespesas(store.paginacaoDespesas.page + 1)" 
            :disabled="store.paginacaoDespesas.page === store.paginacaoDespesas.totalPages"
          >
            Próxima →
          </button>
        </div>
      </div>
    </template>

    <div v-else class="empty">Operadora não encontrada.</div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useOperadorasStore } from '@/stores/operadoras'

const route = useRoute()
const store = useOperadorasStore()

async function carregarDados() {
  await store.carregarOperadora(route.params.cnpj)
  await store.carregarDespesas(route.params.cnpj, 1)
}

function mudarPaginaDespesas(page) {
  store.carregarDespesas(route.params.cnpj, page)
}

function formatarCnpj(cnpj) {
  if (!cnpj) return '-'
  const c = cnpj.replace(/\D/g, '')
  if (c.length !== 14) return cnpj
  return c.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5')
}

function formatarMoeda(valor) {
  if (!valor) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor)
}

onMounted(carregarDados)
onUnmounted(() => store.limparOperadoraAtual())
</script>

<style scoped>
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }

  .btn-voltar {
    padding: 10px 16px;
    background: #ecf0f1;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 20px;
  }

  .btn-voltar:hover {
    background: #bdc3c7;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    gap: 16px;
  }

  .header h1 {
    color: #2c3e50;
    font-size: 24px;
    margin: 0;
  }

  .badge {
    padding: 6px 12px;
    background: #3498db;
    color: white;
    border-radius: 20px;
    font-size: 12px;
    white-space: nowrap;
  }

  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }

  .info-item {
    background: white;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  .info-item-wide {
    grid-column: span 2;
  }

  .info-item label {
    display: block;
    font-size: 12px;
    color: #7f8c8d;
    margin-bottom: 4px;
  }

  .info-item span {
    font-weight: 500;
    color: #2c3e50;
    word-break: break-all;
    overflow-wrap: break-word;
  }

  .despesas-section {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }

  .despesas-section h2 {
    margin: 0 0 20px 0;
    color: #2c3e50;
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

  .empty {
    text-align: center;
    padding: 40px;
    color: #7f8c8d;
  }

  .paginacao {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
  }

  .paginacao button {
    padding: 8px 16px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .paginacao button:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
  }
</style>
