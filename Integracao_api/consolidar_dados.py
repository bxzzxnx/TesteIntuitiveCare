import pandas as pd
import zipfile
from pathlib import Path

INPUT_DIR = "../data/extracted"
OUTPUT_DIR = "../data"

def main():
    lista_dfs = []
    
    arquivos = sorted(Path(INPUT_DIR).glob("*.csv"))
    
    for arquivo in arquivos:
        df = pd.read_csv(arquivo, sep=";", encoding="utf-8", low_memory=False)
    
    
        filtro = df["DESCRICAO"].str.contains("EVENTOS|SINISTROS", case=False, na=False)
        df_filtrado = df[filtro].copy()
        
        nome = arquivo.stem
        df_filtrado["Trimestre"] = int(nome[0]) 
        df_filtrado["Ano"] = int(nome[2:])      
        
        lista_dfs.append(df_filtrado)
    
    df_final = pd.concat(lista_dfs, ignore_index=True)
    
    if "DATA" in df_final.columns:
        df_final = df_final.drop(columns=["DATA"])
    

    for col in ["VL_SALDO_INICIAL", "VL_SALDO_FINAL"]:
        if col in df_final.columns:
            df_final[col] = df_final[col].astype(str).str.replace(",", ".", regex=False)
            df_final[col] = pd.to_numeric(df_final[col], errors="coerce").fillna(0)
    
    print(f"\nTotal: {len(df_final)} registros")
    
    csv_path = Path(OUTPUT_DIR) / "consolidado_despesas.csv"
    df_final.to_csv(csv_path, index=False, sep=";", encoding="utf-8-sig", decimal=".")
    print(f"CSV salvo: {csv_path}")

    zip_path = Path(OUTPUT_DIR) / "consolidado_despesas.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(csv_path, arcname="consolidado_despesas.csv")
    print(f"ZIP criado: {zip_path}")


if __name__ == "__main__":
    main()
