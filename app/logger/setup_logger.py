import logging
import os

def setup_logging(level: str = None):
    level = level or os.getenv("LOG_LEVEL", "INFO")
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=fmt)

def get_logger(name: str = None) -> logging.Logger:
    if name is None:
        name = __name__
    logger = logging.getLogger(name)
    return logger