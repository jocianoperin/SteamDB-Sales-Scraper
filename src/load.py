import os
from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account
from utils.logger import logger

# Carrega o arquivo .env
load_dotenv()

# Caminho para o JSON de autenticação
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Carrega as credenciais
credentials = service_account.Credentials.from_service_account_file(credentials_path)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Função para carregar dados para o BigQuery
def load_data_to_bigquery(data, dataset_id, table_id):
    table_ref = f"{dataset_id}.{table_id}"  # Definindo o ID completo da tabela
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("sale_game_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("sale_discount_price", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("sale_discount_percent", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("sale_scraped_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("sale_extra_info", "STRING", mode="REPEATED"),
            bigquery.SchemaField("sale_rating", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("sale_release_date", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("sale_ends_in", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("sale_started_ago", "TIMESTAMP", mode="NULLABLE")
        ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    # Log de início do carregamento
    logger.info("Iniciando o carregamento dos dados para o BigQuery.")
    
    try:
        # Cria a carga de dados
        load_job = client.load_table_from_json(data, table_ref, job_config=job_config)
        load_job.result()  # Espera o término do job
        logger.info(f"Carregamento concluído: {len(data)} registros adicionados à tabela {table_id}.")
    except Exception as e:
        logger.error(f"Erro ao carregar dados para o BigQuery: {e}")
"""
# Exemplo de dados para carregar
data = [
    {
        "sale_game_name": "Pistol Whip",
        "sale_discount_price": 44.49,
        "sale_discount_percent": 50.0,
        "sale_scraped_at": "2024-11-09T09:53:32Z",
        "sale_extra_info": ["Play For Free", "all-time low:R$ 33,24at -30%"],
        "sale_rating": 4.5,
        "sale_release_date": "Nov 2019",
        "sale_ends_in": "2024-11-11T15:00:00Z",
        "sale_started_ago": "2024-11-08T15:01:54Z"
    }
    # Adicione mais registros conforme necessário
]

# Chama a função para carregar os dados
load_data_to_bigquery(data, os.getenv("DATASET_ID"), os.getenv("TABLE_ID"))
"""