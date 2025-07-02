import logging
import os
from logging import Logger

def setup_logger(log_dir: str, log_level=logging.INFO) -> Logger:
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "calculator.log")

    logger = logging.getLogger("CalculatorApp")
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger