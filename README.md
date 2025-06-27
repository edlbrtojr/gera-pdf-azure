# Gerador de PDF para Power Automate

Aplicação Python integrada ao Microsoft Power Automate para geração de PDFs a partir de dados enviados por um fluxo.

## Funcionalidades

- Recebe dados via requisição HTTP POST do Power Automate
- Gera PDF com os dados recebidos
- Retorna o PDF gerado para o fluxo do Power Automate

## Requisitos

- Python 3.8+
- Biblioteca Flask para API REST
- Biblioteca ReportLab para geração de PDFs

## Configuração Local

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Copie o arquivo `env.sample` para `.env` e ajuste os valores:
   ```
   cp env.sample .env
   ```
4. Execute a aplicação localmente:
   ```
   python app.py
   ```

## Configuração no Azure App Service

1. Faça deploy da aplicação no Azure App Service
2. Configure as seguintes variáveis de ambiente no App Service:
   - `API_KEY`: Chave secreta para autenticação
   - `TEMP_FOLDER`: Pasta para armazenar arquivos temporários (opcional, padrão: 'temp')

## Integração com Power Automate

### Enviar dados para geração de PDF

1. No Power Automate, use a ação "HTTP":
   - Método: POST
   - URL: https://geradordepdf.azurewebsites.net/generate-pdf
   - Cabeçalhos:
     ```
     Content-Type: application/json
     X-API-Key: [sua-chave-api]
     ```
   - Corpo: JSON com os dados para o PDF
     ```json
     {
       "titulo": "Meu Relatório",
       "data": "01/01/2023",
       "cliente": "Nome do Cliente",
       "valor": "R$ 1.000,00"
     }
     ```

2. Na próxima etapa do fluxo, você receberá o arquivo PDF gerado que pode ser:
   - Salvo no SharePoint/OneDrive
   - Enviado por email como anexo
   - Processado de outras formas pelo Power Automate

### Exemplo de Fluxo no Power Automate

1. Trigger (Ex: Quando um item é criado no SharePoint)
2. HTTP - Enviar dados para a API de geração de PDF
3. Criar arquivo - Salvar o PDF retornado
4. Enviar email - Enviar o PDF como anexo

## Verificação de Saúde da Aplicação

- Endpoint: GET https://geradordepdf.azurewebsites.net/health
- Não requer autenticação
- Retorna status da aplicação 