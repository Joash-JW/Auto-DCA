from config import config
from broker import Broker
from requests import get
from futu import OpenUSTradeContext, TrdSide, TrdEnv, OrderType


class MooMoo(Broker):
    # MooMoo Implementation.

    def get_price(self):
        # Yahoo finance used here as MooMoo charges for market data. Data received here will be delayed.
        # query_url = 'https://finance.yahoo.com/quote/'
        query_url = 'https://query2.finance.yahoo.com/v7/finance/quote'
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = get(query_url,
                       params={'symbols': config['SYMBOL']},
                       headers=header)
        return response.json()['quoteResponse']['result'][0]['ask']

    def place_order(self, quantity, ask_price):
        # Create trade object
        trade_context = OpenUSTradeContext(host=config['MOOMOO_IP'], port=config['MOOMOO_PORT'])
        # Remove trd_env for it to trade on your REAL account instead of paper.
        # Market order is not available in paper trading (OrderType.MARKET).
        # Limit order used to demonstrate (OrderType.NORMAL).
        # Change price=0 and order_type=OrderType.MARKET to make it a market order.
        result = trade_context.place_order(
            price=ask_price, qty=quantity, code='US.'+config['SYMBOL'], trd_side=TrdSide.BUY,
            order_type=OrderType.NORMAL, trd_env=TrdEnv.SIMULATE
        )
        # Close trade object
        trade_context.close()

    def do_dca(self):
        ask_price = self.get_price()
        quantity = self.calculate_qty(ask_price)
        self.place_order(quantity, ask_price)
        message = "{broker} Broker - Placed order for {symbol}, {quantity}@{price}".format(
            broker=self.name, symbol=config['SYMBOL'], quantity=quantity, price=ask_price
        )
        self.log_order(message)
        print(message)
