from config import config
from broker import Broker
from requests import get
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.common.consts import Language
from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.util.order_utils import market_order


class Tiger(Broker):
    # Tiger Broker Implementation.

    def __init__(self):
        self._client_config = None
        self.set_config()

    def set_config(self, sandbox=False):
        # Config obtained from https://quant.tigerfintech.com/?locale=en-us#developer
        client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
        client_config.private_key = read_private_key(config['PRIVATE_KEY_PATH'])  # Path to your private key
        client_config.tiger_id = config['TIGER_ID']
        client_config.account = config['TIGER_ACCOUNT']
        client_config.language = Language.en_US
        self._client_config = client_config

    def get_price(self):
        # Yahoo finance used here as Tiger Broker charges for market data.
        # Free data includes pre_close, open, high, low, close, volume
        # Data received here will be delayed.
        query_url = 'https://query2.finance.yahoo.com/v7/finance/quote'
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = get(query_url,
                       params={'symbols': config['SYMBOL']},
                       headers=header)
        return response.json()['quoteResponse']['result'][0]['ask']

    def place_order(self, quantity):
        # Refer to Tiger API - https://quant.itiger.com/openapi/zh/python/operation/trade/placeOrder.html
        trade_client = TradeClient(self._client_config)
        contract = trade_client.get_contract(config['SYMBOL'], currency='USD')
        order = market_order(account=self._client_config.account, contract=contract,
                             action='BUY', quantity=quantity)
        trade_client.place_order(order)
