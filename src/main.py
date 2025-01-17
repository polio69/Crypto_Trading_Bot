# src/main.py
import logging
from connectors.binance_spot import BinanceSpotClient
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

    client = BinanceSpotClient(api_key, secret_key, testnet=True)

    # Get and print balances
    try:
        balances = client.get_balances()
        logger.info("Account Balances:")
        for asset, balance in balances.items():
            if float(balance.free) > 0 or float(balance.locked) > 0:
                logger.info(f"{asset}:")
                logger.info(f"  Free: {balance.free}")
                logger.info(f"  Locked: {balance.locked}")
                logger.info(f"  Total: {balance.free + balance.locked}")
    except Exception as e:
        logger.error(f"Error getting balances: {e}")
