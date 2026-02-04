import re, pandas as pd 

def validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'[^0-9]', '', str(cnpj))
    
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    
    soma = sum(int(cnpj[i]) * (5 - i if i < 4 else 13 - i) for i in range(12))
    d1 = 11 - (soma % 11)
    d1 = 0 if d1 >= 10 else d1
    
    soma = sum(int(cnpj[i]) * (6 - i if i < 5 else 14 - i) for i in range(13))
    d2 = 11 - (soma % 11)
    d2 = 0 if d2 >= 10 else d2
    
    return cnpj[-2:] == f"{d1}{d2}"

def limpar_cnpj(x):
    if pd.notna(x) and str(x).replace('.', '').replace('-', '').isdigit():
        return str(int(x))
    else:
        return x