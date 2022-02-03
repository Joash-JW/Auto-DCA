from config import config
from abc import ABC, abstractmethod
from datetime import datetime
from os import getcwd, makedirs
from os.path import exists


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

    def log_order(self, message):
        now = datetime.now()
        folder_path = getcwd().replace('\\', '/')+'/log'
        if not exists(folder_path):
            makedirs(folder_path)
        with open('log/' + str(now.date()) + '-order-log.txt', 'a') as file_object:
            file_object.write(now.strftime("%Y-%m-%d %H:%M:%S") + ' -- ' + message + '\n')
