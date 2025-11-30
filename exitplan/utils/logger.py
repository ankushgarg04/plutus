import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from config import LOG_DIR

def setup_logger(name="trading_system", log_level=logging.INFO):
    """
    Sets up a logger with console and file handlers.
    File logs are rotated daily.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers if function is called multiple times
    if logger.hasHandlers():
        return logger

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (Daily Rotation)
    log_file = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30
    )
    file_handler.setLevel(logging.DEBUG) # Capture everything in file
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
