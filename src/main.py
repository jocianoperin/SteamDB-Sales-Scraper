import json
from utils.logger import logger
from extract import extract_data
from transform import transform_data

def main():
    logger.info("Iniciando o pipeline de dados SteamDB Sales Scraper.")
    
    try:
        logger.debug("Iniciando a extração dos dados.")
        data = extract_data()
        
        if data:
            # Salva os dados extraídos em um arquivo JSON para análise
            with open("extracted_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info("Dados extraídos salvos em extracted_data.json.")

            logger.debug("Transformando os dados extraídos.")
            transformed_data = transform_data(data)

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
