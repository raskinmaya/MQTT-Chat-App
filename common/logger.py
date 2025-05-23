import logging
from logging import Logger, Formatter

def get_logger(name: str) -> Logger:
    logger: Logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(Formatter('[%(levelname)s] %(asctime)s - %(name)s - %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger