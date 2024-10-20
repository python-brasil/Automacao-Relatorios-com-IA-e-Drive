import os
from conect_drive import *
from extraction import planilha_work, pdf_work
from analise_gpt import *

from enviar_email import EmailSender
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
sender_email = "SEU_EMAIL_PARA_ENVIO"
password = os.getenv("PASSWORD_EMAIL")

folder_enviados = "ID_SUA_PASTA_DRIVE"
folder_para_enviar = "ID_SUA_PASTA_DRIVE"

def obter_extensao(arquivo_path):
    # Converte o caminho em um objeto Path, se necessário
    arquivo = Path(f"files/{arquivo_path}")
    
    if arquivo.is_file():
        # Usa o atributo .suffix para pegar a extensão e remove o ponto com [1:]
        extensao = arquivo.suffix[1:]
        if extensao:  # Apenas retorna se houver uma extensão
            return extensao
    return None

def main():

    list_files = list_files_folder_drive(folder_para_enviar)

    for file in list_files:

        for key, value in file.items():
            type_file = obter_extensao(key)
            path_file = f"files/{key}"
            # Usando match-case para diferentes tipos de arquivos
            match type_file.lower():
                case "csv" | "xlsx" | "xls":
                    print(f"Arquivo: {key} é uma planilha compatível com o Pandas.")
                    infos_for_gpt = planilha_work.ler_planilha_como_string(path_file)
                    
                    system_prompt = f"""Você recebeu uma tabela de dados de um arquivo de planilha chamado {key} e seu conteúdo está contida na chave <dados>. 
                    Por favor, crie um resumo dos principais pontos e padrões encontrados na tabela, com base nas informações destacadas em 
                    <dados>
                    {infos_for_gpt}
                    </dados>.
                    """
                case _:
                    print(f"Arquivo: {key} tem uma extensão não categorizada: {type_file}")
                    continue
                
            response_gpt = menager_response(system_prompt)

           
            receiver_email = "matheusgama821@gmail.com"
            title = f"Análise do documento {key}"
            sender = EmailSender(sender_email, password)
            sender.send_mail_with_attachment(response_gpt, title, receiver_email, path_file)

            move_file_between_folders(value, folder_para_enviar, folder_enviados)
            delete_file_by_name(key) 

main()