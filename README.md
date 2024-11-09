# SteamDB Sales Scraper

Este projeto é um scraper de dados de promoções de jogos da Steam, utilizando a página do [SteamDB](https://steamdb.info/sales/) para coletar informações sobre descontos, preços, avaliações e outras informações das promoções em andamento. Os dados extraídos são processados, transformados e carregados em um banco de dados do Google BigQuery, além de serem exportados para o Google Sheets.

## Funcionalidades

- **Extração de Dados**: Coleta informações sobre promoções de jogos, incluindo nome, preço com desconto, percentagem de desconto, avaliação, data de lançamento e mais.
- **Transformação de Dados**: Os dados extraídos são limpos e transformados para se adequar à estrutura do BigQuery e do Google Sheets.
- **Carregamento no BigQuery**: Os dados transformados são carregados em uma tabela no Google BigQuery.
- **Exportação para o Google Sheets**: Após o carregamento no BigQuery, os dados são exportados para uma planilha do Google Sheets.

## Tecnologias Utilizadas

- **Python 3.x**
- **Selenium**: Para navegar e extrair dados da página do SteamDB.
- **BeautifulSoup**: Para fazer parsing do HTML da página.
- **Google BigQuery**: Para armazenar os dados extraídos e transformados.
- **Google Sheets API**: Para exportar os dados para uma planilha do Google Sheets.
- **Dotenv**: Para carregar variáveis de ambiente a partir de um arquivo `.env`.

## Como Rodar

### 1. Clonando o Repositório

Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/jocianoperin/steamdb-sales-scraper.git
cd steamdb-sales-scraper
```

### 2. Configuração do Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows use .venv\Scripts\activate
```

### 3. Instalação de Dependências

Instale as dependências necessárias com o pip:

```bash
pip install -r requirements.txt
```

### 4. Configuração das Credenciais do Google

Para interagir com o Google BigQuery e o Google Sheets, você precisará configurar credenciais de autenticação.

- Crie um projeto no Google Cloud Console.
- Ative as APIs do BigQuery e do Google Sheets para o seu projeto.
- Crie uma chave de autenticação do serviço (arquivo JSON) e faça o download.
- Salve o arquivo JSON da chave em um diretório de sua escolha e adicione o caminho no arquivo .env na variável GOOGLE_APPLICATION_CREDENTIALS.

### 5. Configuração do Arquivo .env

Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

```bash
# Caminho para o arquivo JSON de credenciais do Google
GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/seu/arquivo-de-credenciais.json

# ID do dataset e da tabela no BigQuery
DATASET_ID=steamdb_sales_scraper
TABLE_ID=steamdb_sales_data.sales

# ID da planilha no Google Sheets e o nome da faixa
SPREADSHEET_ID=seu_id_da_planilha
SHEET_RANGE=sua_faixa_da_planilha
```

### 6. Rodando o Scraper

Com as configurações acima concluídas, execute o pipeline para iniciar a extração, transformação e carregamento dos dados:

```bash
python src/main.py
```
O pipeline realiza as seguintes etapas:

- **Extração**: Coleta os dados da página do SteamDB.
- **Transformação**: Limpa e estrutura os dados para o BigQuery e Google Sheets.
- **Carregamento no BigQuery**: Carrega os dados transformados no Google BigQuery.
- **Exportação para o Google Sheets**: Exporta os dados carregados no BigQuery para uma planilha do Google Sheets.


### Contribuição

Sinta-se à vontade para contribuir com este projeto, seja reportando problemas, sugerindo melhorias ou enviando pull requests.

### Contribuições Futuras

Aqui estão algumas ideias de melhorias para versões futuras:

- **Ler todos os dados da planilha**: Atualmente, o projeto lê apenas a primeira página da tabela no Google Sheets. Uma melhoria seria permitir a leitura de todas as páginas disponíveis.
- **Sincronizar em tempo real**: Implementar uma sincronização contínua, onde o pipeline rode automaticamente em intervalos regulares, mantendo os dados sempre atualizados.
