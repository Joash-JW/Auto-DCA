from config import config
from abc import ABC, abstractmethod


class Broker(ABC):
    # abstract class

    # getter for class name
    @property
    def name(self):
        return self.__class__.__name__

    # methods for subclasses to implement
    @abstractmethod
    def get_price(self): raise NotImplementedError

    def calculate_qty(self, price: float) -> int:
        return config['ALLOCATION']//price

    @abstractmethod
    def place_order(self): raise NotImplementedError

    @abstractmethod
    def do_dca(self): raise NotImplementedError
