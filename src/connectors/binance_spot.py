import logging
import requests
import time
from typing import *
from urllib.parse import urlencode
import hmac
import hashlib
import websocket
import threading

from ..models import Contract


logger = logging.getLogger()

class BinanceSpotClient:
    def __init__(self, public_key: str, secret_key: str, testnet: bool):

        self._public_key = public_key
        self._secret_key = secret_key

        self._base_url = "https://api.binance.com"
        self._wss_url = "wss://testnet.binance.vision/ws-api/v3"

        self._headers = {'X-MBX-APIKEY': self._public_key}

        self.contracts = self.get_contracts()
        self.balances = self.get_balances()

        self.prices = dict()

        self.logs = []

        self._ws_id = 1
        self._ws = None

        t = threading.Thread(target=self._start_ws)
        t.start()

        logger.info("Binance Futures Client successfully initialized")

    def _add_log(self, msg: str):
        logger.info("%s", msg)
        self.logs.append({"log": msg, "displayed": False})

    def _generate_signature(self, data: Dict) -> str:
        return hmac.new(self._secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def _make_request(self, method: str, endpoint: str, data: Dict):
        if method == "GET":
            try:
                response = requests.get(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "POST":
            try:
                response = requests.post(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None

        elif method == "DELETE":
            try:
                response = requests.delete(self._base_url + endpoint, params=data, headers=self._headers)
            except Exception as e:
                logger.error("Connection error while making %s request to %s: %s", method, endpoint, e)
                return None
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making %s request to %s: %s (error code %s)",
                         method, endpoint, response.json(), response.status_code)
            return None

    def get_contracts(self) -> Dict[str, Contract]:
        exchange_info = self._make_request("GET", "/fapi/v1/exchangeInfo", dict())

        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['symbol']] = Contract(contract_data, "binance")

        return contracts