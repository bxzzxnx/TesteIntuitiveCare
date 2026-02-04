WITH despesas_por_trimestre AS (
    SELECT 
        da.REGISTRO_ANS,
        da.Razao_Social,
        da.UF,
        da.Trimestre,
        SUM(da.Total_Despesas) AS Total_Despesas
    FROM despesas_agregadas da
    WHERE da.Ano = 2025
    GROUP BY da.REGISTRO_ANS, da.Razao_Social, da.UF, da.Trimestre
),
primeiro_trimestre AS (
    SELECT REGISTRO_ANS, Razao_Social, UF, Total_Despesas AS Despesas_T1
    FROM despesas_por_trimestre
    WHERE Trimestre = 1
),
ultimo_trimestre AS (
    SELECT REGISTRO_ANS, Total_Despesas AS Despesas_T3
    FROM despesas_por_trimestre
    WHERE Trimestre = 3
)
SELECT 
    pt.Razao_Social,
    pt.UF,
    pt.REGISTRO_ANS,
    pt.Despesas_T1,
    ut.Despesas_T3,
    ROUND(
        ((ut.Despesas_T3 - pt.Despesas_T1) / NULLIF(pt.Despesas_T1, 0)) * 100, 
        2
    ) AS Crescimento_Percentual
FROM primeiro_trimestre pt
INNER JOIN ultimo_trimestre ut ON pt.REGISTRO_ANS = ut.REGISTRO_ANS
WHERE pt.Despesas_T1 > 0
ORDER BY Crescimento_Percentual DESC
LIMIT 5;WITH despesas_por_trimestre AS (
    SELECT 
        da.REGISTRO_ANS,
        da.Razao_Social,
        da.UF,
        da.Trimestre,
        SUM(da.Total_Despesas) AS Total_Despesas
    FROM despesas_agregadas da
    WHERE da.Ano = 2025
    GROUP BY da.REGISTRO_ANS, da.Razao_Social, da.UF, da.Trimestre
),
primeiro_trimestre AS (
    SELECT REGISTRO_ANS, Razao_Social, UF, Total_Despesas AS Despesas_T1
    FROM despesas_por_trimestre
    WHERE Trimestre = 1
),
ultimo_trimestre AS (
    SELECT REGISTRO_ANS, Total_Despesas AS Despesas_T3
    FROM despesas_por_trimestre
    WHERE Trimestre = 3
)
SELECT 
    pt.Razao_Social,
    pt.UF,
    pt.REGISTRO_ANS,
    pt.Despesas_T1,
    ut.Despesas_T3,
    ROUND(
        ((ut.Despesas_T3 - pt.Despesas_T1) / NULLIF(pt.Despesas_T1, 0)) * 100, 
        2
    ) AS Crescimento_Percentual
FROM primeiro_trimestre pt
INNER JOIN ultimo_trimestre ut ON pt.REGISTRO_ANS = ut.REGISTRO_ANS
WHERE pt.Despesas_T1 > 0
ORDER BY Crescimento_Percentual DESC
LIMIT 5;