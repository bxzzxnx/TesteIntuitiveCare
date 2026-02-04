import requests

URL = 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv'
OUTPUT_DIR = "../data/"
FILE = 'relatorio_cadop.csv'

def main():
    response = requests.get(URL)
    if(response.status_code == 200):
        with open(OUTPUT_DIR + FILE, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Erro ao baixar: {response.status_code}")


if __name__ == '__main__':
    main()