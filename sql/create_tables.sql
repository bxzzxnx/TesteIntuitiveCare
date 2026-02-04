CREATE TABLE IF NOT EXISTS despesas_consolidadas (
    ID SERIAL PRIMARY KEY,
    REG_ANS INT NOT NULL,
    CD_CONTA_CONTABIL VARCHAR(20),
    DESCRICAO VARCHAR(500),
    VL_SALDO_INICIAL DECIMAL(18,2),
    VL_SALDO_FINAL DECIMAL(18,2),
    Trimestre INT,
    Ano INT
);

CREATE INDEX IF NOT EXISTS idx_despesas_reg_ans ON despesas_consolidadas(REG_ANS);
CREATE INDEX IF NOT EXISTS idx_despesas_trimestre_ano ON despesas_consolidadas(Trimestre, Ano);


CREATE TABLE IF NOT EXISTS dados_operadoras (
    ID SERIAL PRIMARY KEY,
    REGISTRO_OPERADORA INT NOT NULL UNIQUE,
    CNPJ VARCHAR(20) NOT NULL,
    Razao_Social VARCHAR(255),
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(20),
    Complemento VARCHAR(100),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(10),
    DDD VARCHAR(5),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(100),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS DATE
);

CREATE INDEX IF NOT EXISTS idx_operadoras_cnpj ON dados_operadoras(CNPJ);
CREATE INDEX IF NOT EXISTS idx_operadoras_uf ON dados_operadoras(UF);


CREATE TABLE IF NOT EXISTS despesas_agregadas (
    ID SERIAL PRIMARY KEY,
    Razao_Social VARCHAR(255) NOT NULL,
    UF CHAR(2),
    REGISTRO_ANS INT NOT NULL,
    CNPJ VARCHAR(20),
    Modalidade VARCHAR(100),
    Trimestre INT NOT NULL,
    Ano INT NOT NULL,
    Total_Despesas DECIMAL(18,2) NOT NULL,
    Media_Trimestral DECIMAL(18,2)
);

CREATE INDEX IF NOT EXISTS idx_agregadas_uf ON despesas_agregadas(UF);
CREATE INDEX IF NOT EXISTS idx_agregadas_trimestre_ano ON despesas_agregadas(Trimestre, Ano);
