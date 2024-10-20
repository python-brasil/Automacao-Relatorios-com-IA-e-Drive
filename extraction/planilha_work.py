import pandas as pd

def ler_planilha_como_string(caminho_arquivo):
    # Lê os dados da planilha
    df = pd.read_excel(caminho_arquivo, sheet_name=0)  # Pega sempre a primeira aba da planilha

    # Converte todos os valores em strings e os concatena em uma única variável
    conteudo_completo = ""

    for coluna in df.columns:
        for valor in df[coluna]:
            conteudo_completo += str(valor) + ' '

    # Remove espaços extras no final
    conteudo_completo = conteudo_completo.strip()

    return conteudo_completo


