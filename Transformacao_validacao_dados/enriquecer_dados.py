import pandas as pd
import zipfile
from pathlib import Path
from cnpj_utils import validar_cnpj, limpar_cnpj

CONSOLIDADO = "../data/consolidado_despesas.csv"
CADOP = "../data/relatorio_cadop.csv"
OUTPUT_DIR = "../data/"


def carregar_dados():
    df_despesas = pd.read_csv(CONSOLIDADO, sep=";", encoding="utf-8-sig", low_memory=False)
    df_cadop = pd.read_csv(CADOP, sep=";", encoding="utf-8", low_memory=False)
    return df_despesas, df_cadop


def enriquecer_dados(df_despesas, df_cadop):
    df_despesas["REG_ANS"] = pd.to_numeric(df_despesas["REG_ANS"], errors="coerce")
    df_cadop["REGISTRO_OPERADORA"] = pd.to_numeric(df_cadop["REGISTRO_OPERADORA"], errors="coerce")

    colunas_cadop = ["REGISTRO_OPERADORA", "CNPJ", "Razao_Social", "Modalidade", "UF"]
    df_cadop_sel = df_cadop[colunas_cadop].copy()
    
    duplicatas_cadop = df_cadop_sel[df_cadop_sel.duplicated(subset=["REGISTRO_OPERADORA"], keep="first")]
    if len(duplicatas_cadop) > 0:
        print(f"    [AVISO] {len(duplicatas_cadop)} registros duplicados no CADOP (mantendo primeiro)")
    df_cadop_sel = df_cadop_sel.drop_duplicates(subset=["REGISTRO_OPERADORA"], keep="first")
    
    df_enriquecido = pd.merge(
        df_despesas,
        df_cadop_sel,
        left_on="REG_ANS",
        right_on="REGISTRO_OPERADORA",
        how="left"
    )
    
    # Contabilizar matches
    sem_match = df_enriquecido["REGISTRO_OPERADORA"].isna().sum()
    com_match = len(df_enriquecido) - sem_match
    print(f"    Registros com match: {com_match}")
    print(f"    Registros sem match no CADOP: {sem_match} (mantidos com dados vazios)")
    
    return df_enriquecido


def validar_dados(df: pd.DataFrame):
    relatorio = {
        "total": len(df),
        "cnpj_invalido": 0,
        "cnpj_ausente": 0,
        "valor_negativo": 0,
        "razao_social_vazia": 0
    }
    
    # Validar CNPJ
    df["CNPJ_VALIDO"] = df["CNPJ"].apply(lambda x: validar_cnpj(x) if pd.notna(x) else False)
    relatorio["cnpj_invalido"] = (~df["CNPJ_VALIDO"] & df["CNPJ"].notna()).sum()
    relatorio["cnpj_ausente"] = df["CNPJ"].isna().sum()
    
    print(f"    CNPJs invalidos: {relatorio['cnpj_invalido']} (MANTIDOS e MARCADOS)")
    print(f"    CNPJs ausentes: {relatorio['cnpj_ausente']} (sem match no CADOP)")
    

    for col in ["VL_SALDO_INICIAL", "VL_SALDO_FINAL"]:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)
    
    relatorio["valor_negativo"] = (df["VL_SALDO_FINAL"] < 0).sum()
    relatorio["razao_social_vazia"] = (df["Razao_Social"].isna() | (df["Razao_Social"] == "")).sum()
    
    return df, relatorio



def agregar_dados(df : pd.DataFrame):
    df["ValorDespesas"] = df["VL_SALDO_FINAL"]

    df["CNPJ"] = df["CNPJ"].apply(limpar_cnpj)
    
    
    df_valido = df[df["Razao_Social"].notna() & (df["Razao_Social"] != "")].copy()
    print(f"    Registros validos para agregacao: {len(df_valido)}")
    
    # Agrupar por RazaoSocial, UF, Trimestre e Ano
    df_agregado = df_valido.groupby(["Razao_Social", "UF", "REG_ANS", "CNPJ", "Modalidade", "Trimestre", "Ano"]).agg(
        TotalDespesas=("ValorDespesas", "sum"),
        MediaTrimestral=("ValorDespesas", "mean")
    ).reset_index()
    
    df_agregado = df_agregado.sort_values("TotalDespesas", ascending=False)
    
    df_agregado = df_agregado.rename(columns={
        "Razao_Social": "Razao_Social",
        "REG_ANS": "REGISTRO_ANS",
        "TotalDespesas": "Total_Despesas",
        "MediaTrimestral": "Media_Trimestral"
    })
    
    print(f"    Total de operadoras agregadas: {len(df_agregado)}")
    
    return df_agregado


def salvar_resultado(df, nome_arquivo="despesas_agregadas.csv"):    
    csv_path = Path(OUTPUT_DIR) / nome_arquivo
    zip_path = Path(OUTPUT_DIR) / "Teste_Antonio.zip"
    
    colunas_finais = ["Razao_Social", "UF", "REGISTRO_ANS", "CNPJ", "Modalidade", 
                      "Trimestre", "Ano", "Total_Despesas", "Media_Trimestral"]
    df_final = df[colunas_finais]
    
    df_final.to_csv(csv_path, index=False, sep=";", encoding="utf-8-sig", decimal=".")
    print(f"    CSV salvo: {csv_path} ({len(df_final)} registros)")
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname=nome_arquivo)
    print(f"    ZIP criado: {zip_path}")


def main():
    df_despesas, df_cadop = carregar_dados()
    df_enriquecido = enriquecer_dados(df_despesas, df_cadop)
    df_validado, _ = validar_dados(df_enriquecido)
    df_agregado = agregar_dados(df_validado)
    salvar_resultado(df_agregado)


if __name__ == '__main__':
    main()