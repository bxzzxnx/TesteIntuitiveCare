import requests
import re
import os
from bs4 import BeautifulSoup


BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
OUTPUT_DIR = "../data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def baixar_dados():
    anos = []
    links = []
    trimestre_links = []

    resposta = requests.get(BASE_URL)
    if(resposta.status_code != 200):
        return
    soup = BeautifulSoup(resposta.text, "html.parser")
    anchors = soup.find_all("a")
 
    for a in anchors:
        href = a.get("href")
        if href:
            links.append(href)

    for link in links:
        if re.match(r"^\d{4}/$", link):
            anos.append(link)
    anos = sorted(anos, reverse=True)
    
    if not anos:
        print("Nenhum ano encontrado")
        return
    ano_mais_recente = anos[0] # gambiarra ??
    ano_url = f"{BASE_URL}{ano_mais_recente}"
    

    resposta_ano = requests.get(ano_url)
    if resposta_ano.status_code == 200:
        soup_ano = BeautifulSoup(resposta_ano.text, "html.parser")
    links = soup_ano.find_all('a')
    for link in links:
        href = link.get('href','')
        if any(t in href.upper() for t in ['1T', '2T', '3T', '4T']):
            trimestre_links.append(href)

    if trimestre_links:
        ultimos_trimestres = trimestre_links[-3:]
        for trimestre in ultimos_trimestres:
            url = f"{ano_url}{trimestre}"
            resposta = requests.get(url)
            if resposta.status_code == 200:
                nome_arquivo = f"{OUTPUT_DIR}/{trimestre}"
                with open(nome_arquivo, 'wb') as f:
                    f.write(resposta.content)
            else:
                print(f"Erro ao baixar: {resposta.status_code}")

if __name__ == '__main__':
    baixar_dados()