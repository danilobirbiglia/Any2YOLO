# Logger Setup for Any2YOLO
import logging
from logging.handlers import RotatingFileHandler
import os

# Set up logging
LOG_FILE = "logs/converter.log"

# Automatically delete old log file if it exists
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Create a rotating file handler
file_handler = RotatingFileHandler(
    LOG_FILE, mode='w', maxBytes=5 * 1024 * 1024, backupCount=3  # 5 MB per file, 3 backups
)
file_handler.setLevel(logging.DEBUG)

# Add a console handler for real-time logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define a simplified log format
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(message)s"  # Only log time, level and message
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configure the logger
logger = logging.getLogger("Any2YOLO")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_action(message, level="info"):

    # Log based on the level
    level = level.lower()
    if level == "info":
        logger.info(message)
    elif level == "debug":
        logger.debug(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)
    else:
        logger.info(message)  # Default to info if level is invalid
