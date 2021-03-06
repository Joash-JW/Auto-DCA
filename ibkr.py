from config import config
from broker import Broker
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import MarketDataTypeEnum
from ibapi.ticktype import TickTypeEnum
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Thread


class IBKR(EWrapper, EClient, Broker):
    # IBKR class would need to override methods in EWrapper, EClient and implement Broker.

    def __init__(self):
        EClient.__init__(self, self)
        self._ibkr_thread = None
        self._market_data_type = MarketDataTypeEnum.DELAYED  # Use "REALTIME" if you have market data subscription
        self.next_order_id = None

    def set_connection(self):
        # Make connection to Interactive Brokers TWS/IB Gateway.
        self.connect(config['IBKR_URL'], port=config['IBKR_PORT'], clientId=config['IBKR_ID'])
        print('IBKR Connected!')

    def stop(self):
        # Stop connection to Interactive Brokers TWS/IB Gateway.
        if self.isConnected():
            print('Disconnecting IBKR...')
            self.disconnect()
        else:
            print("IBKR is not connected!")

    def error(self, reqId, errorCode, errorString):
        # To print out the errors sent by Interactive Brokers TWS/IB Gateway.
        # https://interactivebrokers.github.io/tws-api/interfaceIBApi_1_1EWrapper.html#a0dd0ca408b9ef70181cec1e5ac938039
        print('Error: ', reqId, ' ', errorCode, ' ', errorString)

    def nextValidId(self, orderId:int):
        # This method is needed to prevent duplicate orders.
        super().nextValidId(orderId)
        self.next_order_id = orderId
        print("Next Order ID: " + str(self.next_order_id))

    def get_price(self):
        # Query ask/delayed ask price of the stock.
        self.reqMarketDataType(self._market_data_type)

        contract = Contract()
        contract.symbol = config['SYMBOL']
        contract.secType = 'STK'
        contract.currency = 'USD'
        contract.exchange = 'SMART'
        # https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#a7a19258a3a2087c07c1c57b93f659b63
        self.reqMktData(1, contract, '', False, False, [])

    def tickPrice(self, reqId, tickType, price, attrib):
        # Override tickPrice method, returns the ask price of the stock.
        # https://interactivebrokers.github.io/tws-api/interfaceIBApi_1_1EWrapper.html#ae851ec3a1e0fa2d0964c7779b0c89718
        if tickType == TickTypeEnum.ASK or tickType == TickTypeEnum.DELAYED_ASK:
            self.ask_price = price
            quantity = self.calculate_qty(self.ask_price)
            self.place_order(quantity)  # subsequent step after get_price ends

    def place_order(self, quantity):
        # Wrapper method to place order via Interactive Brokers TWS/IB Gateway.
        contract = Contract()
        contract.symbol = config['SYMBOL']
        contract.secType = 'STK'
        contract.currency = 'USD'
        contract.exchange = 'SMART'

        order = Order()
        order.action = 'BUY'
        order.orderType = 'MKT'
        order.totalQuantity = quantity

        self.placeOrder(self.next_order_id, contract, order)
        message = "{broker} Broker - Placed order for {symbol}, {quantity}@{price}".format(
            broker=self.name, symbol=config['SYMBOL'], quantity=quantity, price=self.ask_price
        )
        self.log_order(message)
        print(message)
        self.stop()

    def do_dca(self):
        # Override Parent method
        self.set_connection()
        self._ibkr_thread = Thread(target=self.run, daemon=True)
        self._ibkr_thread.start()

        # IBKR API runs in an async manner
        # get_price method is the entry point
        # subsequent steps are called within the invoked methods
        self.get_price()
