COPY despesas_agregadas (
    Razao_Social, UF, REGISTRO_ANS, CNPJ, Modalidade,
    Trimestre, Ano, Total_Despesas, Media_Trimestral
)
FROM 'D:\Codigos\Python\TesteIntuitiveCare\data\despesas_agregadas.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);

COPY despesas_consolidadas (
    REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, 
    VL_SALDO_INICIAL, VL_SALDO_FINAL, Trimestre, Ano
)
FROM 'D:\Codigos\Python\TesteIntuitiveCare\data\\consolidado_despesas.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);

COPY dados_operadoras (
    REGISTRO_OPERADORA, CNPJ, Razao_Social, Nome_Fantasia, Modalidade,
    Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP,
    DDD, Telefone, Fax, Endereco_eletronico, Representante,
    Cargo_Representante, Regiao_de_Comercializacao, Data_Registro_ANS
)
FROM 'D:\Codigos\Python\TesteIntuitiveCare\data\relatorio_cadop.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ';',
    ENCODING 'UTF8',
    NULL ''
);