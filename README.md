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
git clone https://github.com/seu_usuario/steamdb-sales-scraper.git
cd steamdb-sales-scraper
