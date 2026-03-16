import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/vulnhawk.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_event(message, level="info"):
    print(f"[{level.upper()}] {message}")
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    else:
        logging.debug(message)
