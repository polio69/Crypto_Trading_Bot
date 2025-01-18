import pandas as pd
import logging
from connectors.binance_spot import BinanceSpotClient
from src.models import Contract, Candle

logger = logging.getLogger(__name__)


class BinanceDataCollector:
    def __init__(self, client: BinanceSpotClient):

        self.client = client

    def fetch_historical_data(self, contract: Contract, interval: str, start_time=None, end_time=None) -> pd.DataFrame:

        logger.info(f"Fetching historical data for {contract.symbol} at {interval} interval.")

        data = []
        while True:
            candles = self.client.get_historical_candles(contract, interval)
            if not candles:
                logger.warning(f"No data received for {contract.symbol}.")
                break

            for candle in candles:
                data.append((
                    candle.timestamp,
                    candle.open,
                    candle.high,
                    candle.low,
                    candle.close,
                    candle.volume,
                ))

            if not candles or len(candles) < 1000:
                break

        columns = ["timestamp", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame(data, columns=columns)

        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('datetime', inplace=True)

        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        logger.info(f"Successfully fetched {len(df)} rows of data for {contract.symbol} at {interval} interval.")
        return df

    def save_to_csv(self, df: pd.DataFrame, filename: str):

        df.to_csv(filename)
        logger.info(f"Data saved to {filename}")

    def save_to_hdf5(self, df: pd.DataFrame, contract: Contract, hdf5_client):

        data = df.reset_index().to_numpy()
        tuples = [tuple(row) for row in data]
        hdf5_client.write_data(contract, tuples)
        logger.info(f"Data for {contract.symbol} saved to HDF5 storage.")

