import os
import zipfile

OUTPUT_EXTRACTED = "../data/extracted"
OUTPUT_RAW = "../data/raw"

os.makedirs(OUTPUT_EXTRACTED, exist_ok=True)

def main():
    arquivos = os.listdir(OUTPUT_RAW)
    arquivos_zip = [f for f in arquivos if f.endswith('.zip')]
    
    print(f"Arquivos encontrados em {OUTPUT_RAW}:")
    for arquivo in arquivos_zip:
        caminho_zip = os.path.join(OUTPUT_RAW, arquivo)
        print(f"\nExtraindo: {arquivo}")
        
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(OUTPUT_EXTRACTED)
        
if __name__ == '__main__':
    main()