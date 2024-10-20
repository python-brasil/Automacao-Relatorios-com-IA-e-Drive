
# Automacao de Relatórios com IA para Envio por Email

Este projeto é uma automação desenvolvida em Python que coleta arquivos de uma pasta do Google Drive, analisa os dados presentes nesses arquivos utilizando IA, e envia um relatório por e-mail com o conteúdo gerado. Todo o processo é realizado automaticamente, facilitando a análise de documentos de maneira rápida e eficiente.

- Assista o Tutorial Completo aqui - [TUTORIAL DO PROJETO](https://youtu.be/N_PnXxLO8Lg)

## Funcionalidades

- **Extração de Arquivos do Google Drive**: Conecta-se ao Google Drive e coleta arquivos armazenados em uma pasta específica.
- **Análise de Arquivos**: Utiliza IA (OpenAI GPT) para analisar o conteúdo dos arquivos coletados e gerar um resumo dos principais pontos e padrões encontrados.
- **Envio de E-mail Automatizado**: Envia os relatórios gerados por e-mail, incluindo o arquivo analisado como anexo.
- **Movimentação dos Arquivos**: Os arquivos processados são movidos para uma pasta de arquivos enviados no Google Drive, mantendo tudo organizado.

## Requisitos

- Python 3.8 ou superior.
- Google Drive API configurada para acessar os arquivos.
- Bibliotecas necessárias:
  - `google-api-python-client`
  - `dotenv`
  - `openai`
  - `smtplib` (padrão do Python)
  - `pandas`

### Instalação das Dependências
Para instalar as bibliotecas necessárias, execute o seguinte comando:
```sh
pip install google-api-python-client python-dotenv openai pandas
```

## Como Rodar o Projeto

1. Clone este repositório em sua máquina local.
2. Crie um arquivo `.env` na raiz do projeto contendo as seguintes chaves:
   ```env
   PASSWORD_EMAIL="SuaSenhaDeEmail"
   OPENAI_KEY="SuaChaveOpenAI"
   ```
3. No terminal, execute o script principal:
   ```sh
   python main.py
   ```

## Estrutura do Código

- **Função `obter_extensao(arquivo_path)`**: Retorna a extensão do arquivo especificado para definir como ele será processado.
- **Função `main()`**: É o ponto de entrada do script, responsável por buscar os arquivos no Google Drive, analisar seu conteúdo, e enviar por email.
- **Classe `EmailSender`**: Gerencia o envio de e-mails, utilizando as credenciais fornecidas no arquivo `.env`.

## Observações

- O sistema utiliza a API do Google Drive para acessar os arquivos, então é necessário configurar as credenciais e permissões para uso da API.
- Cada arquivo é movido para uma pasta específica após o processamento, garantindo que o fluxo dos arquivos seja sempre organizado.

## Possíveis Melhorias Futuras

- **Suporte para Mais Tipos de Arquivos**: Implementar suporte a outros formatos de arquivos para ampliar as possibilidades de análise.
- **Customização do Relatório Gerado**: Permitir que o usuário defina o tipo de análise a ser realizada nos arquivos.
- **Interface Gráfica (GUI)**: Adicionar uma interface gráfica para facilitar a configuração do e-mail, pastas do Google Drive e o tipo de relatório.

## Contribuições

Contribuições são sempre bem-vindas! Se você tiver ideias para melhorias, correções de bugs ou novas funcionalidades, sinta-se à vontade para abrir issues ou enviar pull requests.

## Infos de commits

- :package: novas funcionalidades
- :up: atualizações
- :ant: correções de bug
- :checkered_flag: release

## Nos acompanhe nas redes

- Instagram - [@python_brasil](https://www.instagram.com/python_brasil/)
- LinkedIn - [Comunidade Python Brasil](https://www.linkedin.com/company/comunidade-python-brasil)
