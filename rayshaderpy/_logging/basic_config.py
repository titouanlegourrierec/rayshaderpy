import logging
import os
from logging.handlers import RotatingFileHandler

# logs configuration
log_dir = os.path.expanduser("~/py-rayshader-logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "py-rayshader.log")

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=1),
    ],
)
