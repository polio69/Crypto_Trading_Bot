# src/main.py
import logging

from config.config import BINANCE_SPOT_TESTNET  # Import the config dictionary

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == '__main__':
    # Access the API keys from the config dictionary
    api_key = BINANCE_SPOT_TESTNET['api_key']
    secret_key = BINANCE_SPOT_TESTNET['secret_key']

    logger.info("Starting bot with Binance Spot Testnet...")
    # For testing the config is loaded correctly:
    logger.info(f"API Key loaded: {'*' * len(api_key)}")
