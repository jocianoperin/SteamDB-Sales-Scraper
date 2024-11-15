import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from utils.logger import logger
from datetime import datetime 

# Carrega o arquivo .env
load_dotenv()

# Caminho para o JSON de autenticação
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Carrega as credenciais para o Google Sheets API
credentials = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build("sheets", "v4", credentials=credentials)

# Função para exportar dados para o Google Sheets
def export_data_to_google_sheets(data, spreadsheet_id, range_name):
    # Convertendo datetime para string
    for entry in data:
        if isinstance(entry.get("sale_scraped_at"), datetime):
            entry["sale_scraped_at"] = entry["sale_scraped_at"].strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(entry.get("sale_ends_in"), datetime):
            entry["sale_ends_in"] = entry["sale_ends_in"].strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(entry.get("sale_started_ago"), datetime):
            entry["sale_started_ago"] = entry["sale_started_ago"].strftime('%Y-%m-%d %H:%M:%S')

    # Carregar os dados existentes na planilha para verificar duplicações
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    existing_data = result.get('values', [])

    # Lista para armazenar os dados que ainda não existem na planilha
    new_data = []
    for entry in data:
        game_name = entry["sale_game_name"]
        exists = any(existing_entry[0] == game_name for existing_entry in existing_data)
        if not exists:
            # Se o jogo não existe na planilha, adiciona à lista de novos dados
            new_data.append([
                entry["sale_game_name"],
                entry["sale_discount_price"],
                entry["sale_discount_percent"],
                entry["sale_scraped_at"],
                ", ".join(entry["sale_extra_info"]),
                entry["sale_rating"],
                entry["sale_release_date"],
                entry["sale_ends_in"],
                entry["sale_started_ago"]
            ])

    # Se houver novos dados, exporta para o Google Sheets
    if new_data:
        body = {"values": new_data}
        try:
            result = sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            logger.info(f"{result.get('updatedCells')} células atualizadas no Google Sheets.")
        except Exception as e:
            logger.error(f"Erro ao exportar dados para o Google Sheets: {e}")
    else:
        logger.info("Nenhum dado novo para exportar para o Google Sheets.")
