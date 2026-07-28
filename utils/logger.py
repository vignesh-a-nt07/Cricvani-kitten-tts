import logging
from logging.handlers import RotatingFileHandler
from config import settings
import os

def setup_logger():
    logger = logging.getLogger("kitten_tts_server")
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Rotating file handler (10 MB per file, keep 5 backups)
    log_file = os.path.join("logs", "server.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
