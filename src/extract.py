from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from utils.logger import logger
import os

def extract_data():
    logger.info("Extraindo dados do SteamDB.")

    # Definindo o caminho do ChromeDriver
    chromedriver_path = "/home/jociano/Downloads/chromedriver-linux64/chromedriver"
    os.chmod(chromedriver_path, 0o755)  # Garante permissão de execução

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
            if len(columns) > 4:
                game_name = columns[2].get_text(strip=True)
                discount_percent = columns[3].get_text(strip=True)
                discount_price = columns[4].get_text(strip=True)
                
                game_data = {
                    "game_name": game_name,
                    "discount_percent": discount_percent,
                    "discount_price": discount_price,
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
