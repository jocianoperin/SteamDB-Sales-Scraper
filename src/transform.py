import re
from utils.logger import logger

def clean_game_name_and_extract(game_name):
    # Remove informações adicionais e retorna apenas o nome limpo do jogo
    match = re.match(r"^(.*?)(?:[:：]R\$\s*([\d,.]+)at\s*([-]?\d+)%?)?$", game_name)
    if match:
        name = match.group(1).strip()  # Extrai apenas o nome do jogo
        return name
    return game_name

def convert_rating_to_stars(rating_percentage):
    # Converte rating percentual para uma escala de 0 a 5 e arredonda para 1 casa decimal
    stars = round((rating_percentage / 100) * 5, 1)
    # Remove o ".0" para números inteiros
    return int(stars) if stars.is_integer() else stars

def transform_data(data):
    logger.info("Transformando os dados extraídos.")
    transformed_data = []

    for entry in data:
        try:
            # Limpa o nome do jogo e processa dados adicionais
            game_name = clean_game_name_and_extract(entry["game_name"])

            # Converte preço com desconto para float
            discount_price = float(entry["discount_price"].replace("R$", "").replace(",", ".").strip())

            # Remove o símbolo "%" do desconto e converte para valor positivo
            discount_percent = abs(float(entry["discount_percent"].replace("%", "").strip()))

            # Remove o símbolo "%" do rating e converte para uma escala de estrelas (0 a 5)
            rating_percentage = float(entry["rating"].replace("%", "").strip())
            rating_stars = convert_rating_to_stars(rating_percentage)

            # Estrutura os dados transformados
            transformed_entry = {
                "game_name": game_name,
                "discount_price": discount_price,
                "discount_percent": discount_percent,
                "scraped_at": entry["scraped_at"],
                "extra_info": entry["extra_info"],
                "rating": rating_stars,
                "release_date": entry["release_date"],
                "ends_in": entry["ends_in"],
                "started_ago": entry["started_ago"]
            }
            transformed_data.append(transformed_entry)
        except ValueError as e:
            logger.warning("Erro ao transformar dados do jogo '%s': %s", entry["game_name"], e)

    logger.info("Transformação de dados concluída. Total de jogos transformados: %d", len(transformed_data))
    return transformed_data
