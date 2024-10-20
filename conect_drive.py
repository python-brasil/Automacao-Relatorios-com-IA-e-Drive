import json
import io
import os

from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Códigos ANSI para cores
MAGENTA = '\033[35m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

#{"installed":{"client_id":"479633533394-6hnom4t53ts0jlcebq0btofqlej7b7su.apps.googleusercontent.com","project_id":"envio-relatorios","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}

credentials_string = 'credentials.json'
scopes = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/documents', 
          'https://www.googleapis.com/auth/drive']

# Abre o arquivo JSON e carrega seu conteúdo em um dicionário
with open(credentials_string, 'r') as arquivo:
    credentials_dict = json.loads(arquivo.read())
# Criar credenciais a partir do dicionário
credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=scopes)
service = build('drive', 'v3', credentials=credentials)


def list_files_folder_drive(folder_id):
    print(f"Iniciando coleta de arquivos no diretorio = {folder_id}")
    # Definir a query para listar arquivos e pastas a partir da pasta raiz
    query = f"'{folder_id}' in parents"

    # Buscar todos os arquivos e pastas no Google Drive com base na query
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    list_files = []
    
    if isinstance(items, list):
        for i, file in enumerate(items):
            file_name = file.get('name', 'Unknown')
            file_id = file.get('id')
            mime_type = file.get('mimeType', 'Unknown')

            print(f"  > INDICE : [{MAGENTA}{i+1}{RESET}]")
            print(f"  > NAME   : [{MAGENTA}{file_name}{RESET}]")
            print(f"  > MIME   : [{MAGENTA}{mime_type}{RESET}]")

            # Verifica se o item é um arquivo, não uma pasta
            if mime_type != 'application/vnd.google-apps.folder':
                # Criar a requisição para baixar o arquivo
                request = service.files().get_media(fileId=file_id)
                fh = io.BytesIO()  # Cria um arquivo em memória para armazenar o download

                # Configurar o MediaIoBaseDownload para lidar com o download do arquivo
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"  Downloading    :  [{GREEN}Progress: {int(status.progress() * 100)}%{RESET}]")

                # Salvar o conteúdo do arquivo localmente
                local_folder_path = "files"  # Caminho onde o arquivo será salvo localmente
                
                if not os.path.exists(local_folder_path):
                    os.makedirs(local_folder_path)
                
                local_file_path = os.path.join(local_folder_path, file_name)
                
                with open(local_file_path, 'wb') as f:
                    f.write(fh.getvalue())

                print(f"  Downloading    :  [{GREEN}OK{RESET}]")
                
                file_dict = {
                    file_name: file_id
                }
                
                list_files.append(file_dict)
            else:
                print(f"  > TIPO : [{YELLOW}Pasta, ignorado{RESET}]")

            print("-" * 10)
    return list_files

def upload_file_to_drive(folder_id, file_path):
    print(f"Iniciando movimentação do arquivo {file_path} para a pasta {folder_id}")
    file_path = os.path.join("files", file_path)
    
    # Verificar se o arquivo existe
    if not os.path.exists(file_path):
        print(f"{RED}Erro: O arquivo '{file_path}' não foi encontrado.{RESET}")
        return

    # Pega o nome do arquivo do caminho fornecido
    file_name = os.path.basename(file_path)
    
    # Cria os metadados do arquivo para o Google Drive
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]  # Define a pasta onde o arquivo será salvo
    }

    # Cria o MediaFileUpload para fazer o upload do arquivo para o Google Drive
    media = MediaFileUpload(file_path, resumable=True)

    # Faz a requisição para criar o arquivo no Google Drive
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()

    # Mensagem de confirmação
    print(f"{GREEN}Upload concluído: '{file.get('name')}' com ID '{file.get('id')}'{RESET}")
    
    
def delete_file_from_drive(folder_id, file_id):
    try:
        # Buscar informações sobre o arquivo, incluindo donos e permissões
        file_info = service.files().get(fileId=file_id, fields="id, name, owners, permissions").execute()
        owners = file_info.get('owners', [])
        
        # Verificar se a conta de serviço é dona ou tem permissão para deletar
        possui_permissao = any(owner.get('emailAddress') == 'your-service-account-email@project-name.iam.gserviceaccount.com' for owner in owners)

        if not possui_permissao:
            print(f"{RED}Erro: A conta de serviço não tem permissão para deletar o arquivo '{file_info.get('name')}'.{RESET}")
            return

        # Realizar a requisição para deletar o arquivo
        service.files().delete(fileId=file_id).execute()
        print(f"{GREEN}Arquivo com ID '{file_id}' deletado com sucesso.{RESET}")

    except Exception as e:
        print(f"{RED}Erro ao tentar deletar o arquivo com ID '{file_id}': {str(e)}{RESET}")


    except Exception as e:
        print(f"{RED}Erro ao tentar deletar o arquivo com ID '{file_id}': {str(e)}{RESET}")

def move_file_between_folders(file_id, folder_id_origem, folder_id_destino):
    try:
        # Primeiro, busque as informações sobre o arquivo, incluindo as pastas atuais
        file_info = service.files().get(fileId=file_id, fields="parents").execute()
        parents = file_info.get('parents', [])

        # Garantir que a pasta de origem esteja correta antes de tentar mover
        if folder_id_origem not in parents:
            print(f"{YELLOW}A pasta de origem fornecida não corresponde às pastas atuais do arquivo.{RESET}")
            return

        # Atualizar o campo 'parents' do arquivo, removendo da pasta de origem e adicionando à pasta destino
        updated_file = service.files().update(
            fileId=file_id,
            addParents=folder_id_destino,
            removeParents=folder_id_origem,
            fields='id, parents'
        ).execute()

        print(f"{GREEN}Arquivo com ID '{file_id}' movido da pasta '{folder_id_origem}' para a pasta '{folder_id_destino}' com sucesso.{RESET}")

    except Exception as e:
        print(f"{RED}Erro ao tentar mover o arquivo com ID '{file_id}': {str(e)}{RESET}")


def delete_file_by_name(file_name):
    try:
        path_file = os.path.join("files", file_name)
        os.remove(path_file)

        print(f"{GREEN}Arquivo '{file_name}'{RESET}")

    except Exception as e:
        print(f"{RED}Erro ao tentar deletar o arquivo '{file_name}': {str(e)}{RESET}")


