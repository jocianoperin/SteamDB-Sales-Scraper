import json
import os
from utils.logger import logger
from extract import extract_data
from transform import transform_data
from google.cloud import bigquery

def main():
    logger.info("Iniciando o pipeline de dados SteamDB Sales Scraper.")
    
    # Cria a pasta 'data' dentro de 'src' se não existir
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    try:
        logger.debug("Iniciando a extração dos dados.")
        data = extract_data()
        
        if data:
            # Salva os dados extraídos em data/extracted_data.json
            extracted_path = os.path.join(data_dir, "extracted_data.json")
            with open(extracted_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info("Dados extraídos salvos em data/extracted_data.json.")

            logger.debug("Transformando os dados extraídos.")
            transformed_data = transform_data(data)

            # Salva os dados transformados em data/transformed_data.json
            transformed_path = os.path.join(data_dir, "transformed_data.json")
            with open(transformed_path, "w", encoding="utf-8") as f:
                json.dump(transformed_data, f, ensure_ascii=False, indent=4)
            logger.info("Dados transformados salvos em data/transformed_data.json.")

            logger.debug("Carregando os dados no BigQuery.")
            # Aqui chamaremos a função de carga no BigQuery
            # load_data(transformed_data)

            logger.info("Pipeline concluído com sucesso.")
        else:
            logger.warning("Nenhum dado foi extraído, encerrando o pipeline.")

    except Exception as e:
        logger.error("Erro no pipeline: %s", e)

if __name__ == "__main__":
    main()
