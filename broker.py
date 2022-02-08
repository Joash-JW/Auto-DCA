from config import config
from abc import ABC, abstractmethod
from datetime import datetime
from os import getcwd, makedirs
from os.path import exists


class Broker(ABC):
    # abstract class

    def __init__(self):
        self._ask_price = None

    # getter for class name
    @property
    def name(self):
        return self.__class__.__name__

    @property
    def ask_price(self):
        return self._ask_price

    @ask_price.setter
    def ask_price(self, ask_price):
        assert ask_price > 0
        assert type(ask_price) is float
        self._ask_price = ask_price

    # methods for subclasses to implement
    @abstractmethod
    def get_price(self): raise NotImplementedError

    def calculate_qty(self, price: float) -> int:
        return config['ALLOCATION']//price

    @abstractmethod
    def place_order(self, quantity: int): raise NotImplementedError

    def do_dca(self):
        self._ask_price = self.get_price()
        quantity = self.calculate_qty(self._ask_price)
        self.place_order(quantity)
        message = "{broker} Broker - Placed order for {symbol}, {quantity}@{price}".format(
            broker=self.name, symbol=config['SYMBOL'], quantity=quantity, price=self.ask_price
        )
        self.log_order(message)
        print(message)

    def log_order(self, message):
        now = datetime.now()
        folder_path = getcwd().replace('\\', '/')+'/logs'
        if not exists(folder_path):
            makedirs(folder_path)
        with open('logs/' + str(now.date()) + '-order-log.txt', 'a') as file_object:
            file_object.write(now.strftime("%Y-%m-%d %H:%M:%S") + ' -- ' + message + '\n')
