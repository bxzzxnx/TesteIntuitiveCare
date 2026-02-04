SELECT 
    COUNT(*) AS Qtd_Operadoras_Acima_Media_2_Trimestres
FROM (
    SELECT REGISTRO_ANS
    FROM despesas_agregadas
    WHERE Ano = 2025
    GROUP BY REGISTRO_ANS
    HAVING SUM(
        CASE WHEN Total_Despesas > (SELECT AVG(Total_Despesas) FROM despesas_agregadas WHERE Ano = 2025) 
        THEN 1 ELSE 0 END
    ) >= 2
) sub;