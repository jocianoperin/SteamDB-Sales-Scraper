import logging
import os

# Cria a pasta de logs se não existir
os.makedirs("logs", exist_ok=True)

# Configuração básica do logger
def setup_logger():
    logger = logging.getLogger("steamdb_scraper")
    logger.setLevel(logging.DEBUG)

    # Formato dos logs
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Console handler para saída no terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler para registrar os logs em arquivo
    file_handler = logging.FileHandler("logs/scraper.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Adiciona os handlers ao logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Instância do logger para ser importada nos outros módulos
logger = setup_logger()
