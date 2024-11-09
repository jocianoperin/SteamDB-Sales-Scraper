from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import time
import os
from utils.logger import logger
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

# Obtém o caminho do ChromeDriver a partir do .env
chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
os.chmod(chromedriver_path, 0o755)

def extract_data():
    logger.info("Extraindo dados do SteamDB.")

    # Configurando o Chrome com Selenium
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")  # Remova para visualizar a execução no navegador

    # Inicia o serviço do ChromeDriver com o caminho definido
    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.set_page_load_timeout(60)  # Define timeout para carregamento da página

        # Acessando a página da SteamDB
        url = "https://steamdb.info/sales/"
        logger.debug("Abrindo URL: %s", url)
        driver.get(url)

        # Espera até que a tabela com id correto esteja carregada
        logger.debug("Aguardando o carregamento da tabela de vendas.")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#DataTables_Table_0"))
        )
        logger.debug("Tabela carregada com sucesso.")

        # Extrai o conteúdo da página e parseia com BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        logger.debug("Página analisada com BeautifulSoup.")
        
        # Extrai as linhas da tabela de promoções usando o id atualizado
        data = []
        for row in soup.select("table#DataTables_Table_0 tr.app"):
            columns = row.select("td")
            if len(columns) > 7:
                # Extrai apenas o texto do link <a>, que é o nome do jogo
                game_name = columns[2].find("a").get_text(strip=True)
                
                discount_percent = columns[3].get_text(strip=True)
                discount_price = columns[4].get_text(strip=True)
                rating = columns[5].get_text(strip=True)  # Captura a coluna Rating
                release_date = columns[6].get_text(strip=True)  # Captura a coluna Release

                # Captura os valores `data-sort` e converte para data no horário do Brasil
                ends_in_timestamp = columns[7].get("data-sort", None)
                started_ago_timestamp = columns[8].get("data-sort", None)

                # Converte timestamps para datetime com timezone UTC e ajusta para o horário do Brasil (UTC-3)
                ends_in = (
                    datetime.fromtimestamp(int(ends_in_timestamp), tz=timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M:%S')
                    if ends_in_timestamp else ""
                )
                started_ago = (
                    datetime.fromtimestamp(int(started_ago_timestamp), tz=timezone.utc).astimezone(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M:%S')
                    if started_ago_timestamp else ""
                )
                
                # Extraindo informações adicionais como tags extras
                extra_info_tags = columns[2].select("div.subinfo span")
                extra_info = [tag.get_text(strip=True) for tag in extra_info_tags]

                game_data = {
                    "game_name": game_name,
                    "discount_percent": discount_percent,
                    "discount_price": discount_price,
                    "rating": rating,
                    "release_date": release_date,
                    "ends_in": ends_in,
                    "started_ago": started_ago,
                    "extra_info": extra_info,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(game_data)
        
        logger.info("Extração de dados concluída. Total de jogos extraídos: %d", len(data))
        return data
    except Exception as e:
        logger.error("Erro durante a extração de dados: %s", e)
        return []
    finally:
        driver.quit()
