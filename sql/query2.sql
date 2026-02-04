SELECT 
    UF,
    COUNT(DISTINCT REGISTRO_ANS) AS Qtd_Operadoras,
    SUM(Total_Despesas) AS Total_Despesas_UF,
    ROUND(AVG(Total_Despesas), 2) AS Media_Despesas_Por_Operadora,
    ROUND(SUM(Total_Despesas) / NULLIF(COUNT(DISTINCT REGISTRO_ANS), 0), 2) AS Media_Real_Por_Operadora_Unica
FROM despesas_agregadas
WHERE UF IS NOT NULL
GROUP BY UF
ORDER BY Total_Despesas_UF DESC
LIMIT 5;
