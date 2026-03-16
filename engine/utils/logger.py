
import logging

logging.basicConfig(
    filename="logs/trades.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

def log(message):
    logging.info(message)
