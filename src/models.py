
class Contract:
    def __init__(self, contract_info: dict):
            self.symbol = contract_info['symbol']
            self.base_asset = contract_info['baseAsset']
            self.quote_asset = contract_info['quoteAsset']
            self.price_decimals = contract_info['quoteAssetPrecision']
            self.quantity_decimals = contract_info['baseAssetPrecision']
            self.tick_size = 1 / pow(10, contract_info['quoteAssetPrecision'])
            self.lot_size = 1 / pow(10, contract_info['baseAssetPrecision'])

class Candle:
    def __init__(self, candle_info):
            self.timestamp = candle_info[0]
            self.open = float(candle_info[1])
            self.high = float(candle_info[2])
            self.low = float(candle_info[3])
            self.close = float(candle_info[4])
            self.volume = float(candle_info[5])

class Balance:
    def __init__(self, info):
        self.free = float(info['free'])
        self.locked = float(info['locked'])

