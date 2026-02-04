# Teste Intuitive Care

Desafio técnico do processo seletivo para estágio na Intuitive Care 2026 implementando integração com dados públicos da ANS, transformação e validação de dados, análise em banco de dados SQL e API REST com interface web.

## Observações


1. Durante a realização do projeto, mais preciso na fase `1.3 Consolidação e Análise de Inconsistências`. Minha interpretação foi a seguinte, eu juntei os dados em um `.csv` só e fiz a junção do `cnpj` somente na etapa `2.2  Enriquecimento de Dados com Tratamento de Falhas ` 

2. No arquivo `insert_csv.sql` mude o diretório que está ali para o diretório do seu computador onde estão localizados os arquivos `.csv` que precisaremos utilizar 

##  Índice

- [Visão Geral](#-visão-geral)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Fluxo de Execução](#-fluxo-de-execução)
- [Estrutura do Projeto](#-estrutura-do-projeto)

##  Visão Geral

O projeto é dividido em **4 etapas principais**:

1. Integração e download dos 3 últimos trimestres
2. Transofrmação e Validação de arquivos
3. Criação do banco de dados
4. Api e interface web



##  Pré-requisitos

- **Python 3.10+**
- **Node.js 18+**
- **PostgreSQL** (para a API)



## Instalação

### 1. Clone o projeto
```bash
git clone https://github.com/bxzzxnx/TesteIntuitiveCare
cd TesteIntuitiveCare
```

### 2. Criar e ativar ambiente virtual

```bash
# Na raiz do projeto
TesteIntuitiveCare> python -m venv .venv

# Windows
TesteIntuitiveCare> .venv\Scripts\activate

# Linux/Mac
TesteIntuitiveCare> source .venv/bin/activate
```

Quando ativado, você verá `(.venv)` no terminal:
```bash
(.venv) TesteIntuitiveCare>
```

### 3. Instalar dependências Python

```bash
(.venv) TesteIntuitiveCare> pip install -r requirements.txt
```

### 4. Instalar dependências do Frontend

```bash
(.venv) TesteIntuitiveCare> cd client
(.venv) TesteIntuitiveCare\client> npm install
```

---

##  Testando a API (Postman)

O projeto inclui uma coleção Postman para testar todos os endpoints da API.

### Como usar:

1. **Importe a coleção** `postman_collection.json` no Postman
2. **Certifique-se que a API está rodando** (`fastapi dev app.py`)
3. **Execute os requests** da coleção

### Endpoints disponíveis:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/operadoras` | Lista operadoras (com paginação e busca) |
| GET | `/api/operadoras/{cnpj}` | Detalhes de uma operadora |
| GET | `/api/operadoras/{cnpj}/despesas` | Despesas de uma operadora |
| GET | `/api/estatisticas` | Estatísticas gerais |

### Variáveis da coleção:

| Variável | Valor Padrão |
|----------|--------------|
| `base_url` | `http://localhost:8000` |
| `cnpj_exemplo` | `54557861000102` |

---

##  Fluxo de Execução

Execute os scripts **na ordem** para processar os dados corretamente:

### **Etapa 1: Integração de Dados** (`Integracao_api/`)

```bash
(.venv) TesteIntuitiveCare> cd Integracao_api

# 1.1 - Baixar demonstrações contábeis trimestrais da ANS
(.venv) TesteIntuitiveCare\Integracao_api> python download_trimentes.py
# Saída: data/raw/*.zip

# 1.2 - Extrair arquivos ZIP
(.venv) TesteIntuitiveCare\Integracao_api> python extracao_zips.py
# Saída: data/extracted/*.csv

# 1.3 - Consolidar CSVs em arquivo único
(.venv) TesteIntuitiveCare\Integracao_api> python consolidar_dados.py
# Saída: data/consolidado_despesas.csv
```

### **Etapa 2: Transformação e Validação** (`Transformacao_validacao_dados/`)

```bash
(.venv) TesteIntuitiveCare> cd Transformacao_validacao_dados

# 2.1 - Baixar cadastro de operadoras ativas
(.venv) TesteIntuitiveCare\Transformacao_validacao_dados> python download_cadop.py
# Saída: data/relatorio_cadop.csv

# 2.2 - Enriquecer, validar e agregar dados
(.venv) TesteIntuitiveCare\Transformacao_validacao_dados> python enriquecer_dados.py
# Saída: data/despesas_agregadas.csv + data/Teste_Antonio.zip
```


### **Etapa 3: Executar a API** (`server/`)

```bash
(.venv) TesteIntuitiveCare> cd server
(.venv) TesteIntuitiveCare\server fastapi dev app.py
```

| Recurso | URL |
|---------|-----|
| API | http://localhost:8000 |
| Documentação Swagger | http://localhost:8000/docs |

### **Etapa 4: Executar o Frontend** (`client/`)

```bash
(.venv) TesteIntuitiveCare> cd client
(.venv) TesteIntuitiveCare\client> npm run dev
```

| Recurso | URL |
|---------|-----|
| Aplicação Vue.js | http://localhost:5173 |

---

## 📁 Arquivos e Responsabilidades

| Pasta | Arquivo | Descrição |
|-------|---------|-----------|
| `Integracao_api/` | `download_trimentes.py` | Download das demonstrações contábeis trimestrais |
| | `extracao_zips.py` | Extração dos arquivos ZIP baixados |
| | `consolidar_dados.py` | Consolidação dos CSVs em arquivo único |
| `Transformacao_validacao_dados/` | `download_cadop.py` | Download do cadastro de operadoras ativas |
| | `cnpj_utils.py` | Funções de validação de CNPJ |
| | `enriquecer_dados.py` | Enriquecimento, validação e agregação |
| `server/` | `app.py` | Aplicação FastAPI principal |
| | `apirouter.py` | Rotas da API |
| | `models.py` | Modelos Pydantic |
| | `db/db.py` | Conexão com PostgreSQL |
| `client/` | `views/*.vue` | Páginas da aplicação |
| | `stores/operadoras.js` | Estado global (Pinia) |
| | `api/api.js` | Cliente HTTP para API |

---

## 🗂️ Estrutura do Projeto

```
TesteIntuitiveCare/
│
├── 📁 Integracao_api/          # Etapa 1: Coleta de dados
│   ├── 🐍 download_trimentes.py
│   ├── 🐍 extracao_zips.py
│   └── 🐍 consolidar_dados.py
│
├── 📁 Transformacao_validacao_dados/  # Etapa 2: ETL
│   ├── 🐍 cnpj_utils.py
│   ├── 🐍 download_cadop.py
│   └── 🐍 enriquecer_dados.py
│
├── 📁 data/                    # Dados p
│   ├── 📁 raw/                 # ZIPs originais
│   ├── 📁 extracted/           # CSVs extraídos
│   ├── 📄 consolidado_despesas.csv
│   ├── 📄 relatorio_cadop.csv       # CSV das operadoras
│   └── 📄 despesas_agregadas.csv
│
├── 📁 server/                  # Etapa 4.1: API Backend
│   ├── 📁 db/
│   │   └── 🐍 db.py
│   ├── 🐍 app.py
│   ├── 🐍 apirouter.py
│   └── 🐍 models.py
│
├── 📁 client/                  # Etapa 4.2: Frontend
│   ├── 📁 src/
│   │   ├── 📁 api/
│   │   ├── 📁 router/
│   │   ├── 📁 stores/
│   │   └── 📁 views/
│   ├── 🌐 index.html
│   └── ⚙️ vite.config.js
│
├── 📁 sql/                     # Etapa 3: Scripts SQL
│   ├── 📄 create_tables.sql
│   ├── 📄 insert_csv.sql
│   └── 📄 query*.sql
│
├── 📄 requirements.txt
├── 📄 postman_collection.json    # Coleção Postman para testes da API
└── 📝 README.md
```