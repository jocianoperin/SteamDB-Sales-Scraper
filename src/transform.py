import re
from utils.logger import logger

def clean_game_name_and_extract(game_name):
    # Remove informações adicionais e retorna apenas o nome limpo do jogo
    match = re.match(r"^(.*?)(?:[:：]R\$\s*([\d,.]+)at\s*([-]?\d+)%?)?$", game_name)
    if match:
        name = match.group(1).strip()  # Extrai apenas o nome do jogo
        return name
    return game_name

def transform_data(data):
    logger.info("Transformando os dados extraídos.")
    transformed_data = []

    for entry in data:
        try:
            # Limpa o nome do jogo e processa dados adicionais
            game_name = clean_game_name_and_extract(entry["game_name"])

            # Converte preço com desconto e porcentagem para float
            discount_price = float(entry["discount_price"].replace("R$", "").replace(",", ".").strip())
            discount_percent = float(entry["discount_percent"].replace("%", "").strip())

            # Estrutura os dados transformados
            transformed_entry = {
                "game_name": game_name,
                "discount_price": discount_price,
                "discount_percent": discount_percent,
                "scraped_at": entry["scraped_at"],
                "extra_info": entry["extra_info"],
                "rating": entry["rating"],
                "release_date": entry["release_date"],
                "ends_in": entry["ends_in"],
                "started_ago": entry["started_ago"]
            }
            transformed_data.append(transformed_entry)
        except ValueError as e:
            logger.warning("Erro ao transformar dados do jogo '%s': %s", entry["game_name"], e)

    logger.info("Transformação de dados concluída. Total de jogos transformados: %d", len(transformed_data))
    return transformed_data
